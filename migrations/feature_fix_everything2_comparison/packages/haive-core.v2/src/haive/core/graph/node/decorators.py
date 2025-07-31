"""Decorators graph module.

This module provides decorators functionality for the Haive framework.

Functions:
    register_node: Register Node functionality.
    decorator: Decorator functionality.
    tool_node: Tool Node functionality.
"""

# src/haive/core/graph/node/decorators.py
"""From typing import Any, Dict
Decorators for creating and registering nodes.

This module provides decorators that make it easy to create various types
of nodes from functions, with proper configuration and registration.
"""

import logging
from collections.abc import Callable
from typing import Any

from langgraph.types import RetryPolicy

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.types import (
    CommandGoto,
    ConfigType,
    NodeType,
    StateInput,
    StateOutput,
)

logger = logging.getLogger(__name__)


def register_node(
    name: str | None = None,
    node_type: NodeType | None = None,
    command_goto: CommandGoto | None = None,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
    retry_policy: RetryPolicy | None = None,
    **kwargs,
):
    """Decorator to register a function as a node.

    This decorator wraps a function as a node function, with proper configuration
    for node type, command routing, input/output mapping, and retry policy.

    Args:
        name: Optional name for the node (defaults to function name)
        node_type: Type of node to create
        command_goto: Next node to go to after this node
        input_mapping: Mapping from state keys to function input keys
        output_mapping: Mapping from function output keys to state keys
        retry_policy: Retry policy for the node
        **kwargs: Additional options for the node configuration

    Returns:
        Decorated function as a node function
    """

    def decorator(func: Callable[[StateInput, ConfigType | None], StateOutput]):
        # Get node name from function name if not provided
        node_name = name or func.__name__

        # Create node config
        node_config = NodeConfig(
            name=node_name,
            node_type=node_type,
            callable_func=func,
            command_goto=command_goto,
            input_fields=input_mapping,
            output_fields=output_mapping,
            retry_policy=retry_policy,
            **kwargs,
        )

        # Create node function
        node_func = NodeFactory.create_node_function(node_config)

        # Preserve function metadata
        node_func.__name__ = func.__name__
        node_func.__doc__ = func.__doc__

        return node_func

    return decorator


def tool_node(
    tools: list,
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    messages_field: str = "messages",
    handle_tool_errors: bool | str | Callable[..., str] = True,
):
    """Create a tool node.

    This decorator creates a node that handles tool calls using LangGraph's
    ToolNode. It's a specialized version of register_node.

    Args:
        tools: List of tools for the node
        name: Optional name for the node
        command_goto: Next node to go to after this node
        messages_field: Name of the messages key in the state
        handle_tool_errors: How to handle tool errors
    """
    return register_node(
        name=name,
        node_type=NodeType.TOOL,
        command_goto=command_goto,
        input_mapping=(
            {"messages": messages_field} if messages_field != "messages" else None
        ),
        tools=tools,
        messages_field=messages_field,
        handle_tool_errors=handle_tool_errors,
    )


def validation_node(
    schemas: list,
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    messages_field: str = "messages",
):
    """Create a validation node.

    This decorator creates a node that validates inputs against a schema
    using LangGraph's ValidationNode. It's a specialized version of register_node.

    Args:
        schemas: List of validation schemas
        name: Optional name for the node
        command_goto: Next node to go to after this node
        messages_field: Name of the messages key in the state
    """
    return register_node(
        name=name,
        node_type=NodeType.VALIDATION,
        command_goto=command_goto,
        input_mapping=(
            {"messages": messages_field} if messages_field != "messages" else None
        ),
        validation_schemas=schemas,
        messages_field=messages_field,
    )


def branch_node(
    condition: Callable,
    routes: dict[Any, str],
    name: str | None = None,
    input_mapping: dict[str, str] | None = None,
):
    """Create a branch node.

    This decorator creates a node that evaluates a condition on the state
    and routes to different nodes based on the result.

    Args:
        condition: Function that evaluates the state and returns a key for routing
        routes: Mapping from condition outputs to node names
        name: Optional name for the node
        input_mapping: Mapping from state keys to condition function input keys
    """
    return register_node(
        name=name,
        node_type=NodeType.BRANCH,
        input_fields=input_mapping,
        condition=condition,
        routes=routes,
    )


def send_node(
    send_targets: list[str],
    send_field: str,
    name: str | None = None,
    input_mapping: dict[str, str] | None = None,
):
    """Create a send node.

    This decorator creates a node that generates Send objects to route to
    different nodes with different states. It's useful for fan-out operations.

    Args:
        send_targets: List of target node names
        send_field: Key in the state containing items to send
        name: Optional name for the node
        input_mapping: Mapping from state keys to field with items
    """
    return register_node(
        name=name,
        node_type=NodeType.SEND,
        input_fields=input_mapping,
        send_targets=send_targets,
        send_field=send_field,
    )


# Add a new debug decorator
def debug_node(name: str | None = None):
    """Decorator to add detailed debug logging to a node function. Logs input state and
    output result but does not modify the function behavior.

    Args:
        name: Name for the node in logs (defaults to function name)

    Returns:
        Decorated function
    """
    from rich.console import Console
    from rich.panel import Panel
    from rich.pretty import Pretty

    console = Console()

    def decorator(func) -> Any:
        func_name = name or func.__name__

        def wrapper(state: dict[str, Any], config: dict[str, Any] | None = None):
            # Log input
            console.print(
                Panel.fit(
                    f"[bold cyan]Node {func_name} Input:[/bold cyan]\n{
                        Pretty(state)}",
                    border_style="cyan",
                )
            )

            # Call original function
            result = func(state, config)

            # Log output
            result_display = Pretty(result)
            console.print(
                Panel.fit(
                    f"[bold green]Node {func_name} Output:[/bold green]\n{result_display}",
                    border_style="green",
                )
            )

            # Special handling for Command objects
            from langgraph.types import Command

            if isinstance(result, Command):
                console.print(
                    Panel.fit(
                        "[bold yellow]Command Object Detected:[/bold yellow]\n"
                        + f"Type: {type(result).__name__}\n"
                        + f"Attributes: {dir(result)}\n"
                        + f"Update: {getattr(result, 'update', None)}\n"
                        + f"Branch: {getattr(result, 'branch', None)}",
                        border_style="yellow",
                    )
                )

            # Return original result unchanged
            return result

        # Preserve function metadata

        return wraps(func)(wrapper)

    return decorator
