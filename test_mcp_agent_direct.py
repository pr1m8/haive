#!/usr/bin/env python3
"""Test MCP agent directly without server."""

import asyncio
import sys
from pathlib import Path

# Add parent path for imports
sys.path.insert(0, str(Path(__file__).parent))

from haive.mcp.mcp_simple_rag_agent import create_mcp_rag_agent


async def test_mcp_agent():
    """Test the MCP agent with various queries."""

    # Create the agent
    agent = create_mcp_rag_agent()

    # Test queries
    test_queries = [
        "What Python MCP servers can help with databases?",
        "Show me SQLite MCP servers",
        "Which MCP servers work with PostgreSQL?",
        "Find database-related MCP tools",
    ]

    for query in test_queries:

        try:
            # Run the query
            result = await agent.arun(query, debug=True)


            if hasattr(result, "retrieved_documents"):
                docs = result.retrieved_documents

                if docs:
                    for i, doc in enumerate(docs[:3], 1):
                        server_name = doc.metadata.get("server_name", "Unknown")
                        category = doc.metadata.get("category", "general")
                        stars = doc.metadata.get("stars", 0)


                        # Extract description
                        content_lines = doc.page_content.split("\n")
                        for line in content_lines:
                            if line.startswith("Description:"):
                                description = line.replace("Description:", "").strip()
                                if (
                                    description
                                    and description != "No description available"
                                ):
                                    pass}")
                                break
                else:

                    # Try direct vector store search
                    if hasattr(agent, "_vector_store"):
                        vs = agent._vector_store
                    elif hasattr(agent, "vector_store"):
                        vs = agent.vector_store
                    else:
                        continue

                    direct_results = vs.similarity_search(query, k=5)

                    if direct_results:
                        for i, doc in enumerate(direct_results[:3], 1):
                            server_name = doc.metadata.get("server_name", "Unknown")
            else:
                pass

        except Exception as e:
            import traceback

            traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_agent())
