#!/usr/bin/env python3
"""Debug messages handling in multi-agent system."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

import json

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool

from haive.agents.react.agent import ReactAgent


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


# Test ReactAgent and examine its output
add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)
react_agent.compile()

result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})



# Convert to dict if it's a Pydantic model
if hasattr(result, "model_dump"):
    result_dict = result.model_dump()
else:
    result_dict = result

# Examine messages
messages = result_dict.get("messages", []) if isinstance(result_dict, dict) else []

for i, msg in enumerate(messages):

    # For AIMessage, check tool calls
    if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls") and msg.tool_calls:
        print("Tool calls:")
        for tc in msg.tool_calls:
            print(f"  - {tc}")

    # For ToolMessage, check fields
    if isinstance(msg, ToolMessage):

        # Check all attributes

        # Try to dump as dict
        try:
            msg_dict = msg.model_dump()
        except Exception as e:
            pass

# Check if there are any tool messages without tool_call_id

problematic_messages = []
for i, msg in enumerate(messages):
    if isinstance(msg, ToolMessage):
        if not hasattr(msg, "tool_call_id") or not msg.tool_call_id:
            problematic_messages.append((i, msg))

if problematic_messages:
    for idx, msg in problematic_messages:
        pass
else:
    pass")

# Check raw message data

for i, msg in enumerate(messages):
    if isinstance(msg, AIMessage | ToolMessage):
        try:
            # Try different ways to get the raw data
            if hasattr(msg, "__dict__"):
                pass
            if hasattr(msg, "additional_kwargs"):
                pass
        except Exception as e:
            pass
