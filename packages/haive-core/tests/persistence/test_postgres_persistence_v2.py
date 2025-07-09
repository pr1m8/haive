# tests/core/persistence/test_postgres.py

import json
import logging
import os
import uuid

import pytest

# Configure rich logging
from rich.logging import RichHandler
from rich.traceback import install as install_rich_traceback

# Install rich traceback handler
install_rich_traceback(show_locals=True, width=120, word_wrap=True)

# Configure logging with Rich
logging.basicConfig(
    level=logging.DEBUG,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True, markup=True)],
)

logger = logging.getLogger(__name__)

from haive.core.persistence.handlers import (
    ensure_pool_open,
    register_thread_if_needed,
    setup_checkpointer,
)

# Import the modules
from haive.core.persistence.types import (
    CheckpointMode,
    PostgresCheckpointerConfig,
    SyncMode,
)


# Test fixtures
@pytest.fixture
def test_thread_id():
    """Generate a unique test thread ID."""
    return f"test_thread_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def test_data():
    """Create sample test data for checkpoints."""
    return {
        "messages": [{"role": "human", "content": "Hello, this is a test message"}],
        "metadata": {
            "timestamp": "2023-01-01T00:00:00Z",
            "user_id": "test_user_id",
            "session_id": "test_session_id",
        },
        "state": {"_counter": 1, "_last_updated": "2023-01-01T00:00:00Z"},
    }


@pytest.fixture
def postgres_config():
    """
    Create a standard PostgreSQL checkpointer config.

    Skips tests if PostgreSQL is not available.
    """
    try:
        # Check PostgreSQL dependencies
        import psycopg_pool
        from langgraph.checkpoint.postgres import PostgresSaver

        # Create config
        config = PostgresCheckpointerConfig(
            checkpoint_mode=CheckpointMode.standard,
            sync_mode=SyncMode.sync,
            # Use environment variables or defaults
            db_host=os.environ.get("POSTGRES_HOST", "localhost"),
            db_port=int(os.environ.get("POSTGRES_PORT", "5432")),
            db_name=os.environ.get("POSTGRES_DB", "postgres"),
            db_user=os.environ.get("POSTGRES_USER", "postgres"),
            db_pass=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            ssl_mode="disable",
            setup_needed=True,
        )

        # Test connection
        try:
            config.create_checkpointer()
            return config
        except Exception as e:
            pytest.skip(f"PostgreSQL connection failed: {e}")

    except ImportError:
        pytest.skip("PostgreSQL dependencies not available")


@pytest.fixture
def postgres_shallow_config():
    """
    Create a shallow PostgreSQL checkpointer config.
    """
    try:
        import psycopg_pool
        from langgraph.checkpoint.postgres import ShallowPostgresSaver

        config = PostgresCheckpointerConfig(
            checkpoint_mode=CheckpointMode.shallow,
            sync_mode=SyncMode.sync,
            db_host=os.environ.get("POSTGRES_HOST", "localhost"),
            db_port=int(os.environ.get("POSTGRES_PORT", "5432")),
            db_name=os.environ.get("POSTGRES_DB", "postgres"),
            db_user=os.environ.get("POSTGRES_USER", "postgres"),
            db_pass=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            setup_needed=True,
        )

        try:
            config.create_checkpointer()
            return config
        except Exception as e:
            pytest.skip(f"PostgreSQL shallow connection failed: {e}")

    except ImportError:
        pytest.skip("PostgreSQL dependencies not available")


@pytest.fixture
def postgres_async_config():
    """
    Create an async PostgreSQL checkpointer config.
    """
    try:
        import psycopg_pool

        try:
            from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
        except ImportError:
            pytest.skip("Async PostgreSQL dependencies not available")

        config = PostgresCheckpointerConfig(
            checkpoint_mode=CheckpointMode.standard,
            sync_mode=SyncMode.async_,
            db_host=os.environ.get("POSTGRES_HOST", "localhost"),
            db_port=int(os.environ.get("POSTGRES_PORT", "5432")),
            db_name=os.environ.get("POSTGRES_DB", "postgres"),
            db_user=os.environ.get("POSTGRES_USER", "postgres"),
            db_pass=os.environ.get("POSTGRES_PASSWORD", "postgres"),
            setup_needed=True,
        )

        return config

    except ImportError:
        pytest.skip("PostgreSQL dependencies not available")


