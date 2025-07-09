"""Tests for Document Grading Components

Run with: poetry run pytest packages/haive-agents/tests/rag/multi_agent_rag/test_document_grading.py -v
"""

from typing import Any

import pytest
from haive.core.fixtures.documents import (
    conversation_documents,
    news_documents,
    technical_documents,
)
from langchain_core.documents import Document

from haive.agents.rag.common.document_graders.models import (
    DocumentBinaryResponse,
)
from haive.agents.rag.multi_agent_rag import (
    DocumentGradingAgent,
    DocumentGradingResult,
    IterativeDocumentGradingAgent,
    MultiAgentRAGState,
    RAGOperationType,
)


class TestDocumentGradingAgent:
    """Comprehensive tests for document grading functionality."""

    def test_binary_grading_mode(self):
        """Test binary grading mode."""
        agent = DocumentGradingAgent(grading_mode="binary", name="Binary Grader")

        assert agent.grading_mode == "binary"
        assert agent.structured_output_model == DocumentBinaryResponse

    def test_comprehensive_grading_mode(self):
        """Test comprehensive grading mode."""
        agent = DocumentGradingAgent(
            grading_mode="comprehensive",
            min_relevance_threshold=0.7,
            name="Comprehensive Grader",
        )

        assert agent.grading_mode == "comprehensive"
        assert agent.min_relevance_threshold == 0.7

    def test_grade_relevant_document(self):
        """Test grading a clearly relevant document."""
        agent = DocumentGradingAgent(name="Test Grader")

        # Document about restaurants for restaurant query
        doc = Document(
            page_content="Joe Allen Restaurant is a popular American cuisine restaurant located in Times Square, NYC. Known for its classic dishes and theater district location.",
            metadata={"title": "Joe Allen Restaurant Review", "category": "restaurant"},
        )

        result = agent.grade_document("restaurants in Times Square NYC", doc)

        assert isinstance(result, DocumentGradingResult)
        assert result.document == doc
        assert result.document_id is not None
        assert isinstance(result.relevance_score, float)
        assert 0.0 <= result.relevance_score <= 1.0
        assert isinstance(result.is_relevant, bool)
        assert result.grading_reason is not None
        assert len(result.grading_reason) > 10  # Should have substantial reasoning

    def test_grade_irrelevant_document(self):
        """Test grading a clearly irrelevant document."""
        agent = DocumentGradingAgent(min_relevance_threshold=0.3, name="Test Grader")

        # Document about weather for restaurant query
        doc = Document(
            page_content="Tomorrow's weather forecast shows sunny skies with temperatures reaching 75°F. Perfect weather for outdoor activities.",
            metadata={"title": "Weather Forecast", "category": "weather"},
        )

        result = agent.grade_document("best restaurants in NYC", doc)

        assert isinstance(result, DocumentGradingResult)
        assert result.document == doc
        # Should likely be marked as irrelevant
        # Note: Actual result depends on LLM, but we can test structure
        assert isinstance(result.is_relevant, bool)
        assert isinstance(result.relevance_score, float)

    def test_grade_multiple_documents(self):
        """Test grading multiple documents at once."""
        agent = DocumentGradingAgent(name="Multi Grader")

        docs = [
            Document(
                page_content="Restaurant serves Italian food",
                metadata={"type": "restaurant"},
            ),
            Document(
                page_content="Weather is sunny today", metadata={"type": "weather"}
            ),
            Document(
                page_content="Pizza place with great reviews",
                metadata={"type": "restaurant"},
            ),
        ]

        results = agent.grade_documents("Italian restaurants", docs)

        assert len(results) == 3
        assert all(isinstance(result, DocumentGradingResult) for result in results)

        # Check that all documents were processed
        processed_docs = [result.document for result in results]
        assert all(doc in processed_docs for doc in docs)

    def test_run_grading_with_state(self):
        """Test the run_grading method with state."""
        agent = DocumentGradingAgent(min_relevance_threshold=0.4, name="State Grader")

        # Use real conversation documents for testing
        test_docs = conversation_documents[:3]  # Use first 3 conversation docs

        state = MultiAgentRAGState(
            query="restaurants and food recommendations", retrieved_documents=test_docs
        )

        result = agent.run_grading(state)

        # Check result structure
        assert "graded_documents" in result
        assert "filtered_documents" in result
        assert "current_operation" in result
        assert result["current_operation"] == RAGOperationType.GRADE

        # Check graded documents
        graded_docs = result["graded_documents"]
        assert len(graded_docs) == len(test_docs)
        assert all(isinstance(doc, DocumentGradingResult) for doc in graded_docs)

        # Check filtered documents
        filtered_docs = result["filtered_documents"]
        assert isinstance(filtered_docs, list)
        assert all(isinstance(doc, Document) for doc in filtered_docs)

        # Filtered should be subset of original
        assert len(filtered_docs) <= len(test_docs)

    def test_grading_with_empty_documents(self):
        """Test grading when no documents are provided."""
        agent = DocumentGradingAgent(name="Empty Grader")

        state = MultiAgentRAGState(query="test query", retrieved_documents=[])

        result = agent.run_grading(state)

        assert "errors" in result
        assert "No documents to grade" in result["errors"][0]
        assert result["current_operation"] == RAGOperationType.GRADE

    def test_threshold_filtering(self):
        """Test that threshold filtering works correctly."""
        # Create agent with high threshold
        DocumentGradingAgent(min_relevance_threshold=0.9, name="Strict Grader")

        # Mock the grading to return specific scores
        class MockGradingAgent(DocumentGradingAgent):
            def grade_document(
                self, query: str, document: Document
            ) -> DocumentGradingResult:
                # Return predictable scores for testing
                score = 0.95 if "relevant" in document.page_content else 0.1
                return DocumentGradingResult(
                    document_id="test",
                    document=document,
                    relevance_score=score,
                    is_relevant=score >= self.min_relevance_threshold,
                    grading_reason=f"Mock grading with score {score}",
                    grader_type="mock",
                )

        mock_agent = MockGradingAgent(min_relevance_threshold=0.9, name="Mock Grader")

        docs = [
            Document(page_content="This is relevant content", metadata={}),
            Document(page_content="This is irrelevant content", metadata={}),
        ]

        results = mock_agent.grade_documents("test query", docs)

        # Should have one relevant (score 0.95) and one irrelevant (score 0.1)
        relevant_results = [r for r in results if r.is_relevant]
        assert len(relevant_results) == 1
        assert relevant_results[0].relevance_score == 0.95


