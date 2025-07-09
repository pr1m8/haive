"""
Specialized RAG Workflows - FLARE, Dynamic RAG, and Debate RAG

This module implements advanced RAG architectures including Forward-Looking Active REtrieval (FLARE),
Dynamic RAG with add/remove retrievers, and Debate-based RAG for multi-perspective reasoning.
"""

from typing import Any, Dict, List, Optional

from haive.core.schema.prebuilt.rag_state import RAGState

from haive.agents.multi.base import ExecutionMode, MultiAgent
from haive.agents.simple import SimpleAgent


class FLAREState(RAGState):
    """RAG state for Forward-Looking Active REtrieval"""

    current_generation: str = ""
    uncertainty_tokens: List[str] = []
    active_retrieval_points: List[int] = []
    generation_segments: List[str] = []
    confidence_scores: List[float] = []
    retrieval_triggers: List[str] = []


class DynamicRAGState(RAGState):
    """RAG state for Dynamic RAG with configurable retrievers"""

    active_retrievers: Dict[str, Dict[str, Any]] = {}
    retriever_performance: Dict[str, float] = {}
    document_sources: Dict[str, List[str]] = {}
    retriever_configurations: Dict[str, Any] = {}
    adaptive_threshold: float = 0.7


class DebateRAGState(RAGState):
    """RAG state for Debate-based RAG"""

    debate_positions: Dict[str, str] = {}
    arguments_by_position: Dict[str, List[str]] = {}
    evidence_by_position: Dict[str, List[str]] = {}
    debate_rounds: int = 0
    synthesis_attempts: List[str] = []
    consensus_reached: bool = False
    final_answer: str = ""


