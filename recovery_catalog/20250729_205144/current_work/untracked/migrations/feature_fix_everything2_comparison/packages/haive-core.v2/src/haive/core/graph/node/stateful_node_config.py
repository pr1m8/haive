"""Stateful Node Configuration - Enhanced Dynamic Architecture.

This module provides a truly dynamic node architecture where:
- All routing destinations are discovered from state at runtime
- Field configurations are dynamically resolved from state
- Engine references, tool references, and node references are all stateful
- Nodes adapt their behavior based on what's available in state

Key Features:
- Runtime discovery of engines, tools, and routing destinations
- Dynamic field mapping configuration
- Stateful routing with fallback mechanisms
- Type-safe parameter extraction with automatic field detection
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, get_type_hints

from langchain_core.messages import BaseMessage
from langgraph.types import Command
from pydantic import BaseModel, Field

from haive.core.graph.common.types import ConfigLike, StateLike
from haive.core.graph.node.base_node_config import BaseNodeConfig
from haive.core.graph.node.types import NodeType

logger = logging.getLogger(__name__)


class StatefulNodeConfig(BaseNodeConfig, ABC):
    """Base class for stateful nodes that discover resources from state at runtime.

    This class provides the foundation for truly dynamic nodes that:
    - Discover engines by name or type from state
    - Resolve routing destinations based on state configuration
    - Adapt field mappings based on available state fields
    - Handle fallback mechanisms when resources are not found
    """

    # Discovery configuration
    discovery_enabled: bool = Field(
        default=True, description="Whether to enable dynamic discovery from state"
    )

    # Engine discovery
    engine_name: str | None = Field(
        default=None,
        description="Engine name to discover from state (if not found, uses discovery)",
    )

    engine_type: type | None = Field(
        default=None,
        description="Engine type to discover from state (fallback if name not found)",
    )

    # Routing discovery
    routing_discovery_enabled: bool = Field(
        default=True, description="Whether to discover routing destinations from state"
    )

    routing_prefix: str = Field(
        default="",
        description="Prefix for routing key discovery (e.g., 'validation_' for validation_tool_node)",
    )

    # Field discovery
    field_discovery_enabled: bool = Field(
        default=True, description="Whether to discover field mappings from state"
    )

    auto_field_mapping: bool = Field(
        default=True,
        description="Whether to automatically map fields based on type hints",
    )

    # Fallback configuration
    fallback_routing: dict[str, str] = Field(
        default_factory=dict, description="Fallback routing when state discovery fails"
    )

    def discover_engine(self, state: StateLike) -> Any | None:
        """Discover engine from state using multiple strategies.

        Args:
            state: State object to search for engines

        Returns:
            Engine instance or None if not found
        """
        if not self.discovery_enabled:
            return None

        # Strategy 1: By engine name
        if self.engine_name:
            engine = self._discover_engine_by_name(state, self.engine_name)
            if engine:
                logger.info(f"Discovered engine by name: {self.engine_name}")
                return engine

        # Strategy 2: By engine type
        if self.engine_type:
            engine = self._discover_engine_by_type(state, self.engine_type)
            if engine:
                logger.info(
                    f"Discovered engine by type: {
                        self.engine_type.__name__}"
                )
                return engine

        # Strategy 3: From last AI message attribution
        engine = self._discover_engine_from_message_attribution(state)
        if engine:
            logger.info("Discovered engine from message attribution")
            return engine

        # Strategy 4: Default engine in state
        engine = self._discover_default_engine(state)
        if engine:
            logger.info("Discovered default engine from state")
            return engine

        logger.warning("No engine discovered from state")
        return None

    def discover_routing_destination(
        self, state: StateLike, route_key: str
    ) -> str | None:
        """Discover routing destination from state configuration.

        Args:
            state: State object to search
            route_key: Key to look for (e.g., 'tool_node', 'parser_node')

        Returns:
            Node name to route to or None if not found
        """
        if not self.routing_discovery_enabled:
            return self.fallback_routing.get(route_key)

        # Strategy 1: Direct key lookup with prefix
        full_key = f"{self.routing_prefix}{route_key}"
        destination = self._get_state_value(state, full_key)
        if destination:
            logger.info(f"Discovered routing destination: {full_key} -> {destination}")
            return destination

        # Strategy 2: Direct key lookup without prefix
        destination = self._get_state_value(state, route_key)
        if destination:
            logger.info(f"Discovered routing destination: {route_key} -> {destination}")
            return destination

        # Strategy 3: From routing configuration in state
        routing_config = self._get_state_value(state, "routing_config")
        if isinstance(routing_config, dict):
            destination = routing_config.get(route_key)
            if destination:
                logger.info(
                    f"Discovered routing from config: {route_key} -> {destination}"
                )
                return destination

        # Strategy 4: From node registry in state
        node_registry = self._get_state_value(state, "node_registry")
        if isinstance(node_registry, dict):
            destination = node_registry.get(route_key)
            if destination:
                logger.info(
                    f"Discovered routing from registry: {route_key} -> {destination}"
                )
                return destination

        # Strategy 5: Fallback
        fallback = self.fallback_routing.get(route_key)
        if fallback:
            logger.info(f"Using fallback routing: {route_key} -> {fallback}")
            return fallback

        logger.warning(f"No routing destination found for: {route_key}")
        return None

    def discover_field_mapping(
        self, state: StateLike, callable_func: callable | None = None
    ) -> dict[str, str]:
        """Discover field mapping from state and function signatures.

        Args:
            state: State object to analyze
            callable_func: Function to analyze for parameter mapping

        Returns:
            Dictionary mapping parameter names to state field names
        """
        if not self.field_discovery_enabled:
            return {}

        mapping = {}

        # Strategy 1: Explicit field mapping in state
        state_mapping = self._get_state_value(state, "field_mapping")
        if isinstance(state_mapping, dict):
            mapping.update(state_mapping)
            logger.info(f"Discovered field mapping from state: {state_mapping}")

        # Strategy 2: Auto-mapping based on callable signature
        if callable_func and self.auto_field_mapping:
            auto_mapping = self._auto_discover_field_mapping(state, callable_func)
            # Only add auto-mapping if not already explicitly configured
            for param, field in auto_mapping.items():
                if param not in mapping:
                    mapping[param] = field

        # Strategy 3: Type-based field discovery
        if callable_func:
            type_mapping = self._discover_field_mapping_by_types(state, callable_func)
            for param, field in type_mapping.items():
                if param not in mapping:
                    mapping[param] = field

        logger.info(f"Final field mapping: {mapping}")
        return mapping

    def _discover_engine_by_name(self, state: StateLike, name: str) -> Any | None:
        """Discover engine by exact name match."""
        # Check state.engines dict
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            # Direct key lookup
            if name in state.engines:
                return state.engines[name]
            # Name attribute lookup
            for engine in state.engines.values():
                if hasattr(engine, "name") and engine.name == name:
                    return engine

        # Check state attributes
        if hasattr(state, name):
            return getattr(state, name)

        # Check registry
        try:
            from haive.core.engine.base import EngineRegistry

            registry = EngineRegistry.get_instance()
            return registry.find(name)
        except Exception:
            pass

        return None

    def _discover_engine_by_type(
        self, state: StateLike, engine_type: type
    ) -> Any | None:
        """Discover engine by type match."""
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            for engine in state.engines.values():
                if isinstance(engine, engine_type):
                    return engine

        # Check state attributes
        for attr_name in dir(state):
            if not attr_name.startswith("_"):
                attr_value = getattr(state, attr_name)
                if isinstance(attr_value, engine_type):
                    return attr_value

        return None

    def _discover_engine_from_message_attribution(self, state: StateLike) -> Any | None:
        """Discover engine from last AI message attribution."""
        messages = self._get_state_value(state, "messages")
        if not messages:
            return None

        # Find last AI message with engine attribution
        for msg in reversed(messages):
            if hasattr(msg, "additional_kwargs") and msg.additional_kwargs:
                engine_name = msg.additional_kwargs.get("engine_name")
                if engine_name:
                    return self._discover_engine_by_name(state, engine_name)

        return None

    def _discover_default_engine(self, state: StateLike) -> Any | None:
        """Discover default engine from state."""
        # Check for default_engine field
        default_engine = self._get_state_value(state, "default_engine")
        if default_engine:
            return default_engine

        # Check for single engine in engines dict
        if hasattr(state, "engines") and isinstance(state.engines, dict):
            if len(state.engines) == 1:
                return next(iter(state.engines.values()))

        return None

    def _auto_discover_field_mapping(
        self, state: StateLike, callable_func: callable
    ) -> dict[str, str]:
        """Auto-discover field mapping based on parameter names and state fields."""
        import inspect

        mapping = {}
        sig = inspect.signature(callable_func)
        available_fields = self._get_available_state_fields(state)

        for param_name in sig.parameters:
            if param_name in available_fields:
                mapping[param_name] = param_name
                logger.debug(f"Auto-mapped parameter: {param_name} -> {param_name}")

        return mapping

    def _discover_field_mapping_by_types(
        self, state: StateLike, callable_func: callable
    ) -> dict[str, str]:
        """Discover field mapping based on type hints."""
        import inspect

        mapping = {}
        sig = inspect.signature(callable_func)
        type_hints = get_type_hints(callable_func)

        for param_name, _param in sig.parameters.items():
            if param_name in type_hints:
                param_type = type_hints[param_name]

                # Look for state fields with matching types
                field_name = self._find_field_by_type(state, param_type)
                if field_name:
                    mapping[param_name] = field_name
                    logger.debug(f"Type-mapped parameter: {param_name} -> {field_name}")

        return mapping

    def _get_available_state_fields(self, state: StateLike) -> set[str]:
        """Get all available field names from state."""
        fields = set()

        # From state attributes
        if hasattr(state, "__dict__"):
            fields.update(state.__dict__.keys())

        # From state dict access
        if hasattr(state, "keys"):
            fields.update(state.keys())

        # From Pydantic model fields
        if hasattr(state, "model_fields"):
            fields.update(state.model_fields.keys())

        return fields

    def _find_field_by_type(self, state: StateLike, target_type: type) -> str | None:
        """Find state field with matching type."""
        # Check state attributes
        if hasattr(state, "__dict__"):
            for field_name, field_value in state.__dict__.items():
                if isinstance(field_value, target_type):
                    return field_name

        # Check Pydantic model fields
        if hasattr(state, "model_fields"):
            for field_name, field_info in state.model_fields.items():
                if (
                    hasattr(field_info, "annotation")
                    and field_info.annotation == target_type
                ):
                    return field_name

        return None

    def _get_state_value(self, obj: Any, field: str) -> Any:
        """Get value from state object using multiple strategies."""
        # Attribute access
        if hasattr(obj, field):
            return getattr(obj, field)

        # Dict access
        if hasattr(obj, "__getitem__"):
            try:
                return obj[field]
            except (KeyError, TypeError):
                pass

        # Nested field access (e.g., "config.routing.tool_node")
        if "." in field:
            parts = field.split(".")
            current = obj
            for part in parts:
                current = self._get_state_value(current, part)
                if current is None:
                    return None
            return current

        return None

    @abstractmethod
    def execute_stateful_logic(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command:
        """Execute the node's stateful logic.

        This method should be implemented by subclasses to provide the actual
        node functionality using the discovered resources.

        Args:
            state: Current state
            config: Optional configuration

        Returns:
            Command object with updates and routing
        """

    def __call__(self, state: StateLike, config: ConfigLike | None = None) -> Command:
        """Execute the stateful node with dynamic discovery."""
        try:
            # Perform discovery before execution
            logger.info(f"Starting stateful execution for {self.name}")

            # Log discovery results
            if self.discovery_enabled:
                engine = self.discover_engine(state)
                if engine:
                    logger.info(
                        f"Discovered engine: {
                            getattr(
                                engine,
                                'name',
                                type(engine).__name__)}"
                    )

            # Execute the actual node logic
            return self.execute_stateful_logic(state, config)

        except Exception as e:
            logger.exception(f"Error in stateful node {self.name}: {e}")
            # Fallback to default routing
            fallback_goto = self.fallback_routing.get("default", "END")
            return Command(
                update={"error": f"Stateful node error: {e!s}"}, goto=fallback_goto
            )


class StatefulValidationNodeConfig(StatefulNodeConfig):
    """Stateful validation node that discovers everything from state."""

    node_type: NodeType = Field(default=NodeType.VALIDATION)

    # Default routing keys for discovery
    routing_prefix: str = Field(default="validation_")

    # Default fallbacks
    fallback_routing: dict[str, str] = Field(
        default_factory=lambda: {
            "tool_node": "tool_node",
            "parser_node": "parse_output",
            "default": "END",
        }
    )

    def execute_stateful_logic(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command:
        """Execute validation logic with dynamic discovery."""
        # Get messages
        messages = self._get_state_value(state, "messages")
        if not messages:
            return Command(goto="END")

        last_message = messages[-1]
        if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
            return Command(goto="END")

        # Discover routing destinations
        tool_node = self.discover_routing_destination(state, "tool_node")
        parser_node = self.discover_routing_destination(state, "parser_node")

        # Discover engine for tool routes
        engine = self.discover_engine(state)
        tool_routes = self._get_state_value(state, "tool_routes") or {}

        # Process tool calls
        new_messages = []
        destinations = set()

        for tool_call in last_message.tool_calls:
            tool_name = tool_call.get("name")
            route = tool_routes.get(tool_name, "unknown")

            if route == "pydantic_model":
                # Validate and route to parser
                tool_msg = self._validate_pydantic_model(tool_call, engine)
                new_messages.append(tool_msg)
                if parser_node:
                    destinations.add(parser_node)

            elif route in ["langchain_tool", "function", "tool_node"]:
                # Route to tool node
                if tool_node:
                    destinations.add(tool_node)

        # Update state and route
        update_dict = {}
        if new_messages:
            update_dict["messages"] = new_messages

        goto = self._determine_destination(destinations)
        return Command(update=update_dict, goto=goto)

    def _validate_pydantic_model(self, tool_call: dict, engine: Any) -> Any:
        """Validate pydantic model tool call."""
        from langchain_core.messages import ToolMessage

        tool_name = tool_call.get("name")
        tool_id = tool_call.get("id")
        args = tool_call.get("args", {})

        try:
            # Find model in engine
            model_class = self._find_model_in_engine(engine, tool_name)
            if model_class:
                model_instance = model_class(**args)
                return ToolMessage(
                    content=f"Successfully validated {tool_name}: {
                        model_instance.model_dump()}",
                    tool_call_id=tool_id,
                    name=tool_name,
                )
            return ToolMessage(
                content=f"Model class not found: {tool_name}",
                tool_call_id=tool_id,
                name=tool_name,
            )
        except Exception as e:
            return ToolMessage(
                content=f"Validation error: {e!s}",
                tool_call_id=tool_id,
                name=tool_name,
            )

    def _find_model_in_engine(
        self, engine: Any, tool_name: str
    ) -> type[BaseModel] | None:
        """Find pydantic model in engine."""
        if not engine:
            return None

        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
        ) and getattr(engine.structured_output_model, "__name__", None) == tool_name:
            return engine.structured_output_model

        # Check schemas
        if hasattr(engine, "schemas") and engine.schemas:
            for schema in engine.schemas:
                if getattr(schema, "__name__", None) == tool_name:
                    return schema

        return None

    def _determine_destination(self, destinations: set[str]) -> str:
        """Determine routing destination."""
        if not destinations:
            return self.fallback_routing.get("default", "END")

        destinations_list = list(destinations)
        if len(destinations_list) == 1:
            return destinations_list[0]

        # Prioritize tool_node over parser_node
        tool_node = self.discover_routing_destination(None, "tool_node")
        if tool_node in destinations_list:
            return tool_node

        return destinations_list[0]


class StatefulParserNodeConfig(StatefulNodeConfig):
    """Stateful parser node that discovers routing from state."""

    node_type: NodeType = Field(default=NodeType.PARSER)

    # Default routing keys
    routing_prefix: str = Field(default="parser_")

    # Default fallbacks
    fallback_routing: dict[str, str] = Field(
        default_factory=lambda: {"agent_node": "agent", "default": "END"}
    )

    def execute_stateful_logic(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command:
        """Execute parser logic with dynamic discovery."""
        # Discover routing destination
        agent_node = self.discover_routing_destination(state, "agent_node")

        # Discover engine for tool lookup
        engine = self.discover_engine(state)

        # Get messages
        messages = self._get_state_value(state, "messages")
        if not messages:
            return Command(goto=agent_node or "END")

        # Extract tool information
        tool_name, tool_call, tool_message = self._extract_tool_from_messages(messages)
        if not tool_name:
            return Command(goto=agent_node or "END")

        # Find tool class in engine
        tool_class = self._find_tool_in_engine(engine, tool_name)
        if not tool_class:
            return Command(
                update={"error": f"Tool class not found: {tool_name}"},
                goto=agent_node or "END",
            )

        # Parse tool content
        try:
            content = (
                tool_message.content if tool_message else tool_call.get("args", {})
            )
            parsed_result = self._parse_tool_content(content, tool_class)

            # Determine field name
            field_name = self._determine_field_name(tool_class, tool_name)

            return Command(update={field_name: parsed_result}, goto=agent_node or "END")

        except Exception as e:
            return Command(
                update={"error": f"Parse error: {e!s}"}, goto=agent_node or "END"
            )

    def _extract_tool_from_messages(self, messages: list[BaseMessage]) -> tuple:
        """Extract tool information from messages."""
        # Find last AI message with tool calls
        for msg in reversed(messages):
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_call = msg.tool_calls[-1]
                tool_name = tool_call.get("name")

                # Find corresponding tool message
                tool_message = None
                for m in messages:
                    if hasattr(m, "name") and m.name == tool_name:
                        tool_message = m
                        break

                return tool_name, tool_call, tool_message

        return None, None, None

    def _find_tool_in_engine(self, engine: Any, tool_name: str) -> type | None:
        """Find tool class in engine."""
        if not engine:
            return None

        # Check all possible tool sources
        candidates = []

        for attr_name in ["tools", "schemas", "pydantic_tools"]:
            if hasattr(engine, attr_name):
                attr_value = getattr(engine, attr_name)
                if attr_value:
                    candidates.extend(attr_value)

        # Check structured_output_model
        if (
            hasattr(engine, "structured_output_model")
            and engine.structured_output_model
        ):
            candidates.append(engine.structured_output_model)

        # Find matching tool
        for candidate in candidates:
            if getattr(candidate, "__name__", None) == tool_name:
                return candidate

        return None

    def _parse_tool_content(self, content: Any, tool_class: type) -> Any:
        """Parse tool content into model."""
        import json

        if isinstance(content, tool_class):
            return content

        # Try JSON parsing
        if isinstance(content, str):
            try:
                json_data = json.loads(content)
                return tool_class.model_validate(json_data)
            except BaseException:
                pass

        # Try dict validation
        if isinstance(content, dict):
            try:
                return tool_class.model_validate(content)
            except BaseException:
                pass

        return {"content": content, "parse_error": "Could not parse"}

    def _determine_field_name(self, tool_class: type, tool_name: str) -> str:
        """Determine field name for parsed result."""
        # Try to use naming utilities
        try:
            from haive.core.schema.field_utils import get_field_info_from_model

            field_info = get_field_info_from_model(tool_class)
            return field_info["field_name"]
        except BaseException:
            pass

        # Fallback to simple naming
        return (
            tool_name.lower().replace("response", "").replace("result", "").strip()
            or "parsed_result"
        )


class StatefulToolNodeConfig(StatefulNodeConfig):
    """Stateful tool node that discovers tools from state."""

    node_type: NodeType = Field(default=NodeType.TOOL)

    # Default routing keys
    routing_prefix: str = Field(default="tool_")

    # Default fallbacks
    fallback_routing: dict[str, str] = Field(
        default_factory=lambda: {"agent_node": "agent", "default": "END"}
    )

    def execute_stateful_logic(
        self, state: StateLike, config: ConfigLike | None = None
    ) -> Command:
        """Execute tool logic with dynamic discovery."""
        # Discover routing destination
        agent_node = self.discover_routing_destination(state, "agent_node")

        # Discover engine for tool execution
        engine = self.discover_engine(state)

        # Get messages and extract tool calls
        messages = self._get_state_value(state, "messages")
        if not messages:
            return Command(goto=agent_node or "END")

        # Execute tools and create tool messages
        tool_messages = self._execute_tools(messages, engine)

        return Command(update={"messages": tool_messages}, goto=agent_node or "END")

    def _execute_tools(self, messages: list[BaseMessage], engine: Any) -> list[Any]:
        """Execute tools and return tool messages."""
        from langchain_core.messages import ToolMessage

        tool_messages = []

        # Find AI messages with tool calls
        for msg in reversed(messages):
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name")
                    tool_args = tool_call.get("args", {})
                    tool_id = tool_call.get("id")

                    # Find and execute tool
                    try:
                        tool = self._find_tool_in_engine(engine, tool_name)
                        if tool:
                            result = tool.invoke(tool_args)
                            tool_messages.append(
                                ToolMessage(
                                    content=str(result),
                                    tool_call_id=tool_id,
                                    name=tool_name,
                                )
                            )
                        else:
                            tool_messages.append(
                                ToolMessage(
                                    content=f"Tool not found: {tool_name}",
                                    tool_call_id=tool_id,
                                    name=tool_name,
                                )
                            )
                    except Exception as e:
                        tool_messages.append(
                            ToolMessage(
                                content=f"Tool error: {e!s}",
                                tool_call_id=tool_id,
                                name=tool_name,
                            )
                        )

                break  # Only process last AI message

        return tool_messages

    def _find_tool_in_engine(self, engine: Any, tool_name: str) -> Any | None:
        """Find executable tool in engine."""
        if not engine:
            return None

        # Check tools
        if hasattr(engine, "tools") and engine.tools:
            for tool in engine.tools:
                if getattr(tool, "name", None) == tool_name:
                    return tool

        return None
