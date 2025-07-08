"""Test validation improvements by actually invoking agents."""

import asyncio
import uuid
from typing import List
from pydantic import BaseModel, Field
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

from haive.core.engine.aug_llm import AugLLMConfig
from haive.agents.simple import SimpleAgent


# Test schemas
class Plan(BaseModel):
    """A plan with steps."""
    steps: List[str] = Field(description="A list of steps to complete the task")


# Test tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


async def test_pydantic_tool_message_creation():
    """Test that Pydantic model validation creates ToolMessage."""
    print("\n=== Testing Pydantic Model ToolMessage Creation ===")
    
    # Create engine with Pydantic model
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_pydantic_engine",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
    )
    
    # Create simple agent
    agent = SimpleAgent(
        name="test_agent",
        engine=engine
    )
    
    # Create initial state with tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Create a plan for making coffee"),
            AIMessage(
                content="I'll create a plan for making coffee.",
                tool_calls=[{
                    "id": "call_123",
                    "name": "Plan",
                    "args": {
                        "steps": [
                            "Boil water",
                            "Grind coffee beans",
                            "Add coffee to filter",
                            "Pour hot water over coffee",
                            "Wait 4 minutes",
                            "Enjoy"
                        ]
                    }
                }]
            )
        ]
    }
    
    # Run through the graph step by step
    print("\nInitial messages:")
    for i, msg in enumerate(initial_state["messages"]):
        print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
    
    # Get the compiled graph
    graph = agent.create_runnable()
    
    # Run the graph with config
    config = {"configurable": {"thread_id": f"test_thread_{uuid.uuid4().hex[:8]}"}}
    result = await graph.ainvoke(initial_state, config=config)
    
    print("\nFinal messages:")
    for i, msg in enumerate(result["messages"]):
        print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
        if isinstance(msg, ToolMessage):
            print(f"      Tool: {msg.name}, ID: {msg.tool_call_id}")
            print(f"      Content: {msg.content[:200]}...")
    
    # Check if ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]
    assert len(tool_messages) > 0, "No ToolMessage found after Pydantic validation"
    
    # Check the content
    tool_msg = tool_messages[0]
    assert tool_msg.name == "Plan"
    assert tool_msg.tool_call_id == "call_123"
    assert "steps" in tool_msg.content or "Boil water" in tool_msg.content
    
    print("\n✅ Pydantic model correctly created ToolMessage")
    return result


async def test_regular_tool_message_creation():
    """Test that regular tools create ToolMessages."""
    print("\n=== Testing Regular Tool ToolMessage Creation ===")
    
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
        engine=engine
    )
    
    # Create initial state with tool call
    initial_state = {
        "messages": [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[{
                    "id": "call_456",
                    "name": "add_numbers",
                    "args": {"a": 5, "b": 3}
                }]
            )
        ]
    }
    
    # Run the graph
    graph = agent.create_runnable()
    config = {"configurable": {"thread_id": f"test_thread_{uuid.uuid4().hex[:8]}"}}
    result = await graph.ainvoke(initial_state, config=config)
    
    print("\nFinal messages:")
    for i, msg in enumerate(result["messages"]):
        print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
        if isinstance(msg, ToolMessage):
            print(f"      Tool: {msg.name}, ID: {msg.tool_call_id}")
            print(f"      Content: {msg.content}")
    
    # Check if ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]
    assert len(tool_messages) > 0, "No ToolMessage found after tool execution"
    
    tool_msg = tool_messages[0]
    assert tool_msg.name == "add_numbers"
    assert tool_msg.tool_call_id == "call_456"
    assert "8" in str(tool_msg.content) or tool_msg.content == 8.0
    
    print("\n✅ Regular tool correctly created ToolMessage")
    return result


async def test_invalid_tool_error_message():
    """Test that invalid tool calls create error ToolMessages."""
    print("\n=== Testing Invalid Tool Error Message Creation ===")
    
    # Create engine with limited tools
    engine = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="test_limited_engine",
        system_message="You are a helpful assistant.",
        tools=[add_numbers],  # Only has add_numbers
    )
    
    # Create simple agent
    agent = SimpleAgent(
        name="test_agent",
        engine=engine
    )
    
    # Try to call a tool that doesn't exist
    initial_state = {
        "messages": [
            HumanMessage(content="Multiply 5 and 3"),
            AIMessage(
                content="I'll multiply those numbers for you.",
                tool_calls=[{
                    "id": "call_789",
                    "name": "multiply_numbers",  # This tool doesn't exist
                    "args": {"a": 5, "b": 3}
                }]
            )
        ]
    }
    
    # Run the graph
    graph = agent.create_runnable()
    config = {"configurable": {"thread_id": f"test_thread_{uuid.uuid4().hex[:8]}"}}
    result = await graph.ainvoke(initial_state, config=config)
    
    print("\nFinal messages:")
    for i, msg in enumerate(result["messages"]):
        print(f"  [{i}] {type(msg).__name__}: {str(msg)[:100]}...")
        if isinstance(msg, ToolMessage):
            print(f"      Tool: {msg.name}, ID: {msg.tool_call_id}")
            print(f"      Content: {msg.content}")
            if hasattr(msg, "additional_kwargs"):
                print(f"      Error: {msg.additional_kwargs.get('is_error', False)}")
    
    # Check if error ToolMessage was created
    tool_messages = [msg for msg in result["messages"] if isinstance(msg, ToolMessage)]
    assert len(tool_messages) > 0, "No ToolMessage found for invalid tool"
    
    tool_msg = tool_messages[0]
    assert tool_msg.name == "multiply_numbers"
    assert "error" in tool_msg.content.lower() or "not found" in tool_msg.content.lower()
    
    print("\n✅ Invalid tool correctly created error ToolMessage")
    return result


async def main():
    """Run all tests."""
    try:
        await test_pydantic_tool_message_creation()
        await test_regular_tool_message_creation()
        await test_invalid_tool_error_message()
        print("\n🎉 All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())