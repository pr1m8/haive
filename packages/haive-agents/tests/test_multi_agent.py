"""Test file for the enhanced MultiAgent implementation."""

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


def test_multi_agent_sequential():
    """Test the sequential execution of multiple agents."""
    # Configure the engines
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create individual agents
    simple_agent = SimpleAgent(engine=plan_aug)
    react_agent = ReactAgent(engine=add_aug)

    # Create multi-agent system with individual agents
    multi_agent = SequentialAgent(
        name="Planning and Calculation System", agents=[simple_agent, react_agent]
    )

    # Test invocation
    input_data = {
        "messages": [
            HumanMessage(
                content="Create a plan for a day trip, then calculate how many hours we'll need if we spend 2 hours at each location"
            )
        ]
    }

    # This will run the planner first, then the calculator
    result = multi_agent.invoke(input_data)

    # Output the result for debugging

    # Check for output schema fields
    if hasattr(result, "outputs"):
        pass
    else:
        pass

    if hasattr(result, "structured_outputs"):
        pass
    else:
        pass

    # Check that we got a result
    assert result is not None, "No result returned"


def test_multi_agent_factory():
    """Test creating a multi-agent system using factory method."""
    # This should now work with our fixes to avoid recursion
    agent_configs = [
        {
            "type": "simple",
            "name": "Planner",
            "structured_output_model": Plan,
            "structured_output_version": "v2",
        },
        {"type": "react", "name": "Calculator", "tools": [add]},
    ]

    multi_agent = MultiAgent.with_structured_agents(
        agent_configs=agent_configs, name="Planning and Calculation System"
    )

    # Verify agents were created
    assert len(multi_agent._state_instance.agents) == 2, "Not all agents were created"

    # Test invocation
    input_data = {
        "messages": [
            HumanMessage(
                content="Create a plan for a day trip, then calculate how many hours we'll need if we spend 2 hours at each location"
            )
        ]
    }

    result = multi_agent.invoke(input_data)

    # Output debugging info

    # Basic assertion
    assert result is not None, "No result returned"


def test_multi_agent_conditional():
    """Test conditional execution based on agent output."""
    # Create a multi-agent system with conditional execution
    agent_configs = [
        {
            "type": "simple",
            "name": "Planner",
            "structured_output_model": Plan,
            "structured_output_version": "v2",
        },
        {"type": "react", "name": "Calculator", "tools": [add]},
    ]

    multi_agent = MultiAgent.with_structured_agents(
        agent_configs=agent_configs,
        name="Conditional Planning System",
        coordination_strategy="conditional",
    )

    # Define a custom condition function for agent selection
    def select_next_agent(state: MultiAgentState) -> str:
        """Custom function to select the next agent based on output."""
        # Safety check for agents dictionary
        if (
            not hasattr(state, "agents")
            or not isinstance(state.agents, dict)
            or not state.agents
        ):
            return ""

        agent_ids = list(state.agents.keys())
        if not agent_ids:
            return ""

        # If no active agent, start with the first agent (typically the planner)
        if not state.active_agent_id:
            return agent_ids[0]

        # If planner just executed, select calculator as the next agent
        planner_agent_id = next(
            (aid for aid in agent_ids if "Planner" in state.agents[aid].name), None
        )
        calculator_agent_id = next(
            (aid for aid in agent_ids if "Calculator" in state.agents[aid].name), None
        )

        if state.active_agent_id == planner_agent_id and calculator_agent_id:
            return calculator_agent_id

        # Default to ending the process
        return ""

    # Set the custom selection function
    multi_agent._custom_agent_selector = select_next_agent

    # Example of registering a new coordination strategy and handler
    def zigzag_selector(agent_instance, state):
        """A zigzag selector that alternates between agents."""
        if not hasattr(state, "agents") or not state.agents:
            return state

        agent_ids = list(state.agents.keys())
        if not agent_ids:
            return state

        # If no active agent, start with first
        if not state.active_agent_id:
            state.active_agent_id = agent_ids[0]
            return state

        # Get current index
        try:
            current_idx = agent_ids.index(state.active_agent_id)
            # Go to next agent in zigzag pattern
            next_idx = (current_idx + 1) % len(agent_ids)
            state.active_agent_id = agent_ids[next_idx]
        except ValueError:
            # If agent not found, start over
            state.active_agent_id = agent_ids[0]

        return state

    # Register the new strategy (not used in this test but demonstrates extensibility)
    MultiAgent.register_agent_selector("zigzag", zigzag_selector)

    # Verify the strategy was registered
    assert "zigzag" in MultiAgent._agent_selectors, "Strategy not registered"

    # Test invocation with conditional logic
    input_data = {
        "messages": [
            HumanMessage(
                content="Create a plan for a day trip with at least 4 stops, then calculate total hours"
            )
        ]
    }

    result = multi_agent.invoke(input_data)

    # Output debugging info

    # Basic assertion
    assert result is not None, "No result returned"


