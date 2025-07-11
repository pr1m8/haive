#!/usr/bin/env python3
"""Test fix for message serialization."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, Field


# Create a fixed MessageList that properly serializes messages
class FixedMessageList(BaseModel):
    """MessageList that properly serializes tool messages."""

    messages: list[BaseMessage] = Field(default_factory=list)

    def model_dump(self, **kwargs) -> Any:
        """Override to properly serialize messages including tool_call_id."""
        # Get the base dump
        data = super().model_dump(**kwargs)

        # Manually serialize messages to preserve all fields
        if "messages" in data and isinstance(data["messages"], list):
            serialized_messages = []
            for msg in data["messages"]:
                if isinstance(msg, dict):
                    # Already serialized
                    serialized_messages.append(msg)
                elif isinstance(msg, BaseMessage):
                    # Need to serialize - use the message's own model_dump
                    msg_dict = msg.model_dump()

                    # For ToolMessage, ensure tool_call_id is preserved
                    if isinstance(msg, ToolMessage) and hasattr(msg, "tool_call_id"):
                        msg_dict["tool_call_id"] = msg.tool_call_id

                    serialized_messages.append(msg_dict)
                else:
                    # Unknown type, just add it
                    serialized_messages.append(msg)

            data["messages"] = serialized_messages

        return data


# Test the fix

# Create state with messages including ToolMessage
state = FixedMessageList(
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


# Serialize with our fixed method
state_dict = state.model_dump()


# Check the tool message
for i, msg in enumerate(state_dict["messages"]):
    if msg.get("type") == "tool":


# Test 2: Apply fix to actual agent state

from haive.agents.react.state import ReactAgentState

# Import the actual state schemas
from haive.agents.simple.state import SimpleAgentState


# Monkey patch the model_dump method
def fixed_model_dump(self, **kwargs):
    """Fixed model_dump that preserves tool_call_id."""
    data = BaseModel.model_dump(self, **kwargs)

    # Fix messages field if present
    if "messages" in data:
        if hasattr(self, "messages") and hasattr(self.messages, "root"):
            # It's a MessageList with root
            messages = self.messages.root
        elif isinstance(data["messages"], list):
            messages = data["messages"]
        else:
            messages = []

        serialized_messages = []
        for msg in messages:
            if isinstance(msg, BaseMessage):
                msg_dict = msg.model_dump()
                # Preserve tool_call_id for ToolMessage
                if isinstance(msg, ToolMessage) and hasattr(msg, "tool_call_id"):
                    msg_dict["tool_call_id"] = msg.tool_call_id
                serialized_messages.append(msg_dict)
            elif isinstance(msg, dict):
                serialized_messages.append(msg)
            else:
                serialized_messages.append(msg)

        data["messages"] = serialized_messages

    return data


# Apply the fix
SimpleAgentState.model_dump = fixed_model_dump
ReactAgentState.model_dump = fixed_model_dump


from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.tools import tool

from haive.agents.multi.base import SequentialAgent

# Now test with the actual agents
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create and test sequential agent
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

try:
    seq_agent.compile()
    result = seq_agent.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then plan a calculator")]}
    )

    # Check final result
    result_dict = result.model_dump() if hasattr(result, "model_dump") else result


except Exception as e:
    import traceback

    traceback.print_exc()
