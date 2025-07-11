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

# Create a ToolMessage with all required fields
tool_msg = ToolMessage(content="Result: 8", tool_call_id="call_123", name="add")


# Try different serialization methods
try:
    msg_dict = dict(tool_msg)
except Exception as e:
    pass

try:
    msg_dict = tool_msg.model_dump()
except Exception as e:
    pass

try:
    msg_dict = tool_msg.__dict__
except Exception as e:
    pass


# Test 2: Messages in a Pydantic model


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


# Serialize the state
state_dict = state.model_dump()


# Check the tool message
for i, msg in enumerate(state_dict["messages"]):
    if msg.get("type") == "tool":


# Test 3: Recreating messages from dict

# Try to recreate messages from the serialized dict
try:
    new_messages = messages_from_dict(state_dict["messages"])

    # Check the tool message
    for i, msg in enumerate(new_messages):
        if isinstance(msg, ToolMessage):

except Exception as e:
    import traceback

    traceback.print_exc()


# Test 4: Custom serialization fix


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

for i, msg in enumerate(custom_serialized):
    if msg.get("type") == "tool":
