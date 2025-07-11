"""Subgraph registry for the state graph system.

This module provides the SubgraphRegistry class for managing subgraphs
in a graph.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field

from haive.core.graph.state_graph.base.graph_base import GraphBase
from haive.core.graph.state_graph.components.subgraph import Subgraph


class SubgraphRegistry(BaseModel):
    """Registry for managing subgraphs in a graph.

    This class provides a central registry for subgraphs,
    handling their registration, configuration, and retrieval.
    """

    subgraphs: dict[str, Subgraph] = Field(default_factory=dict)
    subgraph_mappings: dict[str, dict[str, dict[str, str]]] = Field(
        default_factory=dict
    )

    model_config = {"arbitrary_types_allowed": True}

    def register_subgraph(
        self,
        subgraph_name: str,
        graph: GraphBase,
        input_mapping: dict[str, str] | None = None,
        output_mapping: dict[str, str] | None = None,
        **kwargs
    ) -> Subgraph:
        """Register a subgraph.

        Args:
            subgraph_name: Name for the subgraph
            graph: Graph to register as a subgraph
            input_mapping: Optional mapping from parent graph to subgraph inputs
            output_mapping: Optional mapping from subgraph outputs to parent graph
            **kwargs: Additional metadata

        Returns:
            Registered Subgraph instance
        """
        # Create a Subgraph wrapper
        subgraph = Subgraph(
            name=subgraph_name,
            graph=graph,
            input_mapping=input_mapping or {},
            output_mapping=output_mapping or {},
            metadata=kwargs,
        )

        # Store the subgraph
        self.subgraphs[subgraph_name] = subgraph

        # Store mappings
        self.subgraph_mappings[subgraph_name] = {
            "input": input_mapping or {},
            "output": output_mapping or {},
        }

        return subgraph

    def unregister_subgraph(self, subgraph_name: str) -> None:
        """Unregister a subgraph.

        Args:
            subgraph_name: Name of the subgraph to unregister
        """
        if subgraph_name in self.subgraphs:
            del self.subgraphs[subgraph_name]

        if subgraph_name in self.subgraph_mappings:
            del self.subgraph_mappings[subgraph_name]

    def get_subgraph(self, subgraph_name: str) -> Subgraph | None:
        """Get a subgraph by name.

        Args:
            subgraph_name: Name of the subgraph

        Returns:
            Subgraph instance or None if not found
        """
        return self.subgraphs.get(subgraph_name)

    def get_all_subgraphs(self) -> dict[str, Subgraph]:
        """Get all registered subgraphs.

        Returns:
            Dictionary of subgraph name to Subgraph instance
        """
        return self.subgraphs

    def list_subgraphs(self) -> list[str]:
        """List all registered subgraph names.

        Returns:
            List of subgraph names
        """
        return list(self.subgraphs.keys())

    def get_mappings(self, subgraph_name: str) -> dict[str, dict[str, str]]:
        """Get the input/output mappings for a subgraph.

        Args:
            subgraph_name: Name of the subgraph

        Returns:
            Dictionary with 'input' and 'output' mapping dictionaries
        """
        return self.subgraph_mappings.get(subgraph_name, {"input": {}, "output": {}})
