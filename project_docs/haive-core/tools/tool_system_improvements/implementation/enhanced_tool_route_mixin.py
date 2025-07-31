"""Enhanced tool route mixin with improved callable support and dynamic routing.

This module provides enhancements to the existing ToolRouteMixin to support:
- Better callable analysis (async, type hints, parameter inspection)
- Dynamic route updates
- Context-aware Pydantic model routing
- Integration with structured output detection
"""

import inspect
import logging
from collections.abc import Callable
from typing import Any, get_type_hints

from haive.core.common.mixins.tool_route_mixin import ToolRouteMixin
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class EnhancedToolRouteMixin(ToolRouteMixin):
    """Enhanced tool route mixin with improved capabilities.

    This extends the base ToolRouteMixin with:
    - Enhanced callable analysis
    - Dynamic route updates
    - Smart Pydantic model routing
    - Better metadata extraction
    """

    # Additional fields for enhanced functionality
    dynamic_routes: bool = Field(
        default=True, description="Allow dynamic route updates"
    )

    structured_output_routes: dict[str, str] = Field(
        default_factory=dict, description="Routes for structured output models"
    )

    callable_metadata_cache: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Cache for callable analysis results"
    )

    def update_tool_route(
        self, tool_name: str, new_route: str
    ) -> "EnhancedToolRouteMixin":
        """Update an existing tool's route dynamically.

        Args:
            tool_name: Name of the tool to update
            new_route: New route to assign

        Returns:
            Self for method chaining
        """
        if not self.dynamic_routes:
            logger.warning("Dynamic routes are disabled")
            return self

        if tool_name not in self.tool_routes:
            logger.warning(f"Tool '{tool_name}' not found in routes")
            return self

        old_route = self.tool_routes[tool_name]
        self.tool_routes[tool_name] = new_route

        # Update metadata
        metadata = self.get_tool_metadata(tool_name) or {}
        metadata["route_updated"] = True
        metadata["previous_route"] = old_route
        metadata["update_timestamp"] = __import__("datetime").datetime.now().isoformat()

        if tool_name not in self.tool_metadata:
            self.tool_metadata[tool_name] = {}
        self.tool_metadata[tool_name].update(metadata)

        logger.debug(f"Updated route for '{tool_name}': {old_route} -> {new_route}")
        return self

    def _analyze_tool(self, tool: Any) -> tuple[str, dict[str, Any] | None]:
        """Enhanced tool analysis with better callable support.

        Args:
            tool: Tool to analyze

        Returns:
            Tuple of (route, metadata)
        """
        # Check if this is a structured output context
        if hasattr(self, "_detect_structured_output_usage"):
            if isinstance(tool, type) and issubclass(tool, BaseModel):
                if self._detect_structured_output_usage(tool):
                    route = "structured_output_tool"
                    return route, {
                        "tool_type": "structured_output",
                        "model_name": tool.__name__,
                        "is_parser": True,
                    }

        # Use parent analysis as baseline
        route, metadata = super()._analyze_tool(tool)

        # Enhance callable analysis
        if route == "function":
            enhanced_metadata = self._analyze_callable(tool)
            if metadata:
                metadata.update(enhanced_metadata)
            else:
                metadata = enhanced_metadata

        # Enhance Pydantic model analysis
        elif route == "pydantic_model":
            enhanced_metadata = self._analyze_pydantic_model(tool)
            if metadata:
                metadata.update(enhanced_metadata)
            else:
                metadata = enhanced_metadata

        return route, metadata

    def _analyze_callable(self, callable_obj: Callable) -> dict[str, Any]:
        """Enhanced callable analysis.

        Args:
            callable_obj: Callable to analyze

        Returns:
            Dictionary of metadata about the callable
        """
        # Check cache first
        cache_key = (
            f"{callable_obj.__module__}.{callable_obj.__qualname__}"
            if hasattr(callable_obj, "__qualname__")
            else str(callable_obj)
        )
        if cache_key in self.callable_metadata_cache:
            return self.callable_metadata_cache[cache_key]

        metadata = {
            "callable_type": type(callable_obj).__name__,
            "has_annotations": hasattr(callable_obj, "__annotations__"),
        }

        try:
            # Get signature
            sig = inspect.signature(callable_obj)
            metadata["parameters"] = list(sig.parameters.keys())
            metadata["parameter_count"] = len(sig.parameters)

            # Check if async
            metadata["is_async"] = inspect.iscoroutinefunction(callable_obj)

            # Get type hints
            try:
                hints = get_type_hints(callable_obj)
                metadata["type_hints"] = {k: str(v) for k, v in hints.items()}
                metadata["has_return_type"] = "return" in hints
            except Exception:
                metadata["type_hints"] = {}

            # Check if method vs function
            if inspect.ismethod(callable_obj):
                metadata["callable_kind"] = "method"
                metadata["bound_to"] = type(callable_obj.__self__).__name__
            elif inspect.isfunction(callable_obj):
                metadata["callable_kind"] = "function"
            elif callable(callable_obj):
                metadata["callable_kind"] = "callable_object"
            else:
                metadata["callable_kind"] = "unknown"

            # Get docstring
            if callable_obj.__doc__:
                metadata["has_docstring"] = True
                metadata["docstring_preview"] = (
                    callable_obj.__doc__[:100] + "..."
                    if len(callable_obj.__doc__) > 100
                    else callable_obj.__doc__
                )

        except Exception as e:
            logger.debug(f"Error analyzing callable: {e}")

        # Cache the result
        self.callable_metadata_cache[cache_key] = metadata

        return metadata

    def _analyze_pydantic_model(self, model: type[BaseModel]) -> dict[str, Any]:
        """Enhanced Pydantic model analysis.

        Args:
            model: Pydantic model class to analyze

        Returns:
            Dictionary of metadata about the model
        """
        metadata = {
            "class_name": model.__name__,
            "module": getattr(model, "__module__", "unknown"),
            "tool_type": "pydantic_model",
        }

        try:
            # Check if it has __call__ method (executable tool)
            if callable(model) and callable(model.__call__):
                metadata["is_executable"] = True
                metadata["suggested_route"] = "pydantic_model"
            else:
                metadata["is_executable"] = False
                metadata["suggested_route"] = "parser"

            # Get field information
            if hasattr(model, "model_fields"):
                metadata["field_count"] = len(model.model_fields)
                metadata["fields"] = list(model.model_fields.keys())
            elif hasattr(model, "__fields__"):
                metadata["field_count"] = len(model.__fields__)
                metadata["fields"] = list(model.__fields__.keys())

            # Check for special methods
            metadata["has_validators"] = any(
                name.startswith(("validate_", "validator_")) for name in dir(model)
            )

            # Get model config
            if hasattr(model, "model_config"):
                metadata["has_config"] = True
                metadata["config_extras"] = getattr(model.model_config, "extra", None)

        except Exception as e:
            logger.debug(f"Error analyzing Pydantic model: {e}")

        return metadata

    def add_routed_tool_enhanced(
        self,
        tool: Any,
        route: str,
        metadata: dict[str, Any] | None = None,
        update_existing: bool = True,
    ) -> "EnhancedToolRouteMixin":
        """Add a tool with enhanced routing and metadata.

        Args:
            tool: Tool to add
            route: Route to assign
            metadata: Optional additional metadata
            update_existing: Whether to update if tool already exists

        Returns:
            Self for method chaining
        """
        # Generate tool name
        tool_name = self._generate_tool_name(
            tool, f"dynamic_{route}", len(self.routed_tools)
        )

        # Check if already exists
        if tool_name in self.tool_routes and not update_existing:
            logger.warning(f"Tool '{tool_name}' already exists, skipping")
            return self

        # Analyze tool for additional metadata
        _, analyzed_metadata = self._analyze_tool(tool)

        # Merge metadata
        final_metadata = analyzed_metadata or {}
        if metadata:
            final_metadata.update(metadata)
        final_metadata["added_dynamically"] = True
        final_metadata["explicit_route"] = route

        # Add to routed tools
        self.routed_tools.append((tool, route))

        # Set route with metadata
        self.set_tool_route(tool_name, route, final_metadata)

        logger.debug(f"Added enhanced routed tool '{tool_name}' with route '{route}'")
        return self

    def route_pydantic_model_smart(
        self, model: type[BaseModel], context: str | None = None
    ) -> str:
        """Smart routing for Pydantic models based on context and capabilities.

        Args:
            model: Pydantic model to route
            context: Optional context hint ("structured_output", "tool", etc.)

        Returns:
            Appropriate route string
        """
        # Check context hints
        if context == "structured_output":
            return "structured_output_tool"
        if context == "parser":
            return "parser"
        if context == "tool":
            return "pydantic_model"

        # Analyze model capabilities
        metadata = self._analyze_pydantic_model(model)

        # Use suggested route from analysis
        return metadata.get("suggested_route", "pydantic_model")

    def get_tools_by_capability(self, capability: str) -> list[tuple[str, Any]]:
        """Get tools that have a specific capability.

        Args:
            capability: Capability to search for (e.g., "is_async", "is_executable")

        Returns:
            List of (tool_name, tool) tuples
        """
        results = []

        for tool_name, metadata in self.tool_metadata.items():
            if metadata and metadata.get(capability):
                # Find the actual tool
                tool = self._find_tool_by_name(tool_name)
                if tool:
                    results.append((tool_name, tool))

        return results

    def _find_tool_by_name(self, tool_name: str) -> Any | None:
        """Find a tool instance by its name.

        Args:
            tool_name: Name of the tool

        Returns:
            Tool instance or None
        """
        # Search in tools_dict
        for tools in self.tools_dict.values():
            for tool in tools:
                if self._generate_tool_name(tool, "", 0) == tool_name:
                    return tool

        # Search in routed_tools
        for tool, _ in self.routed_tools:
            if self._generate_tool_name(tool, "", 0) == tool_name:
                return tool

        return None

    def debug_enhanced_routes(self) -> "EnhancedToolRouteMixin":
        """Enhanced debug output with additional information."""
        # Call parent debug
        super().debug_tool_routes()

        # Add enhanced information
        if self.callable_metadata_cache:
            from rich import print as rprint
            from rich.table import Table

            table = Table(title="Callable Analysis Cache", show_header=True)
            table.add_column("Callable", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Async", style="yellow")
            table.add_column("Parameters", style="magenta")

            for key, metadata in self.callable_metadata_cache.items():
                table.add_row(
                    key,
                    metadata.get("callable_kind", "unknown"),
                    "Yes" if metadata.get("is_async") else "No",
                    str(metadata.get("parameter_count", 0)),
                )

            rprint(table)

        return self
