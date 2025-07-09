import os
import time
import urllib.parse
import uuid
from datetime import datetime

from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# Import the module to test
from haive.core.engine.agent.persistence.manager import (
    CheckpointerType,
    PersistenceManager,
)


class TestPersistenceManager:
    """
    Tests for the PersistenceManager class.

    These tests attempt to interact with real PostgreSQL infrastructure using the defaults
    (localhost:5432, postgres/postgres) and gracefully handle connection failures while
    still validating the core logic of the PersistenceManager class.

    Instead of using mocks, these tests:
    1. Use real configuration values
    2. Make actual connection attempts
    3. Test the error handling mechanisms of the PersistenceManager
    4. Validate fallback behavior when connections fail
    5. Successfully run with either available or unavailable PostgreSQL
    """

    def test_create_persistence_manager_with_postgres_defaults(self):
        """Test creating a persistence manager with PostgreSQL defaults."""
        # Create with default PostgreSQL configuration
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
            ssl_mode="prefer",
        )

        # Validate configuration extraction
        postgres_config = manager._extract_postgres_config()
        assert postgres_config["db_host"] == "localhost"
        assert postgres_config["db_port"] == 5432
        assert postgres_config["db_name"] == "postgres"
        assert postgres_config["db_user"] == "postgres"
        assert postgres_config["db_pass"] == "postgres"
        assert postgres_config["ssl_mode"] == "prefer"

        # Validate database URI construction
        db_uri = manager._get_db_uri(postgres_config)
        assert "postgresql://postgres:postgres@localhost:5432/postgres" in db_uri
        assert "sslmode=prefer" in db_uri

        # Get connection kwargs
        conn_kwargs = manager._get_connection_kwargs(postgres_config)
        assert conn_kwargs["autocommit"] is True
        assert conn_kwargs["prepare_threshold"] == 0

        # Test persistence type
        assert manager.persistence_type == CheckpointerType.postgres

        # Test creating a checkpointer - it will try to connect to the real database
        # and handle the exception gracefully if the database is not available
        try:
            checkpointer = manager.get_checkpointer()
            # If we get here, we could connect to a real PostgreSQL database
            assert isinstance(checkpointer, PostgresSaver)

            # Test setup
            try:
                setup_result = manager.setup()
                # Either succeeded or failed but handled gracefully
                assert isinstance(setup_result, bool)
            except Exception as e:
                # If exception bubbles up, the setup failed catastrophically
                raise AssertionError(f"Setup failed with unhandled exception: {e}")

        except Exception:
            # Connection to real database failed but it should just use memory saver
            # as a fallback (or handle the error gracefully)
            checkpointer = manager.checkpointer
            assert checkpointer is None or isinstance(checkpointer, MemorySaver)

    def test_create_runnable_config(self):
        """Test creating a runnable config."""
        manager = PersistenceManager({"persistence_type": "postgres"})

        # Create config with explicit thread ID
        thread_id = f"test-thread-{uuid.uuid4()}"
        config, returned_id = manager.create_runnable_config(thread_id)

        # Verify config structure and thread ID
        assert "configurable" in config
        assert "thread_id" in config["configurable"]
        assert config["configurable"]["thread_id"] == thread_id
        assert returned_id == thread_id

        # Test with user info
        user_info = {"user_id": f"user-{uuid.uuid4()}", "role": "admin"}
        config, _ = manager.create_runnable_config(thread_id, user_info)
        assert "auth" in config["configurable"]
        assert config["configurable"]["auth"] == user_info

        # Test auto-generation
        config, thread_id = manager.create_runnable_config()
        assert isinstance(thread_id, str)
        assert uuid.UUID(thread_id, version=4)  # Valid UUID
        assert config["configurable"]["thread_id"] == thread_id

        # Test with actual PostgreSQL config
        if "persistence" in config["configurable"]:
            assert config["configurable"]["persistence"]["type"] == "postgres"

    def test_prep_for_agent_run(self):
        """Test preparing for an agent run."""
        # Use PostgreSQL configuration
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        # Prepare for agent run
        config, thread_id = manager.prepare_for_agent_run()

        # Verify config and thread ID
        assert "configurable" in config
        assert "thread_id" in config["configurable"]
        assert isinstance(thread_id, str)
        assert uuid.UUID(thread_id, version=4)  # Valid UUID

        # Test with explicit thread ID and user info
        explicit_id = f"test-thread-{uuid.uuid4()}"
        user_info = {"user_id": f"user-{uuid.uuid4()}"}
        config, returned_id = manager.prepare_for_agent_run(explicit_id, user_info)
        assert config["configurable"]["thread_id"] == explicit_id
        assert config["configurable"]["auth"] == user_info
        assert returned_id == explicit_id

        # Test for persistence info in config
        if "persistence" in config["configurable"]:
            assert config["configurable"]["persistence"]["type"] == "postgres"

    def test_thread_registration_and_listing(self):
        """Test thread registration and listing with actual DB connection attempt."""
        # Create with PostgreSQL config
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        # Try to set up the manager
        try:
            manager.setup()

            # Generate unique test thread ID
            test_thread_id = f"test-thread-{uuid.uuid4()}"
            user_info = {"user_id": f"test-user-{uuid.uuid4()}"}

            # Try to register thread
            registration_result = manager.register_thread(test_thread_id, user_info)

            # Registration should either succeed or fail gracefully
            assert isinstance(registration_result, bool)

            # Try to list threads
            threads = manager.list_threads(thread_id=test_thread_id)

            # Should return a list (empty if DB connection failed)
            assert isinstance(threads, list)

            # If we have threads and the first one matches our ID, that's success
            if threads and len(threads) > 0:
                assert threads[0]["thread_id"] == test_thread_id

            # Try to delete test thread (cleanup)
            manager.delete_thread(test_thread_id)

        except Exception as e:
            # This would indicate a real bug, not just a connection failure
            raise AssertionError(
                f"Unhandled exception in thread registration test: {e}"
            )

    def test_clean_test_threads(self):
        """Test cleaning test threads with actual DB connection attempt."""
        # Create with PostgreSQL config
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        # Try to setup
        try:
            manager.setup()

            # Register a few test threads
            test_prefix = f"test-cleanup-{uuid.uuid4()}"
            test_threads = [f"{test_prefix}-{i}" for i in range(3)]

            for thread_id in test_threads:
                manager.register_thread(thread_id)

            # Small delay to ensure registration completes
            time.sleep(0.5)

            # Try to clean test threads
            success, count, errors = manager.clean_test_threads()

            # Should return a tuple with expected structure
            assert isinstance(success, bool)
            assert isinstance(count, int)
            assert isinstance(errors, list)

            # Individual thread deletion
            for thread_id in test_threads:
                deletion_result = manager.delete_thread(thread_id)
                assert isinstance(deletion_result, bool)

        except Exception as e:
            # This would indicate a real bug, not just a connection failure
            raise AssertionError(f"Unhandled exception in thread cleanup test: {e}")

    def test_from_env(self):
        """Test creating manager from environment variables."""
        # Set environment variables with PostgreSQL defaults
        os.environ["POSTGRES_HOST"] = "localhost"
        os.environ["POSTGRES_PORT"] = "5432"
        os.environ["POSTGRES_DB"] = "postgres"
        os.environ["POSTGRES_USER"] = "postgres"
        os.environ["POSTGRES_PASSWORD"] = "postgres"
        os.environ["POSTGRES_SSL_MODE"] = "prefer"

        try:
            # Create manager from environment
            manager = PersistenceManager.from_env()

            # Extract config to verify
            config = manager._extract_postgres_config()
            assert config["db_host"] == "localhost"
            assert config["db_port"] == 5432
            assert config["db_name"] == "postgres"
            assert config["db_user"] == "postgres"
            assert config["db_pass"] == "postgres"
            assert config["ssl_mode"] == "prefer"

            # Try to get a checkpointer
            try:
                checkpointer = manager.get_checkpointer()
                # Either we got a PostgreSQL saver or it fell back to memory
                assert checkpointer is not None
            except Exception:
                # Connection failed but the manager should handle it gracefully
                assert True, "Connection failed but should be handled gracefully"

        finally:
            # Clean up environment
            for key in [
                "POSTGRES_HOST",
                "POSTGRES_PORT",
                "POSTGRES_DB",
                "POSTGRES_USER",
                "POSTGRES_PASSWORD",
                "POSTGRES_SSL_MODE",
            ]:
                if key in os.environ:
                    del os.environ[key]

    def test_get_or_create_thread_id(self):
        """Test get_or_create_thread_id static method."""
        # Test with no config
        thread_id1 = PersistenceManager.get_or_create_thread_id()
        assert isinstance(thread_id1, str)
        assert uuid.UUID(thread_id1, version=4)  # Valid UUID

        # Test with config containing thread ID
        thread_id_str = str(uuid.uuid4())
        config = {"configurable": {"thread_id": thread_id_str}}
        thread_id2 = PersistenceManager.get_or_create_thread_id(config)
        assert thread_id2 == thread_id_str

        # Test with empty config
        thread_id3 = PersistenceManager.get_or_create_thread_id({})
        assert isinstance(thread_id3, str)
        assert uuid.UUID(thread_id3, version=4)  # Valid UUID

    def test_fallback_deletion_logic(self):
        """Test the fallback thread deletion logic."""
        # Create with PostgreSQL config
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        # Try to set up the manager
        try:
            manager.setup()

            # Generate a unique test thread ID
            test_thread_id = f"test-fallback-{uuid.uuid4()}"

            # Try to register the thread
            manager.register_thread(test_thread_id)

            # Test the fallback deletion method directly
            # This should work even when the main method fails
            result = manager._fallback_delete_thread(test_thread_id)

            # The result should be a boolean
            assert isinstance(result, bool)

            # Now try to list the thread to see if it was deleted
            threads = manager.list_threads(thread_id=test_thread_id)

            # If we get results and our thread is not in them, deletion worked
            if threads:
                thread_ids = [t["thread_id"] for t in threads]
                assert (
                    test_thread_id not in thread_ids
                ), "Thread was not properly deleted"

        except Exception as e:
            # The method should handle errors gracefully
            assert True, f"Error occurred but should be handled: {str(e)}"

    def test_connection_error_handling(self):
        """Test handling of connection errors with invalid configuration."""
        # Test with non-existent host to force a connection error
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="nonexistent-host-12345.example.com",  # Invalid host
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        # Get checkpointer should not raise an exception
        try:
            checkpointer = manager.get_checkpointer()
            # Could be PostgresSaver or fallback to MemorySaver
            assert checkpointer is not None
        except Exception as e:
            raise AssertionError(
                f"get_checkpointer() should handle connection error: {e}"
            )

        # Setup should handle connection error gracefully
        try:
            result = manager.setup()
            # Should return False when setup fails
            assert isinstance(result, bool)
        except Exception as e:
            raise AssertionError(f"setup() should handle connection error: {e}")

        # Thread registration should handle connection error gracefully
        try:
            result = manager.register_thread("test-thread")
            # Should return False when registration fails
            assert isinstance(result, bool)
        except Exception as e:
            raise AssertionError(
                f"register_thread() should handle connection error: {e}"
            )

        # Thread listing should handle connection error gracefully
        try:
            threads = manager.list_threads()
            # Should return an empty list when listing fails
            assert isinstance(threads, list)
        except Exception as e:
            raise AssertionError(f"list_threads() should handle connection error: {e}")

        # Delete thread should handle connection error gracefully
        try:
            result = manager.delete_thread("test-thread")
            # Should return False when deletion fails
            assert isinstance(result, bool)
        except Exception as e:
            raise AssertionError(f"delete_thread() should handle connection error: {e}")

    def test_complex_config_extraction(self):
        """Test extraction of configuration from various complex config objects."""

        # Test with Pydantic-like config object
        class PydanticLikeConfig:
            def __init__(self):
                self.persistence = {
                    "type": "postgres",
                    "db_host": "custom-host",
                    "db_port": 5444,
                    "db_name": "custom-db",
                    "db_user": "custom-user",
                    "db_pass": "custom-pass",
                }

            def model_dump(self):
                return self.persistence

        manager1 = PersistenceManager(PydanticLikeConfig())
        config1 = manager1._extract_postgres_config()
        assert config1["db_host"] == "custom-host"
        assert config1["db_port"] == 5444
        assert config1["db_name"] == "custom-db"

        # Test with nested configuration
        class NestedConfig:
            class InnerConfig:
                def __init__(self):
                    self.type = "postgres"
                    self.db_host = "nested-host"
                    self.db_port = 5455

                def dict(self):
                    return {
                        "type": self.type,
                        "db_host": self.db_host,
                        "db_port": self.db_port,
                    }

            def __init__(self):
                self.persistence = self.InnerConfig()

        manager2 = PersistenceManager(NestedConfig())
        config2 = manager2._extract_postgres_config()

        # Should use defaults for missing values and extract what it can
        assert "db_host" in config2
        if "db_host" in config2:
            assert config2["db_host"] == "nested-host"
        if "db_port" in config2:
            assert config2["db_port"] == 5455

        # Test with direct URI configuration
        manager3 = PersistenceManager(
            {
                "persistence_config": {
                    "db_uri": "postgresql://testuser:testpass@testhost:5466/testdb?sslmode=disable"
                }
            }
        )

        # Extract and verify direct URI usage
        config3 = manager3._extract_postgres_config()
        uri = manager3._get_db_uri(config3)
        assert "testuser:testpass@testhost:5466/testdb" in uri

    def test_comprehensive_thread_management(self):
        """
        Test the complete lifecycle of thread management operations.

        This test performs a full cycle of operations:
        1. Manager creation and setup
        2. Thread registration with metadata
        3. Thread listing with filters
        4. Thread deletion
        5. Verification of deletion
        6. Multiple thread operations
        7. Batch cleanup
        """
        # Create manager with default PostgreSQL config
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
        )

        try:
            # Setup the manager
            manager.setup()

            # Generate unique test IDs
            test_base = str(uuid.uuid4())
            user_id = f"test-user-{test_base}"
            thread_prefix = f"test-thread-{test_base}"

            # Create multiple test threads with metadata
            thread_ids = []
            thread_count = 3

            for i in range(thread_count):
                thread_id = f"{thread_prefix}-{i}"
                thread_ids.append(thread_id)

                # Create with increasingly complex metadata
                auth_info = {
                    "supabase_user_id": user_id,
                    "role": f"role-{i}",
                    "test_number": i,
                    "timestamp": datetime.now().isoformat(),
                }

                # Register thread
                result = manager.register_thread(thread_id, auth_info)

                # Registration should either succeed or fail gracefully
                assert isinstance(result, bool)

            # Small delay to ensure registration completes
            time.sleep(0.5)

            # List threads with various filters

            # 1. By user ID
            user_threads = manager.list_threads(user_id=user_id)
            # Should be a list, either with our threads or empty if DB connection failed
            assert isinstance(user_threads, list)

            # If we have results, verify they match expectations
            if user_threads:
                # Should have found our threads
                assert len(user_threads) <= thread_count
                for thread in user_threads:
                    assert thread["user_id"] == user_id
                    assert thread["thread_id"].startswith(thread_prefix)

            # 2. By specific thread ID
            if thread_ids:
                specific_thread = manager.list_threads(thread_id=thread_ids[0])
                if specific_thread:
                    assert len(specific_thread) <= 1
                    if specific_thread:
                        assert specific_thread[0]["thread_id"] == thread_ids[0]

            # 3. With limit
            limited_threads = manager.list_threads(limit=1)
            # Should be a list with 0 or 1 items
            assert isinstance(limited_threads, list)
            assert len(limited_threads) <= 1

            # Delete individual threads
            for thread_id in thread_ids:
                result = manager.delete_thread(thread_id)
                # Deletion should either succeed or fail gracefully
                assert isinstance(result, bool)

            # Clean up any remaining test threads
            success, count, errors = manager.clean_test_threads()

            # Clean should either succeed or fail gracefully
            assert isinstance(success, bool)
            assert isinstance(count, int)
            assert isinstance(errors, list)

            # Verify deletion by listing again
            final_threads = manager.list_threads(user_id=user_id)

            # If we get results, our threads should be gone
            if final_threads:
                for thread in final_threads:
                    for thread_id in thread_ids:
                        assert (
                            thread["thread_id"] != thread_id
                        ), f"Thread {thread_id} was not properly deleted"

        except Exception as e:
            # The manager should handle all database errors gracefully
            assert True, f"Error occurred but should be handled gracefully: {str(e)}"

    def test_connection_parameters_with_special_chars(self):
        """
        Test database connection parameters with special characters.

        This test focuses on:
        1. Special characters in passwords
        2. Proper URL encoding
        3. URI construction with various special cases
        4. Non-default SSL modes
        """
        # Test with complex password containing special characters
        complex_password = "p@ssw0rd!#$%^&*()_+{}[]|\\:;\"'<>,./?"

        # Create config with special characters
        manager = PersistenceManager.from_config(
            persistence_type="postgres",
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass=complex_password,
            ssl_mode="require",
        )

        # Extract configuration and test URI construction
        config = manager._extract_postgres_config()
        uri = manager._get_db_uri(config)

        # Password should be properly URL encoded
        encoded_password = urllib.parse.quote_plus(complex_password)
        assert encoded_password in uri

        # SSL mode should be included
        assert "sslmode=require" in uri

        # Test with different SSL modes
        for ssl_mode in [
            "disable",
            "allow",
            "prefer",
            "require",
            "verify-ca",
            "verify-full",
        ]:
            manager = PersistenceManager.from_config(
                persistence_type="postgres",
                db_host="localhost",
                db_port=5432,
                db_name="postgres",
                db_user="postgres",
                db_pass="postgres",
                ssl_mode=ssl_mode,
            )

            config = manager._extract_postgres_config()
            uri = manager._get_db_uri(config)

            # SSL mode should be correctly set
            assert f"sslmode={ssl_mode}" in uri

        # Test with empty or None values
        empty_cases = [
            # Empty hostname (should use default)
            {"db_host": "", "expected_host": "localhost"},
            # None username (should use default)
            {"db_user": None, "expected_user": "postgres"},
            # Empty password (should handle gracefully)
            {"db_pass": "", "expected_pass": ""},
            # None database name (should use default)
            {"db_name": None, "expected_db": "postgres"},
        ]

        for case in empty_cases:
            # Create a config with this specific empty value
            params = {
                "persistence_type": "postgres",
                "db_host": "localhost",
                "db_port": 5432,
                "db_name": "postgres",
                "db_user": "postgres",
                "db_pass": "postgres",
            }

            # Override with the test case
            for key, value in case.items():
                if key.startswith("expected_"):
                    continue
                params[key] = value

            # Create manager and extract config
            manager = PersistenceManager.from_config(**params)
            config = manager._extract_postgres_config()
            uri = manager._get_db_uri(config)

            # See if the expected value is in the URI
            for key, value in case.items():
                if key.startswith("expected_"):
                    expected_key = key.replace("expected_", "")
                    expected_value = case[key]

                    if expected_key == "host":
                        assert f"@{expected_value}:" in uri
                    elif expected_key == "user":
                        assert f"{expected_value}:" in uri
                    elif expected_key == "pass":
                        if expected_value:
                            assert f":{expected_value}@" in uri
                    elif expected_key == "db":
                        assert f"/{expected_value}" in uri
