"""Unified RAG Factory.

Create any RAG agent using either traditional or ChainAgent approach.
Integrates with multi-agent system.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document

from haive.agents.base.agent import Agent
from haive.agents.chain import ChainAgent

logger = logging.getLogger(__name__)


class RAGType(str, Enum):
    """Available RAG types."""

    SIMPLE = "simple"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"
    FUSION = "fusion"
    FLARE = "flare"
    SPECULATIVE = "speculative"
    MEMORY_AWARE = "memory_aware"
    STEP_BACK = "step_back"
    SELF_ROUTE = "self_route"
    ADAPTIVE_TOOLS = "adaptive_tools"
    AGENTIC_ROUTER = "agentic_router"
    QUERY_PLANNING = "query_planning"
    SELF_REFLECTIVE = "self_reflective"
    CORRECTIVE = "corrective"


class RAGStyle(str, Enum):
    """Implementation style."""

    TRADITIONAL = "traditional"  # Original implementation
    CHAIN = "chain"  # ChainAgent implementation
    MULTI = "multi"  # MultiAgent implementation


class RAGFactory:
    """Unified factory for creating RAG agents."""

    @staticmethod
    def create(
        rag_type: RAGType,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        style: RAGStyle = RAGStyle.CHAIN,
        name: str | None = None,
        **kwargs,
    ) -> Agent | ChainAgent:
        """Create any RAG agent.

        Args:
            rag_type: Type of RAG to create
            documents: Documents for retrieval
            llm_config: LLM configuration
            style: Implementation style
            name: Agent name
            **kwargs: Additional arguments

        Returns:
            The created RAG agent
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        agent_name = name or f"{rag_type.title()} RAG"

        # Route to appropriate implementation
        if style == RAGStyle.CHAIN:
            return RAGFactory._create_chain(
                rag_type, documents, llm_config, agent_name, **kwargs
            )
        if style == RAGStyle.MULTI:
            return RAGFactory._create_multi(
                rag_type, documents, llm_config, agent_name, **kwargs
            )
        # TRADITIONAL
        return RAGFactory._create_traditional(
            rag_type, documents, llm_config, agent_name, **kwargs
        )

    @staticmethod
    def _create_chain(
        rag_type: RAGType,
        documents: list[Document],
        llm_config: LLMConfig,
        name: str,
        **kwargs,
    ) -> ChainAgent:
        """Create ChainAgent implementation."""
        if rag_type == RAGType.AGENTIC_ROUTER:
            from haive.agents.rag.agentic_router.agent_chain import (
                create_agentic_rag_router_chain,
            )

            return create_agentic_rag_router_chain(documents, llm_config, name)

        if rag_type == RAGType.QUERY_PLANNING:
            from haive.agents.rag.query_planning.agent_chain import (
                create_query_planning_chain,
            )

            return create_query_planning_chain(documents, llm_config, name)

        if rag_type == RAGType.SIMPLE:
            from haive.agents.chain import flow
            from haive.agents.rag.simple.agent import SimpleRAGAgent

            agent = SimpleRAGAgent.from_documents(documents, llm_config)
            return flow(agent, name=name)

        if rag_type == RAGType.FUSION:
            from haive.agents.chain import flow
            from haive.agents.rag.fusion.agent import RAGFusionAgent

            agent = RAGFusionAgent.from_documents(documents, llm_config)
            return flow(agent, name=name)

        # Fallback to traditional and wrap in chain
        traditional = RAGFactory._create_traditional(
            rag_type, documents, llm_config, name, **kwargs
        )
        from haive.agents.chain import flow

        return flow(traditional, name=name)

    @staticmethod
    def _create_multi(
        rag_type: RAGType,
        documents: list[Document],
        llm_config: LLMConfig,
        name: str,
        **kwargs,
    ) -> "ChainMultiAgent":
        """Create MultiAgent implementation."""
        from haive.agents.chain.multi_integration import ChainMultiAgent

        # Create chain version first
        chain = RAGFactory._create_chain(
            rag_type, documents, llm_config, name, **kwargs
        )

        # Convert to multi-agent
        return ChainMultiAgent.from_chain(chain, name=name)

    @staticmethod
    def _create_traditional(
        rag_type: RAGType,
        documents: list[Document],
        llm_config: LLMConfig,
        name: str,
        **kwargs,
    ) -> Agent:
        """Create traditional implementation."""
        # Remove name from kwargs to avoid conflicts
        filtered_kwargs = {k: v for k, v in kwargs.items() if k != "name"}

        if rag_type == RAGType.SIMPLE:
            from haive.agents.rag.simple.agent import SimpleRAGAgent

            return SimpleRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        if rag_type == RAGType.MULTI_QUERY:
            from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent

            return MultiQueryRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        if rag_type == RAGType.HYDE:
            from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2

            return HyDERAGAgentV2.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        if rag_type == RAGType.FUSION:
            from haive.agents.rag.fusion.agent import RAGFusionAgent

            return RAGFusionAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        if rag_type == RAGType.FLARE:
            from haive.agents.rag.flare.agent import FLARERAGAgent

            return FLARERAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        if rag_type == RAGType.SPECULATIVE:
            from haive.agents.rag.speculative.agent import SpeculativeRAGAgent

            return SpeculativeRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        elif rag_type == RAGType.MEMORY_AWARE:
            from haive.agents.rag.memory_aware.agent import MemoryAwareRAGAgent

            return MemoryAwareRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        elif rag_type == RAGType.STEP_BACK:
            from haive.agents.rag.step_back.agent import StepBackRAGAgent

            return StepBackRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        elif rag_type == RAGType.SELF_ROUTE:
            from haive.agents.rag.self_route.agent import SelfRouteRAGAgent

            return SelfRouteRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        elif rag_type == RAGType.ADAPTIVE_TOOLS:
            from haive.agents.rag.adaptive_tools.agent import AdaptiveToolsRAGAgent

            return AdaptiveToolsRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        elif rag_type == RAGType.CORRECTIVE:
            from haive.agents.rag.corrective.agent import CorrectiveRAGAgent

            return CorrectiveRAGAgent.from_documents(
                documents, llm_config, name=name, **filtered_kwargs
            )

        else:
            raise ValueError(f"Unknown RAG type: {rag_type}")


