"""Tests for ToolStateWithValidation functionality."""

from typing import Any, Dict, List

import pytest
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.core.graph.node.validation_node_with_routing import ValidationNodeWithRouting
from haive.core.schema.prebuilt.tool_state_with_validation import (
    ToolStateWithValidation,
)
from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ToolValidationResult,
    ValidationStateManager,
    ValidationStatus,
)


# Real tools for testing
@tool
def search_tool(query: str, limit: int = 10) -> str:
    """Search for information."""
    return f"Found {limit} results for query: {query}"


@tool
def calculator_tool(a: float, b: float, operation: str = "add") -> float:
    """Perform calculation."""
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else 0
    return 0


class CreateDocumentSchema(BaseModel):
    """Schema for document creation."""

    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    tags: List[str] = Field(default_factory=list, description="Document tags")


class TestToolStateWithValidation:
    """Test ToolStateWithValidation with real tools."""

    def test_initialization(self):
        """Test proper initialization of ToolStateWithValidation."""
        state = ToolStateWithValidation()

        # Check all required attributes exist
        assert hasattr(state, "validation_state")
        assert hasattr(state, "tool_metadata")
        assert hasattr(state, "tool_performance")
        assert hasattr(state, "tool_execution_history")
        assert hasattr(state, "tool_categories")
        assert hasattr(state, "tool_dependencies")
        assert hasattr(state, "tool_priorities")
        assert hasattr(state, "tool_message_status")
        assert hasattr(state, "branch_conditions")

        # Check default values
        assert state.validation_state.total_tools == 0
        assert len(state.tool_metadata) == 0
        assert len(state.tool_performance) == 0

    def test_add_tool_with_validation(self):
        """Test adding tools with validation metadata."""
        state = ToolStateWithValidation()

        # Add tools using the parent's add_tool method
        state.add_tool(search_tool)
        state.add_tool(calculator_tool)

        # Verify tools were added
        assert len(state.tools) == 2
        assert "search_tool" in state.tool_routes
        assert "calculator_tool" in state.tool_routes

        # Use add_tool_with_validation for additional metadata
        state.add_tool_with_validation(
            CreateDocumentSchema,
            route="pydantic_model",
            category="creation",
            priority=10,
            metadata={"description": "Creates documents"},
        )

        # Verify enhanced addition
        assert len(state.tools) == 3
        assert "CreateDocumentSchema" in state.tool_routes
        assert state.tool_routes["CreateDocumentSchema"] == "pydantic_model"
        assert "CreateDocumentSchema" in state.tool_metadata
        assert state.tool_priorities.get("CreateDocumentSchema") == 10

    def test_tool_categorization(self):
        """Test automatic tool categorization."""
        state = ToolStateWithValidation()

        # Add tools - they should be auto-categorized
        state.add_tool(search_tool)
        state.add_tool(calculator_tool)

        # Force categorization setup
        state._setup_validation_features()

        # Check categories were assigned
        assert "retrieval" in state.tool_categories  # search_tool
        assert "search_tool" in state.tool_categories["retrieval"]

        # Manually add to category
        state.add_tool_to_category("calculator_tool", "utility")
        assert "calculator_tool" in state.tool_categories["utility"]

        # Get tools by category
        retrieval_tools = state.get_tools_by_category("retrieval")
        assert len(retrieval_tools) == 1
        assert retrieval_tools[0].name == "search_tool"

    def test_validation_state_integration(self):
        """Test validation state integration with tool state."""
        state = ToolStateWithValidation()
        state.add_tool(search_tool)
        state.add_tool(calculator_tool)

        # Create validation results
        routing_state = ValidationStateManager.create_routing_state()

        # Add valid result
        valid_result = ValidationStateManager.create_validation_result(
            tool_call_id="call_001",
            tool_name="search_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        routing_state.add_validation_result(valid_result)

        # Add invalid result
        invalid_result = ValidationStateManager.create_validation_result(
            tool_call_id="call_002",
            tool_name="calculator_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            errors=["Missing required parameter 'b'"],
            corrected_args={"a": 5, "b": 0, "operation": "add"},
        )
        routing_state.add_validation_result(invalid_result)

        # Apply validation results
        state.apply_validation_results(routing_state)

        # Verify application
        assert state.validation_state.total_tools == 2
        assert state.tool_message_status["call_001"] == "valid"
        assert state.tool_message_status["call_002"] == "invalid"

        # Check routing decisions
        assert state.should_continue_to_tools()
        assert not state.should_return_to_agent()
        assert not state.should_end_processing()

        # Get valid calls
        valid_calls = state.get_valid_tool_calls_for_execution()
        assert len(valid_calls) == 1
        assert valid_calls[0] == "call_001"

        # Get correctable calls
        correctable = state.get_correctable_tool_calls()
        assert len(correctable) == 1
        assert correctable[0].tool_call_id == "call_002"

    def test_performance_tracking(self):
        """Test tool execution performance tracking."""
        state = ToolStateWithValidation()
        state.add_tool(search_tool)

        # Track multiple executions
        state.track_tool_execution("search_tool", 0.1, True)
        state.track_tool_execution("search_tool", 0.2, True)
        state.track_tool_execution("search_tool", 0.3, False)

        # Check performance metrics
        assert "search_tool" in state.tool_performance
        metrics = state.tool_performance["search_tool"]
        assert metrics["total_executions"] == 3
        assert metrics["successful_executions"] == 2
        assert metrics["success_rate"] == 2 / 3

        # Check execution history
        assert len(state.tool_execution_history) == 3
        assert all(
            record["tool_name"] == "search_tool"
            for record in state.tool_execution_history
        )

    def test_branch_conditions(self):
        """Test conditional branching support."""
        state = ToolStateWithValidation()

        # Set various branch conditions
        state.set_branch_condition("has_valid_tools", True)
        state.set_branch_condition("error_count", 0)
        state.set_branch_condition("total_tools", 5)

        # Get conditions
        assert state.get_branch_condition("has_valid_tools") == True
        assert state.get_branch_condition("error_count") == 0
        assert state.get_branch_condition("missing_condition", "default") == "default"

        # Evaluate conditions
        assert state.evaluate_branch_condition("has_valid_tools == True")
        assert state.evaluate_branch_condition("error_count == 0")
        assert state.evaluate_branch_condition("total_tools > 3")
        assert not state.evaluate_branch_condition("total_tools < 3")

    def test_validation_routing_data(self):
        """Test getting validation routing data for branching."""
        state = ToolStateWithValidation()
        state.add_tool(search_tool)

        # Get initial routing data
        routing_data = state.get_validation_routing_data()
        assert routing_data["next_action"] == "execute"
        assert routing_data["valid_count"] == 0
        assert routing_data["total_tools_in_state"] == 1
        assert routing_data["has_dependencies"] == False

        # Add validation results
        routing_state = ValidationStateManager.create_routing_state()
        result = ValidationStateManager.create_validation_result(
            tool_call_id="test_call",
            tool_name="search_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        routing_state.add_validation_result(result)
        state.apply_validation_results(routing_state)

        # Get updated routing data
        routing_data = state.get_validation_routing_data()
        assert routing_data["valid_count"] == 1
        assert routing_data["tool_message_statuses"]["test_call"] == "valid"

    def test_get_validation_summary(self):
        """Test getting comprehensive validation summary."""
        state = ToolStateWithValidation()
        state.add_tool(search_tool)
        state.add_tool(calculator_tool)

        # Add some metadata
        state.tool_dependencies["calculator_tool"] = ["search_tool"]
        state.set_branch_condition("test", True)

        # Get summary
        summary = state.get_validation_summary()

        assert summary["total_tools"] == 2
        assert "langchain_tool" in summary["tools_by_route"]
        assert summary["tools_with_dependencies"] == 1
        assert summary["branch_conditions"]["test"] == True
        assert "validation_summary" in summary


class TestValidationNodeWithRouting:
    """Test ValidationNodeWithRouting functionality."""

    def test_initialization(self):
        """Test proper initialization of validation node."""
        node = ValidationNodeWithRouting()

        # Check configuration
        assert node.update_tool_messages == True
        assert node.provide_routing_state == True
        assert node.auto_correct_args == True
        assert node.validation_timeout == 30.0
        assert node.continue_on_partial_validation == True

    def test_create_node_function(self):
        """Test creating the validation node function."""
        node = ValidationNodeWithRouting()

        # Create the function
        validation_func = node.create_node_function()

        # Verify it's callable
        assert callable(validation_func)

        # Test with empty state
        result = validation_func({"messages": []})
        assert isinstance(result, dict)

    def test_validation_with_tool_calls(self):
        """Test validation with actual tool calls."""
        node = ValidationNodeWithRouting(
            engine_name="test_engine", tools=[search_tool, calculator_tool]
        )

        # Create state with tool calls
        ai_message = AIMessage(
            content="I'll search and calculate for you.",
            tool_calls=[
                {
                    "id": "call_001",
                    "name": "search_tool",
                    "args": {"query": "python", "limit": 5},
                },
                {
                    "id": "call_002",
                    "name": "calculator_tool",
                    "args": {"a": 10},  # Missing 'b' parameter
                },
            ],
        )

        state = {
            "messages": [ai_message],
            "tools": [search_tool, calculator_tool],
            "tool_routes": {
                "search_tool": "langchain_tool",
                "calculator_tool": "langchain_tool",
            },
        }

        # Run validation
        validation_func = node.create_node_function()
        result = validation_func(state)

        # Check results
        assert "validation_state" in result
        assert "routing_data" in result

        routing_data = result["routing_data"]
        assert routing_data["should_continue"] == True  # Valid tool exists
        assert routing_data["next_action"] == "execute"
        assert len(routing_data["target_nodes"]) > 0

    def test_tool_message_updates(self):
        """Test that tool messages are updated with validation status."""
        node = ValidationNodeWithRouting(update_tool_messages=True, tools=[search_tool])

        # Create state with tool call and response
        ai_message = AIMessage(
            content="Searching...",
            tool_calls=[
                {"id": "call_001", "name": "search_tool", "args": {"query": "test"}}
            ],
        )

        tool_message = ToolMessage(content="Search results", tool_call_id="call_001")

        state = {
            "messages": [ai_message, tool_message],
            "tools": [search_tool],
            "tool_routes": {"search_tool": "langchain_tool"},
        }

        # Run validation
        validation_func = node.create_node_function()
        result = validation_func(state)

        # Check that validation state was created
        assert "validation_state" in result
        validation_state = result["validation_state"]
        assert validation_state.total_tools == 1

        # Tool message updates should be prepared
        assert "call_001" in validation_state.tool_message_updates


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
