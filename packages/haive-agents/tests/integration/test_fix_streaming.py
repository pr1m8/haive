#!/usr/bin/env python3
"""Test and fix the streaming values issue."""

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_current_streaming():
    """Test current streaming behavior."""

    print("=== Current Streaming Behavior ===\n")

    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test", participants=["Alice"], max_rounds=1
    )

    # Force compilation
    if not hasattr(agent, "_app") or agent._app is None:
        agent.compile()

    print(f"1. Agent has _app: {hasattr(agent, '_app') and agent._app is not None}")

    # Test direct app streaming
    print("\n2. Direct _app.stream() behavior:")
    try:
        config = {"configurable": {"recursion_limit": 3}}

        for i, chunk in enumerate(agent._app.stream({}, config)):
            print(f"\n   Raw Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")

            if isinstance(chunk, dict):
                print(f"      Keys: {list(chunk.keys())}")

                # Check if this has the expected LangGraph structure
                if len(chunk.keys()) == 1:
                    node_name = list(chunk.keys())[0]
                    node_data = chunk[node_name]
                    print(f"      Node '{node_name}' data:")
                    print(f"        Type: {type(node_data)}")

                    if isinstance(node_data, dict):
                        # This is where the actual state values are!
                        print(f"        State keys: {list(node_data.keys())}")
                        for key in [
                            "current_speaker",
                            "turn_count",
                            "conversation_ended",
                        ]:
                            if key in node_data:
                                print(f"          {key}: {node_data[key]}")

            if i >= 2:
                break

    except Exception as e:
        print(f"   ❌ Direct streaming failed: {e}")

    print("\n3. Current stream() method behavior:")
    try:
        for i, chunk in enumerate(
            agent.stream({}, config={"configurable": {"recursion_limit": 3}})
        ):
            print(f"\n   Processed Chunk {i+1}:")
            print(f"      Type: {type(chunk)}")
            print(
                f"      Keys: {list(chunk.keys()) if isinstance(chunk, dict) else 'Not a dict'}"
            )

            if i >= 2:
                break
    except Exception as e:
        print(f"   ❌ Agent streaming failed: {e}")


def propose_fix():
    """Propose the fix for streaming values."""

    print("\n=== Proposed Fix ===\n")

    print("The issue is in _process_stream_chunk() method:")
    print("Current code looks for chunk['values'] but LangGraph returns node updates")
    print()
    print("Current logic:")
    print("  if stream_mode == 'values':")
    print("      if isinstance(chunk, dict) and 'values' in chunk:")
    print("          return chunk['values']  # Never triggered!")
    print("      return chunk  # Returns node updates instead")
    print()
    print("Proposed fix:")
    print("  if stream_mode == 'values':")
    print("      # For LangGraph, accumulate full state from node updates")
    print("      if isinstance(chunk, dict):")
    print("          # Extract state data from node updates")
    print("          for node_name, node_data in chunk.items():")
    print("              if isinstance(node_data, dict):")
    print("                  return node_data  # Return the actual state")
    print("      return chunk")
    print()
    print("This would return the actual state values instead of node names!")


if __name__ == "__main__":
    test_current_streaming()
    propose_fix()
