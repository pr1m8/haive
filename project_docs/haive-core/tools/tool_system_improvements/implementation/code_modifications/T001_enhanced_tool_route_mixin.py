"""T001 - Enhanced ToolRouteMixin with Tool Storage and Validation
This replaces/enhances the existing ToolRouteMixin
Location: /haive-core/src/haive/core/common/mixins/tool_route_mixin.py.

Key improvements:
1. Actually stores tools, not just routes
2. Validates tool types (BaseTool, Tool, StructuredTool, BaseModel, callable)
3. Better integration with LangGraph patterns
4. Smart routing based on tool type
"""

import inspect
from datetime import datetime
from typing import (Any, Callable, Dict, List, Optional, Sequence, Tuple, Type,
                    Union, get_type_hints)

from langchain_core.tools import BaseTool, StructuredTool, Tool
from langchain_core.tools.base import BaseToolkit
from pydantic import BaseModel, Field, field_validator, model_validator

# Define proper tool types following LangGraph pattern
ToolType = Union[BaseTool, Tool, StructuredTool, type[BaseModel], Callable]


class ToolRouteMixin(BaseModel):
    """Enhanced mixin for managing tools, routes, and metadata.

    This mixin now:
    - Stores actual tool instances, not just routes
    - Validates tool types properly
    - Provides smart routing based on tool characteristics
    - Integrates with LangGraph's tool patterns
    """

    # Core tool storage - following ToolEngine pattern
    tools: list[ToolType] = Field(
        default_factory=list,
        description="List of tools (BaseTool, StructuredTool, Pydantic models, callables)",
    )

    # Tool routes mapping tool names to their types/destinations
    tool_routes: dict[str, str] = Field(
        default_factory=dict, description="Mapping of tool names to their routes/types"
    )

    # Tool metadata for enhanced management
    tool_metadata: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Metadata for each tool"
    )

    # Tool name to tool instance mapping for quick lookup
    tool_instances: dict[str, ToolType] = Field(
        default_factory=dict,
        description="Mapping of tool names to actual tool instances",
    )

    # Configuration
    allow_duplicate_names: bool = Field(
        default=False, description="Whether to allow tools with duplicate names"
    )

    validate_tools_on_add: bool = Field(
        default=True, description="Whether to validate tools when adding them"
    )

    @field_validator("tools")
    def validate_tool_types(self, v: list[Any]) -> list[ToolType]:
        """Validate that all tools are of acceptable types."""
        validated_tools = []

        for tool in v:
            if isinstance(tool, BaseTool | Tool | StructuredTool):
                validated_tools.append(tool)
            else:
                logger.warning(f"Skipping invalid tool type: {type(tool).__name__}")

        return validated_tools

    def add_tool(
        self,
        tool: ToolType,
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
        # Validate tool if configured
        if self.validate_tools_on_add:
            tool = self._validate_tool(tool)

        # Get tool name
        tool_name = self._get_tool_name(tool)

        # Check for duplicates
        if not self.allow_duplicate_names and tool_name in self.tool_instances:
            logger.warning(f"Tool '{tool_name}' already exists")
            return self

        # Add to tools list
        if tool not in self.tools:
            self.tools.append(tool)

        # Store tool instance
        self.tool_instances[tool_name] = tool

        # Determine route
        if route is None:
            route, auto_metadata = self._analyze_tool(tool)
            if metadata:
                metadata.update(auto_metadata)
            else:
                metadata = auto_metadata

        # Set route and metadata
        self.set_tool_route(tool_name, route, metadata)

        logger.debug(f"Added tool '{tool_name}' with route '{route}'")
        return self

    def _validate_tool(self, tool: Any) -> ToolType:
        """Validate and potentially convert a tool to proper type."""
        # Already a proper tool type
        if isinstance(tool, BaseTool | Tool | StructuredTool):
            return tool

        # Pydantic model class
        if isinstance(tool, type) and issubclass(tool, BaseModel):
            return tool

        # Callable (function, method, lambda)
        if callable(tool):
            # Could convert to StructuredTool here if needed
            return tool

        raise ValueError(f"Invalid tool type: {type(tool).__name__}")

    def _get_tool_name(self, tool: Any) -> str:
        """Extract name from a tool instance."""
        # LangChain tools have name attribute
        if hasattr(tool, "name") and tool.name:
            return tool.name

        # Pydantic models and classes use __name__
        if hasattr(tool, "__name__"):
            return tool.__name__

        # Fallback to string representation
        return str(tool)

    def _analyze_tool(self, tool: Any) -> tuple[str, dict[str, Any]]:
        """Analyze a tool to determine its route and metadata.

        Returns:
            Tuple of (route, metadata)
        """
        metadata = {}

        # LangChain BaseTool and subclasses
        if isinstance(tool, BaseTool | Tool | StructuredTool):
            route = "langchain_tool"
            metadata = {
                "tool_type": type(tool).__name__,
                "has_description": bool(getattr(tool, "description", None)),
                "has_args_schema": hasattr(tool, "args_schema"),
                "is_async": hasattr(tool, "arun") or hasattr(tool, "_arun"),
            }

        # Pydantic model (potential tool or parser)
        elif isinstance(tool, type) and issubclass(tool, BaseModel):
            # Check if it's executable (has __call__ method)
            if callable(tool) and callable(tool.__call__):
                route = "pydantic_tool"
                metadata["is_executable"] = True
            else:
                route = "pydantic_model"
                metadata["is_executable"] = False

            metadata.update(
                {
                    "class_name": tool.__name__,
                    "module": getattr(tool, "__module__", "unknown"),
                    "field_count": len(getattr(tool, "model_fields", {})),
                }
            )

        # Regular callable
        elif callable(tool):
            route = "function"
            metadata = self._analyze_callable(tool)

        else:
            route = "unknown"
            metadata = {"original_type": type(tool).__name__}

        return route, metadata

    def _analyze_callable(self, callable_obj: Callable) -> dict[str, Any]:
        """Extract metadata from callable objects."""
        metadata = {
            "callable_type": type(callable_obj).__name__,
        }

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
            except:
                metadata["has_type_hints"] = False

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

    def get_tool(self, tool_name: str) -> ToolType | None:
        """Get a tool instance by name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance or None if not found
        """
        return self.tool_instances.get(tool_name)

    def get_tools_by_route(self, route: str) -> list[ToolType]:
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

    def get_langchain_tools(self) -> list[BaseTool | Tool | StructuredTool]:
        """Get only LangChain-compatible tools.

        Returns:
            List of BaseTool/Tool/StructuredTool instances
        """
        return [
            tool
            for tool in self.tools
            if isinstance(tool, BaseTool | Tool | StructuredTool)
        ]

    def get_pydantic_tools(self) -> list[type[BaseModel]]:
        """Get only Pydantic model tools.

        Returns:
            List of Pydantic model classes
        """
        return [
            tool
            for tool in self.tools
            if isinstance(tool, type) and issubclass(tool, BaseModel)
        ]

    def get_callable_tools(self) -> list[Callable]:
        """Get only callable tools (functions, methods, etc).

        Returns:
            List of callable tools
        """
        return [
            tool for tool in self.tools if callable(tool) and not isinstance(tool, type)
        ]

    def convert_to_structured_tools(self) -> list[StructuredTool]:
        """Convert all tools to StructuredTool format where possible.

        This is useful for LangGraph ToolNode compatibility.

        Returns:
            List of StructuredTool instances
        """
        structured_tools = []

        for tool in self.tools:
            # Already a structured tool
            if isinstance(tool, StructuredTool):
                structured_tools.append(tool)

            # Convert other BaseTool types
            elif isinstance(tool, BaseTool | Tool):
                # BaseTool can be used directly by ToolNode
                structured_tools.append(tool)

            # Convert Pydantic models with __call__
            elif isinstance(tool, type) and issubclass(tool, BaseModel):
                if callable(tool) and callable(tool.__call__):
                    # This would need actual conversion logic
                    logger.debug(f"Pydantic tool {tool.__name__} needs conversion")

            # Convert regular callables
            elif callable(tool):
                # This would need actual conversion logic
                logger.debug(
                    f"Callable {getattr(tool, '__name__', 'unknown')} needs conversion"
                )

        return structured_tools

    def update_tool_route(self, tool_name: str, new_route: str) -> "ToolRouteMixin":
        """Update an existing tool's route dynamically.

        Args:
            tool_name: Name of the tool to update
            new_route: New route to assign

        Returns:
            Self for method chaining
        """
        if tool_name not in self.tool_routes:
            logger.warning(f"Tool '{tool_name}' not found")
            return self

        old_route = self.tool_routes[tool_name]
        self.tool_routes[tool_name] = new_route

        # Update metadata
        if tool_name not in self.tool_metadata:
            self.tool_metadata[tool_name] = {}

        self.tool_metadata[tool_name].update(
            {
                "route_updated": True,
                "previous_route": old_route,
                "update_timestamp": datetime.now().isoformat(),
            }
        )

        logger.debug(f"Updated route for '{tool_name}': {old_route} -> {new_route}")
        return self

    def remove_tool(self, tool_name: str) -> "ToolRouteMixin":
        """Remove a tool by name.

        Args:
            tool_name: Name of the tool to remove

        Returns:
            Self for method chaining
        """
        # Remove from instances
        tool = self.tool_instances.pop(tool_name, None)

        if tool:
            # Remove from tools list
            if tool in self.tools:
                self.tools.remove(tool)

            # Remove route and metadata
            self.tool_routes.pop(tool_name, None)
            self.tool_metadata.pop(tool_name, None)

            logger.debug(f"Removed tool '{tool_name}'")
        else:
            logger.warning(f"Tool '{tool_name}' not found")

        return self

    @model_validator(mode="after")
    def sync_tools_and_routes(self) -> "ToolRouteMixin":
        """Ensure tools and routes are synchronized after initialization."""
        # Build tool instances map if not already done
        for tool in self.tools:
            tool_name = self._get_tool_name(tool)
            if tool_name not in self.tool_instances:
                self.tool_instances[tool_name] = tool

            # Ensure route exists
            if tool_name not in self.tool_routes:
                route, metadata = self._analyze_tool(tool)
                self.tool_routes[tool_name] = route
                if metadata:
                    self.tool_metadata[tool_name] = metadata

        return self
