#!/usr/bin/env python3
"""Test if prepared statement issues are truly fixed."""

import os
import sys
from datetime import datetime

import psycopg

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def check_prepared_statements():
    """Check if any prepared statements exist in the database."""
    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return None

    try:
        with psycopg.connect(conn_string) as conn, conn.cursor() as cur:
            # Check for prepared statements
            cur.execute(
                """
                    SELECT name, statement, prepare_time, parameter_types
                    FROM pg_prepared_statements
                    WHERE name LIKE '%pg%'
                    ORDER BY prepare_time DESC
                """
            )

            prepared_stmts = cur.fetchall()

            if prepared_stmts:
                print(f"\n❌ Found {len(prepared_stmts)} prepared statements:")
                for name, stmt, prep_time, params in prepared_stmts:
                    print(f"\n  Name: {name}")
                    print(f"  Statement: {stmt[:100]}...")
                    print(f"  Prepared at: {prep_time}")
                    print(f"  Parameters: {params}")
            else:
                print("\n✅ No prepared statements found!")

            return len(prepared_stmts)

    except Exception as e:
        return -1


def test_conversation_agent():
    """Test a conversation agent to see if it creates prepared statements."""

    from haive.agents.conversation.collaberative.agent import CollaborativeConversation
    from haive.core.engine.aug_llm import AugLLMConfig

    timestamp = datetime.now().strftime("%H%M%S")

    # Check before
    before_count = check_prepared_statements()

    # Create and run agent
    participants = {
        f"TestA_{timestamp}": AugLLMConfig(
            name=f"TestA_{timestamp}",
            system_message="You are test agent A.",
        ),
        f"TestB_{timestamp}": AugLLMConfig(
            name=f"TestB_{timestamp}",
            system_message="You are test agent B.",
        ),
    }

    agent = CollaborativeConversation(
        name=f"TestCollab_{timestamp}",
        participant_agents=participants,
        topic="Testing prepared statements",
        sections=["Test"],
        max_rounds=1,
        persistence=True,
    )

    agent.compile()

    thread_id = f"ps_test_{timestamp}"
    config = {"configurable": {"thread_id": thread_id}}

    agent.invoke(
        {"messages": [], "topic": "Testing prepared statements", "format": "outline"},
        config,
    )

    # Check after
    after_count = check_prepared_statements()

    if after_count > before_count:
        return False
    print(f"\n✅ SUCCESS: No new prepared statements created!")
    return True


def main():
    """Run prepared statement tests."""

    # Initial check
    initial_count = check_prepared_statements()

    # Test conversation agent
    success = test_conversation_agent()

    # Final check
    final_count = check_prepared_statements()

    # Summary

    if final_count > initial_count:


if __name__ == "__main__":
    main()
