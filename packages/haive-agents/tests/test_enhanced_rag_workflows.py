"""Tests for Enhanced RAG Workflows.

Tests the new multi-agent RAG workflows with state management,
callable nodes, and compatibility features.
"""

import pytest
from haive.core.fixtures.documents import conversation_documents
from haive.core.schema.prebuilt.rag_state import MultiAgentRAGState
from langchain_core.messages import HumanMessage

from haive.agents.rag.multi_agent_rag.enhanced_workflows import (
    CorrectiveRAGAgent,
    DocumentGradingAgent,
    HYDERAGAgent,
    SelfRAGAgent,
    create_enhanced_rag_workflow,
)


class TestRAGState:
    """Test the RAG state management."""

    def test_rag_state_basic(self):
        """Test basic RAG state functionality."""
        state = MultiAgentRAGState()

        # Test query handling
        state.query = "What are good restaurants?"
        assert state.query == "What are good restaurants?"

        # Test document handling
        state.retrieved_documents = conversation_documents[:3]
        assert len(state.retrieved_documents) == 3
        assert len(state.documents) == 3  # Alias should work

    def test_document_grading(self):
        """Test document grading functionality."""
        state = MultiAgentRAGState()
        state.retrieved_documents = conversation_documents[:2]

        # Grade first document as relevant
        state.grade_document(0, 0.8, True, "Contains restaurant information")

        # Grade second document as not relevant
        state.grade_document(1, 0.2, False, "Not about restaurants")

        assert len(state.graded_documents) == 2
        assert state.graded_documents[0].is_relevant
        assert not state.graded_documents[1].is_relevant

        # Test relevance ratio
        ratio = state.get_graded_relevance_ratio()
        assert ratio == 0.5  # 1 relevant out of 2

        # Test relevant documents filtering
        relevant_docs = state.relevant_documents
        assert len(relevant_docs) == 1

    def test_requery_logic(self):
        """Test requery decision logic."""
        state = MultiAgentRAGState()
        state.retrieved_documents = conversation_documents[:3]

        # Grade all as irrelevant
        for i in range(3):
            state.grade_document(i, 0.1, False)

        # Should need requery with low relevance
        assert state.should_requery()

        # Grade all as relevant
        state.graded_documents = []
        for i in range(3):
            state.grade_document(i, 0.9, True)

        # Should not need requery with high relevance
        assert not state.should_requery()

        # Test retrieval limit
        state.retrieval_count = 3
        state.max_retrievals = 3
        assert not state.should_requery()  # Hit limit


class TestDocumentGradingAgent:
    """Test the document grading agent."""

    def test_grading_agent_creation(self):
        """Test creating a document grading agent."""
        agent = DocumentGradingAgent()
        assert agent.name == "Document Grading Agent"
        assert agent.graph is not None

    def test_grading_agent_run(self):
        """Test running the document grading agent."""
        agent = DocumentGradingAgent()

        # Create initial state with query and documents
        state = MultiAgentRAGState(
            query="restaurants in Times Square",
            retrieved_documents=conversation_documents[:3],
        )

        # Run the agent
        result = agent.run(state, debug=True)

        # Should have graded documents
        assert hasattr(result, "graded_documents")
        # Note: With simple_document_grader, we expect some grades
        # The exact results depend on the grading logic


class TestCorrectiveRAGAgent:
    """Test the Corrective RAG (CRAG) agent."""

    def test_crag_agent_creation(self):
        """Test creating a CRAG agent."""
        agent = CorrectiveRAGAgent(documents=conversation_documents)
        assert agent.name == "Corrective RAG Agent"
        assert len(agent.agents) == 4  # retrieval, grading, requery, answer

    def test_crag_workflow(self):
        """Test CRAG workflow execution."""
        agent = CorrectiveRAGAgent(documents=conversation_documents)

        # Create input with a query
        input_data = {
            "messages": [
                HumanMessage(content="What are the best restaurants near Times Square?")
            ],
            "query": "What are the best restaurants near Times Square?",
        }

        # Run the workflow
        result = agent.run(input_data, debug=True)

        # Should have messages and some workflow state
        assert hasattr(result, "messages")
        assert hasattr(result, "query")


