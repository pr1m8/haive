"""Test that the base Agent class is simple and doesn't use AgentConfig."""

import pytest
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END

from haive.agents.base import Agent


class SimpleTestAgent(Agent):
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


def test_base_agent_is_simple():
    """Test that base Agent class doesn't use AgentConfig but sets up defaults."""
    agent = SimpleTestAgent(name="simple_agent")

    # Should NOT have config field (base Agent doesn't use AgentConfig)
    assert not hasattr(agent, "config") or getattr(agent, "config", None) is None

    # SHOULD have persistence automatically set up (default PostgreSQL + recursion limit 100)
    assert agent.persistence is not None
    assert agent.runnable_config is not None
    assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    # Should have basic defaults
    assert agent.checkpoint_mode == "sync"
    assert agent.add_store is True
    assert agent.debug is False


def test_base_agent_sets_up_default_persistence():
    """Test that base Agent sets up default persistence when setup is called."""
    agent = SimpleTestAgent(name="simple_agent")

    # Initially no persistence
    assert agent.persistence is None

    # After initialization (which calls setup), should have default persistence
    # The agent setup happens automatically in the model_validator
    assert agent.persistence is not None
    assert agent.runnable_config is not None
    assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    # Should have checkpointer set up
    assert hasattr(agent, "checkpointer")
    assert agent.checkpointer is not None


def test_base_agent_respects_explicit_persistence():
    """Test that base Agent respects explicitly provided persistence."""
    from haive.core.persistence.memory import MemoryCheckpointerConfig

    memory_config = MemoryCheckpointerConfig()

    agent = SimpleTestAgent(
        name="simple_agent", persistence=memory_config, checkpoint_mode="async"
    )

    # Should use the provided persistence
    assert agent.persistence == memory_config
    assert agent.checkpoint_mode == "async"

    # Should still set up checkpointer
    assert agent.checkpointer is not None


def test_base_agent_is_serializable():
    """Test that base Agent is properly serializable."""
    agent = SimpleTestAgent(name="simple_agent")

    # Should be serializable
    agent_dict = agent.model_dump()

    # Should include persistence fields
    assert "persistence" in agent_dict
    assert "checkpoint_mode" in agent_dict
    assert "add_store" in agent_dict
    assert "runnable_config" in agent_dict

    # Should NOT include config (base Agent doesn't have it)
    assert "config" not in agent_dict

    # Should be able to reconstruct
    reconstructed = SimpleTestAgent(**agent_dict)
    assert reconstructed.name == agent.name
    assert reconstructed.checkpoint_mode == agent.checkpoint_mode


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