class Test_PostgresCheckpointer:
    """Tests for the PostgreSQL checkpointer."""

    def test_create_postgres_checkpointer(self, postgres_config):
        """Test creating a PostgreSQL checkpointer."""
        # Create the checkpointer
        checkpointer = postgres_config.create_checkpointer()

        # Verify it's the right type
        assert checkpointer is not None
        assert "PostgresSaver" in str(type(checkpointer))

        logger.info(f"✅ Created PostgreSQL checkpointer: {type(checkpointer)}")

    def test_postgres_connection_uri(self, postgres_config):
        """Test constructing a connection URI."""
        # Get the connection URI
        uri = postgres_config.get_connection_uri()

        # It should start with postgresql:// and include credentials
        assert uri.startswith("postgresql://")
        assert postgres_config.db_user in uri
        assert postgres_config.db_host in uri
        assert str(postgres_config.db_port) in uri

        # Log redacted URI (hide password)
        safe_uri = uri.replace(postgres_config.db_pass, "****")
        logger.info(f"✅ Created connection URI: {safe_uri}")

    def test_register_thread(self, postgres_config, test_thread_id):
        """Test registering a thread."""
        # Register a thread
        postgres_config.register_thread(test_thread_id, metadata={"test": True})

        # Create checkpointer to verify
        checkpointer = postgres_config.create_checkpointer()

        # Ensure pool is open
        pool = ensure_pool_open(checkpointer)

        # Verify thread exists in database
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM threads WHERE thread_id = %s", (test_thread_id,)
                )
                result = cursor.fetchone()

                assert (
                    result is not None
                ), f"Thread {test_thread_id} not found in database"

        logger.info(f"✅ Thread {test_thread_id} registered successfully")

    def test_put_and_get_checkpoint(self, postgres_config, test_thread_id, test_data):
        """Test storing and retrieving a checkpoint."""
        # Register the thread first
        postgres_config.register_thread(test_thread_id)

        # Create a config with the thread ID
        config = {"configurable": {"thread_id": test_thread_id}}

        # Put a checkpoint
        updated_config = postgres_config.put_checkpoint(config, test_data)

        # Verify the config was updated
        assert "checkpoint_id" in updated_config["configurable"]
        checkpoint_id = updated_config["configurable"]["checkpoint_id"]
        logger.info(f"✅ Created checkpoint with ID: {checkpoint_id}")

        # Get the checkpoint data
        checkpoint = postgres_config.get_checkpoint(updated_config)

        # Verify we got data back
        assert checkpoint is not None
        assert "messages" in checkpoint
        assert len(checkpoint["messages"]) == 1
        assert checkpoint["messages"][0]["content"] == "Hello, this is a test message"
        assert "_counter" in checkpoint["state"]
        assert checkpoint["state"]["_counter"] == 1

        logger.info(f"✅ Retrieved checkpoint data: {json.dumps(checkpoint, indent=2)}")

    def test_get_checkpoint_tuple(self, postgres_config, test_thread_id, test_data):
        """Test retrieving a complete checkpoint tuple."""
        # Register thread
        postgres_config.register_thread(test_thread_id)

        # Create a config with the thread ID
        config = {"configurable": {"thread_id": test_thread_id}}

        # Put a checkpoint
        updated_config = postgres_config.put_checkpoint(config, test_data)

        # Get the checkpoint tuple
        tuple_result = postgres_config.get_checkpoint_tuple(updated_config)

        # Verify the tuple
        assert tuple_result is not None
        assert tuple_result.config == updated_config
        assert tuple_result.checkpoint is not None
        assert "channel_values" in tuple_result.checkpoint
        assert tuple_result.metadata is not None

        logger.info(
            f"✅ Retrieved checkpoint tuple with metadata: {tuple_result.metadata}"
        )

    def test_list_checkpoints(self, postgres_config, test_thread_id, test_data):
        """Test listing checkpoints for a thread."""
        # Register thread
        postgres_config.register_thread(test_thread_id)

        # Create a config with the thread ID
        config = {"configurable": {"thread_id": test_thread_id}}

        # Put multiple checkpoints
        for i in range(3):
            test_data_copy = test_data.copy()
            test_data_copy["state"]["_counter"] = i + 1
            postgres_config.put_checkpoint(config, test_data_copy)

            # Brief pause to ensure distinct timestamps
            import time

            time.sleep(0.1)

        # List the checkpoints
        checkpoints = postgres_config.list_checkpoints(config)

        # Verify we got a list
        assert isinstance(checkpoints, list)

        # Verify history is preserved (3 checkpoints for standard mode)
        assert len(checkpoints) == 3, "Expected 3 checkpoints in standard mode"

        # Verify order (newest first)
        for i, checkpoint in enumerate(checkpoints):
            state = checkpoint.checkpoint.get("channel_values", {}).get("state", {})
            counter = state.get("_counter", None)
            expected = 3 - i  # 3, 2, 1
            assert counter == expected, f"Expected counter {expected}, got {counter}"

        logger.info(f"✅ Listed {len(checkpoints)} checkpoints in correct order")

    def test_delete_thread(self, postgres_config, test_thread_id, test_data):
        """Test deleting a thread and all its checkpoints."""
        # Register thread
        postgres_config.register_thread(test_thread_id)

        # Create a config with the thread ID
        config = {"configurable": {"thread_id": test_thread_id}}

        # Put a checkpoint
        updated_config = postgres_config.put_checkpoint(config, test_data)

        # Verify checkpoint exists
        checkpoint = postgres_config.get_checkpoint(updated_config)
        assert checkpoint is not None

        # Delete the thread
        postgres_config.delete_thread(test_thread_id)

        # Create checkpointer to verify
        checkpointer = postgres_config.create_checkpointer()

        # Ensure pool is open
        pool = ensure_pool_open(checkpointer)

        # Verify thread was deleted
        with pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT 1 FROM threads WHERE thread_id = %s", (test_thread_id,)
                )
                result = cursor.fetchone()

                assert (
                    result is None
                ), f"Thread {test_thread_id} still exists in database"

                # Verify checkpoints were deleted
                cursor.execute(
                    "SELECT 1 FROM checkpoints WHERE thread_id = %s", (test_thread_id,)
                )
                result = cursor.fetchone()

                assert (
                    result is None
                ), f"Checkpoints for thread {test_thread_id} still exist in database"

        logger.info(
            f"✅ Thread {test_thread_id} and its checkpoints were deleted successfully"
        )


