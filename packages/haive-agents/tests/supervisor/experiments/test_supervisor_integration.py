"""Integration tests for supervisor system.

These tests verify the complete supervisor functionality without mocks,
testing actual agent registration, tool synchronization, and execution.
"""

import pickle
from datetime import datetime
from typing import Any, Dict, List

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.experiments.supervisor import (
    AgentMetadata,
    BaseSupervisor,
    DynamicSupervisor,
    DynamicSupervisorState,
    SerializedAgent,
    SupervisorState,
)
from haive.agents.react.agent import ReactAgent
from haive.agents.simple.agent import SimpleAgent


# Test fixtures for real engines
@pytest.fixture
def test_llm_config():
    """Create a test LLM config."""
    return AugLLMConfig(model="gpt-3.5-turbo", temperature=0.3, max_tokens=100)


@pytest.fixture
def supervisor_engine(test_llm_config):
    """Create supervisor engine."""
    return test_llm_config


@pytest.fixture
def agent_engine(test_llm_config):
    """Create agent engine."""
    config = test_llm_config.copy()
    config.system_message = "You are a helpful assistant."
    return config


@pytest.fixture
def research_agent(agent_engine):
    """Create a research agent for testing."""
    return SimpleAgent(name="research_agent", engine=agent_engine)


@pytest.fixture
def coding_agent(agent_engine):
    """Create a coding agent for testing."""
    return ReactAgent(name="coding_agent", engine=agent_engine)


class TestSupervisorStateModels:
    """Test state models and serialization."""

    def test_agent_metadata_creation(self):
        """Test AgentMetadata creation and validation."""
        metadata = AgentMetadata(
            name="test_agent",
            description="Test agent for validation",
            capabilities=["research", "analysis"],
            tags=["test", "research"],
        )

        assert metadata.name == "test_agent"
        assert metadata.description == "Test agent for validation"
        assert metadata.capabilities == ["research", "analysis"]
        assert metadata.tags == ["test", "research"]
        assert metadata.usage_count == 0
        assert metadata.performance_score == 1.0
        assert isinstance(metadata.created_at, datetime)

    def test_serialized_agent_creation(self, research_agent):
        """Test agent serialization and deserialization."""
        metadata = AgentMetadata(
            name="research_agent", description="Research specialist"
        )

        # Create serialized agent
        serialized = SerializedAgent.from_agent(research_agent, metadata)

        assert serialized.metadata.name == "research_agent"
        assert "SimpleAgent" in serialized.agent_class
        assert serialized.agent_module is not None
        assert len(serialized.serialized_data) > 0

        # Test deserialization
        deserialized_agent = serialized.get_agent()
        assert deserialized_agent.name == research_agent.name
        assert type(deserialized_agent) == type(research_agent)

    def test_supervisor_state_initialization(self):
        """Test SupervisorState initialization and defaults."""
        state = SupervisorState()

        assert len(state.messages) == 0
        assert len(state.agents) == 0
        assert len(state.tools) == 0
        assert len(state.tool_mappings) == 0
        assert state.auto_sync_tools == True
        assert state.max_history_size == 100
        assert isinstance(state.execution_context.total_steps, int)

    def test_state_agent_registration(self, research_agent):
        """Test agent registration in state."""
        state = SupervisorState()
        metadata = AgentMetadata(
            name="research_agent", description="Research specialist"
        )

        # Register agent
        state.register_agent(research_agent, metadata)

        assert "research_agent" in state.agents
        assert state.agents["research_agent"].metadata.name == "research_agent"

        # Test retrieval
        retrieved_agent = state.get_agent_by_name("research_agent")
        assert retrieved_agent is not None
        assert retrieved_agent.name == research_agent.name

    def test_state_usage_tracking(self, research_agent):
        """Test agent usage tracking."""
        state = SupervisorState()
        metadata = AgentMetadata(name="test_agent", description="Test")
        state.register_agent(research_agent, metadata)

        # Initially no usage
        assert state.agents["test_agent"].metadata.usage_count == 0
        assert state.agents["test_agent"].metadata.last_used is None

        # Update usage
        state.update_agent_usage("test_agent")

        assert state.agents["test_agent"].metadata.usage_count == 1
        assert state.agents["test_agent"].metadata.last_used is not None

    def test_state_execution_history(self):
        """Test execution history management."""
        state = SupervisorState()

        # Add execution records
        record1 = {"agent": "test1", "task": "task1", "success": True}
        record2 = {"agent": "test2", "task": "task2", "success": False}

        state.add_execution_record(record1)
        state.add_execution_record(record2)

        assert len(state.execution_history) == 2
        assert "timestamp" in state.execution_history[0]
        assert state.execution_history[0]["agent"] == "test1"
        assert state.execution_history[1]["success"] == False


