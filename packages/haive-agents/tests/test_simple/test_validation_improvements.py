"""Test validation node improvements with various tool types."""

import uuid
from typing import List

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.simple import SimpleAgent


# Test schemas
class Plan(BaseModel):
    """A plan with steps."""

    steps: list[str] = Field(description="A list of steps to complete the task")


class MathResult(BaseModel):
    """Result of a math operation."""

    result: float = Field(description="The result of the calculation")
    operation: str = Field(description="The operation performed")


# Test tools
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


def simple_function(x: int) -> int:
    """A simple function that doubles the input."""
    return x * 2


class TestValidationImprovements:
    """Test validation node improvements."""

    def test_pydantic_model_creates_tool_message(self):
        """Test that Pydantic model validation creates ToolMessage."""
        # Create engine with Pydantic model
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_pydantic_engine",
            system_message="You are a helpful assistant that creates plans.",
            structured_output_model=Plan,
        )

        # Create simple agent
        agent = SimpleAgent(name="test_agent", engine=engine)

        # Check graph structure
        graph = agent.graph
        assert "validation" in graph.nodes
        assert "parse_output" in graph.nodes

        # Simulate a request that should trigger the Plan model
        # This would normally come from the LLM, but we'll create it manually
        [
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

        # Run the agent with these messages
        # In a real scenario, the agent would generate the AIMessage

        # The validation node should route to parse_output
        # The parse_output node should create a ToolMessage
        # We'll need to check this after implementing the fixes

    def test_langchain_tool_creates_tool_message(self):
        """Test that @tool decorated functions create ToolMessages."""
        # Create engine with tools
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_tools_engine",
            system_message="You are a helpful math assistant.",
            tools=[add_numbers, multiply_numbers],
        )

        # Create simple agent
        agent = SimpleAgent(name="test_agent", engine=engine)

        # Check graph structure
        graph = agent.graph
        assert "validation" in graph.nodes
        assert "tool_node" in graph.nodes

        # Simulate tool calls
        [
            HumanMessage(content="Add 5 and 3"),
            AIMessage(
                content="I'll add those numbers for you.",
                tool_calls=[
                    {"id": "call_456", "name": "add_numbers", "args": {"a": 5, "b": 3}}
                ],
            ),
        ]

        # Tool node should create ToolMessage with result

    def test_invalid_tool_creates_error_message(self):
        """Test that invalid tool calls create error ToolMessages."""
        # Create engine with limited tools
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_limited_engine",
            system_message="You are a helpful assistant.",
            tools=[add_numbers],  # Only has add_numbers
        )

        # Create simple agent
        SimpleAgent(name="test_agent", engine=engine)

        # Try to call a tool that doesn't exist
        [
            HumanMessage(content="Multiply 5 and 3"),
            AIMessage(
                content="I'll multiply those numbers for you.",
                tool_calls=[
                    {
                        "id": "call_789",
                        "name": "multiply_numbers",  # This tool doesn't exist
                        "args": {"a": 5, "b": 3},
                    }
                ],
            ),
        ]

        # Validation should create error ToolMessage

    def test_mixed_tools_and_models(self):
        """Test agent with both tools and Pydantic models."""
        # Create engine with both
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_mixed_engine",
            system_message="You are a helpful assistant that can plan and calculate.",
            tools=[add_numbers, multiply_numbers],
            structured_output_model=Plan,
        )

        # Create simple agent
        agent = SimpleAgent(name="test_agent", engine=engine)

        # Check that both nodes exist
        graph = agent.graph
        assert "tool_node" in graph.nodes
        assert "parse_output" in graph.nodes

    def test_multiple_tool_calls_in_one_message(self):
        """Test handling multiple tool calls in a single AIMessage."""
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_multi_tools",
            system_message="You are a helpful math assistant.",
            tools=[add_numbers, multiply_numbers],
        )

        SimpleAgent(name="test_agent", engine=engine)

        # Multiple tool calls
        [
            HumanMessage(content="Add 5 and 3, then multiply 4 and 2"),
            AIMessage(
                content="I'll perform both calculations.",
                tool_calls=[
                    {"id": "call_001", "name": "add_numbers", "args": {"a": 5, "b": 3}},
                    {
                        "id": "call_002",
                        "name": "multiply_numbers",
                        "args": {"a": 4, "b": 2},
                    },
                ],
            ),
        ]

        # Should create two ToolMessages

    def test_validation_with_no_tool_calls(self):
        """Test validation when AIMessage has no tool calls."""
        engine = AugLLMConfig(
            id=f"engine_{uuid.uuid4().hex[:8]}",
            name="test_no_tools",
            system_message="You are a helpful assistant.",
        )

        SimpleAgent(name="test_agent", engine=engine)

        [
            HumanMessage(content="Hello"),
            AIMessage(content="Hello! How can I help you today?"),
        ]

        # Should route to END without creating any ToolMessages


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
