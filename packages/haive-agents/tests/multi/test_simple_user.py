#!/usr/bin/env python3
"""Test the user's specific example with ReactAgent -> SimpleAgent sequential execution.
Simplified version.
"""

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


@tool
def get_earth_age() -> int:
    """Returns the age of Earth in years."""
    return 4_543_000_000  # 4.543 billion years


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create agents as per user example
add_aug = AugLLMConfig(tools=[add, get_earth_age])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

# Create sequential agent
seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

compiled = seq_agent.compile()

try:
    result = seq_agent.run(
        {
            "messages": [
                HumanMessage(
                    content="Find out the age of earth and add it to itself, then plan a website."
                )
            ]
        }
    )

    # Show the last few messages
    messages = result.get("messages", [])
    if messages:
        for msg in reversed(messages):
            if hasattr(msg, "type") and msg.type == "ai":
                break

    # Check for plan
    if "simple_agent_plan" in result:
        pass

except Exception:
    import traceback

    traceback.print_exc()
