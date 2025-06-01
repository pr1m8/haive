#!/usr/bin/env python3
"""Test script to demonstrate improved subgraph visualization.

This script creates a main graph with a subgraph and shows how the new
visualization properly handles START/END nodes within subgraphs.
"""

import os
import sys

# Add the packages to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src"))

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph


def create_test_subgraph():
    """Create a test subgraph with proper START/END connections."""
    subgraph = BaseGraph(name="structured_output")
    
    # Add nodes to subgraph
    subgraph.add_node("agent_node", lambda _: {"result": "agent_processed"}, node_type=NodeType.ENGINE)
    subgraph.add_node("validation", lambda _: {"validated": True}, node_type=NodeType.VALIDATION)
    subgraph.add_node("parse_output", lambda _: {"parsed": True}, node_type=NodeType.CALLABLE)
    
    # Set up subgraph flow
    subgraph.set_entry_point("agent_node")
    subgraph.add_edge("agent_node", "validation")
    subgraph.add_edge("validation", "parse_output")
    subgraph.set_finish_point("parse_output")
    
    return subgraph


def create_main_graph():
    """Create a main graph that includes a subgraph."""
    main_graph = BaseGraph(name="main_graph")
    
    # Add main graph nodes
    main_graph.add_node("agent_node", lambda _: {"messages": []}, node_type=NodeType.ENGINE)
    main_graph.add_node("validation", lambda _: {"valid": True}, node_type=NodeType.VALIDATION)
    main_graph.add_node("tool_node", lambda _: {"tools_used": True}, node_type=NodeType.TOOL)
    
    # Create and add subgraph
    subgraph = create_test_subgraph()
    main_graph.add_subgraph("structured_output", subgraph)
    
    # Set up main graph flow
    main_graph.set_entry_point("agent_node")
    main_graph.add_edge("tool_node", "agent_node")
    
    # Add conditional edges
    main_graph.add_conditional_edges(
        "agent_node",
        lambda _: True,  # Simple condition
        {True: "validation", False: "END"}
    )
    
        main_graph.add_conditional_edges(
        "validation",
        lambda _: "has_errors",  # Return routing key
        {
            "has_errors": "agent_node",
            "tool_node": "tool_node",
            "structured_output": "structured_output"
        },
        default="END"
    )
    
    return main_graph


def test_visualization_modes():
    """Test different visualization modes."""
    print("Creating test graph with subgraph...")
    graph = create_main_graph()
    
    print("\n" + "="*60)
    print("CLUSTER MODE (Default - Subgraphs as clusters)")
    print("="*60)
    
    cluster_mermaid = graph.to_mermaid(subgraph_mode="cluster")
    print(cluster_mermaid)
    
    print("\n" + "="*60)
    print("INLINE MODE (Subgraph nodes inline with main graph)")
    print("="*60)
    
    inline_mermaid = graph.to_mermaid(subgraph_mode="inline")
    print(inline_mermaid)
    
    print("\n" + "="*60)
    print("NO SUBGRAPHS (Main graph only)")
    print("="*60)
    
    no_subgraph_mermaid = graph.to_mermaid(include_subgraphs=False)
    print(no_subgraph_mermaid)


if __name__ == "__main__":
    test_visualization_modes() 