"""Edge management component for BaseGraph.

This module provides the EdgeManager class that handles all edge-related operations
in the BaseGraph architecture, maintaining clean separation of concerns.
"""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Tuple

from haive.core.graph.state_graph.components.base_component import BaseGraphComponent
from haive.core.logging.rich_logger import get_logger

if TYPE_CHECKING:
    from haive.core.graph.state_graph.base_graph2 import BaseGraph

logger = get_logger(__name__)

# Type alias for edges
Edge = Tuple[str, str]


class EdgeManager(BaseGraphComponent):
    """Manages all edge operations for BaseGraph.

    This component handles direct edge creation, removal, and management
    following the single responsibility principle. It maintains the graph's
    connectivity information and provides validation for edge operations.

    Args:
        graph: Reference to the parent BaseGraph instance

    Attributes:
        component_name: Always "edge_manager"

    Example:
        Using the EdgeManager::

            edge_manager = EdgeManager(graph)
            edge_manager.initialize()

            # Add direct edges
            edge_manager.add_edge("start", "process")
            edge_manager.add_edge("process", "end")

            # Get edges for a node
            outgoing = edge_manager.get_outgoing_edges("start")
            incoming = edge_manager.get_incoming_edges("end")

            # Remove edge
            edge_manager.remove_edge("start", "process")

            # Find connectivity issues
            dangling = edge_manager.find_dangling_edges()
    """

    component_name = "edge_manager"

    def __init__(self, graph: "BaseGraph") -> None:
        """Initialize EdgeManager with graph reference."""
        super().__init__(graph)

    def initialize(self) -> None:
        """Initialize the edge manager."""
        super().initialize()
        logger.debug(f"EdgeManager initialized for graph '{self.graph.name}'")

    def cleanup(self) -> None:
        """Clean up edge manager resources."""
        super().cleanup()
        logger.debug(f"EdgeManager cleaned up for graph '{self.graph.name}'")

    def add_edge(
        self, source: str, target: str, validate_nodes: bool = True
    ) -> "BaseGraph":
        """Add a direct edge between two nodes.

        Args:
            source: Name of the source node
            target: Name of the target node
            validate_nodes: Whether to validate that nodes exist

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If nodes don't exist (when validate_nodes=True)
            ValueError: If edge already exists

        Example:
            Add edge between existing nodes::

                edge_manager.add_edge("start", "process")

            Add edge without validation (for dynamic creation)::

                edge_manager.add_edge("future_node", "end", validate_nodes=False)
        """
        if not self._initialized:
            raise RuntimeError("EdgeManager not initialized")

        # Validate nodes exist if requested
        if validate_nodes:
            self._validate_nodes_exist(source, target)

        # Check for duplicate edge
        edge = (source, target)
        if edge in self.graph.edges:
            raise ValueError(f"Edge from '{source}' to '{target}' already exists")

        # Add edge to graph
        self.graph.edges.append(edge)

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        logger.debug(
            f"Added edge '{source}' -> '{target}' to graph '{self.graph.name}'"
        )

        return self.graph

    def remove_edge(self, source: str, target: Optional[str] = None) -> "BaseGraph":
        """Remove edge(s) from the graph.

        Args:
            source: Name of the source node
            target: Name of the target node. If None, removes all edges from source

        Returns:
            Reference to parent graph for method chaining

        Raises:
            ValueError: If specified edge doesn't exist

        Example:
            Remove specific edge::

                edge_manager.remove_edge("start", "process")

            Remove all edges from a node::

                edge_manager.remove_edge("old_node")
        """
        if not self._initialized:
            raise RuntimeError("EdgeManager not initialized")

        if target is None:
            # Remove all edges from source
            initial_count = len(self.graph.edges)
            self.graph.edges = [edge for edge in self.graph.edges if edge[0] != source]
            removed_count = initial_count - len(self.graph.edges)

            if removed_count == 0:
                raise ValueError(f"No edges found from node '{source}'")

            logger.debug(
                f"Removed {removed_count} edges from '{source}' in graph '{self.graph.name}'"
            )
        else:
            # Remove specific edge
            edge = (source, target)
            if edge not in self.graph.edges:
                raise ValueError(f"Edge from '{source}' to '{target}' not found")

            self.graph.edges.remove(edge)

            logger.debug(
                f"Removed edge '{source}' -> '{target}' from graph '{self.graph.name}'"
            )

        # Update graph metadata
        self.graph.updated_at = self._get_current_time()

        return self.graph

    def get_edges(
        self, source: Optional[str] = None, target: Optional[str] = None
    ) -> List[Edge]:
        """Get edges matching the specified criteria.

        Args:
            source: Filter by source node. If None, include all sources
            target: Filter by target node. If None, include all targets

        Returns:
            List of edges matching the criteria

        Example:
            Get all edges::

                all_edges = edge_manager.get_edges()

            Get outgoing edges from a node::

                outgoing = edge_manager.get_edges(source="start")

            Get incoming edges to a node::

                incoming = edge_manager.get_edges(target="end")

            Get specific edge::

                specific = edge_manager.get_edges(source="start", target="end")
        """
        edges = self.graph.edges.copy()

        if source is not None:
            edges = [edge for edge in edges if edge[0] == source]

        if target is not None:
            edges = [edge for edge in edges if edge[1] == target]

        return edges

    def get_outgoing_edges(self, node_name: str) -> List[Edge]:
        """Get all outgoing edges from a node.

        Args:
            node_name: Name of the source node

        Returns:
            List of edges originating from the node
        """
        return self.get_edges(source=node_name)

    def get_incoming_edges(self, node_name: str) -> List[Edge]:
        """Get all incoming edges to a node.

        Args:
            node_name: Name of the target node

        Returns:
            List of edges terminating at the node
        """
        return self.get_edges(target=node_name)

    def has_edge(self, source: str, target: str) -> bool:
        """Check if an edge exists between two nodes.

        Args:
            source: Name of the source node
            target: Name of the target node

        Returns:
            True if edge exists, False otherwise
        """
        return (source, target) in self.graph.edges

    def get_edge_count(self) -> int:
        """Get total number of edges in the graph."""
        return len(self.graph.edges)

    def find_dangling_edges(self) -> List[Edge]:
        """Find edges that reference non-existent nodes.

        Returns:
            List of edges with missing source or target nodes

        Example:
            Check for connectivity issues::

                dangling = edge_manager.find_dangling_edges()
                if dangling:
                    print(f"Found {len(dangling)} dangling edges")
                    for source, target in dangling:
                        print(f"  {source} -> {target}")
        """
        dangling_edges = []
        node_names = set(self.graph.nodes.keys())

        # Add special nodes that are always valid
        valid_nodes = node_names | {"START", "END", "__start__", "__end__"}

        for source, target in self.graph.edges:
            if source not in valid_nodes or target not in valid_nodes:
                dangling_edges.append((source, target))

        return dangling_edges

    def get_connected_components(self) -> List[List[str]]:
        """Find all connected components in the graph.

        Returns:
            List of connected components, each as a list of node names

        Note:
            This treats edges as undirected for connectivity analysis
        """
        if not self.graph.nodes:
            return []

        # Build undirected adjacency list
        adjacency = {node: set() for node in self.graph.nodes}

        for source, target in self.graph.edges:
            if source in adjacency and target in adjacency:
                adjacency[source].add(target)
                adjacency[target].add(source)

        # Find connected components using DFS
        visited = set()
        components = []

        for node in self.graph.nodes:
            if node not in visited:
                component = self._dfs_component(node, adjacency, visited)
                components.append(component)

        return components

    def get_isolated_nodes(self) -> List[str]:
        """Find nodes with no incoming or outgoing edges.

        Returns:
            List of node names that are completely isolated
        """
        connected_nodes = set()

        for source, target in self.graph.edges:
            connected_nodes.add(source)
            connected_nodes.add(target)

        all_nodes = set(self.graph.nodes.keys())
        isolated = all_nodes - connected_nodes

        return list(isolated)

    def validate_state(self) -> List[str]:
        """Validate the edge manager state.

        Returns:
            List of validation error messages
        """
        errors = super().validate_state()

        # Check for dangling edges
        dangling = self.find_dangling_edges()
        if dangling:
            errors.append(f"Found {len(dangling)} dangling edges")

        # Check for duplicate edges
        edge_set = set()
        duplicates = []
        for edge in self.graph.edges:
            if edge in edge_set:
                duplicates.append(edge)
            else:
                edge_set.add(edge)

        if duplicates:
            errors.append(f"Found {len(duplicates)} duplicate edges")

        return errors

    def _validate_nodes_exist(self, source: str, target: str) -> None:
        """Validate that source and target nodes exist."""
        # Allow special LangGraph nodes
        special_nodes = {"START", "END", "__start__", "__end__"}

        if source not in self.graph.nodes and source not in special_nodes:
            raise ValueError(f"Source node '{source}' not found in graph")

        if target not in self.graph.nodes and target not in special_nodes:
            raise ValueError(f"Target node '{target}' not found in graph")

    def _dfs_component(
        self, start_node: str, adjacency: Dict[str, set], visited: set
    ) -> List[str]:
        """Depth-first search to find connected component."""
        component = []
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                component.append(node)

                # Add unvisited neighbors
                for neighbor in adjacency.get(node, set()):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return component

    def _get_current_time(self):
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now()

    def get_component_info(self) -> Dict[str, Any]:
        """Get detailed component information."""
        base_info = super().get_component_info()

        # Calculate edge statistics
        isolated_nodes = self.get_isolated_nodes()
        dangling_edges = self.find_dangling_edges()
        connected_components = self.get_connected_components()

        base_info.update(
            {
                "total_edges": self.get_edge_count(),
                "isolated_nodes": len(isolated_nodes),
                "dangling_edges": len(dangling_edges),
                "connected_components": len(connected_components),
                "largest_component_size": (
                    max(len(comp) for comp in connected_components)
                    if connected_components
                    else 0
                ),
            }
        )

        return base_info
