#!/usr/bin/env python3
"""Test that conversation agents actually persist data to Supabase."""

import os

import psycopg

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def check_database_after_run():
    """Run a conversation agent and check what gets saved to Supabase."""

    print("=== Testing Database Persistence ===\n")

    # Create and run a conversation agent
    print("1. Creating and running conversation agent...")
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test database persistence", participants=["Alice", "Bob"], max_rounds=1
    )

    # Get the thread_id that will be used
    thread_id = agent._generate_default_thread_id()
    print(f"   Expected thread_id: {thread_id}")

    # Run the agent with minimal input to avoid long execution
    try:
        result = agent.run({}, config={"configurable": {"recursion_limit": 5}})
        print("   ✅ Agent run completed")

        # Get the actual thread_id used
        actual_thread_id = agent.runnable_config["configurable"]["thread_id"]
        print(f"   Actual thread_id used: {actual_thread_id}")
        print(f"   Thread IDs match: {thread_id == actual_thread_id}")

    except Exception as e:
        print(f"   ⚠️ Agent run failed (expected due to LLM errors): {str(e)[:100]}...")
        # Continue with database check anyway

    # Check database for persisted data
    print("\n2. Checking Supabase database for persisted data...")

    connection_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not connection_string:
        print("   ❌ No POSTGRES_CONNECTION_STRING found")
        return

    try:
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                # Check threads table
                print("   Checking threads table...")
                cur.execute(
                    "SELECT thread_id, created_at, updated_at FROM threads WHERE thread_id = %s",
                    (thread_id,),
                )
                thread_rows = cur.fetchall()

                if thread_rows:
                    print(f"   ✅ Found thread in database: {thread_rows[0][0]}")
                    print(f"      Created: {thread_rows[0][1]}")
                    print(f"      Updated: {thread_rows[0][2]}")
                else:
                    print(f"   ❌ Thread {thread_id} not found in threads table")

                # Check checkpoints table
                print("   Checking checkpoints table...")
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
                    print(
                        f"   ✅ Found {len(checkpoint_rows)} checkpoints for thread {thread_id}"
                    )
                    for i, row in enumerate(checkpoint_rows):
                        print(
                            f"      Checkpoint {i+1}: {row[1]} (parent: {row[2]}, type: {row[3]})"
                        )
                        # Print first 100 chars of checkpoint data
                        checkpoint_data = str(row[4])[:100] if row[4] else "None"
                        print(f"         Data preview: {checkpoint_data}...")
                else:
                    print(f"   ❌ No checkpoints found for thread {thread_id}")

                # Check checkpoint_writes table
                print("   Checking checkpoint_writes table...")
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
                    print(
                        f"   ✅ Found {len(writes_rows)} checkpoint writes for thread {thread_id}"
                    )
                    for i, row in enumerate(writes_rows):
                        print(
                            f"      Write {i+1}: task={row[2]}, channel={row[3]}, type={row[4]}"
                        )
                else:
                    print(f"   ❌ No checkpoint writes found for thread {thread_id}")

                # Summary
                print(f"\n📊 Database Summary:")
                print(f"   Thread registered: {'✅' if thread_rows else '❌'}")
                print(
                    f"   Checkpoints saved: {'✅' if checkpoint_rows else '❌'} ({len(checkpoint_rows)} found)"
                )
                print(
                    f"   Writes recorded: {'✅' if writes_rows else '❌'} ({len(writes_rows)} found)"
                )

                if thread_rows and checkpoint_rows and writes_rows:
                    print(f"\n🎉 SUCCESS: Automatic persistence is fully working!")
                    print(
                        f"   Agents are automatically saving state to Supabase database"
                    )
                elif thread_rows:
                    print(f"\n⚠️ PARTIAL: Thread registered but no state data saved")
                    print(f"   This might be due to agent execution errors")
                else:
                    print(f"\n❌ FAILED: No persistence data found in database")

    except Exception as e:
        print(f"   ❌ Database error: {e}")


if __name__ == "__main__":
    check_database_after_run()
