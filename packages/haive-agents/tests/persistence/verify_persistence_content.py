#!/usr/bin/env python3
"""Verify that persistence is working correctly with proper content."""

import json
import os
import sys
from datetime import datetime

import psycopg

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def test_simple_agent_persistence():
    """Test simple agent with message persistence."""

    from langchain_core.messages import HumanMessage

    from haive.agents.simple.agent import SimpleAgent

    timestamp = datetime.now().strftime("%H%M%S")

    # Create agent
    agent = SimpleAgent(
        name=f"TestSimple_{timestamp}",
        system_message="You are a helpful assistant. Always mention your name 'TestSimple' in responses.",
        persistence=True,
    )

    agent.compile()

    thread_id = f"verify_test_{timestamp}"
    config = {"configurable": {"thread_id": thread_id}}

    # First interaction

    result1 = agent.invoke(
        {"messages": [HumanMessage(content="Hello, what's your name?")]}, config
    )

    # Handle result format
    messages1 = result1.messages if hasattr(result1, "messages") else result1.get("messages", [])


    # Second interaction - test memory

    result2 = agent.invoke(
        {"messages": [HumanMessage(content="What did I just ask you?")]}, config
    )

    # Handle result format
    messages2 = result2.messages if hasattr(result2, "messages") else result2.get("messages", [])

    response = messages2[-1].content if messages2 else ""

    # Check if agent remembers
    if "name" in response.lower() or "asked" in response.lower():
        pass")
    else:
        pass")

    return thread_id, len(messages2)


def verify_checkpoint_content(thread_id: str, expected_messages: int):
    """Verify checkpoint content in database."""

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Get latest checkpoint
                cur.execute(
                    """
                    SELECT
                        checkpoint_id,
                        checkpoint
                    FROM public.checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                    LIMIT 1
                """,
                    (thread_id,),
                )

                result = cur.fetchone()
                if result:
                    checkpoint_id, checkpoint_data = result

                    # Parse checkpoint
                    cp_dict = (
                        json.loads(checkpoint_data)
                        if isinstance(checkpoint_data, str)
                        else checkpoint_data
                    )

                    # Check channel values
                    if (
                        "channel_values" in cp_dict
                        and "messages" in cp_dict["channel_values"]
                    ):
                        messages = cp_dict["channel_values"]["messages"]

                        if len(messages) == expected_messages:
                            pass
                        else:
                            pass

                        # Show messages
                        for i, msg in enumerate(messages):
                            msg_type = msg.get("type", "unknown")
                            content = msg.get("content", "")[:100]
                    else:
                        pass")
                else:
                    pass")

                # Check prepared statements
                cur.execute(
                    "SELECT COUNT(*) FROM pg_prepared_statements WHERE name LIKE '%pg%'"
                )
                ps_count = cur.fetchone()[0]

    except Exception as e:
        pass")


def test_async_checkpointer():
    """Test async checkpointer configuration."""

    from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

    # Create async config
    config = PostgresCheckpointerConfig(
        mode="async",
        prepare_threshold=None,
        connection_kwargs={
            "prepare_threshold": None,
            "application_name": "test_async_checkpointer",
        },
    )



def main():
    """Run persistence verification tests."""

    # Test simple agent
    thread_id, message_count = test_simple_agent_persistence()

    # Verify database content
    verify_checkpoint_content(thread_id, message_count)

    # Test async config
    test_async_checkpointer()



if __name__ == "__main__":
    main()
