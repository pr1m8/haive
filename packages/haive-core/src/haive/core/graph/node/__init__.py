# src/haive/core/graph/node/__init__.py
"""
Node system for Haive graph workflows.

This package provides a comprehensive system for creating, configuring, and
managing nodes in a LangGraph-based workflow. It supports various node types,
including engine nodes, callable nodes, tool nodes, validation nodes, branch nodes,
and send nodes.

The system integrates with Haive's engine and schema systems to provide a
consistent interface for building complex graphs with proper type safety
and serialization support.
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, ValidationNode

# Import from LangGraph for convenience
from langgraph.types import Command, RetryPolicy, Send
from pydantic import BaseModel

from haive.core.graph.node.config import NodeConfig

# Decorators for easy node creation
from haive.core.graph.node.decorators import (
    branch_node,
    register_node,
    send_node,
    tool_node,
    validation_node,
)
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.registry import NodeRegistry

# Core types and classes
from haive.core.graph.node.types import (
    AsyncNodeFunction,
    CommandGoto,
    ConfigType,
    NodeFunction,
    NodeType,
    StateInput,
    StateOutput,
)

# Utility functions
from haive.core.graph.node.utils import (  # derive_state_from_components,; create_multi_send_node,; create_command_with_send,; tools_should_validate
    create_send_node,
    extract_io_mapping_from_schema,
)


# Public API for creating nodes
def create_node(
    engine_or_callable: Any,
    name: Optional[str] = None,
    command_goto: Optional[CommandGoto] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    retry_policy: Optional[RetryPolicy] = None,
    **kwargs
) -> NodeFunction:
    """
    Create a node function from an engine or callable.

    This is the main function for creating nodes in the Haive framework.
    It handles various input types and creates the appropriate node function.

    Args:
        engine_or_callable: Engine or callable to use for the node
        name: Optional name for the node
        command_goto: Optional next node to go to
        input_mapping: Optional mapping from state keys to engine input keys
        output_mapping: Optional mapping from engine output keys to state keys
        retry_policy: Optional retry policy for the node
        **kwargs: Additional options for the node configuration

    Returns:
        Node function that can be added to a graph

    Example:
        # Create a node from an engine
        retriever_node = create_node(
            retriever_engine,
            name="retrieve",
            command_goto="generate"
        )

        # Add to graph
        builder.add_node("retrieve", retriever_node)
    """
    # Create node config
    node_config = NodeConfig(
        name=name or getattr(engine_or_callable, "name", None) or "unnamed_node",
        engine=engine_or_callable,
        command_goto=command_goto,
        input_mapping=input_mapping,
        output_mapping=output_mapping,
        retry_policy=retry_policy,
        **kwargs
    )

    # Create and return node function
    return NodeFactory.create_node_function(node_config)


def create_engine_node(
    engine: Any,
    name: Optional[str] = None,
    command_goto: Optional[CommandGoto] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    retry_policy: Optional[RetryPolicy] = None,
) -> NodeFunction:
    """
    Create a node function specifically from an engine.

    This is a specialized version of create_node for engines.

    Args:
        engine: Engine to use for the node
        name: Optional name for the node
        command_goto: Optional next node to go to
        input_mapping: Optional mapping from state keys to engine input keys
        output_mapping: Optional mapping from engine output keys to state keys
        retry_policy: Optional retry policy for the node

    Returns:
        Node function that can be added to a graph
    """
    return create_node(
        engine,
        name=name,
        node_type=NodeType.ENGINE,
        command_goto=command_goto,
        input_mapping=input_mapping,
        output_mapping=output_mapping,
        retry_policy=retry_policy,
    )


def create_validation_node(
    schemas: List[Union[Type[BaseModel], Callable]],
    name: Optional[str] = None,
    command_goto: Optional[CommandGoto] = None,
    messages_key: str = "messages",
) -> NodeFunction:
    """
    Create a validation node.

    This creates a node that uses LangGraph's ValidationNode to validate
    inputs against a schema.

    Args:
        schemas: List of validation schemas
        name: Optional name for the node
        command_goto: Optional next node to go to
        messages_key: Name of the messages key in the state

    Returns:
        Validation node function
    """
    return create_node(
        None,
        name=name or "validation",
        node_type=NodeType.VALIDATION,
        command_goto=command_goto,
        input_mapping=(
            {"messages": messages_key} if messages_key != "messages" else None
        ),
        validation_schemas=schemas,
    )


def create_tool_node(
    tools: List[Any],
    name: Optional[str] = None,
    command_goto: Optional[CommandGoto] = None,
    messages_key: str = "messages",
    handle_tool_errors: Union[bool, str, Callable[..., str]] = True,
) -> NodeFunction:
    """
    Create a tool node.

    This creates a node that uses LangGraph's ToolNode to handle tool calls.

    Args:
        tools: List of tools for the node
        name: Optional name for the node
        command_goto: Optional next node to go to
        messages_key: Name of the messages key in the state
        handle_tool_errors: How to handle tool errors

    Returns:
        Tool node function
    """
    return create_node(
        None,
        name=name or "tools",
        node_type=NodeType.TOOL,
        command_goto=command_goto,
        input_mapping=(
            {"messages": messages_key} if messages_key != "messages" else None
        ),
        tools=tools,
        handle_tool_errors=handle_tool_errors,
    )


def create_branch_node(
    condition: Callable,
    routes: Dict[Any, str],
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
) -> NodeFunction:
    """
    Create a branch node.

    This creates a node that evaluates a condition on the state and routes
    to different nodes based on the result.

    Args:
        condition: Function that evaluates the state and returns a key for routing
        routes: Mapping from condition outputs to node names
        name: Optional name for the node
        input_mapping: Mapping from state keys to condition function input keys

    Returns:
        Branch node function
    """
    return create_node(
        None,
        name=name or "branch",
        node_type=NodeType.BRANCH,
        input_mapping=input_mapping,
        condition=condition,
        routes=routes,
    )


def create_send_node(
    send_targets: List[str],
    send_state_key: str,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
) -> NodeFunction:
    """
    Create a send node.

    This creates a node that generates Send objects to route to different
    nodes with different states. It's useful for fan-out operations.

    Args:
        send_targets: List of target node names
        send_state_key: Key in the state containing items to send
        name: Optional name for the node
        input_mapping: Mapping from state keys to state key with items

    Returns:
        Send node function
    """
    return create_node(
        None,
        name=name or "send",
        node_type=NodeType.SEND,
        input_mapping=input_mapping,
        send_targets=send_targets,
        send_state_key=send_state_key,
    )


def get_registry() -> NodeRegistry:
    """Get the node registry instance."""
    return NodeRegistry.get_instance()


def register_custom_node_type(name: str, config_class: Type[NodeConfig]) -> None:
    """Register a custom node type."""
    NodeRegistry.get_instance().register_custom_node_type(name, config_class)


# Import V3 agent node
from haive.core.graph.node.agent_node_v3 import AgentNodeV3Config, create_agent_node_v3

# Node factory singleton for convenience
factory = NodeFactory()
