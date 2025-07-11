#!/usr/bin/env python3
"""Elegant Plan & Execute using the clean MultiAgentBase structure you wanted.

This shows the elegant approach:
MultiAgentBase(
    agents=[planner, executor, replanner],
    branches=[(source, condition, destinations), ...],
    state_schema_override=PlanExecuteState,
    schema_build_mode=BuildMode.PARALLEL
)
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
from haive.agents.simple.agent import SimpleAgent


async def main():

    # Create engines with tools
    planner_engine = create_planner_aug_llm_config(model_name="gpt-4o-mini")
    executor_engine = create_executor_aug_llm_config(
        model_name="gpt-4o-mini", tools=[tavily_qna]
    )
    replanner_engine = create_replan_aug_llm_config(model_name="gpt-4o-mini")

    # Create agents - all SimpleAgent for simplicity
    planner = SimpleAgent(name="planner", engine=planner_engine)
    executor = SimpleAgent(name="executor", engine=executor_engine)
    replanner = SimpleAgent(name="replanner", engine=replanner_engine)

    # Define routing functions
    def route_after_execution(state) -> str:
        if hasattr(state, "plan") and state.plan and state.plan.is_complete:
            return "replanner"
        return "executor"

    def route_after_replan(state) -> str:
        if hasattr(state, "final_answer") and state.final_answer:
            return END
        if hasattr(state, "plan") and state.plan:
            return "executor"
        return END

    # 🎯 THE ELEGANT STRUCTURE YOU WANTED:
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
        name="Elegant Plan & Execute",
    )

    # Test routing works

    from haive.agents.planning.p_and_e.models import Plan, PlanStep

    test_plan = Plan(
        objective="Test task",
        total_steps=1,
        steps=[
            PlanStep(
                step_id=1,
                description="Test",
                expected_output="Result",
                status="pending",
            )
        ],
    )

    test_state = PlanExecuteState(
        messages=[{"role": "user", "content": "Test task"}], plan=test_plan
    )

    # Get routing functions
    executor_route = system.branches[0][1]
    replanner_route = system.branches[1][1]

    # Test routing
    executor_route(test_state)

    test_state.plan.steps[0].status = "completed"
    executor_route(test_state)

    test_state.final_answer = "Done"
    replanner_route(test_state)


if __name__ == "__main__":
    asyncio.run(main())
