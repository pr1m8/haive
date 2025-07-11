"""Validation Node V2 - Regular node that updates state with ToolMessages.

This is a proper node (not conditional edge) that can update state by adding
ToolMessages for Pydantic model validation and errors. It works with a separate
validation router function for routing decisions.

Flow:
1. V2 Validation Node: Processes tool calls, adds ToolMessages to state
2. V2 Validation Router: Reads updated state, makes routing decisions
"""

import json
import logging
from typing import Any, Dict, List, Optional

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.types import Command
from pydantic import BaseModel, Field, ValidationError

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class ValidationNodeV2(NodeConfig, ToolRouteMixin):
    """V2 Validation node that updates state with ToolMessages using schema-aware I/O.

    This node processes AIMessages with tool calls and:
    1. Validates Pydantic models and creates ToolMessages
    2. Handles errors by creating error ToolMessages
    3. Updates state.messages with new ToolMessages
    4. Returns Command to route to validation router

    Schema Features:
    - Uses enhanced MessageList for input/output
    - Supports engine attribution in tool messages
    - Selective field extraction from state
    """

    node_type: NodeType = Field(default=NodeType.VALIDATION, description="Node type")
    name: str = Field(default="validation_v2", description="Node name")
    messages_key: str = Field(default="messages", description="Messages field in state")

    def model_post_init(self, __context):
        """Setup default field definitions for validation node."""
        if not self.input_field_defs:
            from haive.core.schema.field_registry import StandardFields

            # Validation nodes need messages, tool_routes, and engine_name
            self.input_field_defs = [
                StandardFields.messages(use_enhanced=True),
                StandardFields.tool_routes(),
                StandardFields.engine_name(),
            ]

        if not self.output_field_defs:
            from haive.core.schema.field_registry import StandardFields

            # Validation nodes output updated messages
            self.output_field_defs = [
                StandardFields.messages(use_enhanced=True),
            ]

        # Call parent post_init to handle schema setup
        super().model_post_init(__context)

    # Router node to go to after updating state
    router_node: str = Field(
        default="validation_router", description="Router node for routing decisions"
    )

    def _get_engine_from_state(self, state: StateLike) -> Any | None:
        """Get engine from state - same logic as original validation."""
        logger.debug(f"Getting engine: {self.engine_name}")

        if not self.engine_name:
            return None

        # Try state.engines first
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            engine = state.engines.get(self.engine_name)
            if engine:
                logger.info(f"Found engine in state.engines: {self.engine_name}")
                return engine

            # Try by engine.name attribute
            for _key, eng in state.engines.items():
                if hasattr(eng, "name") and eng.name == self.engine_name:
                    logger.info(f"Found engine by name attribute: {self.engine_name}")
                    return eng

        # Try state attribute
        if hasattr(state, self.engine_name):
            engine = getattr(state, self.engine_name)
            logger.info(f"Found engine as state attribute: {self.engine_name}")
            return engine

        # Try registry
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            engine = registry.find(self.engine_name)
            if engine:
                logger.info(f"Found engine in registry: {self.engine_name}")
                return engine
        except Exception as e:
            logger.warning(f"Registry lookup failed: {e}")

        logger.warning(f"Engine not found: {self.engine_name}")
        return None

    def _get_tool_routes_from_engine(self, engine: Any) -> dict[str, str]:
        """Get tool routes from engine."""
        if hasattr(engine, "tool_routes") and engine.tool_routes:
            return engine.tool_routes
        return {}

    def _find_pydantic_model_class(
        self, tool_name: str, engine: Any
    ) -> type[BaseModel] | None:
        """Find Pydantic model class by name in engine."""
        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
            and getattr(engine.structured_output_model, "__name__", None) == tool_name
        ):
            return engine.structured_output_model

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            for schema in engine.schemas:
                if getattr(schema, "__name__", None) == tool_name:
                    return schema

        # Check pydantic_tools
        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            for tool in engine.pydantic_tools:
                if getattr(tool, "__name__", None) == tool_name:
                    return tool

        return None

    def _create_tool_message_for_pydantic(
        self,
        tool_name: str,
        tool_id: str,
        args: dict[str, Any],
        model_class: type[BaseModel],
    ) -> ToolMessage:
        """Create ToolMessage for Pydantic model validation."""
        try:
            # Validate the model
            model_instance = model_class.model_validate(args)

            # Create success ToolMessage
            success_content = {
                "success": True,
                "model": tool_name,
                "data": model_instance.model_dump(),
                "validated": True,
            }

            return ToolMessage(
                content=json.dumps(success_content, indent=2),
                tool_call_id=tool_id,
                name=tool_name,
                additional_kwargs={
                    "is_error": False,
                    "validation_passed": True,
                    "model_type": "pydantic",
                    "validated_data": success_content["data"],
                },
            )

        except ValidationError as e:
            # Create validation error ToolMessage
            error_content = {
                "success": False,
                "model": tool_name,
                "error": "ValidationError",
                "details": str(e),
                "errors": e.errors() if hasattr(e, "errors") else [],
            }

            return ToolMessage(
                content=json.dumps(error_content, indent=2),
                tool_call_id=tool_id,
                name=tool_name,
                additional_kwargs={
                    "is_error": True,
                    "error_type": "validation_error",
                    "validation_passed": False,
                },
            )

        except Exception as e:
            # Create generic error ToolMessage
            error_content = {
                "success": False,
                "model": tool_name,
                "error": "Exception",
                "details": str(e),
            }

            return ToolMessage(
                content=json.dumps(error_content, indent=2),
                tool_call_id=tool_id,
                name=tool_name,
                additional_kwargs={
                    "is_error": True,
                    "error_type": "exception",
                    "validation_passed": False,
                },
            )

    def _create_error_tool_message(
        self, tool_name: str, tool_id: str, error_msg: str
    ) -> ToolMessage:
        """Create error ToolMessage for unknown tools or other errors."""
        error_content = {"success": False, "tool": tool_name, "error": error_msg}

        return ToolMessage(
            content=json.dumps(error_content, indent=2),
            tool_call_id=tool_id,
            name=tool_name,
            additional_kwargs={"is_error": True, "error_type": "tool_not_found"},
        )

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Process tool calls and update state with ToolMessages."""
        logger.info("=== ValidationNodeV2 Execution ===")

        # Get messages from state
        messages = getattr(state, self.messages_key, [])
        if not messages:
            logger.warning("No messages in state")
            return Command(goto=self.router_node)

        # Get last message
        last_message = messages[-1]
        if not isinstance(last_message, AIMessage):
            logger.warning("Last message is not AIMessage")
            return Command(goto=self.router_node)

        # Get tool calls
        tool_calls = getattr(last_message, "tool_calls", [])
        if not tool_calls:
            logger.warning("No tool calls in last message")
            return Command(goto=self.router_node)

        logger.info(f"Processing {len(tool_calls)} tool calls")

        # Get engine and tool routes
        engine = self._get_engine_from_state(state)
        if not engine:
            logger.error("No engine found")
            return Command(goto=self.router_node)

        tool_routes = self._get_tool_routes_from_engine(engine)

        # Process each tool call and create ToolMessages
        new_tool_messages = []

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_id = tool_call.get("id")
            args = tool_call.get("args", {})

            if not tool_name or not tool_id:
                continue

            logger.info(f"Processing tool call: {tool_name}")

            # Get route for this tool
            route = tool_routes.get(tool_name, "unknown")
            logger.debug(f"Tool route: {tool_name} -> {route}")

            if route == "pydantic_model":
                # Handle Pydantic model
                model_class = self._find_pydantic_model_class(tool_name, engine)
                if model_class:
                    tool_msg = self._create_tool_message_for_pydantic(
                        tool_name, tool_id, args, model_class
                    )
                    new_tool_messages.append(tool_msg)
                    logger.info(f"Created ToolMessage for Pydantic model: {tool_name}")
                else:
                    # Unknown Pydantic model
                    error_msg = f"Pydantic model '{tool_name}' not found in engine"
                    tool_msg = self._create_error_tool_message(
                        tool_name, tool_id, error_msg
                    )
                    new_tool_messages.append(tool_msg)
                    logger.warning(f"Unknown Pydantic model: {tool_name}")

            elif route in ["langchain_tool", "function", "tool_node"]:
                # Regular tools - don't create ToolMessages here, let tool_node handle it
                logger.debug(f"Regular tool {tool_name} will be handled by tool_node")

            else:
                # Unknown tool
                error_msg = f"Unknown tool: {tool_name}"
                tool_msg = self._create_error_tool_message(
                    tool_name, tool_id, error_msg
                )
                new_tool_messages.append(tool_msg)
                logger.warning(f"Unknown tool: {tool_name}")

        # Update state with new ToolMessages
        update_dict = {}
        if new_tool_messages:
            updated_messages = list(messages) + new_tool_messages
            update_dict[self.messages_key] = updated_messages
            logger.info(f"Added {len(new_tool_messages)} ToolMessages to state")

            # Log the ToolMessages for debugging
            for i, tm in enumerate(new_tool_messages):
                logger.debug(f"  [{i}] {tm.name}: {tm.content[:100]}...")

        # Return Command to go to router
        return Command(update=update_dict, goto=self.router_node)
