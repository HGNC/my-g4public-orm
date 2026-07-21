"""Integration fixtures for ephemeral MySQL schema-loading tests."""

from __future__ import annotations

from collections.abc import Generator, Iterator
from pathlib import Path

import docker
import pytest
from sqlalchemy import Engine, create_engine
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.mysql import MySqlContainer

MYSQL_START_COMMAND = "--character-set-server=utf8mb4 --collation-server=utf8mb4_bin"


def _iter_sql_statements(sql: str) -> Iterator[str]:
    """Yield executable SQL statements from a schema dump.

    Handles line comments and block comments, and yields statements terminated by
    a semicolon. Raises if the input ends with an unterminated statement.
    """
    in_block_comment = False
    statement_lines: list[str] = []

    for raw_line in sql.splitlines():
        line = raw_line.strip()

        if in_block_comment:
            if "*/" in line:
                in_block_comment = False
            continue

        if not line:
            continue

        if line.startswith("/*"):
            if "*/" not in line:
                in_block_comment = True
            continue

        if line.startswith("--"):
            continue

        statement_lines.append(raw_line)

        if line.endswith(";"):
            statement = "\n".join(statement_lines).strip()
            statement_lines.clear()
            yield statement[:-1].strip()

    if statement_lines:
        raise ValueError("Schema SQL ended with an unterminated statement")


@pytest.fixture(scope="session")
def mysql_container() -> Generator[MySqlContainer]:
    """Start a mysql:8.0 testcontainer for integration tests."""
    try:
        with MySqlContainer(
            "mysql:8.0",
            root_password="test",
            dbname="g4public",
        ).with_command(MYSQL_START_COMMAND) as container:
            yield container
    except (docker.errors.DockerException, ContainerStartException) as exc:
        pytest.skip(f"MySQL container not available: {exc}")


@pytest.fixture(scope="session")
def schema_path() -> Path:
    """Path to the copied Navicat schema dump used by integration tests."""
    return Path(__file__).resolve().parents[2] / "schema" / "g4public.sql"


@pytest.fixture(scope="session")
def schema_sql(schema_path: Path) -> str:
    """The MySQL schema dump used to hydrate ephemeral integration databases."""
    return schema_path.read_text(encoding="utf-8")


def _to_pymysql_url(raw_url: str) -> str:
    """Normalize testcontainers MySQL URLs to a pymysql SQLAlchemy URL."""
    if raw_url.startswith("mysql+pymysql://"):
        return raw_url
    if raw_url.startswith("mysql://"):
        return raw_url.replace("mysql://", "mysql+pymysql://", 1)
    return raw_url


@pytest.fixture(scope="session")
def mysql_url(mysql_container: MySqlContainer) -> str:
    """SQLAlchemy URL for the ephemeral MySQL database."""
    return _to_pymysql_url(mysql_container.get_connection_url())


def _reset_database(engine: Engine) -> None:
    """Drop all tables so the full dump can be replayed idempotently."""
    with engine.begin() as connection:
        connection.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 0")
        table_rows = connection.exec_driver_sql("SHOW TABLES").all()

        for (table_name,) in table_rows:
            escaped = str(table_name).replace("`", "``")
            connection.exec_driver_sql(f"DROP TABLE IF EXISTS `{escaped}`")

        connection.exec_driver_sql("SET FOREIGN_KEY_CHECKS = 1")


def _load_schema(engine: Engine, sql: str) -> None:
    """Execute the schema dump against the ephemeral database (fail-fast)."""
    with engine.begin() as connection:
        for statement in _iter_sql_statements(sql):
            try:
                connection.exec_driver_sql(statement)
            except Exception as exc:  # pragma: no cover - exercised in failures
                head = statement.splitlines()[0][:140]
                raise RuntimeError(
                    f"Failed executing schema statement: {head}"
                ) from exc


@pytest.fixture(scope="function")
def loaded_schema_engine(mysql_url: str, schema_sql: str) -> Generator[Engine]:
    """Create a fresh schema-loaded SQLAlchemy engine for an integration test."""
    engine = create_engine(mysql_url)

    try:
        _reset_database(engine)
        _load_schema(engine, schema_sql)
        yield engine
    finally:
        engine.dispose()
