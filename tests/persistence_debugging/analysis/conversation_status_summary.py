#!/usr/bin/env python3
"""Simple summary of conversation agent status and errors."""

import os

import psycopg2
from psycopg2.extras import RealDictCursor


def main():
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    # Check threads with prepared statement errors
    cursor.execute(
        """
        SELECT
            thread_id,
            COUNT(*) as error_checkpoints
        FROM checkpoints
        WHERE checkpoint::text ILIKE '%prepared statement%'
        GROUP BY thread_id
        ORDER BY error_checkpoints DESC;
    """
    )

    error_threads = cursor.fetchall()
    for thread in error_threads:
        pass

    # Check recent threads (last 24 hours worth)
    cursor.execute(
        """
        SELECT
            thread_id,
            COUNT(*) as total_checkpoints,
            MAX(CAST(metadata->>'step' AS INTEGER)) as max_step,
            MAX(checkpoint_id) as latest_checkpoint
        FROM checkpoints
        WHERE checkpoint_id::text > (
            SELECT checkpoint_id::text
            FROM checkpoints
            ORDER BY checkpoint_id::text DESC
            OFFSET 200 LIMIT 1
        )
        AND (
            thread_id ILIKE '%conversation%'
            OR thread_id ILIKE '%collab%'
            OR thread_id ILIKE '%test%'
        )
        GROUP BY thread_id
        ORDER BY latest_checkpoint DESC
        LIMIT 10;
    """
    )

    recent_threads = cursor.fetchall()
    for thread in recent_threads:
        # Check if this thread has errors
        cursor.execute(
            """
            SELECT COUNT(*) as error_count
            FROM checkpoints
            WHERE thread_id = %s
            AND checkpoint::text ILIKE '%prepared statement%';
        """,
            (thread["thread_id"],),
        )

        cursor.fetchone()["error_count"]

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
