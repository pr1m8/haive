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
    """Returns the sum of two numbers."""
    return a + b


# Create a simple ReactAgent
add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)

# Compile the agent
react_agent.compile()

# Test with a simple addition
try:
    result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})


    # Check the messages in the result
    if hasattr(result, "messages"):
        messages = result.messages

        for i, msg in enumerate(messages):
            if isinstance(msg, ToolMessage):

except Exception as e:
    import traceback

    traceback.print_exc()
