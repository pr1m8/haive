#!/usr/bin/env python3

import logging
import sys
import traceback

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(name)s:%(lineno)d] %(levelname)s: %(message)s",
    stream=sys.stdout,
)

# Enable specific loggers we care about
logging.getLogger("haive.agents.base.mixins.execution_mixin").setLevel(logging.DEBUG)
logging.getLogger("haive.core.graph.node.agent_node").setLevel(logging.DEBUG)
logging.getLogger("haive.agents.multi.base").setLevel(logging.DEBUG)


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


print("=== DETAILED DEBUG WITH EXTENSIVE LOGGING ===")

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

    print("4. Running ReactAgent -> SimpleAgent test...")
    print("   This should trigger the tool_call_id error...")

    result = structured_react.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then create a plan")]}
    )

    print("✅ SUCCESS! Multi-agent completed without error")
    print(f"Result: {result}")

except Exception as e:
    print(f"\n❌ ERROR CAUGHT: {e}")
    print(f"Error type: {type(e).__name__}")

    print("\n=== FULL TRACEBACK ===")
    traceback.print_exc()

    print("\n=== ANALYZING ERROR CHAIN ===")
    current_exc = e
    level = 0
    while current_exc:
        print(f"Level {level}: {type(current_exc).__name__}: {current_exc}")
        current_exc = getattr(current_exc, "__cause__", None) or getattr(
            current_exc, "__context__", None
        )
        level += 1
        if level > 5:  # Prevent infinite loops
            break
