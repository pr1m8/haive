"""Basic tests for Multi-Agent RAG System.

Run with: poetry run pytest packages/haive-agents/tests/rag/multi_agent_rag/test_multi_agent_rag_basic.py -v
"""

import pytest
from langchain_core.documents import Document

from haive.agents.rag.multi_agent_rag import (
    SIMPLE_RAG_AGENT,
    SIMPLE_RAG_ANSWER_AGENT,
    BaseRAGMultiAgent,
    ConditionalRAGMultiAgent,
    DocumentGradingAgent,
    IterativeDocumentGradingAgent,
    MultiAgentRAGState,
    QueryStatus,
    RAGOperationType,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
    agent_list,
    base_rag_agent,
)


class TestMultiAgentRAGState:
    """Test the RAG state schema."""

    def test_state_creation(self):
        """Test creating RAG state."""
        state = MultiAgentRAGState(query="Test query")
        assert state.query == "Test query"
        assert state.query_status == QueryStatus.PENDING
        assert len(state.documents) == 0
        assert len(state.retrieved_documents) == 0

    def test_state_with_documents(self):
        """Test state with documents."""
        test_docs = [
            Document(page_content="Test content 1", metadata={"id": "1"}),
            Document(page_content="Test content 2", metadata={"id": "2"}),
        ]

        state = MultiAgentRAGState(
            query="Test query", documents=test_docs, retrieved_documents=test_docs[:1]
        )

        assert len(state.documents) == 2
        assert len(state.retrieved_documents) == 1
        assert state.documents[0].page_content == "Test content 1"

    def test_workflow_step_addition(self):
        """Test adding workflow steps."""
        state = MultiAgentRAGState(query="Test query")

        step_id = state.add_workflow_step(
            operation_type=RAGOperationType.RETRIEVE,
            agent_name="TestAgent",
            input_data={"query": "test"},
            output_data={"docs_found": 5},
        )

        assert len(state.workflow_steps) == 1
        assert state.workflow_steps[0].operation_type == RAGOperationType.RETRIEVE
        assert state.workflow_steps[0].agent_name == "TestAgent"
        assert step_id is not None

    def test_quality_metrics_update(self):
        """Test quality metrics calculation."""
        from haive.agents.rag.multi_agent_rag.state import DocumentGradingResult

        state = MultiAgentRAGState(query="Test query")

        # Add some graded documents
        doc = Document(page_content="Test", metadata={"id": "1"})
        grading_result = DocumentGradingResult(
            document_id="1",
            document=doc,
            relevance_score=0.8,
            is_relevant=True,
            grading_reason="Relevant content",
            grader_type="test",
        )

        state.graded_documents = [grading_result]
        state.update_quality_metrics()

        assert state.retrieval_confidence == 1.0  # 1/1 relevant

    def test_should_refine_query(self):
        """Test query refinement logic."""
        state = MultiAgentRAGState(query="Test query")

        # Low confidence should trigger refinement
        state.retrieval_confidence = 0.2
        assert state.should_refine_query()

        # High confidence should not trigger refinement
        state.retrieval_confidence = 0.8
        assert not state.should_refine_query()


class TestSimpleRAGAgent:
    """Test the Simple RAG Agent."""

    def test_agent_creation(self):
        """Test creating SimpleRAGAgent."""
        agent = SimpleRAGAgent(name="Test RAG Agent")
        assert agent.name == "Test RAG Agent"
        assert len(agent.documents) > 0  # Should have conversation_documents

    def test_agent_with_custom_documents(self):
        """Test agent with custom documents."""
        custom_docs = [
            Document(page_content="Custom content", metadata={"source": "test"})
        ]

        agent = SimpleRAGAgent.from_documents(
            documents=custom_docs, name="Custom RAG Agent"
        )

        assert agent.name == "Custom RAG Agent"
        assert len(agent.documents) == 1
        assert agent.documents[0].page_content == "Custom content"

    def test_document_retrieval(self):
        """Test document retrieval functionality."""
        agent = SimpleRAGAgent(name="Test Agent")

        # Test retrieval with a query that should match conversation docs
        retrieved = agent.retrieve_documents("restaurant")

        assert isinstance(retrieved, list)
        assert len(retrieved) > 0
        assert all(isinstance(doc, Document) for doc in retrieved)

    def test_run_retrieval(self):
        """Test the run_retrieval method."""
        agent = SimpleRAGAgent(name="Test Agent")
        state = MultiAgentRAGState(query="restaurant near Times Square")

        result = agent.run_retrieval(state)

        assert "retrieved_documents" in result
        assert "current_operation" in result
        assert result["current_operation"] == RAGOperationType.RETRIEVE
        assert "retrieval_confidence" in result


