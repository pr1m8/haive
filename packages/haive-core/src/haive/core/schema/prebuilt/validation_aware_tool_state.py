"""
Validation-Aware Tool State - Enhanced ToolState with validation tracking.

This state schema extends ToolState to include validation result tracking
and computed fields for intelligent routing decisions based on validation
patterns and history.
"""

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from pydantic import Field, computed_field, model_validator

from haive.core.graph.node.stateful_validation_node import ToolCallValidationResult
from haive.core.schema.prebuilt.tool_state import ToolState

logger = logging.getLogger(__name__)


class ValidationAwareToolState(ToolState):
    """
    Enhanced ToolState with validation result tracking and computed fields.

    This state schema extends ToolState to include:
    - Validation result tracking from stateful validation nodes
    - Computed fields for validation statistics and routing decisions
    - Validation history management
    - Intelligent routing based on validation patterns

    Key features:
    - Tracks validation results from tool calls
    - Computes validation statistics for routing decisions
    - Maintains validation history for analysis
    - Provides computed fields for tool call success rates
    - Supports validation-based routing strategies
    """

    # Validation tracking fields
    validation_results: List[ToolCallValidationResult] = Field(
        default_factory=list, description="Current validation results from tool calls"
    )
    validation_history: List[ToolCallValidationResult] = Field(
        default_factory=list, description="Historical validation results"
    )
    validation_stats: Dict[str, Any] = Field(
        default_factory=dict, description="Computed validation statistics"
    )

    # Validation configuration
    validation_history_limit: int = Field(
        default=100, description="Maximum validation results to keep in history"
    )
    validation_success_threshold: float = Field(
        default=0.8, description="Minimum success rate for routing decisions"
    )

    @computed_field
    @property
    def current_validation_success_rate(self) -> float:
        """Current validation success rate from recent results."""
        if not self.validation_results:
            return 1.0  # No validations yet, assume success

        valid_count = sum(1 for r in self.validation_results if r.is_valid)
        return valid_count / len(self.validation_results)

    @computed_field
    @property
    def overall_validation_success_rate(self) -> float:
        """Overall validation success rate from history."""
        if not self.validation_history:
            return 1.0  # No history yet, assume success

        valid_count = sum(1 for r in self.validation_history if r.is_valid)
        return valid_count / len(self.validation_history)

    @computed_field
    @property
    def validation_success_by_tool(self) -> Dict[str, float]:
        """Validation success rate by tool name."""
        if not self.validation_history:
            return {}

        tool_stats = {}
        for result in self.validation_history:
            tool_name = result.tool_name
            if tool_name not in tool_stats:
                tool_stats[tool_name] = {"total": 0, "valid": 0}

            tool_stats[tool_name]["total"] += 1
            if result.is_valid:
                tool_stats[tool_name]["valid"] += 1

        return {
            tool_name: stats["valid"] / stats["total"] if stats["total"] > 0 else 0
            for tool_name, stats in tool_stats.items()
        }

    @computed_field
    @property
    def validation_success_by_type(self) -> Dict[str, float]:
        """Validation success rate by validation type."""
        if not self.validation_history:
            return {}

        type_stats = {}
        for result in self.validation_history:
            vtype = result.validation_type
            if vtype not in type_stats:
                type_stats[vtype] = {"total": 0, "valid": 0}

            type_stats[vtype]["total"] += 1
            if result.is_valid:
                type_stats[vtype]["valid"] += 1

        return {
            vtype: stats["valid"] / stats["total"] if stats["total"] > 0 else 0
            for vtype, stats in type_stats.items()
        }

    @computed_field
    @property
    def recent_validation_failures(self) -> List[ToolCallValidationResult]:
        """Recent validation failures for analysis."""
        return [result for result in self.validation_results if not result.is_valid]

    @computed_field
    @property
    def problematic_tools(self) -> List[str]:
        """Tools with success rates below threshold."""
        return [
            tool_name
            for tool_name, success_rate in self.validation_success_by_tool.items()
            if success_rate < self.validation_success_threshold
        ]

    @computed_field
    @property
    def recommended_routing_strategy(self) -> str:
        """Recommended routing strategy based on validation patterns."""
        if not self.validation_history:
            return "default"

        current_rate = self.current_validation_success_rate
        overall_rate = self.overall_validation_success_rate

        if current_rate < 0.5:
            return "conservative"  # Route to safer options
        elif current_rate > 0.9 and overall_rate > 0.8:
            return "aggressive"  # Route to more complex tools
        else:
            return "balanced"  # Standard routing

    @computed_field
    @property
    def validation_trending(self) -> str:
        """Trend in validation success (improving, declining, stable)."""
        if len(self.validation_history) < 10:
            return "insufficient_data"

        # Compare recent vs older validation rates
        recent_results = self.validation_history[-10:]
        older_results = (
            self.validation_history[-20:-10]
            if len(self.validation_history) >= 20
            else []
        )

        if not older_results:
            return "insufficient_data"

        recent_rate = sum(1 for r in recent_results if r.is_valid) / len(recent_results)
        older_rate = sum(1 for r in older_results if r.is_valid) / len(older_results)

        if recent_rate > older_rate + 0.1:
            return "improving"
        elif recent_rate < older_rate - 0.1:
            return "declining"
        else:
            return "stable"

    @model_validator(mode="after")
    def update_validation_stats(self) -> "ValidationAwareToolState":
        """Update validation statistics after model creation."""
        # Call parent validator
        super().sync_tools_and_update_routes()

        # Update validation stats if we have new results
        if self.validation_results:
            self._update_validation_statistics()

        return self

    def _update_validation_statistics(self) -> None:
        """Update internal validation statistics."""
        if not self.validation_history:
            return

        # Calculate basic stats
        total_validations = len(self.validation_history)
        valid_validations = sum(1 for r in self.validation_history if r.is_valid)
        invalid_validations = total_validations - valid_validations

        # Calculate stats by validation type
        type_stats = {}
        for result in self.validation_history:
            vtype = result.validation_type
            if vtype not in type_stats:
                type_stats[vtype] = {"total": 0, "valid": 0, "invalid": 0}

            type_stats[vtype]["total"] += 1
            if result.is_valid:
                type_stats[vtype]["valid"] += 1
            else:
                type_stats[vtype]["invalid"] += 1

        # Calculate stats by tool name
        tool_stats = {}
        for result in self.validation_history:
            tool_name = result.tool_name
            if tool_name not in tool_stats:
                tool_stats[tool_name] = {"total": 0, "valid": 0, "invalid": 0}

            tool_stats[tool_name]["total"] += 1
            if result.is_valid:
                tool_stats[tool_name]["valid"] += 1
            else:
                tool_stats[tool_name]["invalid"] += 1

        self.validation_stats = {
            "total_validations": total_validations,
            "valid_validations": valid_validations,
            "invalid_validations": invalid_validations,
            "success_rate": (
                valid_validations / total_validations if total_validations > 0 else 0
            ),
            "type_stats": type_stats,
            "tool_stats": tool_stats,
            "last_updated": datetime.utcnow().isoformat(),
        }

    def add_validation_result(self, result: ToolCallValidationResult) -> None:
        """Add a new validation result and update statistics."""
        self.validation_results.append(result)
        self.validation_history.append(result)

        # Limit history size
        if len(self.validation_history) > self.validation_history_limit:
            self.validation_history = self.validation_history[
                -self.validation_history_limit :
            ]

        # Update statistics
        self._update_validation_statistics()

        logger.debug(
            f"Added validation result for {result.tool_name}: {result.is_valid}"
        )

    def clear_current_validation_results(self) -> None:
        """Clear current validation results (keep history)."""
        self.validation_results = []
        logger.debug("Cleared current validation results")

    def get_validation_summary(self) -> Dict[str, Any]:
        """Get a summary of validation performance."""
        return {
            "current_success_rate": self.current_validation_success_rate,
            "overall_success_rate": self.overall_validation_success_rate,
            "validation_trending": self.validation_trending,
            "recommended_strategy": self.recommended_routing_strategy,
            "problematic_tools": self.problematic_tools,
            "recent_failures": len(self.recent_validation_failures),
            "total_validations": len(self.validation_history),
            "success_by_tool": self.validation_success_by_tool,
            "success_by_type": self.validation_success_by_type,
        }

    def should_route_to_tool(self, tool_name: str) -> bool:
        """Determine if a tool should be routed to based on validation history."""
        if tool_name not in self.validation_success_by_tool:
            return True  # No history, allow routing

        success_rate = self.validation_success_by_tool[tool_name]
        return success_rate >= self.validation_success_threshold

    def get_preferred_tools(self) -> List[str]:
        """Get tools with good validation success rates."""
        return [
            tool_name
            for tool_name, success_rate in self.validation_success_by_tool.items()
            if success_rate >= self.validation_success_threshold
        ]

    def get_routing_recommendation(self, available_destinations: List[str]) -> str:
        """Get routing recommendation based on validation patterns."""
        strategy = self.recommended_routing_strategy

        if strategy == "conservative":
            # Prefer parser over tool execution
            if "parse_output" in available_destinations:
                return "parse_output"
            elif "END" in available_destinations:
                return "END"
        elif strategy == "aggressive":
            # Prefer tool execution over parsing
            if "tool_node" in available_destinations:
                return "tool_node"

        # Default/balanced strategy
        return available_destinations[0] if available_destinations else "END"
