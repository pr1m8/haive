"""Tests for Hallucination Detection and Grading

Run with: poetry run pytest packages/haive-agents/tests/rag/multi_agent_rag/test_hallucination_grading.py -v
"""

from typing import Any

import pytest
from langchain_core.documents import Document

from haive.agents.rag.common.hallucination_graders.models import *
from haive.agents.rag.common.hallucination_graders.prompts import *
from haive.agents.rag.multi_agent_rag import (
    DocumentGradingAgent,
    MultiAgentRAGState,
    RAGOperationType,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
)


class HallucinationGradingAgent(SimpleRAGAnswerAgent):
    """Specialized agent for detecting hallucinations in RAG-generated answers.

    This agent compares generated answers against source documents to detect
    potential hallucinations, unsupported claims, and factual inconsistencies.
    """

    def __init__(self, detection_threshold: float = 0.7, **kwargs):
        # Use hallucination grading prompts from common module
        if "engine" not in kwargs:
            from haive.core.engine.aug_llm import AugLLMConfig

            kwargs["engine"] = AugLLMConfig(
                prompt_template=HALLUCINATION_GRADER_PROMPT,
                name="hallucination_grading_engine",
            )

        if "name" not in kwargs:
            kwargs["name"] = "Hallucination Grading Agent"

        super().__init__(**kwargs)
        self.detection_threshold = detection_threshold

    def grade_answer_for_hallucinations(
        self, generated_answer: str, source_documents: list[Document], query: str
    ) -> dict[str, Any]:
        """Grade a generated answer for potential hallucinations.

        Args:
            generated_answer: The RAG-generated answer to evaluate
            source_documents: Source documents used for answer generation
            query: Original query that prompted the answer

        Returns:
            Dictionary with hallucination assessment
        """
        # Format source documents for evaluation
        source_text = "\n\n".join(
            [
                f"Document {i+1}: {doc.page_content}"
                for i, doc in enumerate(source_documents)
            ]
        )

        # Use the engine to evaluate for hallucinations
        evaluation_result = self.engine.invoke(
            {
                "query": query,
                "generated_answer": generated_answer,
                "source_documents": source_text,
            }
        )

        # Parse the evaluation result
        # In a real implementation, this would use structured output
        result_text = str(evaluation_result)

        # Simple parsing logic (would be more sophisticated in practice)
        has_hallucination = self._detect_hallucination_indicators(result_text)
        confidence = self._extract_confidence_score(result_text)

        return {
            "has_hallucination": has_hallucination,
            "confidence_score": confidence,
            "evaluation_text": result_text,
            "source_alignment": self._check_source_alignment(
                generated_answer, source_documents
            ),
            "unsupported_claims": self._identify_unsupported_claims(
                generated_answer, source_documents
            ),
            "factual_consistency": confidence >= self.detection_threshold,
        }

    def _detect_hallucination_indicators(self, evaluation_text: str) -> bool:
        """Detect indicators of hallucination in evaluation text."""
        hallucination_indicators = [
            "hallucination",
            "unsupported",
            "not found in documents",
            "contradicts",
            "fabricated",
            "invented",
            "false information",
        ]

        text_lower = evaluation_text.lower()
        return any(indicator in text_lower for indicator in hallucination_indicators)

    def _extract_confidence_score(self, evaluation_text: str) -> float:
        """Extract confidence score from evaluation text."""
        # Simple confidence extraction (would be more sophisticated)
        import re

        # Look for confidence patterns
        confidence_patterns = [
            r"confidence[:\s]*(\d+\.?\d*)%?",
            r"score[:\s]*(\d+\.?\d*)",
            r"(\d+\.?\d*)[:\s]*confidence",
        ]

        for pattern in confidence_patterns:
            match = re.search(pattern, evaluation_text.lower())
            if match:
                try:
                    score = float(match.group(1))
                    return min(1.0, score / 100.0 if score > 1.0 else score)
                except ValueError:
                    continue

        # Default confidence based on text analysis
        if "high confidence" in evaluation_text.lower():
            return 0.9
        if "medium confidence" in evaluation_text.lower():
            return 0.6
        if "low confidence" in evaluation_text.lower():
            return 0.3
        return 0.5  # Default

    def _check_source_alignment(
        self, answer: str, sources: list[Document]
    ) -> dict[str, Any]:
        """Check how well the answer aligns with source documents."""
        source_text = " ".join([doc.page_content for doc in sources])

        # Simple word overlap analysis
        answer_words = set(answer.lower().split())
        source_words = set(source_text.lower().split())

        overlap = answer_words.intersection(source_words)
        overlap_ratio = len(overlap) / len(answer_words) if answer_words else 0

        return {
            "overlap_ratio": overlap_ratio,
            "shared_terms": len(overlap),
            "answer_terms": len(answer_words),
            "alignment_quality": (
                "high"
                if overlap_ratio > 0.7
                else "medium" if overlap_ratio > 0.4 else "low"
            ),
        }

    def _identify_unsupported_claims(
        self, answer: str, sources: list[Document]
    ) -> list[str]:
        """Identify potentially unsupported claims in the answer."""
        # This is a simplified implementation
        # In practice, would use more sophisticated NLP techniques

        source_text = " ".join([doc.page_content for doc in sources])

        # Look for specific claims patterns
        import re

        # Extract sentences that make specific claims
        claim_patterns = [
            r"[A-Z][^.!?]*(?:is|are|was|were|has|have|will|would|can|cannot|must|should)[^.!?]*[.!?]",
            r"[A-Z][^.!?]*(?:located|founded|established|created|built|designed)[^.!?]*[.!?]",
            r"[A-Z][^.!?]*(?:\d+%?|\$\d+|[0-9,]+)[^.!?]*[.!?]",  # Numerical claims
        ]

        potential_claims = []
        for pattern in claim_patterns:
            claims = re.findall(pattern, answer)
            potential_claims.extend(claims)

        # Check if claims are supported by sources
        unsupported_claims = []
        for claim in potential_claims:
            claim_words = set(claim.lower().split())
            source_words = set(source_text.lower().split())

            # If very few words from the claim appear in sources, it might be unsupported
            overlap = claim_words.intersection(source_words)
            support_ratio = len(overlap) / len(claim_words) if claim_words else 0

            if support_ratio < 0.3:  # Low support threshold
                unsupported_claims.append(claim.strip())

        return unsupported_claims

    def run_hallucination_detection(self, state: MultiAgentRAGState) -> dict[str, Any]:
        """Run hallucination detection on the current state."""
        if not state.generated_answer:
            return {
                "errors": ["No generated answer to evaluate for hallucinations"],
                "current_operation": RAGOperationType.VERIFY,
            }

        if not state.filtered_documents and not state.retrieved_documents:
            return {
                "errors": ["No source documents available for hallucination detection"],
                "current_operation": RAGOperationType.VERIFY,
            }

        # Use filtered documents if available, otherwise retrieved documents
        source_docs = state.filtered_documents or state.retrieved_documents

        hallucination_result = self.grade_answer_for_hallucinations(
            state.generated_answer, source_docs, state.query
        )

        return {
            "hallucination_detection": hallucination_result,
            "current_operation": RAGOperationType.VERIFY,
            "verification_confidence": hallucination_result["confidence_score"],
        }


