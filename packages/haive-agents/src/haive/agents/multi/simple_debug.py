#!/usr/bin/env python3

import logging
import traceback

# Minimal logging to see the key issues
logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")


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


print("=== SIMPLE DEBUG TEST ===")

# Just test the simplest possible case
try:
    print("1. Creating agents...")
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    react_agent = ReactAgent(engine=add_aug)
    simple_agent = SimpleAgent(engine=plan_aug)

    print("2. Creating multi-agent...")
    structured_react = SequentialAgent(agents=[react_agent, simple_agent])

    print("3. Compiling...")
    structured_react.compile()

    print("4. Running with simple message...")
    result = structured_react.run({"messages": [HumanMessage(content="Hello")]})

    print("✅ SUCCESS! Multi-agent works with simple message")
    print(f"Result type: {type(result)}")

    print("\n5. Testing with tool call message...")
    from langchain_core.messages import ToolMessage

    # Try with a ToolMessage to see if that's the issue
    print("  Creating ToolMessage with tool_call_id...")
    tool_msg = ToolMessage(content="8", name="add", tool_call_id="test_call_123")
    print(f"  ToolMessage created: {tool_msg}")
    print(f"  ToolMessage tool_call_id: {tool_msg.tool_call_id}")

    result2 = structured_react.run(
        {"messages": [HumanMessage(content="Hello"), tool_msg]}
    )

    print("✅ SUCCESS! Multi-agent also works with ToolMessage")
    print(f"Result type: {type(result2)}")

except Exception as e:
    print(f"❌ FAILED: {e}")
    print("\n=== SIMPLE TRACEBACK ===")

    # Get just the last few frames of the traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Key error locations:")
    for frame in tb[-3:]:  # Just show last 3 frames
        print(f"  File: {frame.filename.split('/')[-1]}:{frame.lineno}")
        print(f"  Function: {frame.name}")
        print(f"  Code: {frame.line}")
        print()
