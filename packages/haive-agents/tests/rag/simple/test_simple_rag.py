"""Test Simple RAG Workflow.

Tests the SimpleRAGAgent that uses SequentialAgent to compose
BaseRAGAgent with answer generation.
Uses core fixtures - no mocks.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents

from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.simple import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


class TestSimpleRAGAgent:
    """Test the SimpleRAGAgent workflow."""

    def test_rag_creation_with_documents(self):
        """Test creating SimpleRAG workflow with conversation documents."""
        # Use real fixtures from haive-core
        rag = SimpleRAGAgent.from_documents(conversation_documents)

        assert rag.name == "Simple RAG Agent"
        assert len(rag.agents) == 2

        # Check that first agent is BaseRAGAgent
        first_agent = rag.agents[0]
        assert isinstance(first_agent, BaseRAGAgent)
        assert (
            "retriever" in first_agent.name.lower() or "rag" in first_agent.name.lower()
        )

        # Check that second agent is SimpleAgent
        second_agent = rag.agents[1]
        assert isinstance(second_agent, SimpleAgent)
        assert "answer" in second_agent.name.lower()

    def test_rag_creation_empty_documents(self):
        """Test creating RAG with empty document list."""
        rag = SimpleRAGAgent.from_documents([])
        assert len(rag.agents) == 2

    def test_rag_run_basic_query(self):
        """Test running SimpleRAG workflow with a basic query."""
        # Skip if no documents available
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = SimpleRAGAgent.from_documents(
            conversation_documents[:3]
        )  # Use subset for speed

        # Test the run_rag convenience method
        query = "Tell me about restaurants"

        try:
            result = rag.run_rag(query)

            # Basic checks - should have some result
            assert result is not None
            assert isinstance(result, dict)

            # Should contain retrieved information
            if "retrieved_documents" in result:
                assert isinstance(result["retrieved_documents"], list)

        except Exception as e:
            pytest.fail(f"SimpleRAG workflow failed: {e}")

    def test_rag_workflow_integration(self):
        """Test full workflow integration."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = SimpleRAGAgent.from_documents(conversation_documents)

        # Test with standard input format
        input_data = {
            "query": "What restaurants are mentioned?",
            "messages": [
                {"role": "user", "content": "What restaurants are mentioned?"}
            ],
        }

        try:
            result = rag.run(input_data)

            # Workflow should complete without errors
            assert result is not None

        except Exception as e:
            pytest.fail(f"SimpleRAG integration failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
