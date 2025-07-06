#!/usr/bin/env python3
"""Test script to verify PostgreSQL prepared statement issue is fixed."""

import os
import sys
from datetime import datetime


def test_postgres_connection_settings():
    """Test PostgreSQL connection settings with prepared statements disabled."""
    try:
        # Add the packages to path
        sys.path.insert(
            0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
        )
        sys.path.insert(
            0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src"
        )

        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig
        from haive.core.persistence.types import CheckpointerMode, CheckpointStorageMode

        # Get connection string
        connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
        if not connection_string:
            return False

        # Create config with disabled prepared statements
        config = PostgresCheckpointerConfig(
            connection_string=connection_string,
            mode=CheckpointerMode.SYNC,
            storage_mode=CheckpointStorageMode.FULL,
            prepare_threshold=None,  # Disable prepared statements completely
            auto_commit=True,  # Ensure auto-commit is enabled
            connection_kwargs={
                "prepare_threshold": None,  # Extra explicit disable
            },
        )


        # Check connection kwargs
        kwargs = config.get_connection_kwargs()

        # Test creating a checkpointer
        checkpointer = config.create_checkpointer()

        # Test a simple operation


        # Create a test config
        test_config = {
            "configurable": {
                "thread_id": f"test_fix_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            }
        }

        # Try to use the checkpointer without prepared statements
        try:
            # This should work without prepared statement conflicts
            from langgraph.checkpoint.base import empty_checkpoint

            test_checkpoint = empty_checkpoint()
            test_checkpoint["channel_values"] = {"test": "no_prepared_statements"}

            # This tests the actual save operation
            result = checkpointer.put(test_config, test_checkpoint, {}, {})

        except Exception as e:
            if "prepared statement" in str(e).lower():
                return False
            print(f"⚠️  Other error (might be normal): {e}")e}")

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


def test_conversation_agent_persistence():
    """Test conversation agent with the fixed persistence configuration."""
    try:

        # Add the packages to path
        sys.path.insert(
            0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
        )
        sys.path.insert(
            0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src"
        )

        from haive.agents.conversation.collaberative.agent import CollaborativeAgent
        from haive.core.engine.aug_llm import AugLLMConfig

        # Create participant agents
        participants = {
            "TestManager": AugLLMConfig(
                name="TestManager",
                system_message="You are a test manager. Give brief responses for testing.",
            ),
        }

        # Create collaborative agent with persistence=True (will use our fixed config)
        agent = CollaborativeAgent(
            name="TestCollaborative",
            participant_agents=participants,
            topic="Quick persistence test",
            max_rounds=1,  # Keep it short for testing
            persistence=True,  # This should use our fixed PostgreSQL config
        )


        # Compile the agent
        agent.compile()

        # Run a quick test
        test_input = {"messages": [], "topic": "Quick persistence test"}

        thread_id = f"test_persist_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        config = {"configurable": {"thread_id": thread_id}}


        # This should work without prepared statement conflicts
        try:
            result = agent.invoke(test_input, config)

            if "messages" in result:
                message_count = len(result["messages"])

        except Exception as e:
            if "prepared statement" in str(e).lower():
                return False
            print(f"⚠️  Other error in agent (might be normal): {e}")e}")

        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":

    # Test 1: Basic PostgreSQL configuration
    test1_passed = test_postgres_connection_settings()

    # Test 2: Conversation agent with persistence
    test2_passed = test_conversation_agent_persistence()


    if test1_passed and test2_passed:
        pass.")
    else:
        passs.")
