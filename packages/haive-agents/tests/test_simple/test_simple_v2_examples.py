"""Simple examples showing V2 SimpleAgent and ReactAgent usage.

This test demonstrates the exact usage patterns you requested:
1. SimpleAgent V2 with Plan model
2. ReactAgent with add tool
3. Both with and without safety net configurations
"""

import asyncio
import uuid
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

# Import agents
from haive.agents.simple.agent_v2 import SimpleAgentV2  # V2 with safety nets

# Try to import ReactAgent
try:
    from haive.agents.react.agent import ReactAgent

    REACT_AGENT_AVAILABLE = True
except ImportError:
    REACT_AGENT_AVAILABLE = False
    ReactAgent = None


# Define a simple tool
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


# Define a Plan model for structured output
class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


async def example_simple_agent_v2_with_plan():
    """Example: SimpleAgent V2 with Plan model - your exact pattern."""

    # Create engine configurations exactly as you specified
    plan_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="plan_engine",
        system_message="You are a helpful assistant that creates plans.",
        structured_output_model=Plan,
        structured_output_version="v2",
    )

    # Create agents - your exact pattern
    simple_agent = SimpleAgentV2(
        name="plan_agent_v2",
        engine=plan_aug,
        enable_persistence=False,  # For testing
        # V2 specific config
        use_parser_safety_net=True,
        parser_safety_net_mode="create",
    )


    # Test with a simple request
    try:
        result = await simple_agent.ainvoke(
            {"messages": [HumanMessage(content="Create a plan for making coffee")]}
        )


        # Show any Plan results
        for key, value in result.items():
            if key != "messages" and value is not None:
                pass

        return True

    except Exception as e:
        return False


async def example_react_agent_with_add():
    """Example: ReactAgent with add tool - your exact pattern."""
    if not REACT_AGENT_AVAILABLE:
        return True


    # Create engine configurations exactly as you specified
    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="add_engine",
        system_message="You are a helpful math assistant.",
        tools=[add],
    )

    # Create agents - your exact pattern
    react_agent = ReactAgent(
        name="math_agent", engine=add_aug, enable_persistence=False  # For testing
    )


    # Test with a simple math request
    try:
        result = await react_agent.ainvoke(
            {"messages": [HumanMessage(content="What is 5 + 3?")]}
        )


        # Show the conversation
        for i, msg in enumerate(result.get("messages", [])):
            pass

        return True

    except Exception as e:
        return False


async def example_simple_agent_v2_configurations():
    """Example: Different V2 configuration options."""

    add_aug = AugLLMConfig(
        id=f"engine_{uuid.uuid4().hex[:8]}",
        name="config_engine",
        system_message="You are a helpful assistant.",
        tools=[add],
    )

    # Example 1: Full V2 with all safety nets
    agent_full_v2 = SimpleAgentV2(
        name="full_v2",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=True,
        parser_safety_net_mode="create",
    )

    # Example 2: V2 with warnings only
    agent_warn_only = SimpleAgentV2(
        name="warn_only",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=True,
        parser_safety_net_mode="warn",
    )

    # Example 3: V2 with V1 parser behavior
    agent_v1_parser = SimpleAgentV2(
        name="v1_parser",
        engine=add_aug,
        enable_persistence=False,
        use_parser_safety_net=False,
    )


    return True


async def example_direct_usage_pattern():
    """Example: Direct usage pattern as you specified."""

    # Define your exact pattern
    @tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers."""
        return a + b

    class Plan(BaseModel):
        steps: list[str] = Field(description="list of steps")

    # Create engine configurations
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create agents
    simple_agent = SimpleAgentV2(engine=plan_aug)

    if REACT_AGENT_AVAILABLE:
        react_agent = ReactAgent(engine=add_aug)
    else:
        pass")


    return True


async def main():
    """Run all examples."""

    examples = [
        ("SimpleAgent V2 + Plan", example_simple_agent_v2_with_plan),
        ("ReactAgent + Add Tool", example_react_agent_with_add),
        ("V2 Configuration Options", example_simple_agent_v2_configurations),
        ("Direct Usage Pattern", example_direct_usage_pattern),
    ]

    results = []

    for name, example_func in examples:
        try:
            result = await example_func()
            results.append((name, result))
        except Exception as e:
            results.append((name, False))


    for name, success in results:
        status = "✅ SUCCESS" if success else "❌ FAILED"

    all_success = all(result for _, result in results)
    if all_success:
        if REACT_AGENT_AVAILABLE:
            pass")
    else:
        passes")



if __name__ == "__main__":
    asyncio.run(main())
