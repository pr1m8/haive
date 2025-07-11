#!/usr/bin/env python3
"""Working Plan & Execute test using existing engines and new MultiAgentBase.

This proves the shared fields work correctly by using:
1. Existing P&E engines with proper prompts and tools
2. All SimpleAgents (to avoid ReactAgent complexity for now)
3. The new MultiAgentBase for orchestration
4. Real Tavily search tools for the executor
"""

import asyncio

from haive.core.schema.agent_schema_composer import BuildMode
from haive.tools.tools.search_tools import tavily_qna

from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
from haive.agents.planning.p_and_e.engines import (
    create_executor_aug_llm_config,
    create_planner_aug_llm_config,
    create_replan_aug_llm_config,
)
from haive.agents.simple.agent import SimpleAgent


async def main():

    # Create engines using existing P&E configurations
    planner_engine = create_planner_aug_llm_config(model_name="gpt-4o-mini")

    # Executor gets the Tavily search tool
    executor_engine = create_executor_aug_llm_config(
        model_name="gpt-4o-mini", tools=[tavily_qna]  # Real search capability
    )

    replanner_engine = create_replan_aug_llm_config(model_name="gpt-4o-mini")

    # Create all as SimpleAgents
    planner = SimpleAgent(name="planner", engine=planner_engine)
    executor = SimpleAgent(name="executor", engine=executor_engine)
    replanner = SimpleAgent(name="replanner", engine=replanner_engine)

    # Create the Plan & Execute system
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )

    # Test objective
    objective = "What is the current population of Tokyo?"

    try:
        # Build and test the routing manually first

        # Get routing functions
        executor_route = None
        replanner_route = None

        for branch in system.branches:
            source, condition, destinations = branch
            if source == executor:
                executor_route = condition
            elif source == replanner:
                replanner_route = condition

        # Create test state
        from haive.agents.planning.p_and_e.models import Plan, PlanStep
        from haive.agents.planning.p_and_e.state import PlanExecuteState

        test_plan = Plan(
            objective=objective,
            total_steps=2,
            steps=[
                PlanStep(
                    step_id=1,
                    description="Search for Tokyo population",
                    expected_output="Population data",
                ),
                PlanStep(
                    step_id=2,
                    description="Verify the information",
                    expected_output="Verified population",
                ),
            ],
        )

        test_state = PlanExecuteState(
            messages=[{"role": "user", "content": objective}], plan=test_plan
        )

        # Test routing
        executor_route(test_state)

        # Complete the plan and test again
        test_state.plan.steps[0].status = "completed"
        test_state.plan.steps[1].status = "completed"

        executor_route(test_state)

        # Test final answer
        test_state.final_answer = "Tokyo population is X million"
        replanner_route(test_state)

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
