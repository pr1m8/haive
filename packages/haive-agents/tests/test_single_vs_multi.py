#!/usr/bin/env python
"""Test single agent vs multi-agent to understand serialization issue."""

from langchain_core.messages import HumanMessage

from haive.agents.multi.base import SequentialAgent
from haive.agents.react.agent import ReactAgent

# Test 1: Single ReactAgent

react_agent = ReactAgent(name="Solo React")


# Add tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


# Get the main engine
if hasattr(react_agent, "engines") and "main" in react_agent.engines:
    main_engine = react_agent.engines["main"]
    if hasattr(main_engine, "add_tool"):
        main_engine.add_tool(add)
    else:
react_agent.compile()

try:
    # Check state
    state = react_agent.state_schema()

    # Run
    result = react_agent.run({"messages": [HumanMessage(content="What is 5 + 3?")]})
except Exception as e:
    import traceback

    traceback.print_exc()

# Test 2: Multi-agent with just one agent

multi_single = SequentialAgent(name="Multi Single", agents=[react_agent])

try:
    multi_single.compile()

    # Check state
    state = multi_single.state_schema()

    result = multi_single.run({"messages": [HumanMessage(content="What is 5 + 3?")]})
except Exception as e:
    import traceback

    traceback.print_exc()
