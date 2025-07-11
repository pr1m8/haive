"""Test Component 4: Dynamic Supervisor with ReactAgent integration."""

import asyncio

from haive.agents.experiments.supervisor.component_4_dynamic_supervisor import (
    DynamicSupervisor,
    create_dynamic_supervisor,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def test_supervisor_creation():
    """Test basic supervisor creation and setup."""

    # Test basic creation
    supervisor = DynamicSupervisor(name="test_supervisor")

    return supervisor


def test_supervisor_factory():
    """Test factory function with initial agents."""

    # Create real agents
    agents = create_real_agents()

    # Setup initial agents config
    initial_agents = {
        "search_agent": {
            "agent": agents["search_agent"],
            "description": "Web search and research specialist",
            "active": True,
        },
        "math_agent": {
            "agent": agents["math_agent"],
            "description": "Mathematical calculations specialist",
            "active": True,
        },
    }

    # Create supervisor with initial agents
    supervisor = create_dynamic_supervisor(
        name="factory_supervisor", initial_agents=initial_agents
    )


    # Test agent tools
    tools = supervisor.get_agent_tools()
    for tool in tools:
        pass

    return supervisor


def test_dynamic_agent_management():
    """Test adding/removing agents dynamically."""

    supervisor = DynamicSupervisor(name="dynamic_test")
    agents = create_real_agents()

    # Start with empty state

    # Add agents dynamically
    supervisor.add_agent("math_agent", agents["math_agent"], "Math specialist", True)


    # Add another agent
    supervisor.add_agent(
        "search_agent", agents["search_agent"], "Search specialist", False
    )


    # Remove an agent
    removed = supervisor.remove_agent("search_agent")

    return supervisor


async def test_supervisor_reasoning():
    """Test supervisor reasoning with simple task."""

    # Create supervisor with agents
    agents = create_real_agents()
    initial_agents = {
        "math_agent": {
            "agent": agents["math_agent"],
            "description": "Mathematical calculations specialist",
            "active": True,
        }
    }

    supervisor = create_dynamic_supervisor(
        name="reasoning_supervisor", initial_agents=initial_agents
    )


    # Test with a simple math task
    try:
        # Create initial state
        state = supervisor.state_schema()
        state.messages = [{"role": "user", "content": "Calculate 15 multiplied by 4"}]

        # Test tool syncing
        supervisor._sync_tools_from_state_instance(state)

        # Test routing decision
        routing = supervisor._route_supervisor_decision(state)


    except Exception as e:
        raise

    return supervisor


def test_graph_structure():
    """Test supervisor graph structure."""

    supervisor = DynamicSupervisor(name="graph_test")

    # Check if graph is built
    if hasattr(supervisor, "_app") and supervisor._app:

        # Get graph info if available
        try:
            # Try to get node information
        except Exception as e:
            pass
    else:
        pass")

    return supervisor


def test_state_integration():
    """Test state integration with supervisor."""

    supervisor = DynamicSupervisor(name="state_test")
    agents = create_real_agents()

    # Test state creation
    state = supervisor.state_schema()

    # Test adding agents to state
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Test tool generation from state
    tools = state.get_all_tools()

    # Test validation
    try:
        state.next_agent = "math_agent"
    except Exception as e:
        pass

    try:
        state.next_agent = "nonexistent"
    except Exception as e:
        pass")

    return state


if __name__ == "__main__":

    try:
        # Test basic functionality
        supervisor1 = test_supervisor_creation()
        supervisor2 = test_supervisor_factory()
        supervisor3 = test_dynamic_agent_management()

        # Test state integration
        state = test_state_integration()

        # Test graph structure
        supervisor4 = test_graph_structure()

        # Test reasoning (async)
        try:
            reasoning_supervisor = asyncio.run(test_supervisor_reasoning())
        except Exception as e:
            pass



    except Exception as e:
        import traceback

        traceback.print_exc()
        raise
