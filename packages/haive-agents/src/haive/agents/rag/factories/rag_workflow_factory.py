"""RAG Workflow Factory.

Generic factory for creating RAG workflows by composing callable functions
into different agent patterns. This provides a clean, modular approach to
building complex RAG systems.
"""

from collections.abc import Callable
from typing import Dict, List, Optional

from haive.core.graph.node.callable_node import CallableNodeConfig
from haive.core.graph.node.rag_callables import *
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.schema.prebuilt.rag_state import MultiAgentRAGState
from langchain_core.documents import Document
from langgraph.graph import END, START

from haive.agents.base.agent import Agent
from haive.agents.multi.base import ConditionalAgent, SequentialAgent
from haive.agents.rag.base.agent import SimpleRAGAgent


class GenericCallableAgent(Agent):
    """Generic agent that executes a sequence of callable functions."""

    def __init__(
        self, callables: list[Callable], name: str = "Generic Callable Agent", **kwargs
    ):
        super().__init__(name=name, **kwargs)
        self.callables = callables

    def build_graph(self) -> BaseGraph:
        """Build graph with callable sequence."""
        graph = BaseGraph(name=self.name.replace(" ", ""))

        # Add each callable as a node
        prev_node = START
        for i, callable_func in enumerate(self.callables):
            node_name = f"step_{i}"

            callable_node = CallableNodeConfig(
                name=node_name, callable_func=callable_func, pass_state=True
            )

            graph.add_node(node_name, callable_node)
            graph.add_edge(prev_node, node_name)
            prev_node = node_name

        graph.add_edge(prev_node, END)
        return graph


class ConditionalCallableAgent(Agent):
    """Agent with conditional routing based on callable results."""

    def __init__(
        self,
        router_callable: Callable,
        action_callables: dict[str, Callable],
        name: str = "Conditional Callable Agent",
        **kwargs,
    ):
        super().__init__(name=name, **kwargs)
        self.router_callable = router_callable
        self.action_callables = action_callables

    def build_graph(self) -> BaseGraph:
        """Build graph with conditional routing."""
        graph = BaseGraph(name=self.name.replace(" ", ""))

        # Add router node
        router_node = CallableNodeConfig(
            name="router", callable_func=self.router_callable, pass_state=True
        )
        graph.add_node("router", router_node)
        graph.add_edge(START, "router")

        # Add action nodes
        for action_name, callable_func in self.action_callables.items():
            action_node = CallableNodeConfig(
                name=action_name, callable_func=callable_func, pass_state=True
            )
            graph.add_node(action_name, action_node)

        # Add conditional edges from router
        def route_condition(state) -> str:
            next_action = getattr(state, "next_action", "complete")
            if next_action in self.action_callables:
                return next_action
            return END

        destinations = {name: name for name in self.action_callables}
        destinations[END] = END

        graph.add_conditional_edges(
            "router", route_condition, destinations, default=END
        )

        # Add edges from actions back to router (for loops)
        for action_name in self.action_callables:
            graph.add_edge(action_name, "router")

        return graph


# ============================================================================
# SPECIFIC RAG WORKFLOW FACTORIES
# ============================================================================


def create_corrective_rag_agent(
    documents: list[Document] | None = None, name: str = "Corrective RAG Agent"
) -> Agent:
    """Create a CRAG agent with web search fallback."""
    # Create base retrieval agent
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="CRAG Retrieval"
    )

    # Create conditional agent with CRAG logic
    router_callable = rag_workflow_router

    action_callables = {
        "grade_documents": advanced_document_grader,
        "check_relevance": relevance_threshold_check,
        "web_search": web_search_simulator,
        "generate_response": response_generator,
        "validate_response": hallucination_detector,
    }

    crag_agent = ConditionalCallableAgent(
        router_callable=router_callable, action_callables=action_callables, name=name
    )

    return SequentialAgent(
        name=name, agents=[retrieval_agent, crag_agent], state_schema=MultiAgentRAGState
    )


