# Test SupervisorState schema

from langchain_core.messages import AIMessage, HumanMessage
import pytest

from haive.agents.supervisor.state import SupervisorState


def test_supervisor_state_initialization():
    """Test basic initialization of SupervisorState."""
    state = SupervisorState()

    # Check defaults
    assert state.agent_registry == {}
    assert state.current_agent_name is None
    assert state.current_task is None
    assert state.execution_history == []
    assert state.completed_agents == set()
    assert state.task_complete is False
    assert state.max_iterations == 10
    assert state.current_iteration == 0

    # Check computed properties
    assert state.available_agents == []
    assert state.remaining_agents == []
    assert state.is_at_max_iterations is False


def test_supervisor_state_with_registry():
    """Test SupervisorState with agent registry."""
    registry = {
        "research_agent": {
            "description": "Searches for information",
            "capabilities": ["web_search", "analysis"],
        },
        "math_agent": {
            "description": "Performs calculations",
            "capabilities": ["arithmetic", "algebra"],
        },
    }

    state = SupervisorState(agent_registry=registry)

    assert state.available_agents == ["research_agent", "math_agent"]
    assert state.remaining_agents == ["research_agent", "math_agent"]

    # Test metadata retrieval
    math_meta = state.get_agent_metadata("math_agent")
    assert math_meta["description"] == "Performs calculations"


def test_execution_tracking():
    """Test execution history tracking."""
    state = SupervisorState(
        agent_registry={
            "agent1": {"description": "Test agent 1"},
            "agent2": {"description": "Test agent 2"},
        }
    )

    # Add successful execution
    state.add_execution_record(
        agent_name="agent1",
        task="Find information about X",
        result="Found 5 relevant articles",
        success=True,
    )

    assert len(state.execution_history) == 1
    assert "agent1" in state.completed_agents
    assert state.remaining_agents == ["agent2"]

    # Add failed execution
    state.add_execution_record(
        agent_name="agent2",
        task="Calculate Y",
        result=None,
        success=False,
        error="Division by zero",
    )

    assert len(state.execution_history) == 2
    assert "agent2" not in state.completed_agents  # Failed, so not completed
    assert state.last_error == "Division by zero"


def test_message_integration():
    """Test that SupervisorState maintains MessagesState functionality."""
    state = SupervisorState()

    # Add messages
    state.add_message(HumanMessage(content="Hello"))
    state.add_message(AIMessage(content="Hi there!"))

    assert len(state.messages) == 2
    assert state.get_last_human_message().content == "Hello"
    assert state.get_last_ai_message().content == "Hi there!"


def test_iteration_limits():
    """Test iteration limit tracking."""
    state = SupervisorState(max_iterations=3)

    assert not state.is_at_max_iterations

    state.current_iteration = 2
    assert not state.is_at_max_iterations

    state.current_iteration = 3
    assert state.is_at_max_iterations


def test_reset_functionality():
    """Test resetting state for new task."""
    state = SupervisorState(
        agent_registry={"agent1": {}, "agent2": {}},
        current_agent_name="agent1",
        current_task="Some task",
        current_iteration=5,
    )

    state.add_execution_record("agent1", "task", "result")
    state.last_error = "Some error"

    # Reset
    state.reset_for_new_task()

    assert state.current_agent_name is None
    assert state.current_task is None
    assert state.execution_history == []
    assert state.completed_agents == set()
    assert state.task_complete is False
    assert state.current_iteration == 0
    assert state.last_error is None

    # Registry should remain
    assert len(state.agent_registry) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