class Test_PostgresShallowCheckpointer:
    """Tests for the PostgreSQL shallow checkpointer mode."""

    def test_create_shallow_checkpointer(self, postgres_shallow_config):
        """Test creating a shallow PostgreSQL checkpointer."""
        # Create the checkpointer
        checkpointer = postgres_shallow_config.create_checkpointer()

        # Verify it's the right type
        assert checkpointer is not None
        assert "ShallowPostgresSaver" in str(type(checkpointer))

        logger.info(f"✅ Created shallow PostgreSQL checkpointer: {type(checkpointer)}")

    def test_shallow_list_checkpoints(
        self, postgres_shallow_config, test_thread_id, test_data
    ):
        """Test that shallow mode only keeps the latest checkpoint."""
        # Register thread
        postgres_shallow_config.register_thread(test_thread_id)

        # Create a config with the thread ID
        config = {"configurable": {"thread_id": test_thread_id}}

        # Put multiple checkpoints
        for i in range(3):
            test_data_copy = test_data.copy()
            test_data_copy["state"]["_counter"] = i + 1
            postgres_shallow_config.put_checkpoint(
                config, test_data_copy
            )

            # Brief pause to ensure distinct timestamps
            import time

            time.sleep(0.1)

        # List the checkpoints
        checkpoints = postgres_shallow_config.list_checkpoints(config)

        # Verify we got a list
        assert isinstance(checkpoints, list)

        # Verify only last checkpoint is retained (shallow mode)
        assert len(checkpoints) == 1, "Expected only 1 checkpoint in shallow mode"

        # Verify it's the latest one
        state = checkpoints[0].checkpoint.get("channel_values", {}).get("state", {})
        counter = state.get("_counter", None)
        assert counter == 3, f"Expected counter 3, got {counter}"

        logger.info("✅ Shallow mode correctly retained only the latest checkpoint"t")


class Test_PostgresAsyncCheckpointer:
    """Tests for the PostgreSQL async checkpointer."""

    @pytest.mark.asyncio
    async def test_initialize_async_checkpointer(self, postgres_async_config):
        """Test initializing an async PostgreSQL checkpointer."""
        # Initialize the checkpointer
        try:
            checkpointer = await postgres_async_config.initialize_async_checkpointer()

            # Verify it's the right type
            assert checkpointer is not None
            assert "AsyncPostgresSaver" in str(type(checkpointer))

            logger.info(
                f"✅ Created async PostgreSQL checkpointer: {type(checkpointer)}"
            )

            # Clean up
            await postgres_async_config.aclose()
        except ImportError:
            pytest.skip("Async PostgreSQL dependencies not available")

    @pytest.mark.asyncio
    async def test_async_register_thread(self, postgres_async_config, test_thread_id):
        """Test registering a thread asynchronously."""
        try:
            # Initialize checkpointer
            checkpointer = await postgres_async_config.initialize_async_checkpointer()

            # Register thread
            await postgres_async_config.aregister_thread(
                test_thread_id, metadata={"test": True}
            )

            # Verify thread exists (need to use async connection)
            pool = getattr(checkpointer, "conn", None)
            if pool:
                async with pool.connection() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute(
                            "SELECT 1 FROM threads WHERE thread_id = %s",
                            (test_thread_id,),
                        )
                        result = await cursor.fetchone()

                        assert (
                            result is not None
                        ), f"Thread {test_thread_id} not found in database"

            logger.info(f"✅ Thread {test_thread_id} registered asynchronously")

            # Clean up
            await postgres_async_config.aclose()
        except ImportError:
            pytest.skip("Async PostgreSQL dependencies not available")

    @pytest.mark.asyncio
    async def test_async_put_and_get_checkpoint(
        self, postgres_async_config, test_thread_id, test_data
    ):
        """Test storing and retrieving a checkpoint asynchronously."""
        try:
            # Initialize checkpointer
            await postgres_async_config.initialize_async_checkpointer()

            # Register thread
            await postgres_async_config.aregister_thread(test_thread_id)

            # Create a config with the thread ID
            config = {"configurable": {"thread_id": test_thread_id}}

            # Put a checkpoint
            updated_config = await postgres_async_config.aput_checkpoint(
                config, test_data
            )

            # Verify the config was updated
            assert "checkpoint_id" in updated_config["configurable"]
            checkpoint_id = updated_config["configurable"]["checkpoint_id"]
            logger.info(
                f"✅ Created checkpoint asynchronously with ID: {checkpoint_id}"
            )

            # Get the checkpoint data
            checkpoint = await postgres_async_config.aget_checkpoint(updated_config)

            # Verify we got data back
            assert checkpoint is not None
            assert "messages" in checkpoint
            assert len(checkpoint["messages"]) == 1
            assert "_counter" in checkpoint["state"]
            assert checkpoint["state"]["_counter"] == 1

            logger.info(
                f"✅ Retrieved checkpoint data asynchronously: {json.dumps(checkpoint, indent=2)}"
            )

            # Clean up
            await postgres_async_config.aclose()
        except ImportError:
            pytest.skip("Async PostgreSQL dependencies not available")


# Integration test with setup_checkpointer utility
class Test_CheckpointerSetup:
    """Tests for the checkpointer setup utilities."""

    def test_setup_postgres_checkpointer(self, test_thread_id):
        """Test setting up a PostgreSQL checkpointer using the utility function."""
        try:
            # Import required dependencies
            import psycopg_pool
            from langgraph.checkpoint.postgres import PostgresSaver

            # Create a test agent config
            class TestAgentConfig:
                def __init__(self):
                    self.name = "test_agent"
                    self.persistence = {
                        "type": "postgres",
                        "db_host": os.environ.get("POSTGRES_HOST", "localhost"),
                        "db_port": int(os.environ.get("POSTGRES_PORT", "5432")),
                        "db_name": os.environ.get("POSTGRES_DB", "postgres"),
                        "db_user": os.environ.get("POSTGRES_USER", "postgres"),
                        "db_pass": os.environ.get("POSTGRES_PASSWORD", "postgres"),
                        "setup_needed": True,
                    }

            # Create the config
            agent_config = TestAgentConfig()

            # Set up the checkpointer
            checkpointer = setup_checkpointer(agent_config)

            # Verify it's the right type
            assert checkpointer is not None
            assert "PostgresSaver" in str(type(checkpointer))

            # Test it works by registering a thread
            register_thread_if_needed(checkpointer, test_thread_id, {"test": True})

            logger.info("✅ Set up PostgreSQL checkpointer using utility function"n")

        except ImportError:
            pytest.skip("PostgreSQL dependencies not available")
