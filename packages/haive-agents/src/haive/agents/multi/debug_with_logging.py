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
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


try:
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    react_agent = ReactAgent(engine=add_aug)
    simple_agent = SimpleAgent(engine=plan_aug)

    structured_react = SequentialAgent(agents=[react_agent, simple_agent])

    structured_react.compile()

    result = structured_react.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3, then create a plan")]}
    )


except Exception as e:

    traceback.print_exc()

    current_exc = e
    level = 0
    while current_exc:
        current_exc = getattr(current_exc, "__cause__", None) or getattr(
            current_exc, "__context__", None
        )
        level += 1
        if level > 5:  # Prevent infinite loops
            break
