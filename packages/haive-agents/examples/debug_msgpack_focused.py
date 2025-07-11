#!/usr/bin/env python
"""Focused debugging of msgpack serialization issue."""

# Suppress verbose logging
import logging
import traceback
from typing import List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

logging.getLogger("haive").setLevel(logging.WARNING)


# Define tools/schemas
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")



# Create engines and agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

# Create multi-agent
multi = SequentialAgent(agents=[react_agent, simple_agent])


multi.compile()

prepared = multi._prepare_input({"messages": [HumanMessage(content="Test")]})
if hasattr(prepared, "engines"):
    for name, engine in prepared.engines.items():
        pass
elif isinstance(prepared, dict) and "engines" in prepared:
    for name, engine in prepared["engines"].items():
        pass

try:
    # Capture the full traceback
    result = multi.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})
except Exception as e:
    traceback.print_exc()

    # Check if it's checkpointing related
    if "msgpack" in str(e):

        # Try to isolate what's causing the issue
        if hasattr(multi, "state_schema") and multi.state_schema:
            try:
                # Create a state instance
                test_state = multi.state_schema(messages=[HumanMessage(content="Test")])
                # Check if engines field exists
                if hasattr(test_state, "engines"):
            except Exception as e2:
                pass

# Try to disable checkpointing
try:
    # Create a new multi-agent without checkpointing
    multi_no_checkpoint = SequentialAgent(
        agents=[react_agent, simple_agent],
        # Try to disable checkpointing if possible
    )
    multi_no_checkpoint.compile()

    # Check if we can access the compiled app
    if hasattr(multi_no_checkpoint, "_app"):
        app = multi_no_checkpoint._app
        if hasattr(app, "checkpointer"):
            pass
        if hasattr(app, "config"):
            pass
except Exception as e:
    pass
