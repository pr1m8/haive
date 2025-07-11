"""Shared test configuration for Supabase integration tests."""

import os
import warnings

from dotenv import load_dotenv
import pytest


# Load environment variables
load_dotenv()

# Suppress prepared statement warnings for tests
warnings.filterwarnings("ignore", message=".*prepared statement.*")

# Skip all tests in this module if no Supabase connection
pytestmark = pytest.mark.skipif(
    not os.getenv("POSTGRES_CONNECTION_STRING"),
    reason="POSTGRES_CONNECTION_STRING not configured - Supabase tests require valid connection string",
)


@pytest.fixture
def supabase_connection_string():
    """Provide Supabase connection string for tests."""
    return os.getenv("POSTGRES_CONNECTION_STRING")


@pytest.fixture
def test_thread_id():
    """Generate unique thread ID for test isolation."""
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return f"test_{timestamp}"


@pytest.fixture
def agent_config(test_thread_id):
    """Standard agent configuration for tests."""
    return {"configurable": {"thread_id": test_thread_id, "recursion_limit": 100}}
