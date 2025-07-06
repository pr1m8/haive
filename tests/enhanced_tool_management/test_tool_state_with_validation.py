"""Direct tests for ToolStateWithValidation."""

import os
import sys

import pytest

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

try:
    from packages.haive_core.src.haive.core.graph.node.validation_node_with_routing import (
        ValidationNodeWithRouting,
    )
    from packages.haive_core.src.haive.core.schema.prebuilt.tool_state_with_validation import (
        ToolStateWithValidation,
    )
    from packages.haive_core.src.haive.core.schema.prebuilt.tools.validation_state import (
        RouteRecommendation,
        ValidationStateManager,
        ValidationStatus,
    )

    IMPORTS_AVAILABLE = True
except ImportError as e:
    IMPORTS_AVAILABLE = False


class MockTool:
    """Mock tool for testing."""

    def __init__(self, name):
        self.name = name
        self.args_schema = None


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
class TestToolStateWithValidation:
    """Test ToolStateWithValidation functionality."""

    def test_create_tool_state_with_validation(self):
        """Test creating a ToolStateWithValidation instance."""
        state = ToolStateWithValidation()

        assert hasattr(state, "validation_state")
        assert hasattr(state, "tool_metadata")
        assert hasattr(state, "tool_performance")
        assert hasattr(state, "tool_message_status")
        assert hasattr(state, "branch_conditions")

    def test_add_tool_with_validation(self):
        """Test adding a tool with validation metadata."""
        state = ToolStateWithValidation()

        # Add a mock tool
        tool = MockTool("test_tool")
        state.tools.append(tool)
        state.tool_routes["test_tool"] = "langchain_tool"

        # Verify tool was added
        assert len(state.tools) == 1
        assert "test_tool" in state.tool_routes

    def test_apply_validation_results(self):
        """Test applying validation results to state."""
        state = ToolStateWithValidation()

        # Create validation results
        routing_state = ValidationStateManager.create_routing_state()
        result = ValidationStateManager.create_validation_result(
            tool_call_id="test_call",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        routing_state.add_validation_result(result)

        # Apply results
        state.apply_validation_results(routing_state)

        # Verify results were applied
        assert state.validation_state.total_tools == 1
        assert "test_call" in state.tool_message_status
        assert state.tool_message_status["test_call"] == "valid"

    def test_routing_decisions(self):
        """Test routing decision methods."""
        state = ToolStateWithValidation()

        # Initially should not continue
        assert not state.should_continue_to_tools()
        assert not state.should_return_to_agent()
        assert state.should_end_processing()

        # Add valid validation result
        routing_state = ValidationStateManager.create_routing_state()
        result = ValidationStateManager.create_validation_result(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
        )
        routing_state.add_validation_result(result)
        state.apply_validation_results(routing_state)

        # Now should continue
        assert state.should_continue_to_tools()
        assert not state.should_return_to_agent()
        assert not state.should_end_processing()

    def test_branch_conditions(self):
        """Test branch condition management."""
        state = ToolStateWithValidation()

        # Set branch condition
        state.set_branch_condition("test_condition", True)

        # Get branch condition
        assert state.get_branch_condition("test_condition")
        assert state.get_branch_condition("missing", "default") == "default"

        # Evaluate simple condition
        state.set_branch_condition("value", 10)
        assert state.evaluate_branch_condition("value > 5")
        assert not state.evaluate_branch_condition("value < 5")

    def test_performance_tracking(self):
        """Test tool performance tracking."""
        state = ToolStateWithValidation()

        # Track execution
        state.track_tool_execution("test_tool", 0.5, True)

        # Verify tracking
        assert "test_tool" in state.tool_performance
        metrics = state.tool_performance["test_tool"]
        assert metrics["total_executions"] == 1
        assert metrics["successful_executions"] == 1
        assert metrics["success_rate"] == 1.0
        assert metrics["avg_execution_time"] == 0.5

        # Track another execution
        state.track_tool_execution("test_tool", 1.0, False)

        # Verify updated metrics
        metrics = state.tool_performance["test_tool"]
        assert metrics["total_executions"] == 2
        assert metrics["successful_executions"] == 1
        assert metrics["success_rate"] == 0.5
        # Average should be weighted
        assert 0.5 < metrics["avg_execution_time"] < 1.0


@pytest.mark.skipif(not IMPORTS_AVAILABLE, reason="Required imports not available")
class TestValidationNodeWithRouting:
    """Test ValidationNodeWithRouting functionality."""

    def test_create_validation_node(self):
        """Test creating a ValidationNodeWithRouting instance."""
        node = ValidationNodeWithRouting()

        assert hasattr(node, "update_tool_messages")
        assert hasattr(node, "provide_routing_state")
        assert hasattr(node, "auto_correct_args")
        assert node.update_tool_messages
        assert node.provide_routing_state

    def test_node_function_creation(self):
        """Test creating the validation node function."""
        node = ValidationNodeWithRouting()

        # Create node function
        node_func = node.create_node_function()

        # Verify it's callable
        assert callable(node_func)


if __name__ == "__main__":
    # Run tests directly
    if IMPORTS_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
