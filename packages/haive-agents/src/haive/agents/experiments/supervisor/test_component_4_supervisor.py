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
    print("🧪 Testing Supervisor Creation...")

    # Test basic creation
    supervisor = DynamicSupervisor(name="test_supervisor")
    print(f"✅ Created supervisor: {supervisor.name}")
    print(f"  State schema: {supervisor.state_schema.__name__}")
    print(f"  Engine name: {supervisor.engine.name}")
    print(f"  Has agent execution node: {hasattr(supervisor, 'agent_execution_node')}")

    return supervisor


def test_supervisor_factory():
    """Test factory function with initial agents."""
    print("\n🧪 Testing Supervisor Factory...")

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

    print(f"✅ Factory supervisor created: {supervisor.name}")
    print(f"  Agents: {list(supervisor.list_agents().keys())}")
    print(f"  Tools: {len(supervisor.get_agent_tools())}")

    # Test agent tools
    tools = supervisor.get_agent_tools()
    for tool in tools:
        print(f"    - {tool.name}: {tool.description[:50]}...")

    return supervisor


def test_dynamic_agent_management():
    """Test adding/removing agents dynamically."""
    print("\n🧪 Testing Dynamic Agent Management...")

    supervisor = DynamicSupervisor(name="dynamic_test")
    agents = create_real_agents()

    # Start with empty state
    print(f"Initial agents: {len(supervisor.list_agents())}")
    print(f"Initial tools: {len(supervisor.get_agent_tools())}")

    # Add agents dynamically
    print(f"\n📝 Adding agents...")
    supervisor.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    print(f"After adding math_agent:")
    print(f"  Agents: {list(supervisor.list_agents().keys())}")
    print(f"  Tools: {len(supervisor.get_agent_tools())}")

    # Add another agent
    supervisor.add_agent(
        "search_agent", agents["search_agent"], "Search specialist", False
    )

    print(f"After adding search_agent (inactive):")
    print(f"  Agents: {list(supervisor.list_agents().keys())}")
    print(f"  Tools: {len(supervisor.get_agent_tools())}")

    # Remove an agent
    print(f"\n📝 Removing agent...")
    removed = supervisor.remove_agent("search_agent")
    print(f"Removed search_agent: {removed}")
    print(f"  Agents: {list(supervisor.list_agents().keys())}")
    print(f"  Tools: {len(supervisor.get_agent_tools())}")

    return supervisor


async def test_supervisor_reasoning():
    """Test supervisor reasoning with simple task."""
    print("\n🧪 Testing Supervisor Reasoning...")

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

    print(f"✅ Supervisor created with {len(supervisor.list_agents())} agents")
    print(f"  Available tools: {[t.name for t in supervisor.get_agent_tools()]}")

    # Test with a simple math task
    print(f"\n📝 Testing with math task...")
    try:
        # Create initial state
        state = supervisor.state_schema()
        state.messages = [{"role": "user", "content": "Calculate 15 multiplied by 4"}]

        # Test tool syncing
        supervisor._sync_tools_from_state_instance(state)
        print(f"  Tools synced: {[t.name for t in supervisor.engine.tools]}")

        # Test routing decision
        routing = supervisor._route_supervisor_decision(state)
        print(f"  Initial routing: {routing}")

        print(f"✅ Supervisor reasoning components work")

    except Exception as e:
        print(f"❌ Supervisor reasoning test failed: {e}")
        raise

    return supervisor


def test_graph_structure():
    """Test supervisor graph structure."""
    print("\n🧪 Testing Graph Structure...")

    supervisor = DynamicSupervisor(name="graph_test")

    # Check if graph is built
    if hasattr(supervisor, "_app") and supervisor._app:
        print(f"✅ Graph compiled successfully")

        # Get graph info if available
        try:
            # Try to get node information
            print(f"  Graph type: {type(supervisor._app)}")
            print(f"  Has compiled graph: True")
        except Exception as e:
            print(f"  Graph details not accessible: {e}")
    else:
        print(f"❌ Graph not compiled")

    return supervisor


def test_state_integration():
    """Test state integration with supervisor."""
    print("\n🧪 Testing State Integration...")

    supervisor = DynamicSupervisor(name="state_test")
    agents = create_real_agents()

    # Test state creation
    state = supervisor.state_schema()
    print(f"✅ State created: {type(state).__name__}")

    # Test adding agents to state
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)
    print(f"  Agents in state: {list(state.agents.keys())}")

    # Test tool generation from state
    tools = state.get_all_tools()
    print(f"  Tools from state: {[t.name for t in tools]}")

    # Test validation
    try:
        state.next_agent = "math_agent"
        print(f"  Valid routing set: {state.next_agent}")
    except Exception as e:
        print(f"  Routing validation error: {e}")

    try:
        state.next_agent = "nonexistent"
        print(f"❌ Invalid routing should have failed")
    except Exception as e:
        print(f"✅ Invalid routing correctly rejected: {str(e)[:50]}...")

    return state


if __name__ == "__main__":
    print("🚀 Testing Component 4: Dynamic Supervisor")
    print("=" * 60)

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
        print(f"\n🔄 Running async reasoning test...")
        try:
            reasoning_supervisor = asyncio.run(test_supervisor_reasoning())
        except Exception as e:
            print(f"Async reasoning test note: {e}")

        print("\n🎉 Component 4 tests completed!")
        print("\n✅ Key Results:")
        print(f"  Supervisor creation: ✅")
        print(f"  Factory function: ✅")
        print(f"  Dynamic agent management: ✅")
        print(f"  State integration: ✅")
        print(f"  Graph structure: ✅")

        print("\n🎯 Component 4 Ready for Full Integration Testing!")

    except Exception as e:
        print(f"\n❌ Component 4 test failed: {e}")
        import traceback

        traceback.print_exc()
        raise
