#!/usr/bin/env python3
"""Test message serialization issue."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

import json

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from langchain_core.messages.utils import messages_from_dict
from pydantic import BaseModel, Field

# Test 1: Direct ToolMessage serialization
print("=" * 80)
print("TEST 1: Direct ToolMessage Serialization")
print("=" * 80)

# Create a ToolMessage with all required fields
tool_msg = ToolMessage(content="Result: 8", tool_call_id="call_123", name="add")

print("Original ToolMessage:")
print(f"  content: {tool_msg.content}")
print(f"  tool_call_id: {tool_msg.tool_call_id}")
print(f"  name: {tool_msg.name}")

# Try different serialization methods
print("\n1. Using dict():")
try:
    msg_dict = dict(tool_msg)
    print(f"  Result: {msg_dict}")
except Exception as e:
    print(f"  Error: {e}")

print("\n2. Using model_dump():")
try:
    msg_dict = tool_msg.model_dump()
    print(f"  Result: {json.dumps(msg_dict, indent=2)}")
    print(f"  Has tool_call_id: {'tool_call_id' in msg_dict}")
except Exception as e:
    print(f"  Error: {e}")

print("\n3. Using __dict__:")
try:
    msg_dict = tool_msg.__dict__
    print(f"  Result: {msg_dict}")
except Exception as e:
    print(f"  Error: {e}")


# Test 2: Messages in a Pydantic model
print("\n" + "=" * 80)
print("TEST 2: Messages in Pydantic Model")
print("=" * 80)


class TestState(BaseModel):
    messages: list[BaseMessage] = Field(default_factory=list)


# Create state with messages including ToolMessage
state = TestState(
    messages=[
        HumanMessage(content="Calculate 5 + 3"),
        AIMessage(
            content="",
            tool_calls=[{"id": "call_123", "name": "add", "args": {"a": 5, "b": 3}}],
        ),
        ToolMessage(content="8", tool_call_id="call_123", name="add"),
        AIMessage(content="The result is 8"),
    ]
)

print(f"Original state has {len(state.messages)} messages")

# Serialize the state
print("\nSerializing state with model_dump():")
state_dict = state.model_dump()

print(f"State dict type: {type(state_dict)}")
print(f"Messages field type: {type(state_dict['messages'])}")
print(f"Number of messages: {len(state_dict['messages'])}")

# Check the tool message
for i, msg in enumerate(state_dict["messages"]):
    if msg.get("type") == "tool":
        print(f"\nTool message at index {i}:")
        print(f"  Keys: {list(msg.keys())}")
        print(f"  Content: {msg.get('content')}")
        print(f"  tool_call_id: {msg.get('tool_call_id', 'MISSING')}")
        print(f"  name: {msg.get('name', 'MISSING')}")
        print(f"  Full message: {json.dumps(msg, indent=2)}")


# Test 3: Recreating messages from dict
print("\n" + "=" * 80)
print("TEST 3: Recreating Messages from Dict")
print("=" * 80)

# Try to recreate messages from the serialized dict
try:
    new_messages = messages_from_dict(state_dict["messages"])
    print(f"✅ Successfully recreated {len(new_messages)} messages")

    # Check the tool message
    for i, msg in enumerate(new_messages):
        if isinstance(msg, ToolMessage):
            print(f"\nRecreated ToolMessage at index {i}:")
            print(f"  content: {msg.content}")
            print(f"  tool_call_id: {getattr(msg, 'tool_call_id', 'MISSING')}")
            print(f"  name: {getattr(msg, 'name', 'MISSING')}")

except Exception as e:
    print(f"❌ Error recreating messages: {e}")
    import traceback

    traceback.print_exc()


# Test 4: Custom serialization fix
print("\n" + "=" * 80)
print("TEST 4: Custom Serialization Fix")
print("=" * 80)


def serialize_messages(messages: list[BaseMessage]) -> list[dict]:
    """Custom serialization that preserves all fields."""
    result = []
    for msg in messages:
        msg_dict = msg.model_dump()

        # For ToolMessage, ensure tool_call_id is included
        if isinstance(msg, ToolMessage):
            if hasattr(msg, "tool_call_id") and "tool_call_id" not in msg_dict:
                msg_dict["tool_call_id"] = msg.tool_call_id
            if hasattr(msg, "name") and "name" not in msg_dict:
                msg_dict["name"] = msg.name

        result.append(msg_dict)
    return result


# Test the custom serialization
custom_serialized = serialize_messages(state.messages)
print(f"Custom serialized {len(custom_serialized)} messages")

for i, msg in enumerate(custom_serialized):
    if msg.get("type") == "tool":
        print(f"\nCustom serialized tool message at index {i}:")
        print(f"  Has tool_call_id: {'tool_call_id' in msg}")
        print(f"  tool_call_id value: {msg.get('tool_call_id')}")
