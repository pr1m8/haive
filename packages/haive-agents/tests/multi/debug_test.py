#!/usr/bin/env python3

import logging
import traceback

# Set debug logging
logging.basicConfig(level=logging.DEBUG)

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


# Create engines and agents
add_aug = AugLLMConfig(tools=[add])
plan_aug = AugLLMConfig(structured_output_model=Plan, structured_output_version="v2")
simple_agent = SimpleAgent(engine=plan_aug)
react_agent = ReactAgent(engine=add_aug)

# Create sequential agent
structured_react = SequentialAgent(agents=[react_agent, simple_agent])

print("Testing SequentialAgent...")
try:
    structured_react.compile()
    result = structured_react.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then create a plan")]}
    )
    print("✅ Success!")
    print(f"Result: {result}")
except Exception as e:
    print(f"❌ Error: {e}")
    print("\n=== FULL TRACEBACK ===")
    traceback.print_exc()

    # Print exception chain
    exc = e
    print("\n=== EXCEPTION CHAIN ===")
    while exc:
        print(f"Exception: {type(exc).__name__}: {exc}")
        exc = exc.__cause__ or exc.__context__
        if exc and exc != e:
            print(f"  Caused by: {type(exc).__name__}: {exc}")
