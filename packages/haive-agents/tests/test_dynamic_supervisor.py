"""Tests for Dynamic Supervisor Agent functionality."""

import asyncio
from unittest.mock import AsyncMock, Mock

import pytest
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent
from haive.agents.supervisor.dynamic_state import (
    AgentExecutionConfig,
    DynamicSupervisorState,
)
from haive.agents.supervisor.dynamic_supervisor import DynamicSupervisorAgent


class TestDynamicSupervisorAgent:
    """Test suite for DynamicSupervisorAgent."""

    @pytest.fixture
    def mock_engine(self):
        """Create mock LLM engine."""
        engine = AsyncMock(spec=AugLLMConfig)
        engine.ainvoke = AsyncMock(
            return_value=Mock(content='{"target": "END", "reasoning": "Test decision"}')
        )
        return engine

    @pytest.fixture
    def supervisor(self, mock_engine):
        """Create test supervisor instance."""
        return DynamicSupervisorAgent(
            name="test_supervisor",
            engine=mock_engine,
            auto_rebuild_graph=False,  # Disable for testing
        )

    @pytest.fixture
    def test_agent(self, mock_engine):
        """Create test agent instance."""
        return SimpleAgent(name="test_agent", engine=mock_engine)

    @pytest.mark.asyncio
    async def test_supervisor_initialization(self, supervisor):
        """Test supervisor initializes correctly."""
        assert supervisor.name == "test_supervisor"
        assert supervisor.auto_rebuild_graph is False
        assert supervisor.enable_parallel_execution is False
        assert supervisor.max_execution_history == 100
        assert isinstance(supervisor.agent_registry.get_available_agents(), list)
        assert len(supervisor.agent_registry.get_available_agents()) == 0

    @pytest.mark.asyncio
    async def test_agent_registration(self, supervisor, test_agent):
        """Test dynamic agent registration."""
        # Register agent
        success = await supervisor.register_agent(
            test_agent,
            capability_description="Test agent for testing",
            execution_config={
                "priority": 2,
                "execution_timeout": 60.0,
                "max_retries": 2,
            },
        )

        assert success is True
        assert supervisor.agent_registry.is_agent_registered("test_agent")
        assert "test_agent" in supervisor.agent_registry.get_available_agents()

    @pytest.mark.asyncio
    async def test_agent_unregistration(self, supervisor, test_agent):
        """Test dynamic agent unregistration."""
        # Register first
        await supervisor.register_agent(test_agent, "Test agent")
        assert supervisor.agent_registry.is_agent_registered("test_agent")

        # Unregister
        success = await supervisor.unregister_agent("test_agent")
        assert success is True
        assert not supervisor.agent_registry.is_agent_registered("test_agent")
        assert "test_agent" not in supervisor.agent_registry.get_available_agents()

    @pytest.mark.asyncio
    async def test_agent_config_update(self, supervisor, test_agent):
        """Test agent configuration updates."""
        # Register agent with initial config
        await supervisor.register_agent(
            test_agent, execution_config={"priority": 1, "execution_timeout": 120.0}
        )

        # Update config
        success = await supervisor.update_agent_config(
            "test_agent", {"priority": 3, "execution_timeout": 60.0, "max_retries": 5}
        )

        assert success is True

    @pytest.mark.asyncio
    async def test_state_schema(self):
        """Test DynamicSupervisorState functionality."""
        state = DynamicSupervisorState()

        # Test initial state
        assert len(state.messages) == 0
        assert len(state.registered_agents) == 0
        assert len(state.agent_execution_history) == 0
        assert state.active_agent_count == 0
        assert state.success_rate == 0.0

        # Test agent config management
        config = AgentExecutionConfig(
            agent_name="test_agent",
            capability_description="Test capability",
            priority=2,
        )
        state.add_agent_config("test_agent", config)

        assert state.active_agent_count == 1
        assert state.get_agent_config("test_agent") == config

        # Test agent removal
        removed = state.remove_agent_config("test_agent")
        assert removed is True
        assert state.active_agent_count == 0

    @pytest.mark.asyncio
    async def test_execution_tracking(self):
        """Test execution result tracking."""
        from haive.agents.supervisor.dynamic_state import AgentExecutionResult

        state = DynamicSupervisorState()

        # Add execution result
        result = AgentExecutionResult(
            agent_name="test_agent", success=True, duration=1.5
        )
        state.add_execution_result(result)

        assert len(state.agent_execution_history) == 1
        assert state.session_stats["total_executions"] == 1
        assert state.session_stats["successful_executions"] == 1
        assert state.success_rate == 1.0

        # Add failed execution
        failed_result = AgentExecutionResult(
            agent_name="test_agent", success=False, duration=0.5
        )
        state.add_execution_result(failed_result)

        assert len(state.agent_execution_history) == 2
        assert state.session_stats["total_executions"] == 2
        assert state.session_stats["successful_executions"] == 1
        assert state.success_rate == 0.5

    @pytest.mark.asyncio
    async def test_performance_metrics(self):
        """Test performance metric calculations."""
        from haive.agents.supervisor.dynamic_state import AgentExecutionResult

        state = DynamicSupervisorState()

        # Add agent config
        config = AgentExecutionConfig(
            agent_name="test_agent", capability_description="Test agent"
        )
        state.add_agent_config("test_agent", config)

        # Add multiple execution results
        results = [
            AgentExecutionResult(agent_name="test_agent", success=True, duration=1.0),
            AgentExecutionResult(agent_name="test_agent", success=True, duration=2.0),
            AgentExecutionResult(agent_name="test_agent", success=False, duration=0.5),
        ]

        for result in results:
            state.add_execution_result(result)

        # Test performance calculation
        performance = state.get_agent_performance("test_agent")
        assert performance["executions"] == 3
        assert performance["success_rate"] == 2 / 3
        assert performance["average_duration"] == 1.5  # (1.0 + 2.0 + 0.5) / 3
        assert performance["error_count"] == 1

    @pytest.mark.asyncio
    async def test_retry_logic(self):
        """Test agent retry logic."""
        state = DynamicSupervisorState()

        # Add agent config with retry settings
        config = AgentExecutionConfig(
            agent_name="test_agent", capability_description="Test agent", max_retries=3
        )
        state.add_agent_config("test_agent", config)

        # Test initial retry state
        assert state.should_retry_agent("test_agent") is True
        assert config.retry_count == 0

        # Increment retries
        state.increment_retry_count("test_agent")
        assert config.retry_count == 1
        assert state.should_retry_agent("test_agent") is True

        # Reach max retries
        state.increment_retry_count("test_agent")
        state.increment_retry_count("test_agent")
        assert config.retry_count == 3
        assert state.should_retry_agent("test_agent") is False

        # Reset retries
        state.reset_retry_count("test_agent")
        assert config.retry_count == 0
        assert state.should_retry_agent("test_agent") is True

    @pytest.mark.asyncio
    async def test_graph_building(self, supervisor):
        """Test supervisor graph construction."""
        # Build graph with no agents
        graph = supervisor.build_graph()
        assert graph is not None
        assert "supervisor" in graph.nodes
        assert "coordinator" in graph.nodes
        assert "adapter" in graph.nodes

    @pytest.mark.asyncio
    async def test_decision_tracking(self):
        """Test supervisor decision tracking."""
        from haive.agents.supervisor.dynamic_state import SupervisorDecision

        state = DynamicSupervisorState()

        # Add decision
        decision = SupervisorDecision(
            target_agent="test_agent",
            reasoning="Test reasoning",
            confidence=0.8,
            available_agents=["test_agent", "other_agent"],
        )
        state.add_routing_decision(decision)

        assert len(state.routing_decisions) == 1
        assert state.current_decision == decision

        # Test recent decisions
        recent = state.get_recent_decisions(5)
        assert len(recent) == 1
        assert recent[0] == decision

    @pytest.mark.asyncio
    async def test_cleanup_functionality(self):
        """Test state cleanup for memory management."""
        from haive.agents.supervisor.dynamic_state import (
            AgentExecutionResult,
            SupervisorDecision,
        )

        state = DynamicSupervisorState()

        # Add many execution results
        for i in range(150):
            result = AgentExecutionResult(
                agent_name=f"agent_{i % 3}", success=i % 2 == 0
            )
            state.add_execution_result(result)

        # Add many decisions
        for i in range(150):
            decision = SupervisorDecision(
                target_agent=f"agent_{i % 3}", reasoning=f"Decision {i}"
            )
            state.add_routing_decision(decision)

        assert len(state.agent_execution_history) == 150
        assert len(state.routing_decisions) == 150

        # Test cleanup
        state.cleanup_old_history(max_history=100)

        assert len(state.agent_execution_history) == 100
        assert len(state.routing_decisions) == 100

    @pytest.mark.asyncio
    async def test_performance_summary(self, supervisor, test_agent):
        """Test performance summary generation."""
        # Register agent
        await supervisor.register_agent(test_agent, "Test agent")

        # Get performance summary
        summary = supervisor.get_performance_summary()

        assert "session_stats" in summary
        assert "registered_agents" in summary
        assert "total_executions" in summary
        assert "success_rate" in summary
        assert "agent_performance" in summary

        assert summary["registered_agents"] == 1
        assert summary["total_executions"] == 0  # No executions yet
