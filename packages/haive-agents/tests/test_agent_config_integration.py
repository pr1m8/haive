"""Test the ConfigurableAgent class integration with AgentConfig."""

import pytest
from haive.core.engine.agent.config import POSTGRES_AVAILABLE, AgentConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig
from langgraph.graph import END

from haive.agents.configurable_agent import ConfigurableAgent


class TestAgentConfigIntegration(ConfigurableAgent):
    """Simple test agent implementation."""

    def setup_agent(self):
        """Setup hook."""

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


def test_agent_creates_default_agent_config():
    """Test that Agent automatically creates AgentConfig with proper defaults."""
    agent = TestAgentConfigIntegration(name="test_agent")

    # Should have automatically created AgentConfig
    assert agent.config is not None
    assert hasattr(agent.config, "persistence")
    assert hasattr(agent.config, "runnable_config")

    # Should have synced persistence config from AgentConfig
    assert agent.persistence is not None
    assert agent.persistence == agent.config.persistence

    # Should have proper defaults from AgentConfig
    if POSTGRES_AVAILABLE:
        assert agent.persistence.type.value == "postgres"
    else:
        assert agent.persistence.type.value == "memory"

    # Should have recursion limit of 100 from AgentConfig
    assert agent.runnable_config is not None
    assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    # Should have checkpointer set up
    assert hasattr(agent, "checkpointer")
    assert agent.checkpointer is not None


def test_agent_uses_provided_agent_config():
    """Test that Agent uses a provided AgentConfig instead of creating one."""
    # Create custom AgentConfig
    custom_config = AgentConfig(
        checkpoint_mode="async",
        debug=True,
        save_history=False,
        runnable_config={
            "configurable": {"thread_id": "custom-thread", "recursion_limit": 50}
        },
    )

    agent = TestAgentConfigIntegration(name="test_agent", config=custom_config)

    # Should use the provided config
    assert agent.config is custom_config

    # Should sync fields from the provided config
    assert agent.checkpoint_mode == "async"
    assert agent.debug is True
    assert agent.save_history is False
    assert agent.runnable_config["configurable"]["recursion_limit"] == 50

    # Should have persistence from config
    assert agent.persistence == custom_config.persistence


def test_agent_config_with_supabase():
    """Test Agent with custom Supabase configuration through AgentConfig."""
    supabase_config = AgentConfig(
        persistence=SupabaseCheckpointerConfig(user_id="test-user", setup_needed=False),
        checkpoint_mode="sync",
        runnable_config={"configurable": {"recursion_limit": 75}},
    )

    agent = TestAgentConfigIntegration(name="test_agent", config=supabase_config)

    # Should use Supabase persistence
    assert agent.persistence.type.value == "supabase"
    assert agent.persistence.user_id == "test-user"

    # Should have correct recursion limit
    assert agent.runnable_config["configurable"]["recursion_limit"] == 75

    # Should have checkpointer (may fall back to memory if Supabase not configured)
    assert agent.checkpointer is not None


def test_agent_serialization_with_config():
    """Test that Agent is serializable even with AgentConfig."""
    agent = TestAgentConfigIntegration(name="test_agent")

    # Agent should be serializable (config is excluded)
    agent_dict = agent.model_dump()

    # Should include serializable persistence fields
    assert "persistence" in agent_dict
    assert "checkpoint_mode" in agent_dict
    assert "add_store" in agent_dict
    assert "runnable_config" in agent_dict

    # Should NOT include config (excluded from serialization)
    assert "config" not in agent_dict

    # Should be able to reconstruct from dict (without config)
    reconstructed = TestAgentConfigIntegration(**agent_dict)

    # Should create new AgentConfig automatically
    assert reconstructed.config is not None
    assert reconstructed.config is not agent.config  # Different instance

    # Should have same persistence settings
    assert reconstructed.checkpoint_mode == agent.checkpoint_mode
    assert reconstructed.add_store == agent.add_store


def test_agent_field_overrides():
    """Test that Agent field values can override AgentConfig defaults."""
    # Create agent with explicit field overrides
    agent = TestAgentConfigIntegration(
        name="test_agent",
        checkpoint_mode="async",  # Override default
        debug=True,  # Override default
        add_store=False,  # Override default
    )

    # Fields should keep their explicit values
    assert agent.checkpoint_mode == "async"
    assert agent.debug is True
    assert agent.add_store is False

    # Should still have AgentConfig created
    assert agent.config is not None

    # Config should have its own defaults (not affected by field overrides)
    assert agent.config.checkpoint_mode == "sync"  # AgentConfig default
    assert agent.config.debug is False  # AgentConfig default
    assert agent.config.add_store is False  # AgentConfig default


def test_agent_persistence_config_consistency():
    """Test that persistence configuration is consistent between Agent and AgentConfig."""
    agent = TestAgentConfigIntegration(name="test_agent")

    # Persistence config should be synced
    assert agent.persistence == agent.config.persistence

    # If we update Agent's persistence, it should be independent of config
    from haive.core.persistence.memory import MemoryCheckpointerConfig

    new_persistence = MemoryCheckpointerConfig()

    agent.persistence = new_persistence

    # Agent field updated
    assert agent.persistence == new_persistence

    # Config unchanged (agent fields are independent after initialization)
    assert agent.config.persistence != new_persistence


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
