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


                for cp in checkpoints:
                    thread_id = cp[0]
                    checkpoint_ns = cp[1]
                    checkpoint_id = cp[2]
                    parent_id = cp[3]
                    cp_type = cp[4]
                    cp[5]
                    metadata = cp[6]


                    # Parse and display metadata
                    if metadata:
                        try:
                            meta_dict = (
                                json.loads(metadata)
                                if isinstance(metadata, str)
                                else metadata
                            )

                            # Check for step number
                            if "step" in meta_dict:
                                pass

                            # Check for langgraph metadata
                            if "langgraph_node" in meta_dict:
                                pass
                            if "langgraph_triggers" in meta_dict:
                                pass
                            if "langgraph_checkpoint_ns" in meta_dict:
                                pass

                            # Check for writes (where errors might be)
                            if "writes" in meta_dict:
                                writes = meta_dict["writes"]

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
                                                    elif "error" in content.lower():
                                                        error_count += 1

                                            if error_count == 0:
                                                pass

                            # Check for errors in metadata
                            if "error" in meta_dict:
                                pass")

                            # Show other keys
                            other_keys = [
                                k
                                for k in meta_dict
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
                                pass

                        except Exception as e:
                    else:
                        passa")


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


    except Exception as e:
        pass")


if __name__ == "__main__":
    view_metadata_details()
