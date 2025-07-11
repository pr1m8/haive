#!/usr/bin/env python3
"""Supabase metadata viewer utility for monitoring conversation agent errors."""

import json
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

import psycopg2
from psycopg2.extras import RealDictCursor


def get_database_connection():
    """Get database connection."""
    conn_str = os.getenv("POSTGRES_CONNECTION_STRING")
    if not conn_str:
        raise ValueError("POSTGRES_CONNECTION_STRING environment variable not found")
    return psycopg2.connect(conn_str)


def view_recent_errors(limit: int = 10) -> list[dict[str, Any]]:
    """View recent prepared statement errors from checkpoints metadata."""
    conn = get_database_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Search for prepared statement errors in metadata and checkpoint data
        cursor.execute(
            """
            SELECT
                thread_id,
                checkpoint_id,
                metadata->>'step' as step,
                metadata->>'source' as source,
                metadata->'writes' as writes,
                checkpoint->'channel_values' as channel_values
            FROM checkpoints
            WHERE (
                checkpoint::text ILIKE '%prepared statement%'
                OR checkpoint::text ILIKE '%_pg3_%'
            )
            ORDER BY checkpoint_id DESC
            LIMIT %s;
        """,
            (limit,),
        )

        results = cursor.fetchall()

        errors = []
        for row in results:
            error_info = {
                "thread_id": row["thread_id"],
                "checkpoint_id": row["checkpoint_id"],
                "step": row["step"],
                "source": row["source"],
                "errors_found": [],
            }

            # Check writes for errors
            if row["writes"]:
                writes = row["writes"]
                if isinstance(writes, dict):
                    for write_key, write_data in writes.items():
                        if isinstance(write_data, dict):
                            for key, value in write_data.items():
                                if (
                                    isinstance(value, str | list)
                                    and "prepared statement" in str(value).lower()
                                ):
                                    error_info["errors_found"].append(
                                        {
                                            "location": f"writes.{write_key}.{key}",
                                            "error": (
                                                str(value)[:200] + "..."
                                                if len(str(value)) > 200
                                                else str(value)
                                            ),
                                        }
                                    )

            # Check channel_values for errors
            if row["channel_values"]:
                channel_values = row["channel_values"]
                if isinstance(channel_values, dict):
                    for key, value in channel_values.items():
                        if (
                            isinstance(value, str | list)
                            and "prepared statement" in str(value).lower()
                        ):
                            error_info["errors_found"].append(
                                {
                                    "location": f"channel_values.{key}",
                                    "error": (
                                        str(value)[:200] + "..."
                                        if len(str(value)) > 200
                                        else str(value)
                                    ),
                                }
                            )
                        elif key == "contributions" and isinstance(value, list):
                            # Check contributions for errors
                            for i, contrib in enumerate(value):
                                if isinstance(contrib, list) and len(contrib) >= 3:
                                    agent_name, section, content = (
                                        contrib[0],
                                        contrib[1],
                                        contrib[2],
                                    )
                                    if "prepared statement" in str(content).lower():
                                        error_info["errors_found"].append(
                                            {
                                                "location": f"contributions[{i}]",
                                                "agent": agent_name,
                                                "section": section,
                                                "error": content,
                                            }
                                        )

            if error_info["errors_found"]:
                errors.append(error_info)

        return errors

    finally:
        cursor.close()
        conn.close()


