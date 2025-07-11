# src/haive/agents/react/graph_utils.py

import logging
from collections.abc import Callable

from haive.core.graph.dynamic_graph_builder import DynamicGraph
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


class ReactGraphBuilder(DynamicGraph):
    """Enhanced graph builder for React agents with support for human interaction."""

    def __init__(self, components=None, custom_fields=None, state_schema=None):
        """Initialize the React graph builder."""
        super().__init__(components, custom_fields, state_schema)
        self.has_human_node = False

    def add_human_node(self, name: str, handler: Callable, goto: str | None = None):
        """Add a human interaction node to the graph.

        Args:
            name: Name for the human node
            handler: Function to handle the human interaction
            goto: Where to route after human input (or None for conditional)

        Returns:
            Self for chaining
        """
        self.add_node(name=name, config=handler, command_goto=goto)
        self.has_human_node = True
        return self

    def add_tool_node(
        self,
        name: str,
        tools: list[BaseTool],
        support_human_input: bool = True,
        parallel_tools: bool = True,
        human_node_name: str | None = "human_input",
        command_goto: str | None = None,
    ):
        """Add an enhanced tool node with optional human interaction support.

        Args:
            name: Name of the node
            tools: List of tools
            support_human_input: Whether to support human interaction
            parallel_tools: Whether to run tools in parallel
            human_node_name: Name for the human input node
            command_goto: Where to route after tool execution

        Returns:
            Self for chaining
        """
        from haive.agents.react_class.react_v2.tool_handling import (
            GeneralizedToolNode,
            human_input_node,
        )

        # Create the generalized tool node
        tool_node = GeneralizedToolNode(tools, parallel=parallel_tools)

        # Add the tool node
        self.add_node(name=name, config=tool_node, command_goto=command_goto)

        # Add human input node if supported
        if support_human_input:
            self.add_human_node(
                name=human_node_name,
                handler=human_input_node,
                goto=command_goto or name,  # Route back to calling node by default
            )

            # Add conditional routing from tools to human node
            self.add_conditional_edges(
                from_node=name,
                condition_or_branch=lambda state: (
                    human_node_name
                    if state.get("requires_human_input")
                    else command_goto or name
                ),
                routes={
                    human_node_name: human_node_name,
                    command_goto or name: command_goto or name,
                },
            )

        return self
