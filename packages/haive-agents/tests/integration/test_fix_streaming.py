#!/usr/bin/env python3
"""Test and fix the streaming values issue."""

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_current_streaming():
    """Test current streaming behavior."""

    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test", participants=["Alice"], max_rounds=1
    )

    # Force compilation
    if not hasattr(agent, "_app") or agent._app is None:
        agent.compile()


    # Test direct app streaming
    try:
        config = {"configurable": {"recursion_limit": 3}}

        for i, chunk in enumerate(agent._app.stream({}, config)):

            if isinstance(chunk, dict):

                # Check if this has the expected LangGraph structure
                if len(chunk.keys()) == 1:
                    node_name = next(iter(chunk.keys()))
                    node_data = chunk[node_name]

                    if isinstance(node_data, dict):
                        # This is where the actual state values are!
                        for key in [
                            "current_speaker",
                            "turn_count",
                            "conversation_ended",
                        ]:
                            if key in node_data:
                                pass

            if i >= 2:
                break

    except Exception as e:
        pass")

    try:
        for i, chunk in enumerate(
            agent.stream({}, config={"configurable": {"recursion_limit": 3}})
        ):

            if i >= 2:
                break
    except Exception as e:
        pass")


def propose_fix():
    """Propose the fix for streaming values."""



if __name__ == "__main__":
    test_current_streaming()
    propose_fix()
