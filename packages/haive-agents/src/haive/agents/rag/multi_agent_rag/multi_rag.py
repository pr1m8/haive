"""Multi-Agent RAG System Implementation

This module provides complete multi-agent RAG workflows using the multi-agent framework
with conditional routing, sequential processing, and parallel execution patterns.
"""

from collections.abc import Callable
from typing import Any

from haive.core.fixtures.documents import conversation_documents
from haive.core.schema.compatibility import check_compatibility
from langchain_core.documents import Document

from haive.agents.multi.base import ConditionalAgent, ParallelAgent, SequentialAgent

from .agents import (
    SIMPLE_RAG_AGENT,
    SIMPLE_RAG_ANSWER_AGENT,
    DocumentGradingAgent,
    IterativeDocumentGradingAgent,
    SimpleRAGAgent,
    SimpleRAGAnswerAgent,
)
from .state import MultiAgentRAGState

# ============================================================================
# CONDITIONAL ROUTING FUNCTIONS
# ============================================================================


def should_grade_documents(state: MultiAgentRAGState) -> str:
    """Conditional routing function to determine if documents need grading.

    Returns:
        - "grade": If documents need to be graded
        - "generate": If documents are already good enough
        - "refine": If query needs refinement
    """
    # Check if we have retrieved documents
    if not state.retrieved_documents:
        return "refine"

    # Check if documents are already graded
    if state.graded_documents:
        relevant_count = sum(1 for doc in state.graded_documents if doc.is_relevant)
        if relevant_count >= 2:  # Minimum documents for good answer
            return "generate"

    # Check retrieval confidence
    if state.retrieval_confidence < 0.3:
        return "refine"

    return "grade"


def should_refine_query(state: MultiAgentRAGState) -> str:
    """Conditional routing function to determine if query needs refinement.

    Returns:
        - "retrieve": Try retrieval again with refined query
        - "generate": Generate answer with available documents
        - "END": Stop processing (failure case)
    """
    # Check if we have any relevant documents after grading
    if state.filtered_documents:
        return "generate"

    # Check if we've already tried refinement
    if len(state.queries) > 2:  # Original + 1 refinement attempt
        if state.retrieved_documents:
            return "generate"  # Generate with what we have
        return "END"  # Give up

    return "retrieve"


def document_quality_check(state: MultiAgentRAGState) -> str:
    """Check document quality and route accordingly.

    Returns:
        - "sufficient": Documents are good enough for generation
        - "insufficient": Need more/better documents
        - "regrade": Need different grading approach
    """
    if not state.filtered_documents:
        return "insufficient"

    if len(state.filtered_documents) >= 3:
        return "sufficient"

    if state.retrieval_confidence > 0.7:
        return "sufficient"

    return "insufficient"


# ============================================================================
# BASE MULTI-AGENT RAG SYSTEM
# ============================================================================


class BaseRAGMultiAgent(SequentialAgent):
    """Base multi-agent RAG system with retrieve -> grade -> generate workflow.

    This is the simple sequential RAG agent as mentioned in the user prompt.
    """

    def __init__(
        self,
        retrieval_agent: SimpleRAGAgent | None = None,
        grading_agent: DocumentGradingAgent | None = None,
        answer_agent: SimpleRAGAnswerAgent | None = None,
        **kwargs,
    ):
        # Use default agents if none provided
        agents = [
            retrieval_agent or SIMPLE_RAG_AGENT,
            grading_agent or DocumentGradingAgent(),
            answer_agent or SIMPLE_RAG_ANSWER_AGENT,
        ]

        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Base RAG Multi-Agent"

        super().__init__(agents=agents, **kwargs)


class ConditionalRAGMultiAgent(ConditionalAgent):
    """Conditional multi-agent RAG system with smart routing based on document quality.

    This system uses conditional routing to decide whether to grade documents,
    refine queries, or generate answers based on the current state.
    """

    def __init__(
        self,
        retrieval_agent: SimpleRAGAgent | None = None,
        grading_agent: DocumentGradingAgent | None = None,
        answer_agent: SimpleRAGAnswerAgent | None = None,
        query_refiner: Any | None = None,  # Could be another agent
        **kwargs,
    ):
        # Create agents
        self.retrieval_agent = retrieval_agent or SIMPLE_RAG_AGENT
        self.grading_agent = grading_agent or DocumentGradingAgent()
        self.answer_agent = answer_agent or SIMPLE_RAG_ANSWER_AGENT
        self.query_refiner = query_refiner  # Optional query refinement agent

        agents = [self.retrieval_agent, self.grading_agent, self.answer_agent]

        if self.query_refiner:
            agents.append(self.query_refiner)

        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Conditional RAG Multi-Agent"

        super().__init__(agents=agents, **kwargs)

        # Set up conditional routing
        self._setup_conditional_routing()

    def _setup_conditional_routing(self):
        """Set up conditional edges for smart routing."""
        # After retrieval, decide whether to grade or generate
        self.add_conditional_edge(
            source_agent=self.retrieval_agent,
            condition=should_grade_documents,
            destinations={
                "grade": self.grading_agent,
                "generate": self.answer_agent,
                "refine": (
                    self.query_refiner if self.query_refiner else self.retrieval_agent
                ),
            },
            default=self.grading_agent,
        )

        # After grading, check if we need to refine query or can generate
        self.add_conditional_edge(
            source_agent=self.grading_agent,
            condition=should_refine_query,
            destinations={
                "retrieve": self.retrieval_agent,
                "generate": self.answer_agent,
                "END": "END",
            },
            default=self.answer_agent,
        )


