#!/usr/bin/env python
"""Test individual agent serialization issue."""


from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool

from haive.agents.react.agent import ReactAgent


# Define tool
@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


# Test just ReactAgent with tools
add_aug = AugLLMConfig(tools=[add])
react_agent = ReactAgent(engine=add_aug)


# Check what's in the engine
engine = next(iter(react_agent.engines.values()))
if hasattr(engine, "tools"):
    for tool in engine.tools:
        pass

react_agent.compile()

try:
    result = react_agent.run({"messages": [HumanMessage(content="Calculate 5 + 3")]})
except Exception as e:

    if "msgpack" in str(e):
