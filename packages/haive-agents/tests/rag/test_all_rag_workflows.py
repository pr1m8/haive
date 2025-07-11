"""Comprehensive Test Suite for All RAG Workflows.

Tests all RAG agent implementations to ensure they work correctly.
"""

from typing import List

import pytest
from haive.core.fixtures.documents import conversation_documents
from haive.core.models.llm.base import AzureLLMConfig
from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage

from haive.agents.rag.adaptive.agent import AdaptiveRAGAgent

# Import all RAG agents
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.corrective.agent_v2 import CorrectiveRAGAgentV2
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.memory_aware.agent import MemoryAwareRAGAgent
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent


class TestAllRAGWorkflows:
    """Comprehensive tests for all RAG workflows."""

    @pytest.fixture
    def llm_config(self):
        """Standard LLM configuration for all tests."""
        return AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    @pytest.fixture
    def test_documents(self):
        """Create test documents for RAG."""
        return [
            Document(
                page_content="Python is a versatile programming language used for web development, data science, and automation.",
                metadata={"source": "programming.txt", "topic": "python"},
            ),
            Document(
                page_content="Machine learning algorithms can learn patterns from data without explicit programming.",
                metadata={"source": "ml.txt", "topic": "machine learning"},
            ),
            Document(
                page_content="RAG (Retrieval-Augmented Generation) combines document retrieval with language generation.",
                metadata={"source": "rag.txt", "topic": "AI"},
            ),
            Document(
                page_content="The weather today is sunny with temperatures around 75 degrees Fahrenheit.",
                metadata={"source": "weather.txt", "topic": "weather"},
            ),
            Document(
                page_content="Italian cuisine includes pasta, pizza, and various regional specialties.",
                metadata={"source": "food.txt", "topic": "cuisine"},
            ),
        ]

    def test_base_rag_agent(self, test_documents, llm_config):
        """Test BaseRAGAgent functionality."""
        agent = BaseRAGAgent.from_documents(
            documents=test_documents, name="Test Base RAG"
        )

        result = agent.run({"query": "What is Python?"})

        assert result is not None
        assert "retrieved_documents" in result

    def test_simple_rag_agent(self, test_documents, llm_config):
        """Test SimpleRAGAgent workflow."""
        agent = SimpleRAGAgent.from_documents(
            documents=test_documents, llm_config=llm_config
        )

        result = agent.run({"query": "Tell me about machine learning"})

        assert result is not None
        # Should have both retrieval and answer generation
        assert len(agent.agents) == 2

    def test_corrective_rag_agent(self, test_documents, llm_config):
        """Test CorrectiveRAGAgentV2 with document grading."""
        agent = CorrectiveRAGAgentV2.from_documents(
            documents=test_documents, llm_config=llm_config, relevance_threshold=0.7
        )

        # Test with relevant query
        result = agent.run({"query": "What is RAG in AI?"})
        assert result is not None

        # Test with irrelevant query (should trigger alternative paths)
        result2 = agent.run({"query": "What is quantum computing?"})
        assert result2 is not None


    def test_hyde_rag_agent(self, test_documents, llm_config):
        """Test HyDERAGAgentV2 with hypothetical document generation."""
        agent = HyDERAGAgentV2.from_documents(
            documents=test_documents, llm_config=llm_config
        )

        result = agent.run({"query": "How does retrieval help language models?"})

        assert result is not None
        # Should generate hypothetical document first
        assert len(agent.agents) == 3

    def test_multi_query_rag_agent(self, test_documents, llm_config):
        """Test MultiQueryRAGAgent with query expansion."""
        agent = MultiQueryRAGAgent.from_documents(
            documents=test_documents, llm_config=llm_config
        )

        result = agent.run({"query": "programming languages"})

        assert result is not None
        # Should have query expansion
        if "query_variations" in result:
            assert isinstance(result["query_variations"], dict)

    def test_adaptive_rag_agent(self, test_documents, llm_config):
        """Test AdaptiveRAGAgent with complexity routing."""
        agent = AdaptiveRAGAgent.from_documents(
            documents=test_documents, llm_config=llm_config
        )

        # Test simple query
        result1 = agent.run({"query": "What is Python?"})
        assert result1 is not None

        # Test complex query
        result2 = agent.run(
            {"query": "Compare and contrast different approaches to machine learning"}
        )
        assert result2 is not None


    def test_memory_aware_rag_agent(self, test_documents, llm_config):
        """Test MemoryAwareRAGAgent with conversation history."""
        agent = MemoryAwareRAGAgent.from_documents(
            documents=test_documents, llm_config=llm_config
        )

        # Test with conversation history
        messages = [
            HumanMessage(content="I'm interested in programming"),
            AIMessage(content="Great! Programming is a valuable skill."),
            HumanMessage(content="Tell me more about it"),  # Context from history
        ]

        result = agent.run({"messages": messages, "query": "Tell me more about it"})

        assert result is not None

    def test_rag_comparison(self, test_documents, llm_config):
        """Compare different RAG strategies on the same query."""
        query = "What are the main applications of machine learning?"

        # Create all agents
        agents = {
            "Simple": SimpleRAGAgent.from_documents(test_documents, llm_config),
            "Corrective": CorrectiveRAGAgentV2.from_documents(
                test_documents, llm_config
            ),
            "HyDE": HyDERAGAgentV2.from_documents(test_documents, llm_config),
            "MultiQuery": MultiQueryRAGAgent.from_documents(test_documents, llm_config),
        }

        results = {}
        for name, agent in agents.items():
            try:
                agent.run({"query": query})
                results[name] = "✅ Success"
            except Exception as e:
                results[name] = f"❌ Failed: {str(e)[:50]}"

        for name, status in results.items():
            pass

        # At least some should succeed
        success_count = sum(1 for r in results.values() if "Success" in r)
        assert success_count >= 2, "At least 2 RAG strategies should succeed"

    def test_edge_cases(self, llm_config):
        """Test edge cases for RAG agents."""
        # Empty documents
        empty_docs = []

        # Single document
        single_doc = [Document(page_content="Test content")]

        # Test SimpleRAG with edge cases
        try:
            agent1 = SimpleRAGAgent.from_documents(empty_docs, llm_config)
            agent1.run({"query": "test"})
        except Exception as e:
            passe}")

        try:
            agent2 = SimpleRAGAgent.from_documents(single_doc, llm_config)
            agent2.run({"query": "test"})
        except Exception as e:
            passe}")


if __name__ == "__main__":
    # Run with specific test
    pytest.main([__file__, "-v", "-k", "test_rag_comparison"])
