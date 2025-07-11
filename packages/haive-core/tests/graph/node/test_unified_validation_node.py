"""
Test cases for the unified validation node.
"""

from typing import Any, Dict

import pytest
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command, Send
from pydantic import BaseModel, Field

from haive.core.graph.node.types import NodeType
from haive.core.graph.node.unified_validation_node import (
    UnifiedValidationNodeConfig,
    create_unified_validation_node,
)


# Test models and tools
class UserQuery(BaseModel):
    """Test model for structured output."""

    question: str = Field(description="User's question")
    priority: int = Field(description="Priority level 1-10")


class SearchRequest(BaseModel):
    """Another test model."""

    query: str = Field(description="Search query")
    max_results: int = Field(default=10)


@tool
def calculate(expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression, {"__builtins__": {}}, {})


@tool
def search_web(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"


class MockEngine:
    """Mock engine for testing."""

    def __init__(self, tool_routes=None, schemas=None, tools=None):
        self.tool_routes = tool_routes or {}
        self.schemas = schemas or []
        self.tools = tools or []
        self.structured_output_model = None


class TestUnifiedValidationNode:
    """Test cases for UnifiedValidationNodeConfig."""

    def test_basic_instantiation(self):
        """Test basic node creation."""
        node = UnifiedValidationNodeConfig(
            name="test_validation", engine_name="test_engine"
        )

        assert node.name == "test_validation"
        assert node.engine_name == "test_engine"
        assert node.node_type == NodeType.CALLABLE
        assert node.tool_node == "tool_node"
        assert node.parse_output_node == "parse_output"
        assert node.agent_node == "agent_node"
        assert node.create_tool_messages is True
        assert node.parallel_execution is True

    def test_factory_function(self):
        """Test factory function creation."""
        node = create_unified_validation_node(
            name="factory_node",
            engine_name="factory_engine",
            tool_node="custom_tool_node",
        )

        assert node.name == "factory_node"
        assert node.engine_name == "factory_engine"
        assert node.tool_node == "custom_tool_node"

    def test_no_messages_routing(self):
        """Test routing when no messages present."""
        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {"messages": [], "engines": {}}
        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "agent_node"
        assert result.update == {}

    def test_no_tool_calls_routing(self):
        """Test routing when no tool calls in messages."""
        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Hello"),
                AIMessage(content="Hi there!"),  # No tool calls
            ],
            "engines": {},
        }
        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "agent_node"

    def test_pydantic_model_validation_success(self):
        """Test successful Pydantic model validation."""
        engine = MockEngine(
            tool_routes={"UserQuery": "pydantic_model"}, schemas=[UserQuery]
        )

        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(
                    content="Using UserQuery",
                    tool_calls=[
                        {
                            "name": "UserQuery",
                            "args": {"question": "What is AI?", "priority": 5},
                            "id": "call_1",
                        }
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "parse_output"
        assert "messages" in result.update
        assert len(result.update["messages"]) == 1
        assert isinstance(result.update["messages"][0], ToolMessage)
        assert "successful" in result.update["messages"][0].content.lower()

    def test_pydantic_model_validation_error(self):
        """Test Pydantic model validation with error."""
        engine = MockEngine(
            tool_routes={"UserQuery": "pydantic_model"}, schemas=[UserQuery]
        )

        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(
                    content="Using UserQuery",
                    tool_calls=[
                        {
                            "name": "UserQuery",
                            "args": {"question": "What is AI?"},  # Missing priority
                            "id": "call_1",
                        }
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "agent_node"  # Routes to agent on error
        assert "messages" in result.update
        assert len(result.update["messages"]) == 1
        assert isinstance(result.update["messages"][0], ToolMessage)
        assert "error" in result.update["messages"][0].content.lower()

    def test_langchain_tool_routing(self):
        """Test routing for langchain tools."""
        engine = MockEngine(
            tool_routes={"calculate": "langchain_tool"}, tools=[calculate]
        )

        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Calculate"),
                AIMessage(
                    content="Calculating",
                    tool_calls=[
                        {
                            "name": "calculate",
                            "args": {"expression": "2+2"},
                            "id": "call_1",
                        }
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "tool_node"
        assert result.update == {}  # No messages added for tool routing

    def test_unknown_tool_handling(self):
        """Test handling of unknown tools."""
        engine = MockEngine()

        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(
                    content="Using unknown",
                    tool_calls=[{"name": "unknown_tool", "args": {}, "id": "call_1"}],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "agent_node"
        assert "messages" in result.update
        assert len(result.update["messages"]) == 1
        assert isinstance(result.update["messages"][0], ToolMessage)
        assert "unknown tool" in result.update["messages"][0].content.lower()

    def test_parallel_execution_multiple_tools(self):
        """Test parallel execution with multiple tool calls."""
        engine = MockEngine(
            tool_routes={"calculate": "langchain_tool", "search_web": "langchain_tool"},
            tools=[calculate, search_web],
        )

        node = UnifiedValidationNodeConfig(
            name="test", engine_name="test_engine", parallel_execution=True
        )

        state = {
            "messages": [
                HumanMessage(content="Multi-task"),
                AIMessage(
                    content="Doing multiple things",
                    tool_calls=[
                        {
                            "name": "calculate",
                            "args": {"expression": "2+2"},
                            "id": "call_1",
                        },
                        {"name": "search_web", "args": {"query": "AI"}, "id": "call_2"},
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        # With parallel execution and multiple tool calls, should use Send objects
        assert isinstance(result.goto, list)
        assert len(result.goto) == 2
        assert all(isinstance(s, Send) for s in result.goto)
        assert all(s.node == "tool_node" for s in result.goto)

    def test_single_execution_mode(self):
        """Test single execution mode."""
        engine = MockEngine(
            tool_routes={"calculate": "langchain_tool", "UserQuery": "pydantic_model"},
            tools=[calculate],
            schemas=[UserQuery],
        )

        node = UnifiedValidationNodeConfig(
            name="test", engine_name="test_engine", parallel_execution=False
        )

        state = {
            "messages": [
                HumanMessage(content="Mixed"),
                AIMessage(
                    content="Mixed tools",
                    tool_calls=[
                        {
                            "name": "calculate",
                            "args": {"expression": "2+2"},
                            "id": "call_1",
                        },
                        {
                            "name": "UserQuery",
                            "args": {"question": "Test", "priority": 1},
                            "id": "call_2",
                        },
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        # Mixed destinations should route to agent
        assert result.goto == "agent_node"

    def test_no_tool_messages_mode(self):
        """Test with create_tool_messages disabled."""
        engine = MockEngine()

        node = UnifiedValidationNodeConfig(
            name="test", engine_name="test_engine", create_tool_messages=False
        )

        state = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(
                    content="Unknown tool",
                    tool_calls=[{"name": "unknown", "args": {}, "id": "call_1"}],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "agent_node"
        assert result.update == {}  # No messages created

    def test_structured_output_model_detection(self):
        """Test detection of structured output model."""
        engine = MockEngine()
        engine.structured_output_model = UserQuery

        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")

        state = {
            "messages": [
                HumanMessage(content="Test"),
                AIMessage(
                    content="Using model",
                    tool_calls=[
                        {
                            "name": "UserQuery",
                            "args": {"question": "Test", "priority": 1},
                            "id": "call_1",
                        }
                    ],
                ),
            ],
            "engines": {"test_engine": engine},
        }

        result = node(state)

        assert isinstance(result, Command)
        assert result.goto == "parse_output"

    def test_model_validator(self):
        """Test the model validator."""
        # Should succeed with valid config
        node = UnifiedValidationNodeConfig(name="test", engine_name="test_engine")
        assert node is not None

        # Test with custom destinations
        node2 = UnifiedValidationNodeConfig(
            name="test",
            engine_name="test_engine",
            tool_node="custom_tool",
            parse_output_node="custom_parser",
            agent_node="custom_agent",
        )

        assert node2.tool_node == "custom_tool"
        assert node2.parse_output_node == "custom_parser"
        assert node2.agent_node == "custom_agent"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
