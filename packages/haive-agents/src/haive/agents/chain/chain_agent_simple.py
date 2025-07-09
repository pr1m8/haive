"""ChainAgent - The simplest way to build agent chains

Just list your nodes and define the flow. That's it.
"""

import logging
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.engine.base import Engine
from haive.core.graph.node.base_config import NodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)

# Any type that can be a node
NodeLike = Union[Agent, Engine, Callable, NodeConfig]

# Edge can be string "0->1" or tuple (0, 1) or conditional (0, {...}, func)
EdgeLike = Union[
    str,
    Tuple[Union[int, str], Union[int, str]],
    Tuple[Union[int, str], Dict[Any, Union[int, str]], Callable],
]


class ChainAgent(Agent):
    """The simplest way to build chains - just list nodes and edges."""

    name: str = "Chain Agent"
    nodes: List[NodeLike] = Field(default_factory=list)
    edges: List[EdgeLike] = Field(default_factory=list)

    def __init__(self, *nodes: NodeLike, **kwargs):
        """Initialize with nodes directly.

        Examples:
            ChainAgent(node1, node2, node3)  # Auto-sequential
            ChainAgent(node1, node2, edges=["0->1"])
        """
        edges = kwargs.pop("edges", None)
        name = kwargs.pop("name", "Chain Agent")

        super().__init__(name=name, nodes=list(nodes), edges=edges or [], **kwargs)

        # Auto-sequence if no edges provided
        if not self.edges and len(self.nodes) > 1:
            for i in range(len(self.nodes) - 1):
                self.edges.append(f"{i}->{i+1}")

    def build_graph(self) -> BaseGraph:
        """Build the graph from nodes and edges."""
        graph = BaseGraph(name=self.name.replace(" ", ""))

        # Add nodes
        node_names = {}
        for i, node in enumerate(self.nodes):
            node_name = f"node_{i}"
            node_names[i] = node_name

            # Convert to proper node
            if isinstance(node, Agent):
                graph.add_node(node_name, node)
            elif isinstance(node, AugLLMConfig):
                # Wrap engine in SimpleAgent
                graph.add_node(node_name, SimpleAgent(engine=node, name=node_name))
            elif isinstance(node, Engine):
                # Other engines - create wrapper
                from haive.core.graph.node.engine_node import EngineNodeConfig

                graph.add_node(node_name, EngineNodeConfig(name=node_name, engine=node))
            elif callable(node):
                graph.add_node(node_name, node)
            else:
                graph.add_node(node_name, node)

        # Process edges
        for edge in self.edges:
            self._add_edge_to_graph(graph, edge, node_names)

        # Connect start and end
        if self.nodes:
            graph.add_edge(START, node_names[0])

            # Find terminal nodes
            has_outgoing = set()
            for edge in self.edges:
                if isinstance(edge, str) and "->" in edge:
                    from_idx = int(edge.split("->")[0].strip())
                    has_outgoing.add(from_idx)
                elif isinstance(edge, tuple) and len(edge) >= 2:
                    from_idx = edge[0] if isinstance(edge[0], int) else int(edge[0])
                    has_outgoing.add(from_idx)

            # Connect terminals to END
            for i in range(len(self.nodes)):
                if i not in has_outgoing:
                    graph.add_edge(node_names[i], END)

        return graph

    def _add_edge_to_graph(
        self, graph: BaseGraph, edge: EdgeLike, node_names: Dict[int, str]
    ):
        """Add an edge to the graph."""
        if isinstance(edge, str):
            # Parse "0->1" format
            if "->" in edge:
                from_str, to_str = edge.split("->", 1)
                from_idx = int(from_str.strip())
                to_idx = int(to_str.strip())
                graph.add_edge(node_names[from_idx], node_names[to_idx])

        elif isinstance(edge, tuple):
            if len(edge) == 2:
                # Simple edge (0, 1)
                from_idx = edge[0] if isinstance(edge[0], int) else int(edge[0])
                to_idx = edge[1] if isinstance(edge[1], int) else int(edge[1])
                graph.add_edge(node_names[from_idx], node_names[to_idx])

            elif len(edge) == 3:
                # Conditional edge (0, {"a": 1, "b": 2}, condition)
                from_idx = edge[0] if isinstance(edge[0], int) else int(edge[0])
                branches = {}
                for key, val in edge[1].items():
                    to_idx = val if isinstance(val, int) else int(val)
                    branches[key] = node_names[to_idx]

                graph.add_conditional_edges(
                    node_names[from_idx], edge[2], branches  # condition function
                )

    # Convenience methods
    def add(self, node: NodeLike) -> "ChainAgent":
        """Add a node and auto-link from previous."""
        if self.nodes:
            prev_idx = len(self.nodes) - 1
            self.nodes.append(node)
            curr_idx = len(self.nodes) - 1
            self.edges.append(f"{prev_idx}->{curr_idx}")
        else:
            self.nodes.append(node)
        return self

    def branch(self, condition: Callable, **branches: NodeLike) -> "ChainAgent":
        """Add conditional branching."""
        if not self.nodes:
            raise ValueError("No nodes to branch from")

        from_idx = len(self.nodes) - 1
        branch_map = {}

        for key, node in branches.items():
            self.nodes.append(node)
            to_idx = len(self.nodes) - 1
            branch_map[key] = to_idx

        self.edges.append((from_idx, branch_map, condition))
        return self

    def merge_to(self, target_idx: int) -> "ChainAgent":
        """Merge the last node to a target node."""
        if self.nodes:
            from_idx = len(self.nodes) - 1
            self.edges.append(f"{from_idx}->{target_idx}")
        return self


# Super simple factory functions
def flow(*nodes: NodeLike, **kwargs) -> ChainAgent:
    """Create a flow chain - the simplest way.

    Examples:
        # Sequential
        chain = flow(node1, node2, node3)

        # With edges
        chain = flow(node1, node2, node3, edges=["0->2"])  # Skip node2

        # With name
        chain = flow(node1, node2, name="My Flow")
    """
    return ChainAgent(*nodes, **kwargs)


def flow_with_edges(nodes: List[NodeLike], *edges: EdgeLike) -> ChainAgent:
    """Create a flow with custom edges.

    Example:
        chain = flow_with_edges(
            [classifier, simple, complex, output],
            (0, {"simple": 1, "complex": 2}, lambda s: s.type),
            "1->3",
            "2->3"
        )
    """
    return ChainAgent(*nodes, edges=list(edges))


# Builder pattern for chaining
class FlowBuilder:
    """Builder for method chaining."""

    def __init__(self, initial: Optional[NodeLike] = None):
        self.chain = ChainAgent() if initial is None else ChainAgent(initial)

    def add(self, node: NodeLike) -> "FlowBuilder":
        """Add a node."""
        self.chain.add(node)
        return self

    def branch(self, condition: Callable, **branches: NodeLike) -> "FlowBuilder":
        """Add branching."""
        self.chain.branch(condition, **branches)
        return self

    def merge_to(self, target_idx: int) -> "FlowBuilder":
        """Merge to a previous node."""
        self.chain.merge_to(target_idx)
        return self

    def build(self) -> ChainAgent:
        """Get the chain."""
        return self.chain
