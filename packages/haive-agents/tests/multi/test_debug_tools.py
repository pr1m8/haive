#!/usr/bin/env python3
"""Debug tool handling in multi-agent system."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Enable debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    logger.info(f"Tool 'add' called with a={a}, b={b}")
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Test just the ReactAgent first
print("=" * 80)
print("TEST 1: ReactAgent Only")
print("=" * 80)

add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)

print("Compiling ReactAgent...")
react_agent.compile()

print("Running ReactAgent...")
try:
    result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

    print("\n✅ ReactAgent Success!")
    print(f"Messages: {len(result.get('messages', []))}")

    # Check messages
    for i, msg in enumerate(result.get("messages", [])):
        print(f"\nMessage {i} ({msg.__class__.__name__}):")
        print(f"  Content: {getattr(msg, 'content', 'N/A')[:100]}...")

        # Check for tool calls
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
            print(f"  Tool calls: {msg.tool_calls}")

        # Check tool messages
        if hasattr(msg, "tool_call_id"):
            print(f"  Tool call ID: {msg.tool_call_id}")

except Exception as e:
    print(f"\n❌ ReactAgent Error: {e}")
    import traceback

    traceback.print_exc()


# Test the sequential agent
print("\n" + "=" * 80)
print("TEST 2: Sequential Agent (ReactAgent -> SimpleAgent)")
print("=" * 80)

plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent2 = ReactAgent(name="Calculator", engine=add_aug)
simple_agent = SimpleAgent(name="Planner", engine=plan_aug)

seq_agent = SequentialAgent(agents=[react_agent2, simple_agent])

print("Compiling Sequential Agent...")
seq_agent.compile()

print("Running Sequential Agent...")
try:
    result = seq_agent.run(
        {
            "messages": [
                HumanMessage(
                    content="Calculate 10 + 20, then plan steps to build a calculator app"
                )
            ]
        }
    )

    print("\n✅ Sequential Agent Success!")
    print(f"Messages: {len(result.get('messages', []))}")

    # Show last AI message
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            print(f"\nLast AI message: {msg.content[:200]}...")
            break

except Exception as e:
    print(f"\n❌ Sequential Agent Error: {e}")
    import traceback

    traceback.print_exc()
