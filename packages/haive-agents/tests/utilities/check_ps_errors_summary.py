#!/usr/bin/env python3
"""Summary of prepared statement errors in checkpoints."""

import os

import psycopg


def check_ps_errors():
    """Check prepared statement errors summary."""
    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return


    with psycopg.connect(conn_string) as conn, conn.cursor() as cur:
        # Total with PS errors
        cur.execute(
            """
                SELECT COUNT(DISTINCT thread_id) as threads, COUNT(*) as total
                FROM public.checkpoints
                WHERE metadata::text LIKE %s
            """,
            ("%prepared statement%",),
        )

        threads_with_errors, total_errors = cur.fetchone()

        print(f"\n📊 Overall Statistics:")
        print(f"   Threads with PS errors: {threads_with_errors}")
        print(f"   Total error checkpoints: {total_errors}")

        # Get specific threads with errors
        cur.execute(
            """
                SELECT DISTINCT thread_id
                FROM public.checkpoints
                WHERE metadata::text LIKE %s
                ORDER BY thread_id
            """,
            ("%prepared statement%",),
        )

        error_threads = [row[0] for row in cur.fetchall()]

        # Categorize by type
        test_threads = [t for t in error_threads if "test" in t]
        agent_threads = [t for t in error_threads if "agent" in t]
        other_threads = [
            t
            for t in error_threads
            if t not in test_threads and t not in agent_threads
        ]

        print(f"\n📋 Threads with errors by category:")
        print(f"   Test threads: {len(test_threads)}")
        print(f"   Agent threads: {len(agent_threads)}")
        print(f"   Other threads: {len(other_threads)}")

        # Show some examples
        print(f"\n❌ Example threads with PS errors:")
        for t in error_threads[:10]:
            print(f"   - {t}")

        # Check recent test threads without errors
        cur.execute(
            """
                SELECT DISTINCT thread_id
                FROM public.checkpoints
                WHERE thread_id LIKE %s
                AND thread_id NOT IN (
                    SELECT DISTINCT thread_id
                    FROM public.checkpoints
                    WHERE metadata::text LIKE %s
                )
                ORDER BY thread_id DESC
                LIMIT 10
            """,
            ("%test%", "%prepared statement%"),
        )

        clean_threads = [row[0] for row in cur.fetchall()]

        print(f"\n✅ Recent test threads WITHOUT PS errors:")
        for t in clean_threads:
            print(f"   - {t}")

        # Summary
        print(f"\n📊 Summary:")
        print(f"   Total threads with errors: {threads_with_errors}")
        print(f"   Clean test threads found: {len(clean_threads)}")

        if len(clean_threads) > 0:
            print(f"\n✅ SUCCESS: Recent test threads are clean!")
        else:
            print(f"\n⚠️  WARNING: No clean test threads found")nd")


if __name__ == "__main__":
    check_ps_errors()
