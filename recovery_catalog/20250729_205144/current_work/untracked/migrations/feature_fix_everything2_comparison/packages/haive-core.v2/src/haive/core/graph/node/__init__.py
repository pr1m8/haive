"""Graph Node System - Organized for Better Documentation.

This module provides a comprehensive node system for building LangGraph workflows,
organized into logical groups for better discoverability and documentation.

Engine Nodes
============
Nodes that execute engines with intelligent I/O handling and field mapping.
These nodes are the primary interface between engines and graph workflows.

.. autosummary::
   :toctree: generated/

   EngineNodeConfig - Main engine node with field mapping support

Agent Nodes
===========
Nodes for agent execution and multi-agent coordination patterns.
These enable complex multi-agent workflows with state management.

.. autosummary::
   :toctree: generated/

   AgentNodeV3 - Advanced agent node with state projection

Validation & Routing
====================
Nodes for input/output validation, conditional routing, and workflow control.
These enable dynamic workflow behavior based on state conditions.

.. autosummary::
   :toctree: generated/

   ValidationNodeConfig - Basic validation node
   RoutingValidationNode - Validation with routing logic
   UnifiedValidationNode - Advanced validation with multiple features

Field Mapping & Composition
===========================
Advanced field mapping utilities and schema composition tools.
These enable complex data transformations between workflow stages.

.. autosummary::
   :toctree: generated/

   FieldMapping - Field mapping configuration
   NodeSchemaComposer - Advanced schema composition

Utilities & Factories
=====================
Factory functions, registries, and utilities for creating and managing nodes.
These provide convenient ways to create nodes with common patterns.

.. autosummary::
   :toctree: generated/

   NodeFactory - Factory for creating node functions
   create_node - Main node creation function
   create_engine_node - Engine node creation function
   NodeRegistry - Node type registry

Quick Start Examples
===================

Basic engine node with field mapping::

    from haive.core.graph.node import EngineNodeConfig

    node = EngineNodeConfig(
        name="processof",
        engine=my_engine,
        output_fields={"result": "processed_data"}
    )

Agent node for multi-agent workflows::

    from haive.core.graph.node import AgentNodeV3

    node = AgentNodeV3(
        name="agent_processor",
        agent=my_agent,
        shared_fields=["messages", "context"]
    )

Factory functions for quick node creation::

    from haive.core.graph.node import create_engine_node

    node = create_engine_node(
        engine=my_engine,
        name="quick_processof",
        output_mapping={"result": "output"}
    )
"""

from collections.abc import Callable
from typing import Any

from langgraph.graph import END
from langgraph.prebuilt import ToolNode, ValidationNode
from langgraph.types import Command, RetryPolicy, Send
from pydantic import BaseModel

# ===== ENGINE NODES =====
from .engine_node import EngineNodeConfig

# Try to import additional engine nodes
try:
    from .engine_node_generic import GenericEngineNode
except ImportError:
    GenericEngineNode = None

# ===== AGENT NODES =====
from .agent_node_v3 import AgentNodeV3Config as AgentNodeV3

# Try to import additional agent nodes
try:
    from .multi_agent_node import MultiAgentNode
except ImportError:
    MultiAgentNode = None

try:
    from .intelligent_multi_agent_node import IntelligentMultiAgentNode
except ImportError:
    IntelligentMultiAgentNode = None

# ===== VALIDATION & ROUTING NODES =====
try:
    from .validation_node_config import ValidationNodeConfig
except ImportError:
    ValidationNodeConfig = None

try:
    from .routing_validation_node import RoutingValidationNode
except ImportError:
    RoutingValidationNode = None

try:
    from .state_updating_validation_node import StateUpdatingValidationNode
except ImportError:
    StateUpdatingValidationNode = None

try:
    from .unified_validation_node import UnifiedValidationNode
except ImportError:
    UnifiedValidationNode = None

# ===== FIELD MAPPING & COMPOSITION =====
try:
    from .composer.field_mapping import FieldMapping, FieldMappingConfig
except ImportError:
    FieldMapping = None
    FieldMappingConfig = None

