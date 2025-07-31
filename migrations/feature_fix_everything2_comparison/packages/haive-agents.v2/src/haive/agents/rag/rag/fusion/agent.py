"""RAG Fusion Agents.

from typing import Any
Implementation of RAG Fusion with reciprocal rank fusion for enhanced retrieval.
Based on the architecture pattern from rag-architectures-flows.md.
"""

import logging
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from haive.core.models.llm.base import AzureLLMConfig, LLMConfig
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import END, START
from pydantic import BaseModel, Field

from haive.agents.base.agent import Agent
from haive.agents.multi.base import SequentialAgent
from haive.agents.rag.base.agent import BaseRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class QueryVariationsFusion(BaseModel):
    """Enhanced query variations for fusion."""

    original_query: str = Field(description="Original query")
    semantic_variations: list[str] = Field(
        description="Semantically similar variations"
    )
    syntactic_variations: list[str] = Field(
        description="Syntactically different variations"
    )
    context_variations: list[str] = Field(description="Context-specific variations")

    fusion_strategy: str = Field(description="Recommended fusion strategy")
    expected_overlap: float = Field(
        ge=0.0, le=1.0, description="Expected result overlap"
    )


class FusionResult(BaseModel):
    """Results from reciprocal rank fusion."""

    original_rankings: dict[str, list[str]] = Field(
        description="Original rankings per query"
    )
    fused_ranking: list[str] = Field(description="Final fused ranking")
    fusion_scores: dict[str, float] = Field(description="RRF scores per document")

    confidence: float = Field(ge=0.0, le=1.0, description="Confidence in fusion")
    diversity_score: float = Field(ge=0.0, le=1.0, description="Diversity of results")
    consensus_level: float = Field(
        ge=0.0, le=1.0, description="Agreement between queries"
    )


# Enhanced prompts for fusion
QUERY_EXPANSION_FUSION_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at generating diverse query variations for RAG Fusion.

Create multiple query variations that will retrieve complementary information:

1. **Semantic Variations**: Different ways to express the same meaning
2. **Syntactic Variations**: Different sentence structures and phrasings
3. **Context Variations**: Questions that provide different contextual angles

The goal is to maximize retrieval coverage while maintaining relevance.
Each variation should potentially retrieve different but relevant documents.""",
        ),
        (
            "human",
            """Generate diverse query variations for RAG Fusion:

Original Query: {query}

Create variations that will:
- Capture different aspects of the query
- Use different terminology and phrasing
- Approach the question from different angles
- Maximize retrieval diversity

Provide structured variations and fusion strategy.""",
        ),
    ]
)


FUSION_ANSWER_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert at synthesizing information from multiple retrieval results.

You have access to documents retrieved using different query variations and ranked using
Reciprocal Rank Fusion. The highest-ranked documents are the most relevant across
multiple query perspectives.

Key principles:
- Higher-ranked documents should be weighted more heavily
- Look for consensus across different query results
- Identify and resolve any contradictions
- Provide comprehensive coverage of the topic""",
        ),
        (
            "human",
            """Answer the query using the fusion-ranked documents:

Original Query: {query}
Query Variations Used: {query_variations}

Fusion-Ranked Documents (in order of relevance):
{fusion_ranked_documents}

Fusion Metadata:
- Consensus Level: {consensus_level}
- Diversity Score: {diversity_score}
- Confidence: {fusion_confidence}

Provide a comprehensive answer that leverages the multi-perspective retrieval.""",
        ),
    ]
)


