"""Minimal conftest for LLM model tests."""

import pytest


@pytest.fixture
def mock_api_key():
    """Provide a mock API key for testing."""
    return "test-api-key-12345"


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Fixture to set environment variables for testing."""

    def _set_env(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setenv(key, value)

    return _set_env