class TestSupervisorTools:
    """Test supervisor tool creation and execution."""

    def test_list_agents_tool_creation(self):
        """Test list_agents tool creation and execution."""
        from haive.agents.experiments.supervisor.tools import create_list_agents_tool

        # Create state with agents
        state = SupervisorState()
        state.register_agent(
            SimpleAgent(name="agent1", engine=None),
            AgentMetadata(name="agent1", description="First agent"),
        )
        state.register_agent(
            SimpleAgent(name="agent2", engine=None),
            AgentMetadata(name="agent2", description="Second agent"),
        )

        # Create tool
        tool = create_list_agents_tool(lambda: state)

        # Test tool execution
        result = tool.invoke({})

        assert "Available agents:" in result
        assert "agent1: First agent" in result
        assert "agent2: Second agent" in result

    def test_execution_status_tool(self):
        """Test execution status tool."""
        from haive.agents.experiments.supervisor.tools import (
            create_execution_status_tool,
        )

        state = SupervisorState()
        state.execution_context.current_agent = "test_agent"
        state.execution_context.current_task = "test task"
        state.execution_context.total_steps = 5

        tool = create_execution_status_tool(lambda: state)
        result = tool.invoke({})

        assert "Currently executing: test_agent" in result
        assert "Current task: test task" in result
        assert "Total steps: 5" in result


