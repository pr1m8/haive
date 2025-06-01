#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)
from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph


def create_test_graph():
    """Create the exact same graph structure as the user's issue."""
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

    # Add main graph branches
    main_graph.add_conditional_edges(
        "agent_node",
        lambda state: bool(state.get("has_tool_calls")),
        {True: "structured_output", False: END},
    )

    return main_graph, subgraph


def analyze_graph_contamination(main_graph, subgraph):
    """Analyze if there's any contamination between main graph and subgraph."""

    # Check if main graph has subgraph nodes
    contaminated_nodes = []
    for name in main_graph.nodes:
        if name in subgraph.nodes and name not in ["agent_node", "structured_output"]:
            contaminated_nodes.append(name)

    if not contaminated_nodes:
        pass")

    # Check if main graph has subgraph branches
    contaminated_branches = []
    for branch_id, branch in main_graph.branches.items():
        # Check if branch source is a subgraph-only node
        if branch.source_node in subgraph.nodes and branch.source_node not in [
            "agent_node",
            "structured_output",
        ]:
            contaminated_branches.append((branch_id, branch))

        # Check if branch destinations include subgraph-only nodes
        for _condition, target in branch.destinations.items():
            if target in subgraph.nodes and target not in main_graph.nodes:
                pass

    if not contaminated_branches:
        pass")

    return contaminated_nodes, contaminated_branches


def check_branch_details(main_graph, subgraph):
    """Check detailed branch information."""

    for i, (branch_id, branch) in enumerate(main_graph.branches.items()):

        # Check if source exists in main graph
        if branch.source_node not in main_graph.nodes and branch.source_node not in (
            START,
            END,
        ):
            passh!")

        # Check destinations
        for _condition, target in branch.destinations.items():
            if target not in main_graph.nodes and target not in (START, END):
                passh!")

    for i, (branch_id, branch) in enumerate(subgraph.branches.items()):


def simulate_visualization_logic(main_graph, subgraph):
    """Simulate the visualization logic to see what nodes would be processed."""

    include_subgraphs = True

    for name, node in main_graph.nodes.items():
        if node is None:
            continue

        if name in (START, END):
            continue

        if (
            include_subgraphs
            and hasattr(main_graph, "subgraphs")
            and name in main_graph.subgraphs
        ):
            continue


    for branch_id, branch in main_graph.branches.items():
        source = branch.source_node

        # Check if source exists in main graph
        if source not in main_graph.nodes and source not in (START, END):
            continue


        for condition, target in branch.destinations.items():
            if target not in main_graph.nodes and target not in (START, END):
                pass
            else:
                pass


if __name__ == "__main__":
    main_graph, subgraph = create_test_graph()


    contaminated_nodes, contaminated_branches = analyze_graph_contamination(
        main_graph, subgraph
    )
    check_branch_details(main_graph, subgraph)
    simulate_visualization_logic(main_graph, subgraph)

    # Generate visualization to see current state
    mermaid = main_graph.to_mermaid(
        include_subgraphs=True, subgraph_mode="cluster", show_default_branches=False
    )

    # Check for problematic patterns
    if "validation[" in mermaid and "Main Graph Nodes" in mermaid:
        validation_in_main = mermaid.split("Main Graph Nodes")[1].split(
            "%% Main Graph Direct Edges"
        )[0]
        if "validation[" in validation_in_main:
            passon")
        else:
            pass")

    if "validation -.->|" in mermaid and "Main Graph Branch Connections" in mermaid:
        branches_section = mermaid.split("Main Graph Branch Connections")[1].split(
            "%% Main Graph to Subgraph"
        )[0]
        if "validation -.->|" in branches_section:
            passon")
        else:
            pass")
