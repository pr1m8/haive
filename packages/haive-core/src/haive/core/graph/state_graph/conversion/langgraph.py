"""
LangGraph conversion utilities for Haive graphs.

This module provides functions to convert Haive graphs to and from LangGraph objects.
"""

import inspect
import logging
from typing import Any, Optional, Type

from langgraph.graph import END, START, StateGraph
from langgraph.types import Command
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel

logger = logging.getLogger(__name__)
console = Console()


def convert_to_langgraph(
    graph: Any, state_schema: Optional[Type[BaseModel]] = None
) -> StateGraph:
    """
    Convert a Haive graph to a LangGraph StateGraph.

    Args:
        graph: Haive graph instance (BaseGraph or SchemaGraph)
        state_schema: Optional schema to use for the StateGraph

    Returns:
        LangGraph StateGraph instance
    """
    console.print(
        Panel.fit(
            "[bold blue]Converting to LangGraph StateGraph[/bold blue]",
            border_style="blue",
        )
    )

    # Use provided schema or one from the graph
    schema = state_schema
    if schema is None:
        schema = getattr(graph, "state_schema", None)
    if schema is None:
        schema = dict

    console.print(
        f"Schema: [yellow]{schema.__name__ if hasattr(schema, '__name__') else schema}[/yellow]"
    )

    # Create StateGraph with schema
    graph_builder = StateGraph(schema)
    console.print("[green]✓[/green] Created StateGraph")

    # Add nodes
    console.print("\n[bold]Adding Nodes:[/bold]")
    for node_name, node in graph.nodes.items():
        # Skip special nodes and None nodes
        if node_name in [START, END] or node is None:
            continue

        action = extract_callable(node, node_name)
        graph_builder.add_node(node_name, action)

    # Add direct edges
    console.print("\n[bold]Adding Edges:[/bold]")
    for source, target in graph.edges:
        graph_builder.add_edge(source, target)
        console.print(f"[green]→[/green] {source} → {target}")

    # Add branches
    console.print("\n[bold]Adding Branches:[/bold]")
    for _branch_id, branch in graph.branches.items():
        source = branch.source_node

        # Extract destinations
        destinations = {}
        for key, value in branch.destinations.items():
            destinations[key] = value

        console.print(
            f"Branch from [yellow]{source}[/yellow] with conditions: {list(destinations.keys())}"
        )

        # Add conditional edges based on branch type
        if branch.mode == "FUNCTION" and branch.function:
            # Use parameter-aware wrapper
            branch_func = create_parameter_aware_wrapper(branch.function)
            graph_builder.add_conditional_edges(source, branch_func, destinations)
        else:
            # Use branch object directly
            graph_builder.add_conditional_edges(source, branch, destinations)

    console.print("\n[bold green]LangGraph conversion complete![/bold green]")
    return graph_builder


def extract_callable(node: Any, node_name: str) -> Any:
    """
    Extract a callable from a node.

    Args:
        node: Node object
        node_name: Name of the node (for logging)

    Returns:
        Callable function for the node
    """
    action = None

    # Extract callable with simple priority rules
    if callable(node):
        # 1. Node is directly callable
        action = node
        console.print(f"Node [yellow]{node_name}[/yellow]: Using direct callable")
    elif (
        hasattr(node, "metadata")
        and "callable" in node.metadata
        and callable(node.metadata["callable"])
    ):
        # 2. Node has callable in metadata
        action = node.metadata["callable"]
        console.print(f"Node [yellow]{node_name}[/yellow]: Using metadata callable")
    elif callable(node) and callable(node.__call__):
        # 3. Node has __call__ method
        action = node
        console.print(f"Node [yellow]{node_name}[/yellow]: Using __call__ method")
    else:
        # Fallback
        console.print(
            f"Node [yellow]{node_name}[/yellow]: No callable found, using pass-through"
        )

        def action(state, config=None):
            return state

    # Create parameter-aware wrapper
    return create_parameter_aware_wrapper(action)


def create_parameter_aware_wrapper(func: Any) -> Any:
    """
    Create a wrapper that adapts to the function's parameter count.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that handles parameter count differences
    """
    # Check function signature to determine parameter count
    sig = inspect.signature(func)
    param_count = len(sig.parameters)

    def wrapper(state, config=None):
        try:
            # Call with appropriate number of parameters
            if param_count == 1:
                result = func(state)
            else:
                result = func(state, config)

            # Special handling for Command objects
            if isinstance(result, Command):
                # Commands pass through unchanged
                return result

            return result
        except Exception as e:
            logger.error(f"Error calling function: {e}")
            return state

    return wrapper
