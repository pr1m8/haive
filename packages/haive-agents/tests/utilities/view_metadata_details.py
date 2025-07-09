#!/usr/bin/env python3
"""View detailed metadata from PostgreSQL checkpoints table."""

import json
import os
from datetime import datetime

import psycopg


def view_metadata_details():
    """View detailed metadata from checkpoints."""
    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        print("❌ POSTGRES_CONNECTION_STRING not set")
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Get recent checkpoints with metadata
                cur.execute(
                    """
                    SELECT 
                        thread_id,
                        checkpoint_ns,
                        checkpoint_id,
                        parent_checkpoint_id,
                        type,
                        checkpoint,
                        metadata
                    FROM public.checkpoints
                    WHERE thread_id LIKE '%test_%'
                    ORDER BY checkpoint_id DESC
                    LIMIT 20
                """
                )

                checkpoints = cur.fetchall()

                print(f"\n📊 Test Checkpoints Found: {len(checkpoints)}")
                print("=" * 80)

                for cp in checkpoints:
                    thread_id = cp[0]
                    checkpoint_ns = cp[1]
                    checkpoint_id = cp[2]
                    parent_id = cp[3]
                    cp_type = cp[4]
                    checkpoint_data = cp[5]
                    metadata = cp[6]

                    print(f"\n🔍 Thread: {thread_id}")
                    print(f"   Checkpoint ID: {checkpoint_id}")
                    print(f"   Parent ID: {parent_id}")
                    print(f"   Type: {cp_type}")
                    print(f"   Namespace: {checkpoint_ns}")

                    # Parse and display metadata
                    if metadata:
                        print("\n   📋 METADATA:")
                        try:
                            meta_dict = (
                                json.loads(metadata)
                                if isinstance(metadata, str)
                                else metadata
                            )

                            # Check for step number
                            if "step" in meta_dict:
                                print(f"      Step: {meta_dict['step']}")

                            # Check for langgraph metadata
                            if "langgraph_node" in meta_dict:
                                print(f"      Node: {meta_dict['langgraph_node']}")
                            if "langgraph_triggers" in meta_dict:
                                print(
                                    f"      Triggers: {meta_dict['langgraph_triggers']}"
                                )
                            if "langgraph_checkpoint_ns" in meta_dict:
                                print(
                                    f"      LG Namespace: {meta_dict['langgraph_checkpoint_ns']}"
                                )

                            # Check for writes (where errors might be)
                            if "writes" in meta_dict:
                                writes = meta_dict["writes"]
                                print(
                                    f"      Writes: {list(writes.keys()) if isinstance(writes, dict) else 'present'}"
                                )

                                # Look for process_response in writes
                                for node_name, node_data in writes.items():
                                    if (
                                        isinstance(node_data, dict)
                                        and "process_response" in node_data
                                    ):
                                        process_resp = node_data["process_response"]
                                        if (
                                            isinstance(process_resp, dict)
                                            and "contributions" in process_resp
                                        ):
                                            contribs = process_resp["contributions"]
                                            print(
                                                f"      → {node_name} has {len(contribs)} contributions"
                                            )

                                            # Check for errors in contributions
                                            error_count = 0
                                            for contrib in contribs:
                                                if (
                                                    isinstance(contrib, list)
                                                    and len(contrib) >= 3
                                                ):
                                                    content = str(contrib[2])
                                                    if (
                                                        "prepared statement"
                                                        in content.lower()
                                                    ):
                                                        error_count += 1
                                                        print(
                                                            f"         ❌ Prepared statement error from {contrib[0]}"
                                                        )
                                                    elif "error" in content.lower():
                                                        error_count += 1
                                                        print(
                                                            f"         ❌ Error from {contrib[0]}: {content[:50]}..."
                                                        )

                                            if error_count == 0:
                                                print(
                                                    f"         ✅ No errors in contributions"
                                                )

                            # Check for errors in metadata
                            if "error" in meta_dict:
                                print(f"      ❌ ERROR: {meta_dict['error']}")

                            # Show other keys
                            other_keys = [
                                k
                                for k in meta_dict.keys()
                                if k
                                not in [
                                    "step",
                                    "langgraph_node",
                                    "langgraph_triggers",
                                    "langgraph_checkpoint_ns",
                                    "writes",
                                    "error",
                                ]
                            ]
                            if other_keys:
                                print(f"      Other keys: {other_keys[:5]}...")

                        except Exception as e:
                            print(f"      ⚠️  Error parsing metadata: {e}")
                            print(f"      Raw metadata type: {type(metadata)}")
                    else:
                        print("   📋 No metadata")

                    print("-" * 80)

                # Get summary stats
                cur.execute(
                    """
                    SELECT 
                        COUNT(*) as total,
                        COUNT(DISTINCT thread_id) as unique_threads,
                        COUNT(CASE WHEN metadata::text LIKE '%prepared statement%' THEN 1 END) as ps_errors,
                        COUNT(CASE WHEN metadata::text LIKE '%error%' THEN 1 END) as total_errors
                    FROM public.checkpoints
                    WHERE thread_id LIKE '%test_%'
                """
                )

                stats = cur.fetchone()

                print(f"\n📊 SUMMARY STATS (Test Threads):")
                print(f"   Total checkpoints: {stats[0]}")
                print(f"   Unique threads: {stats[1]}")
                print(f"   Prepared statement errors: {stats[2]}")
                print(f"   Total errors: {stats[3]}")

    except Exception as e:
        print(f"❌ Database error: {e}")


if __name__ == "__main__":
    view_metadata_details()
