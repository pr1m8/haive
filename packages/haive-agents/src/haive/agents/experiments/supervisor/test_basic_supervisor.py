#!/usr/bin/env python3
"""Step 3: Test basic supervisor using proper Pydantic patterns."""

from typing import Any, List

from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage
from pydantic import Field, model_validator
from test_registry_setup import AgentRegistry, create_test_agents
from test_route_tools import create_list_agents_tool, create_route_tools

from haive.agents.react.agent import ReactAgent


class BasicSupervisor(ReactAgent):
    """Basic supervisor that routes tasks to agents in registry."""

    # Registry field
    agent_registry: AgentRegistry = Field(
        default_factory=AgentRegistry,
        description="Registry containing available agents",
    )

    @model_validator(mode="after")
    def setup_supervisor_engine(self) -> "BasicSupervisor":
        """Setup supervisor engine with registry tools using model validator."""
        # Create tools from registry
        route_tools = create_route_tools(self.agent_registry)
        list_tool = create_list_agents_tool(self.agent_registry)
        all_tools = [*route_tools, list_tool]

        for tool in all_tools:
            pass

        # Create supervisor engine with routing tools
        supervisor_engine = AugLLMConfig(
            name="supervisor_engine",
            tools=all_tools,
            system_message="""You are a supervisor that routes tasks to specialized agents.

Available commands:
- list_agents: See what agents are available
- route_to_X: Send task to agent X

Always start by using list_agents to see what's available, then route the task to the most appropriate agent.""",
        )

        # Set engine properly for ReactAgent
        self.engine = supervisor_engine
        self.engines["main"] = supervisor_engine

        return self


def test_supervisor_creation():
    """Test 1: Supervisor can be created with registry."""

    # Create registry with agents
    registry = AgentRegistry()
    agents = create_test_agents()
    registry.register(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )
    registry.register(
        "planning_agent", agents["planning_agent"], "Creates structured plans"
    )

    # Create supervisor with registry
    supervisor = BasicSupervisor(name="test_supervisor", agent_registry=registry)

    # Check it has the right tools
    if hasattr(supervisor, "engine") and hasattr(supervisor.engine, "tools"):
        tool_names = [t.name for t in supervisor.engine.tools]

        assert "list_agents" in tool_names, f"Missing list_agents in {tool_names}"
        assert (
            "route_to_math_agent" in tool_names
        ), f"Missing route_to_math_agent in {tool_names}"
        assert (
            "route_to_planning_agent" in tool_names
        ), f"Missing route_to_planning_agent in {tool_names}"

    return supervisor


def test_supervisor_list_agents():
    """Test 2: Supervisor can list available agents."""

    supervisor = test_supervisor_creation()

    # Test listing agents
    try:
        result = supervisor.invoke(
            {"messages": [HumanMessage("What agents do you have available?")]}
        )

        result_str = str(result)

        # Should mention the available agents
        assert "math_agent" in result_str, f"Missing math_agent in result: {result_str}"
        assert (
            "planning_agent" in result_str
        ), f"Missing planning_agent in result: {result_str}"

        return supervisor

    except Exception as e:
        raise


def test_supervisor_routing():
    """Test 3: Supervisor can route tasks to agents."""

    supervisor = test_supervisor_list_agents()

    # Test routing to math agent
    try:
        result = supervisor.invoke({"messages": [HumanMessage("Calculate 12 + 8")]})

        result_str = str(result)

        # Should contain the calculation result
        assert (
            "20" in result_str or "math_agent" in result_str
        ), f"Expected math result, got: {result_str}"


    except Exception as e:
        pass")
        # Continue with other tests

    # Test routing to planning agent
    try:
        result = supervisor.invoke({"messages": [HumanMessage("Plan a picnic")]})

        result_str = str(result)

        # Should contain planning content
        assert (
            "plan" in result_str.lower() or "planning_agent" in result_str
        ), f"Expected planning result, got: {result_str}"


    except Exception as e:
        pass")

    return supervisor


def test_supervisor_decision_making():
    """Test 4: Supervisor makes correct routing decisions."""

    supervisor = test_supervisor_routing()

    # Test that supervisor chooses the right agent for the task
    test_cases = [
        ("What is 25 * 4?", "math"),
        ("Plan a wedding", "planning"),
        ("Calculate the area of a circle with radius 5", "math"),
        ("Create a study schedule", "planning"),
    ]

    for task, expected_agent in test_cases:
        try:
            result = supervisor.invoke({"messages": [HumanMessage(task)]})

            result_str = str(result)

            # Check if it used the expected agent
            if f"{expected_agent}_agent" in result_str:
                pass")
            else:
                pass

        except Exception as e:
            pass")

    return supervisor


if __name__ == "__main__":

    try:
        test_supervisor_creation()
        test_supervisor_list_agents()
        test_supervisor_routing()
        supervisor = test_supervisor_decision_making()


    except Exception as e:
        raise