class TestSimpleRAGAnswerAgent:
    """Test the Simple RAG Answer Agent."""

    def test_agent_creation(self):
        """Test creating SimpleRAGAnswerAgent."""
        agent = SimpleRAGAnswerAgent(name="Test Answer Agent")
        assert agent.name == "Test Answer Agent"
        assert not agent.use_citations

    def test_agent_with_citations(self):
        """Test agent with citations enabled."""
        agent = SimpleRAGAnswerAgent(use_citations=True, name="Citation Agent")
        assert agent.use_citations

    def test_run_generation_with_documents(self):
        """Test answer generation with documents."""
        agent = SimpleRAGAnswerAgent(name="Test Agent")

        test_docs = [
            Document(page_content="The restaurant serves Italian food", metadata={}),
            Document(page_content="It's located in Times Square", metadata={}),
        ]

        state = MultiAgentRAGState(
            query="What type of food does the restaurant serve?",
            retrieved_documents=test_docs,
        )

        result = agent.run_generation(state)

        assert "generated_answer" in result
        assert "current_operation" in result
        assert result["current_operation"] == RAGOperationType.GENERATE
        assert "generation_confidence" in result

    def test_run_generation_no_documents(self):
        """Test generation with no documents."""
        agent = SimpleRAGAnswerAgent(name="Test Agent")
        state = MultiAgentRAGState(query="Test query")

        result = agent.run_generation(state)

        assert "generated_answer" in result
        assert "No relevant documents found" in result["generated_answer"]
        assert "errors" in result


class TestDocumentGradingAgent:
    """Test the Document Grading Agent."""

    def test_agent_creation(self):
        """Test creating DocumentGradingAgent."""
        agent = DocumentGradingAgent(name="Test Grader")
        assert agent.name == "Test Grader"
        assert agent.grading_mode == "binary"
        assert agent.min_relevance_threshold == 0.5

    def test_agent_with_custom_threshold(self):
        """Test agent with custom threshold."""
        agent = DocumentGradingAgent(min_relevance_threshold=0.8, name="Strict Grader")
        assert agent.min_relevance_threshold == 0.8

    def test_grade_document(self):
        """Test single document grading."""
        agent = DocumentGradingAgent(name="Test Grader")

        doc = Document(
            page_content="This document discusses restaurants in New York",
            metadata={"title": "NYC Restaurants"},
        )

        result = agent.grade_document("restaurants in NYC", doc)

        assert result.document_id is not None
        assert result.document == doc
        assert isinstance(result.relevance_score, float)
        assert isinstance(result.is_relevant, bool)
        assert result.grading_reason is not None
        assert result.grader_type == "binary"

    def test_run_grading(self):
        """Test the run_grading method."""
        agent = DocumentGradingAgent(name="Test Grader")

        test_docs = [
            Document(page_content="Restaurant information", metadata={}),
            Document(page_content="Weather forecast", metadata={}),
        ]

        state = MultiAgentRAGState(
            query="restaurant recommendations", retrieved_documents=test_docs
        )

        result = agent.run_grading(state)

        assert "graded_documents" in result
        assert "filtered_documents" in result
        assert "current_operation" in result
        assert result["current_operation"] == RAGOperationType.GRADE
        assert len(result["graded_documents"]) == 2


class TestIterativeDocumentGradingAgent:
    """Test the Iterative Document Grading Agent."""

    def test_agent_creation(self):
        """Test creating IterativeDocumentGradingAgent."""
        agent = IterativeDocumentGradingAgent(name="Iterative Grader")
        assert agent.name == "Iterative Grader"
        assert agent.custom_grader is None

    def test_agent_with_custom_grader(self):
        """Test agent with custom grader function."""

        def custom_grader(query: str, document: Document) -> dict:
            return {"score": 0.9, "relevant": True, "reason": "Custom grading result"}

        agent = IterativeDocumentGradingAgent(
            custom_grader=custom_grader, name="Custom Grader"
        )
        assert agent.custom_grader is not None

    def test_run_iterative_grading(self):
        """Test iterative grading process."""
        agent = IterativeDocumentGradingAgent(name="Iterative Test")

        test_docs = [
            Document(page_content="Document 1", metadata={"id": "1"}),
            Document(page_content="Document 2", metadata={"id": "2"}),
        ]

        state = MultiAgentRAGState(query="test query", retrieved_documents=test_docs)

        result = agent.run_iterative_grading(state)

        assert "graded_documents" in result
        assert "filtered_documents" in result
        assert len(result["graded_documents"]) == 2
        # Should have added workflow steps for each document
        assert len(state.workflow_steps) == 2


