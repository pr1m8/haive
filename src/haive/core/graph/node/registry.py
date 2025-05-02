"""
Node registry based on AbstractRegistry.

This registry manages all node processors and handlers in a type-safe way.
"""

from __future__ import annotations

import logging
from typing import Any, Callable, Dict, List, Optional, Type, Union, cast

from haive.core.graph.node.protocols import AsyncNodeProtocol, NodeProtocol, NodeReturn, State
from haive.core.registry.base import AbstractRegistry

logger = logging.getLogger(__name__)


class NodeRegistry(AbstractRegistry[Callable]):
    """
    Registry for node functions, processors, and handlers.
    
    This registry is based on AbstractRegistry for consistent API and type safety.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> NodeRegistry:
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry."""
        self.nodes: Dict[str, Union[NodeProtocol, AsyncNodeProtocol]] = {}
        self.node_types: Dict[str, Type[Any]] = {}
        self.node_factories: Dict[str, Callable] = {}
    
    def register(self, item: Callable, id: Optional[str] = None) -> Callable:
        """
        Register an item in the registry.
        
        Args:
            item: The callable to register
            id: Optional ID for the item
            
        Returns:
            The registered callable
        """
        if id is None:
            if hasattr(item, "__name__"):
                id = item.__name__
            else:
                id = f"item_{len(self.nodes)}"
        
        self.nodes[id] = item
        logger.debug(f"Registered node: {id}")
        return item

    def register_node(self, name: str, node: Union[NodeProtocol, AsyncNodeProtocol]) -> None:
        """
        Register a node function.
        
        Args:
            name: Name of the node
            node: Node function implementation
        """
        self.nodes[name] = node
        logger.debug(f"Registered node function: {name}")
    
    def register_node_factory(self, node_type: str, factory: Callable) -> None:
        """
        Register a factory function for creating nodes of a specific type.
        
        Args:
            node_type: Type of node the factory creates
            factory: Factory function that creates nodes
        """
        self.node_factories[node_type] = factory
        logger.debug(f"Registered node factory for: {node_type}")
    
    def register_node_type(self, node_type: str, type_class: Type[Any]) -> None:
        """
        Register a node type class.
        
        Args:
            node_type: Name of the node type
            type_class: Class that implements the node type
        """
        self.node_types[node_type] = type_class
        logger.debug(f"Registered node type: {node_type}")

    def get(self, item_type: Any, name: str) -> Optional[Callable]:
        """
        Get an item by type and name.
        
        Args:
            item_type: Type of item
            name: Name of the item
            
        Returns:
            Item if found, None otherwise
        """
        if item_type == "node":
            return self.nodes.get(name)
        elif item_type == "node_factory":
            return self.node_factories.get(name)
        elif item_type == "node_type":
            return self.node_types.get(name)
        return None

    def find_by_id(self, id: str) -> Optional[Callable]:
        """
        Find an item by ID.
        
        Args:
            id: Item ID
            
        Returns:
            Item if found, None otherwise
        """
        return self.nodes.get(id)

    def list(self, item_type: Any = None) -> List[str]:
        """
        List all items of a type.
        
        Args:
            item_type: Optional type to filter by
            
        Returns:
            List of item names
        """
        if item_type == "node":
            return list(self.nodes.keys())
        elif item_type == "node_factory":
            return list(self.node_factories.keys())
        elif item_type == "node_type":
            return list(self.node_types.keys())
        
        # Return all items if no type specified
        return list(self.nodes.keys())

    def get_all(self, item_type: Any = None) -> Dict[str, Callable]:
        """
        Get all items of a type.
        
        Args:
            item_type: Optional type to filter by
            
        Returns:
            Dictionary of items
        """
        if item_type == "node":
            return self.nodes
        elif item_type == "node_factory":
            return self.node_factories
        elif item_type == "node_type":
            return cast(Dict[str, Callable], self.node_types)
        
        # Return all nodes if no type specified
        return self.nodes

    def clear(self) -> None:
        """Clear the registry."""
        self.nodes.clear()
        self.node_factories.clear()
        self.node_types.clear()

    def create_node(self, node_type: str, **kwargs) -> Union[NodeProtocol, AsyncNodeProtocol]:
        """
        Create a node using a registered factory.
        
        Args:
            node_type: Type of node to create
            **kwargs: Arguments to pass to the factory
            
        Returns:
            Created node function
            
        Raises:
            ValueError: If no factory is registered for the node type
        """
        factory = self.node_factories.get(node_type)
        if factory is None:
            raise ValueError(f"No factory registered for node type: {node_type}")
        
        return factory(**kwargs)