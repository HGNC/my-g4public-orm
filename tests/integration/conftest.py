"""Pytest configuration and fixtures for my-g4public-orm integration tests."""

import os
import pytest
from testcontainers.mysql import MySqlContainer


def pytest_configure(config):
    """Configure pytest for integration tests."""
    config.addinivalue_line("markers", "integration: mark test as integration test")


@pytest.fixture(scope="session")
def mysql_container():
    """Provide a MySQL container for integration tests."""
    # Skip container setup if Docker is not available
    if not os.getenv("DOCKER_AVAILABLE", ""):
        pytest.skip("Docker not available for integration tests")
    
    try:
        with MySqlContainer(
            "mysql:8.0",
            MYSQL_ROOT_PASSWORD="test",
            MYSQL_DATABASE="g4public",
        ).with_command("--character-set-server=utf8mb4 --collation-server=utf8mb4_bin") as mysql:
            yield mysql
    except Exception as e:
        pytest.skip(f"MySQL container not available: {e}")