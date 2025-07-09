"""Test the refactored Agent class with proper config composition."""

import pytest
from haive.core.engine.agent.config import AgentConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig
from langgraph.graph import END, StateGraph

from haive.agents.base import Agent


class TestAgent(Agent):
    """Simple test agent implementation."""

    def setup_agent(self):
        """Setup hook."""
        pass

    def build_graph(self) -> BaseGraph:
        """Build a simple test graph."""
        from haive.core.graph.state_graph.state_graph import (
            StateGraph as HaiveStateGraph,
        )

        graph = HaiveStateGraph(state_schema={"messages": list})

        def dummy_node(state):
            return state

        graph.add_node("test", dummy_node)
        graph.add_edge("test", END)
        graph.set_entry_point("test")

        return graph


def test_agent_with_default_config():
    """Test that agent creates default AgentConfig when none provided."""
    agent = TestAgent(name="test_agent")

    # Should have created a default config
    assert agent.config is not None
    assert isinstance(agent.config, AgentConfig)

    # Should have PostgreSQL persistence by default (if available)
    assert agent.config.persistence is not None
    if hasattr(agent.config.persistence, "type"):
        assert agent.config.persistence.type.value in ["postgres", "memory"]

    # Should have recursion limit of 100
    assert agent.config.runnable_config["configurable"]["recursion_limit"] == 100

    # Agent should use config's runnable_config
    assert agent.runnable_config == agent.config.runnable_config

    # Should have checkpointer set up
    assert agent.checkpointer is not None


def test_agent_with_custom_config():
    """Test that agent uses provided AgentConfig."""
    custom_config = AgentConfig(
        runnable_config={
            "configurable": {"thread_id": "custom-thread", "recursion_limit": 50}
        },
        checkpoint_mode="async",
    )

    agent = TestAgent(name="test_agent", config=custom_config)

    # Should use the provided config
    assert agent.config is custom_config

    # Should use config's runnable_config
    assert agent.runnable_config == custom_config.runnable_config
    assert agent.runnable_config["configurable"]["recursion_limit"] == 50

    # Should have checkpointer set up
    assert agent.checkpointer is not None

    # Should have correct checkpoint mode
    assert agent._checkpoint_mode == "async"


def test_agent_with_supabase_config():
    """Test that agent can use Supabase persistence through config."""
    supabase_config = AgentConfig(
        persistence=SupabaseCheckpointerConfig(
            user_id="test-user", setup_needed=False  # Skip schema setup for test
        ),
        runnable_config={"configurable": {"recursion_limit": 75}},
    )

    agent = TestAgent(name="test_agent", config=supabase_config)

    # Should use Supabase persistence
    assert agent.config.persistence.type.value == "supabase"

    # Should still have correct recursion limit
    assert agent.runnable_config["configurable"]["recursion_limit"] == 75

    # Should have checkpointer (may fall back to memory if Supabase not configured)
    assert agent.checkpointer is not None


def test_agent_not_inheriting_from_config():
    """Test that Agent class does NOT inherit from AgentConfig."""
    # Agent should not be an instance of AgentConfig
    agent = TestAgent(name="test_agent")
    assert not isinstance(agent, AgentConfig)

    # Agent should have a config field that IS an AgentConfig
    assert hasattr(agent, "config")
    assert isinstance(agent.config, AgentConfig)

    # Check MRO doesn't include AgentConfig
    mro_classes = [cls.__name__ for cls in TestAgent.__mro__]
    assert "AgentConfig" not in mro_classes


def test_agent_config_field_types():
    """Test that agent has proper field types."""
    agent = TestAgent(name="test_agent")

    # Check essential fields exist and have correct types
    assert hasattr(agent, "name")
    assert hasattr(agent, "engines")
    assert hasattr(agent, "config")
    assert hasattr(agent, "checkpointer")
    assert hasattr(agent, "runnable_config")

    # Config should be AgentConfig or None
    assert agent.config is None or isinstance(agent.config, AgentConfig)

    # After initialization, config should be set
    agent._setup_persistence()
    assert agent.config is not None
    assert isinstance(agent.config, AgentConfig)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
