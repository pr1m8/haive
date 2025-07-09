#!/usr/bin/env python
"""Debug the difference in state between standalone and multi-agent"""

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
    """Returns the sum of two numbers"""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create engines and agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

print("=== Checking State Differences ===")

# 1. Check standalone ReactAgent state
print("\n1. Standalone ReactAgent:")
react_agent.compile()
if hasattr(react_agent, "state_schema"):
    print(f"   State schema: {react_agent.state_schema.__name__}")
    print(f"   State fields: {list(react_agent.state_schema.model_fields.keys())}")

    # Check engines field
    if "engines" in react_agent.state_schema.model_fields:
        field_info = react_agent.state_schema.model_fields["engines"]
        print(f"   Engines field type: {field_info.annotation}")

# 2. Check multi-agent state
print("\n2. Multi-agent:")
multi = SequentialAgent(agents=[react_agent, simple_agent])
multi.compile()

if hasattr(multi, "state_schema"):
    print(f"   State schema: {multi.state_schema.__name__}")
    print(f"   State fields: {list(multi.state_schema.model_fields.keys())}")

    # Check engines field
    if "engines" in multi.state_schema.model_fields:
        field_info = multi.state_schema.model_fields["engines"]
        print(f"   Engines field type: {field_info.annotation}")

# 3. Check what's in the prepared state
print("\n3. Prepared multi-agent state:")
prepared = multi._prepare_input({"messages": [HumanMessage(content="Test")]})
if hasattr(prepared, "engines"):
    print(f"   Engines attribute type: {type(prepared.engines)}")
    for name, engine in prepared.engines.items():
        print(f"   - {name}: {type(engine)}")
        # Check if it's a dict or object
        if isinstance(engine, dict):
            print(f"     Is dict with keys: {list(engine.keys())[:5]}...")
        else:
            print(f"     Is object with attrs: {list(dir(engine))[:5]}...")

# 4. Try to serialize the state
print("\n4. Testing state serialization:")
try:
    if hasattr(prepared, "model_dump"):
        state_dict = prepared.model_dump()
    else:
        state_dict = prepared

    # Try JSON serialization (similar to msgpack)
    json_str = json.dumps(state_dict)
    print("   ✅ State can be JSON serialized")
except Exception as e:
    print(f"   ❌ State cannot be serialized: {type(e).__name__}: {e}")

    # Find problematic field
    if isinstance(state_dict, dict):
        for key, value in state_dict.items():
            try:
                json.dumps({key: value})
            except:
                print(f"   Problem in field: {key}")
                if key == "engines" and isinstance(value, dict):
                    for eng_name, eng_data in value.items():
                        try:
                            json.dumps({eng_name: eng_data})
                        except Exception as e2:
                            print(f"     Engine '{eng_name}' not serializable: {e2}")
