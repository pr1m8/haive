"""Complete Collection of RAG Agents using ChainAgent.

This module provides a comprehensive collection of Retrieval-Augmented Generation (RAG)
agents implemented using the ChainAgent framework. Each agent represents a different
RAG strategy or pattern, optimized for specific use cases.

Example:
    >>> from haive.agents.rag.chain_collection import RAGChainCollection
    >>> from langchain_core.documents import Document
    >>> from haive.core.models.llm.base import AzureLLMConfig
    >>>
    >>> docs = [Document(page_content="AI is transforming industries...")]
    >>> llm_config = AzureLLMConfig(deployment_name="gpt-4")
    >>> collection = RAGChainCollection()
    >>> agent = collection.create_simple_rag(docs, llm_config)

Typical usage:
    - Create documents for retrieval
    - Choose appropriate RAG strategy
    - Configure LLM and retrieval settings
    - Build agent using collection methods
    - Execute queries through agent interface

Available RAG Strategies:
    - Simple RAG: Basic retrieve-and-generate pattern
    - HyDE RAG: Hypothetical document generation for enhanced retrieval
    - Fusion RAG: Multi-query retrieval with reciprocal rank fusion
    - Step-Back RAG: Abstract reasoning before specific answers
    - Speculative RAG: Hypothesis generation and verification
    - Memory-Aware RAG: Conversation context integration
    - FLARE RAG: Forward-looking active retrieval with refinement
"""

import logging
from typing import Any, Callable, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate

from haive.agents.chain import ChainAgent, flow, flow_with_edges
from haive.agents.rag.models import (
    FusionResult,
    HyDEResult,
    MemoryAnalysis,
    MemoryEntry,
    SpeculativeResult,
    StepBackResult,
)

logger = logging.getLogger(__name__)


# Models are now imported from haive.agents.rag.models


