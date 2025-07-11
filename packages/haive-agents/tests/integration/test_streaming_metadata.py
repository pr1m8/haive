#!/usr/bin/env python3
"""Test streaming metadata from conversation agents."""


from src.haive.agents.conversation.collaberative.agent import CollaborativeConversation


def test_streaming_metadata():
    """Test what metadata gets streamed back from conversation agents."""

    # Create agent
    agent = CollaborativeConversation.create_brainstorming_session(
        topic="Test streaming metadata", participants=["Alice", "Bob"], max_rounds=1
    )

    try:
        result = agent.invoke({}, config={"configurable": {"recursion_limit": 3}})

        # Show sample of result
        if isinstance(result, dict):
            for key, value in result.items():
                if isinstance(value, str):
                    pass
                else:
                    pass
    except Exception as e:
        pass")

    try:
        stream = agent.stream({}, config={"configurable": {"recursion_limit": 3}})

        chunk_count = 0
        metadata_chunks = []

        for chunk in stream:
            chunk_count += 1

            if isinstance(chunk, dict):

                # Look for metadata
                for key, value in chunk.items():
                    if "metadata" in key.lower() or key in ["__metadata__", "metadata"]:
                        metadata_chunks.append(value)
                    elif isinstance(value, dict) and any(
                        "metadata" in k.lower() for k in value
                    ):
                        pass
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
            else:
                pass

            # Limit to first few chunks to avoid too much output
            if chunk_count >= 5:
                break

    except Exception as e:
        pass")

    try:
        import asyncio

        async def test_astream():
            astream = agent.astream({}, config={"configurable": {"recursion_limit": 3}})

            chunk_count = 0
            async for chunk in astream:
                chunk_count += 1

                if isinstance(chunk, dict):
                    # Look specifically for streaming metadata
                    if "__metadata__" in chunk:
                        pass}")

                    # Check for LangGraph streaming metadata
                    for key in chunk:
                        if "metadata" in key.lower():
                            pass}")

                if chunk_count >= 3:
                    break

        asyncio.run(test_astream())

    except Exception as e:
        pass")

    if metadata_chunks:
        for i, metadata in enumerate(metadata_chunks):
            pass


if __name__ == "__main__":
    test_streaming_metadata()