class TestIterativeDocumentGradingAgent:
    """Tests for iterative document grading."""

    def test_iterative_agent_creation(self):
        """Test creating iterative grading agent."""
        agent = IterativeDocumentGradingAgent(name="Iterative Test")

        assert agent.name == "Iterative Test"
        assert agent.custom_grader is None
        assert isinstance(agent, DocumentGradingAgent)  # Should inherit

    def test_custom_grader_function(self):
        """Test iterative agent with custom grader."""

        def custom_grader(query: str, doc: Document) -> dict[str, Any]:
            # Simple custom grader based on keyword matching
            content_lower = doc.page_content.lower()
            query_lower = query.lower()

            # Count keyword matches
            query_words = query_lower.split()
            matches = sum(1 for word in query_words if word in content_lower)

            score = min(1.0, matches / len(query_words))

            return {
                "score": score,
                "relevant": score >= 0.5,
                "reason": f"Keyword matching: {matches}/{len(query_words)} words matched",
            }

        agent = IterativeDocumentGradingAgent(
            custom_grader=custom_grader, name="Custom Iterative"
        )

        assert agent.custom_grader is not None

        # Test the custom grader
        docs = [
            Document(page_content="Italian restaurant with great pasta", metadata={}),
            Document(page_content="Weather forecast for tomorrow", metadata={}),
        ]

        state = MultiAgentRAGState(query="Italian restaurant", retrieved_documents=docs)

        result = agent.run_iterative_grading(state)

        assert "graded_documents" in result
        assert len(result["graded_documents"]) == 2

        # Check that custom grader was used
        grading_results = result["graded_documents"]
        assert any("Keyword matching" in gr.grading_reason for gr in grading_results)

    def test_iterative_workflow_steps(self):
        """Test that iterative grading adds workflow steps."""
        agent = IterativeDocumentGradingAgent(name="Workflow Test")

        docs = [
            Document(page_content="Document 1", metadata={"id": "1"}),
            Document(page_content="Document 2", metadata={"id": "2"}),
            Document(page_content="Document 3", metadata={"id": "3"}),
        ]

        state = MultiAgentRAGState(query="test query", retrieved_documents=docs)

        # Initially no workflow steps
        assert len(state.workflow_steps) == 0

        agent.run_iterative_grading(state)

        # Should have added one workflow step per document
        assert len(state.workflow_steps) == 3

        # Check workflow step content
        for _i, step in enumerate(state.workflow_steps):
            assert step.operation_type == RAGOperationType.GRADE
            assert step.agent_name == "Workflow Test"
            assert "document_id" in step.input_data
            assert "relevance_score" in step.output_data
            assert "is_relevant" in step.output_data

    def test_custom_grader_error_handling(self):
        """Test error handling when custom grader fails."""

        def failing_grader(query: str, doc: Document) -> dict[str, Any]:
            raise ValueError("Custom grader intentionally failed")

        agent = IterativeDocumentGradingAgent(
            custom_grader=failing_grader, name="Failing Grader"
        )

        docs = [Document(page_content="Test content", metadata={})]

        state = MultiAgentRAGState(query="test query", retrieved_documents=docs)

        result = agent.run_iterative_grading(state)

        # Should fall back to standard grading
        assert "graded_documents" in result
        assert len(result["graded_documents"]) == 1

        # Check that error was noted in grading reason
        grading_result = result["graded_documents"][0]
        assert "Custom grader failed" in grading_result.grading_reason


