"""Agentic RAG Router using ChainAgent.

Simplified version using the new ChainAgent approach.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.chain import ChainAgent, flow_with_edges
from haive.agents.rag.flare.agent import FLARERAGAgent
from haive.agents.rag.fusion.agent import RAGFusionAgent
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


class RAGStrategy(str, Enum):
    """Available RAG strategies."""

    SIMPLE = "simple"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"
    FUSION = "fusion"
    FLARE = "flare"


class StrategyDecision(BaseModel):
    """Strategy selection result."""

    strategy: RAGStrategy = Field(description="Selected strategy")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence")
    reasoning: str = Field(description="Why this strategy was chosen")


def create_agentic_rag_router_chain(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    name: str = "Agentic RAG Router",
) -> ChainAgent:
    """Create an agentic RAG router using ChainAgent.

    Super simple compared to the old implementation!
    """
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Strategy selector
    strategy_selector = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """Select the best RAG strategy:
            - simple: Basic queries, direct lookup
            - multi_query: Complex queries needing multiple perspectives
            - hyde: Abstract queries needing expansion
            - fusion: High-quality results through fusion
            - flare: Iterative refinement needed""",
                ),
                ("human", "Query: {query}\nSelect optimal strategy."),
            ]
        ),
        structured_output_model=StrategyDecision,
        output_key="strategy_decision",
    )

    # RAG strategy agents
    simple_rag = SimpleRAGAgent.from_documents(documents, llm_config)
    multi_rag = MultiQueryRAGAgent.from_documents(documents, llm_config)
    hyde_rag = HyDERAGAgentV2.from_documents(documents, llm_config)
    fusion_rag = RAGFusionAgent.from_documents(documents, llm_config)
    flare_rag = FLARERAGAgent.from_documents(documents, llm_config)

    # Synthesis engine
    synthesizer = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Synthesize the RAG results into a final response"),
                (
                    "human",
                    """Original query: {query}
            Selected strategy: {strategy}
            RAG response: {response}

            Create a comprehensive final response.""",
                ),
            ]
        ),
        output_key="final_response",
    )

    # Build the chain - that's it!
    chain = flow_with_edges(
        [
            strategy_selector,  # 0: Select strategy
            simple_rag,  # 1: Simple RAG
            multi_rag,  # 2: Multi-query RAG
            hyde_rag,  # 3: HyDE RAG
            fusion_rag,  # 4: Fusion RAG
            flare_rag,  # 5: FLARE RAG
            synthesizer,  # 6: Synthesize results
        ],
        # Conditional routing based on strategy
        (
            0,
            {"simple": 1, "multi_query": 2, "hyde": 3, "fusion": 4, "flare": 5},
            lambda s: s.get("strategy_decision", {}).get("strategy", "simple"),
        ),
        # All strategies flow to synthesizer
        "1->6",
        "2->6",
        "3->6",
        "4->6",
        "5->6",
    )

    chain.name = name
    return chain


# Even simpler version with just a few strategies
def create_simple_rag_router_chain(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> ChainAgent:
    """Ultra-simple RAG router with just basic routing."""
    if not llm_config:
        llm_config = AzureLLMConfig(
            deployment_name="gpt-4",
            azure_endpoint="${AZURE_OPENAI_API_BASE}",
            api_key="${AZURE_OPENAI_API_KEY}",
        )

    # Simple classifier
    classifier = AugLLMConfig(
        llm_config=llm_config,
        prompt_template=ChatPromptTemplate.from_messages(
            [
                ("system", "Classify query complexity: 'simple' or 'complex'"),
                ("human", "{query}"),
            ]
        ),
        output_key="complexity",
    )

    # Two RAG strategies
    simple_rag = SimpleRAGAgent.from_documents(documents, llm_config)
    complex_rag = MultiQueryRAGAgent.from_documents(documents, llm_config)

    # Just 3 nodes and routing - done!
    return flow_with_edges(
        [classifier, simple_rag, complex_rag],
        (0, {"simple": 1, "complex": 2}, lambda s: s.get("complexity", "simple")),
    )


# Integration with multi-agent
def create_agentic_router_multi_agent(
    documents: list[Document], llm_config: LLMConfig | None = None
) -> "ChainMultiAgent":
    """Create as a multi-agent system."""
    from haive.agents.chain.multi_integration import ChainMultiAgent

    # Create the chain
    chain = create_agentic_rag_router_chain(documents, llm_config)

    # Convert to multi-agent
    return ChainMultiAgent.from_chain(chain)


# I/O schema for compatibility
def get_agentic_router_chain_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for the chain version."""
    return {
        "inputs": ["query", "context", "messages"],
        "outputs": ["strategy_decision", "response", "final_response", "messages"],
    }
