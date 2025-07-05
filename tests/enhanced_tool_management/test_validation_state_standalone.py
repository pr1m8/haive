"""Standalone tests for validation state (without full haive imports)."""

import pytest
import time
from enum import Enum
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, Field


# Copy the validation state classes for standalone testing
class ValidationStatus(str, Enum):
    """Status of tool validation."""
    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    ERROR = "error"
    SKIPPED = "skipped"


class RouteRecommendation(str, Enum):
    """Routing recommendations for validated tools."""
    EXECUTE = "execute"
    RETRY = "retry"
    SKIP = "skip"
    REDIRECT = "redirect"
    AGENT = "agent"
    END = "end"


class ToolValidationResult(BaseModel):
    """Result of validating a single tool call."""
    
    tool_call_id: str = Field(..., description="ID of the tool call")
    tool_name: str = Field(..., description="Name of the tool")
    status: ValidationStatus = Field(..., description="Validation status")
    route_recommendation: RouteRecommendation = Field(..., description="Routing recommendation")
    
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    corrected_args: Optional[Dict[str, Any]] = Field(default=None, description="Corrected arguments")
    
    target_node: Optional[str] = Field(default=None, description="Specific target node")
    engine_name: Optional[str] = Field(default=None, description="Recommended engine")
    priority: int = Field(default=0, description="Execution priority")
    
    validation_time: float = Field(default_factory=time.time, description="Validation timestamp")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class ValidationRoutingState(BaseModel):
    """State for managing validation results and routing decisions."""
    
    tool_validations: Dict[str, ToolValidationResult] = Field(
        default_factory=dict,
        description="Validation results keyed by tool_call_id"
    )
    
    valid_tool_calls: List[str] = Field(
        default_factory=list,
        description="Tool call IDs that passed validation"
    )
    invalid_tool_calls: List[str] = Field(
        default_factory=list,
        description="Tool call IDs that failed validation"
    )
    error_tool_calls: List[str] = Field(
        default_factory=list,
        description="Tool call IDs that had validation errors"
    )
    
    next_action: RouteRecommendation = Field(
        default=RouteRecommendation.EXECUTE,
        description="Overall recommendation for next action"
    )
    target_nodes: Set[str] = Field(
        default_factory=set,
        description="Set of target nodes for routing"
    )
    
    tool_message_updates: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Updates to apply to tool messages"
    )
    
    branch_data: Dict[str, Any] = Field(
        default_factory=dict,
        description="Data for conditional branching decisions"
    )
    
    total_tools: int = Field(default=0, description="Total number of tool calls")
    validation_duration: float = Field(default=0.0, description="Total validation time")
    
    def add_validation_result(self, result: ToolValidationResult) -> None:
        """Add a validation result and update routing state."""
        self.tool_validations[result.tool_call_id] = result
        
        # Update routing lists
        if result.status == ValidationStatus.VALID:
            self.valid_tool_calls.append(result.tool_call_id)
        elif result.status == ValidationStatus.INVALID:
            self.invalid_tool_calls.append(result.tool_call_id)
        elif result.status == ValidationStatus.ERROR:
            self.error_tool_calls.append(result.tool_call_id)
        
        # Update target nodes
        if result.target_node:
            self.target_nodes.add(result.target_node)
        
        # Update total count
        self.total_tools = len(self.tool_validations)
        
        # Update overall recommendation
        self._update_next_action()
        
        # Prepare message updates
        self._prepare_message_updates(result)
    
    def _update_next_action(self) -> None:
        """Update the overall next action based on validation results."""
        if not self.tool_validations:
            self.next_action = RouteRecommendation.END
            return
        
        # Check for errors first
        if self.error_tool_calls:
            self.next_action = RouteRecommendation.AGENT
            return
        
        # If we have valid tools, execute them
        if self.valid_tool_calls:
            self.next_action = RouteRecommendation.EXECUTE
            return
        
        # If all invalid, retry or return to agent
        if len(self.invalid_tool_calls) == self.total_tools:
            # Check if we have corrections
            has_corrections = any(
                result.corrected_args is not None
                for result in self.tool_validations.values()
                if result.status == ValidationStatus.INVALID
            )
            
            if has_corrections:
                self.next_action = RouteRecommendation.RETRY
            else:
                self.next_action = RouteRecommendation.AGENT
            return
        
        # Default to execute
        self.next_action = RouteRecommendation.EXECUTE
    
    def _prepare_message_updates(self, result: ToolValidationResult) -> None:
        """Prepare message updates for a validation result."""
        updates = {}
        
        # Add validation status to message metadata
        updates["validation_status"] = result.status.value
        updates["validation_time"] = result.validation_time
        
        # Add errors/warnings if present
        if result.errors:
            updates["validation_errors"] = result.errors
        if result.warnings:
            updates["validation_warnings"] = result.warnings
        
        # Add routing information
        updates["route_recommendation"] = result.route_recommendation.value
        if result.target_node:
            updates["target_node"] = result.target_node
        if result.engine_name:
            updates["engine_name"] = result.engine_name
        
        # Add corrected args if available
        if result.corrected_args:
            updates["corrected_args"] = result.corrected_args
        
        self.tool_message_updates[result.tool_call_id] = updates
    
    def get_routing_decision(self) -> Dict[str, Any]:
        """Get routing decision data for conditional branching."""
        return {
            "next_action": self.next_action.value,
            "target_nodes": list(self.target_nodes),
            "valid_count": len(self.valid_tool_calls),
            "invalid_count": len(self.invalid_tool_calls),
            "error_count": len(self.error_tool_calls),
            "total_count": self.total_tools,
            "has_corrections": any(
                "corrected_args" in updates
                for updates in self.tool_message_updates.values()
            ),
            "validation_duration": self.validation_duration,
            "branch_data": self.branch_data
        }
    
    def should_continue_execution(self) -> bool:
        """Check if execution should continue based on validation results."""
        return (
            self.next_action in [RouteRecommendation.EXECUTE, RouteRecommendation.RETRY] and
            len(self.valid_tool_calls) > 0
        )
    
    def should_return_to_agent(self) -> bool:
        """Check if processing should return to agent."""
        return self.next_action == RouteRecommendation.AGENT
    
    def should_end_processing(self) -> bool:
        """Check if processing should end."""
        return self.next_action == RouteRecommendation.END


