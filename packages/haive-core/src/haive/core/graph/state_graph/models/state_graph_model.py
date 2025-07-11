from collections import defaultdict
from typing import Any, ClassVar, Dict, Generic, List, Optional, Set, Tuple, TypeVar

from pydantic import Field, computed_field, model_validator

from haive.core.graph.state_graph.base import SerializableModel
from haive.core.graph.state_graph.models.branch_model import BranchModel
from haive.core.graph.state_graph.models.edge_model import EdgeModel
from haive.core.graph.state_graph.models.node_model import NodeModel
from haive.core.graph.state_graph.models.type_ref import TypeReference

TNode = TypeVar("TNode", bound=Any)


class GraphModel(SerializableModel, Generic[TNode]):
    """Serializable representation of a state graph with modification methods."""

    # Basic properties
    edges: Set[Tuple[str, str]] = Field(
        default_factory=set, description="Standard edges"
    )
    waiting_edges: Set[Tuple[Tuple[str, ...], str]] = Field(
        default_factory=set, description="Waiting edges"
    )
    compiled: bool = Field(default=False, description="Compilation status")

    # Entry and exit points
    entry_point: Optional[str] = Field(
        default=None, description="Entry point node name"
    )
    finish_point: Optional[str] = Field(
        default=None, description="Finish point node name"
    )

    # Schemas
    schema: Optional[TypeReference] = Field(
        default=None, description="State schema type"
    )
    input_schema: Optional[TypeReference] = Field(
        default=None, description="Input schema type"
    )
    output_schema: Optional[TypeReference] = Field(
        default=None, description="Output schema type"
    )
    config_schema: Optional[TypeReference] = Field(
        default=None, description="Config schema type"
    )

    # Nodes and branches - using our models
    nodes: Dict[str, NodeModel[TNode]] = Field(
        default_factory=dict, description="Node specifications"
    )
    branches: Dict[str, Dict[str, BranchModel]] = Field(
        default_factory=lambda: defaultdict(dict), description="Branch specifications"
    )

    # Additional metadata
    version: str = Field(default="1.0.0", description="Graph format version")

    __model_type__: ClassVar[str] = "graph"
    __abstract__ = False

    # Private attributes
    _reserved_nodes: ClassVar[List[str]] = ["__start__", "__end__"]

    @computed_field
    @property
    def node_count(self) -> int:
        """Get the number of nodes in the graph."""
        return len(self.nodes)

    @computed_field
    @property
    def edge_count(self) -> int:
        """Get the number of edges in the graph."""
        return (
            len(self.edges)
            + len(self.waiting_edges)
            + sum(
                sum(1 for branch in branch_dict.values() if branch.ends or branch.then)
                for branch_dict in self.branches.values()
            )
        )

    @computed_field
    @property
    def all_edges(self) -> List[EdgeModel]:
        """Get all edges in the graph as EdgeModel objects."""
        result = []

        # Regular edges
        for src, dst in self.edges:
            result.append(EdgeModel.create_standard(src, dst))

        # Waiting edges
        for srcs, dst in self.waiting_edges:
            result.append(EdgeModel.create_waiting(list(srcs), dst))

        # Branch edges
        for src, branch_dict in self.branches.items():
            for branch_name, branch in branch_dict.items():
                if branch.ends:
                    for condition, target in branch.ends.items():
                        result.append(
                            EdgeModel.create_branch(src, target, branch_name, condition)
                        )
                if branch.then:
                    result.append(
                        EdgeModel.create_branch_then(src, branch.then, branch_name)
                    )

        return result

    @model_validator(mode="after")
    def validate_graph_structure(self) -> "GraphModel":
        """Validate the overall graph structure."""
        # Check that entry and finish points exist if set
        if self.entry_point and self.entry_point not in self.nodes:
            raise ValueError(
                f"Entry point '{self.entry_point}' references non-existent node"
            )

        if self.finish_point and self.finish_point not in self.nodes:
            raise ValueError(
                f"Finish point '{self.finish_point}' references non-existent node"
            )

        return self

    def add_node(self, name: str, node_spec: Any) -> "GraphModel":
        """Add a node to the graph."""
        if name in self._reserved_nodes:
            raise ValueError(f"Cannot add reserved node name: {name}")

        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")

        self.nodes[name] = NodeModel.from_node_spec(name, node_spec)
        self.mark_modified()
        return self

    def remove_node(self, name: str) -> "GraphModel":
        """Remove a node and all its connected edges and branches."""
        if name in self._reserved_nodes:
            raise ValueError(f"Cannot remove reserved node: {name}")

        if name not in self.nodes:
            raise ValueError(f"Node '{name}' does not exist")

        # Remove edges to/from this node
        self.edges = {
            (src, dst) for src, dst in self.edges if src != name and dst != name
        }

        # Remove waiting edges involving this node
        new_waiting_edges = set()
        for srcs, dst in self.waiting_edges:
            if dst != name and name not in srcs:
                new_waiting_edges.add((srcs, dst))
            elif dst != name:
                # Filter out this node from sources
                new_srcs = tuple(src for src in srcs if src != name)
                if new_srcs:
                    new_waiting_edges.add((new_srcs, dst))
        self.waiting_edges = new_waiting_edges

        # Remove branches from this node
        if name in self.branches:
            del self.branches[name]

        # Remove branches targeting this node
        for source, branch_dict in list(self.branches.items()):
            for branch_name, branch in list(branch_dict.items()):
                if branch.ends:
                    # Filter out ends that point to the removed node
                    branch.ends = {k: v for k, v in branch.ends.items() if v != name}

                    # Remove branch if it has no ends left
                    if not branch.ends and not branch.then:
                        branch_dict.pop(branch_name, None)

                # Remove branches with 'then' pointing to this node
                elif branch.then == name:
                    branch.then = None
                    if not branch.ends:
                        branch_dict.pop(branch_name, None)

            # Remove empty branch dictionaries
            if not branch_dict:
                self.branches.pop(source, None)

        # Update entry/finish points
        if self.entry_point == name:
            self.entry_point = None

        if self.finish_point == name:
            self.finish_point = None

        # Remove the node
        del self.nodes[name]

        self.mark_modified()
        return self

    def add_edge(self, source: str, target: str) -> "GraphModel":
        """Add an edge between two nodes."""
        # Special handling for reserved nodes
        if source not in self.nodes and source != "__start__":
            raise ValueError(f"Source node '{source}' does not exist")

        if target not in self.nodes and target != "__end__":
            raise ValueError(f"Target node '{target}' does not exist")

        # Add the edge
        self.edges.add((source, target))
        self.mark_modified()
        return self

    def add_sequence(self, nodes: List[Union[str, Tuple[str, Any]]]) -> "GraphModel":
        """
        Add a sequence of nodes that will be executed in order.

        Args:
            nodes: List of node names or (name, spec) tuples to add in sequence

        Returns:
            Self for method chaining
        """
        if not nodes:
            raise ValueError("Sequence requires at least one node")

        previous_name = None

        for node in nodes:
            if isinstance(node, tuple) and len(node) == 2:
                name, node_spec = node
            else:
                name = node
                node_spec = None

            # Add node if it doesn't exist and spec is provided
            if name not in self.nodes and node_spec is not None:
                self.add_node(name, node_spec)
            elif name not in self.nodes:
                raise ValueError(f"Node '{name}' does not exist and no spec provided")

            # Connect to previous node
            if previous_name is not None:
                self.add_edge(previous_name, name)

            previous_name = name

        self.mark_modified()
        return self

    @classmethod
    def from_state_graph(cls, graph: Any, name: str = "unnamed_graph") -> "GraphModel":
        """Create a GraphModel from a StateGraph."""
        model = cls(name=name)

        # Copy basic properties
        model.edges = set(graph.edges)
        model.waiting_edges = set(graph.waiting_edges)
        model.compiled = graph.compiled

        # Copy schemas
        if hasattr(graph, "schema"):
            model.schema = TypeReference.from_type(graph.schema)

        if hasattr(graph, "input"):
            model.input_schema = TypeReference.from_type(graph.input)

        if hasattr(graph, "output"):
            model.output_schema = TypeReference.from_type(graph.output)

        if hasattr(graph, "config_schema"):
            model.config_schema = TypeReference.from_type(graph.config_schema)

        # Copy nodes
        for name, node_spec in graph.nodes.items():
            model.nodes[name] = NodeModel.from_node_spec(name, node_spec)

        # Copy branches
        for source, branch_dict in graph.branches.items():
            for branch_name, branch in branch_dict.items():
                branch_model = BranchModel.from_branch(branch_name, source, branch)
                if branch_model:
                    model.branches[source][branch_name] = branch_model

        # Copy entry and finish points
        if hasattr(graph, "entry_point"):
            model.entry_point = graph.entry_point

        if hasattr(graph, "finish_point"):
            model.finish_point = graph.finish_point

        return model

    def validate(self) -> bool:
        """Validate the graph structure and return True if valid."""
        # Just trigger the validation and return True if no exception is raised
        self.validate_graph_structure()
        return True
