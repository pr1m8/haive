#!/usr/bin/env python3
"""Test streaming metadata from conversation agents."""

import json

from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_streaming_metadata():
    """Test what metadata gets streamed back from conversation agents."""

    print("=== Testing Streaming Metadata ===\n")

    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test streaming metadata", participants=["Alice", "Bob"], max_rounds=1
    )

    print("1. Testing regular invoke (non-streaming):")
    try:
        result = agent.invoke({}, config={"configurable": {"recursion_limit": 3}})
        print(f"   Result type: {type(result)}")
        print(
            f"   Result keys: {list(result.keys()) if isinstance(result, dict) else 'Not a dict'}"
        )

        # Show sample of result
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, str):
                    print(
                        f"   {key}: {value[:100]}..."
                        if len(value) > 100
                        else f"   {key}: {value}"
                    )
                else:
                    print(f"   {key}: {type(value)} - {str(value)[:50]}...")
    except Exception as e:
        print(f"   ❌ Invoke failed: {str(e)[:100]}...")

    print("\n2. Testing streaming invoke:")
    try:
        stream = agent.stream({}, config={"configurable": {"recursion_limit": 3}})

        chunk_count = 0
        metadata_chunks = []

        for chunk in stream:
            chunk_count += 1
            print(f"\n   Chunk {chunk_count}:")
            print(f"      Type: {type(chunk)}")

            if isinstance(chunk, dict):
                print(f"      Keys: {list(chunk.keys())}")

                # Look for metadata
                for key, value in chunk.items():
                    if "metadata" in key.lower() or key in ["__metadata__", "metadata"]:
                        print(f"      METADATA found in '{key}': {value}")
                        metadata_chunks.append(value)
                    elif isinstance(value, dict) and any(
                        "metadata" in k.lower() for k in value.keys()
                    ):
                        print(
                            f"      Nested metadata in '{key}': {[k for k in value.keys() if 'metadata' in k.lower()]}"
                        )
                    else:
                        # Show preview of value
                        if isinstance(value, str):
                            preview = value[:50] + "..." if len(value) > 50 else value
                        else:
                            preview = (
                                str(value)[:50] + "..."
                                if len(str(value)) > 50
                                else str(value)
                            )
                        print(f"      {key}: {preview}")
            else:
                print(f"      Content: {str(chunk)[:100]}...")

            # Limit to first few chunks to avoid too much output
            if chunk_count >= 5:
                print(f"   ... (stopping after {chunk_count} chunks)")
                break

    except Exception as e:
        print(f"   ❌ Streaming failed: {str(e)[:100]}...")

    print("\n3. Testing astream with metadata:")
    try:
        import asyncio

        async def test_astream():
            astream = agent.astream({}, config={"configurable": {"recursion_limit": 3}})

            chunk_count = 0
            async for chunk in astream:
                chunk_count += 1
                print(f"\n   Async Chunk {chunk_count}:")

                if isinstance(chunk, dict):
                    # Look specifically for streaming metadata
                    if "__metadata__" in chunk:
                        print(f"      🔍 METADATA: {chunk['__metadata__']}")

                    # Check for LangGraph streaming metadata
                    for key in chunk.keys():
                        if "metadata" in key.lower():
                            print(f"      📊 {key}: {chunk[key]}")

                if chunk_count >= 3:
                    break

        asyncio.run(test_astream())

    except Exception as e:
        print(f"   ❌ Async streaming failed: {str(e)[:100]}...")

    print("\n4. Summary:")
    print(f"   Total metadata chunks collected: {len(metadata_chunks)}")
    if metadata_chunks:
        print("   Metadata types found:")
        for i, metadata in enumerate(metadata_chunks):
            print(f"      {i+1}. {type(metadata)} - {str(metadata)[:100]}...")


if __name__ == "__main__":
    test_streaming_metadata()
