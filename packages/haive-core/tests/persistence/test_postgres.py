import logging
import time
import uuid
from typing import Any, Dict, List

import pytest
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.types import (
    CheckpointerMode,
    CheckpointerType,
    CheckpointStorageMode,
)

# Set up logging
logger = logging.getLogger(__name__)


# Define test state class
class _TestState(BaseModel):
    """Simple state model for testing."""

    messages: List[Any] = Field(default_factory=list)


# Basic node function for testing
def _simple_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """A simple node that adds an AI message."""
    logger.debug(f"Simple node processing state: {state}")

    # Get the last human message
    messages = state.messages
    last_message = messages[-1] if messages else None

    if isinstance(last_message, HumanMessage):
        # Create a response
        content = f"I received: {last_message.content}"
        response = AIMessage(content=content)

        # Return updated messages
        return Command(update={"messages": [response]})

    return {}


# Helper function to generate thread IDs
def _generate_thread_id() -> str:
    """Generate a unique thread ID for testing."""
    return f"test_{int(time.time()*1000)}_{uuid.uuid4().hex[:8]}"


# Test configuration basics
def test_postgres_config_creation(db_params):
    """Test creating PostgreSQL configurations."""
    # Test basic config
    config = PostgresCheckpointerConfig(**db_params)
    logger.info(f"Created config: {config}")
    assert config.type == CheckpointerType.POSTGRES

    # Test connection URI generation
    uri = config.get_connection_uri()
    logger.info(f"Connection URI: {uri}")
    assert config.db_host in uri
    assert str(config.db_port) in uri


# Test sync graph with checkpointer
def test_sync_graph_with_checkpointer(sync_postgres_config):
    """Test a synchronous graph with checkpointer."""
    # Create checkpointer
    checkpointer = sync_postgres_config.create_checkpointer()

    # Set up a simple graph
    builder = StateGraph(_TestState)
    builder.add_node("processor", _simple_node)
    builder.add_edge(START, "processor")
    builder.add_edge("processor", END)

    # Compile with checkpointer
    graph = builder.compile(checkpointer=checkpointer)

    # Create thread ID and config
    thread_id = _generate_thread_id()
    config = {"configurable": {"thread_id": thread_id}}

    # Send a message
    human_message = HumanMessage(content="Hello, test message")
    input_state = _TestState(messages=[human_message])

    # Invoke the graph
    logger.info(f"Invoking graph with thread_id={thread_id}")
    result = graph.invoke(input_state, config)

    # Verify result
    assert "messages" in result
    assert len(result["messages"]) > 0

    # Get checkpoint from checkpointer
    checkpoint = checkpointer.get(config)

    # Verify checkpoint exists and contains our message
    assert checkpoint is not None
    assert "messages" in checkpoint.get("channel_values", {})
    messages = checkpoint["channel_values"]["messages"]
    assert any("Hello, test message" in str(msg) for msg in messages)


@pytest.mark.asyncio
async def test_async_graph_with_checkpointer(async_postgres_config):
    """Test an asynchronous graph with checkpointer."""
    # Get the context manager
    async_context = async_postgres_config.create_async_checkpointer()

    # Use async with to properly manage the checkpointer lifecycle
    async with async_context() as checkpointer:
        # Set up a simple graph
        builder = StateGraph(_TestState)
        builder.add_node("processor", _simple_node)
        builder.add_edge(START, "processor")
        builder.add_edge("processor", END)

        # Compile with checkpointer
        graph = builder.compile(checkpointer=checkpointer)

        # Create thread ID and config
        thread_id = _generate_thread_id()
        config = {"configurable": {"thread_id": thread_id}}

        # Send a message
        human_message = HumanMessage(content="Hello, async test message")
        input_state = _TestState(messages=[human_message])

        # Invoke the graph asynchronously
        logger.info(f"Async invoking graph with thread_id={thread_id}")
        result = await graph.ainvoke(input_state, config)

        # Verify result
        assert "messages" in result
        assert len(result["messages"]) > 0

        # Get checkpoint from checkpointer
        checkpoint = await checkpointer.aget(config)

        # Verify checkpoint exists and contains our message
        assert checkpoint is not None
        assert "messages" in checkpoint.get("channel_values", {})
        messages = checkpoint["channel_values"]["messages"]
        assert any("Hello, async test message" in str(msg) for msg in messages)

    # When using async with, the pool is automatically closed outside this block


