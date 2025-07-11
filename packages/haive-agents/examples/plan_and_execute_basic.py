"""Basic Plan and Execute Example.

Most basic example with minimal configuration.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.tools import tool

from haive.agents.planning import PlanAndExecuteAgent
from haive.agents.planning.p_and_e.models import Act, Plan
from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent

# Load environment variables
load_dotenv()


# Simple tools
@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Search results for '{query}': The first 5 prime numbers are 2, 3, 5, 7, and 11."


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except:
        return "Error: Invalid expression"


async def main():
    """Run the most basic Plan and Execute example."""
    # Create agents with the simplest configuration
    planner = SimpleAgent(
        name="planner",
        model="gpt-4o-mini",
        instructions="Create a plan to: {objective}",
        output_schema=Plan,
    )

    executor = ReactAgent(
        name="executor",
        model="gpt-4o-mini",
        instructions="Execute step: {current_step}",
        tools=[search, calculate],
    )

    replanner = SimpleAgent(
        name="replanner",
        model="gpt-4o-mini",
        instructions="Review progress and decide next action for: {objective}",
        output_schema=Act,
    )

    # Create Plan and Execute agent using the function
    agent = PlanAndExecuteAgent(
        planner=planner,
        executor=executor,
        replanner=replanner,
        name="plan_execute_basic",
    )

    # Simple query
    query = "Calculate the sum of the first 5 prime numbers"

    try:
        # Run with simple string input
        await agent.arun(query)

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
