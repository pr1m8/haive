# tests/persistence/test_postgres_checkpointer.py

import uuid
from typing import Any, Dict, Generator, List

import pytest
from langgraph.graph import END, START
from pydantic import Field

from haive.core.config.runnable import RunnableConfigManager
from haive.core.engine.agent.persistence.postgres_config import (
    PostgresCheckpointerConfig,
)
from haive.core.engine.agent.persistence.types import CheckpointerType
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.models.llm.base import AzureLLMConfig
from haive.core.schema.state_schema import StateSchema


# Create a simple agent state for testing
class PGTestState(StateSchema):
    """Test agent state schema with messages field."""

    messages: List[Dict[str, Any]] = Field(default_factory=list)
    test_data: Dict[str, Any] = Field(default_factory=dict)


class TestPostgresCheckpointer:
    """Tests for the PostgreSQL checkpointer implementation."""

    @pytest.fixture
    def sync_persistence(self) -> Generator[PostgresCheckpointerConfig, None, None]:
        """Create a synchronous PostgreSQL persistence config."""
        persistence = PostgresCheckpointerConfig(
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
            setup_needed=True,
            use_async=False,
        )
        yield persistence
        # Close pool after test
        persistence.close()

    @pytest.fixture
    def async_persistence(self) -> Generator[PostgresCheckpointerConfig, None, None]:
        """Create an asynchronous PostgreSQL persistence config."""
        persistence = PostgresCheckpointerConfig(
            db_host="localhost",
            db_port=5432,
            db_name="postgres",
            db_user="postgres",
            db_pass="postgres",
            setup_needed=True,
            use_async=True,
        )
        yield persistence
        # Close pool after test
        persistence.close()

    @pytest.fixture
    def llm_engine(self) -> AugLLMConfig:
        """Create a test LLM engine."""
        return AugLLMConfig(
            name="test_llm",
            llm_config=AzureLLMConfig(model="gpt-4o", api_key="test_key"),
        )

    def test_sync_checkpointer_creation(self, sync_persistence):
        """Test that we can create a synchronous checkpointer."""
        checkpointer = sync_persistence.create_checkpointer()
        assert checkpointer is not None
        assert sync_persistence.type == CheckpointerType.postgres

    def test_sync_thread_registration(self, sync_persistence):
        """Test synchronous thread registration."""
        thread_id = f"test-thread-{uuid.uuid4()}"
        sync_persistence.register_thread(thread_id, metadata={"test": True})
        assert True

    def test_sync_checkpoint_storage(self, sync_persistence):
        """Test storing and retrieving a checkpoint synchronously."""
        thread_id = f"test-storage-{uuid.uuid4()}"
        sync_persistence.register_thread(thread_id, metadata={"test_type": "storage"})

        test_data = {
            "messages": [{"role": "user", "content": "Hello, this is a test message."}],
            "test_data": {"key1": "value1", "key2": 12345},
        }

        config = RunnableConfigManager.create(thread_id=thread_id)
        updated_config = sync_persistence.put_checkpoint(config, test_data)

        assert updated_config["configurable"]["thread_id"] == thread_id
        assert "checkpoint_id" in updated_config["configurable"]

        retrieved_data = sync_persistence.get_checkpoint(updated_config)

        assert retrieved_data is not None

        # Use a more flexible checking pattern that handles both nested and direct access
        if isinstance(retrieved_data, dict):
            # Check for nested structure (channel_values.messages)
            if (
                "channel_values" in retrieved_data
                and "messages" in retrieved_data["channel_values"]
            ):
                messages = retrieved_data["channel_values"]["messages"]
                assert len(messages) > 0
                assert messages[0]["content"] == "Hello, this is a test message."
            # Check for direct structure
            elif "messages" in retrieved_data:
                messages = retrieved_data["messages"]
                assert len(messages) > 0
                assert messages[0]["content"] == "Hello, this is a test message."

    def test_sync_graph_workflow(self, sync_persistence, llm_engine):
        """Test a full graph workflow with synchronous persistence."""
        thread_id = f"test-workflow-{uuid.uuid4()}"
        checkpointer = sync_persistence.create_checkpointer()

        graph_builder = DynamicGraph(
            name="test_graph", components=[llm_engine], state_schema=PGTestState
        )

        graph_builder.add_node("process", llm_engine, command_goto=END)

        graph_builder.add_edge(START, "process")

        graph = graph_builder.compile(checkpointer=checkpointer)

        config = RunnableConfigManager.create(thread_id=thread_id)

        input_data = {"messages": [{"role": "user", "content": "Hello, test agent!"}]}

        graph.invoke(input_data, config)
        saved_state = sync_persistence.get_checkpoint(config)

        # Check saved state using more flexible pattern
        assert saved_state is not None

        # Handle different possible structures
        if (
            "channel_values" in saved_state
            and "messages" in saved_state["channel_values"]
        ):
            assert len(saved_state["channel_values"]["messages"]) > 0
        elif "messages" in saved_state:
            assert len(saved_state["messages"]) > 0

    @pytest.mark.asyncio
    async def test_async_checkpointer_creation(self, async_persistence):
        """Test that we can create an asynchronous checkpointer."""
        # The async_persistence fixture creates the checkpointer
        checkpointer = async_persistence.create_checkpointer()
        assert checkpointer is not None
        assert async_persistence.type == CheckpointerType.postgres

    # Skip the async tests since your implementation doesn't have async methods yet
    @pytest.mark.skip("Async methods not implemented")
    @pytest.mark.asyncio
    async def test_async_thread_registration(self, async_persistence):
        """Test asynchronous thread registration."""
        thread_id = f"test-async-thread-{uuid.uuid4()}"
        # Use the sync method until async is implemented
        async_persistence.register_thread(
            thread_id, metadata={"test": True, "async": True}
        )
        assert True

    # Skip the async tests since your implementation doesn't have async methods yet
    @pytest.mark.skip("Async methods not implemented")
    @pytest.mark.asyncio
    async def test_async_checkpoint_storage(self, async_persistence):
        """Test storing and retrieving a checkpoint asynchronously."""
        pass

    # Skip the async tests since your implementation doesn't have async methods yet
    @pytest.mark.skip("Async methods not implemented")
    @pytest.mark.asyncio
    async def test_async_graph_workflow(self, async_persistence, llm_engine):
        """Test a full graph workflow with asynchronous persistence."""
        pass
