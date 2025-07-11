#!/usr/bin/env python3
"""Clean Plan and Execute example using the single-agent implementation.

This avoids the multi-agent serialization issues.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.tools import tool

from haive.agents.planning.p_and_e.agent import PlanAndExecuteAgent

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

    # Create Plan and Execute agent with tools
    agent = PlanAndExecuteAgent(
        name="plan_execute_clean",
        tools=[add, multiply, is_prime, get_nth_prime],
    )

    # Test queries
    queries = [
        "Calculate the sum of the first 5 prime numbers",
        "What is 7 times 8?",
        "Is 17 a prime number?",
    ]

    for query in queries[:1]:  # Just test the first one

        try:
            await agent.arun(query)
        except Exception:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())
