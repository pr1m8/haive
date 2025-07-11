"""Test Basic Sequential RAG Workflow.

Tests the clean implementation using SequentialAgent and core fixtures.
No mocks - real integration testing.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents

from haive.agents.rag.workflows.basic_sequential import AnswerAgent, BasicSequentialRAG


class TestAnswerAgent:
    """Test the AnswerAgent component."""

    def test_answer_agent_creation(self):
        """Test creating AnswerAgent."""
        agent = AnswerAgent()
        assert agent.name == "Answer Agent"
        assert "comprehensive answers" in agent.system_message

    def test_answer_agent_setup(self):
        """Test agent setup creates proper engine."""
        agent = AnswerAgent()
        agent.setup_agent()  # Should create engine

        assert agent.engine is not None
        assert agent.engine.name == "answer_llm"
        assert agent.engine.model == "gpt-4"
        assert "main" in agent.engines


class TestBasicSequentialRAG:
    """Test the BasicSequentialRAG workflow."""

    def test_rag_creation_with_documents(self):
        """Test creating RAG workflow with conversation documents."""
        # Use real fixtures from haive-core
        rag = BasicSequentialRAG.from_documents(conversation_documents)

        assert rag.name == "Basic Sequential RAG"
        assert len(rag.agents) == 2

        # Check agent types
        agent_names = list(rag.agents.keys())
        assert any(
            "retriever" in name.lower() or "rag" in name.lower() for name in agent_names
        )
        assert any("answer" in name.lower() for name in agent_names)

    def test_rag_creation_empty_documents(self):
        """Test creating RAG with empty document list."""
        rag = BasicSequentialRAG.from_documents([])
        assert len(rag.agents) == 2

    def test_rag_run_basic_query(self):
        """Test running RAG workflow with a basic query."""
        # Skip if no documents available
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = BasicSequentialRAG.from_documents(
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
            pytest.fail(f"RAG workflow failed: {e}")

    def test_rag_workflow_integration(self):
        """Test full workflow integration."""
        if not conversation_documents:
            pytest.skip("No conversation_documents available")

        rag = BasicSequentialRAG.from_documents(conversation_documents)

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
            pytest.fail(f"Workflow integration failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
