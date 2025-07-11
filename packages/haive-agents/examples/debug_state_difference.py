#!/usr/bin/env python
"""Debug the difference in state between standalone and multi-agent."""

import json

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


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


# 1. Check standalone ReactAgent state
react_agent.compile()
if hasattr(react_agent, "state_schema"):

    # Check engines field
    if "engines" in react_agent.state_schema.model_fields:
        field_info = react_agent.state_schema.model_fields["engines"]

# 2. Check multi-agent state
multi = SequentialAgent(agents=[react_agent, simple_agent])
multi.compile()

if hasattr(multi, "state_schema"):

    # Check engines field
    if "engines" in multi.state_schema.model_fields:
        field_info = multi.state_schema.model_fields["engines"]

# 3. Check what's in the prepared state
prepared = multi._prepare_input({"messages": [HumanMessage(content="Test")]})
if hasattr(prepared, "engines"):
    for _name, engine in prepared.engines.items():
        # Check if it's a dict or object
        if isinstance(engine, dict):
            pass
        else:
            pass

# 4. Try to serialize the state
try:
    state_dict = prepared.model_dump() if hasattr(prepared, "model_dump") else prepared

    # Try JSON serialization (similar to msgpack)
    json_str = json.dumps(state_dict)
except Exception:

    # Find problematic field
    if isinstance(state_dict, dict):
        for key, value in state_dict.items():
            try:
                json.dumps({key: value})
            except:
                if key == "engines" and isinstance(value, dict):
                    for eng_name, eng_data in value.items():
                        try:
                            json.dumps({eng_name: eng_data})
                        except Exception:
                            pass
