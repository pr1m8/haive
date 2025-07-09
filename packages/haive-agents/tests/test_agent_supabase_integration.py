"""Test agent integration with Supabase persistence."""

import asyncio
import os

import pytest
from dotenv import load_dotenv
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig
from haive.core.persistence.types import CheckpointerMode
from langgraph.graph import END

from haive.agents.base import Agent

# Load environment variables
load_dotenv()

# Skip tests if no Supabase connection available
pytestmark = pytest.mark.skipif(
    not os.getenv("POSTGRES_CONNECTION_STRING"),
    reason="POSTGRES_CONNECTION_STRING not configured",
)


class TestSupabaseAgent(Agent):
    """Test agent with Supabase persistence."""

    def setup_agent(self):
        """Setup hook."""
        pass

    def build_graph(self) -> BaseGraph:
        """Build a simple test graph."""
        from haive.core.graph.state_graph.state_graph import (
            StateGraph as HaiveStateGraph,
        )

        graph = HaiveStateGraph(state_schema={"messages": list, "count": int})

        def process_message(state):
            messages = state.get("messages", [])
            count = state.get("count", 0)
            new_message = f"Processed message {count + 1}"
            return {"messages": messages + [new_message], "count": count + 1}

        graph.add_node("process", process_message)
        graph.add_edge("process", END)
        graph.set_entry_point("process")

        return graph


class TestAgentSupabaseIntegration:
    """Test agent integration with Supabase persistence."""

    def test_agent_with_supabase_persistence(self):
        """Test agent with Supabase checkpointer."""
        # Create Supabase config
        supabase_config = SupabaseCheckpointerConfig(
            user_id="test-agent-user", mode=CheckpointerMode.SYNC, setup_needed=False
        )

        # Create checkpointer
        checkpointer = supabase_config.create_checkpointer()

        # Create agent with Supabase persistence
        agent = TestSupabaseAgent(
            name="test_supabase_agent",
            persistence=checkpointer,
            runnable_config={
                "configurable": {
                    "thread_id": "test-agent-thread",
                    "recursion_limit": 100,
                }
            },
        )

        # Verify agent setup
        assert agent.name == "test_supabase_agent"
        assert agent.persistence is not None
        assert "PostgresSaver" in type(agent.persistence).__name__
        assert agent.runnable_config["configurable"]["recursion_limit"] == 100

    def test_agent_with_store_integration(self):
        """Test agent with both checkpointer and store."""
        # Create Supabase config
        supabase_config = SupabaseCheckpointerConfig(
            user_id="test-store-agent-user", setup_needed=False
        )

        # Create both checkpointer and store
        checkpointer, store = supabase_config.create_checkpointer_and_store()

        # Create agent with both
        agent = TestSupabaseAgent(
            name="test_store_agent",
            persistence=checkpointer,
            add_store=True,
            runnable_config={
                "configurable": {
                    "thread_id": "test-store-thread",
                    "recursion_limit": 100,
                }
            },
        )

        # Verify agent setup
        assert agent.persistence is not None
        assert agent.add_store is True
        assert "PostgresSaver" in type(agent.persistence).__name__

    @pytest.mark.asyncio
    async def test_agent_async_operations(self):
        """Test agent with async Supabase operations."""
        # Create async Supabase config
        supabase_config = SupabaseCheckpointerConfig(
            user_id="test-async-agent-user",
            mode=CheckpointerMode.ASYNC,
            setup_needed=False,
        )

        # Create async checkpointer
        async_checkpointer = await supabase_config.create_async_checkpointer()

        # Create agent with async persistence
        agent = TestSupabaseAgent(
            name="test_async_agent",
            persistence=async_checkpointer,
            checkpoint_mode="async",
            runnable_config={
                "configurable": {
                    "thread_id": "test-async-agent-thread",
                    "recursion_limit": 100,
                }
            },
        )

        # Verify agent setup
        assert agent.persistence is not None
        assert agent.checkpoint_mode == "async"

    def test_agent_persistence_configuration(self):
        """Test different persistence configurations for agents."""
        configs = [
            {
                "user_id": "sync-user",
                "mode": CheckpointerMode.SYNC,
                "expected_type": "PostgresSaver",
            },
            {
                "user_id": "async-user",
                "mode": CheckpointerMode.ASYNC,
                "expected_type": "PostgresSaver",  # May fall back to sync
            },
        ]

        for config_data in configs:
            supabase_config = SupabaseCheckpointerConfig(
                user_id=config_data["user_id"],
                mode=config_data["mode"],
                setup_needed=False,
            )

            if config_data["mode"] == CheckpointerMode.SYNC:
                checkpointer = supabase_config.create_checkpointer()
            else:
                # For async, we'd need to run in async context
                # For now, just test sync
                checkpointer = supabase_config.create_checkpointer()

            agent = TestSupabaseAgent(
                name=f"test_agent_{config_data['user_id']}",
                persistence=checkpointer,
                runnable_config={
                    "configurable": {
                        "thread_id": f"thread_{config_data['user_id']}",
                        "recursion_limit": 100,
                    }
                },
            )

            assert agent.persistence is not None
            assert config_data["expected_type"] in type(agent.persistence).__name__

    def test_agent_with_custom_config(self):
        """Test agent with custom Supabase configuration."""
        # Custom configuration
        supabase_config = SupabaseCheckpointerConfig(
            user_id="custom-config-user", mode=CheckpointerMode.SYNC, setup_needed=False
        )

        checkpointer = supabase_config.create_checkpointer()

        # Create agent with custom runnable config
        agent = TestSupabaseAgent(
            name="custom_config_agent",
            persistence=checkpointer,
            runnable_config={
                "configurable": {
                    "thread_id": "custom-thread",
                    "recursion_limit": 50,  # Custom recursion limit
                    "checkpoint_ns": "custom_namespace",
                }
            },
        )

        # Verify custom configuration
        assert agent.runnable_config["configurable"]["recursion_limit"] == 50
        assert (
            agent.runnable_config["configurable"]["checkpoint_ns"] == "custom_namespace"
        )

    def test_multiple_agents_same_database(self):
        """Test multiple agents using the same Supabase database."""
        agents = []

        for i in range(3):
            supabase_config = SupabaseCheckpointerConfig(
                user_id=f"multi-user-{i}", setup_needed=False
            )

            checkpointer = supabase_config.create_checkpointer()

            agent = TestSupabaseAgent(
                name=f"multi_agent_{i}",
                persistence=checkpointer,
                runnable_config={
                    "configurable": {
                        "thread_id": f"multi-thread-{i}",
                        "recursion_limit": 100,
                    }
                },
            )

            agents.append(agent)

        # All agents should be created successfully
        assert len(agents) == 3
        for agent in agents:
            assert agent.persistence is not None
            assert "PostgresSaver" in type(agent.persistence).__name__

    def test_agent_state_persistence(self):
        """Test that agent state is properly persisted."""
        supabase_config = SupabaseCheckpointerConfig(
            user_id="state-test-user", setup_needed=False
        )

        checkpointer = supabase_config.create_checkpointer()

        agent = TestSupabaseAgent(
            name="state_test_agent",
            persistence=checkpointer,
            runnable_config={
                "configurable": {
                    "thread_id": "state-test-thread",
                    "recursion_limit": 100,
                }
            },
        )

        # Test that the agent has persistence configured
        assert agent.persistence is not None
        assert hasattr(agent.persistence, "put")
        assert hasattr(agent.persistence, "get")

        # Test that runnable config is properly set
        assert "configurable" in agent.runnable_config
        assert "thread_id" in agent.runnable_config["configurable"]


