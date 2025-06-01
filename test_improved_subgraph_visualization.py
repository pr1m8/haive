#!/usr/bin/env python3
"""
Test script to demonstrate improved subgraph visualization.

This script shows how the new visualization properly handles:
1. Subgraphs as separate clusters with their own nodes
2. No duplication of nodes between main graph and subgraphs
3. Proper connection points between main graph and subgraphs
4. Optional hiding of default branches
"""

import os
import sys

# Add the package to the path
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)

from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph


def create_test_graph_with_subgraph():
    """Create a test graph with a subgraph to demonstrate visualization."""

    # Create main graph
    main_graph = BaseGraph(name="main_graph")

    # Add main graph nodes
    main_graph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
    main_graph.add_node("tool_node", lambda state: state, node_type=NodeType.TOOL)

    # Create subgraph
    subgraph = BaseGraph(name="structured_output")
    subgraph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
    subgraph.add_node("validation", lambda state: state, node_type=NodeType.VALIDATION)
    subgraph.add_node("parse_output", lambda state: state, node_type=NodeType.CALLABLE)

    # Add subgraph edges
    subgraph.add_edge(START, "agent_node")
    subgraph.add_edge("parse_output", END)
    subgraph.add_edge("agent_node", "validation")

    # Add subgraph branches
    subgraph.add_conditional_edges(
        "validation",
        lambda state: "has_errors" if state.get("has_errors") else "parse_output",
        {
            "has_errors": "agent_node",
            "parse_output": "parse_output",
        },
        default=END,
    )

    # Add subgraph to main graph
    main_graph.add_subgraph("structured_output", subgraph)

    # Add main graph edges
    main_graph.add_edge(START, "agent_node")
    main_graph.add_edge("tool_node", "agent_node")

    # Add main graph branches
    main_graph.add_conditional_edges(
        "agent_node",
        lambda state: True if state.get("has_tool_calls") else False,
        {True: "structured_output", False: END},  # This will connect to the subgraph
    )

    return main_graph


def test_visualization_modes():
    """Test different visualization modes."""

    print("Creating test graph with subgraph...")
    graph = create_test_graph_with_subgraph()

    print("\n" + "=" * 60)
    print("CLUSTER MODE (with default branches hidden)")
    print("=" * 60)

    # Generate cluster mode visualization (default branches hidden)
    mermaid_code = graph.to_mermaid(
        include_subgraphs=True, subgraph_mode="cluster", show_default_branches=False
    )

    print(mermaid_code)

    print("\n" + "=" * 60)
    print("CLUSTER MODE (with default branches shown)")
    print("=" * 60)

    # Generate cluster mode visualization (default branches shown)
    mermaid_code = graph.to_mermaid(
        include_subgraphs=True, subgraph_mode="cluster", show_default_branches=True
    )

    print(mermaid_code)

    print("\n" + "=" * 60)
    print("INLINE MODE")
    print("=" * 60)

    # Generate inline mode visualization
    mermaid_code = graph.to_mermaid(
        include_subgraphs=True, subgraph_mode="inline", show_default_branches=False
    )

    print(mermaid_code)

    print("\n" + "=" * 60)
    print("NO SUBGRAPHS MODE")
    print("=" * 60)

    # Generate without subgraphs
    mermaid_code = graph.to_mermaid(
        include_subgraphs=False, show_default_branches=False
    )

    print(mermaid_code)


if __name__ == "__main__":
    test_visualization_modes()