class ReciprocalRankFusionAgent(Agent):
    """Agent that performs reciprocal rank fusion on multiple retrieval results."""

    name: str = "Reciprocal Rank Fusion"
    # Proper Pydantic field definitions
    k_parameter: float = Field(
        default=60.0, description="RRF k parameter (typically 60)"
    )
    min_consensus: float = Field(
        default=0.3, description="Minimum consensus required for high confidence"
    )

    def build_graph(self) -> BaseGraph:
        """Build RRF fusion graph."""
        graph = BaseGraph(name="ReciprocalRankFusion")

        def perform_rrf_fusion(state: dict[str, Any]) -> dict[str, Any]:
            """Perform reciprocal rank fusion on multiple document lists."""
            # Get multiple retrieval results
            retrieval_results = getattr(state, "retrieval_results", {})
            getattr(state, "query_variations", [])

            if not retrieval_results:
                # Try to get from individual fields
                retrieved_documents = getattr(state, "retrieved_documents", [])
                if retrieved_documents:
                    retrieval_results = {"original": retrieved_documents}

            if not retrieval_results:
                logger.warning("No retrieval results found for fusion")
                return {
                    "fusion_result": None,
                    "fused_documents": [],
                    "fusion_confidence": 0.0,
                }

            # Perform RRF
            fusion_scores = self._calculate_rrf_scores(retrieval_results)

            # Sort by RRF score
            sorted_docs = sorted(
                fusion_scores.items(), key=lambda x: x[1], reverse=True
            )

            # Build fusion result
            fusion_result = FusionResult(
                original_rankings={
                    query: [self._doc_id(doc) for doc in docs]
                    for query, docs in retrieval_results.items()
                },
                fused_ranking=[doc_id for doc_id, _ in sorted_docs],
                fusion_scores=dict(fusion_scores),
                confidence=self._calculate_confidence(retrieval_results),
                diversity_score=self._calculate_diversity(retrieval_results),
                consensus_level=self._calculate_consensus(retrieval_results),
            )

            # Extract fused documents in order
            doc_lookup = self._build_doc_lookup(retrieval_results)
            fused_documents = [
                doc_lookup[doc_id] for doc_id, _ in sorted_docs if doc_id in doc_lookup
            ]

            return {
                "fusion_result": fusion_result,
                "fused_documents": fused_documents[:10],  # Top 10
                "fusion_confidence": fusion_result.confidence,
                "diversity_score": fusion_result.diversity_score,
                "consensus_level": fusion_result.consensus_level,
                "fusion_scores": fusion_result.fusion_scores,
            }

        graph.add_node("rrf_fusion", perform_rrf_fusion)
        graph.add_edge(START, "rrf_fusion")
        graph.add_edge("rrf_fusion", END)

        return graph

    def _calculate_rrf_scores(
        self, retrieval_results: dict[str, list[Document]]
    ) -> dict[str, float]:
        """Calculate RRF scores for all documents."""
        doc_scores = {}

        for _query, docs in retrieval_results.items():
            for rank, doc in enumerate(docs):
                doc_id = self._doc_id(doc)
                rrf_score = 1.0 / (self.k_parameter + rank + 1)

                if doc_id not in doc_scores:
                    doc_scores[doc_id] = 0.0
                doc_scores[doc_id] += rrf_score

        return doc_scores

    def _doc_id(self, doc: Document) -> str:
        """Generate unique ID for document."""
        return str(hash(doc.page_content[:100]))

    def _calculate_confidence(
        self, retrieval_results: dict[str, list[Document]]
    ) -> float:
        """Calculate confidence in fusion results."""
        if len(retrieval_results) < 2:
            return 0.5

        # Calculate overlap between top results
        top_docs = {}
        for query, docs in retrieval_results.items():
            top_docs[query] = {self._doc_id(doc) for doc in docs[:5]}

        # Average pairwise overlap
        overlaps = []
        queries = list(top_docs.keys())
        for i in range(len(queries)):
            for j in range(i + 1, len(queries)):
                set1, set2 = top_docs[queries[i]], top_docs[queries[j]]
                overlap = len(set1.intersection(set2)) / max(len(set1.union(set2)), 1)
                overlaps.append(overlap)

        return sum(overlaps) / len(overlaps) if overlaps else 0.5

    def _calculate_diversity(
        self, retrieval_results: dict[str, list[Document]]
    ) -> float:
        """Calculate diversity of retrieval results."""
        all_docs = set()
        total_docs = 0

        for docs in retrieval_results.values():
            for doc in docs:
                all_docs.add(self._doc_id(doc))
                total_docs += 1

        return len(all_docs) / max(total_docs, 1) if total_docs > 0 else 0.0

    def _calculate_consensus(
        self, retrieval_results: dict[str, list[Document]]
    ) -> float:
        """Calculate consensus level across queries."""
        if len(retrieval_results) < 2:
            return 1.0

        # Documents that appear in multiple query results
        doc_counts = {}
        for docs in retrieval_results.values():
            for doc in docs:
                doc_id = self._doc_id(doc)
                doc_counts[doc_id] = doc_counts.get(doc_id, 0) + 1

        # Fraction of documents that appear in multiple results
        multi_query_docs = sum(1 for count in doc_counts.values() if count > 1)
        total_unique_docs = len(doc_counts)

        return multi_query_docs / max(total_unique_docs, 1)

    def _build_doc_lookup(
        self, retrieval_results: dict[str, list[Document]]
    ) -> dict[str, Document]:
        """Build lookup from doc ID to document."""
        lookup = {}
        for docs in retrieval_results.values():
            for doc in docs:
                lookup[self._doc_id(doc)] = doc
        return lookup


