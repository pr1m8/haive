#!/usr/bin/env python3
"""Test proper conversation flow with adequate rounds."""

import logging

from haive.agents.conversation.collaberative.agent import CollaborativeConversation

# Set up logging to see conversation flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_proper_conversation_flow():
    """Test conversation with proper round count to see actual conversation."""


    # Create conversation with adequate rounds
    session = CollaborativeConversation.create_brainstorming_session(
        topic="Simple AI assistant features",
        participants=["ProductManager", "Developer"],
        sections=["Core Features"],  # Just one section to keep it simple
        min_contributions_per_section=1,  # Each person contributes once
        max_rounds=10,  # Enough rounds for actual conversation
        persistence=True,
    )


    # Calculate expected contributions
    expected_contributions = (
        len(session.participant_agents)
        * len(session.sections)
        * session.min_contributions_per_section
    )

    # Run conversation
    thread_id = "proper_flow_test_001"
    config = {"configurable": {"thread_id": thread_id, "recursion_limit": 50}}

    try:
        result = session.run({}, config=config)


        # Show conversation flow through messages
        if hasattr(result, "messages"):

            for i, msg in enumerate(result.messages):
                msg_type = type(msg).__name__
                speaker = getattr(msg, "name", "System")

                # Truncate long content but show more for actual contributions
                if speaker in ["ProductManager", "Developer"]:
                    # Show full content for participant contributions
                    content = msg.content
                else:
                    # Truncate system messages
                    content = (
                        msg.content[:150] + "..."
                        if len(msg.content) > 150
                        else msg.content
                    )

        # Show conversation metadata
        metadata_attrs = [
            "round_number",
            "turn_count",
            "conversation_ended",
            "current_section",
            "completed_sections",
        ]
        for attr in metadata_attrs:
            if hasattr(result, attr):
                value = getattr(result, attr)

        # Show contributions if available
        if hasattr(result, "contributions"):
            for i, (contributor, section, content) in enumerate(result.contributions):
                content_preview = (
                    content[:100] + "..." if len(content) > 100 else content
                )

        # Show final document
        if hasattr(result, "shared_document") and result.shared_document:
            # Show the document with proper indentation
            doc_lines = result.shared_document.split("\n")
            for line in doc_lines:
                pass


        # Check persistence
        if hasattr(session.checkpointer, "conn") and session.checkpointer.conn:
            try:
                with session.checkpointer.conn.connection() as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(
                            "SELECT COUNT(*) FROM checkpoints WHERE thread_id = %s",
                            (thread_id,),
                        )
                        checkpoint_count = cursor.fetchone()[0]

                        # Try to retrieve the final state
                        checkpoint_config = {"configurable": {"thread_id": thread_id}}
                        final_checkpoint = session.checkpointer.get(checkpoint_config)
                        if final_checkpoint and "channel_values" in final_checkpoint:
                            channel_values = final_checkpoint["channel_values"]
                            if (
                                isinstance(channel_values, dict)
                                and "messages" in channel_values
                            ):
                                persisted_msg_count = len(channel_values["messages"])
                            else:
                                passed")
                        else:
                            pass")
            except Exception as e:
                pass")

    except Exception as e:
        import traceback

        traceback.print_exc()



if __name__ == "__main__":
    test_proper_conversation_flow()
