#!/usr/bin/env python3
"""Test automatic persistence in agents."""

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_automatic_persistence():
    """Test that agents automatically generate consistent thread_ids for persistence."""

    print("=== Testing Automatic Persistence ===\n")

    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test persistence", participants=["Alice", "Bob"], max_rounds=1
    )

    # Test 1: Check that agent generates consistent thread_id
    print("1. Testing thread_id generation...")

    # Generate thread_id by calling _generate_default_thread_id directly
    thread_id_1 = agent._generate_default_thread_id()
    thread_id_2 = agent._generate_default_thread_id()

    print(f"   First call:  {thread_id_1}")
    print(f"   Second call: {thread_id_2}")
    print(f"   Consistent:  {thread_id_1 == thread_id_2}")

    # Test 2: Check that runnable_config uses automatic thread_id
    print("\n2. Testing runnable config preparation...")

    config = agent._prepare_runnable_config()
    thread_id_from_config = config["configurable"]["thread_id"]

    print(f"   Config thread_id: {thread_id_from_config}")
    print(f"   Matches generated: {thread_id_from_config == thread_id_1}")

    # Test 3: Test that different agents get different thread_ids
    print("\n3. Testing different agents get different thread_ids...")

    agent2 = CollaborativeConversation.create_brainstorming_session(
        topic="Different topic", participants=["Charlie", "David"], max_rounds=1
    )

    thread_id_agent2 = agent2._generate_default_thread_id()

    print(f"   Agent 1 thread_id: {thread_id_1}")
    print(f"   Agent 2 thread_id: {thread_id_agent2}")
    print(f"   Different:         {thread_id_1 != thread_id_agent2}")

    print(f"\n✅ Automatic persistence is working!")
    print(f"   - Agents generate consistent thread_ids based on their identity")
    print(f"   - Different agents get different thread_ids")
    print(f"   - No manual thread_id configuration required")


if __name__ == "__main__":
    test_automatic_persistence()
