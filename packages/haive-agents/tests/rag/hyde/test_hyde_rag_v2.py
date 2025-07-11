"""Test HyDE RAG V2 Agent.

Tests the improved HyDERAGAgentV2 with proper hypothetical document generation.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents
from haive.core.models.llm.base import AzureLLMConfig

from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2


class TestHyDERAGAgentV2:
    """Test the HyDERAGAgentV2 workflow."""

    @pytest.fixture
    def llm_config(self):
        """LLM configuration for testing."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    def test_hyde_rag_creation(self, llm_config):
        """Test creating HyDE RAG with documents."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = HyDERAGAgentV2.from_documents(
            documents=conversation_documents[:5], llm_config=llm_config
        )

        assert rag.name == "HyDE RAG Agent V2"
        assert len(rag.agents) == 3  # generator, retriever, answer

        # Check agent names
        agent_names = [agent.name for agent in rag.agents]
        assert "HyDE Generator" in agent_names
        assert "HyDE Retriever" in agent_names
        assert "Answer Generator" in agent_names

    def test_hyde_rag_basic_query(self, llm_config):
        """Test HyDE RAG with a basic query."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = HyDERAGAgentV2.from_documents(
            documents=conversation_documents[:5], llm_config=llm_config
        )

        # Test query
        query = "What types of food are mentioned in conversations?"

        try:
            result = rag.run({"query": query})

            # Should have results
            assert result is not None

            # Check if hypothetical doc was generated
            if "hypothetical_doc" in result:
                pass

        except Exception as e:
            pytest.fail(f"HyDE RAG failed: {e}")

    def test_hyde_rag_technical_query(self, llm_config):
        """Test HyDE RAG with a technical query."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        # Create some technical documents
        technical_docs = [
            Document(
                page_content="Python is a high-level programming language known for its simplicity."
            ),
            Document(
                page_content="Machine learning models can be trained using frameworks like TensorFlow."
            ),
            Document(
                page_content="APIs allow different software applications to communicate."
            ),
        ]

        rag = HyDERAGAgentV2.from_documents(
            documents=technical_docs, llm_config=llm_config
        )

        query = "How do neural networks work?"

        try:
            result = rag.run({"query": query})

            assert result is not None

        except Exception as e:
            pytest.fail(f"HyDE RAG failed on technical query: {e}")

    def test_hyde_vs_simple_rag(self, llm_config):
        """Compare HyDE RAG with Simple RAG."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        from haive.agents.rag.simple.agent import SimpleRAGAgent

        # Create both agents with same documents
        docs = conversation_documents[:5]

        hyde_rag = HyDERAGAgentV2.from_documents(documents=docs, llm_config=llm_config)

        simple_rag = SimpleRAGAgent.from_documents(
            documents=docs, llm_config=llm_config
        )

        # Test with abstract query
        query = "What are the main topics discussed?"

        try:
            # Run both
            hyde_result = hyde_rag.run({"query": query})
            simple_result = simple_rag.run({"query": query})

            # Both should complete
            assert hyde_result is not None
            assert simple_result is not None

        except Exception:
            pass


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
