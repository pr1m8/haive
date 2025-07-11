import logging
from typing import Any, Dict, List, Optional

from langchain_core.tools import BaseTool
from pydantic import Field, computed_field, model_validator

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from haive.core.schema.prebuilt.messages.messages_with_token_usage import (
    MessagesStateWithTokenUsage,
)

logger = logging.getLogger(__name__)


class ToolState(ToolRouteMixin, MessagesStateWithTokenUsage):
    """State schema for tool-based agents with tool management and token tracking.

    ToolState combines ToolRouteMixin and MessagesStateWithTokenUsage to provide specialized
    functionality for agents that use tools. It provides robust tool management infrastructure
    for tool registration, categorization, routing, and execution while maintaining token
    tracking for all messages.

    This schema serves as the foundation for tool-using agent states in the Haive framework,
    providing seamless integration with various tool types including LangChain tools, Pydantic
    models, and callable functions. It automatically categorizes tools by type, maintains tool
    metadata, and tracks tool relationships while providing LLM-specific features like context
    length awareness and token usage thresholds.

    Key features include:

    - Automatic tool registration and synchronization
    - Automatic tool synchronization from class-level engines (__engines__)
    - Tool categorization by type (LangChain tool, Pydantic model, function, etc.)
    - Tool routing based on tool type and characteristics
    - Support for structured tool inputs and outputs with Pydantic validation
    - Tool schema extraction and management
    - Tool execution tracking and result handling
    - Compatible with all standard tool formats used in LLM agents

    The schema follows the same tool routes pattern as AugLLMConfig for consistency,
    making it easier to work with both components in the same application. It's the
    default base class used by SchemaComposer when tool usage is detected in the
    components being composed.

    This class is commonly used as a base class for specialized agent states that
    need both conversation and tool capabilities, particularly for task-oriented
    agents that interact with external systems or perform complex operations.

    Tool Synchronization:
    --------------------
    Tools are synchronized from multiple sources:

    1. Instance-level engines: The setup_engines_and_tools validator finds engines
       in instance fields and syncs their tools.

    2. Class-level engines: The model_post_init method makes class engines (__engines__)
       available on instances and syncs their tools.

    This ensures tools are properly synchronized regardless of whether engines are
    stored at the class level by SchemaComposer or added directly to instances.
    """

    # Tool-related fields - inherited from ToolRouteMixin
    # tools: List[Any] - provided by ToolRouteMixin
    # tool_routes: Dict[str, str] - provided by ToolRouteMixin
    content: Optional[str] = Field(default=None, description="Content field")
    output_schemas: Dict[str, Any] = Field(
        default_factory=dict, description="Output schemas for tools"
    )

    # Tool routing configuration
    engine_route_config: Dict[str, List[str]] = Field(
        default_factory=lambda: {
            "llm": ["langchain_tool", "function", "pydantic_model"],
            "aug_llm": ["langchain_tool", "function", "pydantic_model"],
            "retriever": ["retriever"],
            "parser": ["pydantic_model"],
        },
        description="Configuration of which tool routes each engine type accepts",
    )

    @model_validator(mode="after")
    def sync_tools_and_update_routes(self) -> "ToolState":
        """
        Sync tools from engines and update tool routes after model creation.

        This runs after the parent validators, so engines and tool routes are already set up.
        """
        # Call parent validators first
        super().auto_track_all_tokens()  # From MessagesStateWithTokenUsage
        super()._validate_and_process_tools()  # From ToolRouteMixin

        # Sync tools from class-level engines if they haven't been synced yet
        if hasattr(self.__class__, "engines") and not self.tools:
            logger.debug(
                f"Initial tool sync from class engines for {self.__class__.__name__}"
            )
            self._sync_tools_from_class_engines()

        # Now sync tool routes based on the current tools
        self._sync_tool_routes()

        # Make sure to sync tools to appropriate engines based on routes
        self._sync_tools_to_engines_by_route()

        return self

    def _sync_tools_from_class_engines(self) -> None:
        """Sync tools from class-level engines to state."""
        if not hasattr(self.__class__, "engines"):
            return

        for engine_name, engine in self.__class__.engines.items():
            if hasattr(engine, "tools") and engine.tools:
                logger.debug(
                    f"Syncing {len(engine.tools)} tools from class engine '{engine_name}'"
                )
                for tool in engine.tools:
                    if tool not in self.tools:
                        self.tools.append(tool)
                        tool_name = getattr(tool, "name", str(tool))
                        logger.debug(
                            f"Added tool '{tool_name}' from class engine '{engine_name}'"
                        )

    def _sync_tools_to_engines_by_route(self) -> None:
        """
        Sync tools to appropriate engines based on their routes and engine types.
        Only syncs tools to engines that can handle their specific route type.
        """
        # Sync to class-level engines
        if hasattr(self.__class__, "engines"):
            for engine_name, engine in self.__class__.engines.items():
                if hasattr(engine, "tools"):
                    engine_type = getattr(engine, "engine_type", "unknown")
                    self._sync_tools_to_engine_by_route(
                        engine, engine_name, engine_type, is_class_level=True
                    )

        # Sync to instance-level engines
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue

            if hasattr(field_value, "engine_type") and hasattr(field_value, "tools"):
                engine_name = getattr(field_value, "name", field_name)
                engine_type = getattr(field_value, "engine_type", "unknown")
                self._sync_tools_to_engine_by_route(
                    field_value, engine_name, engine_type, is_class_level=False
                )

    def _sync_tools_to_engine_by_route(
        self,
        engine: Any,
        engine_name: str,
        engine_type: Any,
        is_class_level: bool = False,
    ) -> None:
        """
        Sync tools to a specific engine based on routing compatibility.

        Args:
            engine: The engine object
            engine_name: Name of the engine
            engine_type: Type of the engine (e.g., 'llm', 'retriever', etc.)
            is_class_level: Whether this is a class-level or instance-level engine
        """
        engine_tools = getattr(engine, "tools", [])
        level_str = "class" if is_class_level else "instance"

        # Convert engine_type to string if it's an enum
        if hasattr(engine_type, "value"):
            engine_type_str = engine_type.value
        else:
            engine_type_str = str(engine_type)

        for tool in self.tools:
            tool_name = getattr(tool, "name", str(tool))
            tool_route = self.tool_routes.get(tool_name, self._get_tool_route(tool))

            # Check if this tool should be synced to this engine
            if self._should_sync_tool_to_engine(tool_route, engine_type_str, engine):
                if tool not in engine_tools:
                    logger.debug(
                        f"Syncing tool '{tool_name}' (route: {tool_route}) to {level_str} engine '{engine_name}' (type: {engine_type_str})"
                    )
                    engine_tools.append(tool)

                    # Update engine tool_routes if it has them
                    if hasattr(engine, "tool_routes"):
                        engine.tool_routes[tool_name] = tool_route
            else:
                logger.debug(
                    f"Skipping tool '{tool_name}' (route: {tool_route}) for {level_str} engine '{engine_name}' (type: {engine_type_str}) - route mismatch"
                )

    def _should_sync_tool_to_engine(
        self, tool_route: str, engine_type: str, engine: Any
    ) -> bool:
        """
        Determine if a tool should be synced to an engine based on routing logic.

        Args:
            tool_route: The route type of the tool (e.g., 'langchain_tool', 'pydantic_model', etc.)
            engine_type: The type of the engine (e.g., 'llm', 'retriever', etc.)
            engine: The actual engine object

        Returns:
            True if the tool should be synced to this engine
        """
        # If engine has specific route preferences, check those first
        if hasattr(engine, "supported_tool_routes"):
            return tool_route in engine.supported_tool_routes

        # Use configured route mapping
        if engine_type in self.engine_route_config:
            return tool_route in self.engine_route_config[engine_type]

        # If engine has existing tool_routes, it probably accepts tools
        if hasattr(engine, "tool_routes"):
            return True

        # Default: don't sync unless we're sure
        return False

    def configure_engine_routes(self, engine_type: str, routes: List[str]) -> None:
        """
        Configure which tool routes an engine type should accept.

        Args:
            engine_type: The engine type (e.g., 'llm', 'retriever', etc.)
            routes: List of tool routes this engine type should accept
        """
        self.engine_route_config[engine_type] = routes
        logger.debug(
            f"Configured engine type '{engine_type}' to accept routes: {routes}"
        )

        # Re-sync tools with new configuration
        self._sync_tools_to_engines_by_route()

    def add_engine_route(self, engine_type: str, route: str) -> None:
        """
        Add a tool route to an engine type's accepted routes.

        Args:
            engine_type: The engine type
            route: The tool route to add
        """
        if engine_type not in self.engine_route_config:
            self.engine_route_config[engine_type] = []

        if route not in self.engine_route_config[engine_type]:
            self.engine_route_config[engine_type].append(route)
            logger.debug(f"Added route '{route}' to engine type '{engine_type}'")

            # Re-sync tools with new configuration
            self._sync_tools_to_engines_by_route()

    def remove_engine_route(self, engine_type: str, route: str) -> None:
        """
        Remove a tool route from an engine type's accepted routes.

        Args:
            engine_type: The engine type
            route: The tool route to remove
        """
        if (
            engine_type in self.engine_route_config
            and route in self.engine_route_config[engine_type]
        ):
            self.engine_route_config[engine_type].remove(route)
            logger.debug(f"Removed route '{route}' from engine type '{engine_type}'")

            # Re-sync tools with new configuration
            self._sync_tools_to_engines_by_route()

    def _sync_tool_routes(self) -> None:
        """Synchronize tool_routes with current tools - matches AugLLMConfig pattern."""
        new_routes = {}

        for i, tool in enumerate(self.tools):
            # Determine tool name
            tool_name = self._get_tool_name(tool, i)

            # Determine route/type - matching AugLLMConfig categorization
            route = self._get_tool_route(tool)

            new_routes[tool_name] = route
            logger.debug(f"Mapped tool '{tool_name}' to route '{route}'")

        self.tool_routes = new_routes

    def _get_tool_name(self, tool: Any, index: int) -> str:
        """Extract tool name from various possible attributes."""
        # Use the mixin's method if available
        if hasattr(super(), "_get_tool_name"):
            return super()._get_tool_name(tool, index)

        # Fallback to local implementation
        if hasattr(tool, "name"):
            return tool.name
        elif isinstance(tool, type) and hasattr(tool, "__name__"):
            return tool.__name__
        elif hasattr(tool, "__name__"):
            return tool.__name__
        else:
            return f"tool_{index}"

    def _get_tool_route(self, tool: Any) -> str:
        """Determine the route type for a tool."""
        if isinstance(tool, type) and self._is_basemodel_subclass(tool):
            return "pydantic_model"
        elif isinstance(tool, BaseTool) or (
            isinstance(tool, type) and issubclass(tool, BaseTool)
        ):
            return "langchain_tool"
        elif callable(tool):
            return "function"
        else:
            return "unknown"

    def _is_basemodel_subclass(self, tool: Any) -> bool:
        """Check if tool is a BaseModel subclass."""
        try:
            from pydantic import BaseModel

            return isinstance(tool, type) and issubclass(tool, BaseModel)
        except Exception:
            return False

    @computed_field
    @property
    def tool_types(self) -> Dict[str, str]:
        """
        Computed field for backward compatibility.

        Maps the new tool_routes to the old tool_types interface:
        - pydantic_model → parse_output
        - langchain_tool → tool_node
        - function → tool_node
        - unknown → tool_node
        """
        legacy_mapping = {
            "pydantic_model": "parse_output",
            "langchain_tool": "tool_node",
            "function": "tool_node",
            "unknown": "tool_node",
        }

        # Handle case where tool_routes might not exist in composed schemas
        if not hasattr(self, "tool_routes"):
            return {}

        return {
            tool_name: legacy_mapping.get(route, "tool_node")
            for tool_name, route in self.tool_routes.items()
        }

    def add_tool(
        self,
        tool: Any,
        route: Optional[str] = None,
        target_engine: Optional[str] = None,
    ) -> None:
        """
        Add a tool and update tool routes - matches AugLLMConfig pattern.
        Syncs to appropriate engines based on routing logic.

        Args:
            tool: Tool to add
            route: Optional explicit route/type (pydantic_model, langchain_tool, function, unknown)
            target_engine: Optional specific engine name to add tool to (bypasses routing logic)
        """
        if tool not in self.tools:
            self.tools.append(tool)

            # Determine tool name
            tool_name = self._get_tool_name(tool, len(self.tools))

            # Set route - use explicit route if provided, otherwise auto-determine
            if route:
                self.tool_routes[tool_name] = route
            else:
                self.tool_routes[tool_name] = self._get_tool_route(tool)

            logger.debug(
                f"Added tool '{tool_name}' with route '{self.tool_routes[tool_name]}'"
            )

            # Sync this new tool to engines
            if target_engine:
                self._sync_tool_to_specific_engine(tool, target_engine)
            else:
                self._sync_single_tool_to_engines(tool)

    def add_tool_to_engine(
        self, tool: Any, engine_name: str, route: Optional[str] = None
    ) -> None:
        """
        Add a tool to a specific engine, bypassing routing logic.

        Args:
            tool: Tool to add
            engine_name: Name of the engine to add tool to
            route: Optional explicit route/type
        """
        # Add to state tools if not already there
        if tool not in self.tools:
            self.tools.append(tool)

        # Determine tool name and route
        tool_name = self._get_tool_name(tool, len(self.tools))
        if route:
            self.tool_routes[tool_name] = route
        else:
            self.tool_routes[tool_name] = self._get_tool_route(tool)

        # Add to specific engine
        self._sync_tool_to_specific_engine(tool, engine_name)

    def _sync_tool_to_specific_engine(self, tool: Any, engine_name: str) -> None:
        """Sync a tool to a specific engine by name."""
        tool_name = getattr(tool, "name", str(tool))
        tool_route = self.tool_routes.get(tool_name, self._get_tool_route(tool))

        # Check class-level engines first
        if hasattr(self.__class__, "engines") and engine_name in self.__class__.engines:
            engine = self.__class__.engines[engine_name]
            if hasattr(engine, "tools"):
                engine_tools = getattr(engine, "tools", [])
                if tool not in engine_tools:
                    engine_tools.append(tool)
                    logger.debug(
                        f"Added tool '{tool_name}' to class engine '{engine_name}'"
                    )
                    if hasattr(engine, "tool_routes"):
                        engine.tool_routes[tool_name] = tool_route
                return

        # Check instance-level engines
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue
            if hasattr(field_value, "engine_type") and hasattr(field_value, "tools"):
                current_engine_name = getattr(field_value, "name", field_name)
                if current_engine_name == engine_name:
                    engine_tools = getattr(field_value, "tools", [])
                    if tool not in engine_tools:
                        engine_tools.append(tool)
                        logger.debug(
                            f"Added tool '{tool_name}' to instance engine '{engine_name}'"
                        )
                    return

        logger.warning(f"Engine '{engine_name}' not found for tool '{tool_name}'")

    def _sync_single_tool_to_engines(self, tool: Any) -> None:
        """Sync a single tool to appropriate engines based on routing logic."""
        tool_name = getattr(tool, "name", str(tool))
        tool_route = self.tool_routes.get(tool_name, self._get_tool_route(tool))

        # Sync to class-level engines
        if hasattr(self.__class__, "engines"):
            for engine_name, engine in self.__class__.engines.items():
                if hasattr(engine, "tools"):
                    engine_type = getattr(engine, "engine_type", "unknown")
                    engine_type_str = (
                        engine_type.value
                        if hasattr(engine_type, "value")
                        else str(engine_type)
                    )

                    if self._should_sync_tool_to_engine(
                        tool_route, engine_type_str, engine
                    ):
                        engine_tools = getattr(engine, "tools", [])
                        if tool not in engine_tools:
                            logger.debug(
                                f"Adding tool '{tool_name}' (route: {tool_route}) to class engine '{engine_name}' (type: {engine_type_str})"
                            )
                            engine_tools.append(tool)
                            # Update engine tool_routes if it has them
                            if hasattr(engine, "tool_routes"):
                                engine.tool_routes[tool_name] = tool_route
                    else:
                        logger.debug(
                            f"Skipping tool '{tool_name}' (route: {tool_route}) for class engine '{engine_name}' (type: {engine_type_str}) - route mismatch"
                        )

        # Sync to instance-level engines
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue

            if hasattr(field_value, "engine_type") and hasattr(field_value, "tools"):
                engine_name = getattr(field_value, "name", field_name)
                engine_type = getattr(field_value, "engine_type", "unknown")
                engine_type_str = (
                    engine_type.value
                    if hasattr(engine_type, "value")
                    else str(engine_type)
                )

                if self._should_sync_tool_to_engine(
                    tool_route, engine_type_str, field_value
                ):
                    engine_tools = getattr(field_value, "tools", [])
                    if tool not in engine_tools:
                        logger.debug(
                            f"Adding tool '{tool_name}' (route: {tool_route}) to instance engine '{engine_name}' (type: {engine_type_str})"
                        )
                        engine_tools.append(tool)
                else:
                    logger.debug(
                        f"Skipping tool '{tool_name}' (route: {tool_route}) for instance engine '{engine_name}' (type: {engine_type_str}) - route mismatch"
                    )

    def remove_tool(self, tool: Any) -> None:
        """
        Remove a tool and update tool routes.
        Also removes from all engines.

        Args:
            tool: Tool to remove
        """
        if tool in self.tools:
            self.tools.remove(tool)

            # Find and remove from tool_routes
            tool_name = None
            for i, t in enumerate(self.tools):
                if t == tool:
                    tool_name = self._get_tool_name(t, i)
                    break

            if tool_name and tool_name in self.tool_routes:
                del self.tool_routes[tool_name]
                logger.debug(f"Removed tool '{tool_name}'")

            # Remove from all engines
            self._remove_tool_from_engines(tool)

            # Re-sync to ensure consistency
            self._sync_tool_routes()

    def _remove_tool_from_engines(self, tool: Any) -> None:
        """Remove a tool from all engines."""
        tool_name = getattr(tool, "name", str(tool))

        # Remove from class-level engines
        if hasattr(self.__class__, "engines"):
            for engine_name, engine in self.__class__.engines.items():
                if hasattr(engine, "tools"):
                    engine_tools = getattr(engine, "tools", [])
                    if tool in engine_tools:
                        engine_tools.remove(tool)
                        logger.debug(
                            f"Removed tool '{tool_name}' from class engine '{engine_name}'"
                        )
                        # Remove from engine tool_routes if it has them
                        if (
                            hasattr(engine, "tool_routes")
                            and tool_name in engine.tool_routes
                        ):
                            del engine.tool_routes[tool_name]

        # Remove from instance-level engines
        for field_name, field_value in self.__dict__.items():
            if field_value is None:
                continue

            if hasattr(field_value, "engine_type") and hasattr(field_value, "tools"):
                engine_name = getattr(field_value, "name", field_name)
                engine_tools = getattr(field_value, "tools", [])

                if tool in engine_tools:
                    engine_tools.remove(tool)
                    logger.debug(
                        f"Removed tool '{tool_name}' from instance engine '{engine_name}'"
                    )

    def get_tool_by_name(self, tool_name: str) -> Optional[Any]:
        """
        Get a tool by its name.

        Args:
            tool_name: Name of tool to retrieve

        Returns:
            Tool if found, None otherwise
        """
        for i, tool in enumerate(self.tools):
            if self._get_tool_name(tool, i) == tool_name:
                return tool
        return None

    def get_tools_by_route(self, route: str) -> List[Any]:
        """
        Get all tools of a specific route type.

        Args:
            route: Route type to retrieve (pydantic_model, langchain_tool, function, unknown)

        Returns:
            List of tools of the specified route type
        """
        result = []
        for tool_name, tool_route in self.tool_routes.items():
            if tool_route == route:
                tool = self.get_tool_by_name(tool_name)
                if tool:
                    result.append(tool)
        return result

    def get_tools_by_type(self, tool_type: str) -> List[Any]:
        """
        Get all tools of a specific type (legacy interface).

        Args:
            tool_type: Type of tools to retrieve (parse_output, tool_node)

        Returns:
            List of tools of the specified type
        """
        # Convert legacy type to routes
        type_to_routes = {
            "parse_output": ["pydantic_model"],
            "tool_node": ["langchain_tool", "function", "unknown"],
        }

        routes = type_to_routes.get(tool_type, [])
        result = []
        for route in routes:
            result.extend(self.get_tools_by_route(route))
        return result

    def has_tool_route(self, route: str) -> bool:
        """
        Check if any tools of a specific route exist.

        Args:
            route: Route to check for (pydantic_model, langchain_tool, function, unknown)

        Returns:
            True if any tools of this route exist
        """
        return route in self.tool_routes.values()

    def has_tool_type(self, tool_type: str) -> bool:
        """
        Check if any tools of a specific type exist (legacy interface).

        Args:
            tool_type: Type to check for (parse_output, tool_node)

        Returns:
            True if any tools of this type exist
        """
        return tool_type in self.tool_types.values()

    def refresh_tool_routes(self) -> None:
        """
        Manually refresh tool routes if needed.
        """
        self._sync_tool_routes()

    def update_tool_types(self) -> None:
        """
        Legacy interface - now calls refresh_tool_routes.
        """
        self.refresh_tool_routes()

    def get_tool_route(self, tool_name: str) -> Optional[str]:
        """
        Get the route of a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool route if found (pydantic_model, langchain_tool, function, unknown), None otherwise
        """
        return self.tool_routes.get(tool_name)

    def get_tool_type(self, tool_name: str) -> Optional[str]:
        """
        Get the type of a specific tool (legacy interface).

        Args:
            tool_name: Name of the tool

        Returns:
            Tool type if found (parse_output, tool_node), None otherwise
        """
        return self.tool_types.get(tool_name)