# Collection of ChainAgent RAG implementations
class RAGChainCollection:
    """Collection of all RAG agents as ChainAgents.

    This class provides static factory methods for creating different types
    of RAG agents using the ChainAgent framework. Each method builds a
    complete RAG workflow with appropriate retrieval and generation steps.

    Example:
        >>> collection = RAGChainCollection()
        >>> agent = collection.create_simple_rag(documents, llm_config)
        >>> response = agent.invoke({"query": "What is machine learning?"})
    """

    @staticmethod
    def create_simple_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """Create a simple RAG agent with basic retrieve-and-generate pattern.

        This is the most straightforward RAG implementation: retrieve relevant
        documents based on the query, then generate an answer using those documents
        as context.

        Args:
            documents (List[Document]): Documents to use for retrieval.
            llm_config (LLMConfig): LLM configuration for generation.

        Returns:
            ChainAgent: A configured simple RAG agent.

        Example:
            >>> from langchain_core.documents import Document
            >>> docs = [Document(page_content="AI helps solve problems...")]
            >>> agent = RAGChainCollection.create_simple_rag(docs, llm_config)
        """

        # Simple retrieval mock
        def retrieve(state: dict[str, Any]) -> dict[str, Any]:
            state.get("query", "")
            # Mock retrieval - in real implementation would use vector search
            relevant_docs = documents[:3]  # Top 3 docs
            context = "\n\n".join([doc.page_content for doc in relevant_docs])
            return {"context": context, "retrieved_docs": len(relevant_docs)}

        # Answer generator
        generator = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Answer based on the provided context"),
                    ("human", "Context: {context}\n\nQuery: {query}"),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(retrieve, generator, name="Simple RAG")

    @staticmethod
    def create_hyde_rag(documents: list[Document], llm_config: LLMConfig) -> ChainAgent:
        """HyDE RAG - generate hypothetical document first."""
        # Hypothetical document generator
        hyde_generator = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Generate a hypothetical document that would answer this query",
                    ),
                    ("human", "{query}"),
                ]
            ),
            structured_output_model=HyDEResult,
            output_key="hyde_result",
        )

        # Enhanced retrieval using hypothesis
        def enhanced_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            hyde_result = state.get("hyde_result", {})
            hypothetical_doc = hyde_result.get("hypothetical_doc", "")

            # Use hypothesis to improve retrieval (mock)
            enhanced_query = f"{state.get('query', '')} {hypothetical_doc}"
            relevant_docs = documents[:3]
            context = "\n\n".join([doc.page_content for doc in relevant_docs])

            return {"context": context, "enhanced_query": enhanced_query}

        # Final answer
        answerer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Answer using context and the hypothetical document insight",
                    ),
                    (
                        "human",
                        """Original Query: {query}
                Hypothetical Document: {hyde_result}
                Retrieved Context: {context}

                Provide a comprehensive answer.""",
                    ),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(hyde_generator, enhanced_retrieve, answerer, name="HyDE RAG")

    @staticmethod
    def create_fusion_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """Fusion RAG - multiple queries with reciprocal rank fusion."""
        # Multi-query generator
        multi_query_gen = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Generate 3 different queries to comprehensively answer the question",
                    ),
                    ("human", "{query}"),
                ]
            ),
            output_key="multi_queries",
        )

        # Fusion ranker
        def fusion_rank(state: dict[str, Any]) -> dict[str, Any]:
            # Mock fusion ranking
            state.get("multi_queries", "").split("\n")[:3]

            # Simulate retrieving for each query and fusing results
            all_docs = documents[:5]
            fusion_scores = [0.9, 0.8, 0.7, 0.6, 0.5]  # Mock scores

            fusion_result = FusionResult(
                fused_documents=[doc.page_content for doc in all_docs],
                fusion_scores=fusion_scores,
                ranking_method="reciprocal_rank_fusion",
            )

            return {"fusion_result": fusion_result}

        # Final synthesis
        synthesizer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Synthesize answer from fusion-ranked documents"),
                    (
                        "human",
                        """Query: {query}
                Fusion Results: {fusion_result}

                Create comprehensive answer.""",
                    ),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(multi_query_gen, fusion_rank, synthesizer, name="Fusion RAG")

    @staticmethod
    def create_step_back_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """Step-Back RAG - abstract reasoning before specific answer."""
        # Step-back reasoner
        step_back = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Think step-back: what higher-level concept does this query relate to?",
                    ),
                    ("human", "{query}"),
                ]
            ),
            structured_output_model=StepBackResult,
            output_key="step_back_result",
        )

        # Enhanced context retrieval
        def context_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            step_back_result = state.get("step_back_result", {})
            abstract_answer = step_back_result.get("abstract_answer", "")

            # Use abstract reasoning to guide retrieval
            context = "\n\n".join([doc.page_content for doc in documents[:3]])

            return {"context": context, "abstract_context": abstract_answer}

        # Final answerer
        answerer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Answer using both abstract reasoning and specific context",
                    ),
                    (
                        "human",
                        """Original Query: {query}
                Abstract Reasoning: {step_back_result}
                Specific Context: {context}

                Provide a well-reasoned answer.""",
                    ),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(step_back, context_retrieve, answerer, name="Step-Back RAG")

    @staticmethod
    def create_speculative_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """Speculative RAG - generate and verify hypotheses."""
        # Hypothesis generator
        hypothesis_gen = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Generate 3 hypotheses that could answer this query"),
                    ("human", "{query}"),
                ]
            ),
            structured_output_model=SpeculativeResult,
            output_key="speculative_result",
        )

        # Hypothesis verifier
        def verify_hypotheses(state: dict[str, Any]) -> dict[str, Any]:
            speculative_result = state.get("speculative_result", {})
            hypotheses = speculative_result.get("hypotheses", [])

            # Mock verification against documents
            verified = []
            for hypothesis in hypotheses[:2]:  # Verify first 2
                # Check if hypothesis is supported by documents (simplified)
                if any(
                    keyword in doc.page_content.lower()
                    for doc in documents
                    for keyword in hypothesis.lower().split()[:3]
                ):
                    verified.append(hypothesis)

            return {"verified_hypotheses": verified}

        # Final synthesis
        synthesizer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Create final answer based on verified hypotheses"),
                    (
                        "human",
                        """Query: {query}
                Verified Hypotheses: {verified_hypotheses}

                Synthesize final answer.""",
                    ),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(
            hypothesis_gen, verify_hypotheses, synthesizer, name="Speculative RAG"
        )

    @staticmethod
    def create_memory_aware_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """Memory-Aware RAG - uses conversation memory."""

        # Memory analyzer
        def analyze_memory(state: dict[str, Any]) -> dict[str, Any]:
            # Mock memory analysis
            state.get("query", "")
            messages = state.get("messages", [])

            # Extract relevant past context (simplified)
            past_topics = ["AI", "machine learning"] if len(messages) > 1 else []
            temporal_context = (
                "Continuing previous discussion" if past_topics else "New topic"
            )

            return {
                "relevant_memories": past_topics,
                "temporal_context": temporal_context,
                "has_memory": len(past_topics) > 0,
            }

        # Context-aware retrieval
        def memory_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            query = state.get("query", "")
            relevant_memories = state.get("relevant_memories", [])

            # Enhanced query with memory context
            enhanced_query = f"{query} {' '.join(relevant_memories)}"
            context = "\n\n".join([doc.page_content for doc in documents[:3]])

            return {"context": context, "enhanced_query": enhanced_query}

        # Memory-enhanced answerer
        answerer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Answer considering conversation history and temporal context",
                    ),
                    (
                        "human",
                        """Current Query: {query}
                Temporal Context: {temporal_context}
                Relevant Memories: {relevant_memories}
                Retrieved Context: {context}

                Provide contextually aware answer.""",
                    ),
                ]
            ),
            output_key="response",
        )

        return ChainAgent(
            analyze_memory, memory_retrieve, answerer, name="Memory-Aware RAG"
        )

    @staticmethod
    def create_flare_rag(
        documents: list[Document], llm_config: LLMConfig
    ) -> ChainAgent:
        """FLARE RAG - forward-looking active retrieval."""
        # Initial answer attempt
        initial_gen = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        "Provide initial answer, noting what additional info you need",
                    ),
                    ("human", "{query}"),
                ]
            ),
            output_key="initial_answer",
        )

        # Active retrieval based on gaps
        def active_retrieve(state: dict[str, Any]) -> dict[str, Any]:
            initial_answer = state.get("initial_answer", "")

            # Identify information gaps (simplified)
            needs_more_info = (
                "need" in initial_answer.lower() or "unclear" in initial_answer.lower()
            )

            if needs_more_info:
                # Retrieve additional context
                additional_context = "\n".join(
                    [doc.page_content for doc in documents[1:3]]
                )
                return {
                    "additional_context": additional_context,
                    "needs_refinement": True,
                }
            return {"needs_refinement": False}

        # Conditional refinement
        def maybe_refine(state: dict[str, Any]) -> dict[str, Any]:
            if state.get("needs_refinement", False):
                # Use LLM to refine answer
                refined_engine = AugLLMConfig(
                    llm_config=llm_config,
                    prompt_template=ChatPromptTemplate.from_messages(
                        [
                            ("system", "Refine answer with additional context"),
                            (
                                "human",
                                """Query: {query}
                        Initial Answer: {initial_answer}
                        Additional Context: {additional_context}

                        Provide refined answer.""",
                            ),
                        ]
                    ),
                    output_key="response",
                )
                return refined_engine.invoke(state)
            return {"response": state.get("initial_answer", "")}

        return ChainAgent(initial_gen, active_retrieve, maybe_refine, name="FLARE RAG")


