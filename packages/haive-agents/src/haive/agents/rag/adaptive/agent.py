"""Adaptive RAG Agent

Dynamic strategy selection based on query complexity.
Routes queries to appropriate RAG strategies.
"""

from typing import Any, Dict, List, Literal, Optional

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.models.llm.base import LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

from haive.agents.multi.base import ConditionalAgent
from haive.agents.rag.hyde.agent_v2 import HyDERAGAgentV2
from haive.agents.rag.multi_query.agent import MultiQueryRAGAgent
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent


class QueryAnalysis(BaseModel):
    """Analysis of query characteristics."""

    complexity: Literal["simple", "medium", "complex", "known"] = Field(
        description="Query complexity level"
    )
    topics: List[str] = Field(description="Main topics in the query")
    requires_multi_hop: bool = Field(
        description="Whether query requires multiple reasoning steps"
    )
    temporal_sensitivity: bool = Field(
        description="Whether query is about current/recent events"
    )
    domain_specific: bool = Field(
        description="Whether query requires specialized knowledge"
    )
    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in the analysis")


QUERY_ANALYZER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert query analyzer for RAG systems.
Analyze queries to determine the best retrieval strategy.

Complexity levels:
- simple: Direct factual questions, single concept lookups
- medium: Questions requiring some context or multiple facts
- complex: Multi-hop reasoning, synthesis across topics
- known: Common knowledge that might not need retrieval

Consider:
- Number of concepts involved
- Need for reasoning vs. direct lookup
- Temporal aspects (current events vs. historical)
- Domain specificity""",
        ),
        (
            "human",
            """Analyze this query and determine its characteristics:

Query: {query}

Provide a structured analysis.""",
        ),
    ]
)


DIRECT_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a knowledgeable assistant. Answer common questions directly.",
        ),
        ("human", "Answer this question based on general knowledge: {query}"),
    ]
)


class AdaptiveRAGAgent(ConditionalAgent):
    """Adaptive RAG that routes queries based on complexity."""

    @classmethod
    def from_documents(
        cls,
        documents: List[Document],
        llm_config: Optional[LLMConfig] = None,
        embedding_model: Optional[str] = None,
        **kwargs
    ):
        """Create Adaptive RAG from documents.

        Args:
            documents: Documents to index
            llm_config: Optional LLM configuration
            embedding_model: Optional embedding model
            **kwargs: Additional arguments

        Returns:
            AdaptiveRAGAgent instance
        """
        # Query analyzer
        query_analyzer = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=QUERY_ANALYZER_PROMPT,
                structured_output_model=QueryAnalysis,
                output_key="query_analysis",
            ),
            name="Query Analyzer",
        )

        # Direct answer agent (for known/simple queries)
        direct_agent = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config, prompt_template=DIRECT_ANSWER_PROMPT
            ),
            name="Direct Answer",
        )

        # Simple RAG for basic queries
        simple_rag = SimpleRAGAgent.from_documents(
            documents=documents, llm_config=llm_config
        )
        simple_rag.name = "Simple RAG"

        # Multi-Query RAG for medium complexity
        multi_rag = MultiQueryRAGAgent.from_documents(
            documents=documents, llm_config=llm_config, embedding_model=embedding_model
        )
        multi_rag.name = "Multi-Query RAG"

        # HyDE RAG for complex/abstract queries
        hyde_rag = HyDERAGAgentV2.from_documents(
            documents=documents, llm_config=llm_config, embedding_model=embedding_model
        )
        hyde_rag.name = "HyDE RAG"

        # Routing function based on query analysis
        def route_query(state: Dict[str, Any]) -> str:
            """Route based on query complexity analysis."""
            analysis = state.get("query_analysis", {})

            if isinstance(analysis, QueryAnalysis):
                complexity = analysis.complexity
                confidence = analysis.confidence
            elif isinstance(analysis, dict):
                complexity = analysis.get("complexity", "simple")
                confidence = analysis.get("confidence", 0.5)
            else:
                # Default to simple if no analysis
                return "simple_rag"

            # Route based on complexity
            if complexity == "known" and confidence > 0.8:
                return "direct"
            elif complexity == "simple":
                return "simple_rag"
            elif complexity == "medium":
                return "multi_rag"
            elif complexity == "complex":
                return "hyde_rag"
            else:
                # Default to multi-query for unknown
                return "multi_rag"

        # Define routing branches
        branches = {
            "analyzer": {
                "condition": route_query,
                "mapping": {
                    "direct": "direct",
                    "simple_rag": "simple_rag",
                    "multi_rag": "multi_rag",
                    "hyde_rag": "hyde_rag",
                },
            }
        }

        return cls(
            agents=[query_analyzer, direct_agent, simple_rag, multi_rag, hyde_rag],
            branches=branches,
            name=kwargs.get("name", "Adaptive RAG Agent"),
            **kwargs
        )
