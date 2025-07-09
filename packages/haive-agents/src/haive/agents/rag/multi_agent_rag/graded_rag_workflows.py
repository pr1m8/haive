"""
Graded RAG Workflows - RAG with comprehensive grading and evaluation

This module implements RAG workflows with integrated document grading,
answer quality assessment, and hallucination detection.
"""

from typing import Dict, List, Optional

from haive.core.schema.prebuilt.rag_state import RAGState

from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.rag.multi_agent_rag.grading_components import (
    AnswerGrade,
    DocumentGrade,
    HallucinationGrade,
    create_answer_grader,
    create_document_grader,
    create_hallucination_grader,
    create_priority_ranker,
    create_query_analyzer,
)
from haive.agents.simple import SimpleAgent


class GradedRAGState(RAGState):
    """RAG state with grading information"""

    # Query analysis
    query_type: str = ""
    query_complexity: str = ""
    key_entities: List[str] = []

    # Document grading
    document_grades: List[DocumentGrade] = []
    priority_ranking: Dict[str, float] = {}
    filtered_documents: List[str] = []

    # Answer grading
    answer_grade: Optional[AnswerGrade] = None
    hallucination_grade: Optional[HallucinationGrade] = None

    # Pipeline metrics
    overall_score: float = 0.0
    improvement_suggestions: List[str] = []


