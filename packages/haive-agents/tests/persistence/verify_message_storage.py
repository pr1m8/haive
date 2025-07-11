#!/usr/bin/env python3
"""Verify messages are actually stored and retrievable."""

import json
import os
import sys
from datetime import datetime

import psycopg

sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def test_message_persistence():
    """Test that messages are actually persisted and retrievable."""

    from langchain_core.messages import HumanMessage

    from haive.agents.simple.agent import SimpleAgent

    timestamp = datetime.now().strftime("%H%M%S")
    thread_id = f"msg_test_{timestamp}"

    # Create agent
    agent = SimpleAgent(
        name=f"MsgTest_{timestamp}",
        system_message="You are a test agent. Always include the word 'PERSISTENCE' in your responses.",
        persistence=True,
    )
    agent.compile()

    config = {"configurable": {"thread_id": thread_id}}

    # First message

    result1 = agent.invoke(
        {"messages": [HumanMessage(content="Hello, this is message one")]}, config
    )

    msg1_response = (
        result1.messages[-1].content if hasattr(result1, "messages") else "No response"
    )

    # Second message

    result2 = agent.invoke(
        {"messages": [HumanMessage(content="What was my first message?")]}, config
    )

    msg2_response = (
        result2.messages[-1].content if hasattr(result2, "messages") else "No response"
    )

    # Check if agent remembers
    remembers = (
        "message one" in msg2_response.lower() or "hello" in msg2_response.lower()
    )

    # Verify in database

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn, conn.cursor() as cur:
            # Get checkpoints for this thread
            cur.execute(
                """
                    SELECT 
                        checkpoint_id,
                        checkpoint
                    FROM public.checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                """,
                (thread_id,),
            )

            checkpoints = cur.fetchall()
            print(
                f"\n📊 Found {len(checkpoints)} checkpoints for thread {thread_id}"
            )

            # Check latest checkpoint
            if checkpoints:
                latest_cp_id, latest_cp = checkpoints[0]
                print(f"\n📋 Latest checkpoint: {latest_cp_id}")

                # Parse checkpoint
                cp_data = (
                    json.loads(latest_cp)
                    if isinstance(latest_cp, str)
                    else latest_cp
                )

                # Check messages
                if (
                    "channel_values" in cp_data
                    and "messages" in cp_data["channel_values"]
                ):
                    messages = cp_data["channel_values"]["messages"]
                    print(f"✅ Found {len(messages)} messages in checkpoint")

                    print("\n📝 Stored messages:")
                    for i, msg in enumerate(messages):
                        msg_type = msg.get("type", "unknown")
                        content = msg.get("content", "")[:80]
                        print(f"   {i+1}. [{msg_type}]: {content}...")

                        # Verify our messages are there
                        if (
                            i == 0
                            and msg_type == "human"
                            and "message one" in msg.get("content", "")
                        ):
                            print("      ✅ First message correctly stored")
                        elif (
                            i == 2
                            and msg_type == "human"
                            and "first message" in msg.get("content", "")
                        ):
                            print("      ✅ Second message correctly stored")
                        elif msg_type == "ai" and "PERSISTENCE" in msg.get(
                            "content", ""
                        ):
                            print(
                                "      ✅ AI response includes PERSISTENCE keyword"
                            )
                else:
                    print("❌ No messages found in checkpoint")

            # Check checkpoint_blobs for actual message storage
            print("\n🔍 Checking checkpoint_blobs table...")
            cur.execute(
                """
                    SELECT 
                        channel,
                        type,
                        length(blob) as blob_size
                    FROM public.checkpoint_blobs
                    WHERE thread_id = %s
                    ORDER BY channel
                """,
                (thread_id,),
            )

            blobs = cur.fetchall()
            if blobs:
                print(f"✅ Found {len(blobs)} blobs")
                for channel, blob_type, size in blobs:
                    print(f"   - {channel}: {blob_type} ({size} bytes)")

    except Exception as e:
        import traceback

        traceback.print_exc()


def check_store_persistence_link():
    """Check if store persistence is properly linked."""

    # Check if stores use the ConnectionManager

    store_files = [
        "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/base.py",
        "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/postgres.py",
    ]

    for file_path in store_files:
        if os.path.exists(file_path):
            try:
                with open(file_path) as f:
                    content = f.read()

                # Check for ConnectionManager usage
                if "ConnectionManager" in content:

                    # Check how it's used
                    for line in content.split("\n"):
                        if "ConnectionManager.get_or_create" in line:
                            pass
                else:
                    pass")

                # Check for prepare_threshold
                if "prepare_threshold" in content:
                    passon")

            except Exception as e:
                pass")
        else:
            pass")

    # Check persistence config integration

    try:
        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

        config = PostgresCheckpointerConfig()

        if config.prepare_threshold is None:
            pass")
        else:
            pass")

    except Exception as e:
        pass")


def main():
    """Run all verification tests."""
    # Test message persistence
    test_message_persistence()

    # Check store integration
    check_store_persistence_link()



if __name__ == "__main__":
    main()
