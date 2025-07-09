#!/usr/bin/env python
"""Test base ReactAgent without multi-agent"""

from langchain_core.messages import HumanMessage

from haive.agents.react.agent import ReactAgent

# Create a simple ReactAgent
agent = ReactAgent(name="Test React Agent")


# Add a tool to the engine
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers"""
    return a + b


# Add tool to the engine
if agent.engine:
    agent.engine.add_tool(add)

# Compile
agent.compile()

# Test
print("Testing base ReactAgent...")
try:
    result = agent.run({"messages": [HumanMessage(content="What is 5 + 3?")]})
    print("✅ Success!")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback

    traceback.print_exc()