def create_self_rag_agent(
    documents: list[Document] | None = None, name: str = "Self-RAG Agent"
) -> Agent:
    """Create a Self-RAG agent with reflection tokens."""

    # Self-RAG specific router
    def self_rag_router(input_data: dict) -> dict:
        state = input_data["state"]

        if not hasattr(state, "needs_retrieval"):
            return {"next_action": "decide_retrieval"}

        needs_retrieval = getattr(state, "needs_retrieval", True)
        if needs_retrieval and not state.retrieved_documents:
            return {"next_action": "retrieve_documents"}

        if state.retrieved_documents and not state.graded_documents:
            return {"next_action": "check_relevance"}

        if not getattr(state, "generated_response", ""):
            return {"next_action": "generate_response"}

        if not hasattr(state, "has_hallucination"):
            return {"next_action": "detect_hallucination"}

        if getattr(state, "needs_regeneration", False):
            return {"next_action": "regenerate_response"}

        return {"next_action": "complete"}

    # Retrieval decision function
    def retrieval_decision(input_data: dict) -> dict:
        state = input_data["state"]
        query = getattr(state, "query", "").lower()

        # Check if query needs external knowledge
        needs_external = any(
            term in query
            for term in [
                "current",
                "latest",
                "recent",
                "today",
                "price",
                "cost",
                "address",
            ]
        )

        return {
            "needs_retrieval": needs_external,
            "retrieval_token": "[Retrieval]" if needs_external else "[No Retrieval]",
        }

    # Create retrieval agent
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="Self-RAG Retrieval"
    )

    # Create conditional agent
    action_callables = {
        "decide_retrieval": retrieval_decision,
        "check_relevance": relevance_threshold_check,
        "generate_response": response_generator,
        "detect_hallucination": hallucination_detector,
        "regenerate_response": response_generator,  # Same as generate but clears previous
    }

    self_rag_agent = ConditionalCallableAgent(
        router_callable=self_rag_router,
        action_callables=action_callables,
        name="Self-RAG Logic",
    )

    return SequentialAgent(
        name=name,
        agents=[retrieval_agent, self_rag_agent],
        state_schema=MultiAgentRAGState,
    )


def create_adaptive_rag_agent(
    documents: list[Document] | None = None, name: str = "Adaptive RAG Agent"
) -> Agent:
    """Create an adaptive RAG agent with complexity-based routing."""
    # Create different RAG strategies
    simple_rag = SimpleRAGAgent.from_documents(documents or [], name="Simple RAG")

    # Multi-query agent
    multi_query_callables = [query_rewriter, response_generator]
    multi_query_agent = GenericCallableAgent(
        callables=multi_query_callables, name="Multi-Query RAG"
    )

    # Complex RAG (CRAG)
    complex_rag = create_corrective_rag_agent(documents, "Complex RAG")

    # Adaptive router
    def adaptive_router(state) -> str:
        complexity = getattr(state, "complexity", QueryComplexity.UNKNOWN)

        if complexity == QueryComplexity.SIMPLE:
            return "simple_rag"
        if complexity == QueryComplexity.MEDIUM:
            return "multi_query_rag"
        if complexity == QueryComplexity.COMPLEX:
            return "complex_rag"
        return "simple_rag"  # Default

    # Create analyzer agent
    analyzer_agent = GenericCallableAgent(
        callables=[query_complexity_analyzer], name="Query Analyzer"
    )

    # Create conditional multi-agent
    class AdaptiveRAGAgent(ConditionalAgent):
        def __init__(self):
            super().__init__(
                name=name,
                agents=[analyzer_agent, simple_rag, multi_query_agent, complex_rag],
                state_schema=MultiAgentRAGState,
            )

            # Set up routing
            self.add_conditional_edge(
                source_agent=analyzer_agent,
                condition=adaptive_router,
                destinations={
                    "simple_rag": simple_rag,
                    "multi_query_rag": multi_query_agent,
                    "complex_rag": complex_rag,
                },
                default=simple_rag,
            )

    return AdaptiveRAGAgent()


def create_hyde_rag_agent(
    documents: list[Document] | None = None, name: str = "HYDE RAG Agent"
) -> Agent:
    """Create a HYDE RAG agent with hypothesis generation."""
    # HYDE workflow callables
    hyde_callables = [hyde_hypothesis_generator, response_generator]

    hyde_agent = GenericCallableAgent(callables=hyde_callables, name="HYDE Generator")

    # Create retrieval agent
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="HYDE Retrieval"
    )

    return SequentialAgent(
        name=name,
        agents=[
            hyde_agent,
            retrieval_agent,
            hyde_agent,
        ],  # Generate hypothesis, retrieve, answer
        state_schema=MultiAgentRAGState,
    )


