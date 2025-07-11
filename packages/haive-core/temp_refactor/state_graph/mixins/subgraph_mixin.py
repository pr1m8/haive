"""
Subgraph management mixin for the state graph system.

This module provides the SubgraphMixin class for managing subgraphs
in a graph.
"""

from typing import Dict, List, Optional

from pydantic import Field

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base.graph_base import GraphBase
from haive.core.graph.state_graph.components.subgraph import Subgraph
from haive.core.graph.state_graph.components.subgraph_registry import SubgraphRegistry


class SubgraphMixin:
    """
    Mixin that adds subgraph management capabilities to a graph.

    This mixin allows the graph to register, configure, and use
    subgraphs within the main graph.
    """

    _subgraph_registry: SubgraphRegistry = Field(default_factory=SubgraphRegistry)

    def add_subgraph(
        self,
        subgraph_name: str,
        graph: GraphBase,
        input_mapping: Optional[Dict[str, str]] = None,
        output_mapping: Optional[Dict[str, str]] = None,
        **kwargs
    ) -> "GraphBase":
        """
        Add a subgraph to the graph.

        Args:
            subgraph_name: Name for the subgraph
            graph: Graph to add as a subgraph
            input_mapping: Optional mapping from parent graph to subgraph inputs
            output_mapping: Optional mapping from subgraph outputs to parent graph
            **kwargs: Additional metadata

        Returns:
            Self for method chaining
        """
        # Register the subgraph
        subgraph = self._subgraph_registry.register_subgraph(
            subgraph_name, graph, input_mapping, output_mapping, **kwargs
        )

        # Add the subgraph as a node in the graph
        self.nodes[subgraph_name] = subgraph

        # Track node type
        self.node_types[subgraph_name] = NodeType.SUBGRAPH

        # Store in the subgraphs dictionary for backward compatibility
        self.subgraphs[subgraph_name] = graph

        # Track change if compilation tracking is enabled
        if hasattr(self, "track_node_change"):
            self.track_node_change(subgraph_name, "add")

        return self

    def remove_subgraph(self, subgraph_name: str) -> "GraphBase":
        """
        Remove a subgraph from the graph.

        Args:
            subgraph_name: Name of the subgraph to remove

        Returns:
            Self for method chaining
        """
        # Remove from nodes
        if subgraph_name in self.nodes:
            del self.nodes[subgraph_name]

        # Remove from node_types
        if subgraph_name in self.node_types:
            del self.node_types[subgraph_name]

        # Remove from subgraphs
        if subgraph_name in self.subgraphs:
            del self.subgraphs[subgraph_name]

        # Unregister from subgraph registry
        self._subgraph_registry.unregister_subgraph(subgraph_name)

        # Track change if compilation tracking is enabled
        if hasattr(self, "track_node_change"):
            self.track_node_change(subgraph_name, "remove")

        return self

    def get_subgraph(self, subgraph_name: str) -> Optional[Subgraph]:
        """
        Get a subgraph by name.

        Args:
            subgraph_name: Name of the subgraph

        Returns:
            Subgraph instance or None if not found
        """
        return self._subgraph_registry.get_subgraph(subgraph_name)

    def get_subgraph_graph(self, subgraph_name: str) -> Optional[GraphBase]:
        """
        Get the underlying graph for a subgraph.

        Args:
            subgraph_name: Name of the subgraph

        Returns:
            Graph instance or None if not found
        """
        subgraph = self.get_subgraph(subgraph_name)
        if subgraph:
            return subgraph.get_graph()
        return None

    def list_subgraphs(self) -> List[str]:
        """
        List all subgraph names.

        Returns:
            List of subgraph names
        """
        return self._subgraph_registry.list_subgraphs()

    def update_subgraph_mappings(
        self,
        subgraph_name: str,
        input_mapping: Optional[Dict[str, str]] = None,
        output_mapping: Optional[Dict[str, str]] = None,
    ) -> "GraphBase":
        """
        Update the input/output mappings for a subgraph.

        Args:
            subgraph_name: Name of the subgraph
            input_mapping: Updated input mapping (or None to keep current)
            output_mapping: Updated output mapping (or None to keep current)

        Returns:
            Self for method chaining
        """
        subgraph = self.get_subgraph(subgraph_name)
        if subgraph:
            if input_mapping is not None:
                subgraph.input_mapping = input_mapping

            if output_mapping is not None:
                subgraph.output_mapping = output_mapping

            # Update registry mappings
            current_mappings = self._subgraph_registry.get_mappings(subgraph_name)

            if input_mapping is not None:
                current_mappings["input"] = input_mapping

            if output_mapping is not None:
                current_mappings["output"] = output_mapping

            # Track change if compilation tracking is enabled
            if hasattr(self, "track_node_change"):
                self.track_node_change(subgraph_name, "update")

        return self

    def check_subgraphs_compilation(self) -> bool:
        """
        Check if any subgraphs need recompilation.

        Returns:
            True if any subgraph needs recompilation, False otherwise
        """
        for name in self.list_subgraphs():
            subgraph = self.get_subgraph(name)
            if subgraph and subgraph.needs_recompilation():
                return True
        return False
