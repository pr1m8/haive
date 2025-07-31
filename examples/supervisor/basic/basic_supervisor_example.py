#!/usr/bin/env python3
"""Basic Dynamic Supervisor Example.

This example demonstrates how to create a simple dynamic supervisor
that can route tasks to different specialized agents.
"""

import asyncio

from haive.agents.dynamic_supervisor import create_dynamic_supervisor
from haive.agents.simple import SimpleAgent
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.tools import tool


@tool
def calculate(expression: str) -> str:
    """Calculate a mathematical expression."""
    try:
        result = eval(expression)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {e!s}"


async def main():
    """Run the basic supervisor example."""
    # Create specialized agents

    # Math agent
    math_engine = AugLLMConfig(
        name="math_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        tools=[calculate],
        system_message="You are a math expert. Use the calculate tool for mathematical operations.",
    )
    math_agent = SimpleAgent(name="math_agent", engine=math_engine)

    # General assistant agent
    general_engine = AugLLMConfig(
        name="general_engine",
        llm_config=AzureLLMConfig(model="gpt-4o"),
        system_message="You are a helpful general assistant. Answer questions clearly.",
    )
    general_agent = SimpleAgent(name="general_agent", engine=general_engine)

    # Create supervisor using factory function
    supervisor = create_dynamic_supervisor(
        name="task_supervisor",
        model="gpt-4o",
        temperature=0.0,
        enable_agent_builder=False,
    )

    # Create initial state and add agents
    state = supervisor.create_initial_state()
    state.add_agent("math_agent", math_agent, "Expert at mathematical calculations")
    state.add_agent("general_agent", general_agent, "General purpose assistant")

    # Test 1: Math task
    await supervisor.arun("Calculate the result of 15 * 23 + 7", state=state)

    # Test 2: General task
    await supervisor.arun("What is the capital of France?", state=state)

    # Test 3: Task requiring reasoning about which agent to use
    await supervisor.arun(
        "I need help with both math and general knowledge. First, calculate 100 / 4, then tell me what that number represents in terms of a perfect score.",
        state=state,
    )


if __name__ == "__main__":
    asyncio.run(main())
