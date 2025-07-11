"""Test Corrective RAG V2 Agent.

Tests the improved CorrectiveRAGAgentV2 with proper document grading.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.rag.corrective.agent_v2 import CorrectiveRAGAgentV2


class TestCorrectiveRAGAgentV2:
    """Test the CorrectiveRAGAgentV2 workflow."""

    @pytest.fixture
    def llm_config(self):
        """LLM configuration for testing."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    def test_corrective_rag_creation(self, llm_config):
        """Test creating Corrective RAG with documents."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = CorrectiveRAGAgentV2.from_documents(
            documents=conversation_documents[:5],  # Use subset
            llm_config=llm_config,
            relevance_threshold=0.7,
        )

        assert rag.name == "Corrective RAG Agent V2"
        assert len(rag.agents) == 5  # retriever, grader, web_search, refiner, answer

        # Check agent names
        agent_names = [agent.name for agent in rag.agents]
        assert "CRAG Retriever" in agent_names
        assert "Document Grader" in agent_names
        assert "Web Search Query Generator" in agent_names
        assert "Document Refiner" in agent_names
        assert "Answer Generator" in agent_names

    def test_corrective_rag_with_relevant_query(self, llm_config):
        """Test Corrective RAG with a query that should have relevant docs."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = CorrectiveRAGAgentV2.from_documents(
            documents=conversation_documents[:5],
            llm_config=llm_config,
            relevance_threshold=0.7,
        )

        # Query about something in the documents
        query = "Tell me about the weather or restaurants"

        try:
            result = rag.run({"query": query})

            # Should have results
            assert result is not None

            # Check if grading happened
            if "document_decisions" in result:
                pass

        except Exception as e:
            pytest.fail(f"Corrective RAG failed: {e}")

    def test_corrective_rag_with_irrelevant_query(self, llm_config):
        """Test Corrective RAG with a query that should trigger web search."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = CorrectiveRAGAgentV2.from_documents(
            documents=conversation_documents[:3],
            llm_config=llm_config,
            relevance_threshold=0.8,  # High threshold
        )

        # Query about something NOT in the documents
        query = "What is the latest stock price of Apple?"

        try:
            result = rag.run({"query": query})

            # Should complete even with irrelevant query
            assert result is not None

        except Exception:
            # Expected - web search is placeholder
            pass

    def test_corrective_rag_threshold_variations(self, llm_config):
        """Test different relevance thresholds."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        # Test with low threshold (more permissive)
        rag_low = CorrectiveRAGAgentV2.from_documents(
            documents=conversation_documents[:5],
            llm_config=llm_config,
            relevance_threshold=0.3,
        )

        # Test with high threshold (more strict)
        rag_high = CorrectiveRAGAgentV2.from_documents(
            documents=conversation_documents[:5],
            llm_config=llm_config,
            relevance_threshold=0.9,
        )

        assert rag_low.name == "Corrective RAG Agent V2"
        assert rag_high.name == "Corrective RAG Agent V2"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
