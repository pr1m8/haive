"""Simple Plan and Execute Agent Example.

A minimal example to test the Plan and Execute pattern with real execution.
"""

import asyncio
import os

from dotenv import load_dotenv
from haive.core.engine import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.planning.p_and_e.models import Act, Plan, PlanStep
from haive.agents.planning.p_and_e.state import PlanExecuteState
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent

# Load environment variables
load_dotenv()


# Simple tools for testing
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': Found relevant information about {query}."


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"


def create_plan_execute_branches(planner, executor, replanner):
    """Create the Plan & Execute routing branches."""

    def should_continue(state) -> str:
        """Decide whether to continue executing or replan."""
        # Check if we have a plan
        if not hasattr(state, "plan") or not state.plan:
            return "replanner"

        # Check if plan is complete
        if hasattr(state.plan, "is_complete") and state.plan.is_complete:
            return "replanner"

        # Check if we should replan
        if hasattr(state, "should_replan") and state.should_replan:
            return "replanner"

        return "executor"

    def should_end(state) -> str:
        """Decide whether to end or continue."""
        # Check for final answer
        if hasattr(state, "final_answer") and state.final_answer:
            return "END"

        # Check if plan has next steps
        if hasattr(state, "plan") and state.plan:
            if hasattr(state.plan, "next_step") and state.plan.next_step:
                return "executor"

        return "END"

    return [
        (executor, should_continue, {"executor": executor, "replanner": replanner}),
        (replanner, should_end, {"executor": executor, "END": "END"}),
    ]


async def main():
    """Run a simple Plan and Execute example."""
    # Create simple agents
    planner = SimpleAgent(
        name="planner",
        model="gpt-4o-mini",
        instructions="""You are a planning agent. Create a simple 2-3 step plan.

User objective: {objective}

Create a plan with clear, executable steps.""",
        output_schema=Plan,
    )

    executor = ReactAgent(
        name="executor",
        model="gpt-4o-mini",
        instructions="""You are an execution agent. Execute the current step.

Current step: {current_step}

Use the available tools to complete the step.""",
        tools=[search, calculate],
    )

    replanner = SimpleAgent(
        name="replanner",
        model="gpt-4o-mini",
        instructions="""You are a replanning agent. Assess progress and decide next action.

Original objective: {objective}
Progress so far: {past_steps}

Decide whether to continue, create a new plan, or provide the final answer.""",
        output_schema=Act,
    )

    # Create branches
    branches = create_plan_execute_branches(planner, executor, replanner)

    # Create the multi-agent system
    plan_execute_system = MultiAgentBase(
        agents=[planner, executor, replanner],
        branches=branches,
        name="plan_execute_demo",
        state_schema_override=PlanExecuteState,
        entry_points=[planner],
    )

    # Simple test query
    query = "Calculate the sum of the first 5 prime numbers"

    try:
        # Run the system
        await plan_execute_system.arun({"objective": query})

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
