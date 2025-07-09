"""Direct tests for validation state functionality."""

import os
import sys

import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../src"))

from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ToolValidationResult,
    ValidationRoutingState,
    ValidationStateManager,
    ValidationStatus,
)


class TestValidationState:
    """Test validation state components."""

    def test_validation_status_enum(self):
        """Test ValidationStatus enum values."""
        assert ValidationStatus.PENDING == "pending"
        assert ValidationStatus.VALID == "valid"
        assert ValidationStatus.INVALID == "invalid"
        assert ValidationStatus.ERROR == "error"
        assert ValidationStatus.SKIPPED == "skipped"

    def test_route_recommendation_enum(self):
        """Test RouteRecommendation enum values."""
        assert RouteRecommendation.EXECUTE == "execute"
        assert RouteRecommendation.RETRY == "retry"
        assert RouteRecommendation.SKIP == "skip"
        assert RouteRecommendation.REDIRECT == "redirect"
        assert RouteRecommendation.AGENT == "agent"
        assert RouteRecommendation.END == "end"

    def test_tool_validation_result_creation(self):
        """Test creating ToolValidationResult."""
        result = ToolValidationResult(
            tool_call_id="test_001",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )

        assert result.tool_call_id == "test_001"
        assert result.tool_name == "test_tool"
        assert result.status == ValidationStatus.VALID
        assert result.route_recommendation == RouteRecommendation.EXECUTE
        assert result.errors == []
        assert result.warnings == []
        assert result.corrected_args is None
        assert result.priority == 0

    def test_validation_routing_state(self):
        """Test ValidationRoutingState functionality."""
        state = ValidationRoutingState()

        # Initial state
        assert state.total_tools == 0
        assert state.next_action == RouteRecommendation.EXECUTE
        assert len(state.valid_tool_calls) == 0
        assert len(state.invalid_tool_calls) == 0
        assert len(state.error_tool_calls) == 0
        assert len(state.target_nodes) == 0

    def test_add_validation_results(self):
        """Test adding validation results to routing state."""
        state = ValidationRoutingState()

        # Add valid result
        valid_result = ToolValidationResult(
            tool_call_id="valid_001",
            tool_name="search_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node",
        )
        state.add_validation_result(valid_result)

        assert state.total_tools == 1
        assert len(state.valid_tool_calls) == 1
        assert "valid_001" in state.valid_tool_calls
        assert state.next_action == RouteRecommendation.EXECUTE
        assert "tool_node" in state.target_nodes

        # Add invalid result
        invalid_result = ToolValidationResult(
            tool_call_id="invalid_001",
            tool_name="create_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            errors=["Missing required field"],
            corrected_args={"field": "value"},
            target_node="tool_node",
        )
        state.add_validation_result(invalid_result)

        assert state.total_tools == 2
        assert len(state.invalid_tool_calls) == 1
        assert "invalid_001" in state.invalid_tool_calls
        # Should still execute because we have valid tools
        assert state.next_action == RouteRecommendation.EXECUTE

        # Add error result
        error_result = ToolValidationResult(
            tool_call_id="error_001",
            tool_name="unknown_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Tool not found"],
            target_node="agent_node",
        )
        state.add_validation_result(error_result)

        assert state.total_tools == 3
        assert len(state.error_tool_calls) == 1
        assert "error_001" in state.error_tool_calls
        # Errors take precedence
        assert state.next_action == RouteRecommendation.AGENT
        assert "agent_node" in state.target_nodes

    def test_routing_decision_logic(self):
        """Test routing decision generation."""
        state = ValidationRoutingState()

        # Only valid tools - should execute
        for i in range(3):
            result = ToolValidationResult(
                tool_call_id=f"valid_{i}",
                tool_name=f"tool_{i}",
                status=ValidationStatus.VALID,
                route_recommendation=RouteRecommendation.EXECUTE,
            )
            state.add_validation_result(result)

        decision = state.get_routing_decision()
        assert decision["next_action"] == "execute"
        assert decision["valid_count"] == 3
        assert decision["invalid_count"] == 0
        assert decision["error_count"] == 0
        assert decision["has_corrections"] == False

        assert state.should_continue_execution()
        assert not state.should_return_to_agent()
        assert not state.should_end_processing()

    def test_correctable_tools(self):
        """Test handling of correctable tool calls."""
        state = ValidationRoutingState()

        # Add correctable invalid tool
        correctable = ToolValidationResult(
            tool_call_id="correctable_001",
            tool_name="fixable_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            corrected_args={"fixed": "args"},
        )
        state.add_validation_result(correctable)

        # Add non-correctable invalid tool
        uncorrectable = ToolValidationResult(
            tool_call_id="uncorrectable_001",
            tool_name="broken_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.AGENT,
        )
        state.add_validation_result(uncorrectable)

        correctable_calls = state.get_correctable_tool_calls()
        assert len(correctable_calls) == 1
        assert correctable_calls[0].tool_call_id == "correctable_001"
        assert correctable_calls[0].corrected_args == {"fixed": "args"}

        # When all invalid but some correctable, should retry
        assert state.next_action == RouteRecommendation.RETRY

    def test_tool_message_updates(self):
        """Test tool message update preparation."""
        state = ValidationRoutingState()

        result = ToolValidationResult(
            tool_call_id="update_001",
            tool_name="test_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            errors=["Error 1", "Error 2"],
            warnings=["Warning 1"],
            corrected_args={"corrected": True},
            target_node="retry_node",
            engine_name="test_engine",
        )

        state.add_validation_result(result)

        updates = state.tool_message_updates["update_001"]
        assert updates["validation_status"] == "invalid"
        assert updates["validation_errors"] == ["Error 1", "Error 2"]
        assert updates["validation_warnings"] == ["Warning 1"]
        assert updates["route_recommendation"] == "retry"
        assert updates["target_node"] == "retry_node"
        assert updates["engine_name"] == "test_engine"
        assert updates["corrected_args"] == {"corrected": True}

    def test_validation_state_manager(self):
        """Test ValidationStateManager utility methods."""
        # Create validation result
        result = ValidationStateManager.create_validation_result(
            tool_call_id="mgr_001",
            tool_name="managed_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            errors=["test error"],
            warnings=["test warning"],
            priority=5,
        )

        assert result.tool_call_id == "mgr_001"
        assert result.priority == 5
        assert result.errors == ["test error"]
        assert result.warnings == ["test warning"]

        # Create routing state
        state = ValidationStateManager.create_routing_state()
        assert isinstance(state, ValidationRoutingState)
        assert state.total_tools == 0

        # Merge states
        state1 = ValidationStateManager.create_routing_state()
        state1.add_validation_result(
            ValidationStateManager.create_validation_result(
                tool_call_id="merge_001",
                tool_name="tool1",
                status=ValidationStatus.VALID,
                route_recommendation=RouteRecommendation.EXECUTE,
            )
        )

        state2 = ValidationStateManager.create_routing_state()
        state2.add_validation_result(
            ValidationStateManager.create_validation_result(
                tool_call_id="merge_002",
                tool_name="tool2",
                status=ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.AGENT,
            )
        )

        merged = ValidationStateManager.merge_routing_states([state1, state2])
        assert merged.total_tools == 2
        assert len(merged.valid_tool_calls) == 1
        assert len(merged.invalid_tool_calls) == 1
        assert "merge_001" in merged.tool_validations
        assert "merge_002" in merged.tool_validations

    def test_routing_summary(self):
        """Test routing summary generation."""
        state = ValidationRoutingState()

        # Add mixed results
        state.add_validation_result(
            ToolValidationResult(
                tool_call_id="summary_001",
                tool_name="tool1",
                status=ValidationStatus.VALID,
                route_recommendation=RouteRecommendation.EXECUTE,
                target_node="node1",
            )
        )
        state.add_validation_result(
            ToolValidationResult(
                tool_call_id="summary_002",
                tool_name="tool2",
                status=ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.RETRY,
                target_node="node2",
            )
        )

        summary = state.get_routing_summary()
        assert "Validated 2 tool calls" in summary
        assert "Valid: 1" in summary
        assert "Invalid: 1" in summary
        assert "Errors: 0" in summary
        assert "Target nodes:" in summary
        assert "Next action: execute" in summary


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
