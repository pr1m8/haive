"""Tests for validation routing and state management."""

from typing import Any, Dict

import pytest
from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ToolValidationResult,
    ValidationRoutingState,
    ValidationStateManager,
    ValidationStatus,
)
from pydantic import BaseModel, Field


class SampleToolSchema(BaseModel):
    """Sample tool schema for testing."""

    query: str = Field(..., description="Query string")
    limit: int = Field(default=10, description="Result limit")


class TestValidationState:
    """Test validation state management."""

    def test_create_validation_result(self):
        """Test creating a validation result."""
        result = ValidationStateManager.create_validation_result(
            tool_call_id="test_call_1",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )

        assert result.tool_call_id == "test_call_1"
        assert result.tool_name == "test_tool"
        assert result.status == ValidationStatus.VALID
        assert result.route_recommendation == RouteRecommendation.EXECUTE
        assert result.errors == []
        assert result.warnings == []

    def test_create_routing_state(self):
        """Test creating a routing state."""
        state = ValidationStateManager.create_routing_state()

        assert isinstance(state, ValidationRoutingState)
        assert state.total_tools == 0
        assert state.next_action == RouteRecommendation.EXECUTE
        assert len(state.valid_tool_calls) == 0

    def test_add_validation_result_valid(self):
        """Test adding a valid validation result."""
        state = ValidationStateManager.create_routing_state()

        result = ValidationStateManager.create_validation_result(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )

        state.add_validation_result(result)

        assert state.total_tools == 1
        assert len(state.valid_tool_calls) == 1
        assert "valid_call" in state.valid_tool_calls
        assert state.next_action == RouteRecommendation.EXECUTE
        assert "tool_node" in state.target_nodes

    def test_add_validation_result_invalid(self):
        """Test adding an invalid validation result."""
        state = ValidationStateManager.create_routing_state()

        result = ValidationStateManager.create_validation_result(
            tool_call_id="invalid_call",
            tool_name="invalid_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Invalid argument type"],
            target_node="agent_node",
        )

        state.add_validation_result(result)

        assert state.total_tools == 1
        assert len(state.invalid_tool_calls) == 1
        assert "invalid_call" in state.invalid_tool_calls
        assert state.next_action == RouteRecommendation.AGENT
        assert "agent_node" in state.target_nodes

    def test_add_validation_result_error(self):
        """Test adding an error validation result."""
        state = ValidationStateManager.create_routing_state()

        result = ValidationStateManager.create_validation_result(
            tool_call_id="error_call",
            tool_name="error_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Tool not found"],
        )

        state.add_validation_result(result)

        assert state.total_tools == 1
        assert len(state.error_tool_calls) == 1
        assert "error_call" in state.error_tool_calls
        assert state.next_action == RouteRecommendation.AGENT

    def test_mixed_validation_results(self):
        """Test adding mixed validation results."""
        state = ValidationStateManager.create_routing_state()

        # Add valid result
        valid_result = ValidationStateManager.create_validation_result(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        state.add_validation_result(valid_result)

        # Add invalid result
        invalid_result = ValidationStateManager.create_validation_result(
            tool_call_id="invalid_call",
            tool_name="invalid_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            corrected_args={"query": "corrected"},
        )
        state.add_validation_result(invalid_result)

        assert state.total_tools == 2
        assert len(state.valid_tool_calls) == 1
        assert len(state.invalid_tool_calls) == 1
        assert (
            state.next_action == RouteRecommendation.EXECUTE
        )  # Valid tools take precedence

    def test_routing_decision_data(self):
        """Test getting routing decision data."""
        state = ValidationStateManager.create_routing_state()

        result = ValidationStateManager.create_validation_result(
            tool_call_id="test_call",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            corrected_args={"query": "test"},
        )
        state.add_validation_result(result)

        decision_data = state.get_routing_decision()

        assert decision_data["next_action"] == "execute"
        assert decision_data["valid_count"] == 1
        assert decision_data["invalid_count"] == 0
        assert decision_data["error_count"] == 0
        assert decision_data["total_count"] == 1
        assert decision_data["has_corrections"]

    def test_should_continue_execution(self):
        """Test should continue execution logic."""
        state = ValidationStateManager.create_routing_state()

        # No tools - should not continue
        assert not state.should_continue_execution()

        # Add valid tool - should continue
        valid_result = ValidationStateManager.create_validation_result(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        state.add_validation_result(valid_result)

        assert state.should_continue_execution()

        # Add error - should not continue (return to agent)
        error_result = ValidationStateManager.create_validation_result(
            tool_call_id="error_call",
            tool_name="error_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
        )
        state.add_validation_result(error_result)

        assert not state.should_continue_execution()
        assert state.should_return_to_agent()

    def test_get_correctable_tool_calls(self):
        """Test getting correctable tool calls."""
        state = ValidationStateManager.create_routing_state()

        # Add result with corrections
        correctable_result = ValidationStateManager.create_validation_result(
            tool_call_id="correctable_call",
            tool_name="correctable_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            corrected_args={"query": "corrected"},
        )
        state.add_validation_result(correctable_result)

        # Add result without corrections
        uncorrectable_result = ValidationStateManager.create_validation_result(
            tool_call_id="uncorrectable_call",
            tool_name="uncorrectable_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.AGENT,
        )
        state.add_validation_result(uncorrectable_result)

        correctable_calls = state.get_correctable_tool_calls()

        assert len(correctable_calls) == 1
        assert correctable_calls[0].tool_call_id == "correctable_call"
        assert correctable_calls[0].corrected_args is not None

    def test_routing_summary(self):
        """Test routing summary generation."""
        state = ValidationStateManager.create_routing_state()

        # Add some results
        for i in range(3):
            result = ValidationStateManager.create_validation_result(
                tool_call_id=f"call_{i}",
                tool_name=f"tool_{i}",
                status=ValidationStatus.VALID if i < 2 else ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.EXECUTE,
                target_node="tool_node",
            )
            state.add_validation_result(result)

        summary = state.get_routing_summary()

        assert "Validated 3 tool calls" in summary
        assert "Valid: 2" in summary
        assert "Invalid: 1" in summary
        assert "Errors: 0" in summary
        assert "Target nodes: tool_node" in summary
        assert "Next action: execute" in summary


class TestValidationStateManager:
    """Test validation state manager utilities."""

    def test_merge_routing_states(self):
        """Test merging multiple routing states."""
        # Create first state
        state1 = ValidationStateManager.create_routing_state()
        result1 = ValidationStateManager.create_validation_result(
            tool_call_id="call1",
            tool_name="tool1",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        state1.add_validation_result(result1)

        # Create second state
        state2 = ValidationStateManager.create_routing_state()
        result2 = ValidationStateManager.create_validation_result(
            tool_call_id="call2",
            tool_name="tool2",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.AGENT,
        )
        state2.add_validation_result(result2)

        # Merge states
        merged = ValidationStateManager.merge_routing_states([state1, state2])

        assert merged.total_tools == 2
        assert len(merged.valid_tool_calls) == 1
        assert len(merged.invalid_tool_calls) == 1
        assert "call1" in merged.tool_validations
        assert "call2" in merged.tool_validations

        # Should execute because we have valid tools
        assert merged.next_action == RouteRecommendation.EXECUTE


if __name__ == "__main__":
    pytest.main([__file__])
