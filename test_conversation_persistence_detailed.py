#!/usr/bin/env python3
"""Detailed test to examine conversation agent inputs, outputs, and persistence behavior."""

import json
import logging

from haive.agents.conversation.collaberative.agent import CollaborativeConversation

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_conversation_persistence_detailed():
    """Test conversation agents with detailed examination of inputs, outputs, and persistence."""

    # Test 1: Run conversation with persistence and examine the flow

    session = CollaborativeConversation.create_brainstorming_session(
        topic="AI-powered productivity tools",
        participants=["ProductManager", "Developer"],
        sections=["Problem Analysis", "Solution Ideas"],
        max_rounds=2,  # Allow for more interaction
        persistence=True,
    )


    # Test 2: Run conversation and capture detailed results
    thread_id = "detailed_test_001"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 100}}


    result = session.run({}, config=config)


    # Extract and display key information from result
    if hasattr(result, "messages"):
        for i, msg in enumerate(result.messages):
            msg_type = type(msg).__name__
            speaker = getattr(msg, "name", "System")
            content_preview = (
                msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
            )

    # Check other result attributes
    for attr in [
        "round_number",
        "turn_count",
        "conversation_ended",
        "speakers",
        "topic",
    ]:
        if hasattr(result, attr):
            pass

    # Test 3: Verify persistence by checking database state

    if hasattr(session.checkpointer, "conn") and session.checkpointer.conn:
        try:
            with session.checkpointer.conn.connection() as conn:
                with conn.cursor() as cursor:
                    # Get thread info
                    cursor.execute(
                        "SELECT thread_id, created_at, last_access, metadata FROM threads WHERE thread_id = %s",
                        (thread_id,),
                    )
                    thread_info = cursor.fetchone()

                    if thread_info:

                        # Try to parse metadata if it exists
                        try:
                            metadata = (
                                json.loads(thread_info[3]) if thread_info[3] else {}
                            )
                        except:
                            pass

                    # Get checkpoint info
                    cursor.execute(
                        "SELECT checkpoint_id, created_at FROM checkpoints WHERE thread_id = %s ORDER BY created_at",
                        (thread_id,),
                    )
                    checkpoints = cursor.fetchall()

                    for i, (cp_id, created_at) in enumerate(
                        checkpoints[:5]
                    ):  # Show first 5
                        pass
                    if len(checkpoints) > 5:
                        pass

        except Exception as e:
            pass")
    else:
        pass")

    # Test 4: Try to retrieve a specific checkpoint

    try:
        checkpoint_config = {"configurable": {"thread_id": thread_id}}
        retrieved_checkpoint = session.checkpointer.get(checkpoint_config)

        if retrieved_checkpoint:

            # Look at channel_values which contains the actual state
            if "channel_values" in retrieved_checkpoint:
                channel_values = retrieved_checkpoint["channel_values"]

                if isinstance(channel_values, dict):
                    for key, value in channel_values.items():
                        if key == "messages":
                            pass
                        else:
                            pass
                elif hasattr(channel_values, "__dict__"):
                    for key, value in channel_values.__dict__.items():
                        if key == "messages":
                            pass
                        else:
                            pass
        else:
            pass")

    except Exception as e:
        pass")

    # Test 5: Try to resume conversation from persisted state

    try:
        # Create a new session but try to continue from the same thread
        resume_session = CollaborativeConversation.create_brainstorming_session(
            topic="Resumed conversation - AI productivity tools",
            participants=["ProductManager", "Developer"],
            sections=["Implementation Plan"],  # New section
            max_rounds=1,
            persistence=True,
        )

        # Try to run with the same thread_id to see if it resumes
        resume_config = {
            "configurable": {"thread_id": thread_id, "recursion_limit": 100}
        }

        resume_result = resume_session.run({}, config=resume_config)


        if hasattr(resume_result, "messages"):

            # Show the last few messages to see continuation
            for msg in resume_result.messages[-3:]:
                msg_type = type(msg).__name__
                speaker = getattr(msg, "name", "System")
                content_preview = (
                    msg.content[:80] + "..." if len(msg.content) > 80 else msg.content
                )

    except Exception as e:
        pass")



if __name__ == "__main__":
    test_conversation_persistence_detailed()
