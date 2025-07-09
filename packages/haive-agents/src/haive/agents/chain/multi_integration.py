"""Integration of ChainAgent with Multi-Agent Base

Makes ChainAgent work seamlessly with the multi-agent framework.
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from pydantic import Field

from haive.agents.base.agent import Agent
from haive.agents.chain.chain_agent_simple import ChainAgent, NodeLike
from haive.agents.multi.base import ExecutionMode, MultiAgent

logger = logging.getLogger(__name__)


class ChainMultiAgent(MultiAgent):
    """ChainAgent that works with the multi-agent framework.

    Combines the simplicity of ChainAgent with the power of MultiAgent.
    """

    execution_mode: ExecutionMode = Field(default=ExecutionMode.SEQUENCE)
    chain_config: Optional[Dict[str, Any]] = Field(
        default=None, description="Chain configuration"
    )

    @classmethod
    def from_chain(
        cls, chain: ChainAgent, name: Optional[str] = None, **kwargs
    ) -> "ChainMultiAgent":
        """Create a MultiAgent from a ChainAgent."""

        # Extract agents from the chain's nodes
        agents = []
        for i, node in enumerate(chain.nodes):
            if isinstance(node, Agent):
                agents.append(node)
            else:
                # Wrap non-agents in a simple wrapper
                agent_name = f"chain_node_{i}"
                wrapper = ChainNodeWrapper(node=node, name=agent_name)
                agents.append(wrapper)

        return cls(
            name=name or chain.name,
            agents=agents,
            chain_config={"edges": chain.edges, "original_nodes": chain.nodes},
            **kwargs,
        )

    @classmethod
    def from_nodes(
        cls,
        nodes: List[NodeLike],
        edges: Optional[List] = None,
        name: str = "Chain Multi Agent",
        **kwargs,
    ) -> "ChainMultiAgent":
        """Create directly from nodes and edges."""

        # Create a ChainAgent first
        chain = ChainAgent(*nodes, edges=edges or [], name=name)

        # Convert to MultiAgent
        return cls.from_chain(chain, name=name, **kwargs)


class ChainNodeWrapper(Agent):
    """Wrapper to make non-agent nodes work in multi-agent framework."""

    name: str = "Chain Node Wrapper"
    node: NodeLike = Field(description="The wrapped node")

    def build_graph(self) -> BaseGraph:
        """Build a simple graph with just this node."""
        from langgraph.graph import END, START

        graph = BaseGraph(name=self.name.replace(" ", ""))

        # Add the node
        if callable(self.node):
            graph.add_node("execute", self.node)
        else:
            # Handle other node types
            graph.add_node("execute", lambda s: s)  # Pass-through

        graph.add_edge(START, "execute")
        graph.add_edge("execute", END)

        return graph


# Helper functions to convert between ChainAgent and MultiAgent
def chain_to_multi(chain: ChainAgent) -> ChainMultiAgent:
    """Convert a ChainAgent to a MultiAgent."""
    return ChainMultiAgent.from_chain(chain)


def multi_to_chain(multi: MultiAgent) -> ChainAgent:
    """Convert a MultiAgent to a ChainAgent (if possible)."""
    if multi.execution_mode == ExecutionMode.SEQUENCE:
        # Simple sequential conversion
        return ChainAgent(*multi.agents, name=multi.name)
    else:
        raise ValueError(
            f"Cannot convert {multi.execution_mode} MultiAgent to ChainAgent"
        )


# Extended execution modes
class ExtendedExecutionMode(ExecutionMode):
    """Extended execution modes including chain-based."""

    CHAIN = "chain"  # Use ChainAgent-style execution


# Factory functions for easy creation
def chain_multi(*nodes: NodeLike, name: str = "Chain Multi") -> ChainMultiAgent:
    """Create a ChainMultiAgent from nodes."""
    return ChainMultiAgent.from_nodes(list(nodes), name=name)


def sequential_multi(*agents: Agent, name: str = "Sequential Multi") -> ChainMultiAgent:
    """Create a sequential multi-agent system."""
    return ChainMultiAgent(
        name=name, agents=list(agents), execution_mode=ExecutionMode.SEQUENCE
    )


def conditional_multi(
    agents: List[Agent],
    conditions: Dict[str, Callable],
    name: str = "Conditional Multi",
) -> ChainMultiAgent:
    """Create a conditional multi-agent system."""

    # Convert conditions to ChainAgent edges format
    edges = []
    for i, (agent_name, condition) in enumerate(conditions.items()):
        # This is simplified - real implementation would be more complex
        edges.append((i, {"true": i + 1, "false": i + 2}, condition))

    return ChainMultiAgent.from_nodes(agents, edges=edges, name=name)
