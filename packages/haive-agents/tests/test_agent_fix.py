"""Test file demonstrating the fixed MultiAgent implementation.

This tests that MultiAgent can properly handle serialization issues
when using SimpleAgent and ReactAgent instances.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from haive.agents.multi.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


@tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


class Plan(BaseModel):
    steps: list[str] = Field(description="list of steps")


def test_multi_agent_serialization():
    """Test that MultiAgent can handle serialization issues with agent instances."""
    # Configure the engines
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create individual agents
    simple_agent = SimpleAgent(engine=plan_aug, name="Planner")
    react_agent = ReactAgent(engine=add_aug, name="Calculator")

    # Create multi-agent directly with list of agents
    multi_agent = MultiAgent(
        agents=[simple_agent, react_agent],
        coordination_strategy="sequential",
        name="Serialization Test System",
    )

    # Verify agents were added correctly
    for _agent_id, _agent in multi_agent._state_instance.agents.items():
        pass

    # Test invocation with serialization handling
    input_data = {
        "messages": [
            HumanMessage(
                content="Create a plan for a day trip, then calculate how many hours we'll need in total"
            )
        ]
    }

    # Run the invocation - should handle serialization error
    result = multi_agent.invoke(input_data)

    # Check if agents were preserved
    if hasattr(result, "agents"):
        for _agent_id, _agent in result.agents.items():
            pass

    # Verify error handling message

    # Basic assertions
    assert result is not None, "No result returned"
    assert hasattr(result, "agents"), "Agents not preserved in result"
    assert len(result.agents) == 2, "Not all agents preserved"

    # Check for the graceful error handling message
    ai_messages = [msg for msg in result.messages if msg.type == "ai"]
    assert any(
        "serialization" in msg.content.lower() for msg in ai_messages
    ), "No serialization error message found"


if __name__ == "__main__":
    test_multi_agent_serialization()
