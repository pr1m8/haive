"""Enhanced validation state for tool message routing and conditional branching."""

import time
from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union

from pydantic import BaseModel, Field


class ValidationStatus(str, Enum):
    """Status of tool validation."""

    PENDING = "pending"
    VALID = "valid"
    INVALID = "invalid"
    ERROR = "error"
    SKIPPED = "skipped"


class RouteRecommendation(str, Enum):
    """Routing recommendations for validated tools."""

    EXECUTE = "execute"  # Execute the tool
    RETRY = "retry"  # Retry with corrections
    SKIP = "skip"  # Skip this tool
    REDIRECT = "redirect"  # Redirect to different tool
    AGENT = "agent"  # Return to agent for clarification
    END = "end"  # End processing


class ToolValidationResult(BaseModel):
    """Result of validating a single tool call."""

    tool_call_id: str = Field(..., description="ID of the tool call")
    tool_name: str = Field(..., description="Name of the tool")
    status: ValidationStatus = Field(..., description="Validation status")
    route_recommendation: RouteRecommendation = Field(
        ..., description="Routing recommendation"
    )

    # Validation details
    errors: List[str] = Field(default_factory=list, description="Validation errors")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    corrected_args: Optional[Dict[str, Any]] = Field(
        default=None, description="Corrected arguments"
    )

    # Routing details
    target_node: Optional[str] = Field(default=None, description="Specific target node")
    engine_name: Optional[str] = Field(default=None, description="Recommended engine")
    priority: int = Field(default=0, description="Execution priority")

    # Metadata
    validation_time: float = Field(
        default_factory=time.time, description="Validation timestamp"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )


class ValidationRoutingState(BaseModel):
    """State for managing validation results and routing decisions."""

    # Validation results
    tool_validations: Dict[str, ToolValidationResult] = Field(
        default_factory=dict, description="Validation results keyed by tool_call_id"
    )

    # Routing decisions
    valid_tool_calls: List[str] = Field(
        default_factory=list, description="Tool call IDs that passed validation"
    )
    invalid_tool_calls: List[str] = Field(
        default_factory=list, description="Tool call IDs that failed validation"
    )
    error_tool_calls: List[str] = Field(
        default_factory=list, description="Tool call IDs that had validation errors"
    )

    # Routing state
    next_action: RouteRecommendation = Field(
        default=RouteRecommendation.EXECUTE,
        description="Overall recommendation for next action",
    )
    target_nodes: Set[str] = Field(
        default_factory=set, description="Set of target nodes for routing"
    )

    # Message updates
    tool_message_updates: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict, description="Updates to apply to tool messages"
    )

    # Branch decision data
    branch_data: Dict[str, Any] = Field(
        default_factory=dict, description="Data for conditional branching decisions"
    )

    # Statistics
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
            "branch_data": self.branch_data,
        }

    def get_valid_tool_calls(self) -> List[ToolValidationResult]:
        """Get validation results for valid tool calls."""
        return [
            self.tool_validations[call_id]
            for call_id in self.valid_tool_calls
            if call_id in self.tool_validations
        ]

    def get_invalid_tool_calls(self) -> List[ToolValidationResult]:
        """Get validation results for invalid tool calls."""
        return [
            self.tool_validations[call_id]
            for call_id in self.invalid_tool_calls
            if call_id in self.tool_validations
        ]

    def get_error_tool_calls(self) -> List[ToolValidationResult]:
        """Get validation results for error tool calls."""
        return [
            self.tool_validations[call_id]
            for call_id in self.error_tool_calls
            if call_id in self.tool_validations
        ]

    def get_correctable_tool_calls(self) -> List[ToolValidationResult]:
        """Get tool calls that have corrections available."""
        return [
            result
            for result in self.tool_validations.values()
            if result.corrected_args is not None
        ]

    def should_continue_execution(self) -> bool:
        """Check if execution should continue based on validation results."""
        return (
            self.next_action in [RouteRecommendation.EXECUTE, RouteRecommendation.RETRY]
            and len(self.valid_tool_calls) > 0
        )

    def should_return_to_agent(self) -> bool:
        """Check if processing should return to agent."""
        return self.next_action == RouteRecommendation.AGENT

    def should_end_processing(self) -> bool:
        """Check if processing should end."""
        return self.next_action == RouteRecommendation.END

    def get_routing_summary(self) -> str:
        """Get a human-readable summary of routing decisions."""
        summary_parts = [
            f"Validated {self.total_tools} tool calls",
            f"Valid: {len(self.valid_tool_calls)}",
            f"Invalid: {len(self.invalid_tool_calls)}",
            f"Errors: {len(self.error_tool_calls)}",
        ]

        if self.target_nodes:
            summary_parts.append(f"Target nodes: {', '.join(self.target_nodes)}")

        summary_parts.append(f"Next action: {self.next_action.value}")

        return " | ".join(summary_parts)


class ValidationStateManager:
    """Manager for validation state operations."""

    @staticmethod
    def create_validation_result(
        tool_call_id: str,
        tool_name: str,
        status: ValidationStatus,
        route_recommendation: RouteRecommendation = RouteRecommendation.EXECUTE,
        errors: Optional[List[str]] = None,
        warnings: Optional[List[str]] = None,
        corrected_args: Optional[Dict[str, Any]] = None,
        target_node: Optional[str] = None,
        engine_name: Optional[str] = None,
        priority: int = 0,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> ToolValidationResult:
        """Create a validation result with all parameters."""
        return ToolValidationResult(
            tool_call_id=tool_call_id,
            tool_name=tool_name,
            status=status,
            route_recommendation=route_recommendation,
            errors=errors or [],
            warnings=warnings or [],
            corrected_args=corrected_args,
            target_node=target_node,
            engine_name=engine_name,
            priority=priority,
            metadata=metadata or {},
        )

    @staticmethod
    def create_routing_state() -> ValidationRoutingState:
        """Create a new validation routing state."""
        return ValidationRoutingState()

    @staticmethod
    def merge_routing_states(
        states: List[ValidationRoutingState],
    ) -> ValidationRoutingState:
        """Merge multiple routing states into one."""
        merged = ValidationRoutingState()

        for state in states:
            # Merge validation results
            merged.tool_validations.update(state.tool_validations)

            # Merge routing lists
            merged.valid_tool_calls.extend(state.valid_tool_calls)
            merged.invalid_tool_calls.extend(state.invalid_tool_calls)
            merged.error_tool_calls.extend(state.error_tool_calls)

            # Merge target nodes
            merged.target_nodes.update(state.target_nodes)

            # Merge message updates
            merged.tool_message_updates.update(state.tool_message_updates)

            # Merge branch data
            merged.branch_data.update(state.branch_data)

            # Update duration
            merged.validation_duration += state.validation_duration

        # Update totals and next action
        merged.total_tools = len(merged.tool_validations)
        merged._update_next_action()

        return merged
