"""Tests for StateUpdatingValidationNode with dual state update and routing functionality."""

from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock

import pytest
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import END, Send

from haive.core.graph.node.state_updating_validation_node import (
    StateUpdatingValidationNode,
    ValidationMode,
    create_state_updating_validation_node,
)
from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationStateManager,
    ValidationStatus,
)


class MockState:
    """Mock state for testing."""

    def __init__(self):
        self.messages = []
        self.tools = []
        self.tool_routes = {}
        self.engines = {}
        self.validation_state = None
        self.error_tool_calls = []

    def get_tool_calls(self) -> List[Dict[str, Any]]:
        """Get tool calls from last AI message."""
        if not self.messages:
            return []

        last_msg = self.messages[-1]
        if isinstance(last_msg, AIMessage) and hasattr(last_msg, "tool_calls"):
            return last_msg.tool_calls or []
        return []

    def apply_validation_results(self, validation_state):
        """Apply validation results to state."""
        self.validation_state = validation_state


class MockTool:
    """Mock tool for testing."""

    def __init__(self, name: str, has_schema: bool = False):
        self.name = name
        self.args_schema = Mock() if has_schema else None

        if has_schema:
            self.args_schema.model_validate = Mock()


class TestStateUpdatingValidationNode:
    """Test StateUpdatingValidationNode functionality."""

    def test_node_creation(self):
        """Test node creation with default and custom config."""
        # Default creation
        node = StateUpdatingValidationNode()
        assert node.name == "state_validation"
        assert node.validation_mode == ValidationMode.PARTIAL
        assert node.update_messages is True

        # Custom creation
        node = create_state_updating_validation_node(
            name="custom_validator",
            validation_mode=ValidationMode.STRICT,
            update_messages=False,
        )
        assert node.name == "custom_validator"
        assert node.validation_mode == ValidationMode.STRICT
        assert node.update_messages is False

    def test_node_function_no_tool_calls(self):
        """Test node function when no tool calls exist."""
        node = StateUpdatingValidationNode()
        node_func = node.create_node_function()

        state = MockState()
        result = node_func(state)

        assert result == state
        assert state.validation_state is not None

    def test_node_function_with_valid_tools(self):
        """Test node function with valid tool calls."""
        node = StateUpdatingValidationNode()
        node_func = node.create_node_function()

        # Setup state
        state = MockState()
        state.tools = [MockTool("search"), MockTool("calculator")]
        state.tool_routes = {"search": "langchain_tool", "calculator": "function"}

        # Add AI message with tool calls
        ai_msg = AIMessage(
            content="Processing...",
            tool_calls=[
                {"id": "1", "name": "search", "args": {"query": "test"}},
                {"id": "2", "name": "calculator", "args": {"a": 1, "b": 2}},
            ],
        )
        state.messages.append(ai_msg)

        # Execute node
        result = node_func(state)

        # Verify state was updated
        assert state.validation_state is not None
        assert len(state.validation_state.valid_tool_calls) == 2
        assert len(state.validation_state.error_tool_calls) == 0

    def test_node_function_with_invalid_tools(self):
        """Test node function with invalid tool calls."""
        node = StateUpdatingValidationNode(update_messages=True, track_error_tools=True)
        node_func = node.create_node_function()

        # Setup state
        state = MockState()
        state.tools = [MockTool("search")]
        state.tool_routes = {"search": "langchain_tool"}

        # Add AI message with invalid tool
        ai_msg = AIMessage(
            content="Processing...",
            tool_calls=[{"id": "1", "name": "unknown_tool", "args": {}}],
        )
        state.messages.append(ai_msg)

        # Execute node
        result = node_func(state)

        # Verify validation state
        assert state.validation_state is not None
        assert len(state.validation_state.error_tool_calls) == 1
        assert len(state.validation_state.valid_tool_calls) == 0

        # Verify error message was added
        assert len(state.messages) == 2
        error_msg = state.messages[-1]
        assert isinstance(error_msg, ToolMessage)
        assert "Tool validation errors" in error_msg.content

    def test_router_function_no_validation_state(self):
        """Test router function when no validation state exists."""
        node = StateUpdatingValidationNode()
        router_func = node.create_router_function()

        state = MockState()
        result = router_func(state)

        assert result == END

    def test_router_function_with_valid_tools(self):
        """Test router function with valid tools in state."""
        node = StateUpdatingValidationNode()
        router_func = node.create_router_function()

        # Setup state with validation results
        state = MockState()
        state.validation_state = ValidationStateManager.create_routing_state()

        # Add valid tool results
        result1 = ValidationStateManager.create_validation_result(
            tool_call_id="1",
            tool_name="search",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        result2 = ValidationStateManager.create_validation_result(
            tool_call_id="2",
            tool_name="calculator",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        state.validation_state.add_validation_result(result1)
        state.validation_state.add_validation_result(result2)

        # Add corresponding tool calls
        ai_msg = AIMessage(
            content="Processing...",
            tool_calls=[
                {"id": "1", "name": "search", "args": {"query": "test"}},
                {"id": "2", "name": "calculator", "args": {"a": 1}},
            ],
        )
        state.messages.append(ai_msg)

        # Execute router
        result = router_func(state)

        # Verify Send objects
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(send, Send) for send in result)
        assert result[0].node == "tool_node"
        assert result[1].node == "tool_node"

    def test_router_function_strict_mode(self):
        """Test router function in strict mode with failures."""
        node = StateUpdatingValidationNode(
            validation_mode=ValidationMode.STRICT, agent_node="agent"
        )
        router_func = node.create_router_function()

        # Setup state with mixed results
        state = MockState()
        state.validation_state = ValidationStateManager.create_routing_state()

        # Add one valid and one invalid result
        valid_result = ValidationStateManager.create_validation_result(
            tool_call_id="1",
            tool_name="search",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        invalid_result = ValidationStateManager.create_validation_result(
            tool_call_id="2",
            tool_name="unknown",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Tool not found"],
        )
        state.validation_state.add_validation_result(valid_result)
        state.validation_state.add_validation_result(invalid_result)

        # Execute router
        result = router_func(state)

        # In strict mode, any failure routes to agent
        assert result == "agent"

    def test_router_function_permissive_mode(self):
        """Test router function in permissive mode."""
        node = StateUpdatingValidationNode(
            validation_mode=ValidationMode.PERMISSIVE, agent_node="agent"
        )
        router_func = node.create_router_function()

        # Setup state with mixed results
        state = MockState()
        state.validation_state = ValidationStateManager.create_routing_state()

        # Add one valid and one invalid result
        valid_result = ValidationStateManager.create_validation_result(
            tool_call_id="1",
            tool_name="search",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        invalid_result = ValidationStateManager.create_validation_result(
            tool_call_id="2",
            tool_name="unknown",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Tool not found"],
        )
        state.validation_state.add_validation_result(valid_result)
        state.validation_state.add_validation_result(invalid_result)

        # Add tool call for valid tool
        ai_msg = AIMessage(
            content="Processing...",
            tool_calls=[{"id": "1", "name": "search", "args": {"query": "test"}}],
        )
        state.messages.append(ai_msg)

        # Execute router
        result = router_func(state)

        # In permissive mode, valid tools still execute
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].node == "tool_node"

    def test_engine_tool_discovery(self):
        """Test tool discovery from engine."""
        node = StateUpdatingValidationNode(engine_name="main_engine")
        node_func = node.create_node_function()

        # Setup state with engine
        state = MockState()
        mock_engine = Mock()
        mock_engine.tools = [MockTool("engine_tool")]
        mock_engine.tool_routes = {"engine_tool": "langchain_tool"}
        state.engines = {"main_engine": mock_engine}

        # Add tool call
        ai_msg = AIMessage(
            content="Using engine tool",
            tool_calls=[{"id": "1", "name": "engine_tool", "args": {}}],
        )
        state.messages.append(ai_msg)

        # Execute node
        result = node_func(state)

        # Verify tool was found and validated
        assert state.validation_state is not None
        assert len(state.validation_state.valid_tool_calls) == 1

    def test_argument_validation(self):
        """Test tool argument validation."""
        node = StateUpdatingValidationNode()
        node_func = node.create_node_function()

        # Setup state with tool that has schema
        state = MockState()
        tool = MockTool("validated_tool", has_schema=True)

        # Mock validation error
        tool.args_schema.model_validate.side_effect = ValueError("Invalid args")

        state.tools = [tool]
        state.tool_routes = {"validated_tool": "function"}

        # Add tool call with bad args
        ai_msg = AIMessage(
            content="Testing validation",
            tool_calls=[{"id": "1", "name": "validated_tool", "args": {"bad": "args"}}],
        )
        state.messages.append(ai_msg)

        # Execute node
        result = node_func(state)

        # Verify validation failed
        assert state.validation_state is not None
        assert len(state.validation_state.invalid_tool_calls) == 1
        assert len(state.validation_state.valid_tool_calls) == 0

    def test_metadata_addition(self):
        """Test adding validation metadata to tool calls."""
        node = StateUpdatingValidationNode(add_validation_metadata=True)
        node_func = node.create_node_function()

        # Setup state
        state = MockState()
        state.tools = [MockTool("search")]
        state.tool_routes = {"search": "langchain_tool"}

        # Add tool call
        tool_calls = [{"id": "1", "name": "search", "args": {}}]
        ai_msg = AIMessage(content="Search for info", tool_calls=tool_calls)
        state.messages.append(ai_msg)

        # Execute node
        result = node_func(state)

        # Verify metadata was added
        updated_tool_call = state.messages[-1].tool_calls[0]
        assert "metadata" in updated_tool_call
        assert updated_tool_call["metadata"]["validation_status"] == "valid"
        assert "target_node" in updated_tool_call["metadata"]

    def test_send_branch_creation(self):
        """Test Send branch creation with enhanced tool calls."""
        node = StateUpdatingValidationNode()
        router_func = node.create_router_function()

        # Setup state
        state = MockState()
        state.validation_state = ValidationStateManager.create_routing_state()

        # Add multiple valid results with different targets
        result1 = ValidationStateManager.create_validation_result(
            tool_call_id="1",
            tool_name="search",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
            metadata={"route": "langchain_tool"},
        )
        result2 = ValidationStateManager.create_validation_result(
            tool_call_id="2",
            tool_name="DocumentSchema",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="parser_node",
            metadata={"route": "pydantic_model"},
        )
        state.validation_state.add_validation_result(result1)
        state.validation_state.add_validation_result(result2)

        # Add tool calls
        ai_msg = AIMessage(
            content="Processing",
            tool_calls=[
                {"id": "1", "name": "search", "args": {"query": "test"}},
                {"id": "2", "name": "DocumentSchema", "args": {"title": "Doc"}},
            ],
        )
        state.messages.append(ai_msg)

        # Execute router
        result = router_func(state)

        # Verify Send objects
        assert isinstance(result, list)
        assert len(result) == 2

        # Check first Send
        send1 = result[0]
        assert send1.node == "tool_node"
        assert send1.arg["validation_metadata"]["status"] == "valid"
        assert send1.arg["validation_metadata"]["route"] == "langchain_tool"

        # Check second Send
        send2 = result[1]
        assert send2.node == "parser_node"
        assert send2.arg["validation_metadata"]["status"] == "valid"
        assert send2.arg["validation_metadata"]["route"] == "pydantic_model"


class TestIntegrationScenarios:
    """Test integration scenarios combining state update and routing."""

    def test_full_workflow(self):
        """Test complete workflow: validation -> state update -> routing."""
        # Create node
        node = StateUpdatingValidationNode(
            update_messages=True, track_error_tools=True, add_validation_metadata=True
        )

        # Get both functions
        node_func = node.create_node_function()
        router_func = node.create_router_function()

        # Setup state
        state = MockState()
        state.tools = [
            MockTool("search"),
            MockTool("calculator"),
            MockTool("writer", has_schema=True),
        ]
        state.tool_routes = {
            "search": "langchain_tool",
            "calculator": "function",
            "writer": "pydantic_model",
        }

        # Add mixed tool calls
        ai_msg = AIMessage(
            content="Multi-tool request",
            tool_calls=[
                {"id": "1", "name": "search", "args": {"query": "python"}},
                {"id": "2", "name": "calculator", "args": {"expr": "2+2"}},
                {"id": "3", "name": "unknown_tool", "args": {}},
                {"id": "4", "name": "writer", "args": {"text": "Hello"}},
            ],
        )
        state.messages.append(ai_msg)

        # Step 1: Run validation node
        updated_state = node_func(state)

        # Verify state updates
        assert updated_state.validation_state is not None
        assert len(updated_state.validation_state.valid_tool_calls) == 3
        assert len(updated_state.validation_state.error_tool_calls) == 1

        # Verify error message was added
        assert len(updated_state.messages) > 1
        last_msg = updated_state.messages[-1]
        if isinstance(last_msg, ToolMessage):
            assert "unknown_tool" in last_msg.content

        # Step 2: Run router function
        routing_result = router_func(updated_state)

        # Verify routing
        assert isinstance(routing_result, list)
        assert len(routing_result) == 3  # Only valid tools

        # Check each Send
        nodes_used = [send.node for send in routing_result]
        assert "tool_node" in nodes_used  # For search and calculator
        assert "parser_node" in nodes_used  # For writer

    def test_dynamic_state_changes(self):
        """Test router adapting to state changes."""
        node = StateUpdatingValidationNode(validation_mode=ValidationMode.PARTIAL)

        node_func = node.create_node_function()
        router_func = node.create_router_function()

        # Initial state
        state = MockState()
        state.tools = [MockTool("tool1")]
        state.tool_routes = {"tool1": "function"}

        # First validation
        ai_msg1 = AIMessage(
            content="First request",
            tool_calls=[{"id": "1", "name": "tool1", "args": {}}],
        )
        state.messages.append(ai_msg1)

        state = node_func(state)
        result1 = router_func(state)

        assert isinstance(result1, list)
        assert len(result1) == 1

        # Modify state - add new tool
        state.tools.append(MockTool("tool2"))
        state.tool_routes["tool2"] = "langchain_tool"

        # Second validation with both tools
        ai_msg2 = AIMessage(
            content="Second request",
            tool_calls=[
                {"id": "2", "name": "tool1", "args": {}},
                {"id": "3", "name": "tool2", "args": {}},
            ],
        )
        state.messages.append(ai_msg2)

        state = node_func(state)
        result2 = router_func(state)

        assert isinstance(result2, list)
        assert len(result2) == 2
