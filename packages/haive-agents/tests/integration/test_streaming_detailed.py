#!/usr/bin/env python3
"""Test detailed streaming metadata from conversation agents."""

import json

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_detailed_streaming():
    """Test streaming with stream_mode configuration to get detailed metadata."""

    print("=== Testing Detailed Streaming Metadata ===\n")

    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test streaming", participants=["Alice"], max_rounds=1
    )

    print("1. Testing stream with 'values' mode:")
    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "values"}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            print(f"\n   Values Chunk {i+1}:")
            if isinstance(chunk, dict):
                # Show key state changes
                for key in ["current_speaker", "turn_count", "conversation_ended"]:
                    if key in chunk:
                        print(f"      {key}: {chunk[key]}")

                # Show message count
                if "messages" in chunk:
                    print(f"      messages: {len(chunk['messages'])} messages")
                    if chunk["messages"]:
                        last_msg = chunk["messages"][-1]
                        if hasattr(last_msg, "name"):
                            print(f"        Latest from: {last_msg.name}")

            if i >= 5:  # Limit output
                break
    except Exception as e:
        print(f"   ❌ Values streaming failed: {str(e)[:100]}...")

    print("\n2. Testing stream with 'updates' mode:")
    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "updates"}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            print(f"\n   Updates Chunk {i+1}:")
            if isinstance(chunk, dict):
                for node_name, update in chunk.items():
                    print(f"      Node '{node_name}' update:")
                    if isinstance(update, dict):
                        # Show interesting update fields
                        for key in ["current_speaker", "turn_count", "speaker_history"]:
                            if key in update:
                                print(f"        {key}: {update[key]}")
                    else:
                        print(f"        {type(update)}")

            if i >= 5:
                break
    except Exception as e:
        print(f"   ❌ Updates streaming failed: {str(e)[:100]}...")

    print("\n3. Testing stream with 'messages' mode (LangGraph metadata):")
    try:
        config = {"configurable": {"recursion_limit": 10}, "stream_mode": "messages"}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            print(f"\n   Messages Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")

            # Check for metadata in LangGraph messages
            if hasattr(chunk, "__dict__"):
                attrs = [attr for attr in dir(chunk) if not attr.startswith("_")]
                print(f"      Attributes: {attrs}")

                # Look for metadata specifically
                if hasattr(chunk, "metadata"):
                    print(f"      🔍 METADATA: {chunk.metadata}")
                if hasattr(chunk, "additional_kwargs"):
                    print(f"      📊 KWARGS: {chunk.additional_kwargs}")

            if isinstance(chunk, dict):
                for key, value in chunk.items():
                    if "metadata" in key.lower():
                        print(f"      📊 {key}: {value}")

            if i >= 5:
                break
    except Exception as e:
        print(f"   ❌ Messages streaming failed: {str(e)[:100]}...")

    print("\n4. Testing with debug mode for more metadata:")
    try:
        config = {
            "configurable": {"recursion_limit": 10, "debug": True},
            "stream_mode": "debug",
        }

        for i, chunk in enumerate(agent.stream({}, config=config)):
            print(f"\n   Debug Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")

            if isinstance(chunk, dict):
                # Look for debug/metadata keys
                debug_keys = [
                    k
                    for k in chunk.keys()
                    if any(
                        word in k.lower()
                        for word in ["debug", "metadata", "trace", "step"]
                    )
                ]
                if debug_keys:
                    print(f"      Debug keys: {debug_keys}")
                    for key in debug_keys:
                        print(f"        {key}: {str(chunk[key])[:100]}...")

            if i >= 3:
                break
    except Exception as e:
        print(f"   ❌ Debug streaming failed: {str(e)[:100]}...")

    print("\n5. Summary of available stream modes:")
    try:
        # Check what stream modes are available
        app = agent.app
        if hasattr(app, "stream_mode"):
            print(f"   Default stream mode: {app.stream_mode}")

        # Try to get available modes
        print("   Attempting to detect available modes from LangGraph...")
        available_modes = ["values", "updates", "messages", "debug"]
        print(f"   Standard LangGraph modes: {available_modes}")

    except Exception as e:
        print(f"   ❌ Stream mode detection failed: {e}")


if __name__ == "__main__":
    test_detailed_streaming()
