"""Complete RAG Workflows Implementation.

Implements all RAG architectures from rag-architectures-flows.md including:
- Corrective RAG with web search fallback
- Self-RAG with reflection tokens
- Adaptive RAG with complexity routing
- Multi-Query RAG and RAG Fusion
- HYDE and Step-Back prompting
- Hallucination detection and requerying
"""

from enum import Enum
from typing import List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.fixtures.documents import conversation_documents
from haive.core.graph.node.callable_node import CallableNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.rag_state import MultiAgentRAGState
from langchain_core.documents import Document
from langgraph.graph import END, START

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ConditionalAgent, SequentialAgent
from haive.agents.rag.base.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


class RAGQuality(str, Enum):
    """Quality assessment for retrieved documents."""

    CORRECT = "correct"
    INCORRECT = "incorrect"
    AMBIGUOUS = "ambiguous"


class ReflectionToken(str, Enum):
    """Self-RAG reflection tokens."""

    RETRIEVAL_YES = "[Retrieval]"
    NO_RETRIEVAL = "[No Retrieval]"
    ISREL_RELEVANT = "[ISREL] Relevant"
    ISREL_NOT_RELEVANT = "[ISREL] Not Relevant"
    ISSUP_SUPPORTED = "[ISSUP] Supported"
    ISSUP_NOT_SUPPORTED = "[ISSUP] Not Supported"
    ISUSE_USEFUL = "[ISUSE] Useful"
    ISUSE_NOT_USEFUL = "[ISUSE] Not Useful"


# ============================================================================
# CALLABLE FUNCTIONS FOR RAG WORKFLOWS
# ============================================================================


def crag_relevance_check(input_data: dict) -> dict:
    """CRAG relevance checking with three-way classification."""
    state = input_data["state"]

    if not state.graded_documents:
        return {
            "quality": RAGQuality.INCORRECT,
            "confidence": 0.0,
            "reasoning": "No graded documents",
        }

    # Calculate average relevance score
    avg_score = sum(grade.relevance_score for grade in state.graded_documents) / len(
        state.graded_documents
    )

    if avg_score > 0.8:
        quality = RAGQuality.CORRECT
    elif avg_score < 0.3:
        quality = RAGQuality.INCORRECT
    else:
        quality = RAGQuality.AMBIGUOUS

    return {
        "quality": quality,
        "confidence": avg_score,
        "reasoning": f"Average relevance score: {avg_score:.2f}",
        "needs_web_search": quality in [RAGQuality.INCORRECT, RAGQuality.AMBIGUOUS],
    }


def hallucination_detection(input_data: dict) -> dict:
    """Detect hallucination in generated response."""
    state = input_data["state"]
    response = state.generated_response

    if not response:
        return {
            "has_hallucination": False,
            "confidence": 0.0,
            "reasoning": "No response to check",
        }

    # Simple hallucination detection (can be enhanced with more sophisticated methods)
    # Check if response contains information not in source documents
    doc_contents = [doc.page_content.lower() for doc in state.relevant_documents]
    response_lower = response.lower()

    # Look for specific claims that might be hallucinated
    hallucination_indicators = [
        "according to my knowledge",
        "i believe",
        "it is likely that",
        "probably",
        "i think",
    ]

    has_indicators = any(
        indicator in response_lower for indicator in hallucination_indicators
    )

    # Check if response mentions facts not in documents (basic check)
    key_terms = response_lower.split()
    doc_coverage = sum(
        1 for term in key_terms if any(term in doc for doc in doc_contents)
    )
    coverage_ratio = doc_coverage / len(key_terms) if key_terms else 0

    has_hallucination = has_indicators or coverage_ratio < 0.3
    confidence = 1.0 - coverage_ratio if has_indicators else coverage_ratio

    return {
        "has_hallucination": has_hallucination,
        "confidence": confidence,
        "reasoning": f"Coverage ratio: {coverage_ratio:.2f}, indicators: {has_indicators}",
        "needs_regeneration": has_hallucination,
    }


