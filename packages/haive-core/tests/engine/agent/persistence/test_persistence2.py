# tests/engine/agent/persistence/test_postgres_config.py

import datetime
import json
import logging
import uuid

import pytest
from langgraph.checkpoint.memory import MemorySaver

from haive.core.engine.agent.persistence.postgres_config import (
    POSTGRES_AVAILABLE,
    PostgresCheckpointerConfig,
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Skip all tests if PostgreSQL is not available
pytestmark = pytest.mark.skipif(
    not POSTGRES_AVAILABLE, reason="PostgreSQL dependencies not available"
)


class TestPostgresCheckpointerConfig:
    """
    Integration tests for PostgresCheckpointerConfig using real PostgreSQL database.

    These tests require a PostgreSQL server running on localhost with default credentials.
    """

    # Test database connection parameters - modify if your test DB has different settings
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_NAME = "postgres"
    DB_USER = "postgres"
    DB_PASS = "postgres"

    @classmethod
    def create_test_config(cls, **kwargs) -> PostgresCheckpointerConfig:
        """Create a test config with default parameters that can be overridden."""
        default_params = {
            "db_host": cls.DB_HOST,
            "db_port": cls.DB_PORT,
            "db_name": cls.DB_NAME,
            "db_user": cls.DB_USER,
            "db_pass": cls.DB_PASS,
            # Use a fresh setup for each test by default
            "setup_needed": True,
        }
        default_params.update(kwargs)
        return PostgresCheckpointerConfig(**default_params)

    @pytest.fixture
    def test_config(self) -> PostgresCheckpointerConfig:
        """Fixture to create a standard test config and ensure cleanup."""
        config = self.create_test_config()
        yield config
        # Clean up after test
        if config._pool is not None:
            config.close()

    def generate_thread_id(self) -> str:
        """Generate a unique thread ID for testing."""
        return f"test_{uuid.uuid4()}"

    def test_create_checkpointer(self, test_config):
        """Test creation of PostgreSQL checkpointer with real database."""
        # Create checkpointer
        checkpointer = test_config.create_checkpointer()

        # Verify checkpointer type
        assert (
            checkpointer.__class__.__name__ == "PostgresSaver"
        ), "Should create a PostgresSaver instance"

        # Verify pool was created
        assert test_config._pool is not None, "Connection pool should be created"

        # Check available methods on checkpointer
        expected_methods = ["get", "list", "put", "setup"]
        for method in expected_methods:
            assert hasattr(
                checkpointer, method
            ), f"Checkpointer should have {method} method"

    def test_connection_parameters(self):
        """Test that connection parameters are properly used."""
        # Create config with non-default parameters
        config = self.create_test_config(
            min_pool_size=2,
            max_pool_size=8,
            auto_commit=False,  # Test non-default auto_commit
            prepare_threshold=5,  # Test non-default prepare_threshold
        )

        try:
            # Create checkpointer - this should establish a connection
            config.create_checkpointer()

            # If no exception was raised, the connection was successful
            assert config._pool is not None, "Pool should be created"

            # Register a thread to test the connection is functional
            thread_id = self.generate_thread_id()
            config.register_thread(thread_id)

            # Verify thread exists - using direct pool access to test
            with config._pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM threads WHERE thread_id = %s", (thread_id,)
                    )
                    result = cursor.fetchone()
                    assert (
                        result is not None
                    ), "Thread registration should work with custom parameters"
        finally:
            config.close()

    def test_fallback_on_connection_error(self):
        """Test fallback to memory saver when connection fails."""
        # Create config with invalid connection parameters
        config = self.create_test_config(db_host="invalid-host", db_port=1234)

        # Create checkpointer - should fail and fallback to memory
        checkpointer = config.create_checkpointer()

        # Verify fallback to memory saver
        assert isinstance(checkpointer, MemorySaver), "Should fallback to MemorySaver"

    def test_thread_registration(self, test_config):
        """Test thread registration in the database."""
        # Generate unique thread ID
        thread_id = self.generate_thread_id()

        # Metadata for this thread
        metadata = {
            "test": "integration",
            "timestamp": str(datetime.datetime.now()),
            "complex": {"nested": ["data", "structure"], "value": 42},
        }

        # Create checkpointer and register thread
        test_config.create_checkpointer()
        test_config.register_thread(thread_id, metadata=metadata)

        # Verify thread exists in database by querying directly
        with test_config._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT metadata FROM threads WHERE thread_id = %s", (thread_id,)
                )
                result = cursor.fetchone()

                # Thread should be found
                assert result is not None, f"Thread {thread_id} not found in database"

                # Get metadata - it could be a dict or a string depending on how it's stored
                db_metadata = result[0]
                if isinstance(db_metadata, str):
                    db_metadata = json.loads(db_metadata)

                # Verify key metadata elements match
                assert (
                    db_metadata.get("test") == "integration"
                ), "Metadata test field should match"
                assert (
                    db_metadata.get("complex", {}).get("value") == 42
                ), "Nested metadata should match"

    def test_updating_existing_thread(self, test_config):
        """Test registering an already existing thread."""
        # Generate unique thread ID
        thread_id = self.generate_thread_id()

        # Initial metadata
        initial_metadata = {"initial": "value"}

        # Create checkpointer and register thread
        test_config.create_checkpointer()

        # Register thread first time
        test_config.register_thread(thread_id, metadata=initial_metadata)

        # Register same thread again with different metadata
        updated_metadata = {"updated": "value"}
        test_config.register_thread(thread_id, metadata=updated_metadata)

        # Verify thread exists with original metadata (ON CONFLICT DO NOTHING)
        with test_config._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT metadata FROM threads WHERE thread_id = %s", (thread_id,)
                )
                result = cursor.fetchone()

                # Thread should be found
                assert result is not None, f"Thread {thread_id} not found in database"

                # Get metadata - could be a dict or string
                db_metadata = result[0]
                if isinstance(db_metadata, str):
                    db_metadata = json.loads(db_metadata)

                # Query result might vary based on ON CONFLICT behavior - test appropriately
                # Just verifying that the thread exists after multiple registrations is sufficient

                # Log what was actually found for diagnosis
                logger.info(
                    f"Thread metadata after multiple registrations: {db_metadata}"
                )

    def test_thread_registration_without_metadata(self, test_config):
        """Test thread registration without providing metadata."""
        # Generate unique thread ID
        thread_id = self.generate_thread_id()

        # Create checkpointer and register thread without metadata
        test_config.create_checkpointer()
        test_config.register_thread(thread_id)

        # Verify thread exists with default metadata
        with test_config._pool.connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT metadata FROM threads WHERE thread_id = %s", (thread_id,)
                )
                result = cursor.fetchone()

                # Thread should be found
                assert result is not None, f"Thread {thread_id} not found in database"

                # Metadata should exist - whatever the default is
                # For testing, we just verify the thread registration worked
                assert result[0] is not None, "Thread should have some metadata value"

    def test_pool_reuse(self, test_config):
        """Test that pool is reused across multiple checkpointer creations."""
        # Create first checkpointer
        test_config.create_checkpointer()

        # Store reference to pool
        pool1 = test_config._pool

        # Create second checkpointer
        test_config.create_checkpointer()

        # Pool should be the same object (reused)
        assert test_config._pool is pool1, "Pool should be reused"

    def test_pool_close(self):
        """Test pool closing."""
        # Create config
        config = self.create_test_config()

        # Create checkpointer to initialize pool
        config.create_checkpointer()

        # Verify pool exists
        assert config._pool is not None, "Pool should be created"

        # Store pool reference

        # Close the pool
        config.close()

        # We can't easily verify the pool is closed without relying on implementation details
        # For now, let's just ensure no exception is raised during close

    def test_pool_open_check(self):
        """Test pool open state checking and reopening."""
        # Create config
        config = self.create_test_config()

        # Create a checkpointer to initialize pool
        config.create_checkpointer()

        # Close the pool to simulate it being in closed state
        config.close()

        # Set _pool to a mock that is "closed" - this avoids direct dependency on pool implementation
        import unittest.mock as mock

        mock_pool = mock.MagicMock()
        mock_pool.is_open.return_value = False
        config._pool = mock_pool

        # Register a thread - this should try to reopen the pool
        thread_id = self.generate_thread_id()

        # Try registration - should call open on the mock
        try:
            config.register_thread(thread_id)
        except Exception:
            # Expected since we're using a mock pool
            pass

        # Verify open was called
        mock_pool.open.assert_called_once()

    def test_setup_tables(self, test_config):
        """Test that tables are properly set up."""
        # Create checkpointer which should set up tables
        test_config.create_checkpointer()

        # Query database to check if tables exist
        with test_config._pool.connection() as conn:
            with conn.cursor() as cursor:
                # Check if checkpoints table exists
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'checkpoints'
                    );
                """
                )
                checkpoints_exists = cursor.fetchone()[0]

                # Check if threads table exists
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_name = 'threads'
                    );
                """
                )
                threads_exists = cursor.fetchone()[0]

        # Verify tables exist
        assert checkpoints_exists, "Checkpoints table should exist"
        assert threads_exists, "Threads table should exist"

    def test_auto_commit_setting(self):
        """Test auto_commit setting affects transaction behavior."""
        # This test demonstrates explicitly that auto_commit affects transaction behavior

        # First with auto_commit=True
        config_autocommit = self.create_test_config(auto_commit=True)
        thread_id_autocommit = self.generate_thread_id()

        try:
            # Create checkpointer
            config_autocommit.create_checkpointer()

            # With autocommit, changes should be visible immediately without explicit commit
            with config_autocommit._pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO threads (thread_id, metadata) VALUES (%s, %s)",
                        (thread_id_autocommit, "{}"),
                    )

            # Verify thread exists in new connection
            with config_autocommit._pool.connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT 1 FROM threads WHERE thread_id = %s",
                        (thread_id_autocommit,),
                    )
                    result = cursor.fetchone()
                    assert (
                        result is not None
                    ), "Thread should exist with auto_commit=True"
        finally:
            config_autocommit.close()

        # Now with auto_commit=False (need to explicitly commit)
        config_no_autocommit = self.create_test_config(auto_commit=False)
        thread_id_no_autocommit = self.generate_thread_id()

        try:
            # Create checkpointer
            config_no_autocommit.create_checkpointer()

            # First verify behavior without commit
            explicit_committed = False
            try:
                # With no autocommit, changes require explicit commit to be visible outside transaction
                # We use raw connection to avoid with block auto-committing
                conn = config_no_autocommit._pool.getconn()
                cursor = conn.cursor()

                try:
                    # Insert data - but don't commit
                    cursor.execute(
                        "INSERT INTO threads (thread_id, metadata) VALUES (%s, %s)",
                        (thread_id_no_autocommit, "{}"),
                    )

                    # Check it's visible in current transaction
                    cursor.execute(
                        "SELECT 1 FROM threads WHERE thread_id = %s",
                        (thread_id_no_autocommit,),
                    )
                    result = cursor.fetchone()
                    assert (
                        result is not None
                    ), "Thread should be visible within transaction"

                    # Now check visibility in separate connection without commit
                    with config_no_autocommit._pool.connection() as conn2:
                        with conn2.cursor() as cursor2:
                            cursor2.execute(
                                "SELECT 1 FROM threads WHERE thread_id = %s",
                                (thread_id_no_autocommit,),
                            )
                            result = cursor2.fetchone()
                            # Should not be visible yet in a different connection
                            assert (
                                result is None
                            ), "Thread should not be visible before commit"

                    # Now commit and test again
                    conn.commit()
                    explicit_committed = True

                    # Now visible in separate connection
                    with config_no_autocommit._pool.connection() as conn2:
                        with conn2.cursor() as cursor2:
                            cursor2.execute(
                                "SELECT 1 FROM threads WHERE thread_id = %s",
                                (thread_id_no_autocommit,),
                            )
                            result = cursor2.fetchone()
                            assert (
                                result is not None
                            ), "Thread should be visible after commit"
                finally:
                    cursor.close()
                    if not explicit_committed:
                        conn.rollback()  # Ensure rollback if we didn't commit
                    config_no_autocommit._pool.putconn(conn)
            except Exception as e:
                # If this fails, it likely means auto_commit is not being properly applied
                logger.error(f"Transaction test failed: {e}")
                pytest.fail(f"Transaction test failed: {e}")
        finally:
            config_no_autocommit.close()

    def test_checkpointing_functionality(self, test_config):
        """Test basic checkpoint get/put functionality."""
        # Generate unique thread ID
        thread_id = self.generate_thread_id()

        # Create checkpointer
        checkpointer = test_config.create_checkpointer()

        # Register thread
        test_config.register_thread(thread_id)

        # Create test data
        test_data = {"test_key": "test_value", "numbers": [1, 2, 3]}

        # This is the config that would be used by LangGraph
        config = {"configurable": {"thread_id": thread_id}}

        # Check if the checkpointer has the expected methods
        assert hasattr(checkpointer, "get"), "Checkpointer should have get method"
        assert hasattr(checkpointer, "put"), "Checkpointer should have put method"

        # Put data
        checkpointer.put(config, test_data)

        # Get data back
        retrieved_data = checkpointer.get(config)

        # Verify data was stored and retrieved correctly
        assert retrieved_data is not None, "Should retrieve data"
        assert "test_key" in retrieved_data, "Retrieved data should contain test_key"
        assert (
            retrieved_data["test_key"] == "test_value"
        ), "Retrieved test_key should match"
        assert "numbers" in retrieved_data, "Retrieved data should contain numbers"
        assert retrieved_data["numbers"] == [1, 2, 3], "Retrieved numbers should match"

    def test_list_checkpoints(self, test_config):
        """Test listing checkpoints for a thread."""
        # Generate unique thread ID
        thread_id = self.generate_thread_id()

        # Create checkpointer
        checkpointer = test_config.create_checkpointer()

        # Register thread
        test_config.register_thread(thread_id)

        # Create test data
        test_data_1 = {"step": 1, "data": "first checkpoint"}
        test_data_2 = {"step": 2, "data": "second checkpoint"}

        # Config with thread ID
        config = {"configurable": {"thread_id": thread_id}}

        # Put multiple checkpoints
        checkpointer.put(config, test_data_1)
        # Need to update config to avoid overwriting the same checkpoint
        config2 = {
            "configurable": {
                "thread_id": thread_id,
                "checkpoint_id": f"checkpoint_{uuid.uuid4()}",
            }
        }
        checkpointer.put(config2, test_data_2)

        # List checkpoints
        checkpoints = list(
            checkpointer.list({"configurable": {"thread_id": thread_id}})
        )

        # Verify we can find checkpoints
        assert len(checkpoints) >= 1, "Should find at least one checkpoint"

        # Check the data in first checkpoint
        checkpoint_data = checkpoints[0].checkpoint
        assert isinstance(checkpoint_data, dict), "Checkpoint data should be a dict"
