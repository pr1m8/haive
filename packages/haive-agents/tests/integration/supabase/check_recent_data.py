#!/usr/bin/env python3
"""Check recent data in Supabase to see if writes are happening."""

import asyncio
import os
from datetime import datetime, timedelta

import psycopg


async def check_recent_data():
    """Check for recent data in Supabase."""

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")

    try:
        async with await psycopg.AsyncConnection.connect(conn_string) as conn:
            async with conn.cursor() as cur:
                # Get recent checkpoint writes
                await cur.execute(
                    """
                    SELECT thread_id, COUNT(*) as write_count, MAX(idx) as max_idx
                    FROM checkpoint_writes
                    GROUP BY thread_id
                    ORDER BY max_idx DESC
                    LIMIT 10
                """
                )

                writes = await cur.fetchall()
                for thread_id, count, _max_idx in writes:
                    pass

                # Get test threads from today
                await cur.execute(
                    """
                    SELECT DISTINCT thread_id
                    FROM checkpoint_writes
                    WHERE thread_id LIKE '%test_%'
                    OR thread_id LIKE '%verify_%'
                    OR thread_id LIKE '%fresh_%'
                    OR thread_id LIKE '%final_%'
                    OR thread_id LIKE '%clean_%'
                    OR thread_id LIKE '%write_%'
                    ORDER BY thread_id DESC
                    LIMIT 20
                """
                )

                test_threads = await cur.fetchall()
                if test_threads:
                    for (thread,) in test_threads:
                        pass
                else:
                    pass

                # Check if our earlier test data is there
                specific_threads = [
                    "write_test_20250630_111828",
                    "final_test_20250630_112126",
                    "verify_test_20250630_113752_409717",
                ]

                for thread_id in specific_threads:
                    await cur.execute(
                        "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                        (thread_id,),
                    )
                    count = (await cur.fetchone())[0]
                    if count > 0:
                        pass")
                    else:
                        pass")

    except Exception as e:
        pass")


if __name__ == "__main__":
    asyncio.run(check_recent_data())
