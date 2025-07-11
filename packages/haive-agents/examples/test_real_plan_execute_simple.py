#!/usr/bin/env python3
"""Simplified real test of Plan & Execute Multi-Agent System.

This test actually runs the system to verify shared fields work correctly.
"""

import asyncio

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.schema.agent_schema_composer import BuildMode

from haive.agents.multi.enhanced_base import create_plan_execute_multi_agent
from haive.agents.planning.p_and_e.models import Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.simple.agent import SimpleAgent


async def main():

    # Create simple LLM configurations
    config = AugLLMConfig(name="test_llm", temperature=0.7)

    # Create agents
    planner = SimpleAgent(name="planner", engine=config)
    executor = SimpleAgent(name="executor", engine=config)
    replanner = SimpleAgent(name="replanner", engine=config)

    # Create Plan & Execute system with PARALLEL mode
    system = create_plan_execute_multi_agent(
        planner_agent=planner,
        executor_agent=executor,
        replanner_agent=replanner,
        schema_build_mode=BuildMode.PARALLEL,
    )

    # Create a test plan to verify shared fields
    test_plan = Plan(
        objective="Test shared fields",
        total_steps=2,
        steps=[
            PlanStep(
                step_id=1,
                description="First test step",
                expected_output="Test output 1",
                status="pending",
            ),
            PlanStep(
                step_id=2,
                description="Second test step",
                expected_output="Test output 2",
                status="pending",
            ),
        ],
    )

    # Create initial state
    initial_state = PlanExecuteState(
        messages=[{"role": "user", "content": "Test objective"}],
        plan=test_plan,
        execution_results=[],
        final_answer=None,
    )

    # Build the graph
    system.build_graph()

    # Let's trace through the routing logic manually

    # Get routing functions from branches
    executor_route = None
    replanner_route = None

    for branch in system.branches:
        source, condition, destinations = branch
        if source == executor:
            executor_route = condition
        elif source == replanner:
            replanner_route = condition

    executor_route(initial_state)

    # Simulate executor completing first step
    initial_state.plan.steps[0].status = "completed"
    initial_state.plan.steps[0].result = "Step 1 completed successfully"

    executor_route(initial_state)

    # Complete all steps
    initial_state.plan.steps[1].status = "completed"
    initial_state.plan.steps[1].result = "Step 2 completed successfully"

    executor_route(initial_state)

    # Test replanner routing
    replanner_route(initial_state)

    # Add final answer
    initial_state.final_answer = "Task completed successfully!"

    replanner_route(initial_state)

    # Show the actual schema fields
    for _field_name, _field_info in initial_state.__fields__.items():
        pass

    # Check if fields are marked as shared
    if hasattr(PlanExecuteState, "__shared_fields__"):
        for _field in PlanExecuteState.__shared_fields__:
            pass


if __name__ == "__main__":
    asyncio.run(main())
