#!/usr/bin/env python3
"""Comprehensive test of persistence including message content and async support."""

import asyncio
import json
import os
import sys
from datetime import datetime

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def test_sync_conversation():
    """Test synchronous conversation with content verification."""

    from haive.agents.conversation.collaberative.agent import CollaborativeConversation
    from haive.core.engine.aug_llm import AugLLMConfig
    from langchain_core.messages import HumanMessage

    timestamp = datetime.now().strftime("%H%M%S")

    participants = {
        f"Alice_{timestamp}": AugLLMConfig(
            name=f"Alice_{timestamp}",
            system_message="You are Alice. Always start your responses with 'Alice here:'",
        ),
        f"Bob_{timestamp}": AugLLMConfig(
            name=f"Bob_{timestamp}",
            system_message="You are Bob. Always start your responses with 'Bob here:'",
        ),
    }

    agent = CollaborativeConversation(
        name=f"TestCollab_{timestamp}",
        participant_agents=participants,
        topic="Testing message persistence",
        sections=["Introduction", "Discussion"],
        max_rounds=2,
        persistence=True,
    )

    agent.compile()

    thread_id = f"content_test_{timestamp}"
    config = {"configurable": {"thread_id": thread_id}}

    # First message

    result1 = agent.invoke(
        {
            "messages": [
                HumanMessage(content="Hello agents, please introduce yourselves")
            ],
            "topic": "Testing message persistence",
            "format": "markdown",
        },
        config,
    )

    # Check the result
    if hasattr(result1, "messages") and result1.messages:
        for i, msg in enumerate(result1.messages[-3:]):  # Last 3 messages
            pass

    # Second message to test persistence

    result2 = agent.invoke(
        {
            "messages": [HumanMessage(content="What did you discuss before?")],
        },
        config,
    )

    if hasattr(result2, "messages") and result2.messages:

        # Check if agents remember previous discussion
        last_msg = result2.messages[-1].content if result2.messages else ""
        if (
            "alice" in last_msg.lower()
            or "bob" in last_msg.lower()
            or "introduce" in last_msg.lower()
        ):
            pass")
        else:
            pass")

    return thread_id


async def test_async_persistence():
    """Test async persistence support."""

    try:
        from haive.core.persistence.factory import acreate_postgres_checkpointer
        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

        # Create async config
        config = PostgresCheckpointerConfig(
            mode="async",
            prepare_threshold=None,
            connection_kwargs={
                "prepare_threshold": None,
            },
        )

        # Create async checkpointer
        checkpointer = await acreate_postgres_checkpointer(config)


        # Test basic async operations
        from uuid import uuid4

        from langgraph.checkpoint.base import Checkpoint

        thread_id = f"async_test_{datetime.now().strftime('%H%M%S')}"
        checkpoint = Checkpoint(
            v=1,
            id=str(uuid4()),
            ts=datetime.now().isoformat(),
            channel_values={},
            channel_versions={},
            versions_seen={},
        )

        # Try to save
        config_dict = {"configurable": {"thread_id": thread_id}}

        # For AsyncPostgresSaver, we need to use async methods
        if hasattr(checkpointer, "aput"):
            await checkpointer.aput(config_dict, checkpoint, {}, {})

            # Try to retrieve
            retrieved = await checkpointer.aget(config_dict)
            if retrieved:
                pass")
            else:
                pass")
        else:
            passds")

    except Exception as e:
        import traceback

        traceback.print_exc()


def verify_database_content(thread_id: str):
    """Verify actual database content."""

    import psycopg

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Get checkpoints
                cur.execute(
                    """
                    SELECT
                        checkpoint_id,
                        parent_checkpoint_id,
                        type,
                        checkpoint,
                        metadata
                    FROM public.checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                    LIMIT 5
                """,
                    (thread_id,),
                )

                checkpoints = cur.fetchall()

                for cp_id, parent_id, _cp_type, checkpoint_data, metadata in checkpoints:

                    # Parse checkpoint data
                    if checkpoint_data:
                        try:
                            cp_dict = (
                                json.loads(checkpoint_data)
                                if isinstance(checkpoint_data, str)
                                else checkpoint_data
                            )
                            if (
                                "channel_values" in cp_dict
                                and "messages" in cp_dict["channel_values"]
                            ):
                                messages = cp_dict["channel_values"]["messages"]
                                for _i, msg in enumerate(messages[-3:]):  # Last 3
                                    if isinstance(msg, dict) and "content" in msg:
                                        pass
                        except Exception as e:
                            passe}")

                    # Check metadata
                    if metadata:
                        try:
                            meta_dict = (
                                json.loads(metadata)
                                if isinstance(metadata, str)
                                else metadata
                            )
                            if "step" in meta_dict:
                                pass
                            if "langgraph_node" in meta_dict:
                                pass
                        except:
                            pass

                # Check for prepared statements
                cur.execute(
                    """
                    SELECT COUNT(*)
                    FROM pg_prepared_statements
                    WHERE name LIKE '%pg%'
                """
                )
                ps_count = cur.fetchone()[0]

    except Exception as e:
        pass")


def main():
    """Run comprehensive persistence tests."""

    # Test sync conversation
    thread_id = test_sync_conversation()

    # Verify database content
    verify_database_content(thread_id)

    # Test async support
    asyncio.run(test_async_persistence())



if __name__ == "__main__":
    main()