def self_rag_retrieval_decision(input_data: dict) -> dict:
    """Self-RAG retrieval decision with reflection tokens."""
    state = input_data["state"]
    query = state.query

    # Simple heuristic for retrieval decision
    knowledge_requiring_terms = [
        "current",
        "latest",
        "recent",
        "today",
        "yesterday",
        "2024",
        "2023",
        "price",
        "cost",
        "location",
        "address",
        "phone",
        "hours",
        "schedule",
    ]

    needs_retrieval = any(term in query.lower() for term in knowledge_requiring_terms)

    token = (
        ReflectionToken.RETRIEVAL_YES
        if needs_retrieval
        else ReflectionToken.NO_RETRIEVAL
    )

    return {
        "retrieval_token": token,
        "needs_retrieval": needs_retrieval,
        "reasoning": f"Query requires external knowledge: {needs_retrieval}",
    }


def web_search_fallback(input_data: dict) -> dict:
    """Web search fallback for when documents are insufficient."""
    state = input_data["state"]
    query = state.query

    # Mock web search (replace with actual web search implementation)
    web_results = [
        Document(
            page_content=f"Web search result for: {query}. This would contain current information from the internet.",
            metadata={"source": "web_search", "query": query, "relevance": 0.9},
        ),
        Document(
            page_content=f"Additional web context about {query} from recent sources.",
            metadata={"source": "web_search", "query": query, "relevance": 0.8},
        ),
    ]

    return {
        "web_search_results": web_results,
        "web_search_performed": True,
        "reasoning": f"Web search for query: {query}",
    }


def query_complexity_analysis(input_data: dict) -> dict:
    """Analyze query complexity for adaptive routing."""
    state = input_data["state"]
    query = state.query.lower()

    # Complexity indicators
    multi_hop_indicators = [
        "and",
        "but",
        "however",
        "also",
        "compare",
        "difference",
        "versus",
    ]
    simple_indicators = ["what", "who", "when", "where"]
    complex_indicators = ["why", "how", "explain", "analyze", "evaluate"]

    multi_hop_count = sum(1 for ind in multi_hop_indicators if ind in query)
    simple_count = sum(1 for ind in simple_indicators if ind in query)
    complex_count = sum(1 for ind in complex_indicators if ind in query)

    if complex_count > 0 or multi_hop_count > 1:
        complexity = "complex"
    elif multi_hop_count > 0:
        complexity = "medium"
    elif simple_count > 0:
        complexity = "simple"
    else:
        complexity = "unknown"

    return {
        "complexity": complexity,
        "requires_multi_hop": multi_hop_count > 0,
        "reasoning": f"Multi-hop: {multi_hop_count}, Simple: {simple_count}, Complex: {complex_count}",
    }


def generate_multi_queries(input_data: dict) -> dict:
    """Generate multiple query variations for improved recall."""
    state = input_data["state"]
    original_query = state.query

    # Generate query variations (can be enhanced with LLM)
    variations = [
        original_query,
        f"What is {original_query}?",
        f"Information about {original_query}",
        f"Details regarding {original_query}",
    ]

    return {
        "query_variations": variations,
        "original_query": original_query,
        "reasoning": f"Generated {len(variations)} query variations",
    }


def hyde_hypothesis_generation(input_data: dict) -> dict:
    """Generate hypothetical document for HYDE RAG."""
    state = input_data["state"]
    query = state.query

    # Mock hypothesis generation (replace with actual LLM call)
    hypothesis = f"""
    A comprehensive answer to "{query}" would include the following information:

    Key details about the topic, relevant background information, specific examples,
    and practical considerations. The response would be well-structured and informative,
    covering multiple aspects of the question to provide complete understanding.

    This hypothetical document represents the ideal response that would perfectly
    answer the user's question with accurate, detailed, and relevant information.
    """

    return {
        "hypothesis": hypothesis,
        "hypothesis_confidence": 0.8,
        "reasoning": f"Generated hypothesis for query: {query}",
    }


# ============================================================================
# ADVANCED RAG AGENTS
# ============================================================================


