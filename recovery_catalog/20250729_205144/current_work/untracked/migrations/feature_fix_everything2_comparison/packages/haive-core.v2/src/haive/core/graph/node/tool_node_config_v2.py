"""Tool_Node_Config_V2 graph module.

This module provides tool node config v2 functionality for the Haive framework.

Classes:
    ToolNodeConfig: ToolNodeConfig implementation.
    LangChainToolNode: LangChainToolNode implementation.
    FunctionToolNode: FunctionToolNode implementation.

Functions:
    validate_tool_source: Validate Tool Source functionality.
    get_default_input_fields: Get Default Input Fields functionality.
    get_default_output_fields: Get Default Output Fields functionality.
"""

# ============================================================================
# TOOL NODE CONFIG V2 - WITH SCHEMA SUPPORT
# ============================================================================

import logging
from collections.abc import Callable
from typing import Any, Optional, Self, TypeVar

from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import ToolNode
from langgraph.types import Command
from pydantic import BaseModel, Field, model_validator
from rich.console import Console

from haive.core.graph.common.types import ConfigLike, NodeType, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.schema.field_definition import FieldDefinition
from haive.core.schema.field_registry import StandardFields

logger = logging.getLogger(__name__)
console = Console()

# Type variables for input/output schemas
TInput = TypeVar("TInput", bound=BaseModel)
TOutput = TypeVar("TOutput", bound=BaseModel)


