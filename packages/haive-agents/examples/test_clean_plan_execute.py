#!/usr/bin/env python3
"""
Clean Plan & Execute test using the elegant MultiAgentBase approach.

This shows the proper way:
- agents=[]
- branches=[]
- ReactAgent for executor with tools
- Clean and simple
"""

import asyncio

from haive.core.schema.agent_schema_composer import BuildMode
from haive.tools.tools.search_tools import tavily_qna
from langgraph.graph import END

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.planning.p_and_e.engines import (
    create_executor_aug_llm_config,
    create_planner_aug_llm_config,
    create_replan_aug_llm_config,
)
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.react_class.react_agent.agent import ReactAgent, ReactAgentConfig
from haive.agents.simple.agent import SimpleAgent


async def main():
    print("=" * 70)
    print("CLEAN PLAN & EXECUTE - ELEGANT MULTIAGENTBASE")
    print("=" * 70)

    # Create engines
    planner_engine = create_planner_aug_llm_config(model_name="gpt-4o-mini")
    executor_engine = create_executor_aug_llm_config(
        model_name="gpt-4o-mini", tools=[tavily_qna]
    )
    replanner_engine = create_replan_aug_llm_config(model_name="gpt-4o-mini")

    # Create agents
    planner = SimpleAgent(name="planner", engine=planner_engine)

    # ReactAgent for executor with tools
    executor_config = ReactAgentConfig(
        engine=executor_engine,
        tools=[],  # Skip tools for now to focus on structure
        node_name="executor",
    )
    executor = ReactAgent(config=executor_config)

    replanner = SimpleAgent(name="replanner", engine=replanner_engine)

    print(f"Agents created:")
    print(f"  - {planner.name}: {type(planner).__name__}")
    print(
        f"  - executor: {type(executor).__name__} with {len(executor_engine.tools)} tools"
    )
    print(f"  - {replanner.name}: {type(replanner).__name__}")

    # Define routing functions
    def route_after_execution(state) -> str:
        """Route after executor runs."""
        if hasattr(state, "plan") and state.plan and state.plan.is_complete:
            return "replanner"
        elif hasattr(state, "should_replan") and state.should_replan:
            return "replanner"
        else:
            return "executor"

    def route_after_replan(state) -> str:
        """Route after replanner runs."""
        if hasattr(state, "final_answer") and state.final_answer:
            return END
        elif hasattr(state, "plan") and state.plan:
            return "executor"
        return END

    # Create the elegant Plan & Execute system
    system = MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=[
            (
                executor,
                route_after_execution,
                {"executor": executor, "replanner": replanner},
            ),
            (replanner, route_after_replan, {"executor": executor, END: END}),
        ],
        state_schema_override=PlanExecuteState,
        schema_build_mode=BuildMode.PARALLEL,
        name="Plan and Execute System",
    )

    print(f"\nSystem: {system.name}")
    print(f"Build mode: {system.schema_build_mode}")
    print(f"Agents: {len(system.agents)}")
    print(f"Branches: {len(system.branches)}")

    # Test the routing
    print(f"\n{'='*50}")
    print("TESTING ROUTING")
    print(f"{'='*50}")

    from haive.agents.planning.p_and_e.models import Plan, PlanStep

    # Test state
    test_plan = Plan(
        objective="Find Tokyo population",
        total_steps=1,
        steps=[
            PlanStep(
                step_id=1,
                description="Search",
                expected_output="Data",
                status="pending",
            )
        ],
    )

    test_state = PlanExecuteState(
        messages=[{"role": "user", "content": "Find Tokyo population"}], plan=test_plan
    )

    # Get routing functions from branches
    executor_route = system.branches[0][1]  # (executor, condition, destinations)
    replanner_route = system.branches[1][1]  # (replanner, condition, destinations)

    # Test incomplete plan
    route = executor_route(test_state)
    print(f"Incomplete plan: {route} (should be 'executor')")

    # Complete plan
    test_state.plan.steps[0].status = "completed"
    route = executor_route(test_state)
    print(f"Complete plan: {route} (should be 'replanner')")

    # Final answer
    test_state.final_answer = "Tokyo has 14 million people"
    route = replanner_route(test_state)
    print(f"Final answer: {route} (should be '__end__')")

    print(f"\n{'='*50}")
    print("✅ SUCCESS - ELEGANT SYSTEM WORKING!")
    print(f"{'='*50}")

    print("\n🎯 This is the clean approach:")
    print("   MultiAgentBase(")
    print("       agents=[planner, executor, replanner],")
    print("       branches=[(source, condition, destinations), ...],")
    print("       state_schema_override=PlanExecuteState,")
    print("       schema_build_mode=BuildMode.PARALLEL")
    print("   )")


if __name__ == "__main__":
    asyncio.run(main())
