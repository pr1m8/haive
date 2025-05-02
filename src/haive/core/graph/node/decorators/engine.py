"""
Engine node decorators.

These decorators create nodes that use various engine types.
"""

from typing import Any, Callable, Dict, List, Optional, Type, Union

from langgraph.types import Command, Send

from haive.core.engine.base import Engine
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.decorators.base import node
from haive.core.graph.node.factory import NodeFactory
from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol


def engine_node(
    engine: Union[Engine, str],
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a node that uses an engine.
    
    This can be used as a decorator on a stub function (which won't actually be called),
    or called directly to create a node function.
    
    Args:
        engine: Engine instance or engine name to use
        command_goto: Where to go after this node completes
        name: Name for the node
        input_mapping: Mapping from state keys to engine input keys
        output_mapping: Mapping from engine output keys to state keys
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A node function or decorator
    """
    # When used as a decorator on an existing function
    if callable(engine) and not isinstance(engine, Engine) and not isinstance(engine, str):
        # engine is actually the function being decorated
        func = engine
        node_name = name or func.__name__
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            # Here we would need to get engine from function metadata or registry
            # For now, we'll just use the function itself
            engine=func,
            command_goto=command_goto,
            input_mapping=input_mapping,
            output_mapping=output_mapping,
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
        
        return node_func
    
    # When used as a function call or decorator factory
    def decorator(func: Optional[Callable] = None) -> Union[NodeProtocol, AsyncNodeProtocol]:
        # If no function provided, create a default "passthrough" function
        actual_func = func
        if actual_func is None:
            def passthrough(state: Any) -> Any:
                return state
            actual_func = passthrough
        
        node_name = name or actual_func.__name__
        
        # Create node config
        config = NodeConfig(
            name=node_name,
            engine=engine,  # Use the provided engine
            command_goto=command_goto,
            input_mapping=input_mapping,
            output_mapping=output_mapping,
            preserve_schema=preserve_schema,
        )
        
        # Create node function
        node_func = NodeFactory.create_node(config)
        
        # Auto-register if requested
        if auto_register:
            registry = NodeFactory.get_registry()
            registry.register_node(node_name, node_func)
        
        # Add metadata for introspection
        node_func.__original_func__ = actual_func
        node_func.__node_config__ = config
        
        return node_func
    
    # When called directly without a function, return the decorator
    return decorator


def llm_node(
    engine: Union[Engine, str],
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a node that uses an LLM engine.
    
    This is a specialized version of engine_node for LLM engines.
    
    Args:
        engine: LLM engine instance or engine name
        command_goto: Where to go after this node completes
        name: Name for the node
        input_mapping: Mapping from state keys to LLM input keys
        output_mapping: Mapping from LLM output keys to state keys
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A node function or decorator
    """
    # Add LLM-specific defaults if not provided
    actual_input_mapping = input_mapping
    if actual_input_mapping is None:
        # Default input mapping for LLMs
        actual_input_mapping = {"messages": "messages"}
    
    actual_output_mapping = output_mapping
    if actual_output_mapping is None:
        # Default output mapping for LLMs
        actual_output_mapping = {"response": "response"}
    
    # Use engine_node with LLM defaults
    return engine_node(
        engine=engine,
        command_goto=command_goto,
        name=name,
        input_mapping=actual_input_mapping,
        output_mapping=actual_output_mapping,
        preserve_schema=preserve_schema,
        auto_register=auto_register,
    )


def retriever_node(
    engine: Union[Engine, str],
    command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
    name: Optional[str] = None,
    input_mapping: Optional[Dict[str, str]] = None,
    output_mapping: Optional[Dict[str, str]] = None,
    preserve_schema: bool = True,
    auto_register: bool = True,
):
    """
    Create a node that uses a retriever engine.
    
    This is a specialized version of engine_node for retriever engines.
    
    Args:
        engine: Retriever engine instance or engine name
        command_goto: Where to go after this node completes
        name: Name for the node
        input_mapping: Mapping from state keys to retriever input keys
        output_mapping: Mapping from retriever output keys to state keys
        preserve_schema: Whether to preserve StateSchema instances
        auto_register: Whether to automatically register the node
        
    Returns:
        A node function or decorator
    """
    # Add retriever-specific defaults if not provided
    actual_input_mapping = input_mapping
    if actual_input_mapping is None:
        # Default input mapping for retrievers
        actual_input_mapping = {"query": "query"}
    
    actual_output_mapping = output_mapping
    if actual_output_mapping is None:
        # Default output mapping for retrievers
        actual_output_mapping = {"documents": "context"}
    
    # Use engine_node with retriever defaults
    return engine_node(
        engine=engine,
        command_goto=command_goto,
        name=name,
        input_mapping=actual_input_mapping,
        output_mapping=actual_output_mapping,
        preserve_schema=preserve_schema,
        auto_register=auto_register,
    )