# tests/persistence/test_persistence.py

import os
import uuid

import pytest

from haive.core.persistence import (
    CheckpointerType,
    create_memory_checkpointer,
    create_sqlite_checkpointer,
    create_supabase_checkpointer,
    setup_checkpointer,
)

# Test data
TEST_DATA = {
    "messages": [
        {"role": "user", "content": "Hello, how are you?"},
        {"role": "assistant", "content": "I'm doing well, thank you for asking!"},
    ],
    "metadata": {"session_id": "test-session", "user_id": "test-user"},
    "state": {"current_step": "greeting", "context": {"topic": "general"}},
}

# Test configs
TEST_CONFIG = {
    "configurable": {
        "thread_id": f"test-thread-{uuid.uuid4()}",
        "checkpoint_ns": "test",
    }
}


class TestMemoryCheckpointer:
    """Tests for the memory-based checkpointer."""

    @pytest.fixture
    def checkpointer_config(self):
        """Create a memory checkpointer config for testing."""
        return create_memory_checkpointer()

    @pytest.fixture
    def checkpointer(self, checkpointer_config):
        """Create the actual checkpointer instance."""
        return checkpointer_config.create_checkpointer()

    def test_create_checkpointer(self, checkpointer_config):
        """Test creating a memory checkpointer."""
        assert checkpointer_config.type == CheckpointerType.memory

        # Create the checkpointer
        checkpointer = checkpointer_config.create_checkpointer()
        assert checkpointer is not None

    def test_register_thread(self, checkpointer_config):
        """Test thread registration."""
        thread_id = f"test-thread-{uuid.uuid4()}"

        # Register thread
        checkpointer_config.register_thread(
            thread_id, name="Test Thread", metadata={"purpose": "testing"}
        )

        # Check that thread was registered
        assert thread_id in checkpointer_config.threads

    def test_put_get_checkpoint(self, checkpointer_config):
        """Test putting and getting a checkpoint."""
        # Generate unique config for this test
        config = {
            "configurable": {
                "thread_id": f"test-thread-{uuid.uuid4()}",
                "checkpoint_ns": "test",
            }
        }

        # Store checkpoint
        updated_config = checkpointer_config.put_checkpoint(
            config, TEST_DATA, metadata={"test": "metadata"}
        )

        # Verify the updated config has a checkpoint_id
        assert "checkpoint_id" in updated_config["configurable"]

        # Retrieve checkpoint
        result = checkpointer_config.get_checkpoint(updated_config)

        # Verify checkpoint data
        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) == 2
        assert result["state"]["current_step"] == "greeting"

    def test_list_checkpoints(self, checkpointer_config):
        """Test listing checkpoints."""
        # Generate unique thread ID for this test
        thread_id = f"test-thread-{uuid.uuid4()}"
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "test"}}

        # Store multiple checkpoints
        for i in range(3):
            data = TEST_DATA.copy()
            data["state"]["step_index"] = i
            checkpointer_config.put_checkpoint(config, data)

        # List checkpoints
        checkpoints = checkpointer_config.list_checkpoints(config)

        # Verify checkpoints
        assert len(checkpoints) == 3


class TestSQLiteCheckpointer:
    """Tests for the SQLite-based checkpointer."""

    @pytest.fixture
    def db_path(self, tmp_path):
        """Create a temporary database path."""
        return os.path.join(tmp_path, "test_checkpoints.db")

    @pytest.fixture
    def checkpointer_config(self, db_path):
        """Create a SQLite checkpointer config for testing."""
        return create_sqlite_checkpointer(db_path=db_path)

    @pytest.fixture
    def checkpointer(self, checkpointer_config):
        """Create the actual checkpointer instance."""
        return checkpointer_config.create_checkpointer()

    def test_create_checkpointer(self, checkpointer_config, db_path):
        """Test creating a SQLite checkpointer."""
        assert checkpointer_config.type == CheckpointerType.sqlite
        assert checkpointer_config.db_path == db_path

        # Create the checkpointer
        checkpointer = checkpointer_config.create_checkpointer()
        assert checkpointer is not None

        # Check that database file was created
        assert os.path.exists(db_path)

    def test_register_thread(self, checkpointer_config):
        """Test thread registration."""
        thread_id = f"test-thread-{uuid.uuid4()}"

        # Register thread
        checkpointer_config.register_thread(
            thread_id, name="Test Thread", metadata={"purpose": "testing"}
        )

    def test_put_get_checkpoint(self, checkpointer_config):
        """Test putting and getting a checkpoint."""
        # Generate unique config for this test
        config = {
            "configurable": {
                "thread_id": f"test-thread-{uuid.uuid4()}",
                "checkpoint_ns": "test",
            }
        }

        # Store checkpoint
        updated_config = checkpointer_config.put_checkpoint(
            config, TEST_DATA, metadata={"test": "metadata"}
        )

        # Verify the updated config has a checkpoint_id
        assert "checkpoint_id" in updated_config["configurable"]

        # Retrieve checkpoint
        result = checkpointer_config.get_checkpoint(updated_config)

        # Verify checkpoint data
        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) == 2
        assert result["state"]["current_step"] == "greeting"

    def test_list_checkpoints(self, checkpointer_config):
        """Test listing checkpoints."""
        # Generate unique thread ID for this test
        thread_id = f"test-thread-{uuid.uuid4()}"
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "test"}}

        # Store multiple checkpoints
        for i in range(3):
            data = TEST_DATA.copy()
            data["state"] = TEST_DATA["state"].copy()
            data["state"]["step_index"] = i
            checkpointer_config.put_checkpoint(config, data)

        # List checkpoints
        checkpoints = checkpointer_config.list_checkpoints(config)

        # Verify checkpoints
        assert len(checkpoints) == 3


