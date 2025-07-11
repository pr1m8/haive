"""Modular RAG using ChainAgent.

Build configurable RAG pipelines with modular components.
"""

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain import ChainAgent, flow_with_edges


class RAGModule(str, Enum):
    """Available RAG modules."""

    QUERY_EXPANSION = "query_expansion"
    DOCUMENT_FILTERING = "document_filtering"
    CONTEXT_RANKING = "context_ranking"
    ANSWER_GENERATION = "answer_generation"
    ANSWER_VERIFICATION = "answer_verification"
    RESPONSE_SYNTHESIS = "response_synthesis"


class ModularConfig(BaseModel):
    """Configuration for modular RAG."""

    modules: list[RAGModule] = Field(description="Modules to include")
    routing_strategy: Literal["sequential", "conditional", "parallel"] = Field(
        default="sequential"
    )
    quality_gates: bool = Field(default=True, description="Include quality checkpoints")


def create_modular_rag(
    documents: list[Document],
    config: ModularConfig,
    llm_config: LLMConfig | None = None,
    name: str = "Modular RAG",
) -> ChainAgent:
    """Create a modular RAG system with configurable components."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Build nodes based on configuration
    nodes = []

    # Query Expansion Module
    if RAGModule.QUERY_EXPANSION in config.modules:
        query_expander = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Expand the query with synonyms and related terms"),
                    ("human", "{query}"),
                ]
            ),
            output_key="expanded_query",
        )
        nodes.append(query_expander)

    # Document Filtering Module
    if RAGModule.DOCUMENT_FILTERING in config.modules:

        def filter_documents(state: dict[str, Any]) -> dict[str, Any]:
            query = state.get("expanded_query") or state.get("query", "")

            # Simple relevance filtering (mock)
            filtered_docs = [
                doc
                for doc in documents
                if any(
                    word.lower() in doc.page_content.lower()
                    for word in query.split()[:3]
                )
            ]

            return {
                "filtered_documents": filtered_docs[:5],
                "filter_count": len(filtered_docs),
            }

        nodes.append(filter_documents)

    # Context Ranking Module
    if RAGModule.CONTEXT_RANKING in config.modules:
        context_ranker = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Rank document relevance for the query"),
                    (
                        "human",
                        """Query: {query}
                Documents: {filtered_documents}

                Rank by relevance and provide top 3.""",
                    ),
                ]
            ),
            output_key="ranked_context",
        )
        nodes.append(context_ranker)

    # Answer Generation Module
    if RAGModule.ANSWER_GENERATION in config.modules:
        answer_generator = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Generate answer based on ranked context"),
                    (
                        "human",
                        """Query: {query}
                Context: {ranked_context}

                Provide comprehensive answer.""",
                    ),
                ]
            ),
            output_key="generated_answer",
        )
        nodes.append(answer_generator)

    # Answer Verification Module
    if RAGModule.ANSWER_VERIFICATION in config.modules:

        def verify_answer(state: dict[str, Any]) -> dict[str, Any]:
            answer = state.get("generated_answer", "")
            state.get("ranked_context", "")

            # Simple verification (mock)
            is_supported = len(answer) > 10 and "context" not in answer.lower()
            confidence = 0.8 if is_supported else 0.4

            return {
                "verification_result": {
                    "is_supported": is_supported,
                    "confidence": confidence,
                    "verified_answer": (
                        answer if is_supported else "Answer needs more evidence"
                    ),
                }
            }

        nodes.append(verify_answer)

    # Response Synthesis Module
    if RAGModule.RESPONSE_SYNTHESIS in config.modules:
        synthesizer = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [
                    ("system", "Synthesize final response with confidence indicators"),
                    (
                        "human",
                        """Original Query: {query}
                Generated Answer: {generated_answer}
                Verification: {verification_result}

                Create final response.""",
                    ),
                ]
            ),
            output_key="response",
        )
        nodes.append(synthesizer)

    # Default minimal pipeline if no modules specified
    if not nodes:
        default_rag = AugLLMConfig(
            llm_config=llm_config,
            prompt_template=ChatPromptTemplate.from_messages(
                [("system", "Answer the query"), ("human", "{query}")]
            ),
            output_key="response",
        )
        nodes.append(default_rag)

    # Build chain based on routing strategy
    if config.routing_strategy == "sequential":
        return ChainAgent(*nodes, name=name)
    if config.routing_strategy == "conditional":
        # Add simple conditional routing
        return flow_with_edges(nodes, *[f"{i}->{i+1}" for i in range(len(nodes) - 1)])
    # parallel - simplified
    return ChainAgent(*nodes, name=name)


def create_simple_modular_rag(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Create a simple modular RAG with basic modules."""
    config = ModularConfig(
        modules=[
            RAGModule.QUERY_EXPANSION,
            RAGModule.DOCUMENT_FILTERING,
            RAGModule.ANSWER_GENERATION,
        ]
    )
    return create_modular_rag(documents, config, llm_config)


def create_comprehensive_modular_rag(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Create a comprehensive modular RAG with all modules."""
    config = ModularConfig(
        modules=[
            RAGModule.QUERY_EXPANSION,
            RAGModule.DOCUMENT_FILTERING,
            RAGModule.CONTEXT_RANKING,
            RAGModule.ANSWER_GENERATION,
            RAGModule.ANSWER_VERIFICATION,
            RAGModule.RESPONSE_SYNTHESIS,
        ],
        quality_gates=True,
    )
    return create_modular_rag(documents, config, llm_config)


def create_custom_modular_rag(
    documents: list[Document],
    modules: list[str],
    llm_config: LLMConfig | None = None,
) -> ChainAgent:
    """Create a custom modular RAG with specified modules."""
    config = ModularConfig(modules=[RAGModule(module) for module in modules])
    return create_modular_rag(documents, config, llm_config)
