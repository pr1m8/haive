#!/usr/bin/env python3
"""Simple viewer to check conversation metadata for prepared statement errors."""

import os

import psycopg2
from psycopg2.extras import RealDictCursor


def main():
    """View conversation errors in metadata."""
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    conn = psycopg2.connect(conn_str)
    cursor = conn.cursor(cursor_factory=RealDictCursor)


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

    for record in step72_records:

        # Check metadata writes
        metadata = record["metadata"]
        if metadata and "writes" in metadata:
            writes = metadata["writes"]
            if "process_response" in writes:
                process_response = writes["process_response"]
                if process_response and "contributions" in process_response:
                    contributions = process_response["contributions"]

                    # Look for prepared statement errors
                    for contrib in contributions[:5]:  # First 5
                        if len(contrib) >= 3:
                            agent, section, content = contrib[0], contrib[1], contrib[2]
                            if "prepared statement" in content:
                                pass")
                            elif "Error" in content:
                                pass..")

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

    for record in ps_records:
        checkpoint = record["checkpoint"]

        # Extract relevant parts that contain errors
        if isinstance(checkpoint, dict):
            # Look in channel_values
            if "channel_values" in checkpoint:
                values = checkpoint["channel_values"]
                for key, value in values.items():
                    if isinstance(value, str) and "prepared statement" in value:
                        pass
                    elif (
                        key == "shared_document"
                        and isinstance(value, str)
                        and "prepared statement" in value
                    ):
                        pass

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
