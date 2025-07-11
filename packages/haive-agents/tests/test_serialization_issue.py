#!/usr/bin/env python
"""Test to isolate the msgpack serialization issue."""

from langchain_core.messages import HumanMessage

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent

# Create agents with tools already configured
react_agent = ReactAgent(name="React Agent")
simple_agent = SimpleAgent(
    name="Simple Agent", structured_output_model=None  # No Plan schema for now
)


multi = SequentialAgent(name="Test Sequential", agents=[react_agent, simple_agent])

try:
    multi.compile()

    # Check what's in the initial state
    initial_state = multi._prepare_input({"messages": [HumanMessage(content="Test")]})

    if hasattr(initial_state, "model_dump"):
        state_dict = initial_state.model_dump()
    else:
        state_dict = initial_state


    if "engines" in state_dict:
        engines = state_dict["engines"]
        for name, engine in engines.items():
            pass

    # Try to run
    result = multi.run({"messages": [HumanMessage(content="Hello")]})

except Exception as e:

    # Check if it's the msgpack error
    if "msgpack" in str(e):