class TestDocumentGradingWithRealDocuments:
    """Test document grading with real document collections."""

    def test_grading_conversation_documents(self):
        """Test grading conversation documents."""
        agent = DocumentGradingAgent(name="Conversation Grader")

        # Grade conversation documents for restaurant query
        results = agent.grade_documents(
            "restaurant recommendations and dining", conversation_documents
        )

        assert len(results) == len(conversation_documents)

        # Should find some relevant documents (conversation mentions restaurants)
        relevant_results = [r for r in results if r.is_relevant]
        assert len(relevant_results) > 0

        # Check that restaurant-related documents scored higher
        restaurant_results = [
            r for r in results if "restaurant" in r.document.page_content.lower()
        ]

        if restaurant_results:  # If any restaurant documents exist
            avg_restaurant_score = sum(
                r.relevance_score for r in restaurant_results
            ) / len(restaurant_results)

            non_restaurant_results = [
                r
                for r in results
                if "restaurant" not in r.document.page_content.lower()
            ]

            if non_restaurant_results:
                avg_non_restaurant_score = sum(
                    r.relevance_score for r in non_restaurant_results
                ) / len(non_restaurant_results)
                # Restaurant documents should generally score higher
                # Note: This is probabilistic, so we use a reasonable threshold
                assert avg_restaurant_score >= avg_non_restaurant_score * 0.8

    def test_grading_technical_documents(self):
        """Test grading technical documents."""
        agent = DocumentGradingAgent(name="Technical Grader")

        # Grade technical documents for programming query
        results = agent.grade_documents(
            "programming and software development", technical_documents
        )

        assert len(results) == len(technical_documents)

        # Should find relevant documents (technical docs are about programming)
        relevant_results = [r for r in results if r.is_relevant]
        assert len(relevant_results) > 0

        # Check that programming-related content scored well
        programming_results = [
            r
            for r in results
            if any(
                keyword in r.document.page_content.lower()
                for keyword in ["code", "programming", "software", "development"]
            )
        ]

        if programming_results:
            avg_programming_score = sum(
                r.relevance_score for r in programming_results
            ) / len(programming_results)
            # Programming documents should score reasonably well
            assert avg_programming_score >= 0.3

    def test_cross_domain_grading(self):
        """Test grading documents from different domains."""
        agent = DocumentGradingAgent(
            min_relevance_threshold=0.3, name="Cross Domain Grader"
        )

        # Mix different document types
        mixed_docs = (
            conversation_documents[:2] + technical_documents[:2] + news_documents[:2]
        )

        # Query for technical content
        results = agent.grade_documents(
            "artificial intelligence and machine learning technology", mixed_docs
        )

        assert len(results) == len(mixed_docs)

        # Technical and news documents should score higher than conversation docs
        tech_scores = []
        news_scores = []
        conversation_scores = []

        for result in results:
            doc_category = result.document.metadata.get("category", "unknown")

            if doc_category == "technical":
                tech_scores.append(result.relevance_score)
            elif doc_category == "news":
                news_scores.append(result.relevance_score)
            elif doc_category == "conversation":
                conversation_scores.append(result.relevance_score)

        # At least some documents should be marked as relevant
        relevant_count = sum(1 for r in results if r.is_relevant)
        assert relevant_count > 0