class TestBaseSupervisor:
    """Test BaseSupervisor functionality."""

    def test_supervisor_initialization(self, supervisor_engine):
        """Test supervisor initialization."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        assert supervisor.name == "test_supervisor"
        assert supervisor.main_engine == supervisor_engine
        assert isinstance(supervisor.get_state(), SupervisorState)

    def test_agent_registration_and_tool_sync(self, supervisor_engine, research_agent):
        """Test agent registration triggers tool synchronization."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        # Initially no agents
        initial_state = supervisor.get_state()
        assert len(initial_state.agents) == 0

        # Register agent
        supervisor.register_agent(
            name="research_agent",
            description="Research specialist",
            agent=research_agent,
            capabilities=["research", "web_search"],
        )

        # Check state updated
        updated_state = supervisor.get_state()
        assert len(updated_state.agents) == 1
        assert "research_agent" in updated_state.agents

        # Check metadata
        metadata = updated_state.agents["research_agent"].metadata
        assert metadata.name == "research_agent"
        assert metadata.description == "Research specialist"
        assert metadata.capabilities == ["research", "web_search"]

    def test_multiple_agent_registration(
        self, supervisor_engine, research_agent, coding_agent
    ):
        """Test registering multiple agents."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        # Register multiple agents
        supervisor.register_agent("research", "Research specialist", research_agent)
        supervisor.register_agent("coding", "Code generation", coding_agent)

        # Check both registered
        state = supervisor.get_state()
        assert len(state.agents) == 2
        assert "research" in state.agents
        assert "coding" in state.agents

        # Check different agent types preserved
        research_restored = state.get_agent_by_name("research")
        coding_restored = state.get_agent_by_name("coding")

        assert isinstance(research_restored, SimpleAgent)
        assert isinstance(coding_restored, ReactAgent)

    def test_agent_unregistration(self, supervisor_engine, research_agent):
        """Test agent removal."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        # Register then unregister
        supervisor.register_agent("test_agent", "Test", research_agent)
        assert len(supervisor.get_state().agents) == 1

        success = supervisor.unregister_agent("test_agent")
        assert success == True
        assert len(supervisor.get_state().agents) == 0

        # Try removing non-existent agent
        success = supervisor.unregister_agent("nonexistent")
        assert success == False

    def test_agent_status_retrieval(self, supervisor_engine, research_agent):
        """Test getting agent status information."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        supervisor.register_agent("test_agent", "Test agent", research_agent)

        # Get specific agent status
        status = supervisor.get_agent_status("test_agent")
        assert status["name"] == "test_agent"
        assert "metadata" in status
        assert "class" in status

        # Get all agents status
        all_status = supervisor.get_agent_status()
        assert "total_agents" in all_status
        assert all_status["total_agents"] == 1
        assert "agents" in all_status

    def test_execution_history_tracking(self, supervisor_engine):
        """Test execution history functionality."""
        supervisor = BaseSupervisor(name="test_supervisor", engine=supervisor_engine)

        # Initially empty
        history = supervisor.get_execution_history()
        assert len(history) == 0

        # Add some records manually to state
        state = supervisor.get_state()
        state.add_execution_record({"agent": "test", "task": "task1"})
        state.add_execution_record({"agent": "test", "task": "task2"})
        supervisor.update_state(state)

        # Check history
        history = supervisor.get_execution_history()
        assert len(history) == 2

        # Clear history
        supervisor.clear_history()
        history = supervisor.get_execution_history()
        assert len(history) == 0


class TestDynamicSupervisor:
    """Test DynamicSupervisor with agent creation capabilities."""

    def test_dynamic_supervisor_initialization(self, supervisor_engine):
        """Test DynamicSupervisor initialization."""
        supervisor = DynamicSupervisor(
            name="dynamic_supervisor", engine=supervisor_engine
        )

        assert isinstance(supervisor.get_state(), DynamicSupervisorState)
        state = supervisor.get_state()
        assert state.can_create_agents == True
        assert state.max_agents == 10

    def test_agent_template_management(self, supervisor_engine):
        """Test agent template functionality."""
        supervisor = DynamicSupervisor(
            name="dynamic_supervisor", engine=supervisor_engine
        )

        # Add template
        template = {
            "agent_type": "simple",
            "system_message": "You are a helpful assistant",
            "tools": [],
        }
        supervisor.add_agent_template("helper_template", template)

        # Check template added
        state = supervisor.get_state()
        assert "helper_template" in state.agent_templates
        assert state.agent_templates["helper_template"] == template

    def test_agent_limit_management(self, supervisor_engine):
        """Test agent limit functionality."""
        supervisor = DynamicSupervisor(
            name="dynamic_supervisor", engine=supervisor_engine
        )

        # Change limit
        supervisor.set_agent_limit(5)
        state = supervisor.get_state()
        assert state.max_agents == 5

    def test_creation_enable_disable(self, supervisor_engine):
        """Test enabling/disabling agent creation."""
        supervisor = DynamicSupervisor(
            name="dynamic_supervisor", engine=supervisor_engine
        )

        # Disable creation
        supervisor.enable_agent_creation(False)
        state = supervisor.get_state()
        assert state.can_create_agents == False

        # Re-enable
        supervisor.enable_agent_creation(True)
        state = supervisor.get_state()
        assert state.can_create_agents == True


class TestStateValidators:
    """Test state model validators work correctly."""

    def test_tool_sync_validator_triggers(self):
        """Test that adding agents triggers tool sync validator."""
        state = SupervisorState()

        # Initially no tools or mappings
        assert len(state.tool_mappings) == 0

        # Add agent - should trigger validator
        agent = SimpleAgent(name="test", engine=None)
        metadata = AgentMetadata(name="test", description="Test agent")
        state.register_agent(agent, metadata)

        # Validator should have created tool mapping
        expected_tool_name = "handoff_to_test"
        assert expected_tool_name in state.tool_mappings
        assert state.tool_mappings[expected_tool_name].agent_name == "test"
        assert state.tool_mappings[expected_tool_name].category == "handoff"

    def test_history_size_validator(self):
        """Test execution history size limiting."""
        state = SupervisorState()
        state.max_history_size = 3

        # Add more records than limit
        for i in range(5):
            state.add_execution_record({"step": i})

        # Should only keep last 3
        assert len(state.execution_history) == 3
        assert state.execution_history[0]["step"] == 2  # Steps 2, 3, 4 kept
        assert state.execution_history[-1]["step"] == 4

    def test_dynamic_agent_limit_validator(self, research_agent):
        """Test dynamic supervisor agent limit enforcement."""
        state = DynamicSupervisorState()
        state.max_agents = 2

        # Add agents up to limit
        for i in range(3):
            agent = SimpleAgent(name=f"agent_{i}", engine=None)
            metadata = AgentMetadata(name=f"agent_{i}", description=f"Agent {i}")
            state.register_agent(agent, metadata)

        # Should only keep 2 agents (most recent)
        assert len(state.agents) == 2


class TestIntegrationScenarios:
    """End-to-end integration tests."""

    def test_complete_supervisor_workflow(
        self, supervisor_engine, research_agent, coding_agent
    ):
        """Test complete supervisor workflow from registration to status."""
        # Create supervisor
        supervisor = BaseSupervisor(
            name="integration_supervisor", engine=supervisor_engine
        )

        # Register multiple agents
        supervisor.register_agent(
            "research",
            "Research and information gathering",
            research_agent,
            capabilities=["web_search", "analysis"],
            tags=["research", "data"],
        )

        supervisor.register_agent(
            "coding",
            "Code generation and debugging",
            coding_agent,
            capabilities=["python", "debugging"],
            tags=["code", "development"],
        )

        # Verify registration
        state = supervisor.get_state()
        assert len(state.agents) == 2

        # Check agent retrieval works
        research_restored = state.get_agent_by_name("research")
        coding_restored = state.get_agent_by_name("coding")

        assert research_restored is not None
        assert coding_restored is not None
        assert research_restored.name == research_agent.name
        assert coding_restored.name == coding_agent.name

        # Check status reporting
        all_status = supervisor.get_agent_status()
        assert all_status["total_agents"] == 2
        assert "research" in all_status["agents"]
        assert "coding" in all_status["agents"]

        # Test individual status
        research_status = supervisor.get_agent_status("research")
        assert research_status["name"] == "research"
        assert research_status["metadata"]["capabilities"] == ["web_search", "analysis"]

    def test_dynamic_supervisor_full_workflow(self, supervisor_engine):
        """Test dynamic supervisor with templates and limits."""
        supervisor = DynamicSupervisor(
            name="dynamic_integration", engine=supervisor_engine
        )

        # Configure supervisor
        supervisor.set_agent_limit(3)
        supervisor.add_agent_template(
            "research_template",
            {
                "agent_type": "simple",
                "system_message": "You are a research assistant",
                "capabilities": ["research", "analysis"],
            },
        )

        # Verify configuration
        state = supervisor.get_state()
        assert state.max_agents == 3
        assert "research_template" in state.agent_templates

        # Test enabling/disabling creation
        supervisor.enable_agent_creation(False)
        assert not supervisor.get_state().can_create_agents

        supervisor.enable_agent_creation(True)
        assert supervisor.get_state().can_create_agents


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