# Only run Supabase tests if credentials are available
@pytest.mark.skipif(
    not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_KEY"),
    reason="Supabase credentials not available",
)
class TestSupabaseCheckpointer:
    """Tests for the Supabase-based checkpointer."""

    @pytest.fixture
    def user_id(self):
        """Create a user ID for testing."""
        return str(uuid.uuid4())

    @pytest.fixture
    def checkpointer_config(self, user_id):
        """Create a Supabase checkpointer config for testing."""
        return create_supabase_checkpointer(
            # URLs and keys are loaded from environment
            user_id=user_id
        )

    @pytest.fixture
    def checkpointer(self, checkpointer_config):
        """Create the actual checkpointer instance."""
        return checkpointer_config.create_checkpointer()

    def test_create_checkpointer(self, checkpointer_config, user_id):
        """Test creating a Supabase checkpointer."""
        assert checkpointer_config.type == CheckpointerType.supabase
        assert checkpointer_config.user_id == user_id

        # Create the checkpointer
        checkpointer = checkpointer_config.create_checkpointer()
        assert checkpointer is not None

    def test_register_thread(self, checkpointer_config):
        """Test thread registration."""
        thread_id = f"test-thread-{uuid.uuid4()}"

        # Register thread
        checkpointer_config.register_thread(
            thread_id, name="Test Thread", metadata={"purpose": "testing"}
        )

    def test_put_get_checkpoint(self, checkpointer_config):
        """Test putting and getting a checkpoint."""
        # Generate unique config for this test
        config = {
            "configurable": {
                "thread_id": f"test-thread-{uuid.uuid4()}",
                "checkpoint_ns": "test",
            }
        }

        # Store checkpoint
        updated_config = checkpointer_config.put_checkpoint(
            config, TEST_DATA, metadata={"test": "metadata"}
        )

        # Verify the updated config has a checkpoint_id
        assert "checkpoint_id" in updated_config["configurable"]

        # Retrieve checkpoint
        result = checkpointer_config.get_checkpoint(updated_config)

        # Verify checkpoint data
        assert result is not None
        assert "messages" in result
        assert len(result["messages"]) == 2
        assert result["state"]["current_step"] == "greeting"

    def test_list_checkpoints(self, checkpointer_config):
        """Test listing checkpoints."""
        # Generate unique thread ID for this test
        thread_id = f"test-thread-{uuid.uuid4()}"
        config = {"configurable": {"thread_id": thread_id, "checkpoint_ns": "test"}}

        # Store multiple checkpoints
        for i in range(3):
            data = TEST_DATA.copy()
            data["state"] = TEST_DATA["state"].copy()
            data["state"]["step_index"] = i
            checkpointer_config.put_checkpoint(config, data)

        # List checkpoints
        checkpoints = checkpointer_config.list_checkpoints(config)

        # Verify checkpoints
        assert len(checkpoints) == 3


def test_setup_checkpointer():
    """Test the setup_checkpointer utility function."""

    # Create a mock agent config
    class MockAgentConfig:
        def __init__(self, persistence=None, name="test_agent"):
            self.persistence = persistence
            self.name = name

    # Test with no persistence
    agent_config = MockAgentConfig()
    checkpointer = setup_checkpointer(agent_config)
    assert checkpointer is not None

    # Test with memory persistence
    memory_config = create_memory_checkpointer()
    agent_config = MockAgentConfig(persistence=memory_config)
    checkpointer = setup_checkpointer(agent_config)
    assert checkpointer is not None

    # Test with SQLite persistence
    sqlite_config = create_sqlite_checkpointer(db_path=":memory:")
    agent_config = MockAgentConfig(persistence=sqlite_config)
    checkpointer = setup_checkpointer(agent_config)
    assert checkpointer is not None
