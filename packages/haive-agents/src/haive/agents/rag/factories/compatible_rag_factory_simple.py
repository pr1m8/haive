"""Simplified Compatible RAG Factory

Simplified version without legacy functions that have import issues.
"""

import logging
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Type, Union

from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document

from haive.agents.multi.base import ConditionalAgent, ParallelAgent, SequentialAgent
from haive.agents.rag.adaptive.agent import AdaptiveRAGAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.corrective.agent_v2 import CorrectiveRAGAgentV2

# from haive.agents.rag.document_grading.agent import DocumentGradingAgent  # Temporarily disabled - missing callable_node
from haive.agents.rag.hallucination_grading.agent import (
    AdvancedHallucinationGraderAgent,
    HallucinationGraderAgent,
    RealtimeHallucinationGraderAgent,
    create_hallucination_grader,
)
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.query_decomposition.agent import (
    AdaptiveQueryDecomposerAgent,
    ContextualQueryDecomposerAgent,
    HierarchicalQueryDecomposerAgent,
    QueryDecomposerAgent,
    create_query_decomposer,
)
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class RAGComponent(Enum):
    """Available RAG component types for plug-and-play composition."""

    # Core retrieval
    SIMPLE_RETRIEVAL = "simple_retrieval"
    HYDE_RETRIEVAL = "hyde_retrieval"
    MULTI_QUERY_RETRIEVAL = "multi_query_retrieval"

    # Document processing
    DOCUMENT_GRADING = "document_grading"
    COMPREHENSIVE_GRADING = "comprehensive_grading"

    # Query processing
    QUERY_DECOMPOSITION = "query_decomposition"
    HIERARCHICAL_DECOMPOSITION = "hierarchical_decomposition"
    CONTEXTUAL_DECOMPOSITION = "contextual_decomposition"
    ADAPTIVE_DECOMPOSITION = "adaptive_decomposition"

    # Quality control
    HALLUCINATION_GRADING = "hallucination_grading"
    ADVANCED_HALLUCINATION_GRADING = "advanced_hallucination_grading"
    REALTIME_HALLUCINATION_GRADING = "realtime_hallucination_grading"

    # Answer generation
    SIMPLE_GENERATION = "simple_generation"
    CORRECTIVE_GENERATION = "corrective_generation"
    FUSION_GENERATION = "fusion_generation"


class WorkflowPattern(Enum):
    """Pre-defined workflow patterns."""

    SIMPLE = "simple"
    GRADED_HYDE = "graded_hyde"
    DECOMPOSED_GRADED = "decomposed_graded"
    FULL_PIPELINE = "full_pipeline"
    MODULAR_RAG = "modular_rag"


class CompatibleRAGFactory:
    """Factory for building RAG workflows with I/O schema compatibility."""

    def __init__(
        self,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        name: str = "Compatible RAG Workflow",
    ):
        """Initialize factory with documents and configuration."""
        self.documents = documents
        self.llm_config = llm_config or AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )
        self.name = name

    @classmethod
    def create_simple_workflow(
        cls, documents: List[Document], llm_config: Optional[LLMConfig] = None, **kwargs
    ) -> SequentialAgent:
        """Create simple RAG workflow."""
        return SimpleRAGAgent.from_documents(
            documents=documents, llm_config=llm_config, **kwargs
        )

    @classmethod
    def create_graded_hyde_workflow(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        enable_search_tools: bool = False,
        **kwargs,
    ) -> SequentialAgent:
        """Create workflow with HyDE and document grading."""
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Create components
        hyde_agent = HyDERAGAgentV2.from_documents(
            documents=documents, llm_config=llm_config, name="HyDE RAG"
        )

        # grading_agent = DocumentGradingAgent(  # Temporarily disabled - missing callable_node
        #     documents=documents, llm_config=llm_config, name="Document Grader"
        # )
        grading_agent = None  # Placeholder until DocumentGradingAgent is fixed

        corrective_agent = CorrectiveRAGAgentV2.from_documents(
            documents=documents, llm_config=llm_config, name="Corrective RAG"
        )

        return SequentialAgent(
            agents=[hyde_agent, grading_agent, corrective_agent],
            name="Graded HyDE Workflow",
            **kwargs,
        )


