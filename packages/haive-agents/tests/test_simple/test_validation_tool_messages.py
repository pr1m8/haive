"""Test validation improvements by actually invoking agents."""

import asyncio
import uuid
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent


# Test schemas
class Plan(BaseModel):
    """A plan with steps."""

    steps: list[str] = Field(description="A list of steps to complete the task")


# Test tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


async def test_pydantic_tool_message_creation():
    """Test that Pydantic model validation creates ToolMessage."""

    # Create engine with Pydantic model
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_pydantic_engine",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
    )

    # Create simple agent without persistence for testing
    agent = SimpleAgent(
        name="test_agent",
        engine=engine,
        enable_persistence=False,  # Disable for testing
    )

    # Create initial state with tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Create a plan for making coffee"),
            AIMessage(
                content="I'll create a plan for making coffee.",
                tool_calls=[
                    {
                        "id": "call_123",
                        "name": "Plan",
                        "args": {
                            "steps": [
                                "Boil water",
                                "Grind coffee beans",
                                "Add coffee to filter",
                                "Pour hot water over coffee",
                                "Wait 4 minutes",
                                "Enjoy",
                            ]
                        },
                    }
                ],
            ),
        ]
    }

    # Run through the graph step by step
    for i, msg in enumerate(initial_state["messages"]):
        pass

    # Get the compiled graph
    graph = agent.create_runnable()

    # Run the graph
    result = await graph.ainvoke(initial_state)

    for i, msg in enumerate(result["messages"]):
        if isinstance(msg, ToolMessage):

    # Check if ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    # This is what we want to verify - currently it might fail
    if len(tool_messages) == 0:
        return False

    # Check the content
    tool_msg = tool_messages[0]
    assert tool_msg.name == "Plan"
    assert tool_msg.tool_call_id == "call_123"
    assert "steps" in tool_msg.content or "Boil water" in tool_msg.content

    return True


async def test_regular_tool_message_creation():
    """Test that regular tools create ToolMessages."""

    # Create engine with tools
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_tools_engine",
        system_message="You are a helpful math assistant.",
        tools=[add_numbers],
    )

    # Create simple agent
    agent = SimpleAgent(
        name="test_agent",
        engine=engine,
        enable_persistence=False,  # Disable for testing
    )

    # Create initial state with tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[
                    {"id": "call_456", "name": "add_numbers", "args": {"a": 5, "b": 3}}
                ],
            ),
        ]
    }

    # Run the graph
    graph = agent.create_runnable()
    result = await graph.ainvoke(initial_state)

    for i, msg in enumerate(result["messages"]):
        if isinstance(msg, ToolMessage):

    # Check if ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]

    if len(tool_messages) == 0:
        return False

    tool_msg = tool_messages[0]
    assert tool_msg.name == "add_numbers"
    assert tool_msg.tool_call_id == "call_456"
    assert "8" in str(tool_msg.content) or tool_msg.content == 8.0

    return True


async def main():
    """Run all tests to see current behavior."""

    results = []

    try:
        result1 = await test_pydantic_tool_message_creation()
        results.append(("Pydantic", result1))
    except Exception as e:
        results.append(("Pydantic", False))

    try:
        result2 = await test_regular_tool_message_creation()
        results.append(("Regular Tool", result2))
    except Exception as e:
        results.append(("Regular Tool", False))

    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"

    if not all(result for _, result in results):
        passix!")
    else:
        pass!")


if __name__ == "__main__":
    asyncio.run(main())
