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
    """Returns the sum of two numbers"""
    return a + b


# Test ReactAgent and examine its output
add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)
react_agent.compile()

print("Running ReactAgent...")
result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

print("\n" + "=" * 80)
print("REACTAGENT OUTPUT ANALYSIS")
print("=" * 80)

print(f"\nResult type: {type(result)}")

# Convert to dict if it's a Pydantic model
if hasattr(result, "model_dump"):
    result_dict = result.model_dump()
    print(f"Result keys: {list(result_dict.keys())}")
else:
    result_dict = result
    print(
        f"Result keys: {list(result.keys()) if hasattr(result, 'keys') else 'Not a dict'}"
    )

# Examine messages
messages = result_dict.get("messages", []) if isinstance(result_dict, dict) else []
print(f"\nTotal messages: {len(messages)}")

for i, msg in enumerate(messages):
    print(f"\n--- Message {i} ---")
    print(f"Type: {msg.__class__.__name__}")
    print(f"Content: {getattr(msg, 'content', 'N/A')[:100]}...")

    # For AIMessage, check tool calls
    if isinstance(msg, AIMessage):
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            print("Tool calls:")
            for tc in msg.tool_calls:
                print(f"  - {tc}")

    # For ToolMessage, check fields
    if isinstance(msg, ToolMessage):
        print("Fields:")
        print(f"  - tool_call_id: {getattr(msg, 'tool_call_id', 'MISSING')}")
        print(f"  - name: {getattr(msg, 'name', 'MISSING')}")
        print(f"  - content: {getattr(msg, 'content', 'MISSING')}")

        # Check all attributes
        print(
            f"  - All attributes: {[attr for attr in dir(msg) if not attr.startswith('_')]}"
        )

        # Try to dump as dict
        try:
            msg_dict = msg.model_dump()
            print(f"  - As dict: {json.dumps(msg_dict, indent=2)}")
        except Exception as e:
            print(f"  - Error dumping as dict: {e}")

# Check if there are any tool messages without tool_call_id
print("\n" + "=" * 80)
print("CHECKING FOR TOOL MESSAGE ISSUES")
print("=" * 80)

problematic_messages = []
for i, msg in enumerate(messages):
    if isinstance(msg, ToolMessage):
        if not hasattr(msg, "tool_call_id") or not msg.tool_call_id:
            problematic_messages.append((i, msg))

if problematic_messages:
    print(f"\n⚠️  Found {len(problematic_messages)} ToolMessages without tool_call_id!")
    for idx, msg in problematic_messages:
        print(f"  - Message {idx}: {msg}")
else:
    print("\n✅ All ToolMessages have tool_call_id")

# Check raw message data
print("\n" + "=" * 80)
print("RAW MESSAGE DATA")
print("=" * 80)

for i, msg in enumerate(messages):
    if isinstance(msg, (AIMessage, ToolMessage)):
        print(f"\nMessage {i} raw data:")
        try:
            # Try different ways to get the raw data
            if hasattr(msg, "__dict__"):
                print(f"  __dict__: {msg.__dict__}")
            if hasattr(msg, "additional_kwargs"):
                print(f"  additional_kwargs: {msg.additional_kwargs}")
        except Exception as e:
            print(f"  Error getting raw data: {e}")