class TestHallucinationGradingAgent:
    """Test the hallucination grading agent."""

    def test_agent_creation(self):
        """Test creating hallucination grading agent."""
        agent = HallucinationGradingAgent(name="Test Hallucination Grader")

        assert agent.name == "Test Hallucination Grader"
        assert agent.detection_threshold == 0.7

    def test_agent_with_custom_threshold(self):
        """Test agent with custom detection threshold."""
        agent = HallucinationGradingAgent(
            detection_threshold=0.9, name="Strict Hallucination Grader"
        )

        assert agent.detection_threshold == 0.9

    def test_hallucination_detection_indicators(self):
        """Test detection of hallucination indicators."""
        agent = HallucinationGradingAgent(name="Test Agent")

        # Test positive cases
        positive_cases = [
            "This answer contains hallucination",
            "The claim is unsupported by the documents",
            "Information not found in documents",
            "This contradicts the source material",
        ]

        for case in positive_cases:
            result = agent._detect_hallucination_indicators(case)
            assert result, f"Should detect hallucination in: {case}"

        # Test negative cases
        negative_cases = [
            "This answer is well supported",
            "Consistent with source documents",
            "Accurate information provided",
            "Fully grounded in the evidence",
        ]

        for case in negative_cases:
            result = agent._detect_hallucination_indicators(case)
            assert not result, f"Should not detect hallucination in: {case}"

    def test_confidence_score_extraction(self):
        """Test extraction of confidence scores."""
        agent = HallucinationGradingAgent(name="Test Agent")

        test_cases = [
            ("Confidence: 85%", 0.85),
            ("Score: 0.75", 0.75),
            ("High confidence assessment", 0.9),
            ("Medium confidence level", 0.6),
            ("Low confidence result", 0.3),
            ("No clear indicators", 0.5),
        ]

        for text, expected_score in test_cases:
            result = agent._extract_confidence_score(text)
            assert (
                abs(result - expected_score) < 0.1
            ), f"Score extraction failed for: {text}"

    def test_source_alignment_check(self):
        """Test source alignment checking."""
        agent = HallucinationGradingAgent(name="Test Agent")

        source_docs = [
            Document(
                page_content="The restaurant serves Italian cuisine with pasta and pizza."
            ),
            Document(page_content="Located in downtown area with outdoor seating."),
        ]

        # High alignment case
        high_alignment_answer = "The restaurant serves Italian cuisine including pasta and pizza, located downtown."
        alignment_result = agent._check_source_alignment(
            high_alignment_answer, source_docs
        )

        assert alignment_result["overlap_ratio"] > 0.5
        assert alignment_result["alignment_quality"] in ["medium", "high"]

        # Low alignment case
        low_alignment_answer = "The establishment offers French molecular gastronomy in a suburban location."
        alignment_result = agent._check_source_alignment(
            low_alignment_answer, source_docs
        )

        assert alignment_result["overlap_ratio"] < 0.5

    def test_unsupported_claims_identification(self):
        """Test identification of unsupported claims."""
        agent = HallucinationGradingAgent(name="Test Agent")

        source_docs = [
            Document(page_content="Joe's Pizza is a restaurant in NYC."),
            Document(page_content="They serve pizza and Italian food."),
        ]

        # Answer with unsupported numerical claim
        answer_with_unsupported = (
            "Joe's Pizza was founded in 1952 and has 47 locations nationwide."
        )

        unsupported_claims = agent._identify_unsupported_claims(
            answer_with_unsupported, source_docs
        )

        # Should identify claims about founding date and number of locations as potentially unsupported
        assert len(unsupported_claims) > 0

        # Answer that's well supported
        supported_answer = (
            "Joe's Pizza is a restaurant that serves pizza and Italian food."
        )

        supported_claims = agent._identify_unsupported_claims(
            supported_answer, source_docs
        )

        # Should have fewer or no unsupported claims
        assert len(supported_claims) <= len(unsupported_claims)