class TestHYDERAGAgent:
    """Test the HYDE RAG agent."""

    def test_hyde_agent_creation(self):
        """Test creating a HYDE RAG agent."""
        agent = HYDERAGAgent(documents=conversation_documents)
        assert agent.name == "HYDE RAG Agent"
        assert len(agent.agents) == 3  # hypothesis, retrieval, answer

    def test_hyde_workflow(self):
        """Test HYDE workflow execution."""
        agent = HYDERAGAgent(documents=conversation_documents)

        input_data = {
            "messages": [
                HumanMessage(content="What are popular restaurant types in NYC?")
            ],
            "query": "What are popular restaurant types in NYC?",
        }

        result = agent.run(input_data, debug=True)

        assert hasattr(result, "messages")
        assert hasattr(result, "query")


class TestSelfRAGAgent:
    """Test the Self-RAG agent."""

    def test_self_rag_agent_creation(self):
        """Test creating a Self-RAG agent."""
        agent = SelfRAGAgent(documents=conversation_documents)
        assert agent.name == "Self-RAG Agent"
        assert len(agent.agents) == 4  # decision, retrieval, relevance, generation

    def test_self_rag_workflow(self):
        """Test Self-RAG workflow execution."""
        agent = SelfRAGAgent(documents=conversation_documents)

        input_data = {
            "messages": [
                HumanMessage(content="How do I make a restaurant reservation?")
            ],
            "query": "How do I make a restaurant reservation?",
        }

        result = agent.run(input_data, debug=True)

        assert hasattr(result, "messages")
        assert hasattr(result, "query")


class TestWorkflowFactory:
    """Test the workflow factory function."""

    def test_create_crag_workflow(self):
        """Test creating CRAG workflow via factory."""
        agent = create_enhanced_rag_workflow("crag", documents=conversation_documents)
        assert isinstance(agent, CorrectiveRAGAgent)

    def test_create_hyde_workflow(self):
        """Test creating HYDE workflow via factory."""
        agent = create_enhanced_rag_workflow("hyde", documents=conversation_documents)
        assert isinstance(agent, HYDERAGAgent)

    def test_create_self_rag_workflow(self):
        """Test creating Self-RAG workflow via factory."""
        agent = create_enhanced_rag_workflow(
            "self_rag", documents=conversation_documents
        )
        assert isinstance(agent, SelfRAGAgent)

    def test_invalid_workflow_type(self):
        """Test error handling for invalid workflow types."""
        with pytest.raises(ValueError, match="Unknown workflow type"):
            create_enhanced_rag_workflow("invalid_type")


class TestIntegration:
    """Integration tests for the complete workflow."""

    def test_end_to_end_crag(self):
        """Test end-to-end CRAG workflow."""
        # Create CRAG agent
        agent = CorrectiveRAGAgent(documents=conversation_documents)

        # Prepare realistic input
        input_data = {
            "messages": [
                HumanMessage(
                    content="I need to find a good Italian restaurant near Times Square for dinner tonight. Can you help me with recommendations and booking?"
                )
            ],
            "query": "Italian restaurant near Times Square dinner reservations",
        }

        # Run with debug enabled
        result = agent.run(input_data, debug=True)

        # Verify we got a proper result
        assert result is not None
        assert hasattr(result, "messages")
        assert len(result.messages) > 0

        # The workflow should have processed the query
        assert hasattr(result, "query")
        assert result.query != ""

    def test_compatibility_between_workflows(self):
        """Test that different workflow types can work with the same state."""
        # Create different workflow types
        crag_agent = create_enhanced_rag_workflow(
            "crag", documents=conversation_documents[:5]
        )
        hyde_agent = create_enhanced_rag_workflow(
            "hyde", documents=conversation_documents[:5]
        )

        # Test that they can both use MultiAgentRAGState
        assert crag_agent.state_schema == MultiAgentRAGState
        assert hyde_agent.state_schema == MultiAgentRAGState

        # Test that they produce compatible outputs
        input_data = {
            "messages": [HumanMessage(content="What's a good restaurant?")],
            "query": "What's a good restaurant?",
        }

        crag_result = crag_agent.run(input_data, debug=True)
        hyde_result = hyde_agent.run(input_data, debug=True)

        # Both should produce results with the expected structure
        for result in [crag_result, hyde_result]:
            assert hasattr(result, "messages")
            assert hasattr(result, "query")


if __name__ == "__main__":
    # Run a quick test

    # Test basic state
    test = TestRAGState()
    test.test_rag_state_basic()
    test.test_document_grading()
    test.test_requery_logic()

    # Test agents
    test_grading = TestDocumentGradingAgent()
    test_grading.test_grading_agent_creation()

    # Test factory
    test_factory = TestWorkflowFactory()
    test_factory.test_create_crag_workflow()
    test_factory.test_create_hyde_workflow()
    test_factory.test_create_self_rag_workflow()