def create_step_back_rag_agent(
    documents: list[Document] | None = None, name: str = "Step-Back RAG Agent"
) -> Agent:
    """Create a step-back prompting RAG agent."""
    # Step-back workflow
    step_back_callables = [step_back_query_generator, response_generator]

    step_back_agent = GenericCallableAgent(
        callables=step_back_callables, name="Step-Back Generator"
    )

    # Create dual retrieval (original + step-back)
    original_retrieval = SimpleRAGAgent.from_documents(
        documents or [], name="Original Retrieval"
    )

    step_back_retrieval = SimpleRAGAgent.from_documents(
        documents or [], name="Step-Back Retrieval"
    )

    return SequentialAgent(
        name=name,
        agents=[
            step_back_agent,
            original_retrieval,
            step_back_retrieval,
            step_back_agent,
        ],
        state_schema=MultiAgentRAGState,
    )


def create_multi_query_rag_agent(
    documents: list[Document] | None = None, name: str = "Multi-Query RAG Agent"
) -> Agent:
    """Create a multi-query RAG agent with query variations."""
    multi_query_callables = [query_rewriter, response_generator]

    multi_query_agent = GenericCallableAgent(
        callables=multi_query_callables, name="Multi-Query Processor"
    )

    # Multiple retrievals could be done in parallel here
    retrieval_agent = SimpleRAGAgent.from_documents(
        documents or [], name="Multi-Query Retrieval"
    )

    return SequentialAgent(
        name=name,
        agents=[multi_query_agent, retrieval_agent, multi_query_agent],
        state_schema=MultiAgentRAGState,
    )


# ============================================================================
# MAIN FACTORY FUNCTION
# ============================================================================


def create_rag_workflow(
    workflow_type: str,
    documents: list[Document] | None = None,
    custom_callables: dict[str, Callable] | None = None,
    **kwargs,
) -> Agent:
    """Main factory function for creating RAG workflows.

    Args:
        workflow_type: Type of RAG workflow to create
        documents: Documents for retrieval
        custom_callables: Custom callable functions to override defaults
        **kwargs: Additional arguments

    Returns:
        Configured RAG agent

    Available workflow types:
        - 'corrective' / 'crag': Corrective RAG with web search
        - 'self_rag': Self-RAG with reflection tokens
        - 'adaptive': Adaptive RAG with complexity routing
        - 'hyde': HYDE RAG with hypothesis generation
        - 'step_back': Step-back prompting RAG
        - 'multi_query': Multi-query RAG with variations
        - 'simple': Basic sequential RAG
    """
    factory_map = {
        "corrective": create_corrective_rag_agent,
        "crag": create_corrective_rag_agent,
        "self_rag": create_self_rag_agent,
        "adaptive": create_adaptive_rag_agent,
        "hyde": create_hyde_rag_agent,
        "step_back": create_step_back_rag_agent,
        "multi_query": create_multi_query_rag_agent,
    }

    if workflow_type == "simple":
        # Create simple RAG with basic validation
        retrieval_agent = SimpleRAGAgent.from_documents(
            documents or [], name="Simple RAG"
        )
        validator_agent = GenericCallableAgent(
            callables=[response_validator], name="Response Validator"
        )
        return SequentialAgent(
            name="Simple RAG Agent",
            agents=[retrieval_agent, validator_agent],
            state_schema=MultiAgentRAGState,
        )

    if workflow_type not in factory_map:
        available = [*list(factory_map.keys()), "simple"]
        raise ValueError(
            f"Unknown workflow type: {workflow_type}. Available: {available}"
        )

    return factory_map[workflow_type](documents=documents, **kwargs)


__all__ = [
    "ConditionalCallableAgent",
    "GenericCallableAgent",
    "create_adaptive_rag_agent",
    "create_corrective_rag_agent",
    "create_hyde_rag_agent",
    "create_multi_query_rag_agent",
    "create_rag_workflow",
    "create_self_rag_agent",
    "create_step_back_rag_agent",
]
