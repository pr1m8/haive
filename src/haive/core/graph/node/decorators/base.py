"""
Base decorators for creating nodes.

These decorators provide a simple way to create nodes from functions with
automatic configuration and registration.
"""

import inspect
from functools import wraps
from typing import Any, Callable, Dict, List, Optional, Type, Union

from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.engine.base import Engine
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol, State
from haive.core.graph.node.registry import NodeRegistry
from haive.core.schema.state_schema import StateSchema


def node(
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Base decorator for creating a node from a function.
    
    Automatically detects function signature and creates appropriate node type.
    
    Args:
        command_goto: Where to go after this node completes
        name: Name for the node (defaults to function name)
        input_mapping: Mapping from state keys to function parameters
        output_mapping: Mapping from function return keys to state keys
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        Decorated function as a node
    """
    def decorator(func: Callable) -> Callable:
        node_name = name or func.__name__
        
        # Check if function is async
        import asyncio
        is_async = asyncio.iscoroutinefunction(func)
        
        # Auto-detect input mapping if not provided
        detected_input_mapping = input_mapping
        if detected_input_mapping is None:
            detected_input_mapping = _auto_detect_input_mapping(func)
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=func,
            command_goto=command_goto,
            input_mapping=detected_input_mapping,
            output_mapping=output_mapping,
            is_async=is_async,
            preserve_schema=preserve_schema,
        )
        
        # Create node function
        node_func = NodeFactory.create_node(config)
        
        # Auto-register if requested
        if auto_register:
            registry = NodeFactory.get_registry()
            registry.register_node(node_name, node_func)
        
        # Add metadata for introspection
        node_func.__original_func__ = func
        node_func.__node_config__ = config
        
        # Return the node function
        return node_func
    
    return decorator


def async_node(
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Decorator for creating an async node from a function.
    
    Args:
        command_goto: Where to go after this node completes
        name: Name for the node (defaults to function name)
        input_mapping: Mapping from state keys to function parameters
        output_mapping: Mapping from function return keys to state keys
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        Decorated function as an async node
    """
    def decorator(func: Callable) -> Callable:
        node_name = name or func.__name__
        
        # Force async mode
        is_async = True
        
        # Auto-detect input mapping if not provided
        detected_input_mapping = input_mapping
        if detected_input_mapping is None:
            detected_input_mapping = _auto_detect_input_mapping(func)
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=func,
            command_goto=command_goto,
            input_mapping=detected_input_mapping,
            output_mapping=output_mapping,
            is_async=is_async,
            preserve_schema=preserve_schema,
        )
        
        # Create node function
        node_func = NodeFactory.create_node(config)
        
        # Auto-register if requested
        if auto_register:
            registry = NodeFactory.get_registry()
            registry.register_node(node_name, node_func)
        
        # Add metadata for introspection
        node_func.__original_func__ = func
        node_func.__node_config__ = config
        
        # Return the node function
        return node_func
    
    return decorator


def _auto_detect_input_mapping(func: Callable) -> Optional[Dict[str, str]]:
    """
    Auto-detect input mapping from function signature.
    
    Args:
        func: Function to analyze
        
    Returns:
        Detected input mapping or None
    """
    # Get function signature
    sig = inspect.signature(func)
    
    # Skip if function takes only state (no explicit parameters)
    if len(sig.parameters) <= 1:
        return None
    
    # Get first parameter name (usually 'state' or similar)
    first_param = list(sig.parameters.keys())[0]
    
    # Extract other parameter names (skipping first one and any with default=None)
    params = []
    for name, param in list(sig.parameters.items())[1:]:
        # Skip parameters that have default=None
        if param.default is not param.empty and param.default is None:
            continue
        params.append(name)
    
    if not params:
        return None
    
    # Create mapping from state to function parameters
    # For each parameter, map from itself to itself (e.g., {'param': 'param'})
    return {param: param for param in params}