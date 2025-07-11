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
except:
    pass


async def test_and_verify():
    """Test agent and verify data in Supabase."""

    # Create unique thread ID
    thread_id = f"verify_test_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

    # Step 1: Create and run agent
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

        if "messages" in result and len(result["messages"]) > 1:
            pass
    except Exception as e:
        return False

    # Step 2: Wait for writes to complete
    await asyncio.sleep(3)

    # Step 3: Check Supabase

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return False


    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Check checkpoint_writes
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
                        pass
                else:
                    pass")

                # Check checkpoints
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
                    for cp_id, parent_id, _cp_type in checkpoints:
                        pass
                else:
                    pass")

                # Check checkpoint_blobs
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
                    for channel, blob_type, size in blobs:
                        pass
                else:
                    pass")

                # Summary
                success = write_count > 0 or len(checkpoints) > 0
                if success:
                else:
                    pass")

                return success

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


async def check_database_status():
    """Check overall database status."""

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
                for table in tables:
                    pass

                # Get counts
                for table_name in [
                    "checkpoint_writes",
                    "checkpoints",
                    "checkpoint_blobs",
                ]:
                    await cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = (await cur.fetchone())[0]

    except Exception as e:
        pass")


if __name__ == "__main__":
    # Run the test
    success = asyncio.run(test_and_verify())

    # Check database status
    asyncio.run(check_database_status())

    if success:
    else:
        pass")
