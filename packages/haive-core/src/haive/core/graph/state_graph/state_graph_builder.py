from typing import Any, List, Optional, Tuple, Type, Union

from haive.core.graph.models.graph_model import GraphModel
from haive.core.graph.models.type_ref import TypeReference
from haive.core.graph.state_graph.pattern_registry import PatternRegistry


class GraphBuilder:
    """Builder for constructing graph models."""

    def __init__(self, name: str, state_schema: Optional[Type] = None):
        """
        Initialize a new graph builder.

        Args:
            name: Name of the graph
            state_schema: Optional state schema type
        """
        self.graph = GraphModel(name=name)

        if state_schema:
            self.graph.schema = TypeReference.from_type(state_schema)

    def add_node(self, name: str, node_spec: Any) -> "GraphBuilder":
        """
        Add a node to the graph.

        Args:
            name: Node name
            node_spec: Node specification

        Returns:
            Self for method chaining
        """
        self.graph.add_node(name, node_spec)
        return self

    def add_edge(self, source: str, target: str) -> "GraphBuilder":
        """
        Add an edge to the graph.

        Args:
            source: Source node name
            target: Target node name

        Returns:
            Self for method chaining
        """
        self.graph.add_edge(source, target)
        return self

    def add_waiting_edge(self, sources: List[str], target: str) -> "GraphBuilder":
        """
        Add a waiting edge to the graph.

        Args:
            sources: Source node names
            target: Target node name

        Returns:
            Self for method chaining
        """
        self.graph.add_waiting_edge(sources, target)
        return self

    def add_sequence(self, nodes: List[Union[str, Tuple[str, Any]]]) -> "GraphBuilder":
        """
        Add a sequence of nodes.

        Args:
            nodes: List of node names or (name, spec) tuples

        Returns:
            Self for method chaining
        """
        self.graph.add_sequence(nodes)
        return self

    def set_entry_point(self, node: str) -> "GraphBuilder":
        """
        Set the entry point for the graph.

        Args:
            node: Entry point node name

        Returns:
            Self for method chaining
        """
        if node not in self.graph.nodes:
            raise ValueError(f"Node '{node}' does not exist")

        self.graph.entry_point = node
        self.graph.mark_modified()
        return self

    def set_finish_point(self, node: str) -> "GraphBuilder":
        """
        Set the finish point for the graph.

        Args:
            node: Finish point node name

        Returns:
            Self for method chaining
        """
        if node not in self.graph.nodes:
            raise ValueError(f"Node '{node}' does not exist")

        self.graph.finish_point = node
        self.graph.mark_modified()
        return self

    def apply_pattern(self, pattern_name: str, **kwargs) -> "GraphBuilder":
        """
        Apply a pattern to the graph.

        Args:
            pattern_name: Name of the pattern to apply
            **kwargs: Pattern parameters

        Returns:
            Self for method chaining
        """
        # Get the pattern from the registry
        registry = PatternRegistry.get_instance()
        pattern = registry.get(None, pattern_name)

        if not pattern:
            raise ValueError(f"Pattern '{pattern_name}' not found")

        # Merge parameters with defaults
        parameters = pattern.parameters.copy()
        parameters.update(kwargs)

        # Resolve the apply function
        apply_func = pattern.apply_func.resolve()
        if not apply_func:
            raise ValueError(
                f"Could not resolve apply function for pattern '{pattern_name}'"
            )

        # Apply the pattern
        apply_func(self, **parameters)

        return self

    def build(self) -> GraphModel:
        """
        Build and validate the graph.

        Returns:
            The built graph model
        """
        self.graph.validate()
        return self.graph

    def register(self) -> GraphModel:
        """
        Build the graph and register it in the registry.

        Returns:
            The registered graph model
        """
from haive.core.graph.registry.graph_registry import GraphRegistry

        graph = self.build()
        registry = GraphRegistry.get_instance()
        return registry.register(graph)
