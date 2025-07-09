"""Test Component 3: Agent execution node that mirrors tool_node pattern."""

import asyncio

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    AgentExecutionNode,
    SyncAgentExecutionNode,
    create_agent_execution_node,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


async def test_agent_execution_node_async():
    """Test async agent execution node."""
    print("\n🧪 Testing Async Agent Execution Node...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    # Add agents
    state.add_agent(
        "search_agent", agents["search_agent"], "Web search specialist", True
    )
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)
    state.add_agent(
        "planning_agent", agents["planning_agent"], "Planning specialist", False
    )  # Inactive

    # Create execution node
    execution_node = AgentExecutionNode("test_execution")
    print(f"✅ Created execution node: {execution_node}")

    # Test 1: Execute active math agent
    print(f"\n📝 Test 1: Execute math agent")
    state.set_routing("math_agent", "Calculate 15 + 25")

    print(f"Before execution:")
    print(f"  next_agent: {state.next_agent}")
    print(f"  agent_task: {state.agent_task}")

    result = await execution_node(state)

    print(f"After execution:")
    print(f"  Result keys: {list(result.keys())}")
    print(f"  agent_response: {result.get('agent_response', 'None')}")
    print(f"  execution_success: {result.get('execution_success', 'None')}")
    print(f"  next_agent cleared: {result.get('next_agent', 'Not cleared')}")

    # Test 2: Try to execute inactive agent
    print(f"\n📝 Test 2: Try inactive planning agent")
    state.set_routing("planning_agent", "Create a plan for testing")

    result2 = await execution_node(state)
    print(f"Inactive agent result: {result2.get('agent_response', 'None')}")
    print(f"Success: {result2.get('execution_success', 'None')}")

    # Test 3: Validation properly rejects nonexistent agent
    print(f"\n📝 Test 3: Validation rejects nonexistent agent")
    try:
        state.set_routing("nonexistent_agent", "Some task")
        print(f"❌ Should have failed validation but didn't")
    except ValueError as e:
        print(f"✅ Validation correctly rejected nonexistent agent: {str(e)[:100]}...")

    # Test 3b: Execution node handles None routing gracefully
    print(f"\n📝 Test 3b: Execution node handles empty routing")
    state.next_agent = None  # Valid empty routing
    state.agent_task = "Some task"

    result3 = await execution_node(state)
    print(f"Empty routing result: {result3.get('agent_response', 'None')}")
    print(f"Success: {result3.get('execution_success', 'None')}")

    # Test 4: Execute search agent
    print(f"\n📝 Test 4: Execute search agent")
    state.set_routing("search_agent", "Search for Python documentation")

    result4 = await execution_node(state)
    print(f"Search agent result type: {type(result4.get('agent_response', None))}")
    print(f"Success: {result4.get('execution_success', 'None')}")
    if result4.get("execution_error"):
        print(f"Error: {result4.get('execution_error')}")


def test_sync_agent_execution_node():
    """Test sync agent execution node."""
    print("\n🧪 Testing Sync Agent Execution Node...")

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    # Add agents
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Create sync execution node
    sync_node = SyncAgentExecutionNode("sync_test")
    print(f"✅ Created sync execution node: {sync_node}")

    # Test sync execution
    print(f"\n📝 Test: Sync math execution")
    state.set_routing("math_agent", "Add 10 and 20")

    result = sync_node(state)
    print(f"Sync result: {result.get('agent_response', 'None')}")
    print(f"Success: {result.get('execution_success', 'None')}")


def test_execution_node_factory():
    """Test factory function."""
    print("\n🧪 Testing Execution Node Factory...")

    node = create_agent_execution_node("factory_test")
    print(f"✅ Factory created node: {node}")
    print(f"✅ Node name: {node.name}")


def test_state_updates():
    """Test that execution node properly updates state."""
    print("\n🧪 Testing State Updates...")

    # Create state and execution node
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    sync_node = SyncAgentExecutionNode("state_test")

    # Set initial routing
    state.set_routing("math_agent", "Multiply 5 by 8")

    print(f"Before execution:")
    print(f"  next_agent: {state.next_agent}")
    print(f"  agent_task: {state.agent_task}")
    print(f"  agent_response: {state.agent_response}")

    # Execute
    result = sync_node(state)

    print(f"Execution result:")
    print(f"  next_agent cleared: {result.get('next_agent') is None}")
    print(f"  agent_task cleared: {result.get('agent_task') == ''}")
    print(f"  response provided: {bool(result.get('agent_response'))}")
    print(f"  last_executed_agent: {result.get('last_executed_agent')}")

    # Apply result to state (simulate what graph would do)
    for key, value in result.items():
        if hasattr(state, key):
            setattr(state, key, value)

    print(f"After applying result to state:")
    print(f"  state.next_agent: {state.next_agent}")
    print(f"  state.agent_task: {state.agent_task}")
    print(f"  state.agent_response: {state.agent_response}")


if __name__ == "__main__":
    print("🚀 Testing Component 3: Agent Execution Node")
    print("=" * 60)

    try:
        # Test sync first
        test_sync_agent_execution_node()
        test_execution_node_factory()
        test_state_updates()

        # Test async
        asyncio.run(test_agent_execution_node_async())

        print("\n🎉 Component 3 tests completed successfully!")

    except Exception as e:
        print(f"\n❌ Component 3 test failed: {e}")
        import traceback

        traceback.print_exc()
        raise
