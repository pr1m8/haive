import pytest

from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

# Import from utils directly (no circular import)
from tests.persistence.utils import get_db_params, setup_test_logging

# Set up logging
logger = setup_test_logging()


@pytest.fixture(scope="module")
def db_params():
    """Get database parameters for testing."""
    params = get_db_params()
    logger.info(
        f"Using DB params: host={params['db_host']}, port={params['db_port']}, db={params['db_name']}"
    )
    return params


@pytest.fixture(scope="function")
def thread_ids():
    """Generate thread IDs for testing."""
    return []


@pytest.fixture(scope="function")
def sync_postgres_config(db_params):
    """Create a synchronous PostgreSQL config."""
    config = PostgresCheckpointerConfig(
        **db_params, mode=CheckpointerMode.SYNC, storage_mode=CheckpointStorageMode.FULL
    )
    logger.info(
        f"Created sync PostgreSQL config with URI: {config.get_connection_uri()}"
    )
    return config


# ... rest of the file remains the same ...


@pytest.fixture(scope="function")
def async_postgres_config(db_params):
    """Create an asynchronous PostgreSQL config."""
    config = PostgresCheckpointerConfig(
        **db_params,
        mode=CheckpointerMode.ASYNC,
        storage_mode=CheckpointStorageMode.FULL,
    )
    logger.info(
        f"Created async PostgreSQL config with URI: {config.get_connection_uri()}"
    )
    return config


@pytest.fixture(scope="function")
def shallow_postgres_config(db_params):
    """Create a shallow PostgreSQL config."""
    config = PostgresCheckpointerConfig(
        **db_params,
        mode=CheckpointerMode.SYNC,
        storage_mode=CheckpointStorageMode.SHALLOW,
    )
    logger.info(
        f"Created shallow PostgreSQL config with URI: {config.get_connection_uri()}"
    )
    return config


@pytest.fixture(scope="function")
def sync_checkpointer(sync_postgres_config):
    """Create a synchronous PostgreSQL checkpointer."""
    checkpointer = sync_postgres_config.create_checkpointer()
    logger.info(f"Created sync checkpointer: {checkpointer}")
    return checkpointer


@pytest.fixture(scope="function")
async def async_checkpointer():
    """Create an asynchronous PostgreSQL checkpointer with proper cleanup."""
    config = PostgresCheckpointerConfig(
        **get_db_params(),
        mode=CheckpointerMode.ASYNC,
        storage_mode=CheckpointStorageMode.FULL,
    )

    # Get the factory
    factory = config.create_async_checkpointer()

    # Use async with to ensure proper cleanup
    async with factory() as checkpointer:
        yield checkpointer
    # Async context manager handles cleanup automatically


@pytest.fixture(scope="function")
def shallow_checkpointer(shallow_postgres_config):
    """Create a shallow PostgreSQL checkpointer."""
    checkpointer = shallow_postgres_config.create_checkpointer()
    logger.info(f"Created shallow checkpointer: {checkpointer}")
    return checkpointer
