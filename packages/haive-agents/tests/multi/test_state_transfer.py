#!/usr/bin/env python3
"""Test state transfer between agents in SequentialAgent."""

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
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

# First, test ReactAgent alone

react_agent.compile()
react_result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

# Convert result
react_dict = react_result.model_dump() if hasattr(react_result, "model_dump") else react_result


# Check messages in detail
messages = react_dict.get("messages", [])
for i, msg in enumerate(messages):

    if isinstance(msg, dict):
        if msg.get("type") == "tool":
    else:
        pass

# Now test what SimpleAgent expects

simple_agent.compile()

# Try to run SimpleAgent with the exact output from ReactAgent
try:
    # The SequentialAgent would pass the entire state from ReactAgent to SimpleAgent
    simple_result = simple_agent.run(react_dict)
except Exception as e:

    # Try with just messages
    try:
        simple_result = simple_agent.run({"messages": react_dict.get("messages", [])})
    except Exception as e2:
        pass")

# Now test the actual SequentialAgent

# Create a new sequential agent to test
seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

# Add some debug logging to see state transfer
import logging


logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)

seq_agent.compile()

try:
    result = seq_agent.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then plan a calculator")]}
    )
except Exception as e:
    import traceback

    traceback.print_exc()
