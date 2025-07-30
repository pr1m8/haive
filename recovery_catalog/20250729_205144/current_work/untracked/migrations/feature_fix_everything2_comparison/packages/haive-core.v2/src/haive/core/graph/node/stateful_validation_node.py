"""Stateful Validation Node - Tracks tool call validation results in state.

This node processes tool calls and stores validation results in state using computed fields.
It separates validation logic from routing logic, enabling intelligent routing decisions
based on validation history and patterns.

Key features:
- Stores validation results in state with computed fields
- Tracks valid vs invalid tool calls for routing decisions
- Supports dynamic routing based on validation patterns
- Maintains validation history for analysis
- Integrates with ToolState for seamless tool tracking
"""

import logging
from datetime import datetime
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, ValidationError

from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class ToolCallValidationResult(BaseModel):
    """Result of a tool call validation."""

    tool_name: str = Field(..., description="Name of the tool")
    tool_id: str = Field(..., description="Tool call ID")
    is_valid: bool = Field(..., description="Whether validation passed")
    validation_type: str = Field(..., description="Type of validation performed")
    error_message: str | None = Field(
        default=None, description="Error message if validation failed"
    )
    validated_args: dict[str, Any] | None = Field(
        default=None, description="Validated arguments"
    )
    timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat(),
        description="Validation timestamp",
    )