class TestPredefinedAgents:
    """Test the predefined agent instances."""

    def test_simple_rag_agent(self):
        """Test SIMPLE_RAG_AGENT instance."""
        assert SIMPLE_RAG_AGENT is not None
        assert hasattr(SIMPLE_RAG_AGENT, "documents")
        assert len(SIMPLE_RAG_AGENT.documents) > 0

    def test_simple_rag_answer_agent(self):
        """Test SIMPLE_RAG_ANSWER_AGENT instance."""
        assert SIMPLE_RAG_ANSWER_AGENT is not None
        assert hasattr(SIMPLE_RAG_ANSWER_AGENT, "engine")

    def test_agent_list(self):
        """Test the agent_list."""
        assert agent_list is not None
        assert len(agent_list) == 2
        assert agent_list[0] == SIMPLE_RAG_AGENT
        assert agent_list[1] == SIMPLE_RAG_ANSWER_AGENT


class TestMultiAgentRAGWorkflows:
    """Test multi-agent RAG workflows."""

    def test_base_rag_multi_agent_creation(self):
        """Test creating BaseRAGMultiAgent."""
        system = BaseRAGMultiAgent(name="Test Base RAG")
        assert system.name == "Test Base RAG"
        assert len(system.agents) == 3  # retrieval, grading, answer
        assert system.state_schema == MultiAgentRAGState

    def test_base_rag_agent_instance(self):
        """Test the base_rag_agent instance."""
        assert base_rag_agent is not None
        assert hasattr(base_rag_agent, "agents")
        assert len(base_rag_agent.agents) == 2

    def test_conditional_rag_creation(self):
        """Test creating ConditionalRAGMultiAgent."""
        system = ConditionalRAGMultiAgent(name="Test Conditional RAG")
        assert system.name == "Test Conditional RAG"
        assert len(system.agents) >= 3  # At least retrieval, grading, answer
        assert system.state_schema == MultiAgentRAGState


class TestRAGSystemIntegration:
    """Integration tests for complete RAG workflows."""

    def test_simple_rag_workflow(self):
        """Test a simple end-to-end RAG workflow."""
        # Create a simple workflow
        retrieval_agent = SimpleRAGAgent(name="Test Retrieval")
        answer_agent = SimpleRAGAnswerAgent(name="Test Answer")

        from haive.agents.multi.base import SequentialAgent

        workflow = SequentialAgent(
            agents=[retrieval_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            name="Simple Test Workflow",
        )

        assert len(workflow.agents) == 2
        assert workflow.state_schema == MultiAgentRAGState

    def test_rag_state_flow(self):
        """Test state flowing through RAG components."""
        initial_state = MultiAgentRAGState(query="Find restaurants in NYC")

        # Test retrieval
        retrieval_agent = SimpleRAGAgent(name="Test Retrieval")
        retrieval_result = retrieval_agent.run_retrieval(initial_state)

        # Update state
        initial_state.retrieved_documents = retrieval_result["retrieved_documents"]
        initial_state.current_operation = retrieval_result["current_operation"]

        # Test grading
        grading_agent = DocumentGradingAgent(name="Test Grading")
        grading_result = grading_agent.run_grading(initial_state)

        # Update state
        initial_state.graded_documents = grading_result["graded_documents"]
        initial_state.filtered_documents = grading_result["filtered_documents"]

        # Test generation
        answer_agent = SimpleRAGAnswerAgent(name="Test Answer")
        answer_result = answer_agent.run_generation(initial_state)

        assert "generated_answer" in answer_result
        assert initial_state.query == "Find restaurants in NYC"
        assert len(initial_state.workflow_steps) >= 2  # From iterative grading


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