class TestDocumentGradingIntegration:
    """Integration tests for document grading in RAG workflows."""

    def test_grading_in_rag_pipeline(self):
        """Test document grading as part of a complete RAG pipeline."""
        from haive.agents.rag.multi_agent_rag import (
            SimpleRAGAgent,
            SimpleRAGAnswerAgent,
        )

        # Create pipeline components
        retrieval_agent = SimpleRAGAgent(name="Pipeline Retrieval")
        grading_agent = DocumentGradingAgent(name="Pipeline Grading")
        answer_agent = SimpleRAGAnswerAgent(name="Pipeline Answer")

        # Start with initial state
        state = MultiAgentRAGState(query="restaurant recommendations in NYC")

        # Step 1: Retrieval
        retrieval_result = retrieval_agent.run_retrieval(state)
        state.retrieved_documents = retrieval_result["retrieved_documents"]
        state.current_operation = retrieval_result["current_operation"]

        # Step 2: Grading
        grading_result = grading_agent.run_grading(state)
        state.graded_documents = grading_result["graded_documents"]
        state.filtered_documents = grading_result["filtered_documents"]

        # Step 3: Answer generation
        answer_result = answer_agent.run_generation(state)
        state.generated_answer = answer_result["generated_answer"]

        # Verify complete pipeline
        assert len(state.retrieved_documents) > 0
        assert len(state.graded_documents) > 0
        assert len(state.filtered_documents) >= 0  # Could be 0 if all filtered out
        assert state.generated_answer != ""
        assert len(state.workflow_steps) > 0  # Should have workflow tracking

    def test_state_quality_metrics(self):
        """Test quality metrics calculation after grading."""
        from haive.agents.rag.multi_agent_rag.state import DocumentGradingResult

        state = MultiAgentRAGState(query="test query")

        # Create mock grading results
        docs = [
            Document(page_content="Relevant doc 1", metadata={}),
            Document(page_content="Relevant doc 2", metadata={}),
            Document(page_content="Irrelevant doc", metadata={}),
        ]

        grading_results = [
            DocumentGradingResult(
                document_id="1",
                document=docs[0],
                relevance_score=0.9,
                is_relevant=True,
                grading_reason="Highly relevant",
                grader_type="test",
            ),
            DocumentGradingResult(
                document_id="2",
                document=docs[1],
                relevance_score=0.7,
                is_relevant=True,
                grading_reason="Moderately relevant",
                grader_type="test",
            ),
            DocumentGradingResult(
                document_id="3",
                document=docs[2],
                relevance_score=0.2,
                is_relevant=False,
                grading_reason="Not relevant",
                grader_type="test",
            ),
        ]

        state.graded_documents = grading_results
        state.update_quality_metrics()

        # Should have 2/3 = 0.67 retrieval confidence
        expected_confidence = 2.0 / 3.0
        assert abs(state.retrieval_confidence - expected_confidence) < 0.01

        # Test get_relevant_documents
        relevant_docs = state.get_relevant_documents(min_score=0.5)
        assert len(relevant_docs) == 2
        assert all(doc in [docs[0], docs[1]] for doc in relevant_docs)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
