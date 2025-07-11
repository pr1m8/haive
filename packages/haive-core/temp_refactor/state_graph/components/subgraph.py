"""Subgraph component for the state graph system.

This module provides the Subgraph class for encapsulating a subgraph
within a parent graph.
"""

from typing import Any, Dict, List, Optional, TypeVar

from pydantic import BaseModel, Field

from haive.core.graph.state_graph.base.graph_base import GraphBase

# Type variable for the state type
T = TypeVar("T")


class Subgraph(BaseModel):
    """Wrapper for a subgraph in a parent graph.

    This class encapsulates a subgraph and provides methods for
    interfacing between the parent graph and the subgraph.
    """

    name: str
    graph: GraphBase
    input_mapping: dict[str, str] = Field(default_factory=dict)
    output_mapping: dict[str, str] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)

    # Interface nodes
    entry_nodes: list[str] = Field(default_factory=list)
    exit_nodes: list[str] = Field(default_factory=list)

    model_config = {"arbitrary_types_allowed": True}

    def __call__(self, state: Any, config: Any | None = None) -> Any:
        """Make the subgraph callable for use in the parent graph.

        Args:
            state: State from the parent graph
            config: Configuration from the parent graph

        Returns:
            Processed state
        """
        # Map inputs from parent state to subgraph state
        subgraph_state = self._map_inputs(state)

        # Create a compiled version of the subgraph
        compiled_graph = (
            self.graph.compile() if hasattr(self.graph, "compile") else self.graph
        )

        # Invoke the subgraph
        result = compiled_graph.invoke(subgraph_state, config)

        # Map outputs back to parent state format
        return self._map_outputs(result, state)

    def _map_inputs(self, parent_state: Any) -> Any:
        """Map parent state to subgraph state.

        Args:
            parent_state: State from parent graph

        Returns:
            Mapped state for subgraph
        """
        # Handle different state types
        if isinstance(parent_state, dict):
            # Dictionary state
            subgraph_state = {}

            # Apply input mapping
            for parent_key, subgraph_key in self.input_mapping.items():
                if parent_key in parent_state:
                    subgraph_state[subgraph_key] = parent_state[parent_key]

            # Pass through unmapped fields
            if not self.input_mapping:
                subgraph_state = parent_state.copy()

            return subgraph_state

        if hasattr(parent_state, "__dict__"):
            # Object state
            from copy import deepcopy

            subgraph_state = deepcopy(parent_state)

            # Apply input mapping
            for parent_key, subgraph_key in self.input_mapping.items():
                if hasattr(parent_state, parent_key):
                    value = getattr(parent_state, parent_key)
                    setattr(subgraph_state, subgraph_key, value)

            return subgraph_state

        # Fallback for other types
        return parent_state

    def _map_outputs(self, subgraph_result: Any, parent_state: Any) -> Any:
        """Map subgraph result to parent state format.

        Args:
            subgraph_result: Result from subgraph
            parent_state: Original parent state

        Returns:
            Mapped result for parent graph
        """
        # Handle different state types
        if isinstance(parent_state, dict) and isinstance(subgraph_result, dict):
            # Dictionary state
            result = parent_state.copy()

            # Apply output mapping
            for subgraph_key, parent_key in self.output_mapping.items():
                if subgraph_key in subgraph_result:
                    result[parent_key] = subgraph_result[subgraph_key]

            # Pass through unmapped fields
            if not self.output_mapping:
                result.update(subgraph_result)

            return result

        if hasattr(parent_state, "__dict__") and hasattr(subgraph_result, "__dict__"):
            # Object state
            from copy import deepcopy

            result = deepcopy(parent_state)

            # Apply output mapping
            for subgraph_key, parent_key in self.output_mapping.items():
                if hasattr(subgraph_result, subgraph_key):
                    value = getattr(subgraph_result, subgraph_key)
                    setattr(result, parent_key, value)

            # Pass through unmapped fields if no mapping defined
            if not self.output_mapping:
                for key, value in subgraph_result.__dict__.items():
                    setattr(result, key, value)

            return result

        # Fallback for other types
        return subgraph_result

    def get_graph(self) -> GraphBase:
        """Get the underlying graph.

        Returns:
            Graph object
        """
        return self.graph

    def get_node_names(self) -> list[str]:
        """Get list of node names in the subgraph.

        Returns:
            List of node names
        """
        return list(self.graph.nodes.keys())

    def is_compiled(self) -> bool:
        """Check if the subgraph is compiled.

        Returns:
            True if compiled, False otherwise
        """
        if hasattr(self.graph, "is_compiled"):
            return self.graph.is_compiled
        if hasattr(self.graph, "needs_recompilation"):
            return not self.graph.needs_recompilation()
        return False

    def needs_recompilation(self) -> bool:
        """Check if the subgraph needs recompilation.

        Returns:
            True if recompilation is needed, False otherwise
        """
        if hasattr(self.graph, "needs_recompilation"):
            return self.graph.needs_recompilation()
        return True
