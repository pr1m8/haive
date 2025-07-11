#!/usr/bin/env python3
"""Example of Plan and Execute agent using SEQUENCE mode to avoid serialization issues.

This demonstrates the Plan and Execute pattern with sequential execution.
"""

import asyncio
import os

from dotenv import load_dotenv
from haive.core.schema.agent_schema_composer import BuildMode
from langchain_core.tools import tool

from haive.agents.multi.enhanced_base import MultiAgentBase
from haive.agents.planning.plan_and_execute_multi import create_plan_execute_branches
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent

# Load environment variables
load_dotenv()


# Simple calculation tool
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))


async def main():

    # Create agents
    planner = SimpleAgent(
        name="planner",
        system_prompt="You are a planning agent. Create step-by-step plans to solve problems.",
    )

    executor = ReactAgent(
        name="executor",
        tools=[add, is_prime],
        system_prompt="You are an execution agent. Execute the given steps using available tools.",
    )

    replanner = SimpleAgent(
        name="replanner",
        system_prompt="You are a replanning agent. Review progress and decide next steps.",
    )

    # Create branches for Plan and Execute
    branches = create_plan_execute_branches(planner, executor, replanner)

    # Create multi-agent system with SEQUENCE mode
    plan_execute_agent = MultiAgentBase(
        name="plan_execute_sequence",
        agents=[planner, executor, replanner],
        branches=branches,
        schema_build_mode=BuildMode.SEQUENCE,  # Use SEQUENCE mode
    )

    # Test query
    query = "Calculate the sum of the first 5 prime numbers"

    try:
        await plan_execute_agent.arun(query)
    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
