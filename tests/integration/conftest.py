"""Pytest configuration and fixtures for my-g4public-orm integration tests."""

import docker
import pytest
from testcontainers.core.exceptions import ContainerStartException
from testcontainers.mysql import MySqlContainer


@pytest.fixture(scope="session")
def mysql_container():
    """Provide a MySQL container for integration tests."""
    try:
        # Attempt to start MySQL container with proper charset settings
        with MySqlContainer(
            "mysql:8.0",
            root_password="test",
            dbname="g4public",
        ).with_command("--character-set-server=utf8mb4 --collation-server=utf8mb4_bin") as mysql:
            yield mysql
    except (docker.errors.DockerException, ContainerStartException) as e:
        pytest.skip(f"MySQL container not available: {e}")
    except Exception as e:
        # Re-raise unexpected errors so they don't get masked as "container not available"
        raise e
