"""
Testing utilities for nodes.

These utilities help with testing node implementations with minimal dependencies.
"""

import inspect
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

from langgraph.types import Command, Send
from pydantic import BaseModel

from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol, State
from haive.core.schema.state_schema import StateSchema


class NodeTester:
    """
    Helper for testing nodes.
    
    This class provides utilities for running and testing nodes in isolation.
    """
    
    @staticmethod
    def run_node(
        node: Union[NodeProtocol, AsyncNodeProtocol],
        state: State,
        config: Optional[Dict[str, Any]] = None,
    ) -> Any:
        """
        Run a node with the given state and config.
        
        Handles both synchronous and asynchronous nodes.
        
        Args:
            node: Node function to run
            state: Input state
            config: Optional runtime configuration
            
        Returns:
            Node execution result
        """
        # Check if node is async
        is_async = NodeTester.is_async_node(node)
        
        if is_async:
            # Run async node
            import asyncio
            return asyncio.run(node(state, config))
        else:
            # Run sync node
            return node(state, config)
    
    @staticmethod
    def is_async_node(node: Union[NodeProtocol, AsyncNodeProtocol]) -> bool:
        """
        Check if a node is asynchronous.
        
        Args:
            node: Node function to check
            
        Returns:
            True if the node is asynchronous, False otherwise
        """
        import asyncio
        return asyncio.iscoroutinefunction(node)
    
    @staticmethod
    def get_node_config(node: Union[NodeProtocol, AsyncNodeProtocol]) -> Optional[Dict[str, Any]]:
        """
        Get a node's configuration.
        
        Args:
            node: Node function to check
            
        Returns:
            Node configuration if available, None otherwise
        """
        if hasattr(node, "__node_config__"):
            config = getattr(node, "__node_config__")
            
            # Convert to dict if it's a pydantic model
            if isinstance(config, BaseModel):
                if hasattr(config, "model_dump"):
                    # Pydantic v2
                    return config.model_dump()
                else:
                    # Pydantic v1
                    return config.dict()
            
            return config
        
        return None
    
    @staticmethod
    def assert_node_output(
        node: Union[NodeProtocol, AsyncNodeProtocol],
        state: State,
        expected_value: Any,
        path: Optional[str] = None,
        config: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Assert that a node's output matches an expected value.
        
        Args:
            node: Node function to test
            state: Input state
            expected_value: Expected output value
            path: Dot-separated path to check in the output (e.g., "messages.0.content")
            config: Optional runtime configuration
            
        Raises:
            AssertionError: If the output doesn't match the expected value
        """
        # Run the node
        result = NodeTester.run_node(node, state, config)
        
        # Handle Command/Send results
        if isinstance(result, Command):
            result = result.update
        elif isinstance(result, Send):
            result = result.arg
        
        # Check specific path
        if path:
            actual_value = NodeTester._get_value_at_path(result, path)
        else:
            actual_value = result
        
        # Assert equality
        assert actual_value == expected_value, f"Expected {expected_value}, got {actual_value}"
    
    @staticmethod
    def _get_value_at_path(obj: Any, path: str) -> Any:
        """
        Get a value at a dot-separated path.
        
        Args:
            obj: Object to navigate
            path: Dot-separated path (e.g., "messages.0.content")
            
        Returns:
            Value at the path
        """
        components = path.split(".")
        current = obj
        
        for component in components:
            if isinstance(current, dict):
                # Handle dictionary access
                if component in current:
                    current = current[component]
                else:
                    raise KeyError(f"Key '{component}' not found in dict at path '{path}'")
            elif isinstance(current, (list, tuple)):
                # Handle list/tuple access
                try:
                    index = int(component)
                    current = current[index]
                except (ValueError, IndexError):
                    raise IndexError(f"Invalid index '{component}' for list at path '{path}'")
            elif hasattr(current, component):
                # Handle attribute access
                current = getattr(current, component)
            else:
                raise AttributeError(f"Attribute '{component}' not found at path '{path}'")
        
        return current