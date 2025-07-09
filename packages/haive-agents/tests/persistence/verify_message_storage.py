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
    print("🔍 Testing Message Storage and Retrieval")
    print("=" * 70)

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
    print(f"\n📝 Thread ID: {thread_id}")
    print("📤 Message 1: 'Hello, this is message one'")

    result1 = agent.invoke(
        {"messages": [HumanMessage(content="Hello, this is message one")]}, config
    )

    msg1_response = (
        result1.messages[-1].content if hasattr(result1, "messages") else "No response"
    )
    print(f"📥 Response 1: {msg1_response[:100]}...")

    # Second message
    print("\n📤 Message 2: 'What was my first message?'")

    result2 = agent.invoke(
        {"messages": [HumanMessage(content="What was my first message?")]}, config
    )

    msg2_response = (
        result2.messages[-1].content if hasattr(result2, "messages") else "No response"
    )
    print(f"📥 Response 2: {msg2_response[:100]}...")

    # Check if agent remembers
    remembers = (
        "message one" in msg2_response.lower() or "hello" in msg2_response.lower()
    )
    print(
        f"\n{'✅' if remembers else '❌'} Agent {'remembers' if remembers else 'does not remember'} the first message"
    )

    # Verify in database
    print("\n🔍 Checking Database Storage...")

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ No connection string")
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
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
        print(f"❌ Database error: {e}")
        import traceback

        traceback.print_exc()


def check_store_persistence_link():
    """Check if store persistence is properly linked."""
    print("\n\n🔍 Checking Store Persistence Integration")
    print("=" * 70)

    # Check if stores use the ConnectionManager
    print("\n1️⃣ Checking store implementations...")

    store_files = [
        "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/base.py",
        "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/postgres.py",
    ]

    for file_path in store_files:
        if os.path.exists(file_path):
            print(f"\n📄 {os.path.basename(file_path)}:")
            try:
                with open(file_path, "r") as f:
                    content = f.read()

                # Check for ConnectionManager usage
                if "ConnectionManager" in content:
                    print("   ✅ Uses ConnectionManager")

                    # Check how it's used
                    for line in content.split("\n"):
                        if "ConnectionManager.get_or_create" in line:
                            print(f"   Found: {line.strip()[:80]}...")
                else:
                    print("   ❌ Does not use ConnectionManager")

                # Check for prepare_threshold
                if "prepare_threshold" in content:
                    print("   ⚠️  Contains prepare_threshold configuration")

            except Exception as e:
                print(f"   ❌ Error reading: {e}")
        else:
            print(f"\n❌ File not found: {file_path}")

    # Check persistence config integration
    print("\n2️⃣ Checking persistence configuration...")

    try:
        from haive.core.persistence.postgres_config import PostgresCheckpointerConfig

        config = PostgresCheckpointerConfig()
        print(f"   Default prepare_threshold: {config.prepare_threshold}")
        print(f"   Default connection_kwargs: {config.connection_kwargs}")

        if config.prepare_threshold is None:
            print("   ✅ Default config disables prepared statements")
        else:
            print("   ❌ Default config does not disable prepared statements")

    except Exception as e:
        print(f"   ❌ Error checking config: {e}")


def main():
    """Run all verification tests."""
    # Test message persistence
    test_message_persistence()

    # Check store integration
    check_store_persistence_link()

    print("\n" + "=" * 70)
    print("✅ Verification complete!")


if __name__ == "__main__":
    main()
