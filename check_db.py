#!/usr/bin/env python3
"""Check what's in the database."""

import os
from datetime import datetime, timedelta

import psycopg2


def check_database():
    """Check database contents."""
    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                # List all tables
                cursor.execute(
                    """
                    SELECT table_name
                    FROM information_schema.tables
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """
                )
                tables = cursor.fetchall()
                for table in tables:
                    pass}")

                # Check threads table
                cursor.execute("SELECT COUNT(*) FROM threads")
                thread_count = cursor.fetchone()[0]

                if thread_count > 0:
                    cursor.execute(
                        """
                        SELECT thread_id, created_at, last_access
                        FROM threads
                        ORDER BY last_access DESC
                        LIMIT 5
                    """
                    )
                    recent_threads = cursor.fetchall()
                    for thread in recent_threads:
                        pass

                # Check checkpoints table
                cursor.execute("SELECT COUNT(*) FROM checkpoints")
                checkpoint_count = cursor.fetchone()[0]

                if checkpoint_count > 0:
                    cursor.execute(
                        """
                        SELECT thread_id, checkpoint_id, created_at
                        FROM checkpoints
                        ORDER BY created_at DESC
                        LIMIT 5
                    """
                    )
                    recent_checkpoints = cursor.fetchall()
                    for cp in recent_checkpoints:
                        pass

                # Check recent activity (last hour)
                one_hour_ago = datetime.now() - timedelta(hours=1)

                cursor.execute(
                    """
                    SELECT COUNT(*) FROM threads
                    WHERE last_access > %s
                """,
                    (one_hour_ago,),
                )
                recent_thread_activity = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT COUNT(*) FROM checkpoints
                    WHERE created_at > %s
                """,
                    (one_hour_ago,),
                )
                recent_checkpoint_activity = cursor.fetchone()[0]

    except Exception as e:
        pass")


if __name__ == "__main__":
    check_database()
