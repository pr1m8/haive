# src/haive/core/graph/tool_injector.py

import functools
import inspect
from collections.abc import Callable
from typing import Any, TypeVar, get_type_hints

from langchain_core.tools import BaseTool, tool
from langgraph.prebuilt.tool_node import InjectedState, InjectedStore

F = TypeVar("F", bound=Callable[..., Any])


class ToolInjector:
    """Utility class for creating tools with automatic state and store injection.

    This class helps create tools that can access graph state and store
    without requiring the agent to provide these values.
    """

    @staticmethod
    def create_state_tool(
        func: F,
        name: str | None = None,
        description: str | None = None,
        state_field: str | None = None,
        return_direct: bool = False,
    ) -> BaseTool:
        """Create a tool that automatically injects state from the agent.

        Args:
            func: The function to wrap as a tool
            name: Optional custom name for the tool
            description: Optional custom description for the tool
            state_field: Optional specific field from state to inject (if None, injects entire state)
            return_direct: Whether the tool should return directly to user without further LLM processing

        Returns:
            A BaseTool that automatically receives state
        """
        # Get the original signature
        sig = inspect.signature(func)

        # Find a suitable parameter to inject state into
        state_param = None
        for param_name, _param in sig.parameters.items():
            if param_name == "state" or param_name.endswith("_state"):
                state_param = param_name
                break

        # If no suitable parameter found, raise error
        if state_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'state' or ending with '_state'"
            )

        # Create a new function with the state parameter annotated for injection
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Update type hints to include InjectedState
        type_hints = get_type_hints(func)
        if state_param in type_hints:
            # Annotate the parameter
            type_hints[state_param] = Any, InjectedState(state_field)

        # Apply the updated type hints
        wrapped_func.__annotations__ = type_hints

        # Create and configure the tool
        tool_instance = None

        # First, create the tool without parameters that might not be supported
        if return_direct:
            # Try with return_direct if supported
            try:
                tool_instance = tool(return_direct=return_direct)(wrapped_func)
            except TypeError:
                # Fallback if return_direct is not supported
                tool_instance = tool()(wrapped_func)
        else:
            tool_instance = tool()(wrapped_func)

        # Set name and description if provided and supported
        if name and hasattr(tool_instance, "name"):
            tool_instance.name = name

        if description and hasattr(tool_instance, "description"):
            tool_instance.description = description

        return tool_instance

    @staticmethod
    def create_store_tool(
        func: F,
        name: str | None = None,
        description: str | None = None,
        return_direct: bool = False,
    ) -> BaseTool:
        """Create a tool that automatically injects the store from the agent.

        Args:
            func: The function to wrap as a tool
            name: Optional custom name for the tool
            description: Optional custom description for the tool
            return_direct: Whether the tool should return directly to user without further LLM processing

        Returns:
            A BaseTool that automatically receives the store
        """
        # Get the original signature
        sig = inspect.signature(func)

        # Find a suitable parameter to inject store into
        store_param = None
        for param_name, _param in sig.parameters.items():
            if param_name == "store" or param_name.endswith("_store"):
                store_param = param_name
                break

        # If no suitable parameter found, raise error
        if store_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'store' or ending with '_store'"
            )

        # Create a new function with the store parameter annotated for injection
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Update type hints to include InjectedStore
        type_hints = get_type_hints(func)
        if store_param in type_hints:
            # Annotate the parameter
            type_hints[store_param] = Any, InjectedStore()

        # Apply the updated type hints
        wrapped_func.__annotations__ = type_hints

        # Create and configure the tool
        tool_instance = None

        # First, create the tool without parameters that might not be supported
        if return_direct:
            # Try with return_direct if supported
            try:
                tool_instance = tool(return_direct=return_direct)(wrapped_func)
            except TypeError:
                # Fallback if return_direct is not supported
                tool_instance = tool()(wrapped_func)
        else:
            tool_instance = tool()(wrapped_func)

        # Set name and description if provided and supported
        if name and hasattr(tool_instance, "name"):
            tool_instance.name = name

        if description and hasattr(tool_instance, "description"):
            tool_instance.description = description

        return tool_instance

    @staticmethod
    def create_hybrid_tool(
        func: F,
        name: str | None = None,
        description: str | None = None,
        state_field: str | None = None,
        return_direct: bool = False,
    ) -> BaseTool:
        """Create a tool that automatically injects both state and store from the agent.

        Args:
            func: The function to wrap as a tool
            name: Optional custom name for the tool
            description: Optional custom description for the tool
            state_field: Optional specific field from state to inject (if None, injects entire state)
            return_direct: Whether the tool should return directly to user without further LLM processing

        Returns:
            A BaseTool that automatically receives both state and store
        """
        # Get the original signature
        sig = inspect.signature(func)

        # Find suitable parameters to inject state and store into
        state_param = None
        store_param = None

        for param_name, _param in sig.parameters.items():
            if param_name == "state" or param_name.endswith("_state"):
                state_param = param_name
            elif param_name == "store" or param_name.endswith("_store"):
                store_param = param_name

        # Check if we found both parameters
        if state_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'state' or ending with '_state'"
            )

        if store_param is None:
            raise ValueError(
                f"Function {func.__name__} must have a parameter named 'store' or ending with '_store'"
            )

        # Create a new function with both parameters annotated for injection
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            return func(*args, **kwargs)

        # Update type hints to include InjectedState and InjectedStore
        type_hints = get_type_hints(func)

        if state_param in type_hints:
            type_hints[state_param] = Any, InjectedState(state_field)

        if store_param in type_hints:
            type_hints[store_param] = Any, InjectedStore()

        # Apply the updated type hints
        wrapped_func.__annotations__ = type_hints

        # Create and configure the tool
        tool_instance = None

        # First, create the tool without parameters that might not be supported
        if return_direct:
            # Try with return_direct if supported
            try:
                tool_instance = tool(return_direct=return_direct)(wrapped_func)
            except TypeError:
                # Fallback if return_direct is not supported
                tool_instance = tool()(wrapped_func)
        else:
            tool_instance = tool()(wrapped_func)

        # Set name and description if provided and supported
        if name and hasattr(tool_instance, "name"):
            tool_instance.name = name

        if description and hasattr(tool_instance, "description"):
            tool_instance.description = description

        return tool_instance


# Convenience decorators
def state_tool(state_field: str | None = None, return_direct: bool = False):
    """Decorator to create a tool that injects state.

    Args:
        state_field: Optional specific field from state to inject
        return_direct: Whether the tool should return directly to user

    Returns:
        Decorator function
    """

    def decorator(func: F) -> BaseTool:
        return ToolInjector.create_state_tool(
            func=func, state_field=state_field, return_direct=return_direct
        )

    return decorator


def store_tool(return_direct: bool = False):
    """Decorator to create a tool that injects store.

    Args:
        return_direct: Whether the tool should return directly to user

    Returns:
        Decorator function
    """

    def decorator(func: F) -> BaseTool:
        return ToolInjector.create_store_tool(func=func, return_direct=return_direct)

    return decorator


def hybrid_tool(state_field: str | None = None, return_direct: bool = False):
    """Decorator to create a tool that injects both state and store.

    Args:
        state_field: Optional specific field from state to inject
        return_direct: Whether the tool should return directly to user

    Returns:
        Decorator function
    """

    def decorator(func: F) -> BaseTool:
        return ToolInjector.create_hybrid_tool(
            func=func, state_field=state_field, return_direct=return_direct
        )

    return decorator
