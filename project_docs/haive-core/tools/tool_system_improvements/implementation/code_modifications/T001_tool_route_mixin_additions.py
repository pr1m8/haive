"""T001 - ToolRouteMixin Enhancements
Add these methods to the existing ToolRouteMixin class
Location: /haive-core/src/haive/core/common/mixins/tool_route_mixin.py.
"""
from __future__ import annotations

import inspect
from datetime import datetime
from typing import get_type_hints

# Add these imports at the top

# Add these methods to the ToolRouteMixin class:


def update_tool_route(self, tool_name: str, new_route: str) -> ToolRouteMixin:
    """Update an existing tool's route dynamically.

    This allows runtime modification of tool routes, useful for:
    - Changing tool behavior based on context
    - Redirecting tools to different handlers
    - Testing different routing strategies

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
            'route_updated': True,
            'previous_route': old_route,
            'update_timestamp': datetime.now().isoformat(),
        }, )

    logger.debug(
        f"Updated route for '{tool_name}': {old_route} -> {new_route}")
    return self


def _get_callable_metadata(self, callable_obj: Callable) -> Dict[str, Any]:
    """Extract enhanced metadata from callable objects.

    This method analyzes callables to determine:
    - Whether they are async or sync
    - Parameter information
    - Type hints availability
    - Function vs method vs lambda

    Args:
        callable_obj: Callable to analyze

    Returns:
        Dictionary of metadata
    """
    metadata = {}

    try:
        # Check if async
        metadata['is_async'] = inspect.iscoroutinefunction(callable_obj)

        # Get signature
        sig = inspect.signature(callable_obj)
        metadata['parameters'] = list(sig.parameters.keys())
        metadata['parameter_count'] = len(sig.parameters)

        # Check for type hints
        try:
            hints = get_type_hints(callable_obj)
            metadata['has_type_hints'] = bool(hints)
            metadata['has_return_type'] = 'return' in hints
            metadata['type_hint_count'] = len(hints)
        except Exception:
            metadata['has_type_hints'] = False
            metadata['has_return_type'] = False

        # Determine callable type
        if inspect.ismethod(callable_obj):
            metadata['callable_kind'] = 'method'
        elif inspect.isfunction(callable_obj):
            metadata['callable_kind'] = 'function'
        elif hasattr(callable_obj,
                     '__name__') and callable_obj.__name__ == '<lambda>':
            metadata['callable_kind'] = 'lambda'
        else:
            metadata['callable_kind'] = 'callable_object'

        # Check for docstring
        metadata['has_docstring'] = bool(callable_obj.__doc__)

    except Exception as e:
        logger.debug(f"Error analyzing callable: {e}")
        metadata['analysis_error'] = str(e)

    return metadata


def route_pydantic_model(
    self,
    model: Type[BaseModel],
    context: Optional[str] = None,
) -> str:
    """Determine appropriate route for a Pydantic model based on context.

    This method provides smart routing for Pydantic models:
    - Models used for structured output → "parser" or "structured_output_tool"
    - Models with __call__ method → "pydantic_model" (executable tool)
    - Context hints override default behavior

    Args:
        model: Pydantic model class to route
        context: Optional context hint ("output", "tool", "structured_output")

    Returns:
        Route string for the model
    """
    # Check if this is a structured output model
    if hasattr(self, 'structured_output_model'
               ) and model == self.structured_output_model:
        # Route based on structured output version
        if hasattr(self, 'structured_output_version'):
            if self.structured_output_version == 'v2':
                return 'structured_output_tool'
            return 'parser'

    # Check explicit context
    if context == 'structured_output':
        return 'structured_output_tool'
    if context in {'output', 'parser'}:
        return 'parser'
    if context == 'tool':
        return 'pydantic_model'

    # Check if model is executable (has __call__)
    if callable(model) and callable(model.__call__):
        return 'pydantic_model'

    # Default to parser for non-executable models
    return 'parser'


# Override the existing _analyze_tool method to use enhanced analysis
def _analyze_tool(self, tool: Any) -> Tuple[str, Optional[Dict[str, Any]]]:
    """Analyze a tool to determine its route and metadata.

    Enhanced version with better callable analysis and context
    awareness.
    """
    metadata = {}

    # Check for Pydantic models with context awareness
    if isinstance(tool, type) and issubclass(tool, BaseModel):
        route = self.route_pydantic_model(tool)
        metadata = {
            'class_name': tool.__name__,
            'module': getattr(tool, '__module__', 'unknown'),
            'tool_type': 'pydantic_model',
            'final_route': route,
        }
    elif hasattr(tool, '__class__') and 'BaseTool' in str(
            tool.__class__.__mro__):
        route = 'langchain_tool'
        metadata = {
            'tool_type': 'BaseTool',
            'is_instance': not isinstance(tool, type),
        }
    elif callable(tool):
        route = 'function'
        # Enhanced callable metadata
        metadata = {
            'callable_type': type(tool).__name__,
            'has_annotations': hasattr(tool, '__annotations__'),
        }
        # Add enhanced analysis
        metadata.update(self._get_callable_metadata(tool))
    else:
        route = 'unknown'
        metadata = {'original_type': type(tool).__name__}

    return route, metadata