class RAGFusionAgent(SequentialAgent):
    """Complete RAG Fusion agent with query expansion and RRF."""

    @classmethod
    def from_documents(
        cls,
        documents: list[Document],
        llm_config: LLMConfig | None = None,
        embedding_model: str | None = None,
        num_variations: int = 3,
        k_parameter: float = 60.0,
        **kwargs,
    ):
        """Create RAG Fusion agent from documents.

        Args:
            documents: Documents to index
            llm_config: LLM configuration
            embedding_model: Embedding model for retrieval
            num_variations: Number of query variations to generate
            k_parameter: RRF k parameter
            **kwargs: Additional arguments

        Returns:
            RAGFusionAgent instance
        """
        if not llm_config:
            llm_config = AzureLLMConfig(
                deployment_name="gpt-4",
                azure_endpoint="${AZURE_OPENAI_API_BASE}",
                api_key="${AZURE_OPENAI_API_KEY}",
            )

        # Step 1: Query expansion
        query_expander = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=QUERY_EXPANSION_FUSION_PROMPT,
                structured_output_model=QueryVariationsFusion,
                output_key="query_variations_fusion",
            ),
            name="Fusion Query Expander",
        )

        # Step 2: Multi-query retrieval
        multi_retriever = MultiQueryRetrievalAgent(
            documents=documents,
            embedding_model=embedding_model,
            name="Multi-Query Retriever",
        )

        # Step 3: RRF fusion
        rrf_agent = ReciprocalRankFusionAgent(
            k_parameter=k_parameter, name="RRF Fusion Engine"
        )

        # Step 4: Fusion-aware answer generation with structured output
        fusion_answerer = SimpleAgent(
            engine=AugLLMConfig(
                llm_config=llm_config,
                prompt_template=FUSION_ANSWER_PROMPT,
                structured_output_model=FusionResult,
                output_key="fusion_answer_result",
            ),
            structured_output_model=FusionResult,
            name="Fusion Answer Generator",
        )

        return cls(
            agents=[query_expander, multi_retriever, rrf_agent, fusion_answerer],
            name=kwargs.get("name", "RAG Fusion Agent"),
            **kwargs,
        )


