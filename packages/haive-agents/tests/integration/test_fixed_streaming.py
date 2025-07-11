#!/usr/bin/env python3
"""Test the fixed streaming behavior."""

from haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_fixed_streaming():
    """Test streaming after the fix."""

    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test fixed streaming", participants=["Alice"], max_rounds=1
    )

    try:
        config = {"configurable": {"recursion_limit": 5}}

        for i, chunk in enumerate(
            agent.stream({}, stream_mode="values", config=config)
        ):

            if isinstance(chunk, dict):

                # Show actual state values
                for key in [
                    "current_speaker",
                    "turn_count",
                    "conversation_ended",
                    "messages",
                ]:
                    if key in chunk:
                        if key == "messages":
                            if chunk[key]:
                                last_msg = chunk[key][-1]
                                preview = (
                                    str(last_msg)[:100] + "..."
                                    if len(str(last_msg)) > 100
                                    else str(last_msg)
                                )
                        else:
                            pass

                # Show other interesting state
                for key in ["topic", "speakers", "shared_document"]:
                    if key in chunk:
                        value = chunk[key]
                        if isinstance(value, str) and len(value) > 50:
                            pass
                        else:
                            pass

            if i >= 3:  # Show first few chunks
                break

    except Exception as e:
        import traceback

        traceback.print_exc()

    try:
        for i, chunk in enumerate(
            agent.stream({}, stream_mode="updates", config=config)
        ):

            if i >= 2:
                break
    except Exception as e:
        pass")



if __name__ == "__main__":
    test_fixed_streaming()
