#!/usr/bin/env python3
"""Decode and view checkpoint blob contents."""

import json
import os
from datetime import datetime

import msgpack
import psycopg


def decode_checkpoint_blobs(thread_id: str):
    """Decode and display checkpoint blob contents."""

    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Get message blobs
                cur.execute(
                    """
                    SELECT
                        version,
                        channel,
                        type,
                        blob
                    FROM public.checkpoint_blobs
                    WHERE thread_id = %s
                    AND channel = 'messages'
                    ORDER BY version DESC
                    LIMIT 4
                """,
                    (thread_id,),
                )

                blobs = cur.fetchall()

                for i, (version, channel, blob_type, blob_data) in enumerate(blobs):

                    if blob_type == "msgpack" and blob_data:
                        try:
                            # Decode msgpack
                            messages = msgpack.unpackb(
                                blob_data, raw=False, strict_map_key=False
                            )

                            if isinstance(messages, list):
                                for j, msg in enumerate(messages):
                                    if isinstance(msg, dict):
                                        msg_type = msg.get("type", "unknown")
                                        content = msg.get("content", "")[:100]
                                    else:
                                        pass
                        except Exception as e:
                            pass")
                    else:
                        pass

                # Also check the actual checkpoint data
                cur.execute(
                    """
                    SELECT
                        checkpoint_id,
                        checkpoint
                    FROM public.checkpoints
                    WHERE thread_id = %s
                    ORDER BY checkpoint_id DESC
                    LIMIT 1
                """,
                    (thread_id,),
                )

                result = cur.fetchone()
                if result:
                    cp_id, cp_data = result

                    # Parse checkpoint
                    cp_dict = (
                        json.loads(cp_data) if isinstance(cp_data, str) else cp_data
                    )

                    # Check structure
                    for key in cp_dict:
                        if key == "channel_values":
                            for channel in cp_dict[key]:
                                pass

    except Exception as e:
        import traceback

        traceback.print_exc()


def check_persistence_store_link():
    """Check store persistence linkage in detail."""

    # Find all store-related files
    store_dir = "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store"

    if os.path.exists(store_dir):
        for file in os.listdir(store_dir):
            if file.endswith(".py"):

                # Check if it imports ConnectionManager
                file_path = os.path.join(store_dir, file)
                try:
                    with open(file_path) as f:
                        content = f.read()

                    if "ConnectionManager" in content:
                        pass")
                    elif "connection" in content.lower():
                        passde")
                except:
                    pass
    else:
        pass")


def main():
    """Run checkpoint decoding tests."""
    import sys

    # Get thread ID from command line or use default
    if len(sys.argv) > 1:
        thread_id = sys.argv[1]
    else:
        # Use the most recent test thread
        thread_id = (
            f"msg_test_{datetime.now().strftime('%H%M%S')[:-2]}02"  # Guess recent
        )

    decode_checkpoint_blobs(thread_id)
    check_persistence_store_link()


if __name__ == "__main__":
    main()
