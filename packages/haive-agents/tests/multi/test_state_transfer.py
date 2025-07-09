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
    """Returns the sum of two numbers"""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


# Create agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")

react_agent = ReactAgent(engine=add_aug)
simple_agent = SimpleAgent(engine=plan_aug)

# First, test ReactAgent alone
print("=" * 80)
print("TEST 1: ReactAgent Alone")
print("=" * 80)

react_agent.compile()
react_result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})

# Convert result
if hasattr(react_result, "model_dump"):
    react_dict = react_result.model_dump()
else:
    react_dict = react_result

print(f"\nReactAgent output type: {type(react_result)}")
print(f"ReactAgent output keys: {list(react_dict.keys())}")
print(f"Number of messages: {len(react_dict.get('messages', []))}")

# Check messages in detail
messages = react_dict.get("messages", [])
for i, msg in enumerate(messages):
    print(f"\nMessage {i}:")
    print(f"  Type in list: {type(msg)}")

    if isinstance(msg, dict):
        print(f"  Dict keys: {list(msg.keys())}")
        print(f"  'type' field: {msg.get('type', 'MISSING')}")
        if msg.get("type") == "tool":
            print("  Tool message fields:")
            print(f"    - content: {msg.get('content')}")
            print(f"    - tool_call_id: {msg.get('tool_call_id', 'MISSING')}")
            print(f"    - id: {msg.get('id', 'MISSING')}")
            print(f"    - name: {msg.get('name', 'MISSING')}")
    else:
        print(f"  Not a dict, it's: {msg}")

# Now test what SimpleAgent expects
print("\n" + "=" * 80)
print("TEST 2: SimpleAgent Input Requirements")
print("=" * 80)

simple_agent.compile()

# Try to run SimpleAgent with the exact output from ReactAgent
print("\nTrying to run SimpleAgent with ReactAgent's output...")
try:
    # The SequentialAgent would pass the entire state from ReactAgent to SimpleAgent
    simple_result = simple_agent.run(react_dict)
    print("✅ SimpleAgent accepted ReactAgent's output!")
except Exception as e:
    print(f"❌ SimpleAgent failed with: {e}")

    # Try with just messages
    print("\nTrying with just messages field...")
    try:
        simple_result = simple_agent.run({"messages": react_dict.get("messages", [])})
        print("✅ SimpleAgent accepted messages!")
    except Exception as e2:
        print(f"❌ Still failed: {e2}")

# Now test the actual SequentialAgent
print("\n" + "=" * 80)
print("TEST 3: SequentialAgent State Transfer")
print("=" * 80)

# Create a new sequential agent to test
seq_agent = SequentialAgent(agents=[react_agent, simple_agent])

# Add some debug logging to see state transfer
import logging

logging.basicConfig(
    level=logging.DEBUG, format="%(name)s - %(levelname)s - %(message)s"
)

print("\nCompiling SequentialAgent...")
seq_agent.compile()

print("\nRunning SequentialAgent...")
try:
    result = seq_agent.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then plan a calculator")]}
    )
    print("✅ Success!")
except Exception as e:
    print(f"❌ Failed: {e}")
    import traceback

    traceback.print_exc()
