#!/usr/bin/env python3
"""Visualize the Plan and Execute Multi-Agent Graph Structure.

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

    # Build and compile the graph

    try:
        # Build the graph
        graph = system.build_graph()

        # Show the structure
        for edge in graph.edges:
            if isinstance(edge, tuple) and len(edge) >= 2:
                pass
            else:
                pass

        for _branch_name, branch in graph.branches.items():
            if hasattr(branch, "condition") and branch.condition:
                pass
            if hasattr(branch, "destinations"):
                pass

        # Compile the graph

        compiled = graph.compile()

        # Get the compiled graph structure
        if hasattr(compiled, "get_graph"):
            exec_graph = compiled.get_graph()

            # Show conditional edges if available
            if hasattr(exec_graph, "_conditional_edges"):
                for _source, _conditions in exec_graph._conditional_edges.items():
                    pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
