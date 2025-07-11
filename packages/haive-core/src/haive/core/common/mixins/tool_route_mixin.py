"""Tool routing mixin for managing tool destinations and metadata.

This module provides a mixin for managing tool routes and related metadata in
configuration classes. It enables mapping tool names to their types or destinations,
keeping track of metadata, and provides utilities for creating tools from configs.

Usage:
    ```python
    from pydantic import BaseModel
    from haive.core.common.mixins import ToolRouteMixin

    class AgentConfig(ToolRouteMixin, BaseModel):
        name: str
        description: str

        def _create_tool_implementation(self, name, description, **kwargs):
            # Custom tool creation logic
            return SomeTool(name=name, description=description)

    # Create config with tool routes
    config = AgentConfig(
        name="MyAgent",
        description="Agent configuration"
    )

    # Set tool routes
    config.set_tool_route("search", "retriever", {"source": "web"})
    config.set_tool_route("math", "function", {"language": "python"})

    # Create a tool
    search_tool = config.to_tool(name="search", description="Web search tool")

    # Get routes by type
    retriever_tools = config.list_tools_by_route("retriever")
    ```
"""

import inspect
import logging
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Sequence,
    Tuple,
    Type,
    Union,
    get_type_hints,
)

from pydantic import BaseModel, Field, field_validator, model_validator
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.tree import Tree

logger = logging.getLogger(__name__)
console = Console()


