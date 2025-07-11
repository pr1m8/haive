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

    # Test 1: Execute active math agent
    state.set_routing("math_agent", "Calculate 15 + 25")


    result = await execution_node(state)


    # Test 2: Try to execute inactive agent
    state.set_routing("planning_agent", "Create a plan for testing")

    result2 = await execution_node(state)

    # Test 3: Validation properly rejects nonexistent agent
    try:
        state.set_routing("nonexistent_agent", "Some task")
    except ValueError as e:
        pass")

    # Test 3b: Execution node handles None routing gracefully
    state.next_agent = None  # Valid empty routing
    state.agent_task = "Some task"

    result3 = await execution_node(state)

    # Test 4: Execute search agent
    state.set_routing("search_agent", "Search for Python documentation")

    result4 = await execution_node(state)
    if result4.get("execution_error"):
        pass


def test_sync_agent_execution_node():
    """Test sync agent execution node."""

    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    # Add agents
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Create sync execution node
    sync_node = SyncAgentExecutionNode("sync_test")

    # Test sync execution
    state.set_routing("math_agent", "Add 10 and 20")

    result = sync_node(state)


def test_execution_node_factory():
    """Test factory function."""

    node = create_agent_execution_node("factory_test")


def test_state_updates():
    """Test that execution node properly updates state."""

    # Create state and execution node
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    sync_node = SyncAgentExecutionNode("state_test")

    # Set initial routing
    state.set_routing("math_agent", "Multiply 5 by 8")


    # Execute
    result = sync_node(state)


    # Apply result to state (simulate what graph would do)
    for key, value in result.items():
        if hasattr(state, key):
            setattr(state, key, value)



if __name__ == "__main__":

    try:
        # Test sync first
        test_sync_agent_execution_node()
        test_execution_node_factory()
        test_state_updates()

        # Test async
        asyncio.run(test_agent_execution_node_async())


    except Exception as e:
        import traceback

        traceback.print_exc()
        raise
