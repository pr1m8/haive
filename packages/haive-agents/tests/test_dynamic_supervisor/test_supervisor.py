"""Tests for dynamic supervisor agent.

This module contains comprehensive tests for the DynamicSupervisorAgent,
including state management, tool generation, and agent execution.

Test Classes:
    TestSupervisorState: Tests for state management
    TestDynamicSupervisor: Tests for supervisor functionality
    TestAgentExecution: Tests for agent execution patterns
"""

import asyncio
from typing import Dict, List

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.dynamic_supervisor import (
    AgentInfo,
    DynamicSupervisorAgent,
    SupervisorState,
    SupervisorStateWithTools,
)
from haive.agents.simple.agent import SimpleAgent


class MockAgent:
    """Mock agent for testing."""

    def __init__(self, name: str, response: str = "Mock response"):
        self.name = name
        self.response = response
        self.calls: List[str] = []

    def run(self, task: str) -> str:
        """Synchronous execution."""
        self.calls.append(task)
        return f"{self.response}: {task}"

    async def arun(self, task: str) -> str:
        """Asynchronous execution."""
        self.calls.append(task)
        return f"{self.response}: {task}"


class TestSupervisorState:
    """Test supervisor state management."""

    def test_state_initialization(self):
        """Test basic state initialization."""
        state = SupervisorState()

        assert state.agents == {}
        assert state.active_agents == []
        assert state.last_executed_agent is None
        assert state.agent_response is None
        assert state.execution_success is True

    def test_add_agent(self):
        """Test adding agents to state."""
        state = SupervisorState()
        mock_agent = MockAgent("test_agent")

        state.add_agent("test", mock_agent, "Test agent", active=True)

        assert "test" in state.agents
        assert state.agents["test"].name == "test"
        assert state.agents["test"].description == "Test agent"
        assert state.agents["test"].is_active()
        assert "test" in state.active_agents

    def test_remove_agent(self):
        """Test removing agents from state."""
        state = SupervisorState()
        mock_agent = MockAgent("test_agent")

        state.add_agent("test", mock_agent, "Test agent")
        assert state.remove_agent("test") is True
        assert "test" not in state.agents
        assert "test" not in state.active_agents

        # Removing non-existent agent
        assert state.remove_agent("nonexistent") is False

    def test_activate_deactivate_agent(self):
        """Test agent activation and deactivation."""
        state = SupervisorState()
        mock_agent = MockAgent("test_agent")

        # Add inactive agent
        state.add_agent("test", mock_agent, "Test agent", active=False)
        assert "test" not in state.active_agents
        assert not state.agents["test"].is_active()

        # Activate
        assert state.activate_agent("test") is True
        assert "test" in state.active_agents
        assert state.agents["test"].is_active()

        # Deactivate
        assert state.deactivate_agent("test") is True
        assert "test" not in state.active_agents
        assert not state.agents["test"].is_active()

    def test_unique_active_agents(self):
        """Test that active_agents list maintains uniqueness."""
        state = SupervisorState()

        # Manually add duplicates
        state.active_agents = ["agent1", "agent2", "agent1", "agent3", "agent2"]

        # Validator should remove duplicates
        validated = SupervisorState.ensure_unique_agents(state.active_agents)
        assert validated == ["agent1", "agent2", "agent3"]

    def test_agent_info_extraction(self):
        """Test AgentInfo automatic extraction."""
        # Create a mock agent with attributes
        mock_agent = MockAgent("search_agent")
        mock_agent.description = "Search specialist"

        info = AgentInfo(
            agent=mock_agent,
            name="",  # Should be extracted
            description="",  # Should be extracted
        )

        assert info.name == "search_agent"
        assert info.description == "Search specialist"

    def test_capability_matching(self):
        """Test capability matching in AgentInfo."""
        mock_agent = MockAgent("translator")

        info = AgentInfo(
            agent=mock_agent,
            name="translator",
            description="Translation specialist for multiple languages",
            capabilities=["translate", "language", "localization"],
        )

        assert info.matches_capability("translate")
        assert info.matches_capability("TRANSLATE")  # Case insensitive
        assert info.matches_capability("language")  # Exact match
        assert not info.matches_capability("translation")  # Not a substring match
        assert not info.matches_capability("search")


