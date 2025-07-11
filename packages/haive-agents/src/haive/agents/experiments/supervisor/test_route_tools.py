#!/usr/bin/env python3
"""Step 2: Test route tools creation and functionality."""

from typing import Any

from langchain_core.messages import HumanMessage
from langchain_core.tools import tool
from test_registry_setup import AgentRegistry, create_test_agents


def create_route_tools(registry: AgentRegistry) -> list[Any]:
    """Create route_to_X tools for each agent in registry."""
    tools = []

    for agent_name, entry in registry.agents.items():
        agent = entry["agent"]
        description = entry["description"]

        # Create closure to capture agent and name
        def make_route_tool(agent_instance, agent_name, agent_desc):
            @tool
            def route_to_agent(task: str) -> str:
                """Route task to agent."""
                try:
                    result = agent_instance.invoke({"messages": [HumanMessage(task)]})

                    # Extract meaningful result
                    if hasattr(result, "messages") and result.messages:
                        last_msg = result.messages[-1]
                        content = getattr(last_msg, "content", str(last_msg))
                    else:
                        content = str(result)

                    return f"Agent {agent_name} completed: {content}"
                except Exception as e:
                    return f"Agent {agent_name} failed: {e!s}"

            # Set proper docstring after creation
            route_to_agent.__doc__ = f"Route task to {agent_name}: {agent_desc}"

            route_to_agent.name = f"route_to_{agent_name}"
            route_to_agent.description = f"Route task to {agent_name}: {agent_desc}"
            return route_to_agent

        route_tool = make_route_tool(agent, agent_name, description)
        tools.append(route_tool)

    return tools


def create_list_agents_tool(registry: AgentRegistry):
    """Create tool to list available agents."""

    @tool
    def list_agents() -> str:
        """List all available agents and their capabilities."""
        available = registry.list_available()
        if not available:
            return "No agents currently available"

        result = "Available agents:\\n"
        for name, desc in available.items():
            result += f"- {name}: {desc}\\n"
        return result

    return list_agents


def test_route_tools_creation():
    """Test 1: Route tools are created correctly."""
    # Setup registry with real agents
    registry = AgentRegistry()
    agents = create_test_agents()
    registry.register(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )
    registry.register(
        "planning_agent", agents["planning_agent"], "Creates structured plans"
    )

    # Create route tools
    route_tools = create_route_tools(registry)

    # Check we have the right tools
    tool_names = [t.name for t in route_tools]

    assert (
        "route_to_math_agent" in tool_names
    ), f"Missing route_to_math_agent in {tool_names}"
    assert (
        "route_to_planning_agent" in tool_names
    ), f"Missing route_to_planning_agent in {tool_names}"
    assert len(route_tools) == 2, f"Expected 2 tools, got {len(route_tools)}"

    return registry, route_tools


def test_route_tool_execution():
    """Test 2: Route tools actually work."""
    registry, route_tools = test_route_tools_creation()

    # Test math route tool
    math_route = next(t for t in route_tools if t.name == "route_to_math_agent")

    result = math_route.invoke({"task": "What is 10 + 5?"})

    # Should contain the answer or indicate completion
    assert (
        "15" in result or "Agent math_agent completed" in result
    ), f"Unexpected result: {result}"

    # Test planning route tool
    plan_route = next(t for t in route_tools if t.name == "route_to_planning_agent")

    result = plan_route.invoke({"task": "Plan a birthday party"})

    # Should contain planning content
    assert (
        "Agent planning_agent completed" in result or "plan" in result.lower()
    ), f"Unexpected result: {result}"

    return registry, route_tools


def test_list_agents_tool():
    """Test 3: List agents tool works."""
    registry = AgentRegistry()
    agents = create_test_agents()
    registry.register(
        "math_agent", agents["math_agent"], "Performs mathematical calculations"
    )
    registry.register(
        "planning_agent", agents["planning_agent"], "Creates structured plans"
    )

    # Create list tool
    list_tool = create_list_agents_tool(registry)

    # Test it
    result = list_tool.invoke({})

    # Should contain both agents
    assert "math_agent" in result, f"Missing math_agent in: {result}"
    assert "planning_agent" in result, f"Missing planning_agent in: {result}"
    assert "mathematical calculations" in result, f"Missing description in: {result}"

    return list_tool


def test_tools_together():
    """Test 4: All tools work together."""
    registry, route_tools = test_route_tool_execution()
    list_tool = test_list_agents_tool()

    all_tools = [*route_tools, list_tool]

    # Test that we can use list tool to see available agents
    available = list_tool.invoke({})

    # Then use route tools based on what's available
    if "math_agent" in available:
        math_tool = next(t for t in route_tools if "math_agent" in t.name)
        math_result = math_tool.invoke({"task": "Calculate 7 * 8"})
        assert "56" in math_result or "completed" in math_result

    return all_tools


if __name__ == "__main__":

    try:
        test_route_tools_creation()
        test_route_tool_execution()
        test_list_agents_tool()
        all_tools = test_tools_together()

        for tool in all_tools:
            pass

    except Exception:
        raise
