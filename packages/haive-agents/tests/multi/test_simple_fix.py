#!/usr/bin/env python3
"""Simple test focusing on the messages issue."""

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


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

# Create sequential agent
seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

print("Compiling...")
compiled = seq_agent.compile()
print("✅ Compiled!")

print("\nRunning...")
try:
    result = seq_agent.run(
        {
            "messages": [
                HumanMessage(
                    content="Calculate 5 + 3, then plan steps for a calculator app"
                )
            ]
        }
    )

    print("\n✅ Success!")

    # Get the result as dict
    if hasattr(result, "model_dump"):
        result_dict = result.model_dump()
    else:
        result_dict = result

    # Get messages
    messages = result_dict.get("messages", [])
    print(f"\nTotal messages: {len(messages)}")

    # Get last message
    if messages:
        last_msg = messages[-1]
        print(f"\nLast message type: {type(last_msg).__name__}")
        print(f"Last message content: {getattr(last_msg, 'content', str(last_msg))}")

    # Alternative: check if there's a specific output field
    # Since the output schema is "Simple AgentOutput", check for that
    if "simple_agent_output" in result_dict:
        print(f"\nSimple Agent Output: {result_dict['simple_agent_output']}")

    # Or check agent_outputs
    if "agent_outputs" in result_dict:
        print("\nAgent outputs:")
        for agent_id, output in result_dict["agent_outputs"].items():
            print(f"  {agent_id}: {output}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    # Let's see exactly where the error occurs
    import traceback

    traceback.print_exc()

    # Try to see what we can get from partial execution
    print("\nChecking if we can get partial results...")
    try:
        # Run just the ReactAgent
        print("\nTrying ReactAgent alone...")
        react_result = react_agent.run(
            {"messages": [HumanMessage(content="Calculate 5 + 3")]}
        )

        if hasattr(react_result, "model_dump"):
            react_dict = react_result.model_dump()
        else:
            react_dict = react_result

        print(f"ReactAgent result type: {type(react_result)}")
        print(f"ReactAgent messages: {len(react_dict.get('messages', []))}")

        # Check what's in the messages
        for i, msg in enumerate(react_dict.get("messages", [])):
            msg_type = type(msg).__name__
            content = (
                getattr(msg, "content", "N/A")[:100] + "..."
                if hasattr(msg, "content")
                else str(msg)[:100] + "..."
            )
            print(f"  Message {i} ({msg_type}): {content}")

    except Exception as e2:
        print(f"ReactAgent also failed: {e2}")
