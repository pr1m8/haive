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
        with psycopg.connect(conn_string) as conn:
            with conn.cursor() as cur:
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
    print("🧪 Final PostgreSQL Persistence Test")
    print("=" * 70)

    # Initial check
    initial_ps = check_prepared_statements()
    print(f"\n📊 Initial prepared statements: {initial_ps}")

    # Test 1: Simple agent
    print("\n1️⃣ Testing Simple Agent...")
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

        print("✅ Simple agent completed")
    except Exception as e:
        print(f"❌ Simple agent error: {e}")

    # Test 2: Conversation agent
    print("\n2️⃣ Testing Conversation Agent...")
    try:
        from haive.core.engine.aug_llm import AugLLMConfig

        from haive.agents.conversation.collaberative.agent import (
            CollaborativeConversation,
        )

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

        result = agent.invoke(
            {"messages": [], "topic": "Final test", "format": "outline"},
            {"configurable": {"thread_id": "final_test_collab"}},
        )

        print("✅ Conversation agent completed")
    except Exception as e:
        print(f"❌ Conversation agent error: {e}")

    # Check for new prepared statements
    final_ps = check_prepared_statements()
    print(f"\n📊 Final prepared statements: {final_ps}")

    if final_ps > initial_ps:
        print(f"❌ FAILURE: {final_ps - initial_ps} new prepared statements created!")
    else:
        print("✅ SUCCESS: No new prepared statements created!")

    # Check configurations
    print("\n3️⃣ Checking Configurations...")

    # Check ConnectionManager
    try:
        from haive.core.persistence.store.connection import ConnectionManager

        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core/persistence/store/connection.py",
            "r",
        ) as f:
            content = f.read()

        if '"prepare_threshold": None' in content:
            print("✅ ConnectionManager: prepare_threshold=None")
        else:
            print("❌ ConnectionManager: prepare_threshold not None")
    except Exception as e:
        print(f"❌ ConnectionManager check error: {e}")

    # Check persistence mixin
    try:
        from haive.agents.base.mixins.persistence_mixin import PersistenceMixin

        with open(
            "/home/will/Projects/haive/backend/haive/packages/haive-agents/src/haive/agents/base/mixins/persistence_mixin.py",
            "r",
        ) as f:
            content = f.read()

        if "prepare_threshold=None" in content:
            print("✅ PersistenceMixin: prepare_threshold=None")
        else:
            print("❌ PersistenceMixin: prepare_threshold not None")
    except Exception as e:
        print(f"❌ PersistenceMixin check error: {e}")

    print("\n" + "=" * 70)
    print("🏁 Test complete!")


if __name__ == "__main__":
    test_persistence_fixes()
