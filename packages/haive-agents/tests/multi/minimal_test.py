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
    """Returns the sum of two numbers"""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


print("=== TESTING INDIVIDUAL AGENTS FIRST ===")

# Test ReactAgent alone
print("\n1. Testing ReactAgent alone...")
try:
    add_aug = AugLLMConfig(tools=[add])
    react_agent = ReactAgent(engine=add_aug)
    react_agent.compile()
    react_result = react_agent.run(
        {"messages": [HumanMessage(content="Calculate 5 + 3")]}
    )
    print(f"✅ ReactAgent alone works. Result type: {type(react_result)}")
    if hasattr(react_result, "messages"):
        print(f"   Messages: {len(react_result.messages)} messages")
        for i, msg in enumerate(react_result.messages):
            print(f"     {i}: {type(msg).__name__}")
            if isinstance(msg, ToolMessage):
                print(f"        tool_call_id: {getattr(msg, 'tool_call_id', 'None')}")
except Exception as e:
    print(f"❌ ReactAgent alone failed: {e}")

# Test SimpleAgent alone
print("\n2. Testing SimpleAgent alone...")
try:
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )
    simple_agent = SimpleAgent(engine=plan_aug)
    simple_agent.compile()
    simple_result = simple_agent.run(
        {"messages": [HumanMessage(content="Create a plan")]}
    )
    print(f"✅ SimpleAgent alone works. Result type: {type(simple_result)}")
except Exception as e:
    print(f"❌ SimpleAgent alone failed: {e}")

print("\n=== TESTING MULTI-AGENT ===")

# Test multi-agent
print("\n3. Testing SequentialAgent...")
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
    print(f"✅ SequentialAgent works! Result type: {type(result)}")
    print(f"   Result: {result}")
except Exception as e:
    print(f"❌ SequentialAgent failed: {e}")
    import traceback

    print("=== TRACEBACK ===")
    traceback.print_exc()
