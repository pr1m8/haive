"""Validation_Node_Config graph module.

This module provides validation node config functionality for the Haive framework.

Classes:
    ValidationNodeConfig: ValidationNodeConfig implementation.
    if: if implementation.
    from: from implementation.

Functions:
    has_tool_error: Has Tool Error functionality.
    get_tool_name: Get Tool Name functionality.
    get_tool_args: Get Tool Args functionality.
"""

# src/haive/core/graph/node/validation_node_config.py

import json
import logging
from collections.abc import Callable
from typing import Any

from langchain_core.messages import AIMessage, ToolMessage
from langgraph.graph import END
from langgraph.prebuilt import ValidationNode
from pydantic import Field

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.node.types import NodeType

# Configure logger with rich handler
logger = logging.getLogger(__name__)

# Add rich handler if not already present
if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
    from rich.logging import RichHandler

    handler = RichHandler(
        rich_tracebacks=True,
        show_time=True,
        show_path=True,
        enable_link_path=True,
        markup=True,
        log_time_format="[%Y-%m-%d %H:%M:%S]",
    )
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def has_tool_error(message: ToolMessage) -> bool:
    """Check if a ToolMessage contains an error."""
    if not isinstance(message, ToolMessage):
        return False

    content = message.content

    # Check string content for error terms
    if isinstance(content, str):
        error_terms = ["error", "invalid", "failed", "exception", "validation error"]
        contains_error = any(term in content.lower() for term in error_terms)
        if contains_error:
            logger.debug(
                f"[bold yellow]Tool error detected in content:[/bold yellow] {content[:100]}..."
            )
        return contains_error

    # Check dict content for error keys
    if isinstance(content, dict):
        error_keys = ["error", "errors", "exception", "validation_error"]
        has_error_key = any(key in content for key in error_keys)
        if has_error_key:
            logger.debug(
                f"[bold yellow]Tool error detected in dict:[/bold yellow] {
                    list(
                        content.keys())}"
            )
        return has_error_key

    # Check additional kwargs
    if hasattr(message, "additional_kwargs") and message.additional_kwargs:
        if message.additional_kwargs.get("is_error"):
            logger.debug(
                "[bold yellow]Tool error detected in additional_kwargs[/bold yellow]"
            )
            return True

    return False


def get_tool_name(tool_call: Any) -> str:
    """Extract tool name from either ToolCall object or dictionary."""
    if hasattr(tool_call, "name"):
        return tool_call.name

    if isinstance(tool_call, dict):
        if "name" in tool_call:
            return tool_call["name"]
        if "function" in tool_call and "name" in tool_call["function"]:
            return tool_call["function"]["name"]

    logger.warning(
        "[bold yellow]Could not extract tool name from tool_call[/bold yellow]"
    )
    return "unknown_tool"


def get_tool_args(tool_call: Any) -> dict[str, Any]:
    """Extract tool arguments from either ToolCall object or dictionary."""
    if hasattr(tool_call, "args"):
        return tool_call.args

    if isinstance(tool_call, dict):
        if "args" in tool_call:
            return tool_call["args"]
        if "arguments" in tool_call:
            args = tool_call["arguments"]
            if isinstance(args, str):
                try:
                    return json.loads(args)
                except BaseException:
                    return {"raw_args": args}
            return args
        if "function" in tool_call and "arguments" in tool_call["function"]:
            args = tool_call["function"]["arguments"]
            if isinstance(args, str):
                try:
                    return json.loads(args)
                except BaseException:
                    return {"raw_args": args}
            return args

    logger.warning(
        "[bold yellow]Could not extract tool args from tool_call[/bold yellow]"
    )
    return {}


def get_tool_id(tool_call: Any) -> str:
    """Extract tool ID from either ToolCall object or dictionary."""
    if hasattr(tool_call, "id"):
        return tool_call.id
    if isinstance(tool_call, dict) and "id" in tool_call:
        return tool_call["id"]

    # Generate a fallback ID
    fallback_id = f"tool_call_{id(tool_call)}"
    logger.debug(f"[bold cyan]Generated fallback tool ID:[/bold cyan] {fallback_id}")
    return fallback_id


