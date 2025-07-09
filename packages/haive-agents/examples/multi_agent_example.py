"""Example of using the MultiAgent with structured output and tools.

This example demonstrates how to create a multi-agent system with:
1. A simple agent with Plan structured output
2. A react agent with an add tool
"""

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from pydantic import BaseModel, Field

from haive.agents.multi.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Define the Plan model
class Plan(BaseModel):
    """A planning model for structured output."""

    steps: list[str] = Field(description="list of steps")


# Define the add tool
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


def create_multi_agent_system():
    """Create a multi-agent system with a planner and calculator."""
    # Create the MultiAgent
    multi_agent = MultiAgent(name="Planning and Calculation System")

    # Create the plan_aug config for structured output
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create the add_aug config for tools
    add_aug = AugLLMConfig(tools=[add])

    # Create the simple agent with plan_aug
    simple_agent = SimpleAgent(name="Planner", engine=plan_aug)

    # Create the react agent with add_aug
    react_agent = ReactAgent(name="Calculator", engine=add_aug)

    # Add agents to multi-agent
    multi_agent.add_agent(simple_agent)
    multi_agent.add_agent(react_agent)

    return multi_agent


def create_multi_agent_with_factory():
    """Create a multi-agent system using the factory method."""
    # Create agent configs
    agent_configs = [
        {
            "type": "simple",
            "name": "Planner",
            "structured_output_model": Plan,
            "structured_output_version": "v2",
        },
        {"type": "react", "name": "Calculator", "tools": [add]},
    ]

    # Create multi-agent using factory method
    multi_agent = MultiAgent.with_structured_agents(
        agent_configs=agent_configs, name="Planning and Calculation System"
    )

    return multi_agent


def run_example():
    """Run the multi-agent example."""
    # Create the multi-agent system
    multi_agent = create_multi_agent_with_factory()

    # Create input with a human message
    input_data = {
        "messages": [
            HumanMessage(
                content="Create a plan for a day trip, then calculate how many hours we'll need if we spend 2 hours at each location"
            )
        ]
    }

    # Invoke the multi-agent
    print(f"Invoking multi-agent: {multi_agent.name}")
    result = multi_agent.invoke(input_data)

    # Print the result
    print("\nMulti-agent result:")

    # Print messages
    if "messages" in result:
        print("\nMessages:")
        for i, msg in enumerate(result["messages"]):
            print(f"  {i+1}. {msg.type}: {msg.content[:100]}...")

    # Print structured outputs
    if "structured_outputs" in result:
        print("\nStructured outputs:")
        for agent_id, output in result["structured_outputs"].items():
            agent_name = multi_agent._state_instance.agents[agent_id].name
            print(f"  {agent_name}:")
            print(f"  {output}")

    # Print agent outputs
    print("\nAgent outputs:")
    for agent_id, output in result.get("outputs", {}).items():
        agent_name = multi_agent._state_instance.agents[agent_id].name
        print(f"  {agent_name}:")
        print(f"  {output}")


if __name__ == "__main__":
    run_example()
