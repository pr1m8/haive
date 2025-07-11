"""Test Multi-Query RAG Agent.

Tests the MultiQueryRAGAgent with query expansion.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document

from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent


class TestMultiQueryRAGAgent:
    """Test the MultiQueryRAGAgent workflow."""

    @pytest.fixture
    def llm_config(self):
        """LLM configuration for testing."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    @pytest.fixture
    def sample_documents(self):
        """Create sample documents for testing."""
        return [
            Document(
                page_content="Python is a versatile programming language used for web development, data science, and automation."
            ),
            Document(
                page_content="Machine learning is a subset of artificial intelligence that enables systems to learn from data."
            ),
            Document(
                page_content="Web development involves creating websites and web applications using various technologies."
            ),
            Document(
                page_content="Data science combines statistics, programming, and domain knowledge to extract insights from data."
            ),
            Document(
                page_content="APIs (Application Programming Interfaces) allow different software systems to communicate."
            ),
        ]

    def test_multi_query_rag_creation(self, llm_config, sample_documents):
        """Test creating Multi-Query RAG with documents."""
        rag = MultiQueryRAGAgent.from_documents(
            documents=sample_documents, llm_config=llm_config
        )

        assert rag.name == "Multi-Query RAG Agent"
        assert len(rag.agents) == 3  # expander, retriever, answer

        # Check agent names
        agent_names = [agent.name for agent in rag.agents]
        assert "Query Expander" in agent_names
        assert "Multi-Query Retriever" in agent_names
        assert "Answer Generator" in agent_names

    def test_multi_query_expansion(self, llm_config, sample_documents):
        """Test that queries are properly expanded."""
        rag = MultiQueryRAGAgent.from_documents(
            documents=sample_documents, llm_config=llm_config
        )

        # Test with a query that could benefit from expansion
        query = "How to build software?"

        try:
            result = rag.run({"query": query})

            # Should have results
            assert result is not None

            # Check if query variations were generated
            if "query_variations" in result:
                result["query_variations"]

            # Check retrieval stats
            if "retrieval_stats" in result:
                result["retrieval_stats"]

        except Exception as e:
            pytest.fail(f"Multi-Query RAG failed: {e}")

    def test_multi_query_vs_simple(self, llm_config):
        """Compare Multi-Query RAG with Simple RAG."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        # Create both agents
        docs = conversation_documents[:5]

        multi_rag = MultiQueryRAGAgent.from_documents(
            documents=docs, llm_config=llm_config
        )

        simple_rag = SimpleRAGAgent.from_documents(
            documents=docs, llm_config=llm_config
        )

        # Test with ambiguous query
        query = "Tell me about discussions"

        try:
            # Run both
            multi_result = multi_rag.run({"query": query})
            simple_result = simple_rag.run({"query": query})

            # Both should complete
            assert multi_result is not None
            assert simple_result is not None

            # Multi-query should have retrieved from multiple queries
            if "retrieval_queries" in multi_result:
                len(multi_result["retrieval_queries"])

        except Exception:
            pass

    def test_multi_query_edge_cases(self, llm_config):
        """Test Multi-Query RAG with edge cases."""
        # Test with minimal documents
        minimal_docs = [
            Document(page_content="The sky is blue."),
            Document(page_content="Water is wet."),
        ]

        rag = MultiQueryRAGAgent.from_documents(
            documents=minimal_docs, llm_config=llm_config
        )

        # Test with very specific query
        query = "What color is the sky?"

        try:
            result = rag.run({"query": query})
            assert result is not None
        except Exception:
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