def create_plug_and_play_component(
    component_type: RAGComponent,
    documents: List[Document],
    llm_config: Optional[LLMConfig] = None,
    **kwargs,
) -> Union[SimpleAgent, BaseRAGAgent]:
    """Create any RAG component as a standalone agent."""

    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Query decomposition components
    if component_type == RAGComponent.QUERY_DECOMPOSITION:
        return QueryDecomposerAgent(llm_config=llm_config, **kwargs)
    elif component_type == RAGComponent.HIERARCHICAL_DECOMPOSITION:
        return HierarchicalQueryDecomposerAgent(llm_config=llm_config, **kwargs)
    elif component_type == RAGComponent.CONTEXTUAL_DECOMPOSITION:
        return ContextualQueryDecomposerAgent(llm_config=llm_config, **kwargs)
    elif component_type == RAGComponent.ADAPTIVE_DECOMPOSITION:
        return AdaptiveQueryDecomposerAgent(llm_config=llm_config, **kwargs)

    # Hallucination grading components
    elif component_type == RAGComponent.HALLUCINATION_GRADING:
        return HallucinationGraderAgent(llm_config=llm_config, **kwargs)
    elif component_type == RAGComponent.ADVANCED_HALLUCINATION_GRADING:
        return AdvancedHallucinationGraderAgent(llm_config=llm_config, **kwargs)
    elif component_type == RAGComponent.REALTIME_HALLUCINATION_GRADING:
        return RealtimeHallucinationGraderAgent(llm_config=llm_config, **kwargs)

    # Document processing components
    elif component_type == RAGComponent.DOCUMENT_GRADING:
        # return DocumentGradingAgent(  # Temporarily disabled - missing callable_node
        #     documents=documents, llm_config=llm_config, **kwargs
        # )
        raise NotImplementedError(
            "DocumentGradingAgent temporarily disabled due to missing dependencies"
        )

    # Retrieval components
    elif component_type == RAGComponent.SIMPLE_RETRIEVAL:
        return BaseRAGAgent.from_documents(
            documents=documents, llm_config=llm_config, **kwargs
        )
    elif component_type == RAGComponent.HYDE_RETRIEVAL:
        return HyDERAGAgentV2.from_documents(
            documents=documents, llm_config=llm_config, **kwargs
        )
    elif component_type == RAGComponent.MULTI_QUERY_RETRIEVAL:
        return MultiQueryRAGAgent.from_documents(
            documents=documents, llm_config=llm_config, **kwargs
        )

    else:
        raise ValueError(f"Unknown component type: {component_type}")


def get_component_compatibility_info(
    component_type: RAGComponent,
) -> Dict[str, List[str]]:
    """Get I/O schema information for a component type."""

    # Simplified I/O schemas for compatibility checking
    schemas = {
        RAGComponent.QUERY_DECOMPOSITION: {
            "inputs": ["query", "messages"],
            "outputs": ["sub_queries", "decomposition_result", "messages"],
        },
        RAGComponent.HALLUCINATION_GRADING: {
            "inputs": ["query", "response", "retrieved_documents", "messages"],
            "outputs": ["hallucination_result", "hallucination_score", "messages"],
        },
        RAGComponent.DOCUMENT_GRADING: {
            "inputs": ["query", "retrieved_documents", "messages"],
            "outputs": ["graded_documents", "relevant_documents", "messages"],
        },
        RAGComponent.SIMPLE_RETRIEVAL: {
            "inputs": ["query", "messages"],
            "outputs": ["retrieved_documents", "messages"],
        },
    }

    return schemas.get(component_type, {"inputs": ["query"], "outputs": ["response"]})
