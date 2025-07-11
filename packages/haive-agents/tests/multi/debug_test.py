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
    """Returns the sum of two numbers."""
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

try:
    structured_react.compile()
    result = structured_react.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then create a plan")]}
    )
except Exception as e:
    traceback.print_exc()

    # Print exception chain
    exc = e
    while exc:
        exc = exc.__cause__ or exc.__context__
        if exc and exc != e:
            pass
