"""Test Pydantic models in LangGraph state."""

import asyncio
from typing import List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from pydantic import BaseModel, Field


# Test nested Pydantic models
class NestedModel(BaseModel):
    value: str
    count: int


class ComplexModel(BaseModel):
    name: str
    nested: NestedModel
    items: list[str]


# Test state with Pydantic models
class TestState(BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)
    simple_field: str = "test"
    nested_model: NestedModel = Field(
        default_factory=lambda: NestedModel(value="default", count=0)
    )
    complex_model: ComplexModel | None = None

    # This is what's causing issues - storing a TYPE not an instance
    model_type: type[BaseModel] | None = None


def test_node(state: TestState):
    """Test node that works with Pydantic state."""

    # Add a message
    new_messages = [*state.messages, AIMessage(content="Test response")]

    # Update nested model
    new_nested = NestedModel(value="updated", count=state.nested_model.count + 1)

    return {
        "messages": new_messages,
        "nested_model": new_nested,
        "complex_model": ComplexModel(
            name="test", nested=new_nested, items=["a", "b", "c"]
        ),
    }


async def test_pydantic_state():
    """Test Pydantic models in LangGraph state."""

    # Build graph
    graph = StateGraph(TestState)
    graph.add_node("test", test_node)
    graph.add_edge(START, "test")
    graph.add_edge("test", END)

    # Test with different checkpointers
    import os

    import psycopg
    from langgraph.checkpoint.memory import MemorySaver
    from langgraph.checkpoint.postgres import PostgresSaver
    from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

    # In-memory checkpointer (should work)
    graph.compile(checkpointer=MemorySaver())

    # PostgreSQL checkpointer (might fail)
    postgres_app = None
    try:
        # Get connection string from environment
        db_url = os.environ.get("DATABASE_URL", "postgresql://localhost:5432/haive")
        with psycopg.connect(db_url) as conn:
            checkpointer = PostgresSaver(conn)
            graph.compile(checkpointer=checkpointer)
    except Exception as e:
        pass

    # Test 1: With Pydantic model instances (should work)
    initial_state = TestState(
        messages=[HumanMessage(content="Hello")],
        nested_model=NestedModel(value="initial", count=5),
    )

    try:
        result = await app.ainvoke(initial_state)
    except Exception as e:
        pass")

    # Test 2: With model type field (this is the problem)
    state_with_type = TestState(
        messages=[HumanMessage(content="Hello")],
        model_type=NestedModel,  # Storing the CLASS not an instance
    )

    try:
        result = await app.ainvoke(state_with_type)
    except Exception as e:


if __name__ == "__main__":
    asyncio.run(test_pydantic_state())
