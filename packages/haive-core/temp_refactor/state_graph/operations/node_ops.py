"""Node operations for the state graph system.

This module provides operations for adding, removing, and manipulating
nodes in a graph.
"""

import logging
import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple

from pydantic import BaseModel

from haive.core.graph.common.types import NodeType
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.state_graph.base.graph_base import GraphBase

# Set up logging
logger = logging.getLogger(__name__)


class Node(BaseModel):
    """Basic node model for internal use."""

    name: str
    function: Callable
    node_type: NodeType = NodeType.CALLABLE
    metadata: dict[str, Any] = {}


class NodeOperations:
    """Operations for managing nodes in a graph.

    This class provides methods for adding, removing, updating,
    and manipulating nodes in a graph.
    """

    @staticmethod
    def add_node(
        graph: GraphBase, node_name: str, node_obj: Any, **kwargs
    ) -> GraphBase:
        """Add a node to the graph.

        Args:
            graph: Graph to add the node to
            node_name: Name for the node
            node_obj: Node object or callable
            **kwargs: Additional node properties

        Returns:
            Updated graph
        """
        # Determine node type
        node_type = NodeOperations._infer_node_type(node_obj)

        # Store the node directly
        graph.nodes[node_name] = node_obj

        # Track the node type
        graph.node_types[node_name] = node_type

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def remove_node(graph: GraphBase, node_name: str) -> GraphBase:
        """Remove a node from the graph.

        Args:
            graph: Graph to remove the node from
            node_name: Name of the node to remove

        Returns:
            Updated graph
        """
        # Check if node exists
        if node_name not in graph.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Remove node
        del graph.nodes[node_name]

        # Remove from node_types if tracked
        if node_name in graph.node_types:
            del graph.node_types[node_name]

        # Remove from subgraphs if it's a subgraph
        if node_name in graph.subgraphs:
            del graph.subgraphs[node_name]

        # Remove associated direct edges
        graph.edges = [
            edge
            for edge in graph.edges
            if edge[0] != node_name and edge[1] != node_name
        ]

        # Remove associated branches
        branch_ids_to_remove = []
        for branch_id, branch in graph.branches.items():
            if branch.source_node == node_name:
                branch_ids_to_remove.append(branch_id)

        for branch_id in branch_ids_to_remove:
            del graph.branches[branch_id]

        # Update any branch destinations that pointed to this node
        for branch in graph.branches.values():
            for condition, target in list(branch.destinations.items()):
                if target == node_name:
                    # Remove or set to default
                    del branch.destinations[condition]

            # Update default if needed
            if branch.default == node_name:
                branch.default = "END"

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def update_node(graph: GraphBase, node_name: str, **updates) -> GraphBase:
        """Update a node's properties.

        Args:
            graph: Graph containing the node
            node_name: Name of the node to update
            **updates: Properties to update

        Returns:
            Updated graph
        """
        # Check if node exists
        if node_name not in graph.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Get current node
        node = graph.nodes[node_name]

        # Cannot update None nodes
        if node is None:
            raise ValueError(f"Cannot update None node '{node_name}'")

        # Apply updates based on node type
        if isinstance(node, dict):
            # Dictionary node
            for key, value in updates.items():
                node[key] = value
        elif hasattr(node, "__dict__"):
            # Object node
            for key, value in updates.items():
                if hasattr(node, key):
                    setattr(node, key, value)
        elif isinstance(node, NodeConfig):
            # NodeConfig - update fields using proper method
            for key, value in updates.items():
                if hasattr(node, key):
                    setattr(node, key, value)

        # Update node type if changed
        if "node_type" in updates and node_name in graph.node_types:
            graph.node_types[node_name] = updates["node_type"]

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def replace_node(
        graph: GraphBase,
        node_name: str,
        new_node: Any,
        preserve_connections: bool = True,
    ) -> GraphBase:
        """Replace a node with a new one, optionally preserving connections.

        Args:
            graph: Graph containing the node
            node_name: Name of the node to replace
            new_node: New node to insert
            preserve_connections: Whether to preserve existing connections

        Returns:
            Updated graph
        """
        # Check if node exists
        if node_name not in graph.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Store existing connections if needed
        incoming_edges = []
        outgoing_edges = []
        source_branches = []

        if preserve_connections:
            # Get direct edges
            for source, target in graph.edges:
                if source == node_name:
                    outgoing_edges.append((source, target))
                elif target == node_name:
                    incoming_edges.append((source, target))

            # Get branches where this is the source
            source_branches = [
                branch
                for branch in graph.branches.values()
                if branch.source_node == node_name
            ]

        # Remove the old node
        NodeOperations.remove_node(graph, node_name)

        # Add the new node
        # Handle different types of new_node
        if isinstance(new_node, dict) and "name" in new_node:
            # Dictionary with name - update name if needed
            new_node = new_node.copy()
            new_node["name"] = node_name
            NodeOperations.add_node(graph, node_name, new_node)
        elif hasattr(new_node, "name") and hasattr(new_node, "model_copy"):
            # Pydantic model with name - create copy with new name
            new_node_copy = new_node.model_copy(deep=True)
            new_node_copy.name = node_name
            NodeOperations.add_node(graph, node_name, new_node_copy)
        elif isinstance(new_node, NodeConfig):
            # NodeConfig - update name if needed
            if hasattr(new_node, "name") and new_node.name != node_name:
                new_node.name = node_name
            NodeOperations.add_node(graph, node_name, new_node)
        else:
            # Generic object - just add it
            NodeOperations.add_node(graph, node_name, new_node)

        # Restore connections if needed
        if preserve_connections:
            # Restore direct edges
            for source, target in incoming_edges:
                if (source, node_name) not in graph.edges:
                    graph.edges.append((source, node_name))

            for source, target in outgoing_edges:
                if (node_name, target) not in graph.edges:
                    graph.edges.append((node_name, target))

            # Restore branches
            for branch in source_branches:
                branch.source_node = node_name
                graph.branches[branch.id] = branch

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def insert_node_after(
        graph: GraphBase,
        target_node: str,
        new_node_name: str,
        new_node_obj: Any,
        **kwargs,
    ) -> GraphBase:
        """Insert a new node after an existing node, redirecting all outgoing connections.

        Args:
            graph: Graph containing the target node
            target_node: Name of the existing node
            new_node_name: Name for the new node
            new_node_obj: Node object or callable for the new node
            **kwargs: Additional node properties

        Returns:
            Updated graph
        """
        # Check if target node exists
        if target_node not in graph.nodes and target_node != "START":
            raise ValueError(f"Target node '{target_node}' not found in graph")

        # Find all outgoing connections from target node
        outgoing_edges = []
        for source, target in graph.edges:
            if source == target_node:
                outgoing_edges.append((source, target))

        # Find all branches from target node
        branches_to_update = []
        for _branch_id, branch in graph.branches.items():
            if branch.source_node == target_node:
                branches_to_update.append(branch)

        # Add the new node
        NodeOperations.add_node(graph, new_node_name, new_node_obj, **kwargs)

        # Remove original outgoing edges
        for source, target in outgoing_edges:
            if (source, target) in graph.edges:
                graph.edges.remove((source, target))

        # Add edge from target to new node
        graph.edges.append((target_node, new_node_name))

        # Add edges from new node to original targets
        for _, target in outgoing_edges:
            graph.edges.append((new_node_name, target))

        # Update branches
        for branch in branches_to_update:
            # Remove old branch
            if branch.id in graph.branches:
                del graph.branches[branch.id]

            # Create new branch from new node
            branch.source_node = new_node_name
            branch.id = str(uuid.uuid4())  # New ID for new branch
            graph.branches[branch.id] = branch

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def insert_node_before(
        graph: GraphBase,
        target_node: str,
        new_node_name: str,
        new_node_obj: Any,
        **kwargs,
    ) -> GraphBase:
        """Insert a new node before an existing node, redirecting all incoming connections.

        Args:
            graph: Graph containing the target node
            target_node: Name of the existing node
            new_node_name: Name for the new node
            new_node_obj: Node object or callable for the new node
            **kwargs: Additional node properties

        Returns:
            Updated graph
        """
        # Check if target node exists
        if target_node not in graph.nodes:
            raise ValueError(f"Target node '{target_node}' not found in graph")

        # Find all incoming connections to target node
        incoming_edges = []
        for source, target in graph.edges:
            if target == target_node:
                incoming_edges.append((source, target))

        # Find all branches pointing to target node
        incoming_branches = []
        for _branch_id, branch in graph.branches.items():
            # Check destinations
            for condition, dest in list(branch.destinations.items()):
                if dest == target_node:
                    incoming_branches.append((branch, condition))

            # Check default
            if branch.default == target_node:
                incoming_branches.append((branch, "default"))

        # Add the new node
        NodeOperations.add_node(graph, new_node_name, new_node_obj, **kwargs)

        # Remove original incoming edges
        for source, target in incoming_edges:
            if (source, target) in graph.edges:
                graph.edges.remove((source, target))

        # Add edges from sources to new node
        for source, _ in incoming_edges:
            graph.edges.append((source, new_node_name))

        # Add edge from new node to target
        graph.edges.append((new_node_name, target_node))

        # Update branches
        for branch, condition in incoming_branches:
            if condition == "default":
                branch.default = new_node_name
            else:
                branch.destinations[condition] = new_node_name

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_prelude_node(
        graph: GraphBase, node_name: str, node_obj: Any, **kwargs
    ) -> GraphBase:
        """Add a node at the beginning of the graph (after START).

        Args:
            graph: Graph to add the prelude node to
            node_name: Name for the prelude node
            node_obj: Node object or callable
            **kwargs: Additional node properties

        Returns:
            Updated graph
        """
        # Get all nodes connected directly from START
        start_edges = [
            (source, target) for source, target in graph.edges if source == "START"
        ]

        # Get all nodes connected from START via branches
        start_branches = [
            branch
            for branch in graph.branches.values()
            if branch.source_node == "START"
        ]

        # Add the prelude node
        NodeOperations.add_node(graph, node_name, node_obj, **kwargs)

        # Remove existing START direct edges
        for _, target in start_edges:
            if ("START", target) in graph.edges:
                graph.edges.remove(("START", target))

        # Add edge from START to prelude
        graph.edges.append(("START", node_name))

        # Add edges from prelude to original start nodes
        for _, target in start_edges:
            graph.edges.append((node_name, target))

        # Handle branches from START
        for branch in start_branches:
            # Remove the old branch
            if branch.id in graph.branches:
                del graph.branches[branch.id]

            # Create new branch from prelude node with same destinations
            branch.source_node = node_name
            branch.id = str(uuid.uuid4())  # New ID
            graph.branches[branch.id] = branch

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_postlude_node(
        graph: GraphBase, node_name: str, node_obj: Any, **kwargs
    ) -> GraphBase:
        """Add a node at the end of the graph (before END).

        Args:
            graph: Graph to add the postlude node to
            node_name: Name for the postlude node
            node_obj: Node object or callable
            **kwargs: Additional node properties

        Returns:
            Updated graph
        """
        # Get all nodes connecting directly to END
        end_edges = [
            (source, target) for source, target in graph.edges if target == "END"
        ]

        # Get all branches pointing to END
        end_branch_destinations = []
        for branch in graph.branches.values():
            # Check destinations
            for condition, target in list(branch.destinations.items()):
                if target == "END":
                    end_branch_destinations.append((branch, condition))

            # Check default
            if branch.default == "END":
                end_branch_destinations.append((branch, "default"))

        # Add the postlude node
        NodeOperations.add_node(graph, node_name, node_obj, **kwargs)

        # Remove existing END edges
        for source, _ in end_edges:
            if (source, "END") in graph.edges:
                graph.edges.remove((source, "END"))

        # Add edges from original end nodes to postlude
        for source, _ in end_edges:
            graph.edges.append((source, node_name))

        # Add edge from postlude to END
        graph.edges.append((node_name, "END"))

        # Update branch destinations
        for branch, condition in end_branch_destinations:
            if condition == "default":
                branch.default = node_name
            else:
                branch.destinations[condition] = node_name

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def add_sequence(
        graph: GraphBase,
        node_sequence: list[tuple[str, Any]],
        connect_start: bool = False,
        connect_end: bool = False,
        **kwargs,
    ) -> GraphBase:
        """Add a sequence of nodes and connect them in order.

        Args:
            graph: Graph to add the sequence to
            node_sequence: List of (name, node_obj) tuples
            connect_start: Whether to connect the first node to START
            connect_end: Whether to connect the last node to END
            **kwargs: Additional properties for all nodes

        Returns:
            Updated graph
        """
        if not node_sequence:
            return graph

        # Add nodes
        node_names = []
        for name, node_obj in node_sequence:
            NodeOperations.add_node(graph, name, node_obj, **kwargs)
            node_names.append(name)

        # Connect START if requested
        if connect_start and node_names:
            graph.edges.append(("START", node_names[0]))

        # Connect nodes in sequence
        for i in range(len(node_names) - 1):
            graph.edges.append((node_names[i], node_names[i + 1]))

        # Connect END if requested
        if connect_end and node_names:
            graph.edges.append((node_names[-1], "END"))

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def _infer_node_type(node: Any) -> NodeType:
        """Infer the node type from a node object.

        Args:
            node: Node object to infer type from

        Returns:
            Inferred NodeType
        """
        # Check if node has an explicit node_type attribute
        if hasattr(node, "node_type"):
            return node.node_type

        # Check for NodeConfig instances
        if hasattr(node, "__class__") and "NodeConfig" in node.__class__.__name__:
            # Different NodeConfig classes map to different node types
            if "EngineNodeConfig" in node.__class__.__name__:
                return NodeType.ENGINE
            if "ToolNodeConfig" in node.__class__.__name__:
                return NodeType.TOOL
            if "ValidationNodeConfig" in node.__class__.__name__:
                return NodeType.VALIDATION
            return NodeType.CALLABLE

        # Check for engine objects
        if hasattr(node, "engine_type") and hasattr(node, "create_runnable"):
            return NodeType.ENGINE

        # Check for subgraphs
        if isinstance(node, GraphBase):
            return NodeType.SUBGRAPH

        # Check for callable objects
        if callable(node):
            return NodeType.CALLABLE

        # Default to callable for other objects
        return NodeType.CALLABLE
