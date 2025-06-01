#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)
from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph

# Create the test graph exactly as in the original issue
main_graph = BaseGraph(name="main_graph")
main_graph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
main_graph.add_node("tool_node", lambda state: state, node_type=NodeType.TOOL)

subgraph = BaseGraph(name="structured_output")
subgraph.add_node("agent_node", lambda state: state, node_type=NodeType.ENGINE)
subgraph.add_node("validation", lambda state: state, node_type=NodeType.VALIDATION)
subgraph.add_node("parse_output", lambda state: state, node_type=NodeType.CALLABLE)

subgraph.add_edge(START, "agent_node")
subgraph.add_edge("parse_output", END)
subgraph.add_edge("agent_node", "validation")

subgraph.add_conditional_edges(
    "validation",
    lambda state: "has_errors" if state.get("has_errors") else "parse_output",
    {"has_errors": "agent_node", "parse_output": "parse_output"},
    default=END,
)

main_graph.add_subgraph("structured_output", subgraph)
main_graph.add_edge(START, "agent_node")
main_graph.add_edge("tool_node", "agent_node")

main_graph.add_conditional_edges(
    "agent_node",
    lambda state: bool(state.get("has_tool_calls")),
    {True: "structured_output", False: END},
)

for i, (branch_id, branch) in enumerate(main_graph.branches.items()):

    # Check if any destination nodes don't exist in main graph
    for _condition, target in branch.destinations.items():
        if target not in main_graph.nodes and target not in (START, END):
            pass
        else:
            pass")

for i, (branch_id, branch) in enumerate(subgraph.branches.items()):

# Now let's check if there's any cross-contamination

# Check if main graph somehow has subgraph nodes
for name in main_graph.nodes:
    if name in subgraph.nodes and name not in [
        "agent_node"
    ]:  # agent_node is legitimately in both
        passh!")

# Check if main graph branches reference subgraph nodes
for branch_id, branch in main_graph.branches.items():
    for _condition, target in branch.destinations.items():
        if target in subgraph.nodes and target not in main_graph.nodes:
            pass'!")
