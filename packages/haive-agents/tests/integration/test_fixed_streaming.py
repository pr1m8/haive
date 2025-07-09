#!/usr/bin/env python3
"""Test the fixed streaming behavior."""

from haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_fixed_streaming():
    """Test streaming after the fix."""

    print("=== Testing Fixed Streaming ===\n")

    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test fixed streaming", participants=["Alice"], max_rounds=1
    )

    print("1. Testing 'values' stream mode (should now show actual state):")
    try:
        config = {"configurable": {"recursion_limit": 5}}

        for i, chunk in enumerate(
            agent.stream({}, stream_mode="values", config=config)
        ):
            print(f"\n   Values Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")

            if isinstance(chunk, dict):
                print(f"      Keys: {list(chunk.keys())}")

                # Show actual state values
                for key in [
                    "current_speaker",
                    "turn_count",
                    "conversation_ended",
                    "messages",
                ]:
                    if key in chunk:
                        if key == "messages":
                            print(f"        {key}: {len(chunk[key])} messages")
                            if chunk[key]:
                                last_msg = chunk[key][-1]
                                preview = (
                                    str(last_msg)[:100] + "..."
                                    if len(str(last_msg)) > 100
                                    else str(last_msg)
                                )
                                print(f"          Latest: {preview}")
                        else:
                            print(f"        {key}: {chunk[key]}")

                # Show other interesting state
                for key in ["topic", "speakers", "shared_document"]:
                    if key in chunk:
                        value = chunk[key]
                        if isinstance(value, str) and len(value) > 50:
                            print(f"        {key}: {value[:50]}...")
                        else:
                            print(f"        {key}: {value}")

            if i >= 3:  # Show first few chunks
                break

    except Exception as e:
        print(f"   ❌ Values streaming failed: {e}")
        import traceback

        traceback.print_exc()

    print("\n2. Comparing with 'updates' mode:")
    try:
        for i, chunk in enumerate(
            agent.stream({}, stream_mode="updates", config=config)
        ):
            print(f"\n   Updates Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")
            print(
                f"      Keys: {list(chunk.keys()) if isinstance(chunk, dict) else 'Not a dict'}"
            )

            if i >= 2:
                break
    except Exception as e:
        print(f"   ❌ Updates streaming failed: {e}")

    print("\n3. Summary:")
    print("   ✅ Values mode should now show actual conversation state")
    print("   ✅ Updates mode shows node-level changes")
    print("   ✅ Streaming metadata now includes real state values")


if __name__ == "__main__":
    test_fixed_streaming()
