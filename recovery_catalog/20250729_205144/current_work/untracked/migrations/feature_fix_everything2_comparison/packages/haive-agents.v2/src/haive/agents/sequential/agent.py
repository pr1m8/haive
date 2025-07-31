"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    SequentialMultiAgent: SequentialMultiAgent implementation.

Functions:
    placeholder_node: Placeholder Node functionality.
    build_graph: Build Graph functionality.
"""

# haive/agents/multi/sequential.py

"""Sequential multi-agent implementation for the Haive framework."""

import logging
from typing import Any

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from langgraph.types import Command

from haive.agents.multi.base import MultiAgent

logger = logging.getLogger(__name__)


def placeholder_node(state: dict[str, Any]):
    """Placeholder node that does nothing."""
    return Command(update={})


class SequentialMultiAgent(MultiAgent):
    """Multi-agent system that executes agents sequentially.

    Each agent runs in order, with the output of one feeding into the next.
    The execution follows a chain pattern: Agent1 -> Agent2 -> ... -> AgentN
    """

    def __init__(self, **kwargs) -> None:
        """Initialize with sequential coordination mode."""
        kwargs["coordination_mode"] = "sequential"
        super().__init__(**kwargs)

    def build_graph(self) -> BaseGraph:
        """Build a sequential execution graph."""
        graph = BaseGraph(name=self.name)

        # Add initial setup node
        graph.add_node("setup", self._setup_node)
        graph.add_edge(START, "setup")

        # Add nodes for each agent
        previous_node = "setup"
        for _i, (agent_name, agent) in enumerate(self.agents.items()):
            node_name = f"{agent_name}_node"

            # Create agent node
            agent_node = self._create_agent_node(agent_name, agent)
            graph.add_node(node_name, agent_node)

            # Add post-processing node
            post_node = f"{agent_name}_post"
            graph.add_node(post_node, self.update_agent_state(agent_name))

            # Connect nodes
            graph.add_edge(previous_node, node_name)
            graph.add_edge(node_name, post_node)

            # Update previous node
            previous_node = post_node

        # Connect last node to end
        graph.add_edge(previous_node, END)

        return graph

    def _setup_node(self, state: Any) -> Command:
        """Initialize the multi-agent state."""
        return Command(
            update={
                "agents": self._agent_order,
                "current_agent": self._agent_order[0] if self._agent_order else None,
                "completed_agents": [],
                "execution_mode": "sequential",
            }
        )
