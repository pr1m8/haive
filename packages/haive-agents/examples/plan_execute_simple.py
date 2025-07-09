#!/usr/bin/env python3
"""
Simplest possible Plan and Execute example.

Uses the PlanAndExecuteAgent class directly.
"""

import asyncio
import os

from dotenv import load_dotenv
from langchain_core.tools import tool

from haive.agents.planning import PlanAndExecuteAgent

# Load environment variables
load_dotenv()


# Simple calculation tool
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
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


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
    print("\n🚀 Starting Simple Plan and Execute Demo\n")

    # Create Plan and Execute agent with tools
    agent = PlanAndExecuteAgent(
        name="plan_execute_simple",
        tools=[add, multiply, is_prime, get_nth_prime],
        verbose=True,
    )

    # Test query
    query = "Calculate the sum of the first 5 prime numbers"
    print(f"📋 Query: {query}\n")

    try:
        result = await agent.arun(query)
        print(f"\n✅ Result: {result}\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        import traceback

        traceback.print_exc()

    print("🎉 Demo completed!")


if __name__ == "__main__":
    asyncio.run(main())