# Test shallow checkpointer
def test_shallow_checkpointer(shallow_postgres_config):
    """Test a shallow checkpointer that only keeps the latest state."""
    # Create checkpointer
    checkpointer = shallow_postgres_config.create_checkpointer()

    # Set up a simple graph
    builder = StateGraph(_TestState)
    builder.add_node("processor", _simple_node)
    builder.add_edge(START, "processor")
    builder.add_edge("processor", END)

    # Compile with checkpointer
    graph = builder.compile(checkpointer=checkpointer)

    # Create thread ID and config
    thread_id = _generate_thread_id()
    config = {"configurable": {"thread_id": thread_id}}

    # First invocation
    first_message = HumanMessage(content="First message")
    input_state1 = _TestState(messages=[first_message])

    logger.info(f"First invocation with thread_id={thread_id}")
    graph.invoke(input_state1, config)

    # Second invocation should overwrite previous state in shallow mode
    second_message = HumanMessage(content="Second message")
    input_state2 = _TestState(messages=[second_message])

    logger.info(f"Second invocation with thread_id={thread_id}")
    graph.invoke(input_state2, config)

    # Get the latest checkpoint
    checkpoint = checkpointer.get(config)

    # Verify it contains the second message
    assert checkpoint is not None
    assert "messages" in checkpoint.get("channel_values", {})
    messages = checkpoint["channel_values"]["messages"]
    assert any("Second message" in str(msg) for msg in messages)


@pytest.mark.asyncio
async def test_persistence_across_restarts(sync_postgres_config):
    """Test that state persists across checkpointer restarts."""
    # Create first checkpointer
    checkpointer1 = sync_postgres_config.create_checkpointer()

    try:
        # Set up a simple graph
        builder = StateGraph(_TestState)
        builder.add_node("processor", _simple_node)
        builder.add_edge(START, "processor")
        builder.add_edge("processor", END)

        # Compile with first checkpointer
        graph1 = builder.compile(checkpointer=checkpointer1)

        # Create thread ID and config
        thread_id = _generate_thread_id()
        config = {"configurable": {"thread_id": thread_id}}

        # First invocation with first checkpointer
        human_message = HumanMessage(content="Persistent message")
        input_state = _TestState(messages=[human_message])

        logger.info(f"First invocation with thread_id={thread_id}")
        graph1.invoke(input_state, config)

        # Create a new checkpointer (simulating a restart)
        logger.info("Creating a new checkpointer (simulating restart)")
        checkpointer2 = sync_postgres_config.create_checkpointer()

        try:
            # Get the state from the new checkpointer
            checkpoint = checkpointer2.get(config)

            # Verify the state was persisted
            assert checkpoint is not None
            assert "messages" in checkpoint.get("channel_values", {})
            messages = checkpoint["channel_values"]["messages"]
            assert any("Persistent message" in str(msg) for msg in messages)
        finally:
            # Clean up checkpointer2 explicitly if needed
            pass
    finally:
        # Clean up checkpointer1 explicitly if needed
        pass


# Fixtures (these should actually be in conftest.py)
@pytest.fixture(scope="module")
def db_params():
    """Get database parameters for testing."""
    return {
        "db_host": "localhost",
        "db_port": 5432,
        "db_name": "postgres",
        "db_user": "postgres",
        "db_pass": "postgres",
    }


@pytest.fixture(scope="function")
def sync_postgres_config(db_params):
    """Create a synchronous PostgreSQL config."""
    config = PostgresCheckpointerConfig(
        **db_params, mode=CheckpointerMode.SYNC, storage_mode=CheckpointStorageMode.FULL
    )
    return config


@pytest.fixture(scope="function")
def async_postgres_config(db_params):
    """Create an asynchronous PostgreSQL config."""
    config = PostgresCheckpointerConfig(
        **db_params,
        mode=CheckpointerMode.ASYNC,
        storage_mode=CheckpointStorageMode.FULL,
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
    return config
