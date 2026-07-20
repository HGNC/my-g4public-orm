"""Pytest configuration and fixtures for my-g4public-orm integration tests."""

import pytest


def pytest_configure(config):
    """Configure pytest for integration tests."""
    config.addinivalue_line("markers", "integration: mark test as integration test")