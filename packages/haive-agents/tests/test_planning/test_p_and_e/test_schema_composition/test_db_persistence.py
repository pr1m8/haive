#!/usr/bin/env python3
"""Test database persistence and retrieve data by thread ID."""

import json
import os
import uuid
from datetime import datetime

import psycopg2
from haive.core.models.llm.base import AugLLMConfig

from haive.agents.conversation.collaberative.agent import CollaborativeConversation
from haive.agents.simple.agent import SimpleAgent


def create_test_conversation():
    """Create a test conversation and return the thread ID."""
    # Generate a unique thread ID
    thread_id = f"test-thread-{uuid.uuid4()}"

    # Create agents
    agents = {
        "Alice": SimpleAgent(
            name="Alice",
            engine=AugLLMConfig(
                system_message="You are Alice, a creative thinker.",
                deployment_name="gpt-4o-mini",
            ),
        ),
        "Bob": SimpleAgent(
            name="Bob",
            engine=AugLLMConfig(
                system_message="You are Bob, a practical analyst.",
                deployment_name="gpt-4o-mini",
            ),
        ),
    }

    # Create conversation with checkpointing enabled
    conversation = CollaborativeConversation.create_brainstorming_session(
        participants=agents,
        topic="Test persistence: Database features",
        sections=["Overview", "Implementation"],
        output_format="outline",
        max_rounds=1,
        persistence=True,  # Enable persistence
        thread_id=thread_id,
    )

    # Run conversation
    conversation.invoke(
        {"messages": []}, config={"configurable": {"thread_id": thread_id}}
    )

    return thread_id


def query_database(thread_id):
    """Query the database to retrieve data for the given thread ID."""
    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg2.connect(conn_string) as conn, conn.cursor() as cursor:
            # 1. Check threads table
            cursor.execute(
                """
                    SELECT thread_id, created_at, last_access, metadata
                    FROM threads
                    WHERE thread_id = %s
                """,
                (thread_id,),
            )

            thread_data = cursor.fetchone()
            if thread_data:
            else:
                pass")

            # 2. Check checkpoints table
            cursor.execute(
                """
                    SELECT COUNT(*) as checkpoint_count,
                           MIN(checkpoint_id) as first_checkpoint,
                           MAX(checkpoint_id) as last_checkpoint
                    FROM checkpoints
                    WHERE thread_id = %s
                """,
                (thread_id,),
            )

            checkpoint_info = cursor.fetchone()
            if checkpoint_info and checkpoint_info[0] > 0:

                # Get latest checkpoint data
                cursor.execute(
                    """
                        SELECT checkpoint_id, parent_checkpoint_id,
                               checkpoint, created_at
                        FROM checkpoints
                        WHERE thread_id = %s
                        ORDER BY checkpoint_id DESC
                        LIMIT 1
                    """,
                    (thread_id,),
                )

                latest = cursor.fetchone()
                if latest:

                    # Parse checkpoint data
                    checkpoint_data = latest[2]
                    if checkpoint_data:

                        # Extract conversation state
                        if "channel_values" in checkpoint_data:
                            values = checkpoint_data["channel_values"]

                            # Show document sections if available
                            if "document_sections" in values:
                                for section, content in values[
                                    "document_sections"
                                ].items():
                                    if content:
                                        pass
            else:
                pass")

            # 3. List recent threads
            cursor.execute(
                """
                    SELECT thread_id, created_at, last_access
                    FROM threads
                    ORDER BY last_access DESC
                    LIMIT 5
                """
            )

            recent_threads = cursor.fetchall()
            for thread in recent_threads:
                pass

    except Exception:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    # Run test conversation
    thread_id = create_test_conversation()

    # Query database
    query_database(thread_id)