class ValidationNodeConfig(NodeConfig, ToolRouteMixin):
    """Configuration for a validation node that routes tool calls to appropriate nodes."""

    node_type: NodeType = Field(
        default=NodeType.VALIDATION, description="The type of node"
    )
    name: str = Field(default="validation", description="The name of the node")
    messages_key: str = Field(
        default="messages", description="The key to use for the messages field"
    )

    # Engine name to get tools/schemas from
    engine_name: str | None = Field(
        default=None, description="Name of the engine to get tools/schemas from"
    )

    # Override tools/schemas if needed
    schemas: list[Any] = Field(
        default_factory=list, description="The schemas to use for validation (override)"
    )
    tools: list[Any] = Field(
        default_factory=list, description="List of available tools (override)"
    )

    format_error: Callable | None = Field(
        default=None, description="Custom formatter for validation errors"
    )

    # Node routing configuration
    agent_node: str = Field(
        default="agent_node", description="Node to return to for validation errors"
    )
    tool_node: str = Field(
        default="tool_node", description="Node for executing standard tools"
    )
    parser_node: str = Field(
        default="parse_output", description="Node for parsing Pydantic models"
    )
    retriever_node: str = Field(
        default="retriever", description="Node for retriever tools"
    )

    # Available nodes in the graph (for validation)
    available_nodes: list[str] = Field(
        default_factory=list, description="List of nodes available in the graph"
    )

    # Custom route mappings
    custom_route_mappings: dict[str, str] = Field(
        default_factory=dict,
        description="Custom mappings from route names to node names",
    )

    # Direct node routes
    direct_node_routes: list[str] = Field(
        default_factory=list,
        description="Routes that map directly to node names without transformation",
    )

    def validate_node_exists(self, node_name: str) -> str:
        """Validate that a node exists in the graph."""
        logger.debug(f"[bold blue]Validating node exists:[/bold blue] {node_name}")

        if not self.available_nodes:
            logger.debug("  No available_nodes list, assuming node exists")
            return node_name

        if node_name in self.available_nodes:
            logger.debug("  [bold green]✓ Node exists[/bold green]")
            return node_name

        # Try fallbacks
        logger.warning(
            f"[bold yellow]Node '{node_name}' not found in available nodes[/bold yellow]"
        )
        fallback_options = [self.agent_node, "agent_node", "START"]

        for fallback in fallback_options:
            if fallback in self.available_nodes:
                logger.info(f"[bold cyan]Using fallback node:[/bold cyan] {fallback}")
                return fallback

        logger.error(
            f"[bold red]No valid fallback found, returning original:[/bold red] {node_name}"
        )
        return node_name

    def _get_node_for_route(self, route: str) -> str:
        """Map tool route to appropriate node."""
        logger.debug(f"[bold blue]Getting node for route:[/bold blue] {route}")

        # Check custom mappings first
        if route in self.custom_route_mappings:
            node = self.custom_route_mappings[route]
            logger.debug(f"  Found in custom mappings: {node}")
            return self.validate_node_exists(node)

        # Check if this is a direct node route
        if route in self.direct_node_routes:
            logger.debug(f"  Direct node route: {route}")
            return self.validate_node_exists(route)

        # Standard route mapping
        route_mapping = {
            "pydantic_model": self.parser_node,
            "langchain_tool": self.tool_node,
            "function": self.tool_node,
            "retriever": self.retriever_node,
            "unknown": self.tool_node,
        }

        target_node = route_mapping.get(route, self.tool_node)
        logger.debug(f"  Standard mapping: {route} -> {target_node}")
        return self.validate_node_exists(target_node)

    def _get_engine_from_state(self, state: StateLike) -> Any | None:
        """Get engine from state.engines or registry."""
        logger.debug(f"[bold blue]Getting engine:[/bold blue] {self.engine_name}")

        if not self.engine_name:
            logger.debug("  No engine name specified")
            return None

        # FIRST: Try to get from state.engines using engine name
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            logger.debug(f"  State has engines dict with {len(state.engines)} engines")
            logger.debug(
                f"  Available engine keys: {
                    list(
                        state.engines.keys())}"
            )

            # Try exact name match
            engine = state.engines.get(self.engine_name)
            if engine:
                logger.info(
                    f"[bold green]✓ Found engine in state.engines:[/bold green] {
                        self.engine_name}"
                )
                logger.debug(f"    Engine type: {type(engine).__name__}")
                logger.debug(
                    f"    Engine has tools: {
                        hasattr(
                            engine,
                            'tools')}"
                )
                logger.debug(
                    f"    Engine has tool_routes: {
                        hasattr(
                            engine,
                            'tool_routes')}"
                )
                return engine

            # Try to find by engine.name attribute
            for key, eng in state.engines.items():
                if hasattr(eng, "name") and eng.name == self.engine_name:
                    logger.info(
                        f"[bold green]✓ Found engine by name attribute:[/bold green] {
                            self.engine_name} (key: {key})"
                    )
                    return eng

        # SECOND: Try to get from state directly (if engines are stored as
        # attributes)
        if hasattr(state, self.engine_name):
            engine = getattr(state, self.engine_name)
            logger.info(
                f"[bold green]✓ Found engine as state attribute:[/bold green] {
                    self.engine_name}"
            )
            return engine

        # LAST: Fallback to registry
        logger.debug("  Engine not found in state, trying registry...")
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            engine = registry.find(self.engine_name)
            if engine:
                logger.info(
                    f"[bold green]✓ Found engine in EngineRegistry:[/bold green] {
                        self.engine_name}"
                )
                return engine
            logger.warning(
                f"[bold yellow]Engine not found in registry:[/bold yellow] {
                    self.engine_name}"
            )
        except Exception as e:
            logger.exception(
                f"[bold red]Error accessing EngineRegistry:[/bold red] {e}"
            )

        logger.error(
            f"[bold red]Engine '{
                self.engine_name}' not found anywhere[/bold red]"
        )
        return None

    def _get_tools_and_schemas_from_engine(
        self, engine: Any
    ) -> tuple[list[Any], list[Any]]:
        """Extract tools and schemas from an engine."""
        logger.debug("[bold blue]Extracting tools and schemas from engine[/bold blue]")

        tools = []
        schemas = []

        # Log what the engine has
        logger.debug(
            f"  Engine attributes: {[attr for attr in dir(engine) if not attr.startswith('_')][:20]}..."
        )

        # Get tools
        if hasattr(engine, "tools") and engine.tools:
            tools.extend(engine.tools)
            logger.debug(f"  Found {len(engine.tools)} tools")
            for tool in engine.tools[:3]:  # Log first 3
                tool_name = getattr(tool, "name", getattr(tool, "__name__", str(tool)))
                logger.debug(f"    - {tool_name}")

        # Get pydantic tools/schemas
        if hasattr(engine, "pydantic_tools") and engine.pydantic_tools:
            schemas.extend(engine.pydantic_tools)
            logger.debug(f"  Found {len(engine.pydantic_tools)} pydantic_tools")

        if hasattr(engine, "schemas") and engine.schemas:
            schemas.extend(engine.schemas)
            logger.debug(f"  Found {len(engine.schemas)} schemas")

        # Check for structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
        ):
            schemas.append(engine.structured_output_model)
            model_name = getattr(
                engine.structured_output_model,
                "__name__",
                str(engine.structured_output_model),
            )
            logger.debug(f"  Found structured_output_model: {model_name}")

        logger.info(
            f"[bold cyan]Total extracted:[/bold cyan] {
                len(tools)} tools, {
                len(schemas)} schemas"
        )
        return tools, schemas

    def _sync_tools_and_schemas(self, state: StateLike) -> tuple[list[Any], list[Any]]:
        """Sync tools and schemas from engine in state - ONLY from the specified engine."""
        logger.info("[bold magenta]Syncing tools and schemas from state[/bold magenta]")

        all_tools = []
        all_schemas = []

        # Get from engine if specified
        if self.engine_name:
            engine = self._get_engine_from_state(state)
            if engine:
                # IMPORTANT: Only use tools/schemas from THIS specific engine
                # Do not use tools from other engines in the state to prevent
                # contamination
                logger.info(
                    f"[bold yellow]Using ONLY tools/schemas from engine: {
                        self.engine_name}[/bold yellow]"
                )

                # Get tools and schemas ONLY from this specific engine
                engine_tools, engine_schemas = self._get_tools_and_schemas_from_engine(
                    engine
                )

                # Filter tools to only include those that actually belong to this engine
                # by checking the engine's original tool definitions
                original_engine_tools = []
                original_engine_schemas = []

                # Get the original tools from the engine - filter out
                # contaminated tools
                if hasattr(engine, "tools") and engine.tools:
                    for tool in engine.tools:
                        tool_name = getattr(
                            tool, "name", getattr(tool, "__name__", str(tool))
                        )

                        # FILTER: Only include tools that are NOT Pydantic model classes
                        # Pydantic models (like Plan) should only be in
                        # structured_output_model, not tools
                        if hasattr(tool, "__bases__") and any(
                            "BaseModel" in str(base) for base in tool.__bases__
                        ):
                            logger.debug(
                                f"  Skipping Pydantic model '{tool_name}' from tools list (belongs in structured_output)"
                            )
                            continue

                        # FILTER: Only include actual callable tools
                        if callable(tool) or hasattr(tool, "invoke"):
                            original_engine_tools.append(tool)
                            logger.debug(f"  Including tool: {tool_name}")
                        else:
                            logger.debug(f"  Skipping non-callable tool: {tool_name}")

                # For schemas, only include structured_output_model if this
                # engine has it
                if (
                    hasattr(engine, "structured_output_model")
                    and engine.structured_output_model
                ):
                    original_engine_schemas.append(engine.structured_output_model)
                    model_name = getattr(
                        engine.structured_output_model,
                        "__name__",
                        str(engine.structured_output_model),
                    )
                    logger.debug(f"  Including structured output model: {model_name}")

                # ADDITIONAL FILTER: Remove any non-tool items that might have
                # been added incorrectly
                filtered_tools = []
                for tool in original_engine_tools:
                    # Skip if this looks like a Pydantic model class
                    if isinstance(tool, type) and hasattr(tool, "model_fields"):
                        logger.debug(
                            f"  Filtering out Pydantic model class from tools: {tool}"
                        )
                        continue
                    filtered_tools.append(tool)

                original_engine_tools = filtered_tools

                # Use filtered tools/schemas instead of all tools
                all_tools = original_engine_tools
                all_schemas = original_engine_schemas

                logger.info(
                    f"[bold green]✓ Filtered to {
                        len(all_tools)} tools and {
                        len(all_schemas)} schemas from engine[/bold green]"
                )

                # Get tool routes from engine, but filter them too
                if hasattr(engine, "tool_routes") and engine.tool_routes:
                    # Only copy routes for tools/schemas we actually have
                    filtered_routes = {}
                    tool_names = {
                        getattr(tool, "name", getattr(tool, "__name__", str(tool)))
                        for tool in all_tools
                    }
                    schema_names = {
                        getattr(schema, "__name__", str(schema))
                        for schema in all_schemas
                    }
                    all_names = tool_names | schema_names

                    for name, route in engine.tool_routes.items():
                        if name in all_names:
                            filtered_routes[name] = route

                    self.tool_routes = filtered_routes
                    logger.info(
                        f"[bold green]✓ Filtered tool routes to {
                            len(
                                self.tool_routes)} entries[/bold green]"
                    )
                    for name, route in list(self.tool_routes.items())[
                        :5
                    ]:  # Log first 5
                        logger.debug(f"    {name} -> {route}")
            else:
                logger.error(
                    f"[bold red]Could not find engine '{
                        self.engine_name}'[/bold red]"
                )

        # Add any manual overrides (these take precedence)
        if self.schemas:
            all_schemas.extend(self.schemas)
            logger.debug(f"  Added {len(self.schemas)} override schemas")
        if self.tools:
            all_tools.extend(self.tools)
            logger.debug(f"  Added {len(self.tools)} override tools")

        # Sync routes if we don't have them from engine
        if not self.tool_routes and (all_tools or all_schemas):
            logger.info("[bold cyan]Syncing tool routes from tools/schemas[/bold cyan]")
            combined = all_schemas + all_tools  # Schemas first for priority
            self.sync_tool_routes_from_tools(combined)
            logger.debug(f"  Generated {len(self.tool_routes)} tool routes")
            # Log first 5
            for name, route in list(self.tool_routes.items())[:5]:
                logger.debug(f"    {name} -> {route}")

        return all_tools, all_schemas

    def __call__(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> str | list[str]:
        """Validate and route tool calls to appropriate nodes.

        Returns ONLY routing decisions - no state updates!
        """
        import json
        import traceback
        from datetime import datetime

        validation_start_time = datetime.now()
        logger.info(
            f"[bold magenta]=== ValidationNodeConfig Execution START at {
                validation_start_time.strftime('%H:%M:%S.%f')} ===[/bold magenta]"
        )

        # Enhanced state debugging
        logger.debug("[bold blue]VALIDATION INPUT ANALYSIS[/bold blue]")
        logger.debug(f"  State type: {type(state).__name__}")
        logger.debug(f"  State ID: {id(state)}")
        logger.debug(f"  Config provided: {config is not None}")
        logger.debug(f"  Available nodes: {self.available_nodes}")
        logger.debug(f"  Engine name: {self.engine_name}")
        logger.debug(f"  Messages key: {self.messages_key}")

        # Log comprehensive state contents for debugging
        logger.debug("[bold cyan]STATE INSPECTION[/bold cyan]")
        if hasattr(state, "__dict__"):
            state_attrs = list(state.__dict__.keys())
            logger.debug(
                f"  State attributes ({
                    len(state_attrs)}): {state_attrs}"
            )

            # Log values for key attributes
            for attr in ["messages", "engines", "tools", "tool_routes"]:
                if hasattr(state, attr):
                    attr_value = getattr(state, attr)
                    if attr == "messages":
                        logger.debug(
                            f"    {attr}: {
                                len(attr_value) if attr_value else 0} messages"
                        )
                        if attr_value:
                            # Last 3 messages
                            for i, msg in enumerate(attr_value[-3:]):
                                logger.debug(
                                    f"      [{i}] {
                                        type(msg).__name__}: {
                                        str(msg)[
                                            :100]}..."
                                )
                    elif attr == "engines":
                        if isinstance(attr_value, dict):
                            logger.debug(
                                f"    {attr}: {
                                    list(
                                        attr_value.keys())}"
                            )
                        else:
                            logger.debug(
                                f"    {attr}: {
                                    type(attr_value)} - {attr_value}"
                            )
                    elif attr == "tools":
                        logger.debug(
                            f"    {attr}: {
                                len(attr_value) if attr_value else 0} tools"
                        )
                        if attr_value:
                            tool_names = [
                                getattr(t, "name", str(t)) for t in attr_value[:5]
                            ]
                            logger.debug(f"      Tools: {tool_names}")
                    elif attr == "tool_routes":
                        if isinstance(attr_value, dict):
                            logger.debug(
                                f"    {attr}: {
                                    len(attr_value)} routes"
                            )
                            for k, v in list(attr_value.items())[:5]:
                                logger.debug(f"      {k} -> {v}")
                        else:
                            logger.debug(
                                f"    {attr}: {
                                    type(attr_value)} - {attr_value}"
                            )
                else:
                    logger.debug(f"    {attr}: NOT PRESENT")

        if hasattr(state, "engines"):
            engines = state.engines
            logger.debug("[bold yellow]ENGINE INSPECTION[/bold yellow]")
            if isinstance(engines, dict):
                logger.debug(
                    f"  Engines dict with {
                        len(engines)} engines: {
                        list(
                            engines.keys())}"
                )
                for name, engine in engines.items():
                    logger.debug(
                        f"    Engine '{name}': {
                            type(engine).__name__}"
                    )
                    if hasattr(engine, "tools"):
                        tools_count = len(engine.tools) if engine.tools else 0
                        logger.debug(f"      Tools: {tools_count}")
                    if hasattr(engine, "tool_routes"):
                        routes_count = (
                            len(engine.tool_routes) if engine.tool_routes else 0
                        )
                        logger.debug(f"      Tool routes: {routes_count}")
                    if hasattr(engine, "schemas"):
                        schemas_count = len(engine.schemas) if engine.schemas else 0
                        logger.debug(f"      Schemas: {schemas_count}")
            else:
                logger.debug(
                    f"  Engines is not dict: {
                        type(engines)} - {engines}"
                )

        # Log configuration state
        logger.debug("[bold green]VALIDATION CONFIG[/bold green]")
        logger.debug(f"  Custom route mappings: {self.custom_route_mappings}")
        logger.debug(f"  Direct node routes: {self.direct_node_routes}")
        logger.debug(
            f"  Tool routes: {len(self.tool_routes) if self.tool_routes else 0}"
        )
        logger.debug(f"  Override tools: {len(self.tools)}")
        logger.debug(f"  Override schemas: {len(self.schemas)}")

        # Get tools and schemas from engine/state with detailed logging
        logger.info("[bold magenta]STEP 1: Syncing tools and schemas[/bold magenta]")
        try:
            validation_tools, validation_schemas = self._sync_tools_and_schemas(state)
            logger.info(
                f"[bold green]✓ Sync complete:[/bold green] {
                    len(validation_tools)} tools, {
                    len(validation_schemas)} schemas"
            )

            # Log detailed tool information
            logger.debug("[bold cyan]VALIDATION TOOLS DETAILS[/bold cyan]")
            for i, tool in enumerate(validation_tools[:10]):  # Log first 10
                tool_name = getattr(
                    tool, "name", getattr(tool, "__name__", f"tool_{i}")
                )
                tool_type = type(tool).__name__
                logger.debug(f"  [{i}] {tool_name} ({tool_type})")
                if hasattr(tool, "args_schema"):
                    logger.debug(f"      Args schema: {tool.args_schema}")

            # Log detailed schema information
            logger.debug("[bold cyan]VALIDATION SCHEMAS DETAILS[/bold cyan]")
            # Log first 10
            for i, schema in enumerate(validation_schemas[:10]):
                schema_name = getattr(schema, "__name__", f"schema_{i}")
                schema_type = type(schema).__name__
                logger.debug(f"  [{i}] {schema_name} ({schema_type})")
                if hasattr(schema, "model_fields"):
                    fields = list(schema.model_fields.keys())[:5]  # First 5 fields
                    logger.debug(f"      Fields: {fields}")

        except Exception as e:
            logger.exception(
                f"[bold red]ERROR in sync_tools_and_schemas: {e}[/bold red]"
            )
            logger.exception(
                f"[bold red]Traceback: {traceback.format_exc()}[/bold red]"
            )
            return "has_errors"

        # Get messages from state with enhanced validation
        logger.info("[bold magenta]STEP 2: Extracting messages[/bold magenta]")
        if not hasattr(state, self.messages_key):
            logger.error(
                f"[bold red]State missing messages key:[/bold red] {
                    self.messages_key}"
            )
            logger.error(
                f"[bold red]Available state attributes: {
                    list(
                        state.__dict__.keys()) if hasattr(
                        state,
                        '__dict__') else 'None'}[/bold red]"
            )
            return "has_errors"

        messages = getattr(state, self.messages_key, [])
        if not messages:
            logger.warning("[bold yellow]No messages found in state[/bold yellow]")
            logger.debug(f"Messages value: {messages}")
            logger.debug(f"Messages type: {type(messages)}")
            return "no_tool_calls"

        logger.info(
            f"[bold cyan]Processing {
                len(messages)} messages[/bold cyan]"
        )

        # Log all messages for debugging
        logger.debug("[bold cyan]MESSAGE ANALYSIS[/bold cyan]")
        for i, msg in enumerate(messages):
            msg_type = type(msg).__name__
            msg_content = str(msg)[:150] + "..." if len(str(msg)) > 150 else str(msg)
            logger.debug(f"  [{i}] {msg_type}: {msg_content}")

            # Special handling for AIMessage
            if isinstance(msg, AIMessage):
                if hasattr(msg, "tool_calls") and msg.tool_calls:
                    logger.debug(f"      Tool calls: {len(msg.tool_calls)}")
                    for j, tc in enumerate(msg.tool_calls[:3]):  # First 3
                        tool_name = get_tool_name(tc)
                        logger.debug(f"        [{j}] {tool_name}")

        last_message = messages[-1]
        logger.debug(
            f"[bold blue]Last message type: {
                type(last_message).__name__}[/bold blue]"
        )
        logger.debug(
            f"[bold blue]Last message content: {
                str(last_message)[
                    :200]}...[/bold blue]"
        )

        if not isinstance(last_message, AIMessage):
            logger.warning(
                f"[bold yellow]Last message is not AIMessage: {
                    type(last_message).__name__}[/bold yellow]"
            )
            logger.debug(f"Message content: {last_message}")
            return "no_tool_calls"

        # Extract tool calls with enhanced debugging
        logger.info("[bold magenta]STEP 3: Extracting tool calls[/bold magenta]")
        tool_calls = []

        # Check primary location for tool calls
        if hasattr(last_message, "tool_calls") and last_message.tool_calls:
            tool_calls = last_message.tool_calls
            logger.info(
                f"[bold green]✓ Found {
                    len(tool_calls)} tool calls in message.tool_calls[/bold green]"
            )
        # Check alternative location
        elif (
            hasattr(last_message, "additional_kwargs")
            and "tool_calls" in last_message.additional_kwargs
        ):
            tool_calls = last_message.additional_kwargs["tool_calls"]
            logger.info(
                f"[bold green]✓ Found {
                    len(tool_calls)} tool calls in additional_kwargs[/bold green]"
            )
        else:
            # Enhanced debugging for missing tool calls
            logger.warning(
                "[bold yellow]No tool calls found in last message[/bold yellow]"
            )
            logger.debug(f"Last message attributes: {dir(last_message)}")
            if hasattr(last_message, "additional_kwargs"):
                logger.debug(
                    f"Additional kwargs keys: {
                        list(
                            last_message.additional_kwargs.keys())}"
                )
            logger.debug(f"Last message full content: {last_message}")
            return "no_tool_calls"

        # Log detailed tool call information
        logger.debug("[bold cyan]TOOL CALLS ANALYSIS[/bold cyan]")
        for i, tool_call in enumerate(tool_calls):
            tool_name = get_tool_name(tool_call)
            tool_args = get_tool_args(tool_call)
            tool_id = get_tool_id(tool_call)
            logger.debug(f"  [{i}] Tool: {tool_name}")
            logger.debug(f"      ID: {tool_id}")
            logger.debug(f"      Args: {tool_args}")
            logger.debug(f"      Raw tool_call: {tool_call}")

        if not tool_calls:
            logger.info(
                "[bold yellow]No tool calls found after extraction[/bold yellow]"
            )
            return "no_tool_calls"

        # Build tool name mapping for validation
        logger.debug("[bold blue]Building tool name mapping[/bold blue]")
        tool_name_mapping = {}

        for schema in validation_schemas:
            if hasattr(schema, "__name__"):
                tool_name_mapping[schema.__name__] = schema
                logger.debug(f"  Schema: {schema.__name__}")
            if hasattr(schema, "name"):
                tool_name_mapping[schema.name] = schema
                logger.debug(f"  Schema (by name): {schema.name}")

        for tool in validation_tools:
            if hasattr(tool, "name"):
                tool_name_mapping[tool.name] = tool
                logger.debug(f"  Tool: {tool.name}")
            elif hasattr(tool, "__name__"):
                tool_name_mapping[tool.__name__] = tool
                logger.debug(f"  Tool (by __name__): {tool.__name__}")

        logger.info(
            f"[bold cyan]Total tools/schemas available:[/bold cyan] {
                len(tool_name_mapping)}"
        )

        # Process tool calls and determine routing with enhanced validation and
        # message creation
        logger.info(
            f"[bold magenta]STEP 5: Processing {
                len(tool_calls)} tool calls for validation and routing[/bold magenta]"
        )
        destinations = set()
        has_errors = False
        tool_messages_to_add = []  # Track tool messages that need to be added to state

        for i, tool_call in enumerate(tool_calls):
            tool_name = get_tool_name(tool_call)
            tool_id = get_tool_id(tool_call)
            tool_args = get_tool_args(tool_call)

            logger.info(
                f"\n[bold cyan]Processing tool call {
                    i + 1}/{
                    len(tool_calls)}: {tool_name}[/bold cyan]"
            )
            logger.debug(f"  Tool ID: {tool_id}")
            logger.debug(
                f"  Tool args: {
                    json.dumps(
                        tool_args,
                        indent=2) if isinstance(
                        tool_args,
                        dict) else tool_args}"
            )

            # Check if tool exists in our mapping
            if tool_name not in tool_name_mapping:
                logger.error(
                    f"  [bold red]✗ Tool '{tool_name}' not found in available tools![/bold red]"
                )
                logger.debug(
                    f"  Available tools: {
                        list(
                            tool_name_mapping.keys())}"
                )

                # Create error tool message for unknown tool
                error_message = ToolMessage(
                    content=f"Error: Tool '{tool_name}' not found in available tools",
                    tool_call_id=tool_id,
                    name=tool_name,
                    additional_kwargs={
                        "is_error": True,
                        "error_type": "tool_not_found",
                    },
                )
                tool_messages_to_add.append(error_message)
                logger.debug("  Created error ToolMessage for unknown tool")

                has_errors = True
                continue

            # Get the tool/schema object and route
            tool_or_schema = tool_name_mapping[tool_name]
            route = self.tool_routes.get(tool_name, "unknown")
            logger.debug(f"  Route: {route}")
            logger.debug(f"  Tool/Schema type: {type(tool_or_schema).__name__}")

            # Determine destination node
            destination = self._get_node_for_route(route)
            logger.debug(f"  Destination node: {destination}")

            # Determine tool type more carefully
            is_pydantic_model = (
                route == "pydantic_model"
                and hasattr(tool_or_schema, "model_fields")
                and hasattr(tool_or_schema, "model_validate")
                # Not a LangChain tool
                and not hasattr(tool_or_schema, "invoke")
                and not hasattr(tool_or_schema, "run")  # Not a LangChain tool
                and not hasattr(tool_or_schema, "_run")  # Not a LangChain tool
            )

            is_structured_tool = (
                hasattr(tool_or_schema, "invoke")
                or hasattr(tool_or_schema, "run")
                or hasattr(tool_or_schema, "_run")
                or hasattr(tool_or_schema, "args_schema")
                or route in ["langchain_tool", "function", "retriever"]
            )

            logger.debug("  Tool type analysis:")
            logger.debug(f"    Route: {route}")
            logger.debug(
                f"    Has model_fields: {
                    hasattr(
                        tool_or_schema,
                        'model_fields')}"
            )
            logger.debug(
                f"    Has model_validate: {
                    hasattr(
                        tool_or_schema,
                        'model_validate')}"
            )
            logger.debug(
                f"    Has invoke: {
                    hasattr(
                        tool_or_schema,
                        'invoke')}"
            )
            logger.debug(f"    Has run: {hasattr(tool_or_schema, 'run')}")
            logger.debug(
                f"    Has args_schema: {
                    hasattr(
                        tool_or_schema,
                        'args_schema')}"
            )
            logger.debug(f"    Is Pydantic model: {is_pydantic_model}")
            logger.debug(f"    Is structured tool: {is_structured_tool}")

            # Handle Pydantic models (actual schema classes, not tools)
            if is_pydantic_model:
                logger.info(
                    f"  [bold blue]Processing Pydantic model: {tool_name}[/bold blue]"
                )

                try:
                    # Validate Pydantic model arguments
                    validated_data = tool_or_schema.model_validate(tool_args)
                    result_content = validated_data.model_dump()

                    # Create successful tool message
                    tool_message = ToolMessage(
                        content=json.dumps(result_content, indent=2),
                        tool_call_id=tool_id,
                        name=tool_name,
                        additional_kwargs={
                            "is_error": False,
                            "validation_passed": True,
                            "model_type": "pydantic",
                            "validated_data": result_content,
                        },
                    )
                    tool_messages_to_add.append(tool_message)

                    # Debug validated tool call (breakpoint removed)
                    logger.debug("=" * 80)
                    logger.debug("🔍 VALIDATED TOOL CALL DEBUG")
                    logger.debug("=" * 80)
                    logger.debug(f"Tool name: {tool_name}")
                    logger.debug(f"Tool ID: {tool_id}")
                    logger.debug(f"Tool args (raw): {tool_args}")
                    logger.debug(f"Validated data: {validated_data}")
                    logger.debug(f"Result content: {result_content}")
                    logger.debug(f"Tool message content: {tool_message.content}")
                    logger.debug(
                        f"Tool message content type: {type(tool_message.content)}"
                    )
                    logger.debug(f"Destination: {destination}")
                    logger.debug("=" * 80)

                    logger.info(
                        f"  [bold green]✓ Pydantic validation passed, created ToolMessage, routing to {destination}[/bold green]"
                    )
                    destinations.add(destination)

                except Exception as e:
                    logger.exception(
                        f"  [bold red]✗ Pydantic validation failed: {e}[/bold red]"
                    )

                    # Create error tool message and route to agent
                    error_message = ToolMessage(
                        content=f"Validation error: {e!s}",
                        tool_call_id=tool_id,
                        name=tool_name,
                        additional_kwargs={
                            "is_error": True,
                            "error_type": "validation_failed",
                            "error_details": str(e),
                        },
                    )
                    tool_messages_to_add.append(error_message)
                    logger.info(
                        "  [bold yellow]Created error ToolMessage, routing to agent[/bold yellow]"
                    )
                    # Route to agent on error
                    destinations.add(self.agent_node)
                continue

            # Check if should skip validation for direct routes
            if route in self.direct_node_routes:
                logger.debug(
                    "  [bold green]✓ Direct route - skipping validation, adding destination[/bold green]"
                )
                destinations.add(destination)
                continue

            # For other tools (langchain tools, functions, etc.), validate and
            # route appropriately
            logger.debug(
                f"  [bold blue]Processing other tool (non-Pydantic): {tool_name}[/bold blue]"
            )

            # Create temporary message for validation
            temp_message = AIMessage(content="", tool_calls=[tool_call])
            temp_messages = [*messages[:-1], temp_message]

            # Create validation node with both tools and schemas
            combined_schemas = list(validation_tools) + list(validation_schemas)
            validation_node = ValidationNode(
                schemas=combined_schemas,
                format_error=self.format_error,
            )

            try:
                # Run validation
                logger.debug("    Invoking ValidationNode...")
                result = validation_node.invoke({"messages": temp_messages})
                validated_messages = result.get("messages", [])
                logger.debug(
                    f"    ValidationNode returned {
                        len(validated_messages)} messages"
                )

                # Check for validation errors
                validation_failed = False

                for msg in validated_messages:
                    if isinstance(msg, ToolMessage) and (
                        msg.name == tool_name
                        or getattr(msg, "tool_call_id", None) == tool_id
                    ):
                        logger.debug(f"    Found ToolMessage: {msg.content[:100]}...")

                        if has_tool_error(msg):
                            logger.warning(
                                f"  [bold red]✗ Validation failed for {tool_name}[/bold red]"
                            )
                            logger.debug(f"    Error content: {msg.content}")
                            validation_failed = True

                            # For other tools: Only create error tool message
                            # on validation failure
                            tool_messages_to_add.append(msg)
                            logger.info(
                                "  [bold yellow]Created error ToolMessage, routing to agent[/bold yellow]"
                            )
                            destinations.add(
                                self.agent_node
                            )  # Route to agent on validation failure
                        else:
                            logger.info(
                                f"  [bold green]✓ Validation passed for {tool_name}[/bold green]"
                            )
                            # For other tools: Validation passed, route to
                            # tool_node (tool_node will create messages)
                            destinations.add(destination)

                        break

                # If no validation errors found, route to tool_node
                if not validation_failed:
                    logger.info(
                        f"  [bold green]✓ No validation errors, routing to {destination}[/bold green]"
                    )
                    destinations.add(destination)

            except Exception as e:
                logger.exception(
                    f"[bold red]Validation exception for {tool_name}:[/bold red] {e}"
                )
                logger.exception(
                    f"[bold red]Full traceback: {
                        traceback.format_exc()}[/bold red]"
                )

                # Create error tool message for validation exception and route
                # to agent
                error_message = ToolMessage(
                    content=f"Validation exception: {e!s}",
                    tool_call_id=tool_id,
                    name=tool_name,
                    additional_kwargs={
                        "is_error": True,
                        "error_type": "validation_exception",
                        "error_details": str(e),
                    },
                )
                tool_messages_to_add.append(error_message)
                # Route to agent on exception
                destinations.add(self.agent_node)
                has_errors = True

        # CRITICAL: Add all tool messages to the state - this was working
        # before
        if tool_messages_to_add:
            logger.info(
                f"[bold magenta]STEP 6: Adding {
                    len(tool_messages_to_add)} tool messages to state[/bold magenta]"
            )

            # Create updated messages list
            updated_messages = list(messages) + tool_messages_to_add

            # Update state with new messages - MULTIPLE approaches to ensure it
            # works
            state_updated = False

            # Method 1: Direct attribute setting (for Pydantic models)
            if hasattr(state, self.messages_key):
                try:
                    setattr(state, self.messages_key, updated_messages)
                    state_updated = True
                    logger.info(
                        f"  [bold green]✓ Method 1: Updated state.{
                            self.messages_key} with {
                            len(tool_messages_to_add)} new tool messages[/bold green]"
                    )
                except Exception as e:
                    logger.warning(f"  Method 1 failed: {e}")

            # Method 2: Dictionary-style setting
            if not state_updated and hasattr(state, "__setitem__"):
                try:
                    state[self.messages_key] = updated_messages
                    state_updated = True
                    logger.info(
                        f"  [bold green]✓ Method 2: Updated state['{
                            self.messages_key}'] with {
                            len(tool_messages_to_add)} new tool messages[/bold green]"
                    )
                except Exception as e:
                    logger.warning(f"  Method 2 failed: {e}")

            # Method 3: For TypedDict or other dict-like objects
            if not state_updated and isinstance(state, dict):
                try:
                    state[self.messages_key] = updated_messages
                    state_updated = True
                    logger.info(
                        f"  [bold green]✓ Method 3: Updated dict state['{
                            self.messages_key}'] with {
                            len(tool_messages_to_add)} new tool messages[/bold green]"
                    )
                except Exception as e:
                    logger.warning(f"  Method 3 failed: {e}")

            if not state_updated:
                logger.error(
                    "  [bold red]CRITICAL: Could not update state with tool messages![/bold red]"
                )
                logger.error(f"  State type: {type(state)}")
                logger.error(f"  State attributes: {dir(state)}")

            # Log the tool messages that were added
            for i, tm in enumerate(tool_messages_to_add):
                logger.debug(
                    f"    [{i}] ToolMessage: {
                        tm.name} (ID: {
                        getattr(
                            tm,
                            'tool_call_id',
                            'unknown')})"
                )
                logger.debug(f"        Content: {tm.content[:100]}...")
                if hasattr(tm, "additional_kwargs") and tm.additional_kwargs:
                    logger.debug(f"        Metadata: {tm.additional_kwargs}")
        else:
            logger.warning(
                "[bold yellow]No tool messages created during validation[/bold yellow]"
            )

        # Determine routing based on results with comprehensive logging
        validation_end_time = datetime.now()
        validation_duration = validation_end_time - validation_start_time

        logger.info("\n[bold magenta]STEP 7: Final routing decision[/bold magenta]")
        logger.info(f"  Destinations found: {destinations}")
        logger.info(f"  Has errors: {has_errors}")
        logger.info(f"  Tool messages created: {len(tool_messages_to_add)}")
        logger.info(
            f"  Validation duration: {
                validation_duration.total_seconds():.3f}s"
        )

        # Log detailed routing analysis
        logger.debug("[bold cyan]ROUTING ANALYSIS[/bold cyan]")
        logger.debug(f"  Total tool calls processed: {len(tool_calls)}")
        logger.debug(
            f"  Tool calls with errors: {
                sum(
                    1 for tc in tool_calls if get_tool_name(tc) not in tool_name_mapping)}"
        )
        logger.debug(f"  Successful validations: {len(destinations)}")

        # If all validations failed, return to agent
        if has_errors and not destinations:
            logger.warning(
                "[bold yellow]All validations failed - routing to 'has_errors'[/bold yellow]"
            )
            logger.debug(
                f"  Reason: has_errors={has_errors}, destinations={destinations}"
            )
            validation_result = "has_errors"
        # Route to appropriate destination(s)
        elif not destinations:
            logger.warning(
                "[bold yellow]No valid destinations found - ending[/bold yellow]"
            )
            logger.debug("  Reason: destinations is empty, END will be returned")
            validation_result = END
        else:
            # Convert destinations to list for consistent return type
            destinations_list = list(destinations)

            if len(destinations_list) == 1:
                destination = destinations_list[0]
                logger.info(
                    f"[bold green]✓ Single destination:[/bold green] {destination}"
                )
                validation_result = destination
            else:
                logger.info(
                    f"[bold green]✓ Multiple destinations:[/bold green] {destinations_list}"
                )
                validation_result = destinations_list

        # Final summary logging
        logger.info(
            f"[bold magenta]=== ValidationNodeConfig Complete at {
                validation_end_time.strftime('%H:%M:%S.%f')} ===[/bold magenta]"
        )
        logger.info(
            f"[bold green]✓ Validation result: {validation_result}[/bold green]"
        )
        logger.info("[bold cyan]Processing summary:[/bold cyan]")
        logger.info(
            f"  • Duration: {
                validation_duration.total_seconds():.3f}s"
        )
        logger.info(f"  • Tool calls: {len(tool_calls)}")
        logger.info(f"  • Tool messages created: {len(tool_messages_to_add)}")
        logger.info(f"  • Validation errors: {has_errors}")
        logger.info(f"  • Final routing: {validation_result}")

        return validation_result
