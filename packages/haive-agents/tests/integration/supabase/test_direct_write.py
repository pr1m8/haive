#!/usr/bin/env python3
"""Direct test to verify Supabase writes."""

import asyncio
import os
from datetime import datetime

import psycopg


async def direct_write_test():
    """Test writing directly to Supabase."""

    print("🧪 Direct Supabase Write Test")
    print("=" * 60)

    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ No connection string")
        return False

    print(f"✅ Using Supabase: {'supabase.com' in conn_string}")

    thread_id = f"direct_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    print(f"📝 Thread ID: {thread_id}")

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
                print("✅ Direct write successful!")

                # Verify it's there
                await cur.execute(
                    "SELECT COUNT(*) FROM checkpoint_writes WHERE thread_id = %s",
                    (thread_id,),
                )
                count = (await cur.fetchone())[0]
                print(f"✅ Verified: {count} row(s) written")

                return True

    except Exception as e:
        print(f"❌ Error: {e}")
        return False


async def check_tables():
    """Check table structure."""

    print("\n📊 Checking Supabase Tables")
    print("=" * 60)

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
                print("✅ Found tables:")
                for (table,) in tables:
                    print(f"   - {table}")

                # Get row counts
                for table_name in [
                    "checkpoint_writes",
                    "checkpoints",
                    "checkpoint_blobs",
                ]:
                    await cur.execute(f"SELECT COUNT(*) FROM {table_name}")
                    count = (await cur.fetchone())[0]
                    print(f"   {table_name}: {count} total rows")

    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    success = asyncio.run(direct_write_test())
    asyncio.run(check_tables())

    if success:
        print("\n✅ Supabase is accessible and writable!")
        print(
            "🔗 https://supabase.com/dashboard/project/zkssazqhwcetsnbiuqik/editor/45942"
        )
