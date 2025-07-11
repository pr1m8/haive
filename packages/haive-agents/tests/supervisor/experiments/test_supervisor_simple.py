"""Simple supervisor test with 3 executor agents - 2 active, 1 in registry."""

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.experiments.supervisor import BaseSupervisor
from haive.agents.simple.agent import SimpleAgent


def test_supervisor_with_three_executors():
    """Test supervisor with 3 executor agents: 2 active, 1 in registry."""
    # Create supervisor
    supervisor_config = AugLLMConfig()
    supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_config)

    # Create 3 executor agents
    planner_config = AugLLMConfig()
    executor_config = AugLLMConfig()
    calculator_config = AugLLMConfig()

    planner_agent = SimpleAgent(name="planner", engine=planner_config)
    executor_agent = SimpleAgent(name="executor", engine=executor_config)
    calculator_agent = SimpleAgent(name="calculator", engine=calculator_config)

    # Register all 3 agents
    supervisor.register_agent(
        name="planner",
        description="Plans tasks and breaks them down",
        agent=planner_agent,
    )

    supervisor.register_agent(
        name="executor", description="Executes planned tasks", agent=executor_agent
    )

    supervisor.register_agent(
        name="calculator", description="Performs calculations", agent=calculator_agent
    )

    # Verify all 3 are registered
    state = supervisor.get_state()
    assert len(state.agents) == 3
    assert "planner" in state.agents
    assert "executor" in state.agents
    assert "calculator" in state.agents

    # Verify tools were created for all agents
    assert "handoff_to_planner" in state.tool_mappings
    assert "handoff_to_executor" in state.tool_mappings
    assert "handoff_to_calculator" in state.tool_mappings

    # Test agent retrieval works
    retrieved_planner = state.get_agent_by_name("planner")
    retrieved_executor = state.get_agent_by_name("executor")
    retrieved_calculator = state.get_agent_by_name("calculator")

    assert retrieved_planner is not None
    assert retrieved_executor is not None
    assert retrieved_calculator is not None

    # Test different agent types preserved
    assert retrieved_planner.name == "planner"
    assert retrieved_executor.name == "executor"
    assert retrieved_calculator.name == "calculator"


def test_supervisor_status_reporting():
    """Test supervisor can report status of all agents."""
    supervisor = BaseSupervisor(name="status_supervisor", engine=AugLLMConfig())

    # Add agents
    for i in range(3):
        agent = SimpleAgent(name=f"agent_{i}", engine=AugLLMConfig())
        supervisor.register_agent(
            name=f"agent_{i}",
            description=f"Executor agent number {i}",
            agent=agent,
            capabilities=[f"task_type_{i}"],
        )

    # Test individual status
    status = supervisor.get_agent_status("agent_1")
    assert status["name"] == "agent_1"
    assert status["metadata"]["description"] == "Executor agent number 1"
    assert status["metadata"]["capabilities"] == ["task_type_1"]

    # Test all agents status
    all_status = supervisor.get_agent_status()
    assert all_status["total_agents"] == 3
    assert len(all_status["agents"]) == 3


def test_supervisor_tool_execution_simulation():
    """Test that supervisor tools can be executed."""
    supervisor = BaseSupervisor(name="exec_supervisor", engine=AugLLMConfig())

    # Register agents
    planner = SimpleAgent(name="planner", engine=AugLLMConfig())
    executor = SimpleAgent(name="executor", engine=AugLLMConfig())

    supervisor.register_agent("planner", "Task planning", planner)
    supervisor.register_agent("executor", "Task execution", executor)

    # Get the tools
    from haive.agents.experiments.supervisor.tools import create_list_agents_tool

    list_tool = create_list_agents_tool(lambda: supervisor.get_state())

    # Execute list tool
    result = list_tool.invoke({})

    assert "Available agents:" in result
    assert "planner: Task planning" in result
    assert "executor: Task execution" in result


def test_supervisor_state_synchronization():
    """Test that state synchronization validators work."""
    supervisor = BaseSupervisor(name="sync_supervisor", engine=AugLLMConfig())

    # Add agent
    agent = SimpleAgent(name="test_agent", engine=AugLLMConfig())
    supervisor.register_agent("test_agent", "Test agent", agent)

    state = supervisor.get_state()

    # Should have created tool mapping automatically
    assert "handoff_to_test_agent" in state.tool_mappings
    assert state.tool_mappings["handoff_to_test_agent"].agent_name == "test_agent"
    assert state.tool_mappings["handoff_to_test_agent"].category == "handoff"

    # Remove agent
    supervisor.unregister_agent("test_agent")

    # Tool mapping should be cleaned up
    updated_state = supervisor.get_state()
    assert "handoff_to_test_agent" not in updated_state.tool_mappings
    assert len(updated_state.agents) == 0


if __name__ == "__main__":
    test_supervisor_with_three_executors()
    test_supervisor_status_reporting()
    test_supervisor_tool_execution_simulation()
    test_supervisor_state_synchronization()
