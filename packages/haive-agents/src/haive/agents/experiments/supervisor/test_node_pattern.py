"""Simple test of the agent execution node pattern."""

import asyncio
from typing import Any, Dict, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.simple.agent import SimpleAgent


@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b


async def test_simple_pattern():
    """Test the basic pattern of dynamic agent execution."""
    # Create a simple math agent
    math_engine = AugLLMConfig(
        name="math_engine",
        model="gpt-4",
        tools=[add],
        system_message="You are a math helper. Use the add tool when needed.",
    ).create()

    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # Create agent registry
    agent_registry = {"math_agent": math_agent}

    # Simulate agent execution node
    async def execute_agent(agent_name: str, task: str) -> str:
        """This simulates the agent_execution_node pattern."""
        agent = agent_registry.get(agent_name)
        if not agent:
            return f"Agent {agent_name} not found"

        try:
            result = await agent.arun(task)
            return f"Success: {result}"
        except Exception as e:
            return f"Error: {e!s}"

    # Test execution

    # Test 1: Execute existing agent
    await execute_agent("math_agent", "What is 5 + 3?")

    # Test 2: Try non-existent agent
    await execute_agent("missing_agent", "Do something")

    # Test 3: Add new agent dynamically

    simple_engine = AugLLMConfig(
        name="simple_engine",
        model="gpt-4",
        system_message="You are a helpful assistant.",
    ).create()

    simple_agent = SimpleAgent(name="simple_agent", engine=simple_engine)

    # Add to registry dynamically
    agent_registry["simple_agent"] = simple_agent

    await execute_agent("simple_agent", "Say hello!")


if __name__ == "__main__":
    asyncio.run(test_simple_pattern())
