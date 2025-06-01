#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)
from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph


def create_contaminated_graph():
    """Create a graph that simulates the user's contamination issue."""
    # Create main graph
    main_graph = BaseGraph(name="main_graph")
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
        {"has_errors": "agent_node", "parse_output": "parse_output"},
        default=END,
    )

    # Add subgraph to main graph
    main_graph.add_subgraph("structured_output", subgraph)

    # Add main graph edges
    main_graph.add_edge(START, "agent_node")
    main_graph.add_edge("tool_node", "agent_node")
    main_graph.add_edge("structured_output", END)

    # Add main graph branches
    main_graph.add_conditional_edges(
        "agent_node",
        lambda state: bool(state.get("has_tool_calls")),
        {True: "structured_output", False: END},
    )

    # SIMULATE CONTAMINATION: Manually add subgraph nodes to main graph
    # This simulates what the user is experiencing

    # Add contaminated validation node to main graph
    main_graph.nodes["validation"] = subgraph.nodes["validation"]
    main_graph.node_types["validation"] = NodeType.VALIDATION

    # Add contaminated branches from subgraph to main graph
    for branch_id, branch in subgraph.branches.items():
        # Create a new branch ID to avoid conflicts
        contaminated_branch_id = f"contaminated_{branch_id}"
        main_graph.branches[contaminated_branch_id] = branch


    return main_graph, subgraph


def test_visualization_with_contamination(main_graph, subgraph):
    """Test the visualization with the contaminated graph."""

    for name in main_graph.nodes:
        pass

    for branch_id, branch in main_graph.branches.items():
        pass

    mermaid = main_graph.to_mermaid(
        include_subgraphs=True, subgraph_mode="cluster", show_default_branches=False
    )

    # Check if contamination is properly filtered out

    # Check main graph nodes section
    if "validation[" in mermaid and "Main Graph Nodes" in mermaid:
        main_nodes_section = mermaid.split("Main Graph Nodes")[1].split(
            "%% Main Graph Direct Edges"
        )[0]
        if "validation[" in main_nodes_section:
            pass")
        else:
            pass")
    else:
        pass")

    # Check main graph branches section
    if "validation -.->|" in mermaid and "Main Graph Branch Connections" in mermaid:
        branches_section = mermaid.split("Main Graph Branch Connections")[1]
        if "%% Main Graph to Subgraph" in branches_section:
            branches_section = branches_section.split("%% Main Graph to Subgraph")[0]

        if "validation -.->|" in branches_section:
            pass")
        else:
            pass
    else:
        pass")

    # Check that legitimate nodes are still present
    if (
        "agent_node[" in mermaid
        and "tool_node[" in mermaid
        and "structured_output[" in mermaid
    ):
        pass")
    else:
        pass")

    # Check that subgraph is still properly rendered
    if "subgraph cluster_structured_output" in mermaid:
        pass")
    else:
        pass")

    return mermaid


if __name__ == "__main__":
    main_graph, subgraph = create_contaminated_graph()
    mermaid = test_visualization_with_contamination(main_graph, subgraph)

