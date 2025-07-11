#!/usr/bin/env python3
"""Debug tool handling in multi-agent system."""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../"))
sys.path.insert(
    0, os.path.join(os.path.dirname(__file__), "../../../../haive-core/src")
)

import logging

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Enable debug logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    logger.info(f"Tool 'add' called with a={a}, b={b}")
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Test just the ReactAgent first

add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)

react_agent.compile()

try:
    result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

    # Check messages
    for _i, msg in enumerate(result.get("messages", [])):

        # Check for tool calls
        if isinstance(msg, AIMessage) and hasattr(msg, "tool_calls"):
            pass

        # Check tool messages
        if hasattr(msg, "tool_call_id"):
            pass

except Exception:
    import traceback

    traceback.print_exc()


# Test the sequential agent

plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent2 = ReactAgent(name="Calculator", engine=add_aug)
simple_agent = SimpleAgent(name="Planner", engine=plan_aug)

seq_agent = SequentialAgent(agents=[react_agent2, simple_agent])

seq_agent.compile()

try:
    result = seq_agent.run(
        {
            "messages": [
                HumanMessage(
                    content="Calculate 10 + 20, then plan steps to build a calculator app"
                )
            ]
        }
    )

    # Show last AI message
    for msg in reversed(result.get("messages", [])):
        if isinstance(msg, AIMessage):
            break

except Exception:
    import traceback

    traceback.print_exc()