# Factory functions for easy creation
def create_rag_chain(
    rag_type: str,
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    **kwargs,
) -> ChainAgent:
    """Create any RAG chain by type."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    collection = RAGChainCollection()

    if rag_type == "simple":
        return collection.create_simple_rag(documents, llm_config)
    if rag_type == "hyde":
        return collection.create_hyde_rag(documents, llm_config)
    if rag_type == "fusion":
        return collection.create_fusion_rag(documents, llm_config)
    if rag_type == "step_back":
        return collection.create_step_back_rag(documents, llm_config)
    if rag_type == "speculative":
        return collection.create_speculative_rag(documents, llm_config)
    if rag_type == "memory_aware":
        return collection.create_memory_aware_rag(documents, llm_config)
    elif rag_type == "flare":
        return collection.create_flare_rag(documents, llm_config)
    else:
        raise ValueError(f"Unknown RAG type: {rag_type}")


# Multi-RAG pipeline
def create_rag_pipeline(
    rag_types: list[str],
    documents: list[Document],
    combination_strategy: str = "sequential",
    llm_config: LLMConfig | None = None,
) -> ChainAgent:
    """Create a pipeline of multiple RAG approaches."""
    chains = [
        create_rag_chain(rag_type, documents, llm_config) for rag_type in rag_types
    ]

    if combination_strategy == "sequential":
        # Sequential execution
        return ChainAgent(*chains, name="RAG Pipeline")
    if combination_strategy == "parallel":
        # All run in parallel then combine (simplified)
        def combiner(state):
            return {"combined_responses": [state.get("response", "")]}

        return flow_with_edges(
            [*chains, combiner], *[f"{i}->-1" for i in range(len(chains))]
        )
    raise ValueError(f"Unknown combination strategy: {combination_strategy}")


# All available RAG types
RAG_TYPES = [
    "simple",
    "hyde",
    "fusion",
    "step_back",
    "speculative",
    "memory_aware",
    "flare",
]
