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
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")



# Just test the simplest possible case
try:
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    react_agent = ReactAgent(engine=add_aug)
    simple_agent = SimpleAgent(engine=plan_aug)

    structured_react = SequentialAgent(agents=[react_agent, simple_agent])

    structured_react.compile()

    result = structured_react.run({"messages": [HumanMessage(content="Hello")]})


    from langchain_core.messages import ToolMessage

    # Try with a ToolMessage to see if that's the issue
    tool_msg = ToolMessage(content="8", name="add", tool_call_id="test_call_123")

    result2 = structured_react.run(
        {"messages": [HumanMessage(content="Hello"), tool_msg]}
    )


except Exception as e:

    # Get just the last few frames of the traceback
    tb = traceback.extract_tb(e.__traceback__)
    for frame in tb[-3:]:  # Just show last 3 frames