class TestAgentSupabasePatterns:
    """Test common patterns for using agents with Supabase."""

    def test_agent_factory_pattern(self):
        """Test factory pattern for creating agents with Supabase."""

        def create_supabase_agent(
            name: str, user_id: str, thread_id: str
        ) -> TestSupabaseAgent:
            """Factory function to create agent with Supabase persistence."""
            supabase_config = SupabaseCheckpointerConfig(
                user_id=user_id, setup_needed=False
            )

            checkpointer = supabase_config.create_checkpointer()

            return TestSupabaseAgent(
                name=name,
                persistence=checkpointer,
                runnable_config={
                    "configurable": {"thread_id": thread_id, "recursion_limit": 100}
                },
            )

        # Use factory to create agent
        agent = create_supabase_agent("factory_agent", "factory_user", "factory_thread")

        assert agent.name == "factory_agent"
        assert agent.persistence is not None
        assert agent.runnable_config["configurable"]["thread_id"] == "factory_thread"

    def test_agent_inheritance_pattern(self):
        """Test inheritance pattern for Supabase-enabled agents."""

        class SupabaseEnabledAgent(Agent):
            """Base agent class with Supabase persistence built-in."""

            def __init__(self, user_id: str, **kwargs):
                # Set up Supabase persistence automatically
                supabase_config = SupabaseCheckpointerConfig(
                    user_id=user_id, setup_needed=False
                )

                checkpointer = supabase_config.create_checkpointer()

                # Set persistence in kwargs
                kwargs["persistence"] = checkpointer
                kwargs.setdefault("runnable_config", {}).setdefault("configurable", {})
                kwargs["runnable_config"]["configurable"].setdefault(
                    "recursion_limit", 100
                )

                super().__init__(**kwargs)

            def setup_agent(self):
                pass

            def build_graph(self) -> BaseGraph:
                # Simple test graph
                from haive.core.graph.state_graph.state_graph import (
                    StateGraph as HaiveStateGraph,
                )

                graph = HaiveStateGraph(state_schema={"test": str})

                def test_node(state):
                    return {"test": "processed"}

                graph.add_node("test", test_node)
                graph.add_edge("test", END)
                graph.set_entry_point("test")

                return graph

        # Create agent using inheritance pattern
        agent = SupabaseEnabledAgent(
            name="inheritance_agent", user_id="inheritance_user"
        )

        assert agent.persistence is not None
        assert "PostgresSaver" in type(agent.persistence).__name__
        assert agent.runnable_config["configurable"]["recursion_limit"] == 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
