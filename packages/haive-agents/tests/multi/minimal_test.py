#!/usr/bin/env python3


from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage, ToolMessage
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



# Test ReactAgent alone
try:
    add_aug = AugLLMConfig(tools=[add])
    react_agent = ReactAgent(engine=add_aug)
    react_agent.compile()
    react_result = react_agent.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3")]}
    )
    if hasattr(react_result, "messages"):
        for i, msg in enumerate(react_result.messages):
            if isinstance(msg, ToolMessage):
                pass
except Exception as e:
    pass")

# Test SimpleAgent alone
try:
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    simple_agent = SimpleAgent(engine=plan_aug)
    simple_agent.compile()
    simple_result = simple_agent.run(
        {"messages": [HumanMessage(content="Create a plan")]}
    )
except Exception as e:
    pass")


# Test multi-agent
try:
    # Create fresh agents for multi-agent test
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
    import traceback

    traceback.print_exc()
