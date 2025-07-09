"""Node management component for BaseGraph.

This module provides the NodeManager class that handles all node-related operations
in the BaseGraph architecture, following the modular design principles.
"""

import uuid
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Union

from haive.core.graph.common.types import NodeType
from haive.core.graph.node.config import NodeConfig
from haive.core.graph.state_graph.components.base_component import BaseGraphComponent
from haive.core.logging.rich_logger import get_logger

if TYPE_CHECKING:
    from haive.core.graph.state_graph.base_graph2 import BaseGraph, Node

logger = get_logger(__name__)


class NodeManager(BaseGraphComponent):
    """Manages all node operations for BaseGraph.

    This component handles node creation, removal, updates, and management
    following the single responsibility principle. It provides a clean interface
    for all node-related operations.

    Args:
        graph: Reference to the parent BaseGraph instance

    Attributes:
        component_name: Always "node_manager"

    Example:
        Using the NodeManager::

            node_manager = NodeManager(graph)
            node_manager.initialize()

            # Add a simple function node
            node_manager.add_node("process", my_function)

            # Add a node with configuration
            config = NodeConfig(timeout_seconds=30)
            node_manager.add_node_from_config("validated", config)

            # Update node properties
            node_manager.update_node("process", metadata={"priority": "high"})

            # Remove node
            node_manager.remove_node("process")
    """

    component_name = "node_manager"

    def __init__(self, graph: "BaseGraph") -> None:
        """Initialize NodeManager with graph reference."""
        super().__init__(graph)
        self._node_type_tracking: Dict[str, NodeType] = {}

    def initialize(self) -> None:
        """Initialize the node manager."""
        super().initialize()
        self._node_type_tracking.clear()
        logger.debug(f"NodeManager initialized for graph '{self.graph.name}'")

    def cleanup(self) -> None:
        """Clean up node manager resources."""
        self._node_type_tracking.clear()
        super().cleanup()
        logger.debug(f"NodeManager cleaned up for graph '{self.graph.name}'")

    def add_node(
        self,
        node_or_name: Union["Node", Dict[str, Any], str, NodeConfig],
        node_like: Optional[Any] = None,
        **kwargs,
    ) -> "BaseGraph":
        """Add a node to the graph.

        This method provides a flexible interface for adding nodes with various
        input types and configurations.

        Args:
            node_or_name: Node identifier or node object
            node_like: Optional node function/config when first arg is string
            **kwargs: Additional node properties

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If node name already exists or inputs are invalid
            TypeError: If node types are incompatible

        Examples:
            Add function node::

                node_manager.add_node("process", my_function)

            Add with configuration::

                node_manager.add_node("engine", engine_config, timeout_seconds=30)

            Add complex node::

                node = Node(name="complex", node_type=NodeType.COMPOSITE)
                node_manager.add_node(node)
        """
        if not self._initialized:
            raise RuntimeError("NodeManager not initialized")

        # Determine node name and configuration
        node_name, node_obj = self._parse_node_inputs(node_or_name, node_like)

        # Check for duplicate names
        if node_name in self.graph.nodes:
            raise ValueError(f"Node '{node_name}' already exists in graph")

        # Infer node type
        node_type = self._infer_node_type(node_obj)

        # Create node object if needed
        if not hasattr(node_obj, "name"):
            node_obj = self._create_node_object(
                node_name, node_obj, node_type, **kwargs
            )

        # Add to graph's nodes collection
        self.graph.nodes[node_name] = node_obj

        # Track node type
        self._track_node_type(node_name, node_type)

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(
            f"Added node '{node_name}' of type {node_type} to graph '{self.graph.name}'"
        )

        return self.graph

    def add_node_from_config(
        self, name: str, config: NodeConfig, **kwargs
    ) -> "BaseGraph":
        """Add a node using a NodeConfig object.

        This method provides a type-safe way to add nodes with proper configuration
        validation and setup.

        Args:
            name: Unique node identifier
            config: NodeConfig instance with node configuration
            **kwargs: Additional properties to override config

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If node name already exists
            ValidationError: If config validation fails

        Example:
            Add node with engine config::

                from haive.core.graph.node.engine_node import EngineNodeConfig

                config = EngineNodeConfig(
                    engine=my_engine,
                    timeout_seconds=60,
                    max_retries=3
                )
                node_manager.add_node_from_config("llm_processor", config)
        """
        if not self._initialized:
            raise RuntimeError("NodeManager not initialized")

        if name in self.graph.nodes:
            raise ValueError(f"Node '{name}' already exists in graph")

        # Validate config
        validated_config = NodeConfig.model_validate(config.model_dump())

        # Override with kwargs if provided
        if kwargs:
            config_dict = validated_config.model_dump()
            config_dict.update(kwargs)
            validated_config = NodeConfig.model_validate(config_dict)

        # Create and add node
        node_obj = self._create_node_from_config(name, validated_config)
        self.graph.nodes[name] = node_obj

        # Track node type
        self._track_node_type(name, validated_config.node_type or NodeType.FUNCTION)

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(f"Added configured node '{name}' to graph '{self.graph.name}'")

        return self.graph

    def remove_node(self, node_name: str, cleanup_edges: bool = True) -> "BaseGraph":
        """Remove a node from the graph.

        Args:
            node_name: Name of the node to remove
            cleanup_edges: Whether to remove associated edges

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If node doesn't exist

        Example:
            Remove node and its edges::

                node_manager.remove_node("old_node")

            Remove node but keep edges (for debugging)::

                node_manager.remove_node("old_node", cleanup_edges=False)
        """
        if not self._initialized:
            raise RuntimeError("NodeManager not initialized")

        if node_name not in self.graph.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Remove from nodes collection
        del self.graph.nodes[node_name]

        # Remove from node type tracking
        if node_name in self._node_type_tracking:
            del self._node_type_tracking[node_name]

        # Clean up edges if requested
        if cleanup_edges:
            self._cleanup_node_edges(node_name)

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(f"Removed node '{node_name}' from graph '{self.graph.name}'")

        return self.graph

    def get_node(self, node_name: str) -> Optional["Node"]:
        """Get a node by name.

        Args:
            node_name: Name of the node to retrieve

        Returns:
            Node object if found, None otherwise
        """
        return self.graph.nodes.get(node_name)

    def update_node(self, node_name: str, **updates) -> "BaseGraph":
        """Update properties of an existing node.

        Args:
            node_name: Name of the node to update
            **updates: Properties to update

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If node doesn't exist
        """
        if not self._initialized:
            raise RuntimeError("NodeManager not initialized")

        if node_name not in self.graph.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        node = self.graph.nodes[node_name]

        # Update node properties
        for key, value in updates.items():
            if hasattr(node, key):
                setattr(node, key, value)
            else:
                # Add to metadata if property doesn't exist
                if not hasattr(node, "metadata"):
                    node.metadata = {}
                node.metadata[key] = value

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(f"Updated node '{node_name}' in graph '{self.graph.name}'")

        return self.graph

    def get_nodes_by_type(self, node_type: NodeType) -> List[str]:
        """Get all nodes of a specific type.

        Args:
            node_type: Type of nodes to retrieve

        Returns:
            List of node names matching the type
        """
        return [
            name
            for name, tracked_type in self._node_type_tracking.items()
            if tracked_type == node_type
        ]

    def get_node_count(self) -> int:
        """Get total number of nodes in the graph."""
        return len(self.graph.nodes)

    def get_node_types_summary(self) -> Dict[NodeType, int]:
        """Get summary of node types and their counts.

        Returns:
            Dictionary mapping node types to their counts
        """
        summary = {}
        for node_type in self._node_type_tracking.values():
            summary[node_type] = summary.get(node_type, 0) + 1
        return summary

    def validate_state(self) -> List[str]:
        """Validate the node manager state.

        Returns:
            List of validation error messages
        """
        errors = super().validate_state()

        # Check node consistency
        graph_nodes = set(self.graph.nodes.keys())
        tracked_nodes = set(self._node_type_tracking.keys())

        if graph_nodes != tracked_nodes:
            missing_tracked = graph_nodes - tracked_nodes
            extra_tracked = tracked_nodes - graph_nodes

            if missing_tracked:
                errors.append(f"Nodes missing from type tracking: {missing_tracked}")
            if extra_tracked:
                errors.append(f"Extra nodes in type tracking: {extra_tracked}")

        return errors

    def _parse_node_inputs(
        self, node_or_name: Any, node_like: Optional[Any]
    ) -> tuple[str, Any]:
        """Parse and validate node input parameters."""
        if isinstance(node_or_name, str):
            if node_like is None:
                raise ValueError("node_like cannot be None when node_or_name is string")
            return node_or_name, node_like
        elif hasattr(node_or_name, "name"):
            return node_or_name.name, node_or_name
        elif isinstance(node_or_name, dict) and "name" in node_or_name:
            return node_or_name["name"], node_or_name
        else:
            raise ValueError(f"Cannot determine node name from {type(node_or_name)}")

    def _infer_node_type(self, node_obj: Any) -> NodeType:
        """Infer node type from node object."""
        if hasattr(node_obj, "node_type"):
            return node_obj.node_type
        elif callable(node_obj):
            return NodeType.FUNCTION
        elif hasattr(node_obj, "tools"):
            return NodeType.TOOL
        else:
            return NodeType.FUNCTION

    def _track_node_type(self, node_name: str, node_type: NodeType) -> None:
        """Track node type for management purposes."""
        self._node_type_tracking[node_name] = node_type

    def _create_node_object(
        self, name: str, node_obj: Any, node_type: NodeType, **kwargs
    ) -> "Node":
        """Create a Node object from raw inputs."""
        # Import here to avoid circular imports
        from haive.core.graph.state_graph.base_graph2 import Node

        return Node(id=str(uuid.uuid4()), name=name, node_type=node_type, **kwargs)

    def _create_node_from_config(self, name: str, config: NodeConfig) -> "Node":
        """Create a Node object from NodeConfig."""
        # Import here to avoid circular imports
        from haive.core.graph.state_graph.base_graph2 import Node

        return Node(
            id=str(uuid.uuid4()),
            name=name,
            node_type=config.node_type or NodeType.FUNCTION,
            input_mapping=config.input_mapping,
            output_mapping=config.output_mapping,
            retry_policy=config.retry_policy,
            metadata=config.metadata or {},
        )

    def _cleanup_node_edges(self, node_name: str) -> None:
        """Remove all edges connected to a node."""
        # Remove from edges list
        self.graph.edges = [
            edge
            for edge in self.graph.edges
            if edge[0] != node_name and edge[1] != node_name
        ]

        # Remove from branches
        branches_to_remove = []
        for branch_id, branch in self.graph.branches.items():
            if hasattr(branch, "source_node") and branch.source_node == node_name:
                branches_to_remove.append(branch_id)

        for branch_id in branches_to_remove:
            del self.graph.branches[branch_id]

    def _get_current_time(self):
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now()

    def get_component_info(self) -> Dict[str, Any]:
        """Get detailed component information."""
        base_info = super().get_component_info()
        base_info.update(
            {
                "total_nodes": self.get_node_count(),
                "node_types": self.get_node_types_summary(),
                "tracked_nodes": len(self._node_type_tracking),
            }
        )
        return base_info
