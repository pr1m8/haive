#!/usr/bin/env python3
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "packages", "haive-core", "src")
)
from langgraph.graph import END, START

from haive.core.graph.common.types import NodeType
from haive.core.graph.state_graph.base_graph2 import BaseGraph

# Create the same test graph
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

print("=== MAIN GRAPH STRUCTURE ===")
print("Main graph nodes:", list(main_graph.nodes.keys()))
print("Main graph edges:", main_graph.edges)
print("Main graph branches:", len(main_graph.branches))
print("Main graph subgraphs:", list(main_graph.subgraphs.keys()))

print("\n=== SUBGRAPH STRUCTURE ===")
print("Subgraph nodes:", list(subgraph.nodes.keys()))
print("Subgraph edges:", subgraph.edges)
print("Subgraph branches:", len(subgraph.branches))

# Now let's manually trace through the visualization logic
print("\n=== VISUALIZATION DEBUG ===")

# Check what nodes the visualization will process
print("Nodes that will be processed in main graph section:")
for name, node in main_graph.nodes.items():
    if node is None:
        print(f"  SKIP: {name} (None node)")
        continue
    if name in (START, END):
        print(f"  SKIP: {name} (special node)")
        continue
    if hasattr(main_graph, "subgraphs") and name in main_graph.subgraphs:
        print(f"  SUBGRAPH CONTAINER: {name} (will be added as subgraph type)")
        continue
    print(f"  MAIN NODE: {name}")

print("\nSubgraph nodes that will be processed:")
if hasattr(main_graph, "subgraphs"):
    for sg_name, sg in main_graph.subgraphs.items():
        print(f"  Subgraph: {sg_name}")
        for sub_node_name, sub_node in sg.nodes.items():
            if sub_node is None or sub_node_name in (START, END):
                print(f"    SKIP: {sub_node_name}")
                continue
            print(f"    SUBGRAPH NODE: {sub_node_name} (will get prefix sg_{sg_name})")
