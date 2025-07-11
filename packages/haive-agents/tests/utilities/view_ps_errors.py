#!/usr/bin/env python3
"""View prepared statement errors in metadata."""

import json
import os

import psycopg


def view_ps_errors():
    """View prepared statement errors from metadata."""
    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return

    try:
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
                # Find checkpoints with prepared statement errors
                cur.execute(
                    """
                    SELECT
                        thread_id,
                        checkpoint_id,
                        metadata
                    FROM public.checkpoints
                    WHERE metadata::text LIKE '%prepared statement%'
                    ORDER BY checkpoint_id DESC
                    LIMIT 3
                """
                )

                results = cur.fetchall()

                for thread_id, checkpoint_id, metadata in results:

                    try:
                        meta_dict = (
                            json.loads(metadata)
                            if isinstance(metadata, str)
                            else metadata
                        )

                        # Show step
                        if "step" in meta_dict:
                            pass

                        # Extract prepared statement errors
                        if "writes" in meta_dict:
                            for node_name, node_data in meta_dict["writes"].items():
                                if isinstance(node_data, dict):
                                    # Check process_response
                                    if "process_response" in node_data:
                                        pr = node_data["process_response"]
                                        if (
                                            isinstance(pr, dict)
                                            and "contributions" in pr
                                        ):
                                            for i, contrib in enumerate(
                                                pr["contributions"]
                                            ):
                                                if (
                                                    isinstance(contrib, list)
                                                    and len(contrib) >= 3
                                                ):
                                                    agent = contrib[0]
                                                    section = contrib[1]
                                                    content = str(contrib[2])
                                                    if (
                                                        "prepared statement"
                                                        in content.lower()
                                                    ):

                                    # Check error field
                                    if "error" in node_data:
                                        pass

                                    # Check messages for errors
                                    if "messages" in node_data:
                                        messages = node_data["messages"]
                                        if isinstance(messages, list):
                                            for msg in messages:
                                                if (
                                                    isinstance(msg, dict)
                                                    and "content" in msg
                                                ):
                                                    if (
                                                        "prepared statement"
                                                        in str(msg["content"]).lower()
                                                    ):
                                                        pass

                        # Check for error at top level
                        if "error" in meta_dict:
                            pass')

                    except Exception as e:
                        passe}")


                # Get stats on which agents have errors
                cur.execute(
                    """
                    SELECT
                        COUNT(DISTINCT thread_id) as unique_threads,
                        COUNT(*) as total_errors
                    FROM public.checkpoints
                    WHERE metadata::text LIKE '%prepared statement%'
                """
                )

                stats = cur.fetchone()

    except Exception as e:
        pass")


if __name__ == "__main__":
    view_ps_errors()