class IterativeRAGMultiAgent(SequentialAgent):
    """Multi-agent RAG system with iterative document processing.

    This system demonstrates iterating over retrieved documents and processing
    each one individually, as mentioned in the user prompt.
    """

    def __init__(
        self,
        retrieval_agent: SimpleRAGAgent | None = None,
        iterative_grader: IterativeDocumentGradingAgent | None = None,
        answer_agent: SimpleRAGAnswerAgent | None = None,
        custom_grader_callable: Callable | None = None,
        **kwargs,
    ):
        # Create iterative grading agent with custom callable if provided
        if not iterative_grader:
            iterative_grader = IterativeDocumentGradingAgent(
                custom_grader=custom_grader_callable
            )

        agents = [
            retrieval_agent or SIMPLE_RAG_AGENT,
            iterative_grader,
            answer_agent or SIMPLE_RAG_ANSWER_AGENT,
        ]

        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Iterative RAG Multi-Agent"

        super().__init__(agents=agents, **kwargs)


class ParallelRAGMultiAgent(ParallelAgent):
    """Parallel multi-agent RAG system for consensus-based processing.

    This system runs multiple RAG agents in parallel and aggregates their results.
    """

    def __init__(self, rag_agents: list[BaseRAGMultiAgent] | None = None, **kwargs):
        # Create default parallel RAG agents if none provided
        if not rag_agents:
            rag_agents = [
                BaseRAGMultiAgent(name="RAG Agent 1"),
                BaseRAGMultiAgent(name="RAG Agent 2"),
                BaseRAGMultiAgent(name="RAG Agent 3"),
            ]

        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Parallel RAG Multi-Agent"

        super().__init__(agents=rag_agents, **kwargs)


# ============================================================================
# ADVANCED MULTI-AGENT RAG WORKFLOWS
# ============================================================================


class AdaptiveRAGMultiAgent(ConditionalAgent):
    """Advanced RAG system that adapts its strategy based on query complexity and results.

    This system demonstrates sophisticated conditional routing with multiple
    decision points and fallback strategies.
    """

    def __init__(
        self,
        simple_rag: BaseRAGMultiAgent | None = None,
        complex_rag: IterativeRAGMultiAgent | None = None,
        consensus_rag: ParallelRAGMultiAgent | None = None,
        **kwargs,
    ):
        self.simple_rag = simple_rag or BaseRAGMultiAgent(name="Simple RAG")
        self.complex_rag = complex_rag or IterativeRAGMultiAgent(name="Complex RAG")
        self.consensus_rag = consensus_rag or ParallelRAGMultiAgent(
            name="Consensus RAG"
        )

        agents = [self.simple_rag, self.complex_rag, self.consensus_rag]

        # Set default state schema
        if "state_schema" not in kwargs:
            kwargs["state_schema"] = MultiAgentRAGState

        # Set default name
        if "name" not in kwargs:
            kwargs["name"] = "Adaptive RAG Multi-Agent"

        super().__init__(agents=agents, **kwargs)

        # Set up adaptive routing
        self._setup_adaptive_routing()

    def _setup_adaptive_routing(self):
        """Set up adaptive routing based on query complexity and results."""

        def route_initial_strategy(state: MultiAgentRAGState) -> str:
            """Route to appropriate initial strategy based on query complexity."""
            query_len = len(state.query.split())

            if query_len <= 5:  # Simple query
                return "simple"
            if query_len <= 15:  # Medium complexity
                return "complex"
            # Complex query
            return "consensus"

        def route_fallback_strategy(state: MultiAgentRAGState) -> str:
            """Route to fallback strategy if initial approach fails."""
            if state.overall_quality_score < 0.5:
                if state.active_agent == "Simple RAG":
                    return "complex"
                if state.active_agent == "Complex RAG":
                    return "consensus"
            return "END"

        # Initial routing
        self.add_conditional_edge(
            source_agent="START",
            condition=route_initial_strategy,
            destinations={
                "simple": self.simple_rag,
                "complex": self.complex_rag,
                "consensus": self.consensus_rag,
            },
            default=self.simple_rag,
        )

        # Fallback routing for each strategy
        for agent in [self.simple_rag, self.complex_rag]:
            self.add_conditional_edge(
                source_agent=agent,
                condition=route_fallback_strategy,
                destinations={
                    "complex": self.complex_rag,
                    "consensus": self.consensus_rag,
                    "END": "END",
                },
                default="END",
            )