class ToolRouteMixin(BaseModel):
    """Enhanced mixin for managing tools, routes, and converting configurations to tools.

    This mixin provides functionality for:
    - Setting and managing tool routes (mapping tool names to types/destinations)
    - Storing and retrieving tool metadata
    - Supporting tools as dict with string keys for tool lists
    - Supporting routed tools with before validators for tuple handling
    - Generating tools from configurations
    - Visualizing tool routing information

    Tool routes define where a tool request should be directed, such as to a
    specific retriever, model, or function. This helps implement routing logic
    in agents and other tool-using components.

    Attributes:
        tool_routes: Dictionary mapping tool names to their routes/types.
        tool_metadata: Dictionary with additional metadata for each tool.
        tools_dict: Dictionary mapping tool category strings to lists of tools.
        routed_tools: List of tuples containing (tool, route) pairs.
        before_tool_validator: Optional callable to validate tools before routing.
    """

    # Tool routes mapping tool names to their types/destinations
    tool_routes: dict[str, str] = Field(
        default_factory=dict, description="Mapping of tool names to their routes/types"
    )

    # Tool metadata for enhanced management
    tool_metadata: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Metadata for each tool"
    )

    # Enhanced tool management
    tools_dict: dict[str, list[Any]] = Field(
        default_factory=dict,
        description="Dictionary mapping tool category strings to lists of tools",
    )

    routed_tools: list[tuple[Any, str]] = Field(
        default_factory=list,
        description="List of (tool, route) tuples for explicit routing",
    )

    before_tool_validator: Callable[[Any], Any] | None = Field(
        default=None,
        description="Optional callable to validate tools before routing",
        exclude=True,  # Exclude from serialization
    )

    # NEW: Actual tool storage
    tools: list[Any] = Field(
        default_factory=list,
        description="List of tools (BaseTool, StructuredTool, Pydantic models, callables)",
    )

    # NEW: Tool instance mapping for quick lookup
    tool_instances: dict[str, Any] = Field(
        default_factory=dict,
        description="Mapping of tool names to actual tool instances",
    )

    def set_tool_route(
        self, tool_name: str, route: str, metadata: dict[str, Any] | None = None
    ) -> "ToolRouteMixin":
        """Set a tool route with optional metadata.

        This method defines where a tool request should be routed, along
        with optional metadata to inform the routing decision.

        Args:
            tool_name: Name of the tool.
            route: Route/type for the tool (e.g., 'retriever', 'pydantic_model', 'function').
            metadata: Optional metadata for the tool.

        Returns:
            Self for method chaining.
        """
        self.tool_routes[tool_name] = route

        if metadata:
            if not hasattr(self, "tool_metadata"):
                self.tool_metadata = {}
            self.tool_metadata[tool_name] = metadata

        logger.debug(f"Set tool route: {tool_name} -> {route}")
        if metadata:
            logger.debug(f"  Metadata: {metadata}")

        return self

    def get_tool_route(self, tool_name: str) -> str | None:
        """Get the route for a specific tool.

        Args:
            tool_name: Name of the tool to look up.

        Returns:
            The route string if found, None otherwise.
        """
        return self.tool_routes.get(tool_name)

    def get_tool_metadata(self, tool_name: str) -> dict[str, Any] | None:
        """Get metadata for a specific tool.

        Args:
            tool_name: Name of the tool to look up.

        Returns:
            Dictionary of metadata if found, None otherwise.
        """
        if not hasattr(self, "tool_metadata"):
            return None
        return self.tool_metadata.get(tool_name)

    def list_tools_by_route(self, route: str) -> list[str]:
        """Get all tool names for a specific route.

        This method finds all tools that are routed to a specific destination.

        Args:
            route: The route to search for.

        Returns:
            List of tool names with the matching route.
        """
        return [name for name, r in self.tool_routes.items() if r == route]

    def remove_tool_route(self, tool_name: str) -> "ToolRouteMixin":
        """Remove a tool route and its metadata.

        Args:
            tool_name: Name of the tool to remove.

        Returns:
            Self for method chaining.
        """
        if tool_name in self.tool_routes:
            del self.tool_routes[tool_name]

        if hasattr(self, "tool_metadata") and tool_name in self.tool_metadata:
            del self.tool_metadata[tool_name]

        logger.debug(f"Removed tool route: {tool_name}")
        return self

    def update_tool_routes(self, routes: dict[str, str]) -> "ToolRouteMixin":
        """Update multiple tool routes at once.

        Args:
            routes: Dictionary mapping tool names to routes.

        Returns:
            Self for method chaining.
        """
        self.tool_routes.update(routes)
        logger.debug(f"Updated tool routes: {routes}")
        return self

    def clear_tool_routes(self) -> "ToolRouteMixin":
        """Clear all tool routes and metadata.

        Returns:
            Self for method chaining.
        """
        self.tool_routes.clear()
        if hasattr(self, "tool_metadata"):
            self.tool_metadata.clear()
        logger.debug("Cleared all tool routes")
        return self

    @model_validator(mode="after")
    def _validate_and_process_tools(self) -> "ToolRouteMixin":
        """Process tools_dict and routed_tools into tool_routes after initialization."""
        # Process tools_dict into tool_routes
        self._process_tools_dict()

        # Process routed_tools into tool_routes
        self._process_routed_tools()

        return self

    def _process_tools_dict(self) -> None:
        """Process tools_dict into individual tool routes."""
        for category, tool_list in self.tools_dict.items():
            for i, tool in enumerate(tool_list):
                # Apply validator if provided
                if self.before_tool_validator:
                    try:
                        tool = self.before_tool_validator(tool)
                    except Exception as e:
                        logger.warning(
                            f"Tool validation failed for {category}[{i}]: {e}"
                        )
                        continue

                # Generate tool name
                tool_name = self._generate_tool_name(tool, category, i)

                # Determine route and metadata
                route, metadata = self._analyze_tool(tool)
                metadata = metadata or {}
                metadata.update(
                    {
                        "category": category,
                        "index_in_category": i,
                        "source": "tools_dict",
                    }
                )

                # Set the route
                self.set_tool_route(tool_name, route, metadata)

    def _process_routed_tools(self) -> None:
        """Process routed_tools tuples into tool routes."""
        for i, (tool, route) in enumerate(self.routed_tools):
            # Apply validator if provided
            if self.before_tool_validator:
                try:
                    tool = self.before_tool_validator(tool)
                except Exception as e:
                    logger.warning(f"Tool validation failed for routed_tools[{i}]: {e}")
                    continue

            # Generate tool name
            tool_name = self._generate_tool_name(tool, f"routed_{route}", i)

            # Get metadata from tool analysis
            _, metadata = self._analyze_tool(tool)
            metadata = metadata or {}
            metadata.update(
                {
                    "explicit_route": route,
                    "index_in_routed": i,
                    "source": "routed_tools",
                }
            )

            # Set the route (use explicit route)
            self.set_tool_route(tool_name, route, metadata)

    def _generate_tool_name(self, tool: Any, prefix: str, index: int) -> str:
        """Generate a unique tool name for a tool."""
        # Try to get name from tool
        if hasattr(tool, "name") and tool.name:
            base_name = tool.name
        elif isinstance(tool, type) and hasattr(tool, "__name__"):
            base_name = tool.__name__
        else:
            base_name = f"tool_{index}"

        # Create prefixed name
        return f"{prefix}_{base_name}" if prefix else base_name

    def _analyze_tool(self, tool: Any) -> tuple[str, dict[str, Any] | None]:
        """Analyze a tool to determine its route and metadata."""
        metadata = {}

        if isinstance(tool, type) and issubclass(tool, BaseModel):
            route = "pydantic_model"
            metadata = {
                "class_name": tool.__name__,
                "module": getattr(tool, "__module__", "unknown"),
                "tool_type": "pydantic_model",
            }
            # Check if it has explicitly defined __call__ method (executable tool)
            # Only consider it executable if __call__ is defined in the class itself
            has_explicit_call = (
                "__call__" in tool.__dict__ if hasattr(tool, "__dict__") else False
            )
            if has_explicit_call and callable(tool.__call__):
                metadata["is_executable"] = True
                route = "pydantic_tool"
            else:
                metadata["is_executable"] = False
        elif hasattr(tool, "__class__") and "BaseTool" in str(tool.__class__.__mro__):
            route = "langchain_tool"
            metadata = {
                "tool_type": "BaseTool",
                "is_instance": not isinstance(tool, type),
            }
        elif callable(tool):
            route = "function"
            metadata = {
                "callable_type": type(tool).__name__,
                "has_annotations": hasattr(tool, "__annotations__"),
            }
            # Enhanced callable analysis
            metadata.update(self._get_callable_metadata(tool))
        else:
            route = "unknown"
            metadata = {"original_type": type(tool).__name__}

        return route, metadata

    def _get_callable_metadata(self, callable_obj: Callable) -> dict[str, Any]:
        """Extract enhanced metadata from callable objects.

        Args:
            callable_obj: Callable to analyze

        Returns:
            Dictionary of metadata
        """
        metadata = {}

        try:
            # Check if async
            metadata["is_async"] = inspect.iscoroutinefunction(callable_obj)

            # Get signature
            sig = inspect.signature(callable_obj)
            metadata["parameters"] = list(sig.parameters.keys())
            metadata["parameter_count"] = len(sig.parameters)

            # Check for type hints
            try:
                hints = get_type_hints(callable_obj)
                metadata["has_type_hints"] = bool(hints)
                metadata["has_return_type"] = "return" in hints
            except Exception:
                metadata["has_type_hints"] = False
                metadata["has_return_type"] = False

            # Determine callable kind
            if inspect.ismethod(callable_obj):
                metadata["callable_kind"] = "method"
            elif inspect.isfunction(callable_obj):
                metadata["callable_kind"] = "function"
            elif (
                hasattr(callable_obj, "__name__")
                and callable_obj.__name__ == "<lambda>"
            ):
                metadata["callable_kind"] = "lambda"
            else:
                metadata["callable_kind"] = "callable_object"

        except Exception as e:
            logger.debug(f"Error analyzing callable: {e}")

        return metadata

    def add_tools_to_category(
        self, category: str, tools: list[Any]
    ) -> "ToolRouteMixin":
        """Add tools to a specific category in tools_dict."""
        if category not in self.tools_dict:
            self.tools_dict[category] = []

        self.tools_dict[category].extend(tools)

        # Reprocess to update routes
        self._process_tools_dict()

        logger.debug(f"Added {len(tools)} tools to category '{category}'")
        return self

    def add_routed_tool(self, tool: Any, route: str) -> "ToolRouteMixin":
        """Add a single tool with explicit route."""
        self.routed_tools.append((tool, route))

        # Reprocess to update routes
        self._process_routed_tools()

        logger.debug(f"Added routed tool to route '{route}'")
        return self

    def set_tool_route_for_existing(
        self, tool_identifier: str, new_route: str
    ) -> "ToolRouteMixin":
        """Set or update the route for an existing tool by name or partial match.

        Args:
            tool_identifier: Tool name or partial name to match
            new_route: New route to assign to the tool

        Returns:
            Self for method chaining.
        """
        # Find matching tool names
        matching_tools = [
            name
            for name in self.tool_routes
            if tool_identifier in name or name == tool_identifier
        ]

        if not matching_tools:
            logger.warning(f"No tools found matching identifier '{tool_identifier}'")
            return self

        for tool_name in matching_tools:
            # Get existing metadata and update it
            metadata = self.get_tool_metadata(tool_name) or {}
            metadata["route_updated"] = True
            metadata["previous_route"] = self.tool_routes[tool_name]

            self.set_tool_route(tool_name, new_route, metadata)
            logger.debug(
                f"Updated route for '{tool_name}': {metadata['previous_route']} -> {new_route}"
            )

        return self

    def get_tools_by_category(self, category: str) -> list[Any]:
        """Get all tools in a specific category."""
        return self.tools_dict.get(category, [])

    def get_all_tools_flat(self) -> list[Any]:
        """Get all tools from tools_dict and routed_tools as a flat list."""
        all_tools = []

        # Add tools from tools_dict
        for tool_list in self.tools_dict.values():
            all_tools.extend(tool_list)

        # Add tools from routed_tools
        for tool, _ in self.routed_tools:
            all_tools.append(tool)

        return all_tools

    def add_tools_from_list(
        self, tools: list[Any | tuple[Any, str]], clear_existing: bool = False
    ) -> "ToolRouteMixin":
        """Add tools from a list to tool_routes without clearing existing routes.

        This method analyzes a list of tools and automatically creates
        appropriate routes based on their types. Supports both regular tools
        and tuples of (tool, route) for explicit routing.

        Args:
            tools: List of tools or (tool, route) tuples to analyze and create routes for.
            clear_existing: Whether to clear existing routes first.

        Returns:
            Self for method chaining.
        """
        if clear_existing:
            self.clear_tool_routes()

        for i, tool_item in enumerate(tools):
            # Check if this is a tuple (tool, route)
            if isinstance(tool_item, tuple) and len(tool_item) == 2:
                tool, explicit_route = tool_item
                # Apply validator if provided
                if self.before_tool_validator:
                    try:
                        tool = self.before_tool_validator(tool)
                    except Exception as e:
                        logger.warning(f"Tool validation failed for tools[{i}]: {e}")
                        continue

                # Generate tool name
                tool_name = self._generate_tool_name(
                    tool, f"explicit_{explicit_route}", i
                )

                # Get metadata from tool analysis
                _, metadata = self._analyze_tool(tool)
                metadata = metadata or {}
                metadata.update(
                    {
                        "explicit_route": explicit_route,
                        "index_in_tools": i,
                        "source": "tools_list_tuple",
                    }
                )

                # Set the route (use explicit route)
                self.set_tool_route(tool_name, explicit_route, metadata)
                continue

            # Regular tool processing
            tool = tool_item
            # Determine tool name
            if hasattr(tool, "name"):
                tool_name = tool.name
            elif isinstance(tool, type) and hasattr(tool, "__name__"):
                tool_name = tool.__name__
            else:
                tool_name = f"tool_{i}"

            # Determine route/type and metadata
            metadata = {}
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                route = "pydantic_model"
                metadata = {
                    "class_name": tool.__name__,
                    "module": getattr(tool, "__module__", "unknown"),
                    "tool_type": "pydantic_model",
                }
            elif hasattr(tool, "__class__") and "BaseTool" in str(
                tool.__class__.__mro__
            ):
                route = "langchain_tool"
                metadata = {
                    "tool_type": "BaseTool",
                    "is_instance": not isinstance(tool, type),
                }
            elif callable(tool):
                route = "function"
                metadata = {
                    "callable_type": type(tool).__name__,
                    "has_annotations": hasattr(tool, "__annotations__"),
                }
            else:
                route = "unknown"
                metadata = {"original_type": type(tool).__name__}

            # Set the route with metadata
            self.set_tool_route(tool_name, route, metadata)

        return self

    def sync_tool_routes_from_tools(self, tools: list[Any]) -> "ToolRouteMixin":
        """Synchronize tool_routes with a list of tools.

        This method analyzes a list of tools and automatically creates
        appropriate routes based on their types.

        Args:
            tools: List of tools to analyze and create routes for.

        Returns:
            Self for method chaining.
        """
        # Clear existing routes and start fresh
        return self.add_tools_from_list(tools, clear_existing=True)

    def to_tool(
        self,
        name: str | None = None,
        description: str | None = None,
        route: str | None = None,
        **kwargs,
    ) -> Any:
        """Convert this configuration to a tool.

        This method provides a base implementation for creating tools from
        configuration objects. Specific config classes should override the
        _create_tool_implementation method to provide custom tool creation logic.

        Args:
            name: Tool name (defaults to config name if available).
            description: Tool description (defaults to config description if available).
            route: Tool route/type to set.
            **kwargs: Additional kwargs for tool creation.

        Returns:
            A tool that can be used with LLMs.
        """
        # Get default name and description from config
        config_name = getattr(self, "name", None)
        config_description = getattr(self, "description", None)

        tool_name = name or config_name or f"tool_{id(self)}"
        tool_description = (
            description
            or config_description
            or f"Tool created from {type(self).__name__}"
        )

        # Set tool route if provided
        if route:
            self.set_tool_route(tool_name, route, kwargs.get("metadata"))

        # Call the specific implementation
        tool = self._create_tool_implementation(tool_name, tool_description, **kwargs)

        logger.debug(f"Created tool: {tool_name} ({type(tool).__name__})")
        return tool

    def _create_tool_implementation(self, name: str, description: str, **kwargs) -> Any:
        """Create the actual tool implementation.

        This method should be overridden by specific config types to provide
        custom tool creation logic. For example:
        - RetrieverConfig: Create retriever tools
        - LLMConfig: Create LLM function tools
        - Other configs: Create appropriate tools

        Args:
            name: Tool name.
            description: Tool description.
            **kwargs: Additional parameters for tool creation.

        Raises:
            NotImplementedError: If not implemented by the subclass.

        Returns:
            A tool instance when implemented by subclasses.
        """
        raise NotImplementedError(
            f"Tool creation not implemented for {type(self).__name__}. "
            f"Override _create_tool_implementation() to create tools from this config type."
        )

    def debug_tool_routes(self) -> "ToolRouteMixin":
        """Print debug information about tool routes.

        This method uses the Rich library to create a visual representation
        of the tool routes and metadata, including the new dict and routed tools.

        Returns:
            Self for method chaining.
        """
        console.print("\n" + "=" * 80)
        console.print("[bold blue]🛤️ ENHANCED TOOL ROUTES DEBUG[/bold blue]")
        console.print("=" * 80)

        # Show tools_dict structure
        if self.tools_dict:
            dict_tree = Tree("📁 [cyan]Tools Dict Categories[/cyan]")
            for category, tools in self.tools_dict.items():
                category_branch = dict_tree.add(
                    f"[green]{category}[/green] ({len(tools)} tools)"
                )
                for i, tool in enumerate(tools):
                    tool_name = self._generate_tool_name(tool, category, i)
                    category_branch.add(
                        f"{tool_name} [dim]({type(tool).__name__})[/dim]"
                    )
            console.print(dict_tree)

        # Show routed_tools structure
        if self.routed_tools:
            routed_tree = Tree("🎯 [cyan]Explicitly Routed Tools[/cyan]")
            for i, (tool, route) in enumerate(self.routed_tools):
                tool_name = self._generate_tool_name(tool, f"routed_{route}", i)
                routed_tree.add(
                    f"{tool_name} → [yellow]{route}[/yellow] [dim]({type(tool).__name__})[/dim]"
                )
            console.print(routed_tree)

        # Show computed tool routes
        if not self.tool_routes:
            console.print("[yellow]No tool routes configured[/yellow]")
            return self

        # Create a tree for routes
        routes_tree = Tree("🛤️ [cyan]Computed Tool Routes[/cyan]")

        # Group by route type
        route_groups = {}
        for tool_name, route in self.tool_routes.items():
            if route not in route_groups:
                route_groups[route] = []
            route_groups[route].append(tool_name)

        for route, tools in route_groups.items():
            route_branch = routes_tree.add(
                f"[yellow]{route}[/yellow] ({len(tools)} tools)"
            )
            for tool_name in tools:
                metadata = self.get_tool_metadata(tool_name)
                source = metadata.get("source", "unknown") if metadata else "unknown"
                category = metadata.get("category", "") if metadata else ""
                source_str = f"[dim]({source})"
                if category:
                    source_str = f"[dim]({source}:{category})"
                route_branch.add(f"{tool_name} {source_str}[/dim]")

        console.print(routes_tree)

        # Show metadata table if available
        if hasattr(self, "tool_metadata") and self.tool_metadata:
            metadata_table = Table(title="Tool Metadata Details", show_header=True)
            metadata_table.add_column("Tool", style="cyan")
            metadata_table.add_column("Source", style="green")
            metadata_table.add_column("Category/Route", style="yellow")
            metadata_table.add_column("Type", style="magenta")

            for tool_name, metadata in self.tool_metadata.items():
                source = metadata.get("source", "unknown")
                category = metadata.get("category", metadata.get("explicit_route", ""))
                tool_type = metadata.get(
                    "tool_type", metadata.get("original_type", "unknown")
                )
                metadata_table.add_row(tool_name, source, category, tool_type)

            console.print(metadata_table)

        console.print("=" * 80 + "\n")
        return self

    def add_tool(
        self,
        tool: Any,
        route: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> "ToolRouteMixin":
        """Add a tool with automatic routing and metadata.

        Args:
            tool: Tool instance to add
            route: Optional explicit route (auto-detected if not provided)
            metadata: Optional metadata for the tool

        Returns:
            Self for method chaining
        """
        # Get tool name
        tool_name = self._get_tool_name(tool, len(self.tools))

        # Add to tools list if not already there
        if tool not in self.tools:
            self.tools.append(tool)

        # Store tool instance
        self.tool_instances[tool_name] = tool

        # Determine route if not provided
        if route is None:
            route, auto_metadata = self._analyze_tool(tool)
            if metadata:
                metadata.update(auto_metadata or {})
            else:
                metadata = auto_metadata

        # Set route and metadata
        self.set_tool_route(tool_name, route, metadata)

        logger.debug(f"Added tool '{tool_name}' with route '{route}'")
        return self

    def get_tool(self, tool_name: str) -> Any | None:
        """Get a tool instance by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance or None if not found
        """
        return self.tool_instances.get(tool_name)

    def get_tools_by_route(self, route: str) -> list[Any]:
        """Get all tools with a specific route.

        Args:
            route: Route to filter by

        Returns:
            List of tools with that route
        """
        tools = []
        for name, tool_route in self.tool_routes.items():
            if tool_route == route:
                tool = self.get_tool(name)
                if tool:
                    tools.append(tool)
        return tools

    def clear_tools(self) -> "ToolRouteMixin":
        """Clear all tools and routes.

        Returns:
            Self for method chaining
        """
        self.tools.clear()
        self.tool_instances.clear()
        self.tool_routes.clear()
        self.tool_metadata.clear()
        logger.debug("Cleared all tools and routes")
        return self

    def update_tool_route(self, tool_name: str, new_route: str) -> "ToolRouteMixin":
        """Update an existing tool's route dynamically.

        Args:
            tool_name: Name of the tool to update
            new_route: New route to assign

        Returns:
            Self for method chaining
        """
        if tool_name not in self.tool_routes:
            logger.warning(f"Tool '{tool_name}' not found in routes")
            return self

        old_route = self.tool_routes[tool_name]
        self.tool_routes[tool_name] = new_route

        # Update metadata to track changes
        if tool_name not in self.tool_metadata:
            self.tool_metadata[tool_name] = {}

        self.tool_metadata[tool_name].update(
            {
                "route_updated": True,
                "previous_route": old_route,
            }
        )

        logger.debug(f"Updated route for '{tool_name}': {old_route} -> {new_route}")
        return self

    def _get_tool_name(self, tool: Any, index: int) -> str:
        """Get a standardized tool name for a tool.

        Args:
            tool: Tool instance to name
            index: Index/position of tool for fallback naming

        Returns:
            Standardized tool name
        """
        # Try to get name from tool
        if hasattr(tool, "name") and tool.name:
            return tool.name
        if isinstance(tool, type) and hasattr(tool, "__name__"):
            return tool.__name__
        return f"tool_{index}"