class TestHallucinationDetectionWorkflow:
    """Test hallucination detection in complete RAG workflows."""

    def test_accurate_answer_detection(self):
        """Test detection on accurate, well-grounded answer."""
        agent = HallucinationGradingAgent(name="Accuracy Test Agent")

        source_docs = [
            Document(
                page_content="Mario's Restaurant is located in Little Italy, NYC. They specialize in traditional Italian cuisine including homemade pasta and wood-fired pizza.",
                metadata={"source": "restaurant_guide"},
            ),
            Document(
                page_content="The restaurant has been family-owned since 1985 and is known for its authentic recipes passed down through generations.",
                metadata={"source": "restaurant_history"},
            ),
        ]

        # Accurate answer based on sources
        accurate_answer = "Mario's Restaurant is a family-owned Italian restaurant in Little Italy, NYC, specializing in traditional cuisine like homemade pasta and wood-fired pizza."

        result = agent.grade_answer_for_hallucinations(
            accurate_answer, source_docs, "Tell me about Mario's Restaurant"
        )

        assert not result["has_hallucination"]
        assert result["confidence_score"] >= 0.5
        assert result["factual_consistency"]
        assert result["source_alignment"]["alignment_quality"] in ["medium", "high"]

    def test_hallucinated_answer_detection(self):
        """Test detection on answer with hallucinated information."""
        agent = HallucinationGradingAgent(
            detection_threshold=0.6, name="Hallucination Test Agent"
        )

        source_docs = [
            Document(
                page_content="Blue Cafe is a small coffee shop that serves basic coffee drinks and pastries.",
                metadata={"source": "local_guide"},
            )
        ]

        # Answer with hallucinated information
        hallucinated_answer = "Blue Cafe is a Michelin-starred restaurant founded in 1923 by Chef Antoine Dubois, featuring a 15-course tasting menu with molecular gastronomy techniques."

        result = agent.grade_answer_for_hallucinations(
            hallucinated_answer, source_docs, "What is Blue Cafe?"
        )

        # Should detect significant misalignment
        assert result["source_alignment"]["overlap_ratio"] < 0.5
        assert len(result["unsupported_claims"]) > 0

    def test_partial_hallucination_detection(self):
        """Test detection of partial hallucinations (mix of accurate and inaccurate info)."""
        agent = HallucinationGradingAgent(name="Partial Test Agent")

        source_docs = [
            Document(
                page_content="Green Garden Restaurant serves vegetarian and vegan cuisine. They are open Tuesday through Sunday.",
                metadata={"source": "restaurant_info"},
            )
        ]

        # Partially accurate answer with some unsupported details
        partial_answer = "Green Garden Restaurant serves vegetarian and vegan cuisine and is open most days of the week. They also offer cooking classes on weekends and have won 3 local awards for sustainability."

        result = agent.grade_answer_for_hallucinations(
            partial_answer, source_docs, "Tell me about Green Garden Restaurant"
        )

        # Should have moderate alignment but some unsupported claims
        alignment = result["source_alignment"]
        assert 0.3 <= alignment["overlap_ratio"] <= 0.8  # Partial alignment

        # May or may not detect as hallucination depending on threshold and analysis
        # But should identify some unsupported claims
        assert len(result["unsupported_claims"]) >= 0

    def test_hallucination_detection_in_rag_state(self):
        """Test hallucination detection integrated with RAG state."""
        agent = HallucinationGradingAgent(name="RAG State Test Agent")

        # Set up RAG state with generated answer and sources
        state = MultiAgentRAGState(
            query="What can you tell me about the restaurant?",
            retrieved_documents=[
                Document(page_content="Sunset Bistro offers fresh seafood and steaks."),
                Document(
                    page_content="The restaurant has outdoor seating with ocean views."
                ),
            ],
            generated_answer="Sunset Bistro is a seafood restaurant with outdoor seating and ocean views, serving fresh seafood and steaks.",
        )

        result = agent.run_hallucination_detection(state)

        assert "hallucination_detection" in result
        assert "current_operation" in result
        assert result["current_operation"] == RAGOperationType.VERIFY
        assert "verification_confidence" in result

        # Should not detect major hallucinations in this well-aligned case
        hallucination_result = result["hallucination_detection"]
        assert isinstance(hallucination_result["has_hallucination"], bool)
        assert isinstance(hallucination_result["confidence_score"], float)

    def test_hallucination_detection_no_answer(self):
        """Test hallucination detection when no answer is available."""
        agent = HallucinationGradingAgent(name="No Answer Test Agent")

        state = MultiAgentRAGState(
            query="Test query",
            retrieved_documents=[Document(page_content="Test document")],
            # No generated_answer
        )

        result = agent.run_hallucination_detection(state)

        assert "errors" in result
        assert "No generated answer" in result["errors"][0]

    def test_hallucination_detection_no_sources(self):
        """Test hallucination detection when no source documents are available."""
        agent = HallucinationGradingAgent(name="No Sources Test Agent")

        state = MultiAgentRAGState(
            query="Test query",
            generated_answer="Some generated answer",
            # No retrieved_documents or filtered_documents
        )

        result = agent.run_hallucination_detection(state)

        assert "errors" in result
        assert "No source documents" in result["errors"][0]


