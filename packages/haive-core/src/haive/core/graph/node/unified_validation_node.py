"""Unified Validation Node V2 - Proper Pydantic implementation.

This replaces the artificial separation between ValidationNodeV2 and validation_router_v2
with a single node that validates and routes in one unified operation.

Fixed to follow proper Pydantic patterns without custom __init__ methods.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langgraph.types import Command, Send
from pydantic import BaseModel, Field, model_validator

from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.logging import get_logger

logger = get_logger(__name__)


class UnifiedValidationNodeConfig(BaseNodeConfig):
    """Unified validation node that combines tool validation and routing.

    This node:
    1. Analyzes tool calls from the last AIMessage
    2. Validates Pydantic models directly
    3. Routes to appropriate destinations via Command/Send
    4. Handles all error cases in one place

    Fixed to follow proper Pydantic patterns.
    """

    # Node type - using proper Field definition
    node_type: NodeType = Field(
        default=NodeType.CALLABLE, description="Node type for unified validation"
    )

    # Engine configuration - required field
    engine_name: str = Field(description="Name of the engine to get tool routes from")

    # Routing destinations with proper defaults
    tool_node: str = Field(
        default="tool_node", description="Node for langchain tool execution"
    )

    parse_output_node: str = Field(
        default="parse_output", description="Node for parsing structured output"
    )

    agent_node: str = Field(
        default="agent_node", description="Node to return to agent on errors"
    )

    # Validation settings with proper defaults
    create_tool_messages: bool = Field(
        default=True,
        description="Whether to create ToolMessages for validation results",
    )

    parallel_execution: bool = Field(
        default=True, description="Whether to use Send for parallel tool execution"
    )

    @model_validator(mode="after")
    def validate_config(self) -> "UnifiedValidationNodeConfig":
        """Validate node configuration."""
        # Ensure we have at least one destination node
        if not any([self.tool_node, self.parse_output_node, self.agent_node]):
            raise ValueError("At least one destination node must be specified")
        return self

    def __call__(
        self, state: dict[str, Any], config: dict[str, Any] | None = None
    ) -> Command:
        """Unified validation and routing function.

        This is the main entry point that processes tool calls and routes them.
        """
        logger.info(f"Unified validation processing for engine: {self.engine_name}")

        # Get messages and engine
        messages = state.get("messages", [])
        engines = state.get("engines", {})

        # Get engine from engines dict
        engine = None
        if isinstance(engines, dict) and self.engine_name in engines:
            engine = engines[self.engine_name]
        elif hasattr(state, "engines") and isinstance(state.engines, dict):
            # Handle case where state is an object with engines attribute
            engine = state.engines.get(self.engine_name)

        if not messages:
            logger.debug("No messages found, routing to agent")
            return Command(update={}, goto=self.agent_node)

        # Get last AI message with tool calls
        last_ai_message = None
        for msg in reversed(messages):
            if (
                isinstance(msg, AIMessage)
                and hasattr(msg, "tool_calls")
                and msg.tool_calls
            ):
                last_ai_message = msg
                break

        if not last_ai_message:
            logger.debug("No tool calls found, routing to agent")
            return Command(update={}, goto=self.agent_node)

        # Process each tool call and determine routing
        routing_decisions = []
        new_messages = []

        for tool_call in last_ai_message.tool_calls:
            decision = self._process_tool_call(tool_call, engine, state)
            routing_decisions.append(decision)

            if decision["tool_message"]:
                new_messages.append(decision["tool_message"])

        # Create update dict
        update_dict = {}
        if new_messages:
            update_dict["messages"] = new_messages

        # Determine routing strategy
        if self.parallel_execution and len(routing_decisions) > 1:
            # Check if we should use Send for parallel execution
            destinations = [
                d["destination"] for d in routing_decisions if d.get("destination")
            ]
            set(destinations)

            # Use Send objects if we have multiple decisions, even if same destination
            sends = self._create_send_objects(routing_decisions)
            if sends:
                return Command(update=update_dict, goto=sends)

        # Use single routing
        destination = self._determine_single_destination(routing_decisions)
        return Command(update=update_dict, goto=destination)

    def _process_tool_call(
        self, tool_call: dict[str, Any], engine: Any, state: dict[str, Any]
    ) -> dict[str, Any]:
        """Process a single tool call and determine routing.

        Returns a decision dict with routing information.
        """
        tool_name = tool_call.get("name", "")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id", "")

        logger.debug(f"Processing tool call: {tool_name}")

        # Get tool route
        route = self._get_tool_route(tool_name, engine)

        decision = {
            "tool_name": tool_name,
            "tool_call": tool_call,
            "route": route,
            "tool_message": None,
            "destination": None,
            "success": False,
            "error": None,
        }

        # Handle different routes
        if route == "pydantic_model":
            # Validate Pydantic model
            validation_result = self._validate_pydantic_model(
                tool_name, tool_args, tool_id, engine
            )
            decision.update(validation_result)

            # Route based on validation success
            if validation_result["success"]:
                decision["destination"] = self.parse_output_node
            else:
                decision["destination"] = self.agent_node

        elif route in ["langchain_tool", "function"]:
            # Route to tool execution
            decision["destination"] = self.tool_node
            decision["success"] = True

        else:
            # Unknown tool - route to agent with error
            decision["destination"] = self.agent_node
            decision["error"] = f"Unknown tool: {tool_name}"

            if self.create_tool_messages:
                decision["tool_message"] = ToolMessage(
                    content=f"Error: Unknown tool '{tool_name}'",
                    tool_call_id=tool_id,
                    name=tool_name,
                )

        return decision

    def _get_tool_route(self, tool_name: str, engine: Any) -> str:
        """Get the route for a tool."""
        if not engine:
            return "unknown"

        # Check tool routes
        tool_routes = getattr(engine, "tool_routes", {})
        if tool_name in tool_routes:
            return tool_routes[tool_name]

        # Check if it's a Pydantic model
        if self._find_pydantic_model(tool_name, engine):
            return "pydantic_model"

        # Check if it's a langchain tool
        if self._find_langchain_tool(tool_name, engine):
            return "langchain_tool"

        return "unknown"

    def _find_pydantic_model(self, tool_name: str, engine: Any) -> type | None:
        """Find a Pydantic model class for the tool."""
        if not engine:
            return None

        # Check structured output model
        structured_output = getattr(engine, "structured_output_model", None)
        if (
            structured_output
            and getattr(structured_output, "__name__", "") == tool_name
        ):
            return structured_output

        # Check schemas
        schemas = getattr(engine, "schemas", [])
        for schema in schemas:
            if hasattr(schema, "__name__") and schema.__name__ == tool_name:
                return schema

        return None

    def _find_langchain_tool(self, tool_name: str, engine: Any) -> bool:
        """Check if tool is a langchain tool."""
        if not engine:
            return False

        tools = getattr(engine, "tools", [])
        return any(hasattr(tool, "name") and tool.name == tool_name for tool in tools)

    def _validate_pydantic_model(
        self, tool_name: str, tool_args: dict[str, Any], tool_id: str, engine: Any
    ) -> dict[str, Any]:
        """Validate a Pydantic model and create ToolMessage."""
        result = {
            "success": False,
            "tool_message": None,
            "error": None,
            "validated_data": None,
        }

        # Find model class
        model_class = self._find_pydantic_model(tool_name, engine)
        if not model_class:
            result["error"] = f"Pydantic model not found: {tool_name}"
            if self.create_tool_messages:
                result["tool_message"] = ToolMessage(
                    content=f"Error: Pydantic model '{tool_name}' not found",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
            return result

        # Validate model
        try:
            validated_instance = model_class.model_validate(tool_args)
            result["success"] = True
            result["validated_data"] = validated_instance

            if self.create_tool_messages:
                result["tool_message"] = ToolMessage(
                    content=f"Validation successful for {tool_name}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )

        except Exception as e:
            result["error"] = str(e)
            if self.create_tool_messages:
                result["tool_message"] = ToolMessage(
                    content=f"Validation error for {tool_name}: {e!s}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )

        return result

    def _create_send_objects(
        self, routing_decisions: list[dict[str, Any]]
    ) -> list[Send]:
        """Create Send objects for parallel execution."""
        sends = []

        for decision in routing_decisions:
            if decision["destination"]:
                sends.append(
                    Send(
                        decision["destination"],
                        {
                            "tool_call": decision["tool_call"],
                            "tool_name": decision["tool_name"],
                            "route": decision["route"],
                            "success": decision["success"],
                            "error": decision["error"],
                        },
                    )
                )

        return sends

    def _determine_single_destination(
        self, routing_decisions: list[dict[str, Any]]
    ) -> str:
        """Determine single destination from routing decisions."""
        if not routing_decisions:
            return self.agent_node

        # If any have errors, route to agent
        if any(not decision["success"] for decision in routing_decisions):
            return self.agent_node

        # If all are same destination, use that
        destinations = [decision["destination"] for decision in routing_decisions]
        unique_destinations = set(destinations)

        if len(unique_destinations) == 1:
            return destinations[0]

        # Mixed destinations - route to agent for disambiguation
        return self.agent_node


# Convenience function for creating unified validation nodes
def create_unified_validation_node(
    name: str = "unified_validation", engine_name: str = "main_engine", **kwargs
) -> UnifiedValidationNodeConfig:
    """Create a unified validation node with sensible defaults."""
    return UnifiedValidationNodeConfig(name=name, engine_name=engine_name, **kwargs)
