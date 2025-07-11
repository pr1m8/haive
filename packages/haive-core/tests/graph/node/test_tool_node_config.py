from typing import Annotated, List

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langgraph.graph import add_messages
from langgraph.types import Command
from pydantic import Field

from haive.core.graph.node.tool_node_config import ToolNodeConfig
from haive.core.schema.state_schema import StateSchema


class CalculatorState(StateSchema):
    """Simple state schema for testing the tool node."""

    messages: List[Annotated[BaseMessage, add_messages]] = Field(default_factory=list)
    result: str = Field(default="")


def test_tool_node_config():
    """Test the ToolNodeConfig with actual tool execution."""

    # Define a simple calculator tool
    def calculator(a: int, b: int, operation: str) -> str:
        """Perform a simple calculation."""
        if operation == "add":
            return f"The result of {a} + {b} = {a + b}"
        elif operation == "subtract":
            return f"The result of {a} - {b} = {a - b}"
        elif operation == "multiply":
            return f"The result of {a} * {b} = {a * b}"
        elif operation == "divide":
            if b == 0:
                raise ValueError("Cannot divide by zero")
            return f"The result of {a} / {b} = {a / b}"
        else:
            raise ValueError(f"Unknown operation: {operation}")

    calculator_tool = StructuredTool.from_function(
        func=calculator,
        name="calculator",
        description="Perform calculations like add, subtract, multiply, divide",
    )

    # Create the tool node config
    tool_node_config = ToolNodeConfig(
        name="calculator_node", tools=[calculator_tool], command_goto="next_node"
    )

    # Create an initial state with a tool call message
    initial_state = CalculatorState(
        messages=[
            HumanMessage(content="What is 5 + 3?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {
                                "name": "calculator",
                                "arguments": '{"a": 5, "b": 3, "operation": "add"}',
                            },
                        }
                    ]
                },
            ),
        ]
    )

    # Execute the tool node
    result = tool_node_config(initial_state)
    print(result)
    # Check that the result is a Command
    assert isinstance(result, Command)

    # Check that the Command has the expected goto
    assert result.goto == "next_node"

    # Check that the Command's update contains the messages key
    assert "messages" in result.update

    # Check that the new messages include a tool message with the result
    updated_messages = result.update["messages"]
    assert any(isinstance(msg, ToolMessage) for msg in updated_messages)

    # Find the tool message and check its content
    tool_messages = [msg for msg in updated_messages if isinstance(msg, ToolMessage)]
    assert len(tool_messages) > 0
    assert "The result of 5 + 3 = 8" in tool_messages[0].content


def test_tool_node_error_handling():
    """Test the ToolNodeConfig with tool execution error."""

    # Define a division tool that might raise errors
    def divide(a: int, b: int) -> str:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return f"The result of {a} / {b} = {a / b}"

    divide_tool = StructuredTool.from_function(
        func=divide, name="divide", description="Divide two numbers"
    )

    # Create the tool node config with error handling
    tool_node_config = ToolNodeConfig(
        name="division_node",
        tools=[divide_tool],
        handle_tool_errors=True,
        command_goto="error_handler",
    )

    # Create an initial state with a division by zero
    initial_state = CalculatorState(
        messages=[
            HumanMessage(content="What is 10 divided by 0?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_456",
                            "type": "function",
                            "function": {
                                "name": "divide",
                                "arguments": '{"a": 10, "b": 0}',
                            },
                        }
                    ]
                },
            ),
        ]
    )

    # Execute the tool node
    result = tool_node_config(initial_state)

    # Check that the result is a Command
    assert isinstance(result, Command)

    # Check that the Command has the expected goto
    assert result.goto == "error_handler"

    # Check that the Command's update contains the messages key
    assert "messages" in result.update

    # Find the tool message and check that it contains an error
    tool_messages = [
        msg for msg in result.update["messages"] if isinstance(msg, ToolMessage)
    ]
    assert len(tool_messages) > 0
    assert (
        "error" in tool_messages[0].content.lower()
        or "divide by zero" in tool_messages[0].content.lower()
    )
