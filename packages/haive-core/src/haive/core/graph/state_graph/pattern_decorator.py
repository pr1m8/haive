"""Graph pattern decorator for registering state graph patterns.

This module provides decorators for registering functions as graph patterns
in the Haive state graph system.
"""

import functools
from typing import Callable

from haive.core.graph.models.function_ref import FunctionReference
from haive.core.graph.state_graph.pattern_registry import (
    PatternDefinition,
    PatternRegistry,
)


def register_pattern(name: str, pattern_type: str, **parameters):
    """Register a function as a graph pattern.

    Args:
        name: Unique identifier for the pattern.
        pattern_type: Type classification of the pattern (e.g., 'sequential', 'parallel').
        **parameters: Default configuration parameters for the pattern.

    Returns:
        Decorator function that registers the pattern and preserves original function.

    Example:
        >>> @register_pattern(name="my_pattern", pattern_type="sequential")
        ... def my_processing_pattern():
        ...     '''Process data sequentially.'''
        ...     pass
    """

    def decorator(func: Callable):
        # Create pattern definition
        pattern = PatternDefinition(
            name=name,
            description=func.__doc__,
            pattern_type=pattern_type,
            apply_func=FunctionReference.from_callable(func, name=name),
            parameters=parameters,
        )

        # Register pattern
        registry = PatternRegistry.get_instance()
        registry.register(pattern)

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    return decorator
