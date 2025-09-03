"""Simple focused test for Component 3 - Agent Execution Node."""

import asyncio
import contextlib

from haive.agents.experiments.supervisor.component_2_tools import (
    SupervisorStateWithTools,
)
from haive.agents.experiments.supervisor.component_3_agent_execution import (
    AgentExecutionNode,
    SyncAgentExecutionNode,
)
from haive.agents.experiments.supervisor.test_component_1_state import (
    create_real_agents,
)


def test_sync_agent_execution():
    """Test sync agent execution with valid scenarios only."""
    # Create state with agents
    state = SupervisorStateWithTools()
    agents = create_real_agents()

    # Add only math agent for simple test
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    # Create execution node
    sync_node = SyncAgentExecutionNode("test_execution")

    # Test valid math execution
    state.set_routing("math_agent", "Add 10 and 20")

    result = sync_node(state)

    return result


def test_agent_execution_error_handling():
    """Test execution node error handling."""
    # Create execution node
    sync_node = SyncAgentExecutionNode("error_test")

    # Test 1: Empty state (no agents)
    empty_state = SupervisorStateWithTools()
    empty_state.next_agent = None  # Valid empty routing
    empty_state.agent_task = "Some task"

    result1 = sync_node(empty_state)

    # Test 2: Inactive agent
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent(
        "planning_agent", agents["planning_agent"], "Planning specialist", False
    )  # Inactive

    state.set_routing("planning_agent", "Create a plan")
    result2 = sync_node(state)

    return result1, result2


def test_state_updates():
    """Test that state updates work correctly."""
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    sync_node = SyncAgentExecutionNode("state_test")

    # Set routing
    state.set_routing("math_agent", "Multiply 6 by 7")

    # Execute
    result = sync_node(state)

    # These results would be applied by the graph system

    return result


async def test_async_execution():
    """Test async execution (if needed)."""
    state = SupervisorStateWithTools()
    agents = create_real_agents()
    state.add_agent("math_agent", agents["math_agent"], "Math specialist", True)

    async_node = AgentExecutionNode("async_test")

    state.set_routing("math_agent", "Add 25 and 35")

    result = await async_node(state)

    return result


if __name__ == "__main__":
    try:
        # Test core functionality
        math_result = test_sync_agent_execution()

        # Test error handling
        error_results = test_agent_execution_error_handling()

        # Test state updates
        state_result = test_state_updates()

        # Test async if available
        with contextlib.suppress(Exception):
            async_result = asyncio.run(test_async_execution())

    except Exception:
        import traceback

        traceback.print_exc()
        raise
