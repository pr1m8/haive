"""
Node factory with minimalist approach.

This module provides a simplified NodeFactory for creating different types of nodes
with strong typing and StateSchema support.
"""

import asyncio
import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from langgraph.graph import END
from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.engine.base import Engine
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol, NodeReturn, State
from haive.core.graph.node.registry import NodeRegistry
from haive.core.schema.state_schema import StateSchema

logger = logging.getLogger(__name__)


class NodeFactory:
    """
    Factory for creating node functions with minimal boilerplate.
    
    Creates node functions from engine instances, callables, or NodeConfig objects
    with proper Command/Send handling and StateSchema support.
    """
    
    # Class-level registry reference
    _registry = None
    
    @classmethod
    def get_registry(cls) -> NodeRegistry:
        """Get the node registry."""
        if cls._registry is None:
            cls._registry = NodeRegistry.get_instance()
        return cls._registry
    
    @classmethod
    def set_registry(cls, registry: NodeRegistry) -> None:
        """Set the node registry."""
        cls._registry = registry
    
    @classmethod
    def create_node(
        cls,
        config: Union[NodeConfig, Engine, Callable, str],
        name: Optional[str] = None,
        command_goto: Optional[Union[str, Command, Send, List[Send]]] = None,
        input_mapping: Optional[Dict[str, str]] = None,
        output_mapping: Optional[Dict[str, str]] = None,
        is_async: Optional[bool] = None,
        preserve_schema: bool = True,
    ) -> Union[NodeProtocol, AsyncNodeProtocol]:
        """
        Create a node function from various input types.
        
        Args:
            config: NodeConfig, Engine, callable function, or engine name
            name: Name for the node (required if config is not NodeConfig)
            command_goto: Optional next node to go to
            input_mapping: Optional mapping from state keys to engine input keys
            output_mapping: Optional mapping from engine output keys to state keys
            is_async: Whether to create an async node
            preserve_schema: Whether to preserve StateSchema instances
            
        Returns:
            A node function compatible with LangGraph
            
        Raises:
            ValueError: If name is not provided when config is not NodeConfig
        """
        # Convert to NodeConfig if not already
        if not isinstance(config, NodeConfig):
            if name is None:
                if hasattr(config, "name"):
                    name = getattr(config, "name")
                elif callable(config) and hasattr(config, "__name__"):
                    name = config.__name__
                else:
                    raise ValueError("Name is required when config is not NodeConfig")
            
            node_config = NodeConfig(
                name=name,
                engine=config,
                command_goto=command_goto,
                input_mapping=input_mapping,
                output_mapping=output_mapping,
                is_async=is_async,
                preserve_schema=preserve_schema,
            )
        else:
            node_config = config
            
            # Update fields if explicitly provided
            if name is not None:
                node_config.name = name
            if command_goto is not None:
                node_config.command_goto = command_goto
            if input_mapping is not None:
                node_config.input_mapping = input_mapping
            if output_mapping is not None:
                node_config.output_mapping = output_mapping
            if is_async is not None:
                node_config.is_async = is_async
            if preserve_schema != node_config.preserve_schema:
                node_config.preserve_schema = preserve_schema
        
        # Set registry reference
        registry = cls.get_registry()
        node_config.registry = registry
        
        # Resolve engine reference if needed
        engine, engine_id = node_config.resolve_engine()
        
        # Create appropriate node function based on type
        if node_config.is_async:
            return cls._create_async_node(node_config, engine, engine_id)
        else:
            return cls._create_sync_node(node_config, engine, engine_id)
    
    @classmethod
    def _create_sync_node(
        cls, 
        config: NodeConfig, 
        engine: Any, 
        engine_id: Optional[str]
    ) -> NodeProtocol:
        """Create a synchronous node function."""
        name = config.name
        command_goto = config.command_goto
        input_mapping = config.input_mapping
        output_mapping = config.output_mapping
        preserve_schema = config.preserve_schema
        
        def node_function(state: State, runtime_config: Optional[Dict[str, Any]] = None) -> NodeReturn:
            """Node function implementation."""
            logger.debug(f"Executing node: {name}")
            
            # Process input based on mapping
            input_data = cls._process_input(state, input_mapping, preserve_schema)
            
            # Execute engine based on its type
            if isinstance(engine, Engine):
                # Create runnable with merged configuration
                final_config = cls._merge_configs(config.runnable_config, runtime_config)
                runnable = engine.create_runnable(final_config)
                
                # Invoke the runnable
                result = runnable.invoke(input_data)
            elif hasattr(engine, "invoke") and callable(engine.invoke):
                # Invokable interface
                result = engine.invoke(input_data, runtime_config)
            elif callable(engine):
                # Direct callable
                if len(inspect.signature(engine).parameters) > 1:
                    result = engine(input_data, runtime_config)
                else:
                    result = engine(input_data)
            else:
                raise ValueError(f"Unsupported engine type for node {name}: {type(engine)}")
            
            # Process output based on mapping
            output = cls._process_output(result, output_mapping, preserve_schema)
            
            # Handle command_goto if specified and result is not already a Command/Send
            if command_goto is not None and not isinstance(output, (Command, Send, list)):
                return Command(update=output, goto=command_goto)
            
            return output
        
        # Add metadata to the function
        node_function.__name__ = name
        node_function.__node_config__ = config
        
        return node_function
    
    @classmethod
    def _create_async_node(
        cls, 
        config: NodeConfig, 
        engine: Any, 
        engine_id: Optional[str]
    ) -> AsyncNodeProtocol:
        """Create an asynchronous node function."""
        name = config.name
        command_goto = config.command_goto
        input_mapping = config.input_mapping
        output_mapping = config.output_mapping
        preserve_schema = config.preserve_schema
        
        async def async_node_function(state: State, runtime_config: Optional[Dict[str, Any]] = None) -> NodeReturn:
            """Async node function implementation."""
            logger.debug(f"Executing async node: {name}")
            
            # Process input based on mapping
            input_data = cls._process_input(state, input_mapping, preserve_schema)
            
            # Execute engine based on its type
            if isinstance(engine, Engine):
                # Create runnable with merged configuration
                final_config = cls._merge_configs(config.runnable_config, runtime_config)
                runnable = engine.create_runnable(final_config)
                
                # Invoke the runnable (checking for async)
                if hasattr(runnable, "ainvoke") and callable(runnable.ainvoke):
                    result = await runnable.ainvoke(input_data)
                else:
                    result = runnable.invoke(input_data)
            elif hasattr(engine, "ainvoke") and callable(engine.ainvoke):
                # Async invokable interface
                result = await engine.ainvoke(input_data, runtime_config)
            elif asyncio.iscoroutinefunction(engine):
                # Direct async callable
                if len(inspect.signature(engine).parameters) > 1:
                    result = await engine(input_data, runtime_config)
                else:
                    result = await engine(input_data)
            elif callable(engine):
                # Fallback to sync function if needed
                if len(inspect.signature(engine).parameters) > 1:
                    result = engine(input_data, runtime_config)
                else:
                    result = engine(input_data)
            else:
                raise ValueError(f"Unsupported engine type for async node {name}: {type(engine)}")
            
            # Process output based on mapping
            output = cls._process_output(result, output_mapping, preserve_schema)
            
            # Handle command_goto if specified and result is not already a Command/Send
            if command_goto is not None and not isinstance(output, (Command, Send, list)):
                return Command(update=output, goto=command_goto)
            
            return output
        
        # Add metadata to the function
        async_node_function.__name__ = name
        async_node_function.__node_config__ = config
        
        return async_node_function
    
    @classmethod
    def _process_input(
        cls, 
        state: State, 
        input_mapping: Optional[Dict[str, str]], 
        preserve_schema: bool
    ) -> Any:
        """
        Process input based on mapping.
        
        Args:
            state: Input state
            input_mapping: Optional mapping from state keys to engine keys
            preserve_schema: Whether to preserve StateSchema
            
        Returns:
            Processed input
        """
        # Handle schema objects
        if isinstance(state, StateSchema) and preserve_schema:
            # If no mapping, return schema directly
            if not input_mapping:
                return state
            
            # Otherwise, extract mapped fields
            input_data = {}
            for state_key, engine_key in input_mapping.items():
                if hasattr(state, state_key):
                    input_data[engine_key] = getattr(state, state_key)
            return input_data
            
        # Handle dict-like state
        if hasattr(state, "get") or isinstance(state, dict):
            # If no mapping, return state directly (make copy to avoid mutation)
            if not input_mapping:
                if isinstance(state, dict):
                    return state.copy()
                return state
            
            # Otherwise, extract mapped fields
            input_data = {}
            for state_key, engine_key in input_mapping.items():
                if isinstance(state, dict) and state_key in state:
                    input_data[engine_key] = state[state_key]
                elif hasattr(state, "get"):
                    input_data[engine_key] = state.get(state_key)
            return input_data
        
        # Handle BaseModel
        if isinstance(state, BaseModel) and preserve_schema:
            # If no mapping, return model directly
            if not input_mapping:
                return state
            
            # Otherwise, extract mapped fields
            input_data = {}
            for state_key, engine_key in input_mapping.items():
                if hasattr(state, state_key):
                    input_data[engine_key] = getattr(state, state_key)
            return input_data
        
        # Last resort - return state as is
        return state
    
    @classmethod
    def _process_output(
        cls, 
        result: Any, 
        output_mapping: Optional[Dict[str, str]], 
        preserve_schema: bool
    ) -> Any:
        """
        Process output based on mapping.
        
        Args:
            result: Engine execution result
            output_mapping: Optional mapping from engine keys to state keys
            preserve_schema: Whether to preserve schema objects
            
        Returns:
            Processed output
        """
        # Pass through Command, Send, or list of Send objects directly
        if isinstance(result, (Command, Send)) or (
            isinstance(result, list) and len(result) > 0 and all(isinstance(item, Send) for item in result)
        ):
            return result
        
        # Handle schema objects
        if isinstance(result, StateSchema) and preserve_schema:
            # If no mapping, return schema directly
            if not output_mapping:
                return result
            
            # Get mutable copy of schema
            if hasattr(result, "model_copy"):
                output = result.model_copy()
            else:
                # Pydantic v1
                output = result.copy()
                
            # Update schema with mapped fields
            for engine_key, state_key in output_mapping.items():
                if hasattr(result, engine_key):
                    setattr(output, state_key, getattr(result, engine_key))
                    
            return output
            
        # Handle dict-like result
        if isinstance(result, dict):
            # If no mapping, return result directly
            if not output_mapping:
                return result
                
            # Start with empty dict if we're mapping
            output = {}
            
            # Add mapped fields
            for engine_key, state_key in output_mapping.items():
                if engine_key in result:
                    output[state_key] = result[engine_key]
                    
            return output
            
        # Handle BaseModel
        if isinstance(result, BaseModel) and preserve_schema:
            # If no mapping, return model directly
            if not output_mapping:
                return result
                
            # Convert to dict with mapped fields
            output = {}
            for engine_key, state_key in output_mapping.items():
                if hasattr(result, engine_key):
                    output[state_key] = getattr(result, engine_key)
                    
            return output
            
        # Last resort - return result as is
        return result
    
    @classmethod
    def _merge_configs(
        cls, 
        base_config: Optional[Dict[str, Any]], 
        override_config: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """Merge two configs with smart handling."""
        # Handle None cases
        if base_config is None and override_config is None:
            return None
        elif base_config is None:
            return override_config
        elif override_config is None:
            return base_config
            
        # Create a new dict with base config
        merged = base_config.copy()
        
        # Override with second config
        for key, value in override_config.items():
            if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                # Recursively merge dicts
                merged[key] = cls._merge_configs(merged[key], value)
            else:
                # Override or add value
                merged[key] = value
                
        return merged