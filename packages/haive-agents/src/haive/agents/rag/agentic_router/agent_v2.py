"""Agentic RAG Router with Proper Conditional Routing.

Implementation using conditional edges for routing between strategies.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.rag.flare.agent import FLARERAGAgent
from haive.agents.rag.fusion.agent import RAGFusionAgent
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class RAGStrategy(str, Enum):
    """Available RAG strategies for routing."""

    SIMPLE = "simple"
    MULTI_QUERY = "multi_query"
    HYDE = "hyde"
    FUSION = "fusion"
    FLARE = "flare"


class StrategyDecision(BaseModel):
    """Strategy selection decision."""

    strategy: RAGStrategy = Field(description="Selected strategy")
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in selection")
    reasoning: str = Field(description="Reasoning for selection")


STRATEGY_SELECTION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """Select the best RAG strategy for the query:
    - simple: Basic queries needing direct retrieval
    - multi_query: Complex queries benefiting from multiple perspectives
    - hyde: Abstract queries needing hypothetical expansion
    - fusion: High-quality results through rank fusion
    - flare: Iterative refinement needed""",
        ),
        ("human", "Query: {query}\n\nSelect the optimal strategy."),
    ]
)


class AgenticRAGRouterV2(Agent):
    """Agentic RAG Router using proper conditional routing."""

    name: str = "Agentic RAG Router V2"
    documents: list[Document] = Field(description="Documents for RAG")
    llm_config: LLMConfig = Field(description="LLM configuration")

    def build_graph(self) -> BaseGraph:
        """Build graph with conditional routing between strategies."""
        graph = BaseGraph(name="AgenticRAGRouter")

        # Strategy selector node
        strategy_selector = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=self.llm_config,
                prompt_template=STRATEGY_SELECTION_PROMPT,
                structured_output_model=StrategyDecision,
                output_key="strategy_decision",
            ),
            name="StrategySelector",
        )

        # Create strategy agents
        simple_rag = SimpleRAGAgent.from_documents(
            documents=self.documents, llm_config=self.llm_config, name="SimpleRAG"
        )

        multi_query_rag = MultiQueryRAGAgent.from_documents(
            documents=self.documents, llm_config=self.llm_config, name="MultiQueryRAG"
        )

        hyde_rag = HyDERAGAgentV2.from_documents(
            documents=self.documents, llm_config=self.llm_config, name="HyDERAG"
        )

        fusion_rag = RAGFusionAgent.from_documents(
            documents=self.documents, llm_config=self.llm_config, name="FusionRAG"
        )

        flare_rag = FLARERAGAgent.from_documents(
            documents=self.documents, llm_config=self.llm_config, name="FLARERAG"
        )

        # Add nodes
        graph.add_node("select_strategy", strategy_selector)
        graph.add_node("simple_rag", simple_rag)
        graph.add_node("multi_query_rag", multi_query_rag)
        graph.add_node("hyde_rag", hyde_rag)
        graph.add_node("fusion_rag", fusion_rag)
        graph.add_node("flare_rag", flare_rag)

        # Routing function
        def route_to_strategy(state: dict[str, Any]) -> str:
            """Route to appropriate RAG strategy based on selection."""
            strategy_decision = state.get("strategy_decision", {})
            strategy = strategy_decision.get("strategy", RAGStrategy.SIMPLE)

            routing_map = {
                RAGStrategy.SIMPLE: "simple_rag",
                RAGStrategy.MULTI_QUERY: "multi_query_rag",
                RAGStrategy.HYDE: "hyde_rag",
                RAGStrategy.FUSION: "fusion_rag",
                RAGStrategy.FLARE: "flare_rag",
            }

            return routing_map.get(strategy, "simple_rag")

        # Add edges
        graph.add_edge(START, "select_strategy")

        # Conditional routing from strategy selector
        graph.add_conditional_edges(
            "select_strategy",
            route_to_strategy,
            {
                "simple_rag": "simple_rag",
                "multi_query_rag": "multi_query_rag",
                "hyde_rag": "hyde_rag",
                "fusion_rag": "fusion_rag",
                "flare_rag": "flare_rag",
            },
        )

        # All strategies go to END
        graph.add_edge("simple_rag", END)
        graph.add_edge("multi_query_rag", END)
        graph.add_edge("hyde_rag", END)
        graph.add_edge("fusion_rag", END)
        graph.add_edge("flare_rag", END)

        return graph
