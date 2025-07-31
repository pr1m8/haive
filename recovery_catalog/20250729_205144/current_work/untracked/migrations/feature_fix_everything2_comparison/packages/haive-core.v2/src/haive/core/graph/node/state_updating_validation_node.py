"""Validation node that updates state AND provides dynamic routing."""

import logging
from collections.abc import Callable
from enum import Enum
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import END, Send
from pydantic import BaseModel, Field

from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationRoutingState,
    ValidationStateManager,
    ValidationStatus,
)

logger = logging.getLogger(__name__)


class ValidationMode(str, Enum):
    """Validation modes for different behaviors."""

    STRICT = "strict"  # All tools must be valid
    PARTIAL = "partial"  # Some tools can fail
    PERMISSIVE = "permissive"  # Continue even with errors


class StateUpdatingValidationNode(BaseModel):
    """Validation node that updates state with results and provides dynamic routing.

    This node combines state updates with routing logic:
    1. Validates tool calls from the state
    2. Updates state with validation results
    3. Provides a router function that uses the updated state
    """

    # Node configuration
    name: str = Field(default="state_validation", description="Node name")
    engine_name: str | None = Field(
        default=None, description="Name of engine to get tools/schemas from"
    )

    # Validation mode
    validation_mode: ValidationMode = Field(
        default=ValidationMode.PARTIAL, description="How strict validation should be"
    )

    # State update configuration
    update_messages: bool = Field(
        default=True, description="Whether to add validation error messages"
    )

    track_error_tools: bool = Field(
        default=True, description="Whether to track error tool calls in state"
    )

    add_validation_metadata: bool = Field(
        default=True, description="Whether to add validation metadata to tool calls"
    )

    # Default nodes for routing
    agent_node: str = Field(
        default="agent", description="Node for errors/clarification"
    )
    tool_node: str = Field(default="tool_node", description="Node for tool execution")
    parser_node: str = Field(
        default="parser_node", description="Node for structured output"
    )

    # Route mappings
    route_to_node_mapping: dict[str, str] = Field(
        default_factory=lambda: {
            "langchain_tool": "tool_node",
            "function": "tool_node",
            "pydantic_model": "parser_node",
            "retriever": "retriever_node",
            "unknown": "tool_node",
        },
        description="Default mapping from tool routes to nodes",
    )

    def create_node_function(self) -> Callable:
        """Create the state-updating validation node function.

        Returns:
            Callable that updates state with validation results
        """

        def validation_node(state: Any, config: dict[str, Any] | None = None) -> Any:
            """Update state with validation results."""
            logger.info(f"[{self.name}] Starting state-updating validation")

            # Get tool calls from state
            tool_calls = self._extract_tool_calls(state)
            if not tool_calls:
                logger.info(f"[{self.name}] No tool calls found")
                return self._handle_no_tool_calls(state)

            # Get available tools and routes
            available_tools, tool_routes = self._get_tools_and_routes(state)

            # Create validation routing state
            routing_state = ValidationStateManager.create_routing_state()

            # Validate each tool call
            for tool_call in tool_calls:
                result = self._validate_tool_call(
                    tool_call, available_tools, tool_routes
                )
                routing_state.add_validation_result(result)

            # Update state with validation results
            updated_state = self._apply_validation_to_state(
                state, routing_state, tool_calls
            )

            logger.info(
                f"[{self.name}] Validation complete: "
                f"{len(routing_state.valid_tool_calls)} valid, "
                f"{len(routing_state.invalid_tool_calls)} invalid, "
                f"{len(routing_state.error_tool_calls)} errors"
            )

            return updated_state

        return validation_node

    def create_router_function(self) -> Callable:
        """Create the dynamic router function that uses validation state.

        Returns:
            Router function that returns Send objects or node names
        """

        def validation_router(state: Any) -> list[Send] | str:
            """Route based on validation results in state."""
            logger.info(f"[{self.name}] Routing based on validation state")

            # Get validation state if available
            validation_state = self._get_validation_state(state)
            if not validation_state:
                logger.warning(f"[{self.name}] No validation state found")
                return END

            # Get routing decision from state
            routing_decision = validation_state.get_routing_decision()

            # Check validation mode
            if self.validation_mode == ValidationMode.STRICT:
                # All tools must be valid
                if (
                    routing_decision["error_count"] > 0
                    or routing_decision["invalid_count"] > 0
                ):
                    logger.info(
                        f"[{self.name}] Strict mode: routing to agent due to failures"
                    )
                    return self.agent_node

            elif self.validation_mode == ValidationMode.PERMISSIVE:
                # Continue unless all failed
                if routing_decision["valid_count"] == 0:
                    logger.info(
                        f"[{self.name}] Permissive mode: no valid tools, routing to agent"
                    )
                    return self.agent_node

            # Get valid tool calls
            valid_results = validation_state.get_valid_tool_calls()
            if not valid_results:
                return self.agent_node if routing_decision["total_count"] > 0 else END

            # Create Send objects for valid tools
            sends = self._create_send_branches(state, valid_results)

            if sends:
                logger.info(f"[{self.name}] Created {len(sends)} Send branches")
                return sends
            return self.agent_node

        return validation_router

    def _extract_tool_calls(self, state: Any) -> list[dict[str, Any]]:
        """Extract tool calls from state."""
        # Use state method if available
        if hasattr(state, "get_tool_calls"):
            return state.get_tool_calls()

        # Manual extraction
        messages = getattr(state, "messages", [])
        if not messages:
            return []

        last_msg = messages[-1]
        if isinstance(last_msg, AIMessage):
            if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                return last_msg.tool_calls
            if hasattr(last_msg, "additional_kwargs"):
                return last_msg.additional_kwargs.get("tool_calls", [])

        return []

    def _get_tools_and_routes(
        self, state: Any
    ) -> tuple[dict[str, Any], dict[str, str]]:
        """Get available tools and routes from state/engine."""
        available_tools = {}
        tool_routes = {}

        # Get from engine if specified
        if self.engine_name:
            engines = getattr(state, "engines", {})
            engine = engines.get(self.engine_name)

            if engine:
                # Get tools
                if hasattr(engine, "tools"):
                    for tool in engine.tools:
                        tool_name = getattr(tool, "name", str(tool))
                        available_tools[tool_name] = tool

                # Get routes
                if hasattr(engine, "tool_routes"):
                    tool_routes.update(engine.tool_routes)

        # Also check state
        if hasattr(state, "tools"):
            for tool in state.tools:
                tool_name = getattr(tool, "name", str(tool))
                available_tools[tool_name] = tool

        if hasattr(state, "tool_routes"):
            tool_routes.update(state.tool_routes)

        return available_tools, tool_routes

    def _validate_tool_call(
        self,
        tool_call: dict[str, Any],
        available_tools: dict[str, Any],
        tool_routes: dict[str, str],
    ) -> Any:
        """Validate a single tool call."""
        tool_name = tool_call.get("name", "unknown")
        tool_id = tool_call.get("id", f"call_{id(tool_call)}")
        tool_args = tool_call.get("args", {})

        # Check if tool exists
        if tool_name not in available_tools:
            return ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.ERROR,
                route_recommendation=RouteRecommendation.AGENT,
                errors=[f"Tool '{tool_name}' not found"],
                target_node=self.agent_node,
            )

        # Get tool and route
        tool = available_tools[tool_name]
        route = tool_routes.get(tool_name, "unknown")
        target_node = self.route_to_node_mapping.get(route, self.tool_node)

        # Validate arguments
        errors = self._validate_arguments(tool, tool_args)

        if errors:
            return ValidationStateManager.create_validation_result(
                tool_call_id=tool_id,
                tool_name=tool_name,
                status=ValidationStatus.INVALID,
                route_recommendation=RouteRecommendation.AGENT,
                errors=errors,
                target_node=self.agent_node,
            )

        # Valid tool
        return ValidationStateManager.create_validation_result(
            tool_call_id=tool_id,
            tool_name=tool_name,
            status=ValidationStatus.VALID,
            route_recommendation=RouteRecommendation.EXECUTE,
            target_node=target_node,
            metadata={"route": route},
        )

    def _validate_arguments(self, tool: Any, args: dict[str, Any]) -> list[str]:
        """Validate tool arguments."""
        errors = []

        if hasattr(tool, "args_schema") and tool.args_schema:
            try:
                tool.args_schema.model_validate(args)
            except Exception as e:
                errors.append(str(e))

        return errors

    def _apply_validation_to_state(
        self,
        state: Any,
        routing_state: ValidationRoutingState,
        original_tool_calls: list[dict[str, Any]],
    ) -> Any:
        """Apply validation results to state."""
        # Apply to state if it has the method
        if hasattr(state, "apply_validation_results"):
            state.apply_validation_results(routing_state)
        # Manual updates
        elif not hasattr(state, "validation_state"):
            state.validation_state = routing_state
        else:
            state.validation_state = routing_state

        # Track error tools if configured
        if self.track_error_tools and hasattr(state, "error_tool_calls"):
            if not hasattr(state, "error_tool_calls"):
                state.error_tool_calls = []

            for tool_id in routing_state.error_tool_calls:
                error_result = routing_state.tool_validations[tool_id]
                state.error_tool_calls.append(
                    {
                        "tool_name": error_result.tool_name,
                        "tool_id": tool_id,
                        "errors": error_result.errors,
                    }
                )

        # Add validation messages if configured
        if self.update_messages and routing_state.error_tool_calls:
            self._add_validation_messages(state, routing_state)

        # Add metadata to tool calls if configured
        if self.add_validation_metadata:
            self._add_tool_metadata(state, routing_state, original_tool_calls)

        return state

    def _add_validation_messages(
        self, state: Any, routing_state: ValidationRoutingState
    ):
        """Add validation error messages to state."""
        if not hasattr(state, "messages"):
            return

        # Create error message for failed validations
        error_summary = []
        for result in routing_state.get_error_tool_calls():
            error_summary.append(f"- {result.tool_name}: {', '.join(result.errors)}")

        for result in routing_state.get_invalid_tool_calls():
            error_summary.append(f"- {result.tool_name}: {', '.join(result.errors)}")

        if error_summary:
            error_content = "Tool validation errors:\n" + "\n".join(error_summary)

            # Add as a tool message
            error_msg = ToolMessage(
                content=error_content,
                name="validation_errof",
                additional_kwargs={"is_error": True},
            )
            state.messages.append(error_msg)

    def _add_tool_metadata(
        self,
        state: Any,
        routing_state: ValidationRoutingState,
        original_tool_calls: list[dict[str, Any]],
    ):
        """Add validation metadata to tool calls in state."""
        if not hasattr(state, "messages") or not state.messages:
            return

        last_msg = state.messages[-1]
        if not isinstance(last_msg, AIMessage) or not hasattr(last_msg, "tool_calls"):
            return

        # Update tool calls with validation metadata
        for _i, tool_call in enumerate(last_msg.tool_calls):
            tool_id = tool_call.get("id")
            if tool_id in routing_state.tool_validations:
                result = routing_state.tool_validations[tool_id]

                # Add metadata
                if "metadata" not in tool_call:
                    tool_call["metadata"] = {}

                tool_call["metadata"]["validation_status"] = result.status.value
                tool_call["metadata"]["target_node"] = result.target_node

                if result.errors:
                    tool_call["metadata"]["validation_errors"] = result.errors

    def _get_validation_state(self, state: Any) -> ValidationRoutingState | None:
        """Get validation state from state object."""
        if hasattr(state, "validation_state"):
            return state.validation_state
        return None

    def _create_send_branches(self, state: Any, valid_results: list[Any]) -> list[Send]:
        """Create Send branches for valid tool calls."""
        sends = []

        # Get original tool calls
        tool_calls = self._extract_tool_calls(state)
        tool_call_map = {tc["id"]: tc for tc in tool_calls}

        for result in valid_results:
            tool_call = tool_call_map.get(result.tool_call_id)
            if not tool_call:
                continue

            # Create enhanced tool call with validation info
            enhanced_call = tool_call.copy()
            enhanced_call["validation_metadata"] = {
                "status": result.status.value,
                "target_node": result.target_node,
                "route": result.metadata.get("route") if result.metadata else None,
            }

            # Create Send to target node
            sends.append(Send(result.target_node, enhanced_call))

        return sends

    def _handle_no_tool_calls(self, state: Any) -> Any:
        """Handle case when no tool calls are found."""
        # Could add a message or set a flag
        if hasattr(state, "validation_state"):
            state.validation_state = ValidationStateManager.create_routing_state()
        return state


def create_state_updating_validation_node(**kwargs) -> StateUpdatingValidationNode:
    """Factory function to create a state-updating validation node."""
    return StateUpdatingValidationNode(**kwargs)
