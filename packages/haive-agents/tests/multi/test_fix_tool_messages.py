#!/usr/bin/env python3
"""Test fix for tool message serialization in multi-agent systems."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

from typing import Any

from langchain_core.messages import BaseMessage, HumanMessage, ToolMessage
from langchain_core.messages.utils import messages_from_dict
from pydantic import BaseModel, Field


# Fix 1: Override state model_dump to properly serialize messages
def fixed_state_model_dump(original_model_dump):
    """Wrapper for model_dump that preserves tool_call_id in messages."""

    def wrapper(self, **kwargs):
        # Get the base dump
        data = original_model_dump(**kwargs)

        # Fix messages field if present
        if "messages" in data and hasattr(self, "messages"):
            # Get the actual message objects
            messages = self.messages

            # Manually serialize messages to preserve all fields
            serialized_messages = []
            for msg in messages:
                if isinstance(msg, BaseMessage):
                    # Use the message's model_dump to get all fields
                    msg_dict = msg.model_dump()

                    # For ToolMessage, explicitly ensure tool_call_id is included
                    if isinstance(msg, ToolMessage):
                        # Double-check that tool_call_id is preserved
                        if (
                            hasattr(msg, "tool_call_id")
                            and "tool_call_id" not in msg_dict
                        ):
                            msg_dict["tool_call_id"] = msg.tool_call_id
                        if hasattr(msg, "name") and "name" not in msg_dict:
                            msg_dict["name"] = msg.name

                    serialized_messages.append(msg_dict)
                elif isinstance(msg, dict):
                    # Already serialized
                    serialized_messages.append(msg)
                else:
                    # Unknown type
                    serialized_messages.append(msg)

            data["messages"] = serialized_messages

        return data

    return wrapper


# Fix 2: Custom message deserializer that handles tool_call_id
def deserialize_messages(messages_data: list[Any]) -> list[BaseMessage]:
    """Deserialize messages ensuring tool_call_id is preserved."""
    if not messages_data:
        return []

    # Use messages_from_dict which properly handles tool_call_id
    return messages_from_dict(messages_data)


# Apply the fix to state classes
def apply_state_serialization_fix():
    """Apply the serialization fix to agent state classes."""
    from haive.agents.simple.state import SimpleAgentState

    # Wrap the model_dump methods
    SimpleAgentState.model_dump = fixed_state_model_dump(SimpleAgentState.model_dump)



# Test the fix
if __name__ == "__main__":

    # Apply the fix
    apply_state_serialization_fix()

    # Test with actual agents
    from haive.core.engine.aug_llm import AugLLMConfig
    from langchain_core.tools import tool

    from haive.agents.multi.base import SequentialAgent
    from haive.agents.react.agent import ReactAgent
    from haive.agents.simple.agent import SimpleAgent

    @tool
    def add(a: int, b: int) -> int:
        """Returns the sum of two numbers."""
        return a + b

    class Plan(BaseModel):
        steps: list[str] = Field(description="list of steps")

    # Create agents
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    react_agent = ReactAgent(engine=add_aug)
    simple_agent = SimpleAgent(engine=plan_aug)

    seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

    try:
        seq_agent.compile()
        result = seq_agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="Calculate 5 + 3, then create a plan for building a calculator app"
                    )
                ]
            }
        )


        # Check final result
        result_dict = result.model_dump() if hasattr(result, "model_dump") else result


        # Check if we have the expected messages
        messages = result_dict.get("messages", [])
        has_tool_message = any(
            msg.get("type") == "tool" for msg in messages if isinstance(msg, dict)
        )
        has_plan = any(
            "steps" in str(msg.get("content", ""))
            for msg in messages
            if isinstance(msg, dict)
        )


        if has_tool_message and has_plan:
            pass")

    except Exception as e:
        import traceback

        traceback.print_exc()
