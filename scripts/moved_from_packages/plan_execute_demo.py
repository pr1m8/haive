#!/usr/bin/env python3
"""Demo of Plan and Execute Multi-Agent System using Enhanced MultiAgentBase.

This shows:
1. How branches create conditional routing (NOT parallel execution)
2. The actual graph structure being built
3. How BuildMode affects schema composition, not execution flow
"""

from haive.agents.multi.enhanced_base import (
    MultiAgentBase,
    create_plan_execute_multi_agent,
)
from haive.agents.planning.p_and_e.models import Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode
from langgraph.graph import END


def visualize_graph_structure(system):
    """Helper to visualize the graph structure."""
    # Build the graph
    try:
        graph = system.build_graph()

        # Get nodes
        if hasattr(graph, "_nodes") or hasattr(graph, "nodes"):
            pass
        else:
            pass

        # Get edges
        if hasattr(graph, "edges"):
            for edge in graph.edges:
                if hasattr(edge, "source") and hasattr(edge, "target"):
                    pass
                else:
                    pass

        # Get branches (conditional routing)
        if hasattr(graph, "branches"):
            for _branch_name, branch in graph.branches.items():
                if hasattr(branch, "condition"):
                    pass
                if hasattr(branch, "destinations"):
                    pass
                if hasattr(branch, "default"):
                    pass

        return graph
    except Exception:
        import traceback

        traceback.print_exc()
        return None


def main():
    # Create configuration
    config = AugLLMConfig(
        name="demo_llm", system_message="You are a helpful assistant.", temperature=0.7
    )

    # Create agents
    planner = SimpleAgent(name="planner", engine=config)

    executor = SimpleAgent(name="executor", engine=config)

    replanner = SimpleAgent(name="replanner", engine=config)

    # Create Plan & Execute system using convenience function
    pe_system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,  # This affects schema composition, NOT execution flow!
    )

    # Show the branches
    if pe_system.branches:
        for _i, branch in enumerate(pe_system.branches):
            source, condition, destinations = branch[:3]
            source.name if hasattr(source, "name") else str(source)

    # Visualize the graph
    graph = visualize_graph_structure(pe_system)

    # Try to compile and see the actual runnable graph
    if graph:
        try:
            compiled = graph.compile()

            # Show the actual execution graph structure
            if hasattr(compiled, "get_graph"):
                compiled.get_graph()
        except Exception:
            pass

    # Define routing functions
    def route_after_execution(state) -> str:
        """Routing logic after executor runs."""
        if hasattr(state, "plan") and state.plan:
            if state.plan.is_complete:
                return "replanner"
            if hasattr(state, "should_replan") and state.should_replan:
                return "replanner"
            return "executor"
        return "replanner"

    def route_after_replan(state) -> str:
        """Routing logic after replanner runs."""
        if hasattr(state, "final_answer") and state.final_answer:
            return END
        if hasattr(state, "plan") and state.plan:
            return "executor"
        return END

    # Manual system creation
    manual_system = MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=[
            # After executor runs, route based on plan status
            (
                executor,
                route_after_execution,
                {"executor": executor, "replanner": replanner},
            ),
            # After replanner runs, route based on decision
            (replanner, route_after_replan, {"executor": executor, END: END}),
        ],
        entry_points=[planner],  # Start with planner
        finish_points=[],  # No default finish points - handled by routing to END
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,  # Again, this is for schema, not execution!
        name="Manual Plan & Execute",
    )

    # Visualize manual graph
    visualize_graph_structure(manual_system)

    # Demo routing logic

    # Create sample states
    incomplete_plan = Plan(
        objective="Test task",
        total_steps=2,
        steps=[
            PlanStep(
                step_id=1,
                description="Step 1",
                expected_output="Result 1",
                status="completed",
            ),
            PlanStep(
                step_id=2,
                description="Step 2",
                expected_output="Result 2",
                status="pending",
            ),
        ],
    )

    complete_plan = Plan(
        objective="Test task",
        total_steps=1,
        steps=[
            PlanStep(
                step_id=1,
                description="Step 1",
                expected_output="Result 1",
                status="completed",
            )
        ],
    )

    # Test incomplete plan state
    state1 = PlanExecuteState(plan=incomplete_plan, messages=[])
    route_after_execution(state1)

    # Test complete plan state
    state2 = PlanExecuteState(plan=complete_plan, messages=[])
    route_after_execution(state2)

    # Test final answer state
    state3 = PlanExecuteState(final_answer="Task completed!", messages=[])
    route_after_replan(state3)


if __name__ == "__main__":
    main()
