#!/usr/bin/env python3
"""
Visualize the Plan and Execute Multi-Agent Graph Structure.

This script shows the actual compiled graph structure for Plan & Execute.
"""

import os

os.environ["NO_COLOR"] = "1"  # Disable color output for clarity

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode

from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
from haive.agents.simple.agent import SimpleAgent

# Silence most logs for clarity
logging.getLogger().setLevel(logging.ERROR)
logging.getLogger("haive").setLevel(logging.ERROR)


def main():
    print("=" * 70)
    print("PLAN & EXECUTE MULTI-AGENT GRAPH VISUALIZATION")
    print("=" * 70)

    # Create agents
    config = AugLLMConfig()
    planner = SimpleAgent(name="planner", engine=config)
    executor = SimpleAgent(name="executor", engine=config)
    replanner = SimpleAgent(name="replanner", engine=config)

    # Create Plan & Execute system
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )

    print(f"\nSystem: {system.name}")
    print(f"Build Mode: {system.schema_build_mode}")
    print(f"State Schema: {system.state_schema_override.__name__}")

    # Build and compile the graph
    print("\n" + "-" * 70)
    print("BUILDING GRAPH...")
    print("-" * 70)

    try:
        # Build the graph
        graph = system.build_graph()
        print("✓ Graph built successfully")

        # Show the structure
        print(f"\nNodes: {list(graph.nodes.keys())}")
        print(f"\nEdges: ")
        for edge in graph.edges:
            if isinstance(edge, tuple) and len(edge) >= 2:
                print(f"  {edge[0]} -> {edge[1]}")
            elif hasattr(edge, "source") and hasattr(edge, "target"):
                print(f"  {edge.source} -> {edge.target}")
            else:
                print(f"  {edge}")

        print(f"\nBranches (Conditional Routing):")
        for branch_name, branch in graph.branches.items():
            print(f"\n  Branch: {branch_name}")
            print(f"    Source: {branch.source}")
            if hasattr(branch, "condition") and branch.condition:
                print(
                    f"    Condition: {branch.condition.__name__ if hasattr(branch.condition, '__name__') else branch.condition}"
                )
            if hasattr(branch, "destinations"):
                print(f"    Destinations: {branch.destinations}")

        # Compile the graph
        print("\n" + "-" * 70)
        print("COMPILING GRAPH...")
        print("-" * 70)

        compiled = graph.compile()
        print("✓ Graph compiled successfully")

        # Get the compiled graph structure
        if hasattr(compiled, "get_graph"):
            exec_graph = compiled.get_graph()
            print(f"\nCompiled graph structure:")
            print(f"  Nodes: {exec_graph.nodes()}")
            print(f"  Edges: {exec_graph.edges()}")

            # Show conditional edges if available
            if hasattr(exec_graph, "_conditional_edges"):
                print(f"\n  Conditional edges:")
                for source, conditions in exec_graph._conditional_edges.items():
                    print(f"    {source}: {conditions}")

        print("\n" + "-" * 70)
        print("EXECUTION FLOW:")
        print("-" * 70)
        print(
            """
1. START -> planner
   - User provides objective
   - Planner creates initial plan
   
2. planner -> executor  
   - Executor receives plan
   - Executes current step
   
3. executor -> [CONDITIONAL ROUTING]
   - route_after_execution() evaluates state:
     * If plan complete -> replanner
     * If should replan -> replanner  
     * Otherwise -> executor (continue)
     
4. replanner -> [CONDITIONAL ROUTING]
   - route_after_replan() evaluates state:
     * If final answer -> END
     * If new plan -> executor
     * Otherwise -> END
     
This is SEQUENTIAL CONDITIONAL execution, NOT parallel!
BuildMode.PARALLEL only affects how agent schemas are composed.
"""
        )

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 70)
    print("KEY POINT: Branches create CONDITIONAL ROUTING, not parallel execution!")
    print("=" * 70)


if __name__ == "__main__":
    main()
