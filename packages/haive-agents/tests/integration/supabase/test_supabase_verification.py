#!/usr/bin/env python3
"""Test and verify Supabase writes are working."""

import asyncio
import os
from datetime import datetime

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent

# Clear cached pools
print("🧹 Clearing cached pools...")
try:
    from haive.core.persistence.postgres_config import (
        ASYNC_CHECKPOINTERS,
        ASYNC_POOLS,
        SYNC_CHECKPOINTERS,
        SYNC_POOLS,
    )

    SYNC_POOLS.clear()
    ASYNC_POOLS.clear()
    SYNC_CHECKPOINTERS.clear()
    ASYNC_CHECKPOINTERS.clear()
    print("✅ Cleared all cached pools")
except:
    pass


async def test_and_verify():
    """Test agent and verify data in Supabase."""

    print("\n🧪 Testing Supabase Write and Verification")
    print("=" * 60)

    # Create unique thread ID
    thread_id = f"verify_test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
    print(f"\n📝 Thread ID: {thread_id}")

    # Step 1: Create and run agent
    print("\n🤖 Step 1: Creating and running agent...")
    try:
        engine = AugLLMConfig()
        agent = SimpleAgent(engine=engine, name="Verification Test Agent")

        # Run agent
        result = agent.run(
            {
                "messages": [
                    HumanMessage(
                        content="Hello Supabase! Please acknowledge this message."
                    )
                ]
            },
            config={"configurable": {"thread_id": thread_id}},
        )

        print("✅ Agent ran successfully")
        if "messages" in result and len(result["messages"]) > 1:
            print(f"   Response: {result['messages'][-1].content[:100]}...")
    except Exception as e:
        print(f"❌ Agent failed: {e}")
        return False

    # Step 2: Wait for writes to complete
    print("\n⏳ Step 2: Waiting for database writes...")
    await asyncio.sleep(3)

    # Step 3: Check Supabase
    print("\n🔍 Step 3: Checking Supabase for data...")

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ No POSTGRES_CONNECTION_STRING found")
        return False

    print(f"   Connection: ...{conn_string.split('@')[1].split(':')[0]}")

    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Check checkpoint_writes
                print("\n📊 Checking checkpoint_writes table:")
                await cur.execute(
                    """
                    SELECT COUNT(*), MIN(idx), MAX(idx) 
                    FROM checkpoint_writes 
                    WHERE thread_id = %s
                """,
                    (thread_id,),
                )

                write_count, min_idx, max_idx = await cur.fetchone()
                if write_count > 0:
                    print(
                        f"   ✅ Found {write_count} writes (idx range: {min_idx}-{max_idx})"
                    )

                    # Show some details
                    await cur.execute(
                        """
                        SELECT channel, type, idx 
                        FROM checkpoint_writes 
                        WHERE thread_id = %s 
                        ORDER BY idx 
                        LIMIT 5
                    """,
                        (thread_id,),
                    )

                    writes = await cur.fetchall()
                    for channel, write_type, idx in writes:
                        print(f"      - {channel}: {write_type} (idx: {idx})")
                else:
                    print("   ❌ No writes found")

                # Check checkpoints
                print("\n📊 Checking checkpoints table:")
                await cur.execute(
                    """
                    SELECT checkpoint_id, parent_checkpoint_id, type 
                    FROM checkpoints 
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id
                """,
                    (thread_id,),
                )

                checkpoints = await cur.fetchall()
                if checkpoints:
                    print(f"   ✅ Found {len(checkpoints)} checkpoints:")
                    for cp_id, parent_id, cp_type in checkpoints:
                        print(
                            f"      - {cp_id[:8]}... (parent: {parent_id[:8] if parent_id else 'None'}...)"
                        )
                else:
                    print("   ❌ No checkpoints found")

                # Check checkpoint_blobs
                print("\n📊 Checking checkpoint_blobs table:")
                await cur.execute(
                    """
                    SELECT channel, type, LENGTH(blob) as blob_size
                    FROM checkpoint_blobs 
                    WHERE thread_id = %s
                    LIMIT 5
                """,
                    (thread_id,),
                )

                blobs = await cur.fetchall()
                if blobs:
                    print(f"   ✅ Found checkpoint blobs:")
                    for channel, blob_type, size in blobs:
                        print(f"      - {channel}: {blob_type} ({size} bytes)")
                else:
                    print("   ❌ No blobs found")

                # Summary
                print("\n📈 Summary:")
                success = write_count > 0 or len(checkpoints) > 0
                if success:
                    print(f"   ✅ Data successfully written to Supabase!")
                    print(f"   Thread ID: {thread_id}")
                    print(f"   Writes: {write_count}")
                    print(f"   Checkpoints: {len(checkpoints)}")
                else:
                    print("   ❌ No data found in Supabase")

                return success

    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback

        traceback.print_exc()
        return False


async def check_database_status():
    """Check overall database status."""

    print("\n\n📊 Database Status Check")
    print("=" * 60)

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")

    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Check tables exist
                await cur.execute(
                    """
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name IN ('checkpoints', 'checkpoint_writes', 'checkpoint_blobs')
                    ORDER BY table_name
                """
                )

                tables = await cur.fetchall()
                print("✅ Found tables:")
                for table in tables:
                    print(f"   - {table[0]}")

                # Get counts
                for table_name in [
                    "checkpoint_writes",
                    "checkpoints",
                    "checkpoint_blobs",
                ]:
                    await cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = (await cur.fetchone())[0]
                    print(f"   {table_name}: {count} rows")

    except Exception as e:
        print(f"❌ Error checking database: {e}")


if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_and_verify())

    # Check database status
    asyncio.run(check_database_status())

    print("\n" + "=" * 60)
    if success:
        print("✅ SUCCESS: Supabase persistence is working!")
        print("\n🔗 View in Supabase dashboard:")
        print(
            "   https://supabase.com/dashboard/project/zkssazqhwcetsnbiuqik/editor/45942"
        )
    else:
        print("❌ FAILED: Data not being written to Supabase")