# Convenience functions
def create_rag(
    rag_type: str | RAGType,
    documents: list[Document],
    style: str | RAGStyle = "chain",
    **kwargs,
) -> Agent | ChainAgent:
    """Simple function to create any RAG agent."""
    if isinstance(rag_type, str):
        rag_type = RAGType(rag_type)
    if isinstance(style, str):
        style = RAGStyle(style)

    return RAGFactory.create(rag_type, documents, style=style, **kwargs)


def create_rag_chain(
    rag_type: str | RAGType, documents: list[Document], **kwargs
) -> ChainAgent:
    """Create a RAG agent as a ChainAgent."""
    return create_rag(rag_type, documents, style="chain", **kwargs)


def create_rag_multi(rag_type: str | RAGType, documents: list[Document], **kwargs):
    """Create a RAG agent as a MultiAgent."""
    return create_rag(rag_type, documents, style="multi", **kwargs)


def create_rag_pipeline(
    rag_types: list[str | RAGType],
    documents: list[Document],
    style: RAGStyle = RAGStyle.CHAIN,
    **kwargs,
) -> ChainAgent:
    """Create a pipeline of RAG agents."""
    agents = []
    for rag_type in rag_types:
        agent = create_rag(rag_type, documents, style=style, **kwargs)
        agents.append(agent)

    return ChainAgent(*agents, name="RAG Pipeline")


# Examples of easy usage
def example_usage():
    """Examples of how to use the unified factory."""
    docs = [Document(page_content="Test document")]

    # Simple creation
    simple_rag = create_rag("simple", docs)

    # Chain version
    router_chain = create_rag_chain("agentic_router", docs)

    # Multi-agent version
    planning_multi = create_rag_multi("query_planning", docs)

    # Pipeline of multiple RAG types
    pipeline = create_rag_pipeline(["simple", "fusion", "flare"], docs, style="chain")

    # Traditional implementation
    traditional = create_rag("hyde", docs, style="traditional")

    return {
        "simple": simple_rag,
        "router_chain": router_chain,
        "planning_multi": planning_multi,
        "pipeline": pipeline,
        "traditional": traditional,
    }