class FullyGradedRAGAgent(MultiAgent):
    """
    Fully Graded RAG - comprehensive grading at every step of the RAG pipeline.
    Includes query analysis, document grading, prioritization, answer quality,
    and hallucination detection.
    """

    def __init__(self, relevance_threshold: float = 0.5, **kwargs):
        self._relevance_threshold = relevance_threshold

        # Query analyzer
        query_analyzer = create_query_analyzer("query_analyzer")

        # Retrieval agent
        retriever = SimpleAgent(
            name="retriever",
            instructions="""
            Retrieve documents based on the query and analysis.
            Use key entities and query type to optimize retrieval strategy.
            Cast a wide net initially - grading will filter results.
            """,
            output_schema={
                "documents": "List[str]",
                "retrieval_strategy": "str",
                "num_retrieved": "int",
            },
        )

        # Document grader
        document_grader = create_document_grader("document_relevance_grader")

        # Priority ranker
        priority_ranker = create_priority_ranker("document_priority_ranker")

        # Filtering agent
        filter_agent = SimpleAgent(
            name="document_filter",
            instructions=f"""
            Filter documents based on relevance grades and priority ranking.
            - Include documents with relevance >= {self._relevance_threshold}
            - Respect priority ranking for ordering
            - Limit to top K documents if too many pass threshold
            - Provide filtering statistics
            """,
            output_schema={
                "filtered_documents": "List[str]",
                "num_filtered": "int",
                "filter_reason": "Dict[str, str]",
                "avg_relevance": "float",
            },
        )

        # Answer generator
        answer_generator = SimpleAgent(
            name="graded_answer_generator",
            instructions="""
            Generate a comprehensive answer using only the filtered, high-quality documents.
            - Focus on documents with highest priority scores
            - Cite sources explicitly
            - Acknowledge any limitations or gaps
            - Maintain factual accuracy - only use information from documents
            """,
            output_schema={
                "answer": "str",
                "sources_used": "List[str]",
                "confidence": "float",
                "limitations": "List[str]",
            },
        )

        # Answer quality grader
        answer_grader = create_answer_grader("answer_quality_grader")

        # Hallucination detector
        hallucination_grader = create_hallucination_grader("hallucination_detector")

        # Final synthesis
        synthesis_agent = SimpleAgent(
            name="grade_synthesis",
            instructions="""
            Synthesize all grading information and provide final assessment.
            - Calculate overall pipeline score
            - Identify key improvement areas
            - Provide actionable suggestions
            - Determine if answer meets quality threshold
            """,
            output_schema={
                "overall_score": "float",
                "meets_quality_threshold": "bool",
                "key_strengths": "List[str]",
                "improvement_areas": "List[str]",
                "actionable_suggestions": "List[str]",
            },
        )

        agents = [
            query_analyzer,
            retriever,
            document_grader,
            priority_ranker,
            filter_agent,
            answer_generator,
            answer_grader,
            hallucination_grader,
            synthesis_agent,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for graded RAG workflow"""
        return None  # Use default sequential execution


class AdaptiveGradedRAGAgent(MultiAgent):
    """
    Adaptive Graded RAG - adjusts grading thresholds based on query complexity
    and document availability.
    """

    def __init__(self, **kwargs):
        # Query complexity analyzer
        complexity_analyzer = SimpleAgent(
            name="complexity_analyzer",
            instructions="""
            Analyze query complexity and set appropriate grading thresholds.
            - Simple queries: Higher relevance threshold (stricter)
            - Complex queries: Lower threshold (more inclusive)
            - Technical queries: Focus on accuracy over breadth
            - Exploratory queries: Focus on coverage over precision
            """,
            output_schema={
                "complexity_level": "str",
                "suggested_relevance_threshold": "float",
                "suggested_doc_limit": "int",
                "grading_strategy": "str",
            },
        )

        # Adaptive retriever
        adaptive_retriever = SimpleAgent(
            name="adaptive_retriever",
            instructions="""
            Retrieve documents with adaptive strategy based on complexity analysis.
            - Adjust retrieval parameters dynamically
            - Use multiple retrieval methods if needed
            - Balance precision and recall based on query type
            """,
            output_schema={
                "documents": "List[str]",
                "retrieval_methods_used": "List[str]",
                "adaptive_parameters": "Dict[str, Any]",
            },
        )

        # Dynamic grader
        dynamic_grader = SimpleAgent(
            name="dynamic_grader",
            instructions="""
            Grade documents with adaptive thresholds based on:
            - Query complexity
            - Number of retrieved documents
            - Initial relevance distribution
            
            Adjust thresholds to ensure adequate document coverage
            while maintaining quality.
            """,
            output_schema={
                "graded_documents": "List[Dict[str, Any]]",
                "applied_threshold": "float",
                "threshold_adjustments": "List[str]",
                "grade_distribution": "Dict[str, int]",
            },
        )

        # Iterative refiner
        iterative_refiner = SimpleAgent(
            name="iterative_refiner",
            instructions="""
            Refine answer iteratively based on grading feedback.
            - If answer quality is low, identify specific issues
            - If hallucinations detected, revise using only supported claims
            - If incomplete, identify missing information
            - Iterate until quality threshold met or max iterations
            """,
            output_schema={
                "refined_answer": "str",
                "refinement_iterations": "int",
                "refinement_actions": "List[str]",
                "final_quality_score": "float",
            },
        )

        agents = [
            complexity_analyzer,
            adaptive_retriever,
            dynamic_grader,
            iterative_refiner,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for adaptive graded RAG"""
        return None


class MultiCriteriaGradedRAGAgent(MultiAgent):
    """
    Multi-Criteria Graded RAG - uses multiple grading criteria and perspectives
    to evaluate documents and answers.
    """

    def __init__(self, grading_criteria: Optional[List[str]] = None, **kwargs):
        if grading_criteria is None:
            grading_criteria = [
                "relevance",
                "accuracy",
                "completeness",
                "clarity",
                "authority",
            ]

        # Multi-criteria document grader
        multi_criteria_grader = SimpleAgent(
            name="multi_criteria_grader",
            instructions=f"""
            Grade documents across multiple criteria: {', '.join(grading_criteria)}
            
            For each criterion:
            - Provide a score (0.0-1.0)
            - Give specific reasoning
            - Note strengths and weaknesses
            
            Calculate composite score with weighted average.
            """,
            output_schema={
                "document_id": "str",
                "criteria_scores": "Dict[str, float]",
                "criteria_reasoning": "Dict[str, str]",
                "composite_score": "float",
                "primary_strength": "str",
                "primary_weakness": "str",
            },
        )

        # Perspective aggregator
        perspective_aggregator = SimpleAgent(
            name="perspective_aggregator",
            instructions="""
            Aggregate grading from multiple criteria to make filtering decisions.
            - Consider which criteria are most important for the query
            - Weight criteria dynamically based on query type
            - Identify documents that excel in critical criteria
            - Flag documents with major weaknesses in any criterion
            """,
            output_schema={
                "aggregated_scores": "Dict[str, float]",
                "criteria_weights": "Dict[str, float]",
                "recommended_documents": "List[str]",
                "excluded_documents": "List[str]",
                "aggregation_reasoning": "str",
            },
        )

        # Balanced answer generator
        balanced_generator = SimpleAgent(
            name="balanced_answer_generator",
            instructions="""
            Generate answers that balance all grading criteria:
            - Ensure high relevance to query
            - Maintain factual accuracy
            - Provide complete coverage
            - Express clearly and concisely
            - Cite authoritative sources
            
            Note which criteria might be compromised and why.
            """,
            output_schema={
                "answer": "str",
                "criteria_balance": "Dict[str, str]",
                "compromises_made": "List[str]",
                "optimization_focus": "str",
            },
        )

        agents = [multi_criteria_grader, perspective_aggregator, balanced_generator]

        self._grading_criteria = grading_criteria

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for multi-criteria graded RAG"""
        return None


class ReflexiveGradedRAGAgent(MultiAgent):
    """
    Reflexive Graded RAG - uses grading feedback to improve its own performance
    through self-reflection and strategy adjustment.
    """

    def __init__(self, **kwargs):
        # Self-assessment agent
        self_assessor = SimpleAgent(
            name="self_assessor",
            instructions="""
            Assess current RAG pipeline performance:
            - Review previous grading results
            - Identify systematic issues or patterns
            - Determine if current strategies are effective
            - Suggest strategic adjustments
            """,
            output_schema={
                "performance_assessment": "str",
                "identified_patterns": "List[str]",
                "strategy_effectiveness": "Dict[str, float]",
                "suggested_adjustments": "List[str]",
            },
        )

        # Strategy adapter
        strategy_adapter = SimpleAgent(
            name="strategy_adapter",
            instructions="""
            Adapt RAG strategies based on self-assessment:
            - Adjust retrieval parameters
            - Modify grading thresholds
            - Change answer generation approach
            - Update document filtering criteria
            
            Implement changes that address identified issues.
            """,
            output_schema={
                "adapted_strategies": "Dict[str, Any]",
                "parameter_changes": "Dict[str, Any]",
                "expected_improvements": "List[str]",
                "adaptation_reasoning": "str",
            },
        )

        # Reflexive executor
        reflexive_executor = SimpleAgent(
            name="reflexive_executor",
            instructions="""
            Execute RAG pipeline with adapted strategies and monitor results.
            - Apply new parameters and approaches
            - Track improvements in real-time
            - Collect feedback for next iteration
            - Determine if adaptations were successful
            """,
            output_schema={
                "execution_results": "Dict[str, Any]",
                "improvement_metrics": "Dict[str, float]",
                "adaptation_success": "bool",
                "lessons_learned": "List[str]",
            },
        )

        agents = [self_assessor, strategy_adapter, reflexive_executor]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=GradedRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for reflexive graded RAG"""
        return None
