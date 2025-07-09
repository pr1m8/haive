"""
Main graph implementation for the Haive framework.

This module provides the StateGraph class, which combines all
the components into a complete graph implementation.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from pydantic import Field

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base.graph_base import GraphBase
from haive.core.graph.state_graph.mixins.compilation_mixin import CompilationMixin
from haive.core.graph.state_graph.mixins.schema_mixin import SchemaMixin
from haive.core.graph.state_graph.mixins.validation_mixin import ValidationMixin

# Set up logging
logger = logging.getLogger(__name__)


class StateGraph(GraphBase, ValidationMixin, CompilationMixin, SchemaMixin):
    """
    Main graph implementation for the Haive framework.

    This class combines the base graph functionality with validation,
    compilation tracking, and schema management to provide a complete
    graph implementation.
    """

    # Configuration options
    allow_cycles: bool = Field(
        default=False, description="Whether to allow cycles in the graph"
    )
    require_end_path: bool = Field(
        default=True, description="Whether all nodes must have a path to END"
    )

    def __init__(self, **data):
        """
        Initialize a StateGraph.

        Args:
            **data: Keyword arguments for graph initialization
        """
        super().__init__(**data)

        # Initialize the _compiled_graph attribute for CompilationMixin
        self._compiled_graph = None

    def add_node(self, node_name: str, function: Callable, **kwargs) -> "StateGraph":
        """
        Add a node to the graph with function.

        Args:
            node_name: Name for the node
            function: Function or callable for the node
            **kwargs: Additional node properties

        Returns:
            Self for method chaining
        """
        # Store the node
        self.nodes[node_name] = function

        # If function has a node_type attribute, use it
        node_type = getattr(function, "node_type", NodeType.CALLABLE)

        # Track the node type
        self.node_types[node_name] = node_type

        # Track the change for compilation
        self.track_node_change(node_name, "add")

        return self

    def remove_node(self, node_name: str) -> "StateGraph":
        """
        Remove a node from the graph.

        Args:
            node_name: Name of the node to remove

        Returns:
            Self for method chaining
        """
        # Check if node exists
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Remove node
        del self.nodes[node_name]

        # Remove from node_types if tracked
        if node_name in self.node_types:
            del self.node_types[node_name]

        # Remove from subgraphs if it's a subgraph
        if node_name in self.subgraphs:
            del self.subgraphs[node_name]

        # Remove associated direct edges
        self.edges = [
            edge for edge in self.edges if edge[0] != node_name and edge[1] != node_name
        ]

        # Remove associated branches
        branch_ids_to_remove = []
        for branch_id, branch in self.branches.items():
            if branch.source_node == node_name:
                branch_ids_to_remove.append(branch_id)

        for branch_id in branch_ids_to_remove:
            del self.branches[branch_id]

        # Update any branch destinations that pointed to this node
        for branch in self.branches.values():
            for condition, target in list(branch.destinations.items()):
                if target == node_name:
                    # Remove or set to default
                    del branch.destinations[condition]

            # Update default if needed
            if branch.default == node_name:
                branch.default = "END"

        # Track the change for compilation
        self.track_node_change(node_name, "remove")

        return self

    def add_edge(self, source: str, target: str) -> "StateGraph":
        """
        Add a direct edge to the graph.

        Args:
            source: Source node name
            target: Target node name

        Returns:
            Self for method chaining
        """
        # Validate source and target
        if source != "START" and source not in self.nodes:
            raise ValueError(f"Source node '{source}' not found in graph")
        if target != "END" and target not in self.nodes:
            raise ValueError(f"Target node '{target}' not found in graph")

        # Create edge
        edge = (source, target)

        # Check if edge already exists
        if edge in self.edges:
            logger.warning(f"Edge {source} -> {target} already exists in graph")
            return self

        # Add edge
        self.edges.append(edge)

        # Track the change for compilation
        self.track_edge_change(source, target, "add")

        return self

    def remove_edge(self, source: str, target: Optional[str] = None) -> "StateGraph":
        """
        Remove an edge from the graph.

        Args:
            source: Source node name
            target: Target node name (if None, removes all edges from source)

        Returns:
            Self for method chaining
        """
        original_edge_count = len(self.edges)

        if target:
            # Remove specific direct edge
            self.edges = [
                edge
                for edge in self.edges
                if not (edge[0] == source and edge[1] == target)
            ]

            # Track the change for compilation if edge was removed
            if len(self.edges) < original_edge_count:
                self.track_edge_change(source, target, "remove")
        else:
            # Remove all edges from source
            removed_edges = []
            for s, t in self.edges:
                if s == source:
                    removed_edges.append((s, t))

            self.edges = [edge for edge in self.edges if edge[0] != source]

            # Track the changes for compilation
            for s, t in removed_edges:
                self.track_edge_change(s, t, "remove")

        return self

    def add_conditional_edges(
        self,
        source: str,
        condition: Callable,
        destinations: Dict[Any, str],
        default: str = "END",
    ) -> "StateGraph":
        """
        Add conditional edges from a source node.

        Args:
            source: Source node name
            condition: Function that returns a key for destinations
            destinations: Dictionary mapping condition results to target nodes
            default: Default destination if no condition matches

        Returns:
            Self for method chaining
        """
        # Validate source node
        if source != "START" and source not in self.nodes:
            raise ValueError(f"Source node '{source}' not found in graph")

        # Validate destination nodes
        for dest_node in destinations.values():
            if dest_node != "END" and dest_node not in self.nodes:
                raise ValueError(f"Destination node '{dest_node}' not found in graph")

        # Create a branch ID
        branch_id = str(id(condition))

        # Create a branch object
        from haive.core.graph.branches.types import BranchMode

        branch = Branch(
            id=branch_id,
            name=f"branch_{branch_id}",
            source_node=source,
            function=condition,
            destinations=destinations,
            default=default,
            mode=BranchMode.FUNCTION,
        )

        # Add to branches
        self.branches[branch_id] = branch

        # Track the change for compilation
        self.track_branch_change(branch_id, "add")

        return self

    def set_entry_point(self, node_name: str) -> "StateGraph":
        """
        Set an entry point of the graph.

        Args:
            node_name: Name of the node to set as an entry point

        Returns:
            Self for method chaining
        """
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Store the entry point in the list if not already there
        if node_name not in self.entry_points:
            self.entry_points.append(node_name)

        # For backward compatibility
        self.entry_point = node_name

        # Add edge from START to entry point if not already present
        edge = ("START", node_name)
        if edge not in self.edges:
            self.edges.append(edge)
            self.track_edge_change("START", node_name, "add")

        return self

    def set_finish_point(self, node_name: str) -> "StateGraph":
        """
        Set a finish point of the graph.

        Args:
            node_name: Name of the node to set as a finish point

        Returns:
            Self for method chaining
        """
        if node_name not in self.nodes:
            raise ValueError(f"Node '{node_name}' not found in graph")

        # Store the finish point in the list if not already there
        if node_name not in self.finish_points:
            self.finish_points.append(node_name)

        # For backward compatibility
        self.finish_point = node_name

        # Add edge from finish point to END if not already present
        edge = (node_name, "END")
        if edge not in self.edges:
            self.edges.append(edge)
            self.track_edge_change(node_name, "END", "add")

        return self

    def to_langgraph(self) -> Any:
        """
        Convert to a LangGraph StateGraph.

        Returns:
            LangGraph StateGraph
        """
        from langgraph.graph import StateGraph as LangGraphStateGraph

        # Use provided schema
        schema = self.state_schema or dict

        # Create StateGraph with the schema
        lang_graph = LangGraphStateGraph(schema)

        # Add nodes
        for node_name, node in self.nodes.items():
            # Skip None nodes
            if node is None:
                continue

            # Skip special nodes (START/END)
            if node_name in ["START", "END"]:
                continue

            # Add the node
            lang_graph.add_node(node_name, node)

        # Add edges
        for source, target in self.edges:
            lang_graph.add_edge(source, target)

        # Add branches
        for _branch_id, branch in self.branches.items():
            source = branch.source_node

            # Extract condition function
            condition = getattr(branch, "function", branch)

            # Extract destinations
            destinations = branch.destinations

            # If function has __call__ method, use it
            if not callable(condition) and callable(condition):
                condition = condition.__call__

            # Add conditional edges
            lang_graph.add_conditional_edges(source, condition, destinations)

        return lang_graph

    def visualize(
        self,
        include_subgraphs: bool = True,
        highlight_nodes: Optional[List[str]] = None,
        highlight_paths: Optional[List[List[str]]] = None,
        max_depth: int = 3,
        show_node_type: bool = True,
        theme: str = "default",
        output_path: Optional[str] = None,
        save_png: bool = False,
        width: str = "100%",
    ) -> str:
        """
        Generate and display a visualization of the graph.

        Args:
            include_subgraphs: Whether to include subgraphs
            highlight_nodes: List of nodes to highlight
            highlight_paths: List of paths to highlight
            max_depth: Maximum depth for subgraph rendering
            show_node_type: Whether to show node types
            theme: Mermaid theme to use
            output_path: Path to save the diagram
            save_png: Whether to save as PNG
            width: Width of displayed diagram

        Returns:
            The generated Mermaid code
        """
        # Import here to avoid circular imports
        from haive.core.graph.state_graph.visualization import MermaidGenerator
        from haive.core.utils.mermaid_utils import display_mermaid

        # Combine nodes from highlight_paths with highlight_nodes
        all_highlight_nodes = highlight_nodes or []

        if highlight_paths:
            for path in highlight_paths:
                all_highlight_nodes.extend(path)

        # Generate the Mermaid code
        mermaid_code = MermaidGenerator.generate(
            graph=self,
            include_subgraphs=include_subgraphs,
            highlight_nodes=all_highlight_nodes if all_highlight_nodes else None,
            max_depth=max_depth,
            show_node_type=show_node_type,
            theme=theme,
        )

        # Display the diagram
        display_mermaid(
            mermaid_code, output_path=output_path, save_png=save_png, width=width
        )

        return mermaid_code
