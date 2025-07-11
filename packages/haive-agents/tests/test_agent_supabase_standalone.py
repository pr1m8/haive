"""Standalone agent Supabase integration tests (no conftest dependencies)."""

import os
import sys
from pathlib import Path

# Add the packages to Python path
agents_path = Path(__file__).parent.parent / "src"
core_path = Path(__file__).parent.parent.parent / "haive-core" / "src"
sys.path.insert(0, str(agents_path))
sys.path.insert(0, str(core_path))

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_agent_import():
    """Test that we can import the agent classes."""
    try:

        return True

    except Exception as e:
        return False


def test_agent_with_supabase_config():
    """Test creating agent with Supabase configuration."""
    if not os.getenv("POSTGRES_CONNECTION_STRING"):
        return True

    try:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig
        from haive.core.persistence.types import CheckpointerMode
        from langgraph.graph import END

        from haive.agents.base import Agent

        # Create a test agent class
        class TestAgent(Agent):
            def setup_agent(self):
                pass

            def build_graph(self) -> BaseGraph:
                # Import here to avoid circular imports
                try:
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
                except ImportError:
                    # Fallback to basic implementation
                    from haive.core.graph.state_graph.base_graph2 import BaseGraph

                    return BaseGraph()

        # Create Supabase config
        supabase_config = SupabaseCheckpointerConfig(
            user_id="test-agent-user", mode=CheckpointerMode.SYNC, setup_needed=False
        )

        # Create checkpointer
        checkpointer = supabase_config.create_checkpointer()

        # Create agent with Supabase persistence
        agent = TestAgent(
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
        assert agent.runnable_config["configurable"]["recursion_limit"] == 100

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_agent_store_integration():
    """Test agent with store integration."""
    if not os.getenv("POSTGRES_CONNECTION_STRING"):
        return True

    try:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig

        from haive.agents.base import Agent

        class StoreTestAgent(Agent):
            def setup_agent(self):
                pass

            def build_graph(self) -> BaseGraph:
                return BaseGraph()

        # Create Supabase config
        supabase_config = SupabaseCheckpointerConfig(
            user_id="test-store-agent-user", setup_needed=False
        )

        # Create both checkpointer and store
        checkpointer, store = supabase_config.create_checkpointer_and_store()

        # Create agent with both
        agent = StoreTestAgent(
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

        return True

    except Exception as e:
        return False


def test_agent_persistence_fields():
    """Test that agent persistence fields are properly set."""
    try:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph

        from haive.agents.base import Agent

        class FieldTestAgent(Agent):
            def setup_agent(self):
                pass

            def build_graph(self) -> BaseGraph:
                return BaseGraph()

        # Test agent with persistence fields
        agent = FieldTestAgent(
            name="field_test_agent",
            persistence=None,  # No actual persistence for this test
            checkpoint_mode="sync",
            add_store=True,
            runnable_config={
                "configurable": {
                    "thread_id": "field-test-thread",
                    "recursion_limit": 100,
                }
            },
        )

        # Verify fields are set correctly
        assert agent.name == "field_test_agent"
        assert agent.checkpoint_mode == "sync"
        assert agent.add_store is True
        assert agent.runnable_config["configurable"]["recursion_limit"] == 100

        return True

    except Exception as e:
        return False


def test_agent_factory_pattern():
    """Test factory pattern for creating agents with Supabase."""
    if not os.getenv("POSTGRES_CONNECTION_STRING"):
        return True

    try:
        from haive.core.graph.state_graph.base_graph2 import BaseGraph
        from haive.core.persistence.supabase_config import SupabaseCheckpointerConfig

        from haive.agents.base import Agent

        class FactoryAgent(Agent):
            def setup_agent(self):
                pass

            def build_graph(self) -> BaseGraph:
                return BaseGraph()

        def create_supabase_agent(
            name: str, user_id: str, thread_id: str
        ) -> FactoryAgent:
            """Factory function to create agent with Supabase persistence."""
            supabase_config = SupabaseCheckpointerConfig(
                user_id=user_id, setup_needed=False
            )

            checkpointer = supabase_config.create_checkpointer()

            return FactoryAgent(
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

        return True

    except Exception as e:
        return False


def main():
    """Run all agent tests."""

    results = []
    results.append(test_agent_import())
    results.append(test_agent_with_supabase_config())
    results.append(test_agent_store_integration())
    results.append(test_agent_persistence_fields())
    results.append(test_agent_factory_pattern())

    passed = sum(results)
    total = len(results)


    if passed == total:
        pass!")
    else:
        passed")

    return passed == total


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
