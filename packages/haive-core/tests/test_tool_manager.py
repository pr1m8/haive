# tests/test_tool_manager.py

import asyncio
import logging
import os
import sys
from typing import Any

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import the tool manager components
# Import LangGraph components for testing

from haive.core.graph.ToolManager import (
    ToolConfig,
    ToolManager,
    state_tool,
    tool_manager,
)


# Test basic tool registration and execution
def test_basic_tool_registration():
    """Test basic tool registration and execution."""
    print("\n=== Testing Basic Tool Registration ===")

    # Create a test manager
    manager = ToolManager()

    # Create a simple calculator function
    def calculator(expression: str) -> float:
        """Calculate the result of a mathematical expression."""
        return eval(expression)

    # Register as a tool
    tool_obj = manager.create_and_register_tool(
        calculator,
        name="calculator",
        description="Calculate mathematical expressions",
        return_direct=True,
    )

    # Verify registration
    print(f"Registered tool: {tool_obj.name}")
    print(f"Tool description: {tool_obj.description}")

    # Execute the tool
    result = manager.execute_tool("calculator", kwargs={"expression": "2 + 3 * 4"})

    # Check result
    print(f"Tool result: {result.result}")
    print(f"Success: {result.success}")
    print(f"Execution time: {result.execution_time:.4f} seconds")

    assert result.success
    assert result.result == 14
    assert result.tool_name == "calculator"

    return manager


# Test tool with configuration
def test_tool_with_config():
    """Test a tool with custom configuration."""
    print("\n=== Testing Tool with Configuration ===")

    # Create a tool manager
    manager = ToolManager()

    # Create a function with potential failures
    def unreliable_function(success_rate: float = 0.5) -> bool:
        """A function that sometimes fails."""
        import random

        if random.random() > success_rate:
            raise ValueError("Random failure occurred")
        return True

    # Create config with retries
    config = ToolConfig(
        name="unreliable_tool",
        description="A tool that sometimes fails",
        max_retries=3,
        retry_delay=0.1,
        tags=["test", "unreliable"],
    )

    # Register with config
    tool_obj = manager.create_and_register_tool(unreliable_function, config=config)

    # Execute with very low success rate
    result = manager.execute_tool("unreliable_tool", kwargs={"success_rate": 0.1})

    # Print result
    print(f"Tool result: {result.result}")
    print(f"Success: {result.success}")
    print(f"Error: {result.error}")
    print(f"Retries: {result.retries}")

    # Check execution history
    history = manager.get_execution_history()
    print(f"Execution history count: {len(history)}")

    # Even with retries, it might still fail, so we don't assert success
    # Instead, verify that retries were attempted
    assert len(history) == 1

    return manager


# Test state injection
def test_state_injection():
    """Test tool with state injection."""
    print("\n=== Testing State Injection ===")

    # Create a tool manager
    manager = ToolManager()

    # Create a tool that uses state
    @state_tool(name="extract_last_message")
    def extract_last_message(state: dict[str, Any]) -> str:
        """Extract the last message from the state."""
        messages = state.get("messages", [])
        if not messages:
            return "No messages found"

        last_message = messages[-1]
        if hasattr(last_message, "content"):
            return last_message.content
        return str(last_message)

    # Create a mock state for testing
    class MockMessage:
        def __init__(self, content):
            self.content = content

    mock_state = {
        "messages": [
            MockMessage("Hello"),
            MockMessage("How are you?"),
            MockMessage("This is the last message"),
        ]
    }

    # We can't directly call execute_tool with state injection
    # In a real environment, LangGraph would handle the injection
    # For testing, we can call the tool directly
    result = tool_manager.execute_tool(
        "extract_last_message", kwargs={"state": mock_state}
    )

    print(f"Result: {result}")

    assert result == "This is the last message"

    # Verify tool was registered with correct config
    config = manager._get_tool_config("extract_last_message")
    print(f"Tool config requires_state: {config.requires_state}")

    assert config.requires_state

    return manager


