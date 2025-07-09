# tests/graph/node/test_validation_node.py
from typing import Any, List

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command
from pydantic import Field

from haive.core.graph.node.types import NodeType
from haive.core.graph.node.validation_node_config import ValidationNodeConfig
from haive.core.schema.state_schema import StateSchema


# Define state schema (renamed to avoid pytest collection issues)
class _ValidationState(StateSchema):
    """State schema with messages and validation fields."""

    messages: List[Any] = Field(default_factory=list)
    validated: bool = Field(default=False)


# Define tool functions for validation
@tool
def get_weather(location: str, unit: str = "fahrenheit") -> str:
    """Get the current weather in a location."""
    return f"Weather in {location} is sunny and 75 degrees {unit}"


@tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    return f"Result: {eval(expression)}"


# Create test fixtures
@pytest.fixture
def validation_tools():
    """Create validation tools for testing."""
    return [get_weather, calculate]


@pytest.fixture
def validation_node_config(validation_tools):
    """Create a ValidationNodeConfig for testing."""
    return ValidationNodeConfig(
        name="validation_node",
        schemas=validation_tools,  # Use the tool functions directly
        messages_field="messages",
        validation_status_key="validated",
        command_goto="next_node",
    )


@pytest.fixture
def valid_state():
    """Create a state with valid tool calls."""
    return _ValidationState(
        messages=[
            HumanMessage(content="What's the weather in Seattle?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_123",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"location": "Seattle, WA", "unit": "fahrenheit"}',
                            },
                        }
                    ]
                },
            ),
        ]
    )


@pytest.fixture
def invalid_state():
    """Create a state with invalid tool calls (missing required field)."""
    return _ValidationState(
        messages=[
            HumanMessage(content="What's the weather like?"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "call_456",
                            "type": "function",
                            "function": {
                                "name": "get_weather",
                                "arguments": '{"unit": "celsius"}',
                            },
                        }
                    ]
                },
            ),
        ]
    )


@pytest.fixture
def mixed_state():
    """Create a state with both valid and invalid tool calls."""
    return _ValidationState(
        messages=[
            HumanMessage(content="Calculate 2+2 and check weather"),
            AIMessage(
                content="",
                additional_kwargs={
                    "tool_calls": [
                        {
                            "id": "calc_123",
                            "type": "function",
                            "function": {
                                "name": "calculate",
                                "arguments": '{"expression": "2+2"}',
                            },
                        },
                        {
                            "id": "weather_123",
                            "type": "function",
                            "function": {"name": "get_weather", "arguments": "{}"},
                        },
                    ]
                },
            ),
        ]
    )


# Test cases
def test_validation_config_creation(validation_node_config):
    """Test that ValidationNodeConfig can be created correctly."""
    assert validation_node_config.node_type == NodeType.VALIDATION
    assert validation_node_config.name == "validation_node"
    assert len(validation_node_config.schemas) == 2
    assert validation_node_config.messages_field == "messages"
    assert validation_node_config.validation_status_key == "validated"
    assert validation_node_config.command_goto == "next_node"


def test_valid_tool_call_validation(validation_node_config, valid_state):
    """Test validation with valid tool calls."""
    result = validation_node_config(valid_state)

    # Should be a Command object
    assert isinstance(result, Command)

    # Should set validated to True
    assert result.update["validated"] is True

    # Should not modify messages since validation passed
    assert "messages" not in result.update

    # Should include command_goto
    assert result.goto == "next_node"


def test_invalid_tool_call_validation(validation_node_config, invalid_state):
    """Test validation with invalid tool calls."""
    result = validation_node_config(invalid_state)

    # Should be a Command object
    assert isinstance(result, Command)

    # Should set validated to False
    assert result.update["validated"] is False

    # Should include updated messages with error
    assert "messages" in result.update

    # Check that messages contain validation error in ToolMessage
    messages = result.update["messages"]
    error_found = False

    for msg in messages:
        if isinstance(msg, ToolMessage) and msg.name == "get_weather":
            # Check if the content contains an error message
            if "validation error" in msg.content and "location" in msg.content:
                error_found = True
                break

    assert error_found, "No validation error found in ToolMessages for get_weather"

    # Should include command_goto
    assert result.goto == "next_node"


def test_mixed_validation_state(validation_node_config, mixed_state):
    """Test validation with both valid and invalid tool calls."""
    result = validation_node_config(mixed_state)

    # Should be a Command object
    assert isinstance(result, Command)

    # Even one invalid call should set validated to False
    assert result.update["validated"] is False

    # Should include updated messages with error
    assert "messages" in result.update

    # Check both valid and invalid messages
    messages = result.update["messages"]

    # The calculate tool should have a successful tool call
    calculate_found = False
    weather_error_found = False

    for msg in messages:
        if isinstance(msg, ToolMessage):
            if msg.name == "calculate":
                # Should not contain error message
                if "validation error" not in msg.content:
                    calculate_found = True

            if msg.name == "get_weather":
                # Should contain error message
                if "validation error" in msg.content and "location" in msg.content:
                    weather_error_found = True

    assert calculate_found, "Valid calculate tool call not found"
    assert weather_error_found, "Validation error for get_weather not found"


def test_command_goto_propagation(validation_tools):
    """Test that command_goto is properly propagated."""
    # Create validation node with different command_goto
    node_config = ValidationNodeConfig(
        name="validation_node", schemas=validation_tools, command_goto="alternate_node"
    )

    # Test with simple state
    simple_state = _ValidationState(
        messages=[
            HumanMessage(content="Hello"),
            AIMessage(content=""),  # Empty content but still an AIMessage
        ]
    )

    result = node_config(simple_state)

    # Should include command_goto
    assert result.goto == "alternate_node"


def test_no_command_goto(validation_tools, valid_state):
    """Test behavior when command_goto is not specified."""
    # Create validation node without command_goto
    node_config = ValidationNodeConfig(
        name="validation_node", schemas=validation_tools, command_goto=None
    )

    result = node_config(valid_state)

    # Should still be a Command
    assert isinstance(result, Command)

    # But goto should be None
    assert result.goto is None
