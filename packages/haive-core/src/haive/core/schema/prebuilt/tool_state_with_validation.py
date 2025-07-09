"""Enhanced ToolState with validation routing and tool message management."""

import logging
import time
from typing import Any, Callable, Dict, List, Optional, Set, Union

from pydantic import Field, model_validator

from haive.core.schema.prebuilt.tool_state import ToolState
from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationRoutingState,
    ValidationStateManager,
    ValidationStatus,
)

logger = logging.getLogger(__name__)


class EnhancedToolState(ToolState):
    """Enhanced ToolState with validation routing and tool message management.

    Extends the prebuilt ToolState with:
    - Validation state management for routing decisions
    - Tool message updates and status tracking
    - Conditional branching support
    - Enhanced tool categorization and performance tracking

    Maintains full compatibility with existing ToolState functionality while
    adding powerful validation and routing capabilities.
    """

    # Validation and routing state
    validation_state: ValidationRoutingState = Field(
        default_factory=ValidationStateManager.create_routing_state,
        description="State for validation results and routing decisions",
    )

    # Enhanced tool management
    tool_metadata: Dict[str, Dict[str, Any]] = Field(
        default_factory=dict,
        description="Rich metadata for each tool including categories, priorities, etc.",
    )

    tool_performance: Dict[str, Dict[str, float]] = Field(
        default_factory=dict,
        description="Performance metrics for tool execution tracking",
    )

    tool_execution_history: List[Dict[str, Any]] = Field(
        default_factory=list, description="History of tool executions for analysis"
    )

    # Tool organization (excluded from serialization due to sets)
    tool_categories: Dict[str, Set[str]] = Field(
        default_factory=dict,
        description="Organization of tools by category",
        exclude=True,
    )

    tool_dependencies: Dict[str, List[str]] = Field(
        default_factory=dict, description="Tool dependency mapping"
    )

    tool_priorities: Dict[str, int] = Field(
        default_factory=dict,
        description="Tool execution priorities (higher = more important)",
    )

    # Message management
    tool_message_status: Dict[str, str] = Field(
        default_factory=dict, description="Status tracking for tool messages"
    )

    # Conditional branching support
    branch_conditions: Dict[str, Any] = Field(
        default_factory=dict, description="Conditions for conditional branching"
    )

    @model_validator(mode="after")
    def enhanced_tool_setup(self) -> "EnhancedToolState":
        """Enhanced setup that preserves ToolState functionality."""
        # Call parent setup first to maintain all existing functionality
        super().sync_tools_and_update_routes()

        # Setup enhanced features
        self._setup_enhanced_tool_features()

        return self

    def _setup_enhanced_tool_features(self) -> None:
        """Setup enhanced tool management features."""
        # Auto-categorize any uncategorized tools
        for tool_name in self.tool_routes.keys():
            if not self._tool_is_categorized(tool_name):
                self._auto_categorize_tool(tool_name)

        # Initialize performance tracking for new tools
        for tool_name in self.tool_routes.keys():
            if tool_name not in self.tool_performance:
                self.tool_performance[tool_name] = {
                    "avg_execution_time": 0.0,
                    "success_rate": 0.0,
                    "total_executions": 0,
                    "successful_executions": 0,
                }

    def _tool_is_categorized(self, tool_name: str) -> bool:
        """Check if a tool is already categorized."""
        return any(tool_name in tools for tools in self.tool_categories.values())

    def _auto_categorize_tool(self, tool_name: str) -> None:
        """Automatically categorize a tool based on its route and name."""
        route = self.tool_routes.get(tool_name, "unknown")

        # Base category from route
        route_categories = {
            "langchain_tool": "execution",
            "pydantic_model": "validation",
            "function": "utility",
            "unknown": "general",
        }

        # Refine based on tool name patterns
        name_lower = tool_name.lower()
        if any(word in name_lower for word in ["search", "query", "find", "retrieve"]):
            category = "retrieval"
        elif any(word in name_lower for word in ["write", "create", "save", "update"]):
            category = "creation"
        elif any(word in name_lower for word in ["analyze", "process", "transform"]):
            category = "processing"
        elif any(word in name_lower for word in ["validate", "check", "verify"]):
            category = "validation"
        else:
            category = route_categories.get(route, "general")

        self.add_tool_to_category(tool_name, category)

    # Enhanced tool management methods

    def add_tool_enhanced(
        self,
        tool: Any,
        route: Optional[str] = None,
        category: Optional[str] = None,
        priority: int = 0,
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        target_engine: Optional[str] = None,
    ) -> None:
        """Enhanced tool addition with metadata and categorization."""
        # Use parent's proven add_tool method
        super().add_tool(tool, route, target_engine)

        # Get tool name for enhancements
        tool_name = self._get_tool_name(tool, len(self.tools) - 1)

        # Add enhanced features
        if category:
            self.add_tool_to_category(tool_name, category)
        else:
            self._auto_categorize_tool(tool_name)

        if priority != 0:
            self.tool_priorities[tool_name] = priority

        if dependencies:
            self.tool_dependencies[tool_name] = dependencies

        if metadata:
            self.tool_metadata[tool_name] = metadata

        # Initialize performance tracking
        if tool_name not in self.tool_performance:
            self.tool_performance[tool_name] = {
                "avg_execution_time": 0.0,
                "success_rate": 0.0,
                "total_executions": 0,
                "successful_executions": 0,
            }

    def add_tool_to_category(self, tool_name: str, category: str) -> None:
        """Add a tool to a category."""
        if category not in self.tool_categories:
            self.tool_categories[category] = set()
        self.tool_categories[category].add(tool_name)

        # Store in metadata for serialization
        if tool_name not in self.tool_metadata:
            self.tool_metadata[tool_name] = {}
        self.tool_metadata[tool_name]["category"] = category

    def get_tools_by_category(self, category: str) -> List[Any]:
        """Get actual tool objects for a category."""
        if category not in self.tool_categories:
            return []

        tool_names = self.tool_categories[category]
        return [
            self.get_tool_by_name(name)
            for name in tool_names
            if self.get_tool_by_name(name)
        ]

    # Validation and routing methods

    def update_tool_message_status(self, tool_call_id: str, status: str) -> None:
        """Update the status of a tool message."""
        self.tool_message_status[tool_call_id] = status
        logger.debug(f"Updated tool message {tool_call_id} status to: {status}")

    def get_tool_message_status(self, tool_call_id: str) -> Optional[str]:
        """Get the status of a tool message."""
        return self.tool_message_status.get(tool_call_id)

    def apply_validation_results(
        self, validation_state: ValidationRoutingState
    ) -> None:
        """Apply validation results to update tool message states."""
        # Update our validation state
        self.validation_state = validation_state

        # Update tool message statuses
        for tool_call_id, result in validation_state.tool_validations.items():
            self.update_tool_message_status(tool_call_id, result.status.value)

        # Update branch conditions with routing data
        self.branch_conditions.update(validation_state.get_routing_decision())

        logger.info(
            f"Applied validation results: {validation_state.get_routing_summary()}"
        )

    def get_validation_routing_data(self) -> Dict[str, Any]:
        """Get data for conditional branching based on validation results."""
        base_data = self.validation_state.get_routing_decision()

        # Add additional routing information
        base_data.update(
            {
                "tool_message_statuses": self.tool_message_status.copy(),
                "available_categories": list(self.tool_categories.keys()),
                "total_tools_in_state": len(self.tools),
                "has_dependencies": len(self.tool_dependencies) > 0,
            }
        )

        return base_data

    def should_continue_to_tools(self) -> bool:
        """Check if execution should continue to tool nodes."""
        return self.validation_state.should_continue_execution()

    def should_return_to_agent(self) -> bool:
        """Check if execution should return to agent for clarification."""
        return self.validation_state.should_return_to_agent()

    def should_end_processing(self) -> bool:
        """Check if processing should end."""
        return self.validation_state.should_end_processing()

    def get_next_nodes(self) -> List[str]:
        """Get recommended next nodes based on validation results."""
        return list(self.validation_state.target_nodes)

    def get_valid_tool_calls_for_execution(self) -> List[Any]:
        """Get tool calls that passed validation and are ready for execution."""
        valid_results = self.validation_state.get_valid_tool_calls()
        return [result.tool_call_id for result in valid_results]

    def get_correctable_tool_calls(self) -> List[Any]:
        """Get tool calls that have corrections available."""
        return self.validation_state.get_correctable_tool_calls()

    # Conditional branching support

    def set_branch_condition(self, condition_name: str, value: Any) -> None:
        """Set a condition for conditional branching."""
        self.branch_conditions[condition_name] = value

    def get_branch_condition(self, condition_name: str, default: Any = None) -> Any:
        """Get a branch condition value."""
        return self.branch_conditions.get(condition_name, default)

    def evaluate_branch_condition(self, condition_expr: str) -> bool:
        """Evaluate a branch condition expression."""
        try:
            # Simple evaluation - in production would use a safer evaluator
            return eval(condition_expr, {"__builtins__": {}}, self.branch_conditions)
        except Exception as e:
            logger.warning(
                f"Failed to evaluate branch condition '{condition_expr}': {e}"
            )
            return False

    # Performance tracking (inherited and enhanced)

    def track_tool_execution(
        self,
        tool_name: str,
        execution_time: float,
        success: bool,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Track tool execution for performance monitoring."""
        # Add to history
        execution_record = {
            "tool_name": tool_name,
            "execution_time": execution_time,
            "success": success,
            "timestamp": time.time(),
            "context": context or {},
        }
        self.tool_execution_history.append(execution_record)

        # Update performance metrics
        if tool_name not in self.tool_performance:
            self.tool_performance[tool_name] = {
                "avg_execution_time": 0.0,
                "success_rate": 0.0,
                "total_executions": 0,
                "successful_executions": 0,
            }

        metrics = self.tool_performance[tool_name]
        metrics["total_executions"] += 1

        if success:
            metrics["successful_executions"] += 1

        # Update averages
        metrics["success_rate"] = (
            metrics["successful_executions"] / metrics["total_executions"]
        )

        # Update average execution time (exponential moving average)
        alpha = 0.1
        if metrics["avg_execution_time"] == 0:
            metrics["avg_execution_time"] = execution_time
        else:
            metrics["avg_execution_time"] = (
                alpha * execution_time + (1 - alpha) * metrics["avg_execution_time"]
            )

    # Summary and utility methods

    def get_enhanced_summary(self) -> Dict[str, Any]:
        """Get comprehensive summary of enhanced tool state."""
        base_summary = {
            "total_tools": len(self.tools),
            "tools_by_route": {
                route: len(self.get_tools_by_route(route))
                for route in set(self.tool_routes.values())
            },
            "tools_by_category": {
                cat: len(tools) for cat, tools in self.tool_categories.items()
            },
            "tools_with_dependencies": len(self.tool_dependencies),
            "tools_with_performance_data": len(self.tool_performance),
        }

        # Add validation summary
        base_summary["validation_summary"] = {
            "total_validations": self.validation_state.total_tools,
            "valid_count": len(self.validation_state.valid_tool_calls),
            "invalid_count": len(self.validation_state.invalid_tool_calls),
            "error_count": len(self.validation_state.error_tool_calls),
            "next_action": self.validation_state.next_action.value,
            "target_nodes": list(self.validation_state.target_nodes),
        }

        # Add branch conditions
        base_summary["branch_conditions"] = self.branch_conditions.copy()

        return base_summary
