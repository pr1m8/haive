#!/usr/bin/env python3
"""Simple test of database persistence."""

import os
import uuid

import psycopg2

from haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_conversation_with_db():
    """Test conversation with database persistence."""

    # Generate a unique thread ID
    thread_id = f"test-{uuid.uuid4()}"

    # Create a simple brainstorming session
    session = CollaborativeConversation.create_brainstorming_session(
        topic="Database Persistence Test",
        participants=["Alice", "Bob"],
        sections=["Overview", "Testing"],
        max_rounds=1,
        persistence=True,  # Enable persistence
    )

    # Run with specific thread ID
    result = session.invoke({}, config={"configurable": {"thread_id": thread_id}})


    # Handle result which might be an object
    if hasattr(result, "messages"):
        pass
    elif isinstance(result, dict):
        pass

    return thread_id


def query_database(thread_id):
    """Query database for thread data."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg2.connect(conn_string) as conn, conn.cursor() as cursor:
            # Check threads table
            cursor.execute(
                """
                    SELECT thread_id, created_at, last_access
                    FROM threads WHERE thread_id = %s
                """,
                (thread_id,),
            )

            thread = cursor.fetchone()
            if thread:
                print(f"✅ Thread found in threads table")
                print(f"   Created: {thread[1]}")
                print(f"   Last access: {thread[2]}")

            # Check checkpoints
            cursor.execute(
                """
                    SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s
                """,
                (thread_id,),
            )

            count = cursor.fetchone()[0]
            print(f"\n✅ Checkpoints found: {count}")

            # Get latest checkpoint
            cursor.execute(
                """
                    SELECT checkpoint_id, checkpoint, created_at
                    FROM checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                    LIMIT 1
                """,
                (thread_id,),
            )

            checkpoint = cursor.fetchone()
            if checkpoint:
                print(f"\nLatest checkpoint:")
                print(f"   ID: {checkpoint[0]}")
                print(f"   Created: {checkpoint[2]}")

                # Extract state
                data = checkpoint[1]
                if "channel_values" in data:
                    values = data["channel_values"]
                    print(f"\nState summary:")
                    print(f"   Messages: {len(values.get('messages', []))}")
                    print(f"   Topic: {values.get('topic')}")
                    print(f"   Speakers: {values.get('speakers', [])}")
                    print(f"   Turn count: {values.get('turn_count')}")

                    # Show sections
                    sections = values.get("document_sections", {})
                    if sections:
                        print(f"\nDocument sections:")
                        for section, content in sections.items():
                            if content:
                                print(f"   - {section}: {len(content)} chars")

    except Exception as e:
        pass")


if __name__ == "__main__":
    # Run test
    thread_id = test_conversation_with_db()

    # Query database
    query_database(thread_id)
