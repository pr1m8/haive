"""Test case for the Multi-Agent implementation using the example from the user's request.

This module tests a specific example where we have:
1. A simple agent with Plan structured output
2. A react agent with add tool
"""

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import BaseModel, Field

from haive.agents.multi.agent import MultiAgent
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# The Plan model as per user request
class Plan(BaseModel):
    """A planning model for structured output."""

    steps: list[str] = Field(description="list of steps")


# The add tool as per user request
def add(a: int, b: int) -> int:
    """Returns the sum of two numbers."""
    return a + b


def test_user_example():
    """Test the specific example from the user's request."""
    # Create the MultiAgent
    multi_agent = MultiAgent(name="Test User Example")

    # Create the plan_aug config
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create the add_aug config
    add_aug = AugLLMConfig(tools=[add])

    # Create the simple agent with plan_aug
    simple_agent = SimpleAgent(name="Planner", engine=plan_aug)

    # Create the react agent with add_aug
    react_agent = ReactAgent(name="Calculator", engine=add_aug)

    # Add agents to multi-agent
    simple_id = multi_agent.add_agent(simple_agent)
    react_id = multi_agent.add_agent(react_agent)

    # Verify agents were added
    assert simple_id in multi_agent._state_instance.agents
    assert react_id in multi_agent._state_instance.agents

    # Verify agent engines have the correct configuration
    planner = multi_agent._state_instance.agents[simple_id]
    calculator = multi_agent._state_instance.agents[react_id]

    # Check planner configuration
    assert hasattr(planner, "engine")
    assert hasattr(planner.engine, "structured_output_model")
    assert planner.engine.structured_output_model == Plan
    assert planner.engine.structured_output_version == "v2"

    # Check calculator configuration
    assert hasattr(calculator, "engine")
    assert hasattr(calculator.engine, "tools")
    assert len(calculator.engine.tools) == 1

    # Verify tool registration
    assert "Plan" in multi_agent._state_instance.tool_routes
    assert multi_agent._state_instance.tool_routes["Plan"] == simple_id

    assert "add" in multi_agent._state_instance.tool_routes
    assert multi_agent._state_instance.tool_routes["add"] == react_id


def test_user_example_factory():
    """Test the factory method with the user's example configuration."""
    # Create agent configs using the user's example
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
        agent_configs=agent_configs, name="Test Factory User Example"
    )

    # Verify agents were created
    assert len(multi_agent._state_instance.agents) == 2

    # Find the agents
    planner_id = None
    calculator_id = None

    for agent_id, agent in multi_agent._state_instance.agents.items():
        if agent.name == "Planner":
            planner_id = agent_id
        elif agent.name == "Calculator":
            calculator_id = agent_id

    assert planner_id is not None
    assert calculator_id is not None

    # Get the agents
    planner = multi_agent._state_instance.agents[planner_id]
    calculator = multi_agent._state_instance.agents[calculator_id]

    # Check planner configuration
    assert hasattr(planner, "structured_output_model")
    assert planner.structured_output_model == Plan
    assert hasattr(planner.engine, "structured_output_model")
    assert planner.engine.structured_output_model == Plan
    assert planner.engine.structured_output_version == "v2"

    # Check calculator configuration
    assert hasattr(calculator.engine, "tools")
    assert len(calculator.engine.tools) == 1
    assert calculator.engine.tools[0] == add

    # Verify tool registration
    assert "Plan" in multi_agent._state_instance.tool_routes
    assert multi_agent._state_instance.tool_routes["Plan"] == planner_id

    assert "add" in multi_agent._state_instance.tool_routes
    assert multi_agent._state_instance.tool_routes["add"] == calculator_id
