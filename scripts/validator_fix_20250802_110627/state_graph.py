from collections.abc import Callable
from datetime import datetime
from typing import Any, ClassVar, Generic, Self, TypeVar
from uuid import uuid4

from haive.core.graph.state_graph.branch_spec import BranchSpec
from haive.core.graph.state_graph.node_spec import NodeSpec
from haive.core.graph.state_graph.serializer import FunctionReference, TypeReference
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    PrivateAttr,
    computed_field,
    field_validator,
    model_validator,
)

TNode = TypeVar("TNode", bound=Any)


class StateGraphSerializable(BaseModel, Generic[TNode]):
    """Enhanced serializable representation of a StateGraph with modification methods.

    This class provides a serializable representation of a LangGraph StateGraph with
    methods for modifying the graph structure and validating its correctness.

    Attributes:
        id: Unique identifier for this graph
        name: Name of the graph
        edges: Set of edges as (source, target) pairs
        waiting_edges: Set of waiting edges as (sources, target) pairs
        compiled: Whether the graph has been compiled
        entry_point: Entry point node name
        finish_point: Finish point node name
        schema: Reference to the state schema type
        input_schema: Reference to the input schema type
        output_schema: Reference to the output schema type
        config_schema: Reference to the config schema type
        nodes: Dictionary of node specifications
        branches: Dictionary of branch specifications
        metadata: Additional metadata for the graph
        version: Version of the graph format
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: str = Field(
        default_factory=lambda: str(uuid4()), description="Unique identifier"
    )
    name: str = Field(default="unnamed_graph", description="Graph name")
    edges: set[tuple[str, str]] = Field(default_factory=set, description="Graph edges")
    waiting_edges: set[tuple[tuple[str, ...], str]] = Field(
        default_factory=set, description="Edges that wait for multiple source nodes"
    )
    compiled: bool = Field(
        default=False, description="Whether the graph has been compiled"
    )
    entry_point: str | None = Field(default=None, description="Entry point node name")
    finish_point: str | None = Field(default=None, description="Finish point node name")
    schema: TypeReference | None = Field(default=None, description="State schema type")
    input_schema: TypeReference | None = Field(
        default=None, description="Input schema type"
    )
    output_schema: TypeReference | None = Field(
        default=None, description="Output schema type"
    )
    config_schema: TypeReference | None = Field(
        default=None, description="Config schema type"
    )
    nodes: dict[str, NodeSpec[TNode]] = Field(
        default_factory=dict, description="Node specifications"
    )
    branches: dict[str, dict[str, BranchSpec]] = Field(
        default_factory=lambda: defaultdict(dict), description="Branch specifications"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    version: str = Field(default="1.0.0", description="Graph format version")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.now, description="Last update timestamp"
    )
    _modified: bool = PrivateAttr(default=False)
    _reserved_nodes: ClassVar[list[str]] = ["__start__", "__end__"]
    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
        str_strip_whitespace=True,
        validate_assignment=True,
        json_encoders={datetime: lambda dt: dt.isoformat()},
    )

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self._modified = False

    @field_validator("name")
    def validate_name(cls, v: str) -> str:
        """Validate graph name."""
        if not v:
            raise ValueError("Graph name cannot be empty")
        return v

    @model_validator(mode="after")
    def validate_graph_structure(self) -> Self:
        """Validate the overall graph structure."""
        if self.entry_point and self.entry_point not in self.nodes:
            raise ValueError(
                f"Entry point '{self.entry_point}' references non-existent node"
            )
        if self.finish_point and self.finish_point not in self.nodes:
            raise ValueError(
                f"Finish point '{self.finish_point}' references non-existent node"
            )
        return self

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
            + sum((len(branch_dict) for branch_dict in self.branches.values()))
        )

    @computed_field
    @property
    def all_edges(self) -> list[dict[str, Any]]:
        """Get all edges in the graph in a structured format."""
        result = []
        for src, dst in self.edges:
            result.append({"type": "edge", "source": src, "target": dst})
        for srcs, dst in self.waiting_edges:
            result.append(
                {"type": "waiting_edge", "sources": list(srcs), "target": dst}
            )
        for src, branch_dict in self.branches.items():
            for branch_name, branch in branch_dict.items():
                if branch.ends:
                    for condition, target in branch.ends.items():
                        result.append(
                            {
                                "type": "branch_edge",
                                "source": src,
                                "target": target,
                                "branch": branch_name,
                                "condition": condition,
                            }
                        )
                if branch.then:
                    result.append(
                        {
                            "type": "branch_then",
                            "source": src,
                            "target": branch.then,
                            "branch": branch_name,
                        }
                    )
        return result

    def mark_modified(self) -> None:
        """Mark the graph as modified and update the updated_at timestamp."""
        self._modified = True
        self.updated_at = datetime.now()

    def add_node(self, name: str, node_spec: Any) -> "StateGraphSerializable":
        """Add a node to the graph."""
        if name in self._reserved_nodes:
            raise ValueError(f"Cannot add reserved node name: {name}")
        if name in self.nodes:
            raise ValueError(f"Node '{name}' already exists")
        self.nodes[name] = NodeSpec(name=name, spec=node_spec)
        self.mark_modified()
        return self

    def remove_node(self, name: str) -> "StateGraphSerializable":
        """Remove a node and all its connected edges and branches."""
        if name in self._reserved_nodes:
            raise ValueError(f"Cannot remove reserved node: {name}")
        if name not in self.nodes:
            raise ValueError(f"Node '{name}' does not exist")
        self.edges = {(src, dst) for src, dst in self.edges if name not in (src, dst)}
        new_waiting_edges = set()
        for srcs, dst in self.waiting_edges:
            if dst != name and name not in srcs:
                new_waiting_edges.add((srcs, dst))
            elif dst != name:
                new_srcs = tuple((src for src in srcs if src != name))
                if new_srcs:
                    new_waiting_edges.add((new_srcs, dst))
        self.waiting_edges = new_waiting_edges
        if name in self.branches:
            del self.branches[name]
        for source, branch_dict in list(self.branches.items()):
            for branch_name, branch in list(branch_dict.items()):
                if branch.ends:
                    branch.ends = {k: v for k, v in branch.ends.items() if v != name}
                    if not branch.ends and (not branch.then):
                        branch_dict.pop(branch_name, None)
                elif branch.then == name:
                    branch.then = None
                    if not branch.ends:
                        branch_dict.pop(branch_name, None)
            if not branch_dict:
                self.branches.pop(source, None)
        if self.entry_point == name:
            self.entry_point = None
        if self.finish_point == name:
            self.finish_point = None
        del self.nodes[name]
        self.mark_modified()
        return self

    def add_edge(self, source: str, target: str) -> "StateGraphSerializable":
        """Add an edge between two nodes."""
        if source not in self.nodes and source != "__start__":
            raise ValueError(f"Source node '{source}' does not exist")
        if target not in self.nodes and target != "__end__":
            raise ValueError(f"Target node '{target}' does not exist")
        self.edges.add((source, target))
        self.mark_modified()
        return self

    def remove_edge(self, source: str, target: str) -> "StateGraphSerializable":
        """Remove an edge between two nodes."""
        if (source, target) not in self.edges:
            raise ValueError(f"Edge from '{source}' to '{target}' does not exist")
        self.edges.remove((source, target))
        self.mark_modified()
        return self

    def add_waiting_edge(
        self, sources: list[str], target: str
    ) -> "StateGraphSerializable":
        """Add a waiting edge (edge that waits for multiple source nodes to complete)."""
        for source in sources:
            if source not in self.nodes and source not in self._reserved_nodes:
                raise ValueError(f"Source node '{source}' does not exist")
        if target not in self.nodes and target != "__end__":
            raise ValueError(f"Target node '{target}' does not exist")
        self.waiting_edges.add((tuple(sources), target))
        self.mark_modified()
        return self

    def remove_waiting_edge(
        self, sources: list[str], target: str
    ) -> "StateGraphSerializable":
        """Remove a waiting edge."""
        source_tuple = tuple(sources)
        if (source_tuple, target) not in self.waiting_edges:
            raise ValueError(
                f"Waiting edge from {sources} to '{target}' does not exist"
            )
        self.waiting_edges.remove((source_tuple, target))
        self.mark_modified()
        return self

    def set_entry_point(self, node: str) -> "StateGraphSerializable":
        """Set the entry point for the graph."""
        if node not in self.nodes:
            raise ValueError(f"Node '{node}' does not exist")
        self.entry_point = node
        self.mark_modified()
        return self

    def set_finish_point(self, node: str) -> "StateGraphSerializable":
        """Set the finish point for the graph."""
        if node not in self.nodes:
            raise ValueError(f"Node '{node}' does not exist")
        self.finish_point = node
        self.mark_modified()
        return self

    def add_sequence(
        self, nodes: list[str | tuple[str, Any]]
    ) -> "StateGraphSerializable":
        """Add a sequence of nodes that will be executed in order.

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
            if name not in self.nodes and node_spec is not None:
                self.add_node(name, node_spec)
            elif name not in self.nodes:
                raise ValueError(f"Node '{name}' does not exist and no spec provided")
            if previous_name is not None:
                self.add_edge(previous_name, name)
            previous_name = name
        self.mark_modified()
        return self

    def add_conditional_edge(
        self,
        source: str,
        condition_func: Callable | FunctionReference,
        targets: dict[str, str],
        then: str | None = None,
    ) -> "StateGraphSerializable":
        """Add a conditional edge from a source node to multiple targets.

        Args:
            source: Source node name
            condition_func: Function that determines routing
            targets: Mapping of condition values to target nodes
            then: Optional node to route to after condition routing

        Returns:
            Self for method chaining
        """
        if source not in self.nodes:
            raise ValueError(f"Source node '{source}' does not exist")
        for target in targets.values():
            if target not in self.nodes and target != "__end__":
                raise ValueError(f"Target node '{target}' does not exist")
        if then and then not in self.nodes and (then != "__end__"):
            raise ValueError(f"Then node '{then}' does not exist")
        branch_name = f"condition_{len(self.branches.get(source, {})) + 1}"
        branch = BranchSpec(
            name=branch_name,
            path=(
                FunctionReference.from_callable(condition_func)
                if not isinstance(condition_func, FunctionReference)
                else condition_func
            ),
            ends=targets,
            then=then,
            branch_type="conditional",
        )
        if source not in self.branches:
            self.branches[source] = {}
        self.branches[source][branch_name] = branch
        self.mark_modified()
        return self

    def remove_conditional_edge(
        self, source: str, branch_name: str
    ) -> "StateGraphSerializable":
        """Remove a conditional edge.

        Args:
            source: Source node name
            branch_name: Name of the branch to remove

        Returns:
            Self for method chaining
        """
        if source not in self.branches or branch_name not in self.branches[source]:
            raise ValueError(f"Branch '{branch_name}' from '{source}' does not exist")
        del self.branches[source][branch_name]
        if not self.branches[source]:
            del self.branches[source]
        self.mark_modified()
        return self

    def get_node_connections(self, node: str) -> dict[str, list[str]]:
        """Get all connections for a node (incoming and outgoing).

        Args:
            node: Node name to get connections for

        Returns:
            Dictionary with connection information
        """
        result = {
            "incoming_edges": [],
            "outgoing_edges": [],
            "incoming_waiting_edges": [],
            "outgoing_waiting_edges": [],
            "incoming_branches": [],
            "outgoing_branches": [],
        }
        for src, dst in self.edges:
            if src == node:
                result["outgoing_edges"].append(dst)
            elif dst == node:
                result["incoming_edges"].append(src)
        for srcs, dst in self.waiting_edges:
            if node in srcs:
                result["outgoing_waiting_edges"].append(dst)
            elif dst == node:
                result["incoming_waiting_edges"].extend(list(srcs))
        for src, branch_dict in self.branches.items():
            if src == node:
                for _branch_name, branch in branch_dict.items():
                    if branch.ends:
                        for target in branch.ends.values():
                            if target not in result["outgoing_branches"]:
                                result["outgoing_branches"].append(target)
                    if branch.then and branch.then not in result["outgoing_branches"]:
                        result["outgoing_branches"].append(branch.then)
            else:
                for _branch_name, branch in branch_dict.items():
                    targets = list(branch.ends.values()) if branch.ends else []
                    if branch.then:
                        targets.append(branch.then)
                    if node in targets and src not in result["incoming_branches"]:
                        result["incoming_branches"].append(src)
        return result

    def is_node_reachable(self, node: str) -> bool:
        """Check if a node is reachable from the entry point.

        Args:
            node: Node to check

        Returns:
            True if the node is reachable, False otherwise
        """
        if node not in self.nodes:
            return False
        if not self.entry_point:
            return self._is_reachable("__start__", node)
        return self._is_reachable(self.entry_point, node)

    def _is_reachable(self, start: str, target: str) -> bool:
        """Internal method to check if target is reachable from start."""
        visited = set()
        queue = [start]
        while queue:
            current = queue.pop(0)
            if current == target:
                return True
            if current in visited:
                continue
            visited.add(current)
            for src, dst in self.edges:
                if src == current and dst not in visited:
                    queue.append(dst)
            for srcs, dst in self.waiting_edges:
                if current in srcs and dst not in visited:
                    queue.append(dst)
            if current in self.branches:
                for _branch_name, branch in self.branches[current].items():
                    if branch.ends:
                        for dst in branch.ends.values():
                            if dst not in visited:
                                queue.append(dst)
                    if branch.then and branch.then not in visited:
                        queue.append(branch.then)
        return False

    def validate(self) -> bool:
        """Validate the graph structure.

        Checks:
        - All nodes referenced in edges exist
        - Entry and finish points exist
        - All nodes are reachable from entry point

        Returns:
            True if valid, raises ValueError otherwise
        """
        for src, dst in self.edges:
            if src != "__start__" and src not in self.nodes:
                raise ValueError(f"Edge references non-existent source node '{src}'")
            if dst != "__end__" and dst not in self.nodes:
                raise ValueError(f"Edge references non-existent target node '{dst}'")
        for srcs, dst in self.waiting_edges:
            for src in srcs:
                if src != "__start__" and src not in self.nodes:
                    raise ValueError(
                        f"Waiting edge references non-existent source node '{src}'"
                    )
            if dst != "__end__" and dst not in self.nodes:
                raise ValueError(
                    f"Waiting edge references non-existent target node '{dst}'"
                )
        for src, branch_dict in self.branches.items():
            if src not in self.nodes:
                raise ValueError(f"Branch from non-existent node '{src}'")
            for _branch_name, branch in branch_dict.items():
                if branch.ends:
                    for end in branch.ends.values():
                        if end != "__end__" and end not in self.nodes:
                            raise ValueError(
                                f"Branch references non-existent target node '{end}'"
                            )
                if (
                    branch.then
                    and branch.then != "__end__"
                    and (branch.then not in self.nodes)
                ):
                    raise ValueError(
                        f"Branch 'then' references non-existent node '{branch.then}'"
                    )
        if self.entry_point and self.entry_point not in self.nodes:
            raise ValueError(f"Entry point '{self.entry_point}' does not exist")
        if self.finish_point and self.finish_point not in self.nodes:
            raise ValueError(f"Finish point '{self.finish_point}' does not exist")
        if self.entry_point:
            for node in self.nodes:
                if not self._is_reachable(self.entry_point, node):
                    logger.warning(f"Node '{node}' is not reachable from entry point")
        return True

    def is_modified(self) -> bool:
        """Check if the graph has been modified."""
        return self._modified

    def reset_modified(self) -> None:
        """Reset the modified flag."""
        self._modified = False

    def to_dict(self) -> dict[str, Any]:
        """Convert to a dictionary for serialization."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "StateGraphSerializable":
        """Create from a dictionary."""
        return cls.model_validate(data)

    def to_json(self, **kwargs) -> str:
        """Convert to JSON string."""
        return self.model_dump_json(**kwargs)

    @classmethod
    def from_json(cls, json_str: str) -> "StateGraphSerializable":
        """Create from JSON string."""
        return cls.model_validate_json(json_str)

    @classmethod
    def from_state_graph(cls, graph: Any) -> "StateGraphSerializable":
        """Create a serializable representation from a StateGraph."""
        serializable = cls(
            edges=set(graph.edges),
            waiting_edges=set(graph.waiting_edges),
            compiled=graph.compiled,
        )
        if hasattr(graph, "schema"):
            serializable.schema = TypeReference.from_type(graph.schema)
        if hasattr(graph, "input"):
            serializable.input_schema = TypeReference.from_type(graph.input)
        if hasattr(graph, "output"):
            serializable.output_schema = TypeReference.from_type(graph.output)
        if hasattr(graph, "config_schema"):
            serializable.config_schema = TypeReference.from_type(graph.config_schema)
        for name, node_spec in graph.nodes.items():
            node = NodeSpec.from_node_spec(name, node_spec)
            if node:
                serializable.nodes[name] = node
        for source, branch_dict in graph.branches.items():
            for branch_name, branch in branch_dict.items():
                branch_spec = BranchSpec.from_branch(branch_name, branch)
                if branch_spec:
                    if source not in serializable.branches:
                        serializable.branches[source] = {}
                    serializable.branches[source][branch_name] = branch_spec
        if hasattr(graph, "entry_point"):
            serializable.entry_point = graph.entry_point
        if hasattr(graph, "finish_point"):
            serializable.finish_point = graph.finish_point
        serializable._modified = False
        return serializable
