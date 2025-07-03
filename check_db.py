#!/usr/bin/env python3
"""Check what's in the database."""

import os
import psycopg2
from datetime import datetime, timedelta

def check_database():
    """Check database contents."""
    conn_string = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ No connection string")
        return
    
    try:
        with psycopg2.connect(conn_string) as conn:
            with conn.cursor() as cursor:
                # List all tables
                print("=== Database Tables ===")
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                tables = cursor.fetchall()
                for table in tables:
                    print(f"   📋 {table[0]}")
                
                # Check threads table
                print(f"\n=== Threads Table ===")
                cursor.execute("SELECT COUNT(*) FROM threads")
                thread_count = cursor.fetchone()[0]
                print(f"   Total threads: {thread_count}")
                
                if thread_count > 0:
                    cursor.execute("""
                        SELECT thread_id, created_at, last_access
                        FROM threads 
                        ORDER BY last_access DESC 
                        LIMIT 5
                    """)
                    recent_threads = cursor.fetchall()
                    print(f"\n   Recent threads:")
                    for thread in recent_threads:
                        print(f"   - {thread[0][:50]}... (last: {thread[2].strftime('%H:%M:%S')})")
                
                # Check checkpoints table
                print(f"\n=== Checkpoints Table ===")
                cursor.execute("SELECT COUNT(*) FROM checkpoints")
                checkpoint_count = cursor.fetchone()[0]
                print(f"   Total checkpoints: {checkpoint_count}")
                
                if checkpoint_count > 0:
                    cursor.execute("""
                        SELECT thread_id, checkpoint_id, created_at
                        FROM checkpoints 
                        ORDER BY created_at DESC 
                        LIMIT 5
                    """)
                    recent_checkpoints = cursor.fetchall()
                    print(f"\n   Recent checkpoints:")
                    for cp in recent_checkpoints:
                        print(f"   - Thread: {cp[0][:30]}... ID: {cp[1]} (at: {cp[2].strftime('%H:%M:%S')})")
                
                # Check recent activity (last hour)
                print(f"\n=== Recent Activity (last hour) ===")
                one_hour_ago = datetime.now() - timedelta(hours=1)
                
                cursor.execute("""
                    SELECT COUNT(*) FROM threads 
                    WHERE last_access > %s
                """, (one_hour_ago,))
                recent_thread_activity = cursor.fetchone()[0]
                print(f"   Active threads: {recent_thread_activity}")
                
                cursor.execute("""
                    SELECT COUNT(*) FROM checkpoints 
                    WHERE created_at > %s
                """, (one_hour_ago,))
                recent_checkpoint_activity = cursor.fetchone()[0]
                print(f"   New checkpoints: {recent_checkpoint_activity}")
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_database()