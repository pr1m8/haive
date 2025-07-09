#!/usr/bin/env python3
"""Test the user's specific example with ReactAgent -> SimpleAgent sequential execution."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)


from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


@tool
def get_earth_age() -> int:
    """Returns the age of Earth in years"""
    return 4_543_000_000  # 4.543 billion years


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


def test_user_example():
    """Test the exact user example with ReactAgent -> SimpleAgent"""
    print("=" * 80)
    print("TEST: User Example - ReactAgent -> SimpleAgent Sequential")
    print("=" * 80)

    # Create agents as per user example
    add_aug = AugLLMConfig(tools=[add, get_earth_age])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    react_agent = ReactAgent(engine=add_aug)
    simple_agent = SimpleAgent(engine=plan_aug)

    # Create sequential agent
    seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

    # Visualize structure
    seq_agent.visualize_structure()

    # Compile and run
    try:
        print("\nCompiling sequential agent...")
        seq_agent.compile()
        print("✅ Sequential agent compiled successfully!")

        print("\nRunning with user's exact input...")
        result = seq_agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="Find out the age of earth and add it to itself, then plan a website."
                    )
                ]
            }
        )

        print("\n" + "=" * 80)
        print("RESULT:")
        print("=" * 80)

        if isinstance(result, dict):
            # Print messages
            if "messages" in result:
                print("\nMessages:")
                for msg in result["messages"]:
                    print(f"  {msg.type}: {msg.content[:200]}...")

            # Print plan if available
            if "simple_agent_plan" in result:
                print(f"\nPlan: {result['simple_agent_plan']}")
            elif "planner_plan" in result:
                print(f"\nPlan: {result['planner_plan']}")

            # Print agent outputs
            if "agent_outputs" in result:
                print("\nAgent Outputs:")
                for agent_id, output in result["agent_outputs"].items():
                    print(f"  {agent_id}: {type(output).__name__}")
        else:
            print(f"Result type: {type(result).__name__}")
            print(f"Result: {result}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


def test_with_different_tools():
    """Test with different tools and tasks"""
    print("\n" + "=" * 80)
    print("TEST: Different Tools Example")
    print("=" * 80)

    @tool
    def multiply(a: int, b: int) -> int:
        """Multiply two numbers"""
        return a * b

    @tool
    def divide(a: int, b: int) -> float:
        """Divide two numbers"""
        if b == 0:
            return float("inf")
        return a / b

    class WebsitePlan(BaseModel):
        title: str = Field(description="Website title")
        sections: list[str] = Field(description="Main sections of the website")
        technologies: list[str] = Field(description="Technologies to use")

    # Create agents with calculation tools
    calc_aug = AugLLMConfig(tools=[add, multiply, divide])
    website_aug = AugLLMConfig(
        structured_output_model=WebsitePlan, structured_output_version="v2"
    )

    calc_agent = ReactAgent(name="Calculator", engine=calc_aug)
    planner_agent = SimpleAgent(name="Website Planner", engine=website_aug)

    # Create sequential agent
    seq_agent = SequentialAgent(
        name="Calc then Plan", agents=[calc_agent, planner_agent]
    )

    try:
        seq_agent.compile()
        print("✅ Agent compiled successfully!")

        result = seq_agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="""
                Calculate (10 + 5) * 3, then divide by 5.
                After that, plan a website for a calculator app.
            """
                    )
                ]
            }
        )

        print("\nResult received!")

        if isinstance(result, dict) and "messages" in result:
            print(f"\nTotal messages: {len(result['messages'])}")
            # Show last few messages
            for msg in result["messages"][-3:]:
                print(f"\n{msg.type}:")
                print(f"  {msg.content[:300]}...")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run the user's exact example
    test_user_example()

    # Run additional test
    test_with_different_tools()

    print("\n" + "=" * 80)
    print("All tests completed!")
    print("=" * 80)
