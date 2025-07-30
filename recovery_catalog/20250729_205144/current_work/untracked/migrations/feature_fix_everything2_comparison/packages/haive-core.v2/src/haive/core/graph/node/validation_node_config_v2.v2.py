"""Validation Node Configuration V2 - Improved version that can update state.

This version addresses the key issues with the original validation node:
1. Can add ToolMessages to state (not just route)
2. Handles dynamic tool routes properly
3. Uses Command with Send objects for proper routing
4. Supports both Pydantic models and regular tools

Key improvements:
- Proper node implementation (not conditional edge)
- ToolMessage creation for Pydantic model validation
- Error handling with appropriate ToolMessages
- Dynamic routing based on actual tool calls
"""

import logging
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.utils.pydantic import is_basemodel_subclass
from langgraph.prebuilt import ValidationNode
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.graph.common.types import StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class ValidationNodeConfigV2(BaseNodeConfig):
    """V2 Validation node that can update state and add ToolMessages.

    This node processes tool calls from AIMessages and:
    1. Validates Pydantic models and creates ToolMessages
    2. Routes regular tools to appropriate nodes
    3. Handles errors by creating error ToolMessages
    4. Updates state with new messages before routing

    Args:
        engine_name: Name of the engine to get tool routes from
        tool_node: Name of the tool execution node
        parser_node: Name of the parser node
        available_nodes: List of available nodes for routing
        pydantic_models: Dict of model name -> model class for validation
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
    node_type: NodeType = Field(default=NodeType.VALIDATION, description="Node type")

    def __call__(self, state: StateLike) -> Command:
        """Process tool calls and update state with ToolMessages using LangGraph
        ValidationNode pattern.
        """
        # Store current state for use in processing
        self._current_state = state

        # Get messages from state (StateLike supports both dict and BaseModel access)
        messages = (
            state.get("messages", [])
            if hasattr(state, "get")
            else getattr(state, "messages", [])
        )
        if not messages:
            return Command(goto="END")

        last_message = messages[-1]

        # Check if last message is AIMessage with tool calls
        if not isinstance(last_message, AIMessage):
            return Command(goto="END")

        tool_calls = getattr(last_message, "tool_calls", [])
        if not tool_calls:
            return Command(goto="END")

        # Get tool routes from state (handle both dict and BaseModel access)
        if hasattr(state, "get"):
            tool_routes = state.get("tool_routes", {})
        else:
            tool_routes = getattr(state, "tool_routes", {})

        # Use LangGraph ValidationNode like V1 does (correct approach)
        try:
            # Get tool schemas for validation like LangGraph ValidationNode
            schemas_by_name = {}
            for tool_call in tool_calls:
                tool_name = tool_call.get("name")
                if not tool_name:
                    continue

                # Get tool.args_schema like LangGraph ValidationNode does
                tool_schema = self._get_tool_args_schema(tool_name, state)
                if tool_schema:
                    schemas_by_name[tool_name] = tool_schema

            # Create LangGraph ValidationNode with collected schemas
            validation_node = ValidationNode(schemas=list(schemas_by_name.values()))

            # Run LangGraph validation using .invoke() like V1 does (this adds proper ToolMessages to state)
            validation_result = validation_node.invoke(state)

            # Process validation results and determine routing using Send objects like dynamic routing examples
            return self._process_validation_results(
                validation_result, tool_routes, tool_calls
            )

        except Exception as e:
            logger.exception(f"ValidationNodeV2 error: {e}")
            # Create error ToolMessages for all tool calls
            error_messages = []
            for tool_call in tool_calls:
                tool_id = tool_call.get("id")
                tool_name = tool_call.get("name")
                if tool_id and tool_name:
                    error_messages.append(
                        ToolMessage(
                            content=f"Validation error: {e}",
                            tool_call_id=tool_id,
                            name=tool_name,
                            additional_kwargs={"is_error": True},
                        )
                    )

            return Command(
                update={"messages": error_messages} if error_messages else {},
                goto="agent_node",  # Route errors back to agent
            )

    def _process_validation_results(
        self, validation_result: dict, tool_routes: dict, tool_calls: list
    ) -> Command:
        """Process LangGraph validation results and route using Send objects like dynamic
        routing examples.
        """
        logger.info("Processing LangGraph validation results with dynamic routing")

        # Get the ToolMessages from validation result and combine with original state messages
        validation_tool_messages = validation_result.get("messages", [])

        # The validation_result contains only new ToolMessages, we need to add them to the original state
        # Get original messages from the state that was passed to ValidationNode
        original_messages = []
        if hasattr(self, "_current_state"):
            if hasattr(self._current_state, "get"):
                original_messages = self._current_state.get("messages", [])
            else:
                original_messages = getattr(self._current_state, "messages", [])

        # Combine original messages with new ToolMessages
        messages = original_messages + validation_tool_messages
        logger.info(
            f"Combined {len(original_messages)} original messages with {len(validation_tool_messages)} validation results"
        )

        # Analyze the ToolMessages added by LangGraph ValidationNode
        destinations = set()
        has_errors = False
        validated_tool_calls = []  # Tool calls that passed validation for tool_node

        # Get the latest ToolMessages (added by ValidationNode)
        recent_tool_messages = []
        for msg in reversed(messages):
            if isinstance(msg, ToolMessage):
                recent_tool_messages.append(msg)
            elif isinstance(msg, AIMessage):
                break  # Stop at the AIMessage that triggered validation

        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_id = tool_call.get("id")

            if not tool_name or not tool_id:
                continue

            route = tool_routes.get(tool_name, "unknown")

            # Find corresponding ToolMessage from ValidationNode
            tool_message = None
            for msg in recent_tool_messages:
                if getattr(msg, "tool_call_id", None) == tool_id:
                    tool_message = msg
                    break

            if route == "pydantic_model":
                if tool_message and tool_message.additional_kwargs.get("is_error"):
                    logger.warning(f"Pydantic validation failed for {tool_name}")
                    destinations.add("agent_node")
                    has_errors = True
                else:
                    logger.info(f"Pydantic validation passed for {tool_name}")
                    destinations.add("parse_output")

            elif route in ["langchain_tool", "function", "tool_node"]:
                if tool_message and tool_message.additional_kwargs.get("is_error"):
                    logger.warning(f"Tool validation failed for {tool_name}")
                    destinations.add("agent_node")
                    has_errors = True
                else:
                    logger.info(
                        f"Tool validation passed for {tool_name}, routing to tool_node"
                    )
                    destinations.add("tool_node")
                    # Keep validated tool call for injection into AIMessage
                    validated_tool_calls.append(tool_call)

            else:
                logger.warning(f"Unknown tool {tool_name}, routing to agent")
                destinations.add("agent_node")
                has_errors = True

        # If routing to tool_node, inject validated tool calls into AIMessage
        updated_messages = messages
        if "tool_node" in destinations and validated_tool_calls:
            updated_messages = self._inject_validated_tool_calls(
                messages, validated_tool_calls
            )

        # Use Send objects for dynamic routing like the examples show
        return self._route_with_send_objects(
            {"messages": updated_messages}, destinations, has_errors
        )

    def _route_with_send_objects(
        self, validation_result: dict, destinations: set, has_errors: bool
    ) -> Command:
        """Route using Send objects for dynamic routing without compile-time literals."""
        destinations_list = list(destinations)

        logger.info(
            f"Dynamic routing - Destinations: {destinations_list}, Has errors: {has_errors}"
        )

        # Update state with validation results (which already includes injected AIMessage if needed)
        update_dict = validation_result

        if not destinations_list:
            logger.info("No destinations found, ending")
            return Command(update=update_dict, goto="END")

        # Use Send objects for dynamic routing like the examples
        if len(destinations_list) == 1:
            destination = destinations_list[0]
            logger.info(f"Single destination, using Send: {destination}")
            # Use Send object for dynamic routing without literals
            return Command(update=update_dict, goto=destination)

        # Multiple destinations - prioritize like validation_router_v2
        if "agent_node" in destinations_list:
            logger.info("Multiple destinations with errors, routing to agent_node")
            return Command(update=update_dict, goto="agent_node")
        if "tool_node" in destinations_list:
            logger.info("Multiple destinations, prioritizing tool_node")
            return Command(update=update_dict, goto="tool_node")
        if "parse_output" in destinations_list:
            logger.info("Multiple destinations, prioritizing parse_output")
            return Command(update=update_dict, goto="parse_output")
        # Fallback to first destination
        destination = destinations_list[0]
        logger.info(f"Multiple destinations, using first: {destination}")
        return Command(update=update_dict, goto=destination)

    def _get_tool_args_schema(
        self, tool_name: str, state: StateLike
    ) -> type[BaseModel] | None:
        """Get tool.args_schema like LangGraph ValidationNode does.

        This is the CORRECT approach - get the actual tool and use its args_schema.
        """
        engine = self._get_engine_from_state(state)
        if not engine:
            logger.warning(f"No engine found for tool schema lookup: {tool_name}")
            return None

        # Get tools from engine (same logic as ToolNodeConfigV2)
        tools = []
        for attr in ["tools", "schemas", "pydantic_tools"]:
            if hasattr(engine, attr):
                attr_value = getattr(engine, attr)
                if attr_value:
                    tools.extend(attr_value)

        # Find the specific tool by name
        for tool in tools:
            if hasattr(tool, "name") and tool.name == tool_name:
                # This is a BaseTool - get its args_schema
                if hasattr(tool, "args_schema") and tool.args_schema:
                    logger.info(
                        f"Found tool.args_schema for {tool_name}: {tool.args_schema}"
                    )
                    return tool.args_schema
                logger.warning(f"Tool {tool_name} has no args_schema")
                return None
            if hasattr(tool, "__name__") and tool.__name__ == tool_name:
                # This is a Pydantic model class directly
                if is_basemodel_subclass(tool):
                    logger.info(f"Found Pydantic model for {tool_name}: {tool}")
                    return tool
                logger.warning(f"Tool {tool_name} is not a BaseModel subclass")
                return None

        logger.warning(f"Tool not found in engine tools: {tool_name}")
        return None

    def _get_engine_from_state(self, state: StateLike) -> Any | None:
        """Get engine from state using engine_name."""
        if not self.engine_name:
            return None

        # Try state.engines first (handle both dict and BaseModel access)
        engines = (
            state.get("engines")
            if hasattr(state, "get")
            else getattr(state, "engines", None)
        )

        if engines and isinstance(engines, dict):
            engine = engines.get(self.engine_name)
            if engine:
                logger.info(f"Found engine in state.engines: {self.engine_name}")
                return engine

            # Try by engine.name attribute
            for _key, eng in engines.items():
                if hasattr(eng, "name") and eng.name == self.engine_name:
                    logger.info(f"Found engine by name attribute: {self.engine_name}")
                    return eng

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

    def _find_model_class_from_engine(
        self, tool_name: str, state: StateLike
    ) -> type[BaseModel] | None:
        """Find Pydantic model class from engine."""
        engine = self._get_engine_from_state(state)
        if not engine:
            return None

        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
            and getattr(engine.structured_output_model, "__name__", None) == tool_name
        ):
            logger.info(f"Found model in engine.structured_output_model: {tool_name}")
            return engine.structured_output_model

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            for schema in engine.schemas:
                if getattr(schema, "__name__", None) == tool_name:
                    logger.info(f"Found model in engine.schemas: {tool_name}")
                    return schema

        # Check pydantic_tools
        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            for tool in engine.pydantic_tools:
                if getattr(tool, "__name__", None) == tool_name:
                    logger.info(f"Found model in engine.pydantic_tools: {tool_name}")
                    return tool

        return None

    def _find_model_class(
        self, tool_name: str, state: StateLike | None = None
    ) -> type[BaseModel] | None:
        """Try to find Pydantic model class by name."""
        # FIRST: Try to find from engine (using attribution)
        if state:
            model_class = self._find_model_class_from_engine(tool_name, state)
            if model_class:
                return model_class

        # FALLBACK: Look in current module globals
        if tool_name in globals():
            candidate = globals()[tool_name]
            if isinstance(candidate, type) and issubclass(candidate, BaseModel):
                return candidate

        # FALLBACK: Try to import from common locations
        try:
            # Try importing from test modules
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

    def _inject_validated_tool_calls(
        self, messages: list, validated_tool_calls: list
    ) -> list:
        """Inject validated tool calls back into AIMessage for ToolNode execution.

        This is critical for langchain_tool routes - ToolNode expects AIMessage with tool_calls.
        """
        if not validated_tool_calls:
            return messages

        # Find the last AIMessage and create a new one with only validated tool calls
        updated_messages = messages.copy()

        # Find the AIMessage that contains these tool calls
        for i in reversed(range(len(updated_messages))):
            msg = updated_messages[i]
            if (
                isinstance(msg, AIMessage)
                and hasattr(msg, "tool_calls")
                and msg.tool_calls
            ):
                # Create new AIMessage with only the validated tool calls
                validated_ai_message = AIMessage(
                    content=msg.content,
                    tool_calls=validated_tool_calls,
                    id=msg.id,
                    name=msg.name,
                    additional_kwargs=msg.additional_kwargs,
                    response_metadata=msg.response_metadata,
                    invalid_tool_calls=msg.invalid_tool_calls,
                    usage_metadata=msg.usage_metadata,
                )

                # Replace the original AIMessage
                updated_messages[i] = validated_ai_message
                logger.info(
                    f"Injected {len(validated_tool_calls)} validated tool calls into AIMessage"
                )
                break

        return updated_messages
