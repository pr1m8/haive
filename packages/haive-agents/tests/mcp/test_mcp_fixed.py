#!/usr/bin/env python3
"""Test the fixed MCP RAG agent with proper VectorStoreConfig pattern"""
import asyncio
import sys
from pathlib import Path

# Add the correct path for imports
sys.path.insert(0, str(Path(__file__).parent))


async def test_mcp_rag_agent():
    """Test the MCP RAG agent with proper configuration."""

    try:
        # Import after path setup
        sys.path.insert(
            0, str(Path(__file__).parent / "packages" / "haive-mcp" / "src")
        )
        from haive.mcp.mcp_simple_rag_agent import create_mcp_rag_agent

        # Create the agent
        agent = create_mcp_rag_agent()


        # Test with a simple query
        test_queries = [
            "python database",
            "SQLAlchemy",
            "PostgreSQL server",
            "GitHub integration",
        ]

        for query in test_queries:

            try:
                # Test with proper input format
                result = await agent.arun(query)


                # Check if we got retrieved documents
                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents

                    if docs:
                    else:

                        # Try direct vector store test
                        if hasattr(agent.engine, "vector_store_config"):
                            vs_config = agent.engine.vector_store_config
                            vectorstore = vs_config.create_vectorstore()
                            direct_results = vectorstore.similarity_search(query, k=3)

                            if direct_results:
                                for i, doc in enumerate(direct_results[:2], 1):
                                    pass
                else:
                    pass.")

            except Exception as e:
                import traceback

                traceback.print_exc()

    except Exception as e:
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_rag_agent())