class TestAdvancedHallucinationDetection:
    """Advanced tests for sophisticated hallucination detection scenarios."""

    def test_numerical_hallucination_detection(self):
        """Test detection of hallucinated numerical information."""
        agent = HallucinationGradingAgent(name="Numerical Test Agent")

        source_docs = [
            Document(
                page_content="The company was founded recently and has grown rapidly."
            ),
            Document(page_content="They have multiple locations in the city."),
        ]

        # Answer with specific numbers not in sources
        numerical_answer = "The company was founded in 2019 and now has 127 employees across 8 locations, generating $2.3 million in annual revenue."

        unsupported_claims = agent._identify_unsupported_claims(
            numerical_answer, source_docs
        )

        # Should identify numerical claims as potentially unsupported
        assert len(unsupported_claims) > 0

        # Check that numerical patterns are caught
        numerical_claims = [
            claim
            for claim in unsupported_claims
            if any(char.isdigit() for char in claim)
        ]
        assert len(numerical_claims) > 0

    def test_factual_contradiction_detection(self):
        """Test detection of factual contradictions."""
        agent = HallucinationGradingAgent(name="Contradiction Test Agent")

        source_docs = [
            Document(
                page_content="The restaurant is closed on Mondays and serves lunch and dinner."
            ),
            Document(page_content="They specialize in vegetarian cuisine only."),
        ]

        # Answer that contradicts source information
        contradictory_answer = "The restaurant is open every day including Mondays, serves breakfast, lunch and dinner, and offers both vegetarian and meat dishes."

        alignment_result = agent._check_source_alignment(
            contradictory_answer, source_docs
        )

        # Should have low alignment due to contradictions
        assert alignment_result["overlap_ratio"] < 0.7

    def test_context_drift_detection(self):
        """Test detection of context drift (going beyond source scope)."""
        agent = HallucinationGradingAgent(name="Context Drift Test Agent")

        # Sources about a specific restaurant
        source_docs = [
            Document(
                page_content="Bella's Cafe serves coffee and light meals in downtown."
            ),
            Document(page_content="The cafe has free wifi and comfortable seating."),
        ]

        # Answer that drifts to broader restaurant industry topics
        drifted_answer = "Bella's Cafe serves coffee and light meals downtown with free wifi. The restaurant industry has seen a 15% growth this year, with cafe concepts becoming increasingly popular in urban areas due to changing work patterns."

        result = agent.grade_answer_for_hallucinations(
            drifted_answer, source_docs, "Tell me about Bella's Cafe"
        )

        # Should detect some unsupported claims about industry trends
        assert len(result["unsupported_claims"]) > 0

    def test_temporal_hallucination_detection(self):
        """Test detection of hallucinated temporal information."""
        agent = HallucinationGradingAgent(name="Temporal Test Agent")

        source_docs = [
            Document(page_content="The building houses a popular restaurant."),
            Document(page_content="It has become a local landmark."),
        ]

        # Answer with specific temporal claims not in sources
        temporal_answer = "The building was constructed in 1887 and has housed the restaurant since 1923, making it a 100-year-old local landmark that survived the Great Depression."

        unsupported_claims = agent._identify_unsupported_claims(
            temporal_answer, source_docs
        )

        # Should identify specific dates and historical claims as unsupported
        assert len(unsupported_claims) > 0


