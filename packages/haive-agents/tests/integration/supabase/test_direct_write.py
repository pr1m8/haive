#!/usr/bin/env python3
"""Direct test to verify Supabase writes."""

import asyncio
import os
from datetime import datetime

import psycopg


async def direct_write_test():
    """Test writing directly to Supabase."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return False


    thread_id = f"direct_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # Write some test data
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Insert a test checkpoint write
                await cur.execute(
                    """
                    INSERT INTO checkpoint_writes (thread_id, checkpoint_ns, checkpoint_id, task_id, idx, channel, type, blob)
                    VALUES (%s, '', '00000000-0000-0000-0000-000000000000', '00000000-0000-0000-0000-000000000000', 1, 'test', 'direct_test', %s)
                """,
                    (thread_id, b"test data"),
                )

                await conn.commit()

                # Verify it's there
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                    (thread_id,),
                )
                count = (await cur.fetchone())[0]

                return True

    except Exception as e:
        return False


async def check_tables():
    """Check table structure."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")

    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Check tables
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
                for (table,) in tables:
                    pass

                # Get row counts
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
    success = asyncio.run(direct_write_test())
    asyncio.run(check_tables())

    if success:
