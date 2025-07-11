#!/usr/bin/env python3
"""Test that conversation agents actually persist data to Supabase."""

import os

import psycopg

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def check_database_after_run():
    """Run a conversation agent and check what gets saved to Supabase."""

    # Create and run a conversation agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test database persistence", participants=["Alice", "Bob"], max_rounds=1
    )

    # Get the thread_id that will be used
    thread_id = agent._generate_default_thread_id()

    # Run the agent with minimal input to avoid long execution
    try:
        agent.run({}, config={"configurable": {"recursion_limit": 5}})

        # Get the actual thread_id used
        actual_thread_id = agent.runnable_config["configurable"]["thread_id"]

    except Exception as e:
        pass..")
        # Continue with database check anyway

    # Check database for persisted data

    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not connection_string:
        return

    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                # Check threads table
                cur.execute(
                    "SELECT thread_id, created_at, updated_at FROM threads WHERE thread_id = %s",
                    (thread_id,),
                )
                thread_rows = cur.fetchall()

                if thread_rows:
                else:
                    pass")

                # Check checkpoints table
                cur.execute(
                    """
                    SELECT thread_id, checkpoint_id, parent_checkpoint_id, type, checkpoint
                    FROM checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id
                    LIMIT 5
                """,
                    (thread_id,),
                )
                checkpoint_rows = cur.fetchall()

                if checkpoint_rows:
                    for i, row in enumerate(checkpoint_rows):
                        # Print first 100 chars of checkpoint data
                        checkpoint_data = str(row[4])[:100] if row[4] else "None"
                else:
                    pass")

                # Check checkpoint_writes table
                cur.execute(
                    """
                    SELECT thread_id, checkpoint_id, task_id, channel, type, value
                    FROM checkpoint_writes
                    WHERE thread_id = %s
                    LIMIT 5
                """,
                    (thread_id,),
                )
                writes_rows = cur.fetchall()

                if writes_rows:
                    for i, row in enumerate(writes_rows):
                        pass
                else:
                    pass")

                # Summary

                if thread_rows and checkpoint_rows and writes_rows:
                elif thread_rows:
                else:
                    pass")

    except Exception as e:
        pass")


if __name__ == "__main__":
    check_database_after_run()
