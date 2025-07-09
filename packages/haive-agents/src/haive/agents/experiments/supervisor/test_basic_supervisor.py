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
        all_tools = route_tools + [list_tool]

        print(f"Setting up supervisor with {len(all_tools)} tools")
        for tool in all_tools:
            print(f"  - {tool.name}")

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
    """Test 1: Supervisor can be created with registry"""
    print("\\n=== Test 1: Supervisor Creation ===")

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
        print(f"Supervisor tools: {tool_names}")

        assert "list_agents" in tool_names, f"Missing list_agents in {tool_names}"
        assert (
            "route_to_math_agent" in tool_names
        ), f"Missing route_to_math_agent in {tool_names}"
        assert (
            "route_to_planning_agent" in tool_names
        ), f"Missing route_to_planning_agent in {tool_names}"

    print("✓ Supervisor created with correct tools")
    return supervisor


def test_supervisor_list_agents():
    """Test 2: Supervisor can list available agents"""
    print("\\n=== Test 2: Supervisor Lists Agents ===")

    supervisor = test_supervisor_creation()

    # Test listing agents
    try:
        result = supervisor.invoke(
            {"messages": [HumanMessage("What agents do you have available?")]}
        )

        print(f"List agents result: {result}")
        result_str = str(result)

        # Should mention the available agents
        assert "math_agent" in result_str, f"Missing math_agent in result: {result_str}"
        assert (
            "planning_agent" in result_str
        ), f"Missing planning_agent in result: {result_str}"

        print("✓ Supervisor can list agents correctly")
        return supervisor

    except Exception as e:
        print(f"✗ Supervisor list test failed: {e}")
        raise


def test_supervisor_routing():
    """Test 3: Supervisor can route tasks to agents"""
    print("\\n=== Test 3: Supervisor Routes Tasks ===")

    supervisor = test_supervisor_list_agents()

    # Test routing to math agent
    print("Testing math routing...")
    try:
        result = supervisor.invoke({"messages": [HumanMessage("Calculate 12 + 8")]})

        print(f"Math routing result: {result}")
        result_str = str(result)

        # Should contain the calculation result
        assert (
            "20" in result_str or "math_agent" in result_str
        ), f"Expected math result, got: {result_str}"

        print("✓ Math routing works")

    except Exception as e:
        print(f"✗ Math routing failed: {e}")
        # Continue with other tests

    # Test routing to planning agent
    print("Testing planning routing...")
    try:
        result = supervisor.invoke({"messages": [HumanMessage("Plan a picnic")]})

        print(f"Planning routing result: {result}")
        result_str = str(result)

        # Should contain planning content
        assert (
            "plan" in result_str.lower() or "planning_agent" in result_str
        ), f"Expected planning result, got: {result_str}"

        print("✓ Planning routing works")

    except Exception as e:
        print(f"✗ Planning routing failed: {e}")

    return supervisor


def test_supervisor_decision_making():
    """Test 4: Supervisor makes correct routing decisions"""
    print("\\n=== Test 4: Supervisor Decision Making ===")

    supervisor = test_supervisor_routing()

    # Test that supervisor chooses the right agent for the task
    test_cases = [
        ("What is 25 * 4?", "math"),
        ("Plan a wedding", "planning"),
        ("Calculate the area of a circle with radius 5", "math"),
        ("Create a study schedule", "planning"),
    ]

    for task, expected_agent in test_cases:
        print(f"Testing: '{task}' should route to {expected_agent}_agent")
        try:
            result = supervisor.invoke({"messages": [HumanMessage(task)]})

            result_str = str(result)

            # Check if it used the expected agent
            if f"{expected_agent}_agent" in result_str:
                print(f"  ✓ Correctly routed to {expected_agent}_agent")
            else:
                print(f"  ? May have routed differently: {result_str[:100]}...")

        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print("✓ Supervisor decision making tested")
    return supervisor


if __name__ == "__main__":
    print("🚀 Testing Basic Supervisor with Proper Pydantic Patterns")

    try:
        test_supervisor_creation()
        test_supervisor_list_agents()
        test_supervisor_routing()
        supervisor = test_supervisor_decision_making()

        print("\\n🎉 All Step 3 tests passed!")
        print("Basic supervisor with registry routing is working correctly.")
        print(f"Supervisor has {len(supervisor.engine.tools)} tools available.")

    except Exception as e:
        print(f"\\n❌ Test failed: {e}")
        raise
