#!/usr/bin/env python3
"""Clean up prepared statements and test again."""

import asyncio
import os
from datetime import datetime

import psycopg
from haive.core.engine.aug_llm import AugLLMConfig
from langchain_core.messages import HumanMessage

from haive.agents.simple.agent import SimpleAgent


async def cleanup_prepared_statements():
    """Clean up all prepared statements."""
    print("🧹 Cleaning up prepared statements...")

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Deallocate all prepared statements
                await cur.execute("DEALLOCATE ALL")
                print("✅ Cleaned up prepared statements")
    except Exception as e:
        print(f"⚠️  Could not clean up: {e}")


async def test_after_cleanup():
    """Test agent after cleanup."""

    # Clean up first
    await cleanup_prepared_statements()

    print("\n🧪 Testing After Cleanup")
    print("=" * 60)

    thread_id = f"cleaned_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"\n📝 Thread ID: {thread_id}")

    # Clear cached pools
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
        print("✅ Cleared cached pools")
    except:
        pass

    # Create agent
    print("\n🤖 Creating agent...")
    engine = AugLLMConfig()
    agent = SimpleAgent(engine=engine, name="Cleaned Agent")

    # Run agent
    print("\n💬 Running agent...")
    try:
        result = agent.run(
            {"messages": [HumanMessage(content="Test after cleanup.")]},
            config={"configurable": {"thread_id": thread_id}},
        )
        print("✅ Agent completed!")

        # Wait and verify
        await asyncio.sleep(2)

        conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                    (thread_id,),
                )
                count = (await cur.fetchone())[0]

                if count > 0:
                    print(f"\n✅ SUCCESS! Found {count} checkpoint writes!")
                    print(f"   Thread ID: {thread_id}")
                else:
                    print("\n❌ No data found")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(test_after_cleanup())