def view_conversation_threads(limit: int = 20) -> list[dict[str, Any]]:
    """View recent conversation threads and their status."""
    conn = get_database_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        cursor.execute(
            """
            SELECT
                thread_id,
                COUNT(*) as checkpoint_count,
                MAX(CAST(metadata->>'step' AS INTEGER)) as max_step,
                MIN(checkpoint_id) as first_checkpoint,
                MAX(checkpoint_id) as last_checkpoint,
                COUNT(CASE WHEN checkpoint::text ILIKE '%error%' THEN 1 END) as error_count
            FROM checkpoints
            WHERE (
                thread_id ILIKE '%conversation%'
                OR thread_id ILIKE '%collaborative%'
                OR thread_id ILIKE '%agent%'
                OR metadata::text ILIKE '%ProductManager%'
                OR metadata::text ILIKE '%Designer%'
                OR metadata::text ILIKE '%Engineer%'
                OR metadata::text ILIKE '%Marketer%'
            )
            GROUP BY thread_id
            ORDER BY last_checkpoint DESC
            LIMIT %s;
        """,
            (limit,),
        )

        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_thread_details(thread_id: str) -> dict[str, Any]:
    """Get detailed information about a specific thread."""
    conn = get_database_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Get thread overview
        cursor.execute(
            """
            SELECT
                COUNT(*) as total_checkpoints,
                MAX(CAST(metadata->>'step' AS INTEGER)) as max_step,
                MIN(checkpoint_id) as first_checkpoint,
                MAX(checkpoint_id) as last_checkpoint
            FROM checkpoints
            WHERE thread_id = %s;
        """,
            (thread_id,),
        )

        overview = cursor.fetchone()

        # Get recent checkpoints
        cursor.execute(
            """
            SELECT
                checkpoint_id,
                metadata->>'step' as step,
                metadata->>'source' as source,
                metadata->'writes' as writes
            FROM checkpoints
            WHERE thread_id = %s
            ORDER BY checkpoint_id DESC
            LIMIT 10;
        """,
            (thread_id,),
        )

        recent_checkpoints = cursor.fetchall()

        # Check for errors
        cursor.execute(
            """
            SELECT COUNT(*) as error_count
            FROM checkpoints
            WHERE thread_id = %s
            AND (
                checkpoint::text ILIKE '%error%'
                OR metadata::text ILIKE '%error%'
            );
        """,
            (thread_id,),
        )

        error_count = cursor.fetchone()["error_count"]

        return {
            "thread_id": thread_id,
            "overview": dict(overview) if overview else {},
            "recent_checkpoints": [dict(cp) for cp in recent_checkpoints],
            "error_count": error_count,
        }

    finally:
        cursor.close()
        conn.close()


def test_conversation_agent_with_new_id():
    """Test conversation agent with a fresh thread ID to verify prepared statement fix."""
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src"
    )
    sys.path.insert(
        0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src"
    )

    try:
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.collaberative.agent import (
            CollaborativeConversation,
        )

        # Create fresh participant agents with unique names
        timestamp = datetime.now().strftime("%H%M%S")
        participants = {
            f"TestPM_{timestamp}": AugLLMConfig(
                name=f"TestPM_{timestamp}",
                system_message="You are a test product manager. Give very brief responses.",
            ),
            f"TestDev_{timestamp}": AugLLMConfig(
                name=f"TestDev_{timestamp}",
                system_message="You are a test developer. Give very brief responses.",
            ),
        }

        # Create agent with fresh ID and persistence
        agent = CollaborativeConversation(
            name=f"TestCollab_{timestamp}",
            participant_agents=participants,
            topic="Quick prepared statement test",
            sections=["Problem", "Solution"],  # Keep it minimal
            max_rounds=2,  # Very short test
            persistence=True,
        )

        agent.compile()

        # Use completely fresh thread ID
        fresh_thread_id = f"fresh_test_{timestamp}_{datetime.now().microsecond}"
        config = {"configurable": {"thread_id": fresh_thread_id}}


        test_input = {
            "messages": [],
            "topic": "Quick prepared statement test",
            "format": "outline",
        }

        result = agent.invoke(test_input, config)


        # Check result for errors
        if hasattr(result, "shared_document"):
            doc = result.shared_document
            if "prepared statement" in str(doc).lower():
                return fresh_thread_id, False
            print("✅ No prepared statement errors in result")
            return fresh_thread_id, True

        return fresh_thread_id, True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return None, False


def main():
    """Main function to run the metadata viewer."""

    try:
        # View recent errors

        errors = view_recent_errors(limit=5)
        if errors:
            for i, error in enumerate(errors, 1):

                for err in error["errors_found"][:3]:  # Show first 3 errors
                    pass
        else:
            pass")

        # View conversation threads

        threads = view_conversation_threads(limit=10)
        for thread in threads:
            status = "❌ HAS ERRORS" if thread["error_count"] > 0 else "✅ Clean"

        # Test with new thread ID

        fresh_thread_id, success = test_conversation_agent_with_new_id()

        if fresh_thread_id and success:
            details = get_thread_details(fresh_thread_id)


            if details["error_count"] == 0:
                pass")
            else:
                pass")

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