class TestSupervisorStateWithTools:
    """Test supervisor state with tool generation."""

    def test_tool_generation(self):
        """Test dynamic tool generation from agents."""
        state = SupervisorStateWithTools()
        mock_agent = MockAgent("search")

        state.add_agent("search", mock_agent, "Search expert")

        assert "handoff_to_search" in state.generated_tools
        assert "choose_agent" in state.generated_tools
        assert len(state.generated_tools) == 2

    def test_choice_model_sync(self):
        """Test choice model synchronization with agents."""
        state = SupervisorStateWithTools()

        # Initially only END option
        assert "END" in state.agent_choice_model.option_names
        assert len(state.agent_choice_model.option_names) == 1

        # Add agent
        mock_agent = MockAgent("math")
        state.add_agent("math", mock_agent, "Math expert")

        # Check choice model updated
        assert "math" in state.agent_choice_model.option_names
        assert "END" in state.agent_choice_model.option_names

    def test_get_all_tools(self):
        """Test getting tool instances."""
        state = SupervisorStateWithTools()
        mock_agent = MockAgent("coder")

        state.add_agent("coder", mock_agent, "Code expert")
        tools = state.get_all_tools()

        assert len(tools) == 2  # handoff_to_coder + choose_agent
        assert any(t.name == "handoff_to_coder" for t in tools)
        assert any(t.name == "choose_agent" for t in tools)


class TestDynamicSupervisor:
    """Test dynamic supervisor agent."""

    def test_supervisor_creation(self):
        """Test creating a supervisor instance."""
        engine = AugLLMConfig(
            name="test_engine",
            llm_config=AzureLLMConfig(model="gpt-4"),
            force_tool_use=True,
        )

        supervisor = DynamicSupervisorAgent(name="test_supervisor", engine=engine)

        assert supervisor.name == "test_supervisor"
        # State schema is composed dynamically, not the raw class
        assert supervisor.state_schema.__name__ == "DynamicSupervisorAgentState"
        assert supervisor.enable_agent_builder is False

    def test_create_initial_state(self):
        """Test initial state creation."""
        supervisor = DynamicSupervisorAgent(name="supervisor")
        state = supervisor.create_initial_state()

        assert isinstance(state, SupervisorStateWithTools)
        assert state.agents == {}
        assert state.active_agents == []

    @pytest.mark.asyncio
    async def test_supervisor_with_mock_agent(self):
        """Test supervisor execution with mock agent."""
        # Create supervisor
        engine = AugLLMConfig(
            name="supervisor_engine",
            llm_config=AzureLLMConfig(model="gpt-4"),
            force_tool_use=True,
            tools=[],
        )

        supervisor = DynamicSupervisorAgent(name="test_supervisor", engine=engine)

        # Create state with mock agent
        state = supervisor.create_initial_state()
        mock_agent = MockAgent("helper", "I helped with")
        state.add_agent("helper", mock_agent, "General helper")

        # Get handoff tool
        tools = state.get_all_tools()
        handoff_tool = next(t for t in tools if t.name == "handoff_to_helper")

        # Execute handoff directly
        result = handoff_tool.invoke({"task_description": "test task"})

        assert "completed" in result.lower()
        assert state.agent_response == "I helped with: test task"
        assert state.last_executed_agent == "helper"
        # Check that agent was called (tool uses sync execution)
        assert len(mock_agent.calls) == 1
        assert mock_agent.calls[0] == "test task"

    def test_execution_state(self):
        """Test execution state management."""
        state = SupervisorState()

        # Simulate execution
        state.last_executed_agent = "search_agent"
        state.agent_response = "Found information about Paris"
        state.execution_success = True

        assert state.last_executed_agent == "search_agent"
        assert state.agent_response == "Found information about Paris"

        state.clear_execution_state()

        assert state.last_executed_agent is None
        assert state.agent_response is None
        assert state.execution_success is True


class TestSerialization:
    """Test state serialization."""

    def test_state_serialization(self):
        """Test that state can be serialized properly."""
        import ormsgpack

        state = SupervisorState()
        mock_agent = MockAgent("test")
        state.add_agent("test", mock_agent, "Test agent")

        # Should serialize without error (agent excluded)
        state_dict = state.model_dump()
        serialized = ormsgpack.packb(state_dict)

        assert isinstance(serialized, bytes)
        assert len(serialized) > 0

        # Check agent is excluded
        assert "test" in state_dict["agents"]
        agent_data = state_dict["agents"]["test"]
        assert "agent" not in agent_data  # Excluded!
        assert agent_data["name"] == "test"
        assert agent_data["description"] == "Test agent"


# Integration test example
@pytest.mark.integration
class TestSupervisorIntegration:
    """Integration tests with real agents."""

    @pytest.mark.asyncio
    async def test_multi_agent_coordination(self):
        """Test coordinating multiple agents."""
        # This would use real agents in a full integration test
        pass