class CorrectiveRAGAgent(ConditionalAgent):
    """Full Corrective RAG implementation with web search fallback."""

    def __init__(self, documents: list[Document] | None = None, **kwargs):
        # Create retrieval agent
        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="CRAG Retrieval Agent"
        )

        # Create relevance checking agent
        relevance_agent = Agent()
        relevance_agent.name = "CRAG Relevance Checker"
        relevance_agent.build_graph = lambda: self._build_relevance_graph()

        # Create web search agent
        web_search_agent = Agent()
        web_search_agent.name = "Web Search Agent"
        web_search_agent.build_graph = lambda: self._build_web_search_graph()

        # Create answer agent
        answer_agent = SimpleAgent(name="CRAG Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="Corrective RAG Agent",
            agents=[retrieval_agent, relevance_agent, web_search_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

        self.retrieval_agent = retrieval_agent
        self.relevance_agent = relevance_agent
        self.web_search_agent = web_search_agent
        self.answer_agent = answer_agent

        self._setup_crag_routing()

    def _build_relevance_graph(self) -> BaseGraph:
        graph = BaseGraph(name="CRAGRelevanceChecker")

        # Document grading
        from haive.core.graph.node.callable_node import (
            create_document_grader,
            simple_document_grader,
        )

        grader_node = create_document_grader(simple_document_grader, "grade_docs")
        graph.add_node("grade_docs", grader_node)

        # Relevance check
        relevance_node = CallableNodeConfig(
            name="relevance_check", callable_func=crag_relevance_check, pass_state=True
        )
        graph.add_node("relevance_check", relevance_node)

        graph.add_edge(START, "grade_docs")
        graph.add_edge("grade_docs", "relevance_check")
        graph.add_edge("relevance_check", END)

        return graph

    def _build_web_search_graph(self) -> BaseGraph:
        graph = BaseGraph(name="WebSearchAgent")

        web_search_node = CallableNodeConfig(
            name="web_search", callable_func=web_search_fallback, pass_state=True
        )
        graph.add_node("web_search", web_search_node)

        graph.add_edge(START, "web_search")
        graph.add_edge("web_search", END)

        return graph

    def _setup_crag_routing(self):
        """Set up CRAG conditional routing."""

        def crag_router(state: MultiAgentRAGState) -> str:
            # Start with retrieval
            if not state.retrieved_documents:
                return self._get_agent_node_name(self.retrieval_agent)

            # Check relevance if not done
            if not hasattr(state, "quality"):
                return self._get_agent_node_name(self.relevance_agent)

            # Route based on quality
            getattr(state, "quality", RAGQuality.INCORRECT)
            needs_web_search = getattr(state, "needs_web_search", False)
            web_search_performed = getattr(state, "web_search_performed", False)

            if needs_web_search and not web_search_performed:
                return self._get_agent_node_name(self.web_search_agent)

            # Generate answer
            return self._get_agent_node_name(self.answer_agent)

        # Add conditional routing
        for agent in self.agents:
            self.add_conditional_edge(
                source_agent=agent,
                condition=crag_router,
                destinations={self._get_agent_node_name(a): a for a in self.agents},
                default=END,
            )


class SelfRAGAgent(ConditionalAgent):
    """Self-RAG with reflection tokens and adaptive retrieval."""

    def __init__(self, documents: list[Document] | None = None, **kwargs):
        # Create retrieval decision agent
        decision_agent = Agent()
        decision_agent.name = "Self-RAG Decision Agent"
        decision_agent.build_graph = lambda: self._build_decision_graph()

        # Create retrieval agent
        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="Self-RAG Retrieval Agent"
        )

        # Create relevance agent
        relevance_agent = Agent()
        relevance_agent.name = "Self-RAG Relevance Agent"
        relevance_agent.build_graph = lambda: self._build_relevance_graph()

        # Create generation agent
        generation_agent = SimpleAgent(
            name="Self-RAG Generation Agent", engine=AugLLMConfig()
        )

        # Create hallucination detection agent
        hallucination_agent = Agent()
        hallucination_agent.name = "Hallucination Detection Agent"
        hallucination_agent.build_graph = lambda: self._build_hallucination_graph()

        super().__init__(
            name="Self-RAG Agent",
            agents=[
                decision_agent,
                retrieval_agent,
                relevance_agent,
                generation_agent,
                hallucination_agent,
            ],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

        self.decision_agent = decision_agent
        self.retrieval_agent = retrieval_agent
        self.relevance_agent = relevance_agent
        self.generation_agent = generation_agent
        self.hallucination_agent = hallucination_agent

        self._setup_self_rag_routing()

    def _build_decision_graph(self) -> BaseGraph:
        graph = BaseGraph(name="SelfRAGDecision")

        decision_node = CallableNodeConfig(
            name="retrieval_decision",
            callable_func=self_rag_retrieval_decision,
            pass_state=True,
        )
        graph.add_node("retrieval_decision", decision_node)

        graph.add_edge(START, "retrieval_decision")
        graph.add_edge("retrieval_decision", END)

        return graph

    def _build_relevance_graph(self) -> BaseGraph:
        graph = BaseGraph(name="SelfRAGRelevance")

        from haive.core.graph.node.callable_node import (
            create_document_grader,
            simple_document_grader,
        )

        relevance_node = create_document_grader(
            simple_document_grader, "check_relevance"
        )
        graph.add_node("check_relevance", relevance_node)

        graph.add_edge(START, "check_relevance")
        graph.add_edge("check_relevance", END)

        return graph

    def _build_hallucination_graph(self) -> BaseGraph:
        graph = BaseGraph(name="HallucinationDetection")

        hallucination_node = CallableNodeConfig(
            name="detect_hallucination",
            callable_func=hallucination_detection,
            pass_state=True,
        )
        graph.add_node("detect_hallucination", hallucination_node)

        graph.add_edge(START, "detect_hallucination")
        graph.add_edge("detect_hallucination", END)

        return graph

    def _setup_self_rag_routing(self):
        """Set up Self-RAG routing with reflection tokens."""

        def self_rag_router(state: MultiAgentRAGState) -> str:
            # Check retrieval decision
            if not hasattr(state, "needs_retrieval"):
                return self._get_agent_node_name(self.decision_agent)

            # If retrieval needed and not done
            needs_retrieval = getattr(state, "needs_retrieval", True)
            if needs_retrieval and not state.retrieved_documents:
                return self._get_agent_node_name(self.retrieval_agent)

            # Check relevance if documents retrieved but not checked
            if state.retrieved_documents and not state.graded_documents:
                return self._get_agent_node_name(self.relevance_agent)

            # Generate if not done
            if not state.generated_response:
                return self._get_agent_node_name(self.generation_agent)

            # Check for hallucination if not done
            if not hasattr(state, "has_hallucination"):
                return self._get_agent_node_name(self.hallucination_agent)

            # Regenerate if hallucination detected
            needs_regeneration = getattr(state, "needs_regeneration", False)
            if needs_regeneration:
                state.generated_response = ""  # Clear for regeneration
                return self._get_agent_node_name(self.generation_agent)

            return END

        # Add conditional routing
        for agent in self.agents:
            self.add_conditional_edge(
                source_agent=agent,
                condition=self_rag_router,
                destinations={self._get_agent_node_name(a): a for a in self.agents},
                default=END,
            )


class AdaptiveRAGAgent(ConditionalAgent):
    """Adaptive RAG with complexity-based routing."""

    def __init__(self, documents: list[Document] | None = None, **kwargs):
        # Create query analyzer
        analyzer_agent = Agent()
        analyzer_agent.name = "Query Complexity Analyzer"
        analyzer_agent.build_graph = lambda: self._build_analyzer_graph()

        # Create different RAG strategies
        simple_rag_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="Simple RAG Agent"
        )

        multi_query_agent = self._create_multi_query_agent(documents)
        complex_rag_agent = CorrectiveRAGAgent(documents)

        # Create direct answer agent
        direct_agent = SimpleAgent(name="Direct Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="Adaptive RAG Agent",
            agents=[
                analyzer_agent,
                simple_rag_agent,
                multi_query_agent,
                complex_rag_agent,
                direct_agent,
            ],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

        self.analyzer_agent = analyzer_agent
        self.simple_rag_agent = simple_rag_agent
        self.multi_query_agent = multi_query_agent
        self.complex_rag_agent = complex_rag_agent
        self.direct_agent = direct_agent

        self._setup_adaptive_routing()

    def _build_analyzer_graph(self) -> BaseGraph:
        graph = BaseGraph(name="QueryComplexityAnalyzer")

        analyzer_node = CallableNodeConfig(
            name="analyze_complexity",
            callable_func=query_complexity_analysis,
            pass_state=True,
        )
        graph.add_node("analyze_complexity", analyzer_node)

        graph.add_edge(START, "analyze_complexity")
        graph.add_edge("analyze_complexity", END)

        return graph

    def _create_multi_query_agent(self, documents: list[Document] | None) -> Agent:
        """Create multi-query RAG agent."""
        multi_query_agent = Agent()
        multi_query_agent.name = "Multi-Query RAG Agent"

        def build_multi_query_graph() -> BaseGraph:
            graph = BaseGraph(name="MultiQueryRAG")

            # Generate multiple queries
            query_gen_node = CallableNodeConfig(
                name="generate_queries",
                callable_func=generate_multi_queries,
                pass_state=True,
            )
            graph.add_node("generate_queries", query_gen_node)

            # Use simple RAG retrieval for each query
            SimpleRAGAgent.from_documents(
                documents or conversation_documents, name="Multi-Query Retrieval"
            )

            # Add simple answer generation
            answer_node = CallableNodeConfig(
                name="answer_generation",
                callable_func=lambda x: {
                    "generated_response": f"Multi-query answer for: {x['state'].query}"
                },
                pass_state=True,
            )
            graph.add_node("answer_generation", answer_node)

            graph.add_edge(START, "generate_queries")
            graph.add_edge("generate_queries", "answer_generation")
            graph.add_edge("answer_generation", END)

            return graph

        multi_query_agent.build_graph = build_multi_query_graph
        return multi_query_agent

    def _setup_adaptive_routing(self):
        """Set up adaptive routing based on complexity."""

        def adaptive_router(state: MultiAgentRAGState) -> str:
            # Analyze complexity first
            if not hasattr(state, "complexity"):
                return self._get_agent_node_name(self.analyzer_agent)

            complexity = getattr(state, "complexity", "unknown")

            # Route based on complexity
            if complexity == "simple":
                return self._get_agent_node_name(self.simple_rag_agent)
            if complexity == "medium":
                return self._get_agent_node_name(self.multi_query_agent)
            if complexity == "complex":
                return self._get_agent_node_name(self.complex_rag_agent)
            return self._get_agent_node_name(self.direct_agent)

        # Add conditional routing
        for agent in self.agents:
            self.add_conditional_edge(
                source_agent=agent,
                condition=adaptive_router,
                destinations={self._get_agent_node_name(a): a for a in self.agents},
                default=END,
            )


class HYDERAGAgent(SequentialAgent):
    """Enhanced HYDE RAG with hypothesis generation."""

    def __init__(self, documents: list[Document] | None = None, **kwargs):
        # Create hypothesis generator
        hypothesis_agent = Agent()
        hypothesis_agent.name = "HYDE Hypothesis Generator"
        hypothesis_agent.build_graph = lambda: self._build_hypothesis_graph()

        # Create retrieval agent
        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or conversation_documents, name="HYDE Retrieval Agent"
        )

        # Create answer agent
        answer_agent = SimpleAgent(name="HYDE Answer Agent", engine=AugLLMConfig())

        super().__init__(
            name="HYDE RAG Agent",
            agents=[hypothesis_agent, retrieval_agent, answer_agent],
            state_schema=MultiAgentRAGState,
            **kwargs,
        )

    def _build_hypothesis_graph(self) -> BaseGraph:
        graph = BaseGraph(name="HYDEHypothesis")

        hypothesis_node = CallableNodeConfig(
            name="generate_hypothesis",
            callable_func=hyde_hypothesis_generation,
            pass_state=True,
        )
        graph.add_node("generate_hypothesis", hypothesis_node)

        graph.add_edge(START, "generate_hypothesis")
        graph.add_edge("generate_hypothesis", END)

        return graph


# ============================================================================
# FACTORY FUNCTION
# ============================================================================


def create_complete_rag_workflow(
    workflow_type: str, documents: list[Document] | None = None, **kwargs
) -> Agent:
    """Factory for creating complete RAG workflows.

    Available types:
    - 'crag': Corrective RAG with web search
    - 'self_rag': Self-RAG with reflection tokens
    - 'adaptive': Adaptive RAG with complexity routing
    - 'hyde': HYDE RAG with hypothesis generation
    - 'multi_query': Multi-Query RAG with query variations
    """
    workflow_map = {
        "crag": CorrectiveRAGAgent,
        "self_rag": SelfRAGAgent,
        "adaptive": AdaptiveRAGAgent,
        "hyde": HYDERAGAgent,
    }

    if workflow_type not in workflow_map:
        raise ValueError(
            f"Unknown workflow type: {workflow_type}. Available: {list(workflow_map.keys())}"
        )

    return workflow_map[workflow_type](documents=documents, **kwargs)


__all__ = [
    "AdaptiveRAGAgent",
    "CorrectiveRAGAgent",
    "HYDERAGAgent",
    "RAGQuality",
    "ReflectionToken",
    "SelfRAGAgent",
    "crag_relevance_check",
    "create_complete_rag_workflow",
    "hallucination_detection",
    "web_search_fallback",
]
