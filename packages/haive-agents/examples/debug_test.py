#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)
from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START

# Create main graph
main_graph = BaseGraph(name="main_graph")
main_graph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
main_graph.add_node("tool_node", lambda state: state, node_type=NodeType.TOOL)

print("Main graph nodes after adding main nodes:", list(main_graph.nodes.keys()))
print("Main graph branches after adding main nodes:", len(main_graph.branches))

# Create subgraph
subgraph = BaseGraph(name="structured_output")
subgraph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
subgraph.add_node("validation", lambda state: state, node_type=NodeType.VALIDATION)
subgraph.add_node("parse_output", lambda state: state, node_type=NodeType.CALLABLE)

print("Subgraph nodes:", list(subgraph.nodes.keys()))

# Add subgraph edges
subgraph.add_edge(START, "agent_node")
subgraph.add_edge("parse_output", END)
subgraph.add_edge("agent_node", "validation")

print("Subgraph edges:", subgraph.edges)

# Add subgraph branches
subgraph.add_conditional_edges(
    "validation",
    lambda state: "has_errors" if state.get("has_errors") else "parse_output",
    {"has_errors": "agent_node", "parse_output": "parse_output"},
    default=END,
)

print("Subgraph branches:", len(subgraph.branches))

# Add subgraph to main graph
main_graph.add_subgraph("structured_output", subgraph)

print("Main graph nodes after adding subgraph:", list(main_graph.nodes.keys()))
print("Main graph branches after adding subgraph:", len(main_graph.branches))

# Add main graph edges
main_graph.add_edge(START, "agent_node")
main_graph.add_edge("tool_node", "agent_node")

print("Main graph edges after adding main edges:", main_graph.edges)

# Add main graph branches
main_graph.add_conditional_edges(
    "agent_node",
    lambda state: bool(state.get("has_tool_calls")),
    {True: "structured_output", False: END},
)

print("Main graph nodes after adding main branches:", list(main_graph.nodes.keys()))
print("Main graph branches after adding main branches:", len(main_graph.branches))

# Check what's in the branches
for i, (_branch_id, branch) in enumerate(main_graph.branches.items()):
    print(
        f"Branch {i}: source={branch.source_node}, destinations={branch.destinations}"
    )
