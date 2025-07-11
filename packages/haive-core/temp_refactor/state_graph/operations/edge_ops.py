"""Edge operations for the state graph system.

This module provides operations for adding, removing, and managing
edges in a graph.
"""

import logging
from datetime import datetime
from typing import List, Optional, Tuple

from haive.core.graph.state_graph.base.graph_base import GraphBase

# Set up logging
logger = logging.getLogger(__name__)


class EdgeOperations:
    """Operations for managing edges in a graph.

    This class provides methods for adding, removing, and
    querying edges in a graph.
    """

    @staticmethod
    def add_edge(graph: GraphBase, source: str, target: str) -> GraphBase:
        """Add a direct edge to the graph.

        Args:
            graph: Graph to add the edge to
            source: Source node name
            target: Target node name

        Returns:
            Updated graph
        """
        # Validate source and target
        if source != "START" and source not in graph.nodes:
            raise ValueError(f"Source node '{source}' not found in graph")
        if target != "END" and target not in graph.nodes:
            raise ValueError(f"Target node '{target}' not found in graph")

        # Create edge
        edge = (source, target)

        # Check if edge already exists
        if edge in graph.edges:
            logger.warning(f"Edge {source} -> {target} already exists in graph")
            return graph

        # Add edge
        graph.edges.append(edge)
        logger.debug(f"Added edge {source} -> {target}")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def remove_edge(
        graph: GraphBase, source: str, target: str | None = None
    ) -> GraphBase:
        """Remove an edge from the graph.

        Args:
            graph: Graph to remove the edge from
            source: Source node name
            target: Target node name (if None, removes all edges from source)

        Returns:
            Updated graph
        """
        if target:
            # Remove specific direct edge
            graph.edges = [
                edge
                for edge in graph.edges
                if not (edge[0] == source and edge[1] == target)
            ]
            logger.debug(f"Removed edge {source} -> {target}")
        else:
            # Remove all edges from source
            original_count = len(graph.edges)
            graph.edges = [edge for edge in graph.edges if edge[0] != source]
            removed_count = original_count - len(graph.edges)
            logger.debug(f"Removed {removed_count} edges from {source}")

        # Update graph timestamp
        graph.updated_at = datetime.now()

        return graph

    @staticmethod
    def get_edges(
        graph: GraphBase,
        source: str | None = None,
        target: str | None = None,
        include_branches: bool = True,
    ) -> list[tuple[str, str]]:
        """Get edges matching criteria.

        Args:
            graph: Graph to query
            source: Filter by source node (optional)
            target: Filter by target node (optional)
            include_branches: Include edges from branches

        Returns:
            List of matching edges as (source, target) tuples
        """
        result = []

        # Direct edges
        for edge_source, edge_target in graph.edges:
            # Apply filters
            source_match = source is None or edge_source == source
            target_match = target is None or edge_target == target

            if source_match and target_match:
                result.append((edge_source, edge_target))

        # Branch-based edges
        if include_branches:
            for branch in graph.branches.values():
                # Check source filter
                if source is not None and branch.source_node != source:
                    continue

                # Add all destinations that match target filter
                for dest in branch.destinations.values():
                    if target is None or dest == target:
                        result.append((branch.source_node, dest))

                # Check default destination
                if branch.default and (target is None or branch.default == target):
                    result.append((branch.source_node, branch.default))

        return result

    @staticmethod
    def find_all_paths(
        graph: GraphBase,
        start_node: str = "START",
        end_node: str = "END",
        max_depth: int = 100,
        include_loops: bool = False,
    ) -> list[list[str]]:
        """Find all possible paths between two nodes.

        Args:
            graph: Graph to search in
            start_node: Starting node (defaults to START)
            end_node: Ending node (defaults to END)
            max_depth: Maximum path depth to prevent infinite loops
            include_loops: Whether to include paths with loops/cycles

        Returns:
            List of paths (each path is a list of node names)
        """
        paths = []
        visited = set()

        # Stack-based DFS with path tracking
        stack = [(start_node, [start_node])]

        while stack:
            current, path = stack.pop()

            # Check if we reached the end
            if current == end_node:
                paths.append(path)
                continue

            # Limit path depth to prevent inf loops
            if len(path) > max_depth:
                continue

            # Skip already visited nodes if not including loops
            if not include_loops and current in visited:
                continue

            # Mark as visited
            visited.add(current)

            # Follow direct edges
            for src, dst in graph.edges:
                if src == current:
                    # Skip visited nodes unless we're including loops
                    if not include_loops and dst in visited:
                        continue
                    stack.append((dst, [*path, dst]))

            # Follow branch destinations
            for branch in graph.branches.values():
                if branch.source_node == current:
                    # Add all possible destinations
                    for dest in set(branch.destinations.values()):
                        if not include_loops and dest in visited:
                            continue
                        stack.append((dest, [*path, dest]))

                    # Add default if different
                    if (
                        branch.default
                        and branch.default not in branch.destinations.values()
                    ):
                        if not include_loops and branch.default in visited:
                            continue
                        stack.append((branch.default, [*path, branch.default]))

        return paths

    @staticmethod
    def has_path(graph: GraphBase, source: str, target: str) -> bool:
        """Check if there is a path between source and target nodes.

        Args:
            graph: Graph to search in
            source: Source node name
            target: Target node name

        Returns:
            True if path exists, False otherwise
        """
        # Simple BFS implementation
        visited = set()
        queue = [source]

        while queue:
            current = queue.pop(0)

            if current == target:
                return True

            if current in visited:
                continue

            visited.add(current)

            # Find all outgoing connections including branches
            outgoing = EdgeOperations.get_edges(
                graph, source=current, include_branches=True
            )
            for _, dest in outgoing:
                if dest not in visited:
                    queue.append(dest)

        return False
