#!/usr/bin/env python3
"""Test detailed streaming metadata from conversation agents."""


from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_detailed_streaming():
    """Test streaming with stream_mode configuration to get detailed metadata."""

    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test streaming", participants=["Alice"], max_rounds=1
    )

    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "values"}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            if isinstance(chunk, dict):
                # Show key state changes
                for key in ["current_speaker", "turn_count", "conversation_ended"]:
                    if key in chunk:
                        pass

                # Show message count
                if "messages" in chunk:
                    if chunk["messages"]:
                        last_msg = chunk["messages"][-1]
                        if hasattr(last_msg, "name"):
                            pass

            if i >= 5:  # Limit output
                break
    except Exception as e:
        pass")

    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "updates"}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            if isinstance(chunk, dict):
                for node_name, update in chunk.items():
                    if isinstance(update, dict):
                        # Show interesting update fields
                        for key in ["current_speaker", "turn_count", "speaker_history"]:
                            if key in update:
                                pass
                    else:
                        pass

            if i >= 5:
                break
    except Exception as e:
        pass")

    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "messages"}

        for i, chunk in enumerate(agent.stream({}, config=config)):

            # Check for metadata in LangGraph messages
            if hasattr(chunk, "__dict__"):
                attrs = [attr for attr in dir(chunk) if not attr.startswith("_")]

                # Look for metadata specifically
                if hasattr(chunk, "metadata"):
                    pass}")
                if hasattr(chunk, "additional_kwargs"):
                    pass}")

            if isinstance(chunk, dict):
                for key, value in chunk.items():
                    if "metadata" in key.lower():
                        pass}")

            if i >= 5:
                break
    except Exception as e:
        pass")

    try:
        config = {
            "configurable": {"recursion_limit": 10, "debug": True},
            "stream_mode": "debug",
        }

        for i, chunk in enumerate(agent.stream({}, config=config)):

            if isinstance(chunk, dict):
                # Look for debug/metadata keys
                debug_keys = [
                    k
                    for k in chunk
                    if any(
                        word in k.lower()
                        for word in ["debug", "metadata", "trace", "step"]
                    )
                ]
                if debug_keys:
                    for key in debug_keys:
                        pass

            if i >= 3:
                break
    except Exception as e:
        pass")

    try:
        # Check what stream modes are available
        app = agent.app
        if hasattr(app, "stream_mode"):
            pass

        # Try to get available modes
        available_modes = ["values", "updates", "messages", "debug"]

    except Exception as e:
        pass")


if __name__ == "__main__":
    test_detailed_streaming()
