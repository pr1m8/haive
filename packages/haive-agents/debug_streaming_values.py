#!/usr/bin/env python3
"""Debug why streaming values are empty."""

import json

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def debug_streaming_values():
    """Debug what's actually in the streaming chunks."""

    print("=== Debugging Streaming Values ===\n")

    # Create simple agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test", participants=["Alice"], max_rounds=1
    )

    print("1. Raw streaming chunk inspection:")
    try:
        config = {"configurable": {"recursion_limit": 5}}

        for i, chunk in enumerate(agent.stream({}, config=config)):
            print(f"\n--- CHUNK {i+1} ---")
            print(f"Type: {type(chunk)}")
            print(f"Dir: {[attr for attr in dir(chunk) if not attr.startswith('_')]}")

            if hasattr(chunk, "__dict__"):
                print(f"Dict: {chunk.__dict__}")

            if isinstance(chunk, dict):
                print(f"Keys: {list(chunk.keys())}")
                for key, value in chunk.items():
                    print(f"  {key}:")
                    print(f"    Type: {type(value)}")
                    if isinstance(value, dict):
                        print(f"    Keys: {list(value.keys())}")
                        # Show first few key-value pairs
                        for k, v in list(value.items())[:3]:
                            if isinstance(v, str) and len(v) > 100:
                                print(f"      {k}: {v[:100]}...")
                            else:
                                print(f"      {k}: {v}")
                        if len(value) > 3:
                            print(f"      ... and {len(value)-3} more keys")
                    elif isinstance(value, list):
                        print(f"    Length: {len(value)}")
                        if value:
                            print(f"    First item type: {type(value[0])}")
                    else:
                        print(f"    Value: {str(value)[:100]}")

            if i >= 3:  # Limit to avoid too much output
                break

    except Exception as e:
        print(f"❌ Streaming failed: {e}")
        import traceback

        traceback.print_exc()

    print("\n2. Testing if agent has app attribute:")
    try:
        if hasattr(agent, "app"):
            print(f"   ✅ Agent has 'app' attribute: {type(agent.app)}")

            # Test streaming directly on app
            print("   Testing app.stream directly:")
            for i, chunk in enumerate(agent.app.stream({}, config=config)):
                print(f"   App chunk {i+1}: {type(chunk)}")
                if isinstance(chunk, dict) and chunk:
                    print(f"     Keys: {list(chunk.keys())}")
                    # Show state values
                    for key, value in chunk.items():
                        if key in [
                            "current_speaker",
                            "turn_count",
                            "conversation_ended",
                        ]:
                            print(f"       {key}: {value}")
                        elif key == "messages" and isinstance(value, list):
                            print(f"       messages: {len(value)} items")

                if i >= 2:
                    break
        else:
            print("   ❌ Agent doesn't have 'app' attribute")
            print(
                f"   Available attributes: {[attr for attr in dir(agent) if not attr.startswith('_')]}"
            )

    except Exception as e:
        print(f"   ❌ App streaming failed: {e}")

    print("\n3. Testing different stream modes for values:")
    try:
        modes = ["values", "updates", "messages"]
        for mode in modes:
            print(f"\n   Mode '{mode}':")
            config = {"configurable": {"recursion_limit": 3}, "stream_mode": mode}

            chunk_count = 0
            for chunk in agent.stream({}, config=config):
                chunk_count += 1
                if isinstance(chunk, dict) and chunk:
                    print(f"     Chunk {chunk_count}: {list(chunk.keys())}")
                    if mode == "values":
                        # For values mode, show actual state
                        for key in ["current_speaker", "turn_count", "messages"]:
                            if key in chunk:
                                if key == "messages":
                                    print(f"       {key}: {len(chunk[key])} messages")
                                else:
                                    print(f"       {key}: {chunk[key]}")
                elif chunk:
                    print(
                        f"     Chunk {chunk_count}: {type(chunk)} - {str(chunk)[:50]}..."
                    )
                else:
                    print(f"     Chunk {chunk_count}: EMPTY")

                if chunk_count >= 2:
                    break
    except Exception as e:
        print(f"   ❌ Multi-mode test failed: {e}")

    print("\n4. Check if it's a compilation issue:")
    try:
        # Check if agent is properly compiled
        print(f"   Agent compiled: {hasattr(agent, 'app') and agent.app is not None}")

        # Try to get state schema
        if hasattr(agent, "state_schema"):
            print(f"   State schema: {agent.state_schema}")
            if hasattr(agent.state_schema, "model_fields"):
                print(
                    f"   State fields: {list(agent.state_schema.model_fields.keys())}"
                )

        # Check if graph is built
        if hasattr(agent, "graph"):
            print(f"   Graph: {type(agent.graph)}")
            if hasattr(agent.graph, "nodes"):
                print(f"   Graph nodes: {list(agent.graph.nodes)}")

    except Exception as e:
        print(f"   ❌ Compilation check failed: {e}")


if __name__ == "__main__":
    debug_streaming_values()
