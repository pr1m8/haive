# src/haive/core/graph/node/registry.py
"""
Node registry for managing and accessing nodes.

This module provides a registry for node configurations, allowing nodes to be
registered, looked up, and managed throughout the application.
"""

import logging
from typing import Dict, List, Optional, Type

from haive.core.graph.node.config import NodeConfig
from haive.core.graph.node.types import NodeType
from haive.core.registry.base import AbstractRegistry

logger = logging.getLogger(__name__)


class NodeRegistry(AbstractRegistry[NodeConfig]):
    """
    Registry for node configurations and types.

    This registry keeps track of all registered node configurations
    and implements the AbstractRegistry interface from the Haive framework.

    It provides methods for:
    - Registering node configurations
    - Looking up nodes by ID, name, or type
    - Listing all nodes or nodes of a specific type
    - Registering custom node types
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "NodeRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry with empty storage."""
        self.nodes_by_id: Dict[str, NodeConfig] = {}
        self.nodes_by_type: Dict[NodeType, Dict[str, NodeConfig]] = {
            node_type: {} for node_type in NodeType
        }
        self.custom_node_types: Dict[str, Type[NodeConfig]] = {}

    def register(self, item: NodeConfig) -> NodeConfig:
        """
        Register a node configuration.

        Args:
            item: Node configuration to register

        Returns:
            The registered node configuration
        """
        self.nodes_by_id[item.id] = item
        self.nodes_by_type[item.node_type][item.name] = item
        logger.debug(f"Registered node config: {item.name} (id: {item.id})")
        return item

    def get(self, item_type: NodeType, name: str) -> Optional[NodeConfig]:
        """
        Get a node configuration by type and name.

        Args:
            item_type: Node type
            name: Node name

        Returns:
            Node configuration if found, None otherwise
        """
        return self.nodes_by_type[item_type].get(name)

    def find_by_id(self, id: str) -> Optional[NodeConfig]:
        """
        Find a node configuration by ID.

        Args:
            id: Node ID

        Returns:
            Node configuration if found, None otherwise
        """
        return self.nodes_by_id.get(id)

    def find_by_name(self, name: str) -> Optional[NodeConfig]:
        """
        Find a node configuration by name (searches all types).

        Args:
            name: Node name

        Returns:
            Node configuration if found, None otherwise
        """
        for node_type in NodeType:
            if node_config := self.get(node_type, name):
                return node_config
        return None

    def list(self, item_type: NodeType) -> List[str]:
        """
        List all node names of a specific type.

        Args:
            item_type: Node type

        Returns:
            List of node names
        """
        return list(self.nodes_by_type[item_type].keys())

    def get_all(self, item_type: NodeType) -> Dict[str, NodeConfig]:
        """
        Get all nodes of a specific type.

        Args:
            item_type: Node type

        Returns:
            Dictionary mapping node names to configurations
        """
        return self.nodes_by_type[item_type]

    def list_all_names(self) -> List[str]:
        """
        List all registered node names across all types.

        Returns:
            List of all node names
        """
        names = []
        for node_type in NodeType:
            names.extend(self.list(node_type))
        return names

    def register_custom_node_type(
        self, name: str, config_class: Type[NodeConfig]
    ) -> None:
        """
        Register a custom node configuration class.

        Args:
            name: Name of the custom node type
            config_class: Custom NodeConfig class
        """
        self.custom_node_types[name] = config_class
        logger.debug(f"Registered custom node type: {name}")

    def clear(self) -> None:
        """Clear all registrations."""
        self.nodes_by_id = {}
        self.nodes_by_type = {node_type: {} for node_type in NodeType}
        self.custom_node_types = {}