class TestValidationStateStandalone:
    """Test validation state functionality in isolation."""
    
    def test_validation_result_creation(self):
        """Test creating validation results."""
        result = ToolValidationResult(
            tool_call_id="test_call",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE
        )
        
        assert result.tool_call_id == "test_call"
        assert result.tool_name == "test_tool"
        assert result.status == ValidationStatus.VALID
        assert result.route_recommendation == RouteRecommendation.EXECUTE
        assert result.errors == []
        assert result.warnings == []
        assert result.corrected_args is None
    
    def test_routing_state_creation(self):
        """Test creating routing state."""
        state = ValidationRoutingState()
        
        assert state.total_tools == 0
        assert state.next_action == RouteRecommendation.EXECUTE
        assert len(state.valid_tool_calls) == 0
        assert len(state.invalid_tool_calls) == 0
        assert len(state.error_tool_calls) == 0
    
    def test_add_valid_result(self):
        """Test adding valid validation result."""
        state = ValidationRoutingState()
        
        result = ToolValidationResult(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node="tool_node"
        )
        
        state.add_validation_result(result)
        
        assert state.total_tools == 1
        assert len(state.valid_tool_calls) == 1
        assert "valid_call" in state.valid_tool_calls
        assert state.next_action == RouteRecommendation.EXECUTE
        assert "tool_node" in state.target_nodes
    
    def test_add_invalid_result(self):
        """Test adding invalid validation result."""
        state = ValidationRoutingState()
        
        result = ToolValidationResult(
            tool_call_id="invalid_call",
            tool_name="invalid_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Invalid argument"],
            target_node="agent_node"
        )
        
        state.add_validation_result(result)
        
        assert state.total_tools == 1
        assert len(state.invalid_tool_calls) == 1
        assert "invalid_call" in state.invalid_tool_calls
        assert state.next_action == RouteRecommendation.AGENT
        assert "agent_node" in state.target_nodes
    
    def test_add_error_result(self):
        """Test adding error validation result."""
        state = ValidationRoutingState()
        
        result = ToolValidationResult(
            tool_call_id="error_call",
            tool_name="error_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT,
            errors=["Tool not found"]
        )
        
        state.add_validation_result(result)
        
        assert state.total_tools == 1
        assert len(state.error_tool_calls) == 1
        assert "error_call" in state.error_tool_calls
        assert state.next_action == RouteRecommendation.AGENT
    
    def test_mixed_results_priority(self):
        """Test priority handling with mixed results."""
        state = ValidationRoutingState()
        
        # Add valid result first
        valid_result = ToolValidationResult(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE
        )
        state.add_validation_result(valid_result)
        
        # Add invalid result
        invalid_result = ToolValidationResult(
            tool_call_id="invalid_call",
            tool_name="invalid_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            corrected_args={"query": "corrected"}
        )
        state.add_validation_result(invalid_result)
        
        assert state.total_tools == 2
        assert len(state.valid_tool_calls) == 1
        assert len(state.invalid_tool_calls) == 1
        # Should execute because we have valid tools
        assert state.next_action == RouteRecommendation.EXECUTE
    
    def test_error_takes_precedence(self):
        """Test that errors take precedence over valid tools."""
        state = ValidationRoutingState()
        
        # Add valid result
        valid_result = ToolValidationResult(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE
        )
        state.add_validation_result(valid_result)
        assert state.next_action == RouteRecommendation.EXECUTE
        
        # Add error result - should change next action
        error_result = ToolValidationResult(
            tool_call_id="error_call",
            tool_name="error_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT
        )
        state.add_validation_result(error_result)
        
        assert state.next_action == RouteRecommendation.AGENT
    
    def test_routing_decision_data(self):
        """Test routing decision data generation."""
        state = ValidationRoutingState()
        
        result = ToolValidationResult(
            tool_call_id="test_call",
            tool_name="test_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            corrected_args={"query": "test"}
        )
        state.add_validation_result(result)
        
        decision = state.get_routing_decision()
        
        assert decision["next_action"] == "execute"
        assert decision["valid_count"] == 1
        assert decision["invalid_count"] == 0
        assert decision["error_count"] == 0
        assert decision["total_count"] == 1
        assert decision["has_corrections"] == True
    
    def test_should_continue_execution(self):
        """Test execution continuation logic."""
        state = ValidationRoutingState()
        
        # No tools - should not continue
        assert not state.should_continue_execution()
        
        # Add valid tool - should continue
        valid_result = ToolValidationResult(
            tool_call_id="valid_call",
            tool_name="valid_tool",
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE
        )
        state.add_validation_result(valid_result)
        assert state.should_continue_execution()
        
        # Add error - should not continue (return to agent)
        error_result = ToolValidationResult(
            tool_call_id="error_call",
            tool_name="error_tool",
            status=ValidationStatus.ERROR,
            route_recommendation=RouteRecommendation.AGENT
        )
        state.add_validation_result(error_result)
        
        assert not state.should_continue_execution()
        assert state.should_return_to_agent()
    
    def test_message_updates_generation(self):
        """Test tool message updates generation."""
        state = ValidationRoutingState()
        
        result = ToolValidationResult(
            tool_call_id="test_call",
            tool_name="test_tool",
            status=ValidationStatus.INVALID,
            route_recommendation=RouteRecommendation.RETRY,
            errors=["Missing field"],
            warnings=["Deprecated parameter"],
            corrected_args={"field": "value"},
            target_node="tool_node",
            engine_name="test_engine"
        )
        
        state.add_validation_result(result)
        
        updates = state.tool_message_updates["test_call"]
        
        assert updates["validation_status"] == "invalid"
        assert updates["validation_errors"] == ["Missing field"]
        assert updates["validation_warnings"] == ["Deprecated parameter"]
        assert updates["route_recommendation"] == "retry"
        assert updates["target_node"] == "tool_node"
        assert updates["engine_name"] == "test_engine"
        assert updates["corrected_args"] == {"field": "value"}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])