# ============================================================================
# COMPATIBILITY TESTING UTILITIES
# ============================================================================


def test_agent_compatibility(agent1, agent2) -> dict[str, Any]:
    """Test compatibility between two agents using the compatibility module.

    This demonstrates using the compatibility module to test if agents
    can work together as mentioned in the user prompt.
    """
    try:
        # Check if agents have compatible schemas
        result = check_compatibility(agent1.output_schema, agent2.input_schema)

        return {
            "compatible": result.is_compatible,
            "compatibility_score": getattr(result, "compatibility_score", 0.0),
            "missing_fields": getattr(result, "missing_required_fields", []),
            "issues": getattr(result, "issues", []),
            "suggestions": getattr(result, "suggested_mappings", {}),
        }

    except Exception as e:
        return {
            "compatible": False,
            "error": str(e),
            "suggestions": ["Check agent schema definitions"],
        }


def validate_multi_agent_compatibility(agents: list[Any]) -> dict[str, Any]:
    """Validate compatibility across multiple agents in a workflow.

    Returns a comprehensive compatibility report for the agent chain.
    """
    compatibility_results = {}

    for i in range(len(agents) - 1):
        agent1, agent2 = agents[i], agents[i + 1]
        agent1_name = getattr(agent1, "name", f"Agent_{i}")
        agent2_name = getattr(agent2, "name", f"Agent_{i+1}")

        result = test_agent_compatibility(agent1, agent2)
        compatibility_results[f"{agent1_name} -> {agent2_name}"] = result

    # Overall compatibility
    all_compatible = all(
        result.get("compatible", False) for result in compatibility_results.values()
    )

    return {
        "overall_compatible": all_compatible,
        "individual_results": compatibility_results,
        "total_connections": len(compatibility_results),
        "compatible_connections": sum(
            1
            for result in compatibility_results.values()
            if result.get("compatible", False)
        ),
    }


# ============================================================================
# PREDEFINED MULTI-AGENT INSTANCES (as mentioned in user prompt)
# ============================================================================

# The simple sequential RAG agent as mentioned in the prompt
base_rag_agent = SequentialAgent(
    agents=[SIMPLE_RAG_AGENT, SIMPLE_RAG_ANSWER_AGENT],
    state_schema=MultiAgentRAGState,
    name="Base RAG Sequential Agent",
)

# List of agents for testing compatibility
agent_list = [SIMPLE_RAG_AGENT, SIMPLE_RAG_ANSWER_AGENT]


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_sequential_rag_system(
    documents: list[Document] | None = None,
    use_grading: bool = True,
    use_citations: bool = False,
) -> SequentialAgent:
    """Create a sequential RAG system with configurable components."""
    # Create agents
    retrieval_agent = SimpleRAGAgent.from_documents(documents or conversation_documents)
    answer_agent = SimpleRAGAnswerAgent(use_citations=use_citations)

    agents = [retrieval_agent]

    if use_grading:
        grading_agent = DocumentGradingAgent()
        agents.append(grading_agent)

    agents.append(answer_agent)

    return SequentialAgent(
        agents=agents, state_schema=MultiAgentRAGState, name="Sequential RAG System"
    )


def create_conditional_rag_system(
    documents: list[Document] | None = None, custom_grader: Callable | None = None
) -> ConditionalRAGMultiAgent:
    """Create a conditional RAG system with smart routing."""
    retrieval_agent = SimpleRAGAgent.from_documents(documents or conversation_documents)

    return ConditionalRAGMultiAgent(
        retrieval_agent=retrieval_agent,
        grading_agent=IterativeDocumentGradingAgent(custom_grader=custom_grader),
    )


def create_iterative_rag_system(
    documents: list[Document] | None = None, custom_grader: Callable | None = None
) -> IterativeRAGMultiAgent:
    """Create an iterative RAG system with document-by-document processing."""
    retrieval_agent = SimpleRAGAgent.from_documents(documents or conversation_documents)

    return IterativeRAGMultiAgent(
        retrieval_agent=retrieval_agent, custom_grader_callable=custom_grader
    )
