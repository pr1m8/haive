"""Validation node that returns Send objects for routing based on validation results."""

import logging
from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import AIMessage
from langgraph.types import END, Send
from pydantic import BaseModel, Field

from haive.core.schema.prebuilt.tools.validation_state import (
    RouteRecommendation,
    ValidationStateManager,
    ValidationStatus,
)

logger = logging.getLogger(__name__)


class RoutingValidationNode(BaseModel):
    """Validation node that creates Send branches based on validation results.

    This node:
    1. Gets tool calls from the last AI message (via computed fields)
    2. Validates each tool call against available tools/schemas
    3. Creates Send objects to route valid tools to appropriate nodes
    4. Returns routing decisions based on validation results
    """

    # Node configuration
    name: str = Field(default="routing_validation", description="Node name")
    engine_name: Optional[str] = Field(
        default=None, description="Name of engine to get tools/schemas from"
    )

    # Route mappings from tool routes to node names
    route_to_node_mapping: Dict[str, str] = Field(
        default_factory=lambda: {
            "langchain_tool": "langchain_tools",
            "function": "langchain_tools",
            "pydantic_model": "structured_output",
            "retriever": "retriever",
            "unknown": "langchain_tools",
        },
        description="Mapping from tool routes to node names",
    )

    # Validation options
    allow_partial_success: bool = Field(
        default=True, description="Whether to continue with valid tools if some fail"
    )

    return_to_agent_on_all_failures: bool = Field(
        default=True, description="Whether to route to agent if all validations fail"
    )

    agent_node_name: str = Field(
        default="agent", description="Name of agent node for error handling"
    )

    def __call__(
        self, state: Any, config: Optional[Dict[str, Any]] = None
    ) -> Union[List[Send], str]:
        """Validate tool calls and return Send objects for routing.

        Args:
            state: State object with messages and tool information
            config: Optional configuration

        Returns:
            List[Send]: Send objects for routing tool calls to nodes
            str: Single node name for error cases or END
        """
        logger.info("Starting routing validation")

        # Get tool calls from state
        tool_calls = self._get_tool_calls_from_state(state)
        if not tool_calls:
            logger.info("No tool calls found")
            return END

        logger.info(f"Found {len(tool_calls)} tool calls to validate")

        # Get available tools and routes from state/engine
        available_tools, tool_routes = self._get_tools_and_routes(state)

        # Create validation state
        validation_state = ValidationStateManager.create_routing_state()

        # Validate each tool call
        for tool_call in tool_calls:
            tool_name = tool_call.get("name", "unknown")
            tool_args = tool_call.get("args", {})
            tool_id = tool_call.get("id", f"call_{id(tool_call)}")

            logger.debug(f"Validating tool: {tool_name}")

            # Check if tool exists
            if tool_name not in available_tools:
                result = ValidationStateManager.create_validation_result(
                    tool_call_id=tool_id,
                    tool_name=tool_name,
                    status=ValidationStatus.ERROR,
                    route_recommendation=RouteRecommendation.AGENT,
                    errors=[f"Tool '{tool_name}' not found in available tools"],
                )
                validation_state.add_validation_result(result)
                continue

            # Get tool and route
            tool = available_tools[tool_name]
            route = tool_routes.get(tool_name, "unknown")

            # Validate arguments
            validation_errors = self._validate_tool_arguments(tool, tool_args)

            if validation_errors:
                result = ValidationStateManager.create_validation_result(
                    tool_call_id=tool_id,
                    tool_name=tool_name,
                    status=ValidationStatus.INVALID,
                    route_recommendation=RouteRecommendation.AGENT,
                    errors=validation_errors,
                    target_node=self.agent_node_name,
                )
            else:
                # Determine target node from route
                target_node = self._get_node_for_route(route)

                result = ValidationStateManager.create_validation_result(
                    tool_call_id=tool_id,
                    tool_name=tool_name,
                    status=ValidationStatus.VALID,
                    route_recommendation=RouteRecommendation.EXECUTE,
                    target_node=target_node,
                )

            validation_state.add_validation_result(result)

        # Apply validation results to state if it supports it
        if hasattr(state, "apply_validation_results"):
            state.apply_validation_results(validation_state)

        # Create routing decision based on validation results
        return self._create_routing_decision(validation_state, tool_calls)

    def _get_tool_calls_from_state(self, state: Any) -> List[Dict[str, Any]]:
        """Extract tool calls from state's last AI message."""
        # Use state's method if available
        if hasattr(state, "get_tool_calls"):
            return state.get_tool_calls()

        # Otherwise extract manually
        messages = getattr(state, "messages", [])
        if not messages:
            return []

        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            return []

        # Get tool calls from message
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            return last_message.tool_calls
        elif hasattr(last_message, "additional_kwargs"):
            return last_message.additional_kwargs.get("tool_calls", [])

        return []

    def _get_tools_and_routes(
        self, state: Any
    ) -> tuple[Dict[str, Any], Dict[str, str]]:
        """Get available tools and their routes from state/engine."""
        available_tools = {}
        tool_routes = {}

        # Get from engine if specified
        if self.engine_name:
            engines = getattr(state, "engines", {})
            engine = engines.get(self.engine_name)

            if engine:
                # Get tools from engine
                if hasattr(engine, "tools"):
                    for tool in engine.tools:
                        tool_name = getattr(tool, "name", str(tool))
                        available_tools[tool_name] = tool

                # Get routes from engine
                if hasattr(engine, "tool_routes"):
                    tool_routes.update(engine.tool_routes)

        # Also check state for tools and routes
        if hasattr(state, "tools"):
            for tool in state.tools:
                tool_name = getattr(tool, "name", str(tool))
                available_tools[tool_name] = tool

        if hasattr(state, "tool_routes"):
            tool_routes.update(state.tool_routes)

        return available_tools, tool_routes

    def _validate_tool_arguments(self, tool: Any, args: Dict[str, Any]) -> List[str]:
        """Validate tool arguments and return list of errors."""
        errors = []

        # Check if tool has args_schema for validation
        if hasattr(tool, "args_schema") and tool.args_schema:
            try:
                # Validate with Pydantic schema
                tool.args_schema.model_validate(args)
            except Exception as e:
                errors.append(f"Argument validation failed: {str(e)}")

        return errors

    def _get_node_for_route(self, route: str) -> str:
        """Get target node name for a tool route."""
        return self.route_to_node_mapping.get(route, "langchain_tools")

    def _create_routing_decision(
        self, validation_state: Any, original_tool_calls: List[Dict[str, Any]]
    ) -> Union[List[Send], str]:
        """Create routing decision based on validation results."""
        # Get valid tool calls
        valid_results = validation_state.get_valid_tool_calls()

        if not valid_results and self.return_to_agent_on_all_failures:
            logger.warning("All tool validations failed, returning to agent")
            return self.agent_node_name

        if not valid_results:
            logger.warning("No valid tools, ending")
            return END

        # Create Send objects for valid tools
        sends = []
        tool_call_map = {tc["id"]: tc for tc in original_tool_calls}

        for result in valid_results:
            tool_call = tool_call_map.get(result.tool_call_id)
            if not tool_call:
                continue

            # Create enhanced tool call with validation metadata
            enhanced_call = tool_call.copy()
            enhanced_call["validation_status"] = result.status.value
            enhanced_call["target_node"] = result.target_node

            # Create Send object to route to target node
            sends.append(Send(result.target_node, enhanced_call))

            logger.info(f"Routing {result.tool_name} to {result.target_node}")

        # Return Send objects or agent if none
        if sends:
            return sends
        elif self.return_to_agent_on_all_failures:
            return self.agent_node_name
        else:
            return END


def create_routing_validation_node(**kwargs) -> RoutingValidationNode:
    """Factory function to create a routing validation node."""
    return RoutingValidationNode(**kwargs)