def create_multi_query_retrieval_callable(
    documents: list[Document],
    embedding_model: str | None = None,
    max_docs_per_query: int = 10,
):
    """Create a callable function for multi-query retrieval that can be used as a graph node."""

    def multi_query_retrieve(state: dict[str, Any]) -> dict[str, Any]:
        """Retrieve documents for multiple query variations using callable node pattern."""
        # Get query variations from state (should be from RAGState)
        variations_fusion = getattr(state, "query_variations_fusion", None)
        original_query = getattr(state, "query", "")

        if variations_fusion and hasattr(variations_fusion, "semantic_variations"):
            # Use structured variations from query expansion
            all_queries = [original_query]
            all_queries.extend(variations_fusion.semantic_variations)
            all_queries.extend(variations_fusion.syntactic_variations)
            all_queries.extend(variations_fusion.context_variations)
        else:
            # Fallback to original query
            all_queries = [original_query]

        # Remove duplicates and empty queries
        all_queries = list({q.strip() for q in all_queries if q.strip()})
        logger.info(
            f"Multi-query retrieval with {len(all_queries)} queries: {all_queries}"
        )

        # Create base retriever on-demand
        base_retriever = BaseRAGAgent.from_documents(
            documents=documents,
            embedding_model=embedding_model,
            name="On-Demand Base Retrievef",
        )

        # Retrieve for each query
        retrieval_results = {}

        for i, query in enumerate(all_queries):
            try:
                logger.debug(f"Retrieving for query {i}: {query}")
                result = base_retriever.run({"query": query})
                docs = []

                if hasattr(result, "retrieved_documents"):
                    docs = result.retrieved_documents
                elif isinstance(result, dict) and "retrieved_documents" in result:
                    docs = result["retrieved_documents"]

                # Limit docs per query
                docs = docs[:max_docs_per_query]
                retrieval_results[f"query_{i}"] = docs
                logger.debug(f"Retrieved {len(docs)} documents for query {i}")

            except Exception as e:
                logger.warning(f"Retrieval failed for query '{query}': {e}")
                retrieval_results[f"query_{i}"] = []

        # Combine all documents for backward compatibility
        all_retrieved_docs = []
        for docs in retrieval_results.values():
            all_retrieved_docs.extend(docs)

        logger.info(
            f"Total retrieved: {len(all_retrieved_docs)} documents across {len(all_queries)} queries"
        )

        return {
            "retrieval_results": retrieval_results,
            "retrieved_documents": all_retrieved_docs,
            "query_variations_used": all_queries,
            "num_query_variations": len(all_queries),
            "total_retrieved": len(all_retrieved_docs),
        }

    return multi_query_retrieve


class MultiQueryRetrievalAgent(Agent):
    """Agent that uses a callable node for multi-query retrieval - proper Pydantic approach."""

    name: str = "Multi-Query Retrieval"
    # Define Pydantic fields properly
    documents: list[Document] = Field(description="Documents for retrieval")
    embedding_model: str | None = Field(default=None, description="Embedding model")
    max_docs_per_query: int = Field(default=10, description="Max docs per query")

    def build_graph(self) -> BaseGraph:
        """Build multi-query retrieval graph with callable node using Pydantic fields."""
        graph = BaseGraph(name="MultiQueryRetrieval")

        # Create callable function using the Pydantic fields
        multi_query_retrieve = create_multi_query_retrieval_callable(
            documents=self.documents,
            embedding_model=self.embedding_model,
            max_docs_per_query=self.max_docs_per_query,
        )

        # Add callable node to graph
        graph.add_node("multi_retrieve", multi_query_retrieve)
        graph.add_edge(START, "multi_retrieve")
        graph.add_edge("multi_retrieve", END)

        return graph


# Factory function for easy creation
def create_rag_fusion_agent(
    documents: list[Document],
    llm_config: LLMConfig | None = None,
    fusion_type: str = "standard",
    **kwargs,
) -> RAGFusionAgent:
    """Create a RAG Fusion agent.

    Args:
        documents: Documents for retrieval
        llm_config: LLM configuration
        fusion_type: Type of fusion ("standard", "aggressive", "conservative")
        **kwargs: Additional arguments

    Returns:
        Configured RAG Fusion agent
    """
    # Adjust parameters based on fusion type
    if fusion_type == "aggressive":
        kwargs.setdefault("num_variations", 5)
        kwargs.setdefault("k_parameter", 30.0)
    elif fusion_type == "conservative":
        kwargs.setdefault("num_variations", 2)
        kwargs.setdefault("k_parameter", 90.0)
    else:  # standard
        kwargs.setdefault("num_variations", 3)
        kwargs.setdefault("k_parameter", 60.0)

    return RAGFusionAgent.from_documents(
        documents=documents, llm_config=llm_config, **kwargs
    )


# I/O schema for compatibility
def get_rag_fusion_io_schema() -> dict[str, list[str]]:
    """Get I/O schema for RAG Fusion agents."""
    return {
        "inputs": ["query", "messages"],
        "outputs": [
            "query_variations_fusion",
            "retrieval_results",
            "retrieved_documents",
            "fusion_result",
            "fused_documents",
            "fusion_confidence",
            "diversity_score",
            "consensus_level",
            "fusion_scores",
            "response",
            "messages",
        ],
    }