class ToolNodeConfig(BaseNodeConfig[TInput, TOutput]):
    """Configuration for a schema-aware tool node in a graph.

    Tool nodes execute LangChain tools and handle tool calls from LLM messages.
    This version supports typed input/output schemas for better state management.

    Input Schema Requirements:
    - Must have a 'messages' field (List[BaseMessage]) or custom messages field
    - Should have 'tool_routes' field (Dict[str, str]) if using routing
    - May have 'engines' field (Dict[str, Any]) if getting tools from engines

    Output Schema:
    - Will contain updated messages with ToolMessages added
    - Optional error fields for tool execution failures
    """

    node_type: NodeType = Field(default=NodeType.TOOL, description="The type of node")

    # Field names
    messages_field: str = Field(
        default="messages",
        description="Name of the messages field in input/output schema",
    )

    tool_routes_field: str = Field(
        default="tool_routes",
        description="Name of the tool routes field in input schema",
    )

    engines_field: str = Field(
        default="engines", description="Name of the engines field in input schema"
    )

    error_field: str = Field(
        default="tool_error", description="Name of the error field in output schema"
    )

    # Tool configuration
    tags: list[str] | None = Field(
        default=None, description="Optional tags for the tool node"
    )

    handle_tool_errors: (
        bool | str | Callable[..., str] | tuple[type[Exception], ...]
    ) = Field(default=True, description="How to handle tool errors")

    # Engine reference for getting tools
    engine_name: str | None = Field(
        default=None, description="Name of engine to get tools from"
    )

    # Direct tools (if not using engine)
    tools: list[BaseTool] | None = Field(
        default=None, description="Direct list of tools to use", exclude=True
    )

    # Tool filtering - which routes should this node handle
    allowed_routes: list[str] = Field(
        default_factory=lambda: ["langchain_tool", "function", "tool_node"],
        description="Tool routes this node should handle",
    )

    # Options
    require_tool_calls: bool = Field(
        default=True, description="Whether to require tool calls in the last message"
    )

    create_error_messages: bool = Field(
        default=True, description="Whether to create ToolMessages for errors"
    )

    @model_validator(mode="after")
    def validate_tool_source(self) -> Self:
        """Validate that we have a source for tools."""
        if not self.tools and not self.engine_name:
            raise ValueError("Either 'tools' or 'engine_name' must be provided")
        return self

    def get_default_input_fields(self) -> list[FieldDefinition]:
        """Get default input field definitions."""
        fields = [
            StandardFields.messages(use_enhanced=True),
            StandardFields.tool_routes(),
        ]

        if self.engine_name:
            # Add engines field if we need to get tools from engine
            fields.append(
                FieldDefinition(
                    name=self.engines_field,
                    field_type=dict[str, Any],
                    default_factory=dict,
                    description="Dictionary of available engines",
                )
            )

        return fields

    def get_default_output_fields(self) -> list[FieldDefinition]:
        """Get default output field definitions."""
        return [
            StandardFields.messages(use_enhanced=True),
            FieldDefinition(
                name=self.error_field,
                field_type=Optional[str],
                default=None,
                description="Tool execution error message if any",
            ),
        ]

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute the tool node with the given state and configuration.

        Args:
            state: The current state of the graph
            config: Optional runtime configuration

        Returns:
            A Command with state update including tool execution results
        """
        logger.info("=" * 60)
        logger.info(f"TOOL NODE V2 EXECUTION: {self.name}")
        logger.info("=" * 60)

        # Get messages from state
        messages = self._get_messages_from_state(state)

        if not messages:
            logger.warning("No messages in state")
            return self._create_no_op_response()

        # Check for tool calls
        last_message = messages[-1]
        if not self._has_tool_calls(last_message):
            if self.require_tool_calls:
                logger.warning("No tool calls in last message")
                return self._create_no_op_response()
            logger.info("No tool calls but not required, passing through")
            return self._create_no_op_response()

        logger.info(f"Found {len(last_message.tool_calls)} tool calls to process")

        # Get tools
        tools = self._get_tools(state)
        if not tools:
            logger.error("No tools available")
            return self._create_error_response(
                messages, "No tools available for execution"
            )

        # Get tool routes if available
        tool_routes = self._get_tool_routes(state)

        # Filter tools by allowed routes
        filtered_tools = self._filter_tools_by_route(tools, tool_routes)

        if not filtered_tools:
            logger.warning("No tools available after filtering")
            return self._create_error_response(
                messages,
                f"No tools match allowed routes: {
                    self.allowed_routes}",
            )

        logger.info(f"Using {len(filtered_tools)} tools after filtering")

        # Execute tools
        try:
            result = self._execute_tools(state, filtered_tools, messages, config)
            return result

        except Exception as e:
            logger.exception(f"Error executing tools: {e}")
            return self._create_error_response(messages, str(e))

    def _get_messages_from_state(self, state: StateLike) -> list[BaseMessage]:
        """Extract messages from state."""
        if hasattr(state, self.messages_field):
            messages = getattr(state, self.messages_field)
        elif hasattr(state, "get"):
            messages = state.get(self.messages_field, [])
        else:
            messages = []

        # Ensure it's a list
        if not isinstance(messages, list):
            messages = []

        return messages

    def _has_tool_calls(self, message: Any) -> bool:
        """Check if a message has tool calls."""
        if not isinstance(message, AIMessage):
            return False
        return bool(getattr(message, "tool_calls", None))

    def _get_tools(self, state: StateLike) -> list[BaseTool]:
        """Get tools from direct list or engine."""
        if self.tools:
            return self.tools

        # Get from engine
        if not self.engine_name:
            return []

        engine = self._get_engine_from_state(state)
        if not engine:
            return []

        # Collect tools from various engine attributes
        tools = []

        for attr in ["tools", "schemas", "pydantic_tools"]:
            if hasattr(engine, attr):
                attr_value = getattr(engine, attr)
                if attr_value:
                    tools.extend(attr_value)
                    logger.debug(
                        f"Found {
                            len(attr_value)} tools in engine.{attr}"
                    )

        return tools

    def _get_engine_from_state(self, state: StateLike) -> Any | None:
        """Get engine from state."""
        if hasattr(state, self.engines_field):
            engines = getattr(state, self.engines_field, {})
        elif hasattr(state, "get"):
            engines = state.get(self.engines_field, {})
        else:
            engines = {}

        if not isinstance(engines, dict):
            logger.error(f"Engines field is not a dict: {type(engines)}")
            return None

        return engines.get(self.engine_name)

    def _get_tool_routes(self, state: StateLike) -> dict[str, str]:
        """Get tool routes from state or engine."""
        # First try state
        if hasattr(state, self.tool_routes_field):
            routes = getattr(state, self.tool_routes_field, {})
            if routes:
                return routes

        # Then try engine
        engine = self._get_engine_from_state(state) if self.engine_name else None
        if engine and hasattr(engine, "tool_routes"):
            return engine.tool_routes or {}

        return {}

    def _filter_tools_by_route(
        self, tools: list[BaseTool], tool_routes: dict[str, str]
    ) -> list[BaseTool]:
        """Filter tools by allowed routes."""
        filtered = []

        for tool in tools:
            tool_name = getattr(tool, "name", getattr(tool, "__name__", str(tool)))
            route = tool_routes.get(tool_name, "langchain_tool")  # Default route

            if route in self.allowed_routes:
                filtered.append(tool)
                logger.debug(f"Including tool '{tool_name}' (route: {route})")
            else:
                logger.debug(
                    f"Excluding tool '{tool_name}' "
                    f"(route: {route} not in {self.allowed_routes})"
                )

        return filtered

    def _execute_tools(
        self,
        state: StateLike,
        tools: list[BaseTool],
        messages: list[BaseMessage],
        config: ConfigLike | None,
    ) -> Command:
        """Execute tools and return updated state."""
        # Create the tool node
        tool_node = ToolNode(
            tools=tools,
            name=self.name,
            tags=self.tags,
            handle_tool_errors=self.handle_tool_errors,
            messages_key=self.messages_field,
        )

        # Convert state to dict if needed
        state_dict = state if isinstance(state, dict) else state.dict()

        # Execute
        result = tool_node.invoke(state_dict, config)

        # Extract updated messages
        if isinstance(result, dict) and self.messages_field in result:
            updated_messages = result[self.messages_field]

            # Count ToolMessages added
            tool_msg_count = sum(
                1
                for msg in updated_messages[len(messages) :]
                if isinstance(msg, ToolMessage)
            )

            logger.info(f"Added {tool_msg_count} ToolMessages")

            # Return update
            return Command(
                update={self.messages_field: updated_messages, self.error_field: None},
                goto=self._get_goto_node(),
            )
        logger.error(f"Unexpected result from ToolNode: {type(result)}")
        return self._create_error_response(
            messages, "Unexpected result format from tool execution"
        )

    def _create_no_op_response(self) -> Command:
        """Create a no-operation response."""
        return Command(update={self.error_field: None}, goto=self._get_goto_node())

    def _create_error_response(
        self, messages: list[BaseMessage], error_msg: str
    ) -> Command:
        """Create an error response."""
        update = {self.error_field: error_msg}

        if self.create_error_messages and messages:
            # Add error ToolMessages for any pending tool calls
            last_message = messages[-1]
            if self._has_tool_calls(last_message):
                new_messages = list(messages)

                for tool_call in last_message.tool_calls:
                    tool_name = (
                        tool_call["name"]
                        if isinstance(tool_call, dict)
                        else tool_call.name
                    )
                    tool_id = (
                        tool_call.get("id", f"call_{tool_name}")
                        if isinstance(tool_call, dict)
                        else tool_call.id
                    )

                    tool_msg = ToolMessage(
                        content=f"Tool execution error: {error_msg}",
                        name=tool_name,
                        tool_call_id=tool_id,
                    )
                    new_messages.append(tool_msg)

                update[self.messages_field] = new_messages

        return Command(update=update, goto=self._get_goto_node())

    def _get_goto_node(self) -> str:
        """Get the node to go to after tool execution."""
        return self.command_goto or "agent"


# ============================================================================
# SPECIALIZED TOOL NODE CONFIGURATIONS
# ============================================================================


class LangChainToolNode(ToolNodeConfig):
    """Tool node specifically for LangChain tools."""

    def __init__(self, **kwargs) -> None:
        if "allowed_routes" not in kwargs:
            kwargs["allowed_routes"] = ["langchain_tool", "tool_node"]
        super().__init__(**kwargs)


class FunctionToolNode(ToolNodeConfig):
    """Tool node specifically for function tools."""

    def __init__(self, **kwargs) -> None:
        if "allowed_routes" not in kwargs:
            kwargs["allowed_routes"] = ["function"]
        super().__init__(**kwargs)


class PydanticToolNode(ToolNodeConfig):
    """Tool node specifically for Pydantic model tools."""

    def __init__(self, **kwargs) -> None:
        if "allowed_routes" not in kwargs:
            kwargs["allowed_routes"] = ["pydantic_model", "parse_output"]
        super().__init__(**kwargs)


# ============================================================================
# CONVENIENCE FACTORY FUNCTIONS
# ============================================================================


def create_tool_node(
    name: str = "tool_node",
    engine_name: str | None = None,
    tools: list[BaseTool] | None = None,
    allowed_routes: list[str] | None = None,
    **kwargs,
) -> ToolNodeConfig:
    """Create a generic tool node."""
    config_kwargs = {"name": name, "engine_name": engine_name, "tools": tools, **kwargs}

    if allowed_routes:
        config_kwargs["allowed_routes"] = allowed_routes

    return ToolNodeConfig(**config_kwargs)


def create_langchain_tool_node(
    name: str = "langchain_tools",
    engine_name: str | None = None,
    tools: list[BaseTool] | None = None,
    **kwargs,
) -> LangChainToolNode:
    """Create a tool node for LangChain tools."""
    return LangChainToolNode(name=name, engine_name=engine_name, tools=tools, **kwargs)


def create_function_tool_node(
    name: str = "function_tools",
    engine_name: str | None = None,
    tools: list[BaseTool] | None = None,
    **kwargs,
) -> FunctionToolNode:
    """Create a tool node for function tools."""
    return FunctionToolNode(name=name, engine_name=engine_name, tools=tools, **kwargs)


def create_pydantic_tool_node(
    name: str = "pydantic_tools",
    engine_name: str | None = None,
    tools: list[BaseTool] | None = None,
    **kwargs,
) -> PydanticToolNode:
    """Create a tool node for Pydantic model tools."""
    return PydanticToolNode(name=name, engine_name=engine_name, tools=tools, **kwargs)


def create_tool_node_from_route_filter(
    allowed_routes: list[str], engine_name: str, name: str | None = None, **kwargs
) -> ToolNodeConfig:
    """Create a tool node configuration for specific routes.

    Args:
        allowed_routes: List of tool routes this node should handle
        engine_name: Name of engine in state.engines dict
        name: Optional node name
        **kwargs: Additional configuration parameters

    Returns:
        Configured ToolNodeConfig
    """
    if not name:
        name = f"tool_node_{'+'.join(allowed_routes)}"

    return ToolNodeConfig(
        name=name, allowed_routes=allowed_routes, engine_name=engine_name, **kwargs
    )
