#!/usr/bin/env python
"""Debug the msgpack serialization issue systematically."""

import json
import pickle
from typing import List

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


# Create engines
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")


# Test if engine can be dumped
try:
    dumped = add_aug.model_dump()
except Exception as e:
    pass")

# Test pickle on engine directly
try:
    pickle.dumps(add_aug)
except Exception as e:
    pass")

# Test json on dumped engine
try:
    dumped = add_aug.model_dump()
    json.dumps(dumped)
except Exception as e:

    # Find problematic fields
    for key, value in dumped.items():
        try:
            json.dumps({key: value})
        except:
            pass


# Test ReactAgent alone
react = ReactAgent(engine=add_aug)
react.compile()
try:
    result = react.run({"messages": [HumanMessage(content="Test")]})
except Exception as e:
    pass")

# Test SimpleAgent alone
simple = SimpleAgent(engine=plan_aug)
simple.compile()
try:
    result = simple.run({"messages": [HumanMessage(content="Test")]})
except Exception as e:
    pass")

multi = SequentialAgent(agents=[react, simple])
multi.compile()

# Get prepared input
prepared = multi._prepare_input({"messages": [HumanMessage(content="Test")]})

state_dict = prepared.model_dump() if hasattr(prepared, "model_dump") else prepared

if "engines" in state_dict:
    for name, engine in state_dict["engines"].items():
        pass

if "engines" in state_dict:
    for eng_name, eng_data in state_dict["engines"].items():
        if hasattr(eng_data, "model_fields"):
            pass
        elif isinstance(eng_data, dict):
            pass
        else:
            pass

# The real test - run the multi-agent
try:
    result = multi.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})
except Exception as e:
    if "msgpack" in str(e):

# Create agents without tools/schemas
simple_react = ReactAgent(name="Simple React")
simple_simple = SimpleAgent(name="Simple Simple")
simple_multi = SequentialAgent(agents=[simple_react, simple_simple])
simple_multi.compile()

try:
    result = simple_multi.run({"messages": [HumanMessage(content="Test")]})
except Exception as e:
    pass")