class StatefulValidationNode(BaseNodeConfig):
    """Stateful validation node that tracks tool call validation results in state.

    This node processes tool calls and updates state with validation results,
    enabling intelligent routing decisions based on validation patterns.

    The node:
    1. Validates tool calls (Pydantic models, function signatures, etc.)
    2. Creates ToolMessages for results
    3. Stores validation results in state
    4. Routes based on validation outcomes
    5. Maintains validation history for analysis

    Args:
        engine_name: Name of the engine to get tool routes from
        tool_node: Name of the tool execution node
        parser_node: Name of the parser node
        available_nodes: List of available nodes for routing
        pydantic_models: Dict of model name -> model class for validation
        validation_history_limit: Maximum number of validation results to keep
        route_on_validation_pattern: Whether to route based on validation patterns
    """

    engine_name: str = Field(..., description="Engine name for tool routes")
    tool_node: str = Field(default="tool_node", description="Tool execution node name")
    parser_node: str = Field(default="parse_output", description="Parser node name")
    available_nodes: list[str] = Field(
        default_factory=list, description="Available nodes"
    )
    pydantic_models: dict[str, type[BaseModel]] = Field(
        default_factory=dict, description="Pydantic models for validation"
    )
    validation_history_limit: int = Field(
        default=100, description="Maximum validation results to keep in history"
    )
    route_on_validation_pattern: bool = Field(
        default=True, description="Whether to route based on validation patterns"
    )
    node_type: NodeType = Field(default=NodeType.VALIDATION, description="Node type")

    def __call__(self, state: dict[str, Any]) -> Command:
        """Process tool calls and update state with validation results."""
        # Get messages from state
        messages = state.get("messages", [])
        if not messages:
            return Command(goto="END")

        last_message = messages[-1]

        # Check if last message is AIMessage with tool calls
        if not isinstance(last_message, AIMessage):
            return Command(goto="END")

        tool_calls = getattr(last_message, "tool_calls", [])
        if not tool_calls:
            return Command(goto="END")

        # Get tool routes from state
        tool_routes = state.get("tool_routes", {})

        # Process each tool call and collect results
        validation_results = []
        new_messages = []
        destinations = set()

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_id = tool_call.get("id")
            args = tool_call.get("args", {})

            if not tool_name or not tool_id:
                continue

            # Get route for this tool
            route = tool_routes.get(tool_name, "unknown")

            # Validate the tool call
            validation_result = self._validate_tool_call(
                tool_name, tool_id, args, route
            )
            validation_results.append(validation_result)

            # Create ToolMessage based on validation result
            if validation_result.is_valid:
                if validation_result.validation_type == "pydantic_model":
                    tool_msg = ToolMessage(
                        content=f"Successfully validated {tool_name}: {
                            validation_result.validated_args}",
                        tool_call_id=tool_id,
                        name=tool_name,
                    )
                    destinations.add(self.parser_node)
                else:
                    # For non-pydantic tools, we don't create a ToolMessage here
                    # They'll be handled by the tool node
                    destinations.add(self.tool_node)
                    continue
            else:
                # Create error ToolMessage
                tool_msg = ToolMessage(
                    content=validation_result.error_message
                    or f"Validation failed for {tool_name}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
                destinations.add("END")

            new_messages.append(tool_msg)

        # Update state with validation results and messages
        update_dict = {}

        # Add validation results to state
        if validation_results:
            update_dict["validation_results"] = validation_results

            # Update validation history
            existing_history = state.get("validation_history", [])
            new_history = existing_history + validation_results

            # Limit history size
            if len(new_history) > self.validation_history_limit:
                new_history = new_history[-self.validation_history_limit :]

            update_dict["validation_history"] = new_history

            # Update validation stats
            update_dict["validation_stats"] = self._calculate_validation_stats(
                new_history
            )

        # Add new messages if any
        if new_messages:
            update_dict["messages"] = new_messages

        # Determine routing destination
        goto = self._determine_destination(destinations, validation_results)

        logger.info(
            f"StatefulValidation: Processed {
                len(validation_results)} tool calls, "
            f"routing to {goto}"
        )

        return Command(update=update_dict, goto=goto)

    def _validate_tool_call(
        self, tool_name: str, tool_id: str, args: dict[str, Any], route: str
    ) -> ToolCallValidationResult:
        """Validate a single tool call and return result."""
        if route == "pydantic_model":
            return self._validate_pydantic_model(tool_name, tool_id, args)
        if route in ["langchain_tool", "function"]:
            return self._validate_function_call(tool_name, tool_id, args, route)
        # Unknown route
        return ToolCallValidationResult(
            tool_name=tool_name,
            tool_id=tool_id,
            is_valid=False,
            validation_type="unknown",
            error_message=f"Unknown tool route: {route}",
        )

    def _validate_pydantic_model(
        self, tool_name: str, tool_id: str, args: dict[str, Any]
    ) -> ToolCallValidationResult:
        """Validate a Pydantic model tool call."""
        try:
            # Get model class
            model_class = self.pydantic_models.get(tool_name)

            if not model_class:
                # Try to dynamically find model class
                model_class = self._find_model_class(tool_name)

            if not model_class:
                return ToolCallValidationResult(
                    tool_name=tool_name,
                    tool_id=tool_id,
                    is_valid=False,
                    validation_type="pydantic_model",
                    error_message=f"Unknown Pydantic model: {tool_name}",
                )

            # Validate the model
            model_instance = model_class(**args)

            return ToolCallValidationResult(
                tool_name=tool_name,
                tool_id=tool_id,
                is_valid=True,
                validation_type="pydantic_model",
                validated_args=model_instance.model_dump(),
            )

        except ValidationError as e:
            return ToolCallValidationResult(
                tool_name=tool_name,
                tool_id=tool_id,
                is_valid=False,
                validation_type="pydantic_model",
                error_message=f"Validation error: {e!s}",
            )
        except Exception as e:
            return ToolCallValidationResult(
                tool_name=tool_name,
                tool_id=tool_id,
                is_valid=False,
                validation_type="pydantic_model",
                error_message=f"Unexpected error: {e!s}",
            )

    def _validate_function_call(
        self, tool_name: str, tool_id: str, args: dict[str, Any], route: str
    ) -> ToolCallValidationResult:
        """Validate a function/tool call (basic validation)."""
        # For now, we assume function calls are valid if they have a known route
        # More sophisticated validation could be added here (signature
        # checking, etc.)

        return ToolCallValidationResult(
            tool_name=tool_name,
            tool_id=tool_id,
            is_valid=True,
            validation_type=route,
            validated_args=args,
        )

    def _find_model_class(self, tool_name: str) -> type[BaseModel] | None:
        """Try to find Pydantic model class by name."""
        # Try to import from common locations
        try:
            from haive.agents.planning.p_and_e.models import (
                Act,
                Plan,
                PlanStep,
                Response,
            )

            models = {
                "Plan": Plan,
                "PlanStep": PlanStep,
                "Act": Act,
                "Response": Response,
            }
            if tool_name in models:
                return models[tool_name]
        except ImportError:
            pass

        return None

    def _calculate_validation_stats(
        self, validation_history: list[ToolCallValidationResult]
    ) -> dict[str, Any]:
        """Calculate statistics from validation history."""
        if not validation_history:
            return {}

        total_validations = len(validation_history)
        valid_validations = sum(1 for r in validation_history if r.is_valid)
        invalid_validations = total_validations - valid_validations

        # Calculate stats by validation type
        type_stats = {}
        for result in validation_history:
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
        for result in validation_history:
            tool_name = result.tool_name
            if tool_name not in tool_stats:
                tool_stats[tool_name] = {"total": 0, "valid": 0, "invalid": 0}

            tool_stats[tool_name]["total"] += 1
            if result.is_valid:
                tool_stats[tool_name]["valid"] += 1
            else:
                tool_stats[tool_name]["invalid"] += 1

        return {
            "total_validations": total_validations,
            "valid_validations": valid_validations,
            "invalid_validations": invalid_validations,
            "success_rate": (
                valid_validations / total_validations if total_validations > 0 else 0
            ),
            "type_stats": type_stats,
            "tool_stats": tool_stats,
        }

    def _determine_destination(
        self, destinations: set[str], validation_results: list[ToolCallValidationResult]
    ) -> str:
        """Determine where to route based on destinations and validation patterns."""
        if not destinations:
            return "END"

        destinations_list = list(destinations)

        if len(destinations_list) == 1:
            return destinations_list[0]

        # Multiple destinations - use validation pattern routing if enabled
        if self.route_on_validation_pattern:
            return self._route_by_validation_pattern(
                destinations_list, validation_results
            )

        # Default prioritization
        if self.tool_node in destinations_list:
            return self.tool_node
        if self.parser_node in destinations_list:
            return self.parser_node
        return "END"

    def _route_by_validation_pattern(
        self,
        destinations: list[str],
        validation_results: list[ToolCallValidationResult],
    ) -> str:
        """Route based on validation patterns."""
        # Count successful validations by destination type
        pydantic_successes = sum(
            1
            for r in validation_results
            if r.is_valid and r.validation_type == "pydantic_model"
        )

        tool_successes = sum(
            1
            for r in validation_results
            if r.is_valid and r.validation_type in ["langchain_tool", "function"]
        )

        # Route based on success patterns
        if pydantic_successes > 0 and self.parser_node in destinations:
            return self.parser_node
        if tool_successes > 0 and self.tool_node in destinations:
            return self.tool_node
        # Fallback to first available destination
        return destinations[0]