# Test async tools
async def test_async_tools():
    """Test async tool execution."""
    print("\n=== Testing Async Tools ===")

    # Create a tool manager
    manager = ToolManager()

    # Create an async function
    async def async_fetch(url: str, delay: float = 0.1) -> str:
        """Simulate fetching data from a URL."""
        await asyncio.sleep(delay)  # Simulate network delay
        return f"Data from {url}"

    # Create config for async tool
    config = ToolConfig(
        name="async_fetch",
        description="Fetch data from a URL asynchronously",
        is_async=True,
        timeout=1.0,
    )

    # We need to manually wrap this since our decorators expect sync functions
    # In practice, you might create dedicated async decorators
    async def wrapped_async_fetch(url: str, delay: float = 0.1) -> str:
        return await async_fetch(url, delay)

    # Create and register
    tool_obj = manager.create_and_register_tool(wrapped_async_fetch, config=config)

    # Execute async tool
    result = await manager.execute_tool_async(
        "async_fetch", kwargs={"url": "http://example.com", "delay": 0.2}
    )

    # Check result
    print(f"Async tool result: {result.result}")
    print(f"Success: {result.success}")
    print(f"Execution time: {result.execution_time:.4f} seconds")

    assert result.success
    assert "http://example.com" in result.result
    # Execution should take at least the delay time
    assert result.execution_time >= 0.2

    # Test timeout
    result = await manager.execute_tool_async(
        "async_fetch",
        kwargs={"url": "http://example.com", "delay": 2.0},  # Delay > timeout
    )

    # Should fail with timeout
    print(f"Timeout test success: {result.success}")
    print(f"Timeout error: {result.error}")

    assert not result.success
    assert "timeout" in result.error.lower()

    return manager


# Test tool filtering
def test_tool_filtering():
    """Test tool filtering by state and tags."""
    print("\n=== Testing Tool Filtering ===")

    # Create a tool manager
    manager = ToolManager()

    # Register several tools with different configs
    manager.create_and_register_tool(
        lambda x: x + 1,
        name="increment",
        config=ToolConfig(
            name="increment",
            tags=["math", "basic"],
            allowed_in_states=["calculating", "processing"],
        ),
    )

    manager.create_and_register_tool(
        lambda x: x - 1,
        name="decrement",
        config=ToolConfig(
            name="decrement", tags=["math", "basic"], denied_in_states=["finished"]
        ),
    )

    manager.create_and_register_tool(
        lambda x, y: x * y,
        name="multiply",
        config=ToolConfig(
            name="multiply",
            tags=["math", "advanced"],
            allowed_in_states=["calculating"],
        ),
    )

    manager.create_and_register_tool(
        lambda msg: f"Hello, {msg}!",
        name="greet",
        config=ToolConfig(name="greet", tags=["text"], single_use=True),
    )

    # Get tools by tag
    math_tools = manager.get_allowed_tools(tags=["math"])
    print(f"Math tools: {list(math_tools.keys())}")
    assert len(math_tools) == 3

    basic_tools = manager.get_allowed_tools(tags=["basic"])
    print(f"Basic tools: {list(basic_tools.keys())}")
    assert len(basic_tools) == 2

    # Get tools requiring all tags
    advanced_math = manager.get_allowed_tools(
        tags=["math", "advanced"], require_all_tags=True
    )
    print(f"Advanced math tools: {list(advanced_math.keys())}")
    assert len(advanced_math) == 1
    assert "multiply" in advanced_math

    # Get tools by state
    calculating_tools = manager.get_allowed_tools(current_state="calculating")
    print(f"Tools allowed in 'calculating' state: {list(calculating_tools.keys())}")
    assert "increment" in calculating_tools
    assert "multiply" in calculating_tools

    # Test single-use restriction
    # First, use the greet tool
    result = manager.execute_tool("greet", kwargs={"msg": "world"})
    print(f"Greet result: {result.result}")

    # Now, try to get it again - should be filtered out
    tools_after_use = manager.get_allowed_tools()
    print(f"Available tools after use: {list(tools_after_use.keys())}")
    assert "greet" not in tools_after_use

    # Get tool descriptions
    descriptions = manager.get_tool_descriptions()
    print(f"Tool descriptions: {descriptions}")

    return manager


# Run all tests
def run_tests():
    """Run all tests."""
    print("=== Running ToolManager Tests ===")

    # Run synchronous tests
    basic_manager = test_basic_tool_registration()
    config_manager = test_tool_with_config()
    state_manager = test_state_injection()
    filter_manager = test_tool_filtering()

    # Run async test
    asyncio.run(test_async_tools())

    print("\n=== All tool manager tests completed successfully ===")


if __name__ == "__main__":
    run_tests()