def test_direct_agent_construction():
    """Test creating a multi-agent system directly with a list of agents."""
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
        name="Direct Construction System",
    )

    # Verify agents were added correctly
    for _agent_id, _agent in multi_agent._state_instance.agents.items():
        pass

    assert len(multi_agent._state_instance.agents) == 2, "Not all agents were added"

    # Get agent IDs and verify names
    agent_ids = list(multi_agent._state_instance.agents.keys())
    assert any(
        "Planner" in multi_agent._state_instance.agents[aid].name for aid in agent_ids
    ), "Planner agent not found"
    assert any(
        "Calculator" in multi_agent._state_instance.agents[aid].name
        for aid in agent_ids
    ), "Calculator agent not found"

    # Test invocation
    input_data = {
        "messages": [
            HumanMessage(
                content="First plan a day trip with at least 3 stops, then calculate the total hours"
            )
        ]
    }

    # Run the invocation
    result = multi_agent.invoke(input_data)

    # Check if agents were preserved
    if hasattr(result, "agents"):
        for _agent_id, _agent in result.agents.items():
            pass

    # Check outputs

    # Print basic result info

    # Basic assertion
    assert result is not None, "No result returned"

    # Check if agents are preserved
    if hasattr(result, "agents"):
        assert len(result.agents) > 0, "No agents in result"


def test_dynamic_agent_addition():
    """Test dynamically adding agents to an existing MultiAgent state."""
    # Configure the engines
    add_aug = AugLLMConfig(tools=[add])
    plan_aug = AugLLMConfig(
        structured_output_model=Plan, structured_output_version="v2"
    )

    # Create an empty multi-agent system first
    multi_agent = MultiAgent(name="Dynamic Agent System")

    # Create individual agents
    simple_agent = SimpleAgent(engine=plan_aug, name="Planner")
    react_agent = ReactAgent(engine=add_aug, name="Calculator")

    # Add the agents directly to the MultiAgentState instance
    multi_agent._state_instance.agents["planner_agent"] = simple_agent
    multi_agent._state_instance.agents["calculator_agent"] = react_agent

    # Set active agent
    multi_agent._state_instance.active_agent_id = "planner_agent"

    # Register the tools
    multi_agent._state_instance._register_agent_tools("planner_agent", simple_agent)
    multi_agent._state_instance._register_agent_tools("calculator_agent", react_agent)

    # Prepare input data
    input_data = {
        "messages": [
            HumanMessage(
                content="First plan a day trip, then calculate how many hours we need"
            )
        ]
    }

    # Create a new instance with the modified state
    result = multi_agent.invoke(input_data)

    # Verify that the result contains the agents

    # Check if agents were preserved in the original state
    for _agent_id, _agent in multi_agent._state_instance.agents.items():
        pass

    # Basic assertion
    assert result is not None, "No result returned"
    assert len(multi_agent._state_instance.agents) == 2, "Agents not preserved in state"


if __name__ == "__main__":
    test_multi_agent_sequential()

    try:
        test_multi_agent_factory()
    except Exception:
        pass

    try:
        test_multi_agent_conditional()
    except Exception:
        pass

    try:
        test_dynamic_agent_addition()
    except Exception:
        pass

    try:
        test_direct_agent_construction()
    except Exception:
        pass
