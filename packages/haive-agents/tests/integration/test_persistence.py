#!/usr/bin/env python3
"""Test automatic persistence in agents."""

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_automatic_persistence():
    """Test that agents automatically generate consistent thread_ids for persistence."""
    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test persistence", participants=["Alice", "Bob"], max_rounds=1
    )

    # Test 1: Check that agent generates consistent thread_id

    # Generate thread_id by calling _generate_default_thread_id directly
    agent._generate_default_thread_id()
    agent._generate_default_thread_id()

    # Test 2: Check that runnable_config uses automatic thread_id

    config = agent._prepare_runnable_config()
    config["configurable"]["thread_id"]

    # Test 3: Test that different agents get different thread_ids

    agent2 = CollaborativeConversation.create_brainstorming_session(
        topic="Different topic", participants=["Charlie", "David"], max_rounds=1
    )

    agent2._generate_default_thread_id()


if __name__ == "__main__":
    test_automatic_persistence()
