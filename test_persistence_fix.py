#!/usr/bin/env python3
"""Test script to verify persistence fix for conversation agents."""

import logging

from haive.agents.conversation.collaberative.agent import CollaborativeConversation

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_persistence_fix():
    """Test that conversation agents properly use persistence when persistence=True."""

    # Test 1: Create conversation with persistence=True
    session = CollaborativeConversation.create_brainstorming_session(
        topic="Database Persistence Test",
        participants=["Alice", "Bob"],
        sections=["Overview", "Testing"],
        max_rounds=1,
        persistence=True,  # This should enable actual database persistence
    )

    # Display what persistence configuration was set up

    # Run a very short conversation
    thread_id = "test_persistence_fix_001"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 50}}

    result = session.run({}, config=config)


    # Test 2: Try to retrieve state from the same thread_id to verify persistence

    # Create another session with the same persistence config
    session2 = CollaborativeConversation.create_brainstorming_session(
        topic="Database Persistence Test - Session 2",
        participants=["Charlie", "Dave"],
        sections=["Continuation"],
        max_rounds=1,
        persistence=True,
    )

    # Try to get checkpoint
    if session2.checkpointer:
        try:
            checkpoint_config = {"configurable": {"thread_id": thread_id}}
            checkpoint = session2.checkpointer.get(checkpoint_config)
            if checkpoint:
            else:
                pass")
        except Exception as e:
            pass")
    else:
        pass")

    # Test 3: Query database directly to verify thread and checkpoint tables
    try:
        # Try to access the checkpointer's connection to query the database
        if hasattr(session.checkpointer, "conn"):
            pool = session.checkpointer.conn
            if pool:
                with pool.connection() as conn:
                    with conn.cursor() as cursor:
                        # Check threads table
                        cursor.execute(
                            "SELECT thread_id, created_at FROM threads WHERE thread_id = %s",
                            (thread_id,),
                        )
                        thread_result = cursor.fetchone()
                        if thread_result:
                            pass
                        else:
                            pass")

                        # Check checkpoints table
                        cursor.execute(
                            "SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s",
                            (thread_id,),
                        )
                        checkpoint_count = cursor.fetchone()[0]

                        if checkpoint_count > 0:
                            pass
                        else:
                            pass")
        else:
            pass")

    except Exception as e:
        pass")



if __name__ == "__main__":
    test_persistence_fix()
