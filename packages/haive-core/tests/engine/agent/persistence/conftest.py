"""Pytest configuration for Haive persistence tests."""

import logging
import os
from typing import Any, Dict

import pytest

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("pytest_conf")

# Check for PostgreSQL dependencies
try:
    from langgraph.checkpoint.postgres import PostgresSaver
    from psycopg_pool import ConnectionPool

    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False
    logger.warning("PostgreSQL dependencies not available. Some tests will be skipped.")

# Check for pytest-asyncio
try:
    import pytest_asyncio

    ASYNCIO_AVAILABLE = True
except ImportError:
    ASYNCIO_AVAILABLE = False
    logger.warning("pytest-asyncio not available. Async tests will be skipped.")


def pytest_configure(config):
    """Configure pytest for our tests."""
    # Register markers
    config.addinivalue_line("markers", "postgres: mark test as requiring PostgreSQL")
    config.addinivalue_line("markers", "asyncio: mark test as requiring asyncio")


def pytest_collection_modifyitems(config, items):
    """Skip tests based on availability of dependencies."""
    skips = []

    # Skip PostgreSQL tests if dependencies are missing
    if not POSTGRES_AVAILABLE:
        skip_postgres = pytest.mark.skip(reason="PostgreSQL dependencies not available")
        for item in items:
            if "postgres" in item.keywords:
                item.add_marker(skip_postgres)
                skips.append(item.name)

    # Skip asyncio tests if dependencies are missing
    if not ASYNCIO_AVAILABLE:
        skip_asyncio = pytest.mark.skip(reason="pytest-asyncio not available")
        for item in items:
            if "asyncio" in item.keywords:
                item.add_marker(skip_asyncio)
                skips.append(item.name)

    if skips:
        logger.warning(f"Skipping tests: {', '.join(skips)}")


@pytest.fixture(scope="session")
def pg_params() -> dict[str, Any]:
    """Get PostgreSQL connection parameters from environment or defaults."""
    return {
        "db_host": os.environ.get("TEST_POSTGRES_HOST", "localhost"),
        "db_port": int(os.environ.get("TEST_POSTGRES_PORT", "5432")),
        "db_name": os.environ.get("TEST_POSTGRES_DB", "postgres"),
        "db_user": os.environ.get("TEST_POSTGRES_USER", "postgres"),
        "db_pass": os.environ.get("TEST_POSTGRES_PASSWORD", "postgres"),
        "ssl_mode": os.environ.get("TEST_POSTGRES_SSL_MODE", "disable"),
        "use_async": False,
        "setup_needed": True,
    }


@pytest.fixture(scope="session")
def check_postgres_connection(pg_params):
    """Check if PostgreSQL connection works and skip tests if it doesn't."""
    if not POSTGRES_AVAILABLE:
        pytest.skip("PostgreSQL dependencies not available")

    try:
        from psycopg_pool import ConnectionPool

        # Create connection string
        db_uri = f"postgresql://{pg_params['db_user']}:{pg_params['db_pass']}@{pg_params['db_host']}:{pg_params['db_port']}/{pg_params['db_name']}"
        if pg_params["ssl_mode"]:
            db_uri += f"?sslmode={pg_params['ssl_mode']}"

        # Test connection
        with ConnectionPool(db_uri, min_size=1, max_size=1) as pool:
            with pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    assert result[0] == 1

        return True
    except Exception as e:
        logger.exception(f"PostgreSQL connection failed: {e}")
        pytest.skip(f"PostgreSQL connection failed: {e}")
        return False
