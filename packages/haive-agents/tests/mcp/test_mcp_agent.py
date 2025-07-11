#!/usr/bin/env python3
"""Test script for MCP RAG Agent"""
import asyncio
import sys
from pathlib import Path

# Add to path
sys.path.insert(0, str(Path(__file__).parent / "packages" / "haive-mcp" / "src"))


async def test_mcp_agent():
    """Test the MCP RAG agent directly."""

    try:
        from haive.mcp.mcp_simple_rag_agent import create_mcp_rag_agent

        # Create agent
        agent = create_mcp_rag_agent()


        # Test queries
        queries = [
            "python database servers",
            "PostgreSQL MCP server",
            "GitHub integration",
            "file system operations",
        ]

        for query in queries:

            try:
                result = await agent.arun(query)

                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents

                    if docs:
                        for i, doc in enumerate(docs[:3], 1):
                            server_name = doc.metadata.get("server_name", "Unknown")
                            category = doc.metadata.get("category", "unknown")
                            stars = doc.metadata.get("stars", 0)
                    else:
                        pass
                else:
                    pass.")

            except Exception as e:
                pass")

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_agent())
