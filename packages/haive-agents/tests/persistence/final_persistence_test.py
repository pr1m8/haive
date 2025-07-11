#!/usr/bin/env python3
"""Final comprehensive test of PostgreSQL persistence fixes."""

import json
import os
import sys
from datetime import datetime

import psycopg

# Add paths
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-agents/src")


def check_prepared_statements():
    """Check current prepared statements."""
    conn_string = os.environ.get("POSTGRES_CONNECTION_STRING")
    if not conn_string:
        return -1

    try:
        with psycopg.connect(conn_string) as conn, conn.cursor() as cur:
            cur.execute(
                """
                    SELECT COUNT(*) 
                    FROM pg_prepared_statements 
                    WHERE name LIKE '%pg%'
                """
            )
            return cur.fetchone()[0]
    except:
        return -1


def test_persistence_fixes():
    """Test all persistence fixes."""

    # Initial check
    initial_ps = check_prepared_statements()

    # Test 1: Simple agent
    try:
        from langchain_core.messages import HumanMessage

        from haive.agents.simple.agent import SimpleAgent

        agent = SimpleAgent(
            name="FinalTestSimple",
            persistence=True,
        )
        agent.compile()

        result = agent.invoke(
            {"messages": [HumanMessage(content="Test message")]},
            {"configurable": {"thread_id": "final_test_simple"}},
        )

    except Exception as e:
        pass")

    # Test 2: Conversation agent
    try:
        from haive.agents.conversation.collaberative.agent import (
            CollaborativeConversation,
        )
        from haive.core.engine.aug_llm import AugLLMConfig

        participants = {
            "TestA": AugLLMConfig(name="TestA", system_message="Test A"),
            "TestB": AugLLMConfig(name="TestB", system_message="Test B"),
        }

        agent = CollaborativeConversation(
            name="FinalTestCollab",
            participant_agents=participants,
            topic="Final test",
            sections=["Test"],
            max_rounds=1,
            persistence=True,
        )
        agent.compile()

        agent.invoke(
            {"messages": [], "topic": "Final test", "format": "outline"},
            {"configurable": {"thread_id": "final_test_collab"}},
        )

    except Exception as e:
        pass")

    # Check for new prepared statements
    final_ps = check_prepared_statements()

    if final_ps > initial_ps:
        pass")
    else:
        pass")

    # Check configurations

    # Check ConnectionManager
    try:

        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py",
        ) as f:
            content = f.read()

        if '"prepare_threshold": None' in content:
            pass")
        else:
            pass")
    except Exception as e:
        pass")

    # Check persistence mixin
    try:

        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py",
        ) as f:
            content = f.read()

        if "prepare_threshold=None" in content:
            pass")
        else:
            pass")
    except Exception as e:
        pass")



if __name__ == "__main__":
    test_persistence_fixes()
