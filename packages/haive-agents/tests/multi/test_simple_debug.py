#!/usr/bin/env python3
"""Simple debug test for tool message serialization."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import tool

from haive.agents.react.agent import ReactAgent


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


# Create a simple ReactAgent
add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)

# Compile the agent
react_agent.compile()

# Test with a simple addition
try:
    result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

    print("✅ ReactAgent worked!")

    # Check the messages in the result
    if hasattr(result, "messages"):
        messages = result.messages
        print(f"\nFinal result has {len(messages)} messages:")

        for i, msg in enumerate(messages):
            print(f"  {i}: {type(msg).__name__}")
            if isinstance(msg, ToolMessage):
                print(f"    tool_call_id: {getattr(msg, 'tool_call_id', 'MISSING')}")
                print(f"    name: {getattr(msg, 'name', 'MISSING')}")
                print(f"    content: {msg.content}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