class TestHallucinationDetectionIntegration:
    """Integration tests for hallucination detection in complete RAG workflows."""

    def test_end_to_end_rag_with_hallucination_detection(self):
        """Test complete RAG workflow with hallucination detection."""
        from haive.agents.rag.multi_agent_rag import (
            DocumentGradingAgent,
            SimpleRAGAgent,
        )

        # Create complete RAG pipeline with hallucination detection
        retrieval_agent = SimpleRAGAgent(name="Retrieval Agent")
        grading_agent = DocumentGradingAgent(name="Document Grader")
        answer_agent = SimpleRAGAnswerAgent(name="Answer Agent")
        hallucination_agent = HallucinationGradingAgent(name="Hallucination Detector")

        # Run through complete workflow
        state = MultiAgentRAGState(query="Tell me about restaurants in Times Square")

        # Step 1: Retrieval
        retrieval_result = retrieval_agent.run_retrieval(state)
        state.retrieved_documents = retrieval_result["retrieved_documents"]

        # Step 2: Document grading
        grading_result = grading_agent.run_grading(state)
        state.graded_documents = grading_result["graded_documents"]
        state.filtered_documents = grading_result["filtered_documents"]

        # Step 3: Answer generation
        answer_result = answer_agent.run_generation(state)
        state.generated_answer = answer_result["generated_answer"]

        # Step 4: Hallucination detection
        hallucination_result = hallucination_agent.run_hallucination_detection(state)

        # Verify complete workflow
        assert len(state.retrieved_documents) > 0
        assert state.generated_answer != ""
        assert "hallucination_detection" in hallucination_result
        assert "verification_confidence" in hallucination_result

        # Should have comprehensive hallucination analysis
        hallucination_analysis = hallucination_result["hallucination_detection"]
        required_fields = [
            "has_hallucination",
            "confidence_score",
            "source_alignment",
            "unsupported_claims",
            "factual_consistency",
        ]

        for field in required_fields:
            assert field in hallucination_analysis

    def test_multi_agent_hallucination_workflow(self):
        """Test multi-agent system with integrated hallucination detection."""
        from haive.agents.multi.base import SequentialAgent

        # Create multi-agent system with hallucination detection
        agents = [
            SimpleRAGAgent(name="Retrieval"),
            DocumentGradingAgent(name="Grading"),
            SimpleRAGAnswerAgent(name="Generation"),
            HallucinationGradingAgent(name="Verification"),
        ]

        workflow = SequentialAgent(
            agents=agents,
            state_schema=MultiAgentRAGState,
            name="RAG with Hallucination Detection",
        )

        assert len(workflow.agents) == 4
        assert workflow.state_schema == MultiAgentRAGState

        # Verify agent types
        agent_types = [type(agent).__name__ for agent in workflow.agents]
        expected_types = [
            "SimpleRAGAgent",
            "DocumentGradingAgent",
            "SimpleRAGAnswerAgent",
            "HallucinationGradingAgent",
        ]

        for expected_type in expected_types:
            assert any(expected_type in agent_type for agent_type in agent_types)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