class FLAREAgent(MultiAgent):
    """
    Forward-Looking Active REtrieval (FLARE) - generates text while actively
    predicting when retrieval would be beneficial.
    """

    def __init__(self, **kwargs):
        # Generation monitor agent
        generation_monitor = SimpleAgent(
            name="generation_monitor",
            instructions="""
            Monitor text generation for uncertainty indicators and retrieval needs.
            Look for:
            - Low confidence tokens or phrases
            - Requests for specific information
            - Uncertainty markers (e.g., "possibly", "might be", "I think")
            - Points where factual information would strengthen the response
            
            Mark these points as active retrieval triggers.
            """,
            output_schema={
                "current_segment": "str",
                "uncertainty_detected": "bool",
                "uncertainty_tokens": "List[str]",
                "confidence_score": "float",
                "retrieval_needed": "bool",
                "retrieval_query": "Optional[str]",
            },
        )

        # Active retrieval agent
        active_retrieval = SimpleAgent(
            name="active_retrieval",
            instructions="""
            When triggered by uncertainty or information needs, perform targeted retrieval.
            Focus on:
            - The specific uncertain claim or question
            - Context from the generation so far
            - Predictive queries for upcoming content
            
            Retrieve documents that can resolve uncertainty or provide needed facts.
            """,
            output_schema={
                "retrieval_query": "str",
                "retrieved_documents": "List[str]",
                "relevance_scores": "List[float]",
                "retrieval_type": "str",  # "uncertainty", "predictive", "factual"
            },
        )

        # Informed generation agent
        informed_generator = SimpleAgent(
            name="informed_generator",
            instructions="""
            Continue or revise generation using retrieved information.
            - If retrieval occurred, incorporate the new information naturally
            - Maintain coherence with previous segments
            - Increase confidence in areas where retrieval provided support
            - Continue until the next uncertainty point or completion
            """,
            output_schema={
                "generated_segment": "str",
                "confidence_score": "float",
                "information_used": "List[str]",
                "generation_complete": "bool",
                "next_prediction": "Optional[str]",
            },
        )

        # Synthesis agent
        synthesis_agent = SimpleAgent(
            name="synthesis_agent",
            instructions="""
            Combine all generation segments into a final coherent response.
            - Ensure smooth transitions between segments
            - Verify factual consistency across retrieved information
            - Highlight where retrieval improved the response
            - Provide confidence assessment
            """,
            output_schema={
                "final_response": "str",
                "retrieval_impact": "str",
                "overall_confidence": "float",
                "key_facts_verified": "List[str]",
            },
        )

        agents = [
            generation_monitor,
            active_retrieval,
            informed_generator,
            synthesis_agent,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=FLAREState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for FLARE workflow"""
        # FLARE uses conditional execution based on uncertainty detection
        return None  # Use default graph structure


class DynamicRAGAgent(MultiAgent):
    """
    Dynamic RAG with add/remove retrievers - adapts retrieval strategy
    based on query characteristics and retriever performance.
    """

    def __init__(self, **kwargs):
        # Retriever manager agent
        retriever_manager = SimpleAgent(
            name="retriever_manager",
            instructions="""
            Manage the pool of active retrievers based on:
            - Query characteristics and domain
            - Past retriever performance
            - Document source requirements
            - Computational resources
            
            Decide which retrievers to activate, deactivate, or reconfigure.
            """,
            output_schema={
                "query_analysis": "Dict[str, Any]",
                "recommended_retrievers": "List[str]",
                "retrievers_to_add": "List[Dict[str, Any]]",
                "retrievers_to_remove": "List[str]",
                "configuration_updates": "Dict[str, Any]",
            },
        )

        # Multi-retriever coordinator
        retriever_coordinator = SimpleAgent(
            name="retriever_coordinator",
            instructions="""
            Coordinate retrieval across all active retrievers:
            - Execute parallel retrieval from different sources
            - Handle different retriever types (dense, sparse, hybrid)
            - Merge and deduplicate results
            - Track retriever performance metrics
            """,
            output_schema={
                "retrieval_results": "Dict[str, List[str]]",
                "performance_metrics": "Dict[str, float]",
                "source_distribution": "Dict[str, int]",
                "deduplication_stats": "Dict[str, int]",
            },
        )

        # Performance analyzer
        performance_analyzer = SimpleAgent(
            name="performance_analyzer",
            instructions="""
            Analyze retriever performance and adapt strategy:
            - Measure relevance and diversity of results
            - Track retriever latency and resource usage
            - Identify underperforming retrievers
            - Suggest optimizations and reconfigurations
            """,
            output_schema={
                "performance_report": "Dict[str, Dict[str, float]]",
                "optimization_suggestions": "List[str]",
                "retriever_rankings": "Dict[str, float]",
                "adaptation_needed": "bool",
            },
        )

        # Answer synthesis agent
        dynamic_synthesis = SimpleAgent(
            name="dynamic_synthesis",
            instructions="""
            Synthesize answer using dynamically retrieved documents:
            - Weight information based on retriever performance
            - Acknowledge source diversity
            - Handle conflicting information across retrievers
            - Provide confidence based on retrieval quality
            """,
            output_schema={
                "answer": "str",
                "sources_used": "Dict[str, List[str]]",
                "confidence_by_source": "Dict[str, float]",
                "synthesis_strategy": "str",
            },
        )

        agents = [
            retriever_manager,
            retriever_coordinator,
            performance_analyzer,
            dynamic_synthesis,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.SEQUENCE,
            state_schema=DynamicRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for Dynamic RAG workflow"""
        return None  # Use default graph structure


class DebateRAGAgent(MultiAgent):
    """
    Debate RAG - multiple agents with different perspectives debate
    to reach a comprehensive answer through dialectical reasoning.
    """

    def __init__(self, debate_positions: Optional[List[str]] = None, **kwargs):
        # Default positions if not provided
        if debate_positions is None:
            debate_positions = ["Affirmative", "Negative", "Neutral"]

        # Create position agents
        position_agents = []
        for position in debate_positions:
            agent = SimpleAgent(
                name=f"{position.lower()}_position",
                instructions=f"""
                You represent the {position} perspective in this debate.
                - Retrieve and present evidence supporting your position
                - Construct logical arguments based on retrieved documents
                - Acknowledge but counter opposing viewpoints
                - Maintain intellectual honesty while advocating your position
                
                Your goal is to contribute to finding the truth through debate.
                """,
                output_schema={
                    "position": "str",
                    "argument": "str",
                    "evidence": "List[str]",
                    "counterpoints": "Dict[str, str]",
                    "confidence": "float",
                },
            )
            position_agents.append(agent)

        # Moderator agent
        moderator = SimpleAgent(
            name="debate_moderator",
            instructions="""
            Moderate the debate between different positions:
            - Ensure all perspectives are heard
            - Identify key points of agreement and disagreement
            - Direct retrieval toward resolving conflicts
            - Maintain focus on the original question
            - Facilitate productive exchange
            """,
            output_schema={
                "debate_summary": "str",
                "key_agreements": "List[str]",
                "key_conflicts": "List[str]",
                "information_gaps": "List[str]",
                "next_focus": "str",
            },
        )

        # Evidence arbiter
        evidence_arbiter = SimpleAgent(
            name="evidence_arbiter",
            instructions="""
            Evaluate evidence presented by all positions:
            - Assess source credibility and relevance
            - Identify contradictions in evidence
            - Weight evidence based on quality
            - Highlight strongest supporting facts
            - Note where evidence is lacking
            """,
            output_schema={
                "evidence_evaluation": "Dict[str, Dict[str, Any]]",
                "strongest_evidence": "List[str]",
                "conflicting_evidence": "List[Dict[str, str]]",
                "evidence_gaps": "List[str]",
                "credibility_scores": "Dict[str, float]",
            },
        )

        # Synthesis judge
        synthesis_judge = SimpleAgent(
            name="synthesis_judge",
            instructions="""
            Synthesize the debate into a final comprehensive answer:
            - Consider all positions and evidence fairly
            - Integrate the strongest arguments from each side
            - Acknowledge uncertainty where consensus wasn't reached
            - Provide a nuanced, balanced conclusion
            - Explain the reasoning path taken
            """,
            output_schema={
                "final_answer": "str",
                "reasoning_path": "str",
                "position_contributions": "Dict[str, str]",
                "confidence_level": "float",
                "remaining_uncertainty": "List[str]",
            },
        )

        agents = position_agents + [moderator, evidence_arbiter, synthesis_judge]

        # Store debate configuration as instance variable
        self._debate_positions = debate_positions

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=DebateRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for Debate RAG workflow"""
        # Debate RAG uses complex conditional routing between positions
        return None  # Use default graph structure


class AdaptiveThresholdRAGAgent(MultiAgent):
    """
    Adaptive Threshold RAG - dynamically adjusts retrieval thresholds
    based on query difficulty and answer confidence.
    """

    def __init__(self, **kwargs):
        # Query analyzer
        query_analyzer = SimpleAgent(
            name="query_analyzer",
            instructions="""
            Analyze query characteristics to set initial thresholds:
            - Assess query complexity and specificity
            - Identify domain and required expertise
            - Estimate information density needed
            - Predict retrieval difficulty
            
            Set initial thresholds for retrieval and relevance.
            """,
            output_schema={
                "query_complexity": "float",
                "domain": "str",
                "specificity": "float",
                "initial_threshold": "float",
                "retrieval_strategy": "str",
            },
        )

        # Adaptive retriever
        adaptive_retriever = SimpleAgent(
            name="adaptive_retriever",
            instructions="""
            Perform retrieval with dynamic threshold adjustment:
            - Start with initial threshold
            - If too few results, lower threshold
            - If too many low-quality results, raise threshold
            - Balance precision and recall based on query needs
            """,
            output_schema={
                "documents": "List[str]",
                "relevance_scores": "List[float]",
                "threshold_used": "float",
                "threshold_adjustments": "List[float]",
                "retrieval_rounds": "int",
            },
        )

        # Confidence assessor
        confidence_assessor = SimpleAgent(
            name="confidence_assessor",
            instructions="""
            Assess answer confidence and need for more retrieval:
            - Evaluate if retrieved documents sufficiently answer the query
            - Identify information gaps
            - Determine if threshold adjustment could help
            - Recommend further retrieval if needed
            """,
            output_schema={
                "answer_confidence": "float",
                "information_completeness": "float",
                "gaps_identified": "List[str]",
                "recommend_adjustment": "bool",
                "suggested_threshold": "Optional[float]",
            },
        )

        # Final answer generator
        threshold_aware_generator = SimpleAgent(
            name="threshold_aware_generator",
            instructions="""
            Generate answer with awareness of retrieval thresholds:
            - Acknowledge if high thresholds limited information
            - Note if low thresholds included marginal content
            - Provide confidence calibrated to retrieval quality
            - Suggest areas for deeper investigation if needed
            """,
            output_schema={
                "answer": "str",
                "retrieval_quality": "str",
                "confidence": "float",
                "limitations": "List[str]",
                "further_investigation": "Optional[List[str]]",
            },
        )

        agents = [
            query_analyzer,
            adaptive_retriever,
            confidence_assessor,
            threshold_aware_generator,
        ]

        super().__init__(
            agents=agents,
            execution_mode=ExecutionMode.CONDITIONAL,
            state_schema=DynamicRAGState,
            **kwargs,
        )

    def build_custom_graph(self):
        """Build the custom graph for Adaptive Threshold RAG workflow"""
        return None  # Use default graph structure
