"""Agent core module.

This module provides agent functionality for the Haive framework.

Classes:
    ReactAgent: ReactAgent implementation.

Functions:
    build_graph: Build Graph functionality.
"""

from haive.core.graph.state_graph.base_graph2 import BaseGraph

# ============================================================================
# REACT AGENT
# ============================================================================
from langgraph.graph import END

from haive.agents.simple import SimpleAgent

# ========================================================================
# REACT AGENT
# ============================================================================


class ReactAgent(SimpleAgent):
    """ReAct agent with looping behavior."""

    def build_graph(self) -> BaseGraph:
        """Build ReAct graph with proper looping."""
        # Build base graph first
        graph = super().build_graph()

        # Modify connections for ReAct looping
        main_engine = self.main_engine
        if not main_engine:
            return graph

        # Change end destinations to loop back to agent_node
        if self._needs_tool_node() and "tool_node" in graph.nodes:
            # Remove existing edge and add loop back
            graph.remove_edge("tool_node", END)
            graph.add_edge("tool_node", "agent_node")

        if self._needs_parser_node() and "parse_output" in graph.nodes:
            # Remove existing edge and add loop back
            graph.remove_edge("parse_output", END)
            graph.add_edge("parse_output", "agent_node")

        return graph
