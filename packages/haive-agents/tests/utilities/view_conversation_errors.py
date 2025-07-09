#!/usr/bin/env python3
"""Simple viewer to check conversation metadata for prepared statement errors."""

import json
import os

import psycopg2
from psycopg2.extras import RealDictCursor


def main():
    """View conversation errors in metadata."""
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    print("🔍 Checking metadata for prepared statement errors...")

    # Look for records with step 72 (from your example)
    cursor.execute(
        """
        SELECT 
            thread_id,
            metadata,
            checkpoint
        FROM checkpoints 
        WHERE metadata->>'step' = '72'
        LIMIT 5;
    """
    )

    step72_records = cursor.fetchall()
    print(f"\n📊 Found {len(step72_records)} records at step 72:")

    for record in step72_records:
        print(f"\nThread: {record['thread_id']}")

        # Check metadata writes
        metadata = record["metadata"]
        if metadata and "writes" in metadata:
            writes = metadata["writes"]
            if "process_response" in writes:
                process_response = writes["process_response"]
                if process_response and "contributions" in process_response:
                    contributions = process_response["contributions"]
                    print(f"  Contributions found: {len(contributions)}")

                    # Look for prepared statement errors
                    for contrib in contributions[:5]:  # First 5
                        if len(contrib) >= 3:
                            agent, section, content = contrib[0], contrib[1], contrib[2]
                            if "prepared statement" in content:
                                print(f"    ❌ {agent} -> {section}: {content}")
                            elif "Error" in content:
                                print(f"    ⚠️  {agent} -> {section}: {content[:50]}...")

    # Also look for any records with "prepared statement" in text
    cursor.execute(
        """
        SELECT 
            thread_id,
            metadata->>'step' as step,
            checkpoint
        FROM checkpoints 
        WHERE checkpoint::text ILIKE '%prepared statement%'
        LIMIT 3;
    """
    )

    ps_records = cursor.fetchall()
    print(f"\n🔍 Found {len(ps_records)} records with 'prepared statement' text:")

    for record in ps_records:
        print(f"\nThread: {record['thread_id']}, Step: {record['step']}")
        checkpoint = record["checkpoint"]

        # Extract relevant parts that contain errors
        if isinstance(checkpoint, dict):
            # Look in channel_values
            if "channel_values" in checkpoint:
                values = checkpoint["channel_values"]
                for key, value in values.items():
                    if isinstance(value, str) and "prepared statement" in value:
                        print(f"  Found in {key}: {value[:100]}...")
                    elif (
                        key == "shared_document"
                        and isinstance(value, str)
                        and "prepared statement" in value
                    ):
                        print(f"  Found in shared_document: {value[:100]}...")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
