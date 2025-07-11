#!/usr/bin/env python3
"""Working Plan and Execute example.

This demonstrates a simpler approach that avoids the serialization issues.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.tools import tool

from haive.agents.react import ReactAgent
from haive.agents.simple import SimpleAgent

# Load environment variables
load_dotenv()


# Simple calculation tools
@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


@tool
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    return all(n % i != 0 for i in range(2, int(n**0.5) + 1))


@tool
def get_nth_prime(n: int) -> int:
    """Get the nth prime number (1-indexed)."""
    if n < 1:
        return 0

    count = 0
    num = 2
    while count < n:
        if is_prime(num):
            count += 1
            if count == n:
                return num
        num += 1
    return num


async def main():

    # Create a simple planning agent
    planner = SimpleAgent(
        name="planner",
        system_prompt="""You are a planning agent. When given a task, create a step-by-step plan.

Format your plan as:
1. First step
2. Second step
3. Third step
...

Be specific and break down complex calculations into simple steps.""",
    )

    # Create an executor agent with tools
    executor = ReactAgent(
        name="executor",
        tools=[add, multiply, is_prime, get_nth_prime],
        system_prompt="You are an execution agent. Follow the given plan and use tools to complete each step.",
        max_steps=10,
    )

    # Test query
    query = "Calculate the sum of the first 5 prime numbers"

    try:
        # Step 1: Create plan
        plan_result = await planner.arun(query)

        # Step 2: Execute plan
        execution_prompt = f"""Execute this plan step by step:

{plan_result}

Original task: {query}

Use the available tools to complete each step and provide the final answer."""

        await executor.arun(execution_prompt)

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