try:
    from .composer.node_schema_composer import NodeSchemaComposer
except ImportError:
    NodeSchemaComposer = None

# ===== BASE CLASSES & TYPES =====
from .config import NodeConfig

# Import decorators for compatibility
from .decorators import (
    branch_node,
    register_node,
    send_node,
    tool_node,
    validation_node,
)

# ===== UTILITIES & FACTORIES =====
from .factory import NodeFactory
from .registry import NodeRegistry
from .types import (
    AsyncNodeFunction,
    CommandGoto,
    ConfigType,
    NodeFunction,
    NodeType,
    StateInput,
    StateOutput,
)

# Import utility functions
from .utils import (
    create_send_node,
    extract_io_mapping_from_schema,
)

# ===== FACTORY FUNCTIONS (Keep existing API) =====


def create_node(
    engine_or_callable: Any,
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
    retry_policy: RetryPolicy | None = None,
    **kwargs
) -> NodeFunction:
    """Create a node function from an engine or callable.

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
        Create a node from an engine::

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
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    input_mapping: dict[str, str] | None = None,
    output_mapping: dict[str, str] | None = None,
    retry_policy: RetryPolicy | None = None,
) -> NodeFunction:
    """Create a node function specifically from an engine.

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
    schemas: list[type[BaseModel] | Callable],
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    messages_key: str = "messages",
) -> NodeFunction:
    """Create a validation node.

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
    tools: list[Any],
    name: str | None = None,
    command_goto: CommandGoto | None = None,
    messages_key: str = "messages",
    handle_tool_errors: bool | str | Callable[..., str] = True,
) -> NodeFunction:
    """Create a tool node.

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
    routes: dict[Any, str],
    name: str | None = None,
    input_mapping: dict[str, str] | None = None,
) -> NodeFunction:
    """Create a branch node.

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


def get_registry() -> NodeRegistry:
    """Get the node registry instance."""
    return NodeRegistry.get_instance()


def register_custom_node_type(name: str, config_class: type[NodeConfig]) -> None:
    """Register a custom node type."""
    NodeRegistry.get_instance().register_custom_node_type(name, config_class)


# Node factory singleton for convenience
factory = NodeFactory()

# Build __all__ list dynamically based on what's available
__all__ = [
    "END",
    "AgentNodeV3",
    # ===== TYPES =====
    "AsyncNodeFunction",
    # ===== LANGRAPH RE-EXPORTS =====
    "Command",
    "CommandGoto",
    "ConfigType",
    "EngineNodeConfig",
    # ===== CORE CLASSES =====
    "NodeConfig",
    # ===== UTILITIES =====
    "NodeFactory",
    "NodeFunction",
    "NodeRegistry",
    "NodeType",
    "RetryPolicy",
    "Send",
    "StateInput",
    "StateOutput",
    "ToolNode",
    "ValidationNode",
    # ===== DECORATORS =====
    "branch_node",
    "create_branch_node",
    "create_engine_node",
    # ===== FACTORY FUNCTIONS =====
    "create_node",
    "create_send_node",
    "create_tool_node",
    "create_validation_node",
    # ===== UTILITIES =====
    "extract_io_mapping_from_schema",
    "factory",
    "get_registry",
    "register_custom_node_type",
    "register_node",
    "send_node",
    "tool_node",
    "validation_node",
]

# Add conditionally available items
if GenericEngineNode:
    __all__.append("GenericEngineNode")
if MultiAgentNode:
    __all__.append("MultiAgentNode")
if IntelligentMultiAgentNode:
    __all__.append("IntelligentMultiAgentNode")
if ValidationNodeConfig:
    __all__.append("ValidationNodeConfig")
if RoutingValidationNode:
    __all__.append("RoutingValidationNode")
if StateUpdatingValidationNode:
    __all__.append("StateUpdatingValidationNode")
if UnifiedValidationNode:
    __all__.append("UnifiedValidationNode")
if FieldMapping:
    __all__.extend(["FieldMapping", "FieldMappingConfig"])
if NodeSchemaComposer:
    __all__.append("NodeSchemaComposer")
