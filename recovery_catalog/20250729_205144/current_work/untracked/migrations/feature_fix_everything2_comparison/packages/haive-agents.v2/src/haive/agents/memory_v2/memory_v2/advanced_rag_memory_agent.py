"""Advanced RAG Memory Agent with multi-stage retrieval and reranking.

This implementation provides state-of-the-art RAG capabilities:
1. Multi-stage retrieval: dense → sparse → reranking
2. Hybrid search combining vector, key, and graph
3. Query decomposition for complex questions
4. Memory-augmented generation with citations
5. Adaptive retrieval based on query complexity
"""

import asyncio
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from langchain.retrievers import EnsembleRetriever
from langchain.retrievers.contextual_compression import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import (
    CrossEncoderReranker,
    LLMChainExtractor,
)
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.cross_encoders import HuggingFaceCrossEncoder
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import FAISS, Chroma
from langchain_core.documents import Document

from haive.agents.memory_v2.time_weighted_retriever import TimeWeightedRetriever
from haive.agents.rag.simple.agent import SimpleRAGAgent
from haive.agents.simple.agent import SimpleAgent

logger = logging.getLogger(__name__)


class RetrievalStrategy(str, Enum):
    """Different retrieval strategies available."""

    DENSE_ONLY = "dense_only"  # Vector similarity only
    SPARSE_ONLY = "sparse_only"  # BM25 key only
    HYBRID = "hybrid"  # Dense + sparse ensemble
    MULTI_QUERY = "multi_query"  # Query decomposition
    CONTEXTUAL = "contextual"  # With compression
    RERANKED = "reranked"  # With cross-encoder reranking
    ADAPTIVE = "adaptive"  # System chooses best strategy


class QueryComplexity(str, Enum):
    """Query complexity levels."""

    SIMPLE = "simple"  # Single entity or fact
    MEDIUM = "medium"  # Multiple entities or relationships
    COMPLEX = "complex"  # Multi-hop reasoning required


@dataclass
class AdvancedRAGConfig:
    """Configuration for Advanced RAG Memory Agent."""

    # Basic settings
    user_id: str = "default_user"
    memory_store_path: str | None = None
    llm_config: AugLLMConfig | None = None

    # Retrieval settings
    strategy: RetrievalStrategy = RetrievalStrategy.ADAPTIVE
    k_initial: int = 20  # Initial retrieval count
    k_final: int = 5  # Final results after reranking

    # Dense retrieval
    embedding_model: str = "openai"
    vector_store_type: str = "faiss"  # faiss, chroma

    # Sparse retrieval
    enable_bm25: bool = True
    bm25_k1: float = 1.2
    bm25_b: float = 0.75

    # Ensemble weights
    dense_weight: float = 0.6
    sparse_weight: float = 0.4

    # Reranking
    enable_reranking: bool = True
    reranker_model: str = "BAAI/bge-reranker-large"
    rerank_top_k: int = 10

    # Query processing
    enable_query_expansion: bool = True
    max_query_variations: int = 3

    # Memory-specific
    enable_time_weighting: bool = True
    importance_boost: float = 1.2
    recency_decay: float = 0.01

    # Generation
    include_citations: bool = True
    citation_format: str = "[{doc_id}]"
    max_context_length: int = 4000

    def __post_init__(self):
        if self.llm_config is None:
            self.llm_config = AugLLMConfig(temperature=0.7)


class AdvancedRAGMemoryAgent:
    """Advanced RAG Memory Agent with multi-stage retrieval.

    This agent implements state-of-the-art retrieval-augmented generation
    with sophisticated memory management capabilities.
    """

    def __init__(self, config: AdvancedRAGConfig):
        self.config = config
        self.logger = logger

        # Initialize storage
        self.documents: list[Document] = []
        self.document_metadata: dict[str, dict[str, Any]] = {}

        # Initialize retrievers
        self._init_vector_store()
        self._init_retrievers()

        # Initialize generation components
        self._init_generation_components()

        # Memory for query analysis
        self.query_history: list[dict[str, Any]] = []

    def _init_vector_store(self):
        """Initialize vector store for dense retrieval."""
        embeddings = OpenAIEmbeddings()

        if self.config.memory_store_path:
            try:
                if self.config.vector_store_type == "faiss":
                    self.vector_store = FAISS.load_local(
                        self.config.memory_store_path,
                        embeddings,
                        allow_dangerous_deserialization=True,
                    )
                elif self.config.vector_store_type == "chroma":
                    self.vector_store = Chroma(
                        persist_directory=self.config.memory_store_path,
                        embedding_function=embeddings,
                    )
                self.logger.info(
                    f"Loaded existing vector store from {
                        self.config.memory_store_path}"
                )
            except Exception as e:
                self.logger.warning(
                    f"Could not load existing store: {e}, creating new one"
                )
                self._create_new_vector_store(embeddings)
        else:
            self._create_new_vector_store(embeddings)

    def _create_new_vector_store(self, embeddings):
        """Create new vector store."""
        # Create with initial dummy document
        initial_doc = Document(
            page_content="Initial memory system setup",
            metadata={
                "timestamp": datetime.now().isoformat(),
                "user_id": self.config.user_id,
                "doc_id": "init_0",
                "importance": "low",
            },
        )

        if self.config.vector_store_type == "faiss":
            self.vector_store = FAISS.from_documents([initial_doc], embeddings)
        elif self.config.vector_store_type == "chroma":
            self.vector_store = Chroma.from_documents([initial_doc], embeddings)

        self.documents = [initial_doc]

    def _init_retrievers(self):
        """Initialize all retrieval components."""
        # Dense retriever (vector similarity)
        self.dense_retriever = self.vector_store.as_retriever(
            search_kwargs={"k": self.config.k_initial}
        )

        # Time-weighted dense retriever
        if self.config.enable_time_weighting:
            self.time_weighted_retriever = TimeWeightedRetriever(
                vectorstore=self.vector_store,
                decay_rate=self.config.recency_decay,
                k=self.config.k_initial,
            )

        # Sparse retriever (BM25)
        if self.config.enable_bm25 and self.documents:
            try:
                self.sparse_retriever = BM25Retriever.from_documents(
                    self.documents, k=self.config.k_initial
                )
                self.sparse_retriever.k = self.config.k_initial
            except Exception as e:
                self.logger.warning(f"Could not initialize BM25: {e}")
                self.sparse_retriever = None
        else:
            self.sparse_retriever = None

        # Ensemble retriever (hybrid)
        if self.sparse_retriever:
            self.ensemble_retriever = EnsembleRetriever(
                retrievers=[self.dense_retriever, self.sparse_retriever],
                weights=[self.config.dense_weight, self.config.sparse_weight],
            )
        else:
            self.ensemble_retriever = self.dense_retriever

        # Multi-query retriever
        if self.config.enable_query_expansion:
            llm = self.config.llm_config.instantiate()
            self.multi_query_retriever = MultiQueryRetriever.from_llm(
                retriever=self.ensemble_retriever, llm=llm
            )

        # Contextual compression retriever
        self._init_contextual_retriever()

        # Reranking retriever
        self._init_reranking_retriever()

    def _init_contextual_retriever(self):
        """Initialize contextual compression retriever."""
        try:
            llm = self.config.llm_config.instantiate()
            compressor = LLMChainExtractor.from_llm(llm)

            self.contextual_retriever = ContextualCompressionRetriever(
                base_compressor=compressor, base_retriever=self.ensemble_retriever
            )
        except Exception as e:
            self.logger.warning(f"Could not initialize contextual retriever: {e}")
            self.contextual_retriever = self.ensemble_retriever

    def _init_reranking_retriever(self):
        """Initialize reranking retriever."""
        if not self.config.enable_reranking:
            self.reranking_retriever = self.ensemble_retriever
            return

        try:
            # Initialize cross-encoder for reranking
            cross_encoder = HuggingFaceCrossEncoder(
                model_name=self.config.reranker_model
            )
            reranker = CrossEncoderReranker(
                model=cross_encoder, top_k=self.config.rerank_top_k
            )

            self.reranking_retriever = ContextualCompressionRetriever(
                base_compressor=reranker, base_retriever=self.ensemble_retriever
            )
        except Exception as e:
            self.logger.warning(f"Could not initialize reranking: {e}")
            self.reranking_retriever = self.ensemble_retriever

    def _init_generation_components(self):
        """Initialize components for generation."""
        # Memory-enhanced agent
        try:
            self.memory_agent = SimpleRAGAgent.from_retriever(
                retriever=self.reranking_retriever,
                llm=self.config.llm_config.instantiate(),
                name="advanced_rag_memory",
            )
        except Exception as e:
            # Fallback to basic agent
            self.logger.warning(f"Could not create SimpleRAGAgent: {e}")
            self.memory_agent = SimpleAgent(
                name="fallback_memory_agent", engine=self.config.llm_config
            )

        # Citation generator
        self.citation_agent = SimpleAgent(
            name="citation_generator", engine=self.config.llm_config
        )

    def analyze_query_complexity(self, query: str) -> QueryComplexity:
        """Analyze query complexity to choose optimal strategy."""
        query_lower = query.lower()

        # Count indicators of complexity
        complexity_indicators = {
            "multi_entity": len(
                [w for w in ["and", "or", "between", "among"] if w in query_lower]
            ),
            "temporal": len(
                [
                    w
                    for w in ["when", "before", "after", "during", "since"]
                    if w in query_lower
                ]
            ),
            "relational": len(
                [
                    w
                    for w in ["how", "why", "relationship", "connection", "related"]
                    if w in query_lower
                ]
            ),
            "comparative": len(
                [
                    w
                    for w in ["compare", "difference", "similar", "versus"]
                    if w in query_lower
                ]
            ),
            "quantitative": len(
                [
                    w
                    for w in ["how many", "count", "number", "statistics"]
                    if w in query_lower
                ]
            ),
        }

        total_complexity = sum(complexity_indicators.values())
        word_count = len(query.split())

        if total_complexity >= 3 or word_count > 15:
            return QueryComplexity.COMPLEX
        if total_complexity >= 1 or word_count > 7:
            return QueryComplexity.MEDIUM
        return QueryComplexity.SIMPLE

    def choose_retrieval_strategy(
        self, query: str, complexity: QueryComplexity
    ) -> RetrievalStrategy:
        """Choose optimal retrieval strategy based on query and complexity."""
        if self.config.strategy != RetrievalStrategy.ADAPTIVE:
            return self.config.strategy

        # Strategy selection logic
        query_lower = query.lower()

        # Use reranking for complex queries
        if complexity == QueryComplexity.COMPLEX:
            return RetrievalStrategy.RERANKED

        # Use multi-query for medium complexity
        if complexity == QueryComplexity.MEDIUM:
            return RetrievalStrategy.MULTI_QUERY

        # Use hybrid for key-heavy queries
        if any(word in query_lower for word in ["specific", "exact", "name", "title"]):
            return RetrievalStrategy.HYBRID

        # Default to contextual compression
        return RetrievalStrategy.CONTEXTUAL

    async def retrieve_documents(
        self,
        query: str,
        strategy: RetrievalStrategy | None = None,
        k: int | None = None,
    ) -> list[Document]:
        """Retrieve documents using specified strategy."""
        if strategy is None:
            complexity = self.analyze_query_complexity(query)
            strategy = self.choose_retrieval_strategy(query, complexity)

        k = k or self.config.k_final

        try:
            if strategy == RetrievalStrategy.DENSE_ONLY:
                if self.config.enable_time_weighting:
                    self.time_weighted_retriever.k = k
                    docs = self.time_weighted_retriever.get_relevant_documents(query)
                else:
                    docs = self.dense_retriever.get_relevant_documents(query)

            elif strategy == RetrievalStrategy.SPARSE_ONLY and self.sparse_retriever:
                self.sparse_retriever.k = k
                docs = self.sparse_retriever.get_relevant_documents(query)

            elif strategy == RetrievalStrategy.HYBRID:
                docs = self.ensemble_retriever.get_relevant_documents(query)

            elif strategy == RetrievalStrategy.MULTI_QUERY and hasattr(
                self, "multi_query_retriever"
            ):
                docs = self.multi_query_retriever.get_relevant_documents(query)

            elif strategy == RetrievalStrategy.CONTEXTUAL:
                docs = self.contextual_retriever.get_relevant_documents(query)

            elif strategy == RetrievalStrategy.RERANKED:
                docs = self.reranking_retriever.get_relevant_documents(query)

            else:
                # Fallback to dense retrieval
                docs = self.dense_retriever.get_relevant_documents(query)

            # Apply importance boosting if available
            docs = self._apply_importance_boost(docs)

            # Limit results
            return docs[:k]

        except Exception as e:
            self.logger.exception(f"Error in retrieval with strategy {strategy}: {e}")
            # Fallback to simple dense retrieval
            return self.dense_retriever.get_relevant_documents(query)[:k]

    def _apply_importance_boost(self, docs: list[Document]) -> list[Document]:
        """Boost important documents in ranking."""
        if not self.config.importance_boost or self.config.importance_boost == 1.0:
            return docs

        # Sort by importance, then by original ranking
        def importance_score(doc):
            importance = doc.metadata.get("importance", "normal")
            importance_values = {"critical": 4, "high": 3, "normal": 2, "low": 1}
            base_score = importance_values.get(importance, 2)
            return base_score * self.config.importance_boost

        # Sort by importance while maintaining relative order within importance
        # levels
        docs_with_scores = [
            (doc, importance_score(doc), i) for i, doc in enumerate(docs)
        ]
        docs_with_scores.sort(key=lambda x: (-x[1], x[2]))

        return [doc for doc, _, _ in docs_with_scores]

    async def generate_with_citations(
        self,
        query: str,
        retrieved_docs: list[Document],
        include_citations: bool | None = None,
    ) -> dict[str, Any]:
        """Generate response with citations."""
        include_citations = include_citations or self.config.include_citations

        # Prepare context with document IDs
        context_parts = []
        doc_citations = {}

        for i, doc in enumerate(retrieved_docs):
            doc_id = doc.metadata.get("doc_id", f"doc_{i}")
            doc_citations[doc_id] = {
                "content": doc.page_content,
                "metadata": doc.metadata,
                "index": i,
            }

            if include_citations:
                citation = self.config.citation_format.format(doc_id=doc_id)
                context_parts.append(f"{doc.page_content} {citation}")
            else:
                context_parts.append(doc.page_content)

        # Combine context
        full_context = "\n\n".join(context_parts)

        # Truncate if too long
        if len(full_context) > self.config.max_context_length:
            full_context = full_context[: self.config.max_context_length] + "..."

        # Generate response
        if hasattr(self.memory_agent, "arun"):
            generation_prompt = f"""Context from memory:
{full_context}

Question: {query}

Please provide a comprehensive answer based on the context above."""

            response = await self.memory_agent.arun(generation_prompt)
        else:
            # Fallback for SimpleAgent
            generation_prompt = f"""Based on this context from memory, answer the question.

Context:
{full_context}

Question: {query}

Answer:"""
            response = await self.memory_agent.arun(generation_prompt)

        return {
            "answer": response,
            "citations": doc_citations if include_citations else None,
            "retrieved_docs": len(retrieved_docs),
            "context_length": len(full_context),
        }

    async def add_memory(
        self,
        content: str,
        metadata: dict[str, Any] | None = None,
        importance: str = "normal",
    ) -> dict[str, Any]:
        """Add new memory to the system."""
        # Prepare metadata
        doc_metadata = {
            "timestamp": datetime.now().isoformat(),
            "user_id": self.config.user_id,
            "doc_id": f"mem_{len(self.documents)}_{int(datetime.now().timestamp())}",
            "importance": importance,
            **(metadata or {}),
        }

        # Create document
        doc = Document(page_content=content, metadata=doc_metadata)

        # Add to vector store
        self.vector_store.add_documents([doc])

        # Update document lists
        self.documents.append(doc)
        self.document_metadata[doc_metadata["doc_id"]] = doc_metadata

        # Reinitialize BM25 if enabled
        if self.config.enable_bm25:
            try:
                self.sparse_retriever = BM25Retriever.from_documents(
                    self.documents, k=self.config.k_initial
                )

                # Update ensemble retriever
                self.ensemble_retriever = EnsembleRetriever(
                    retrievers=[self.dense_retriever, self.sparse_retriever],
                    weights=[self.config.dense_weight, self.config.sparse_weight],
                )
            except Exception as e:
                self.logger.warning(f"Could not reinitialize BM25: {e}")

        return {
            "doc_id": doc_metadata["doc_id"],
            "stored": True,
            "total_documents": len(self.documents),
        }

    async def query_memory(
        self,
        query: str,
        strategy: RetrievalStrategy | None = None,
        include_analysis: bool = True,
    ) -> dict[str, Any]:
        """Query memory with advanced RAG capabilities."""
        start_time = datetime.now()

        # Analyze query
        complexity = self.analyze_query_complexity(query)
        chosen_strategy = strategy or self.choose_retrieval_strategy(query, complexity)

        # Retrieve documents
        retrieved_docs = await self.retrieve_documents(query, chosen_strategy)

        # Generate response with citations
        generation_result = await self.generate_with_citations(query, retrieved_docs)

        # Calculate timing
        end_time = datetime.now()
        processing_time = (end_time - start_time).total_seconds()

        # Store query in history
        query_record = {
            "query": query,
            "complexity": complexity.value,
            "strategy": chosen_strategy.value,
            "retrieved_docs": len(retrieved_docs),
            "processing_time": processing_time,
            "timestamp": start_time.isoformat(),
        }
        self.query_history.append(query_record)

        result = {
            "query": query,
            "answer": generation_result["answer"],
            "processing_time": processing_time,
            **generation_result,
        }

        if include_analysis:
            result["analysis"] = {
                "complexity": complexity.value,
                "strategy_used": chosen_strategy.value,
                "total_documents": len(self.documents),
                "user_id": self.config.user_id,
            }

        return result

    async def get_memory_analytics(self) -> dict[str, Any]:
        """Get comprehensive analytics about memory usage."""
        # Document statistics
        doc_stats = {
            "total_documents": len(self.documents),
            "by_importance": {},
            "by_usef": {},
            "recent_additions": 0,
        }

        # Analyze documents
        recent_threshold = datetime.now().timestamp() - 86400  # 24 hours

        for doc in self.documents:
            importance = doc.metadata.get("importance", "normal")
            user_id = doc.metadata.get("user_id", "unknown")

            doc_stats["by_importance"][importance] = (
                doc_stats["by_importance"].get(importance, 0) + 1
            )
            doc_stats["by_user"][user_id] = doc_stats["by_user"].get(user_id, 0) + 1

            # Check if recent
            try:
                timestamp_str = doc.metadata.get("timestamp", "")
                if timestamp_str:
                    doc_time = datetime.fromisoformat(
                        timestamp_str.replace("Z", "+00:00")
                    ).timestamp()
                    if doc_time > recent_threshold:
                        doc_stats["recent_additions"] += 1
            except BaseException:
                pass

        # Query statistics
        query_stats = {
            "total_queries": len(self.query_history),
            "avg_processing_time": 0,
            "complexity_distribution": {},
            "strategy_usage": {},
        }

        if self.query_history:
            query_stats["avg_processing_time"] = sum(
                q["processing_time"] for q in self.query_history
            ) / len(self.query_history)

            for query in self.query_history:
                complexity = query["complexity"]
                strategy = query["strategy"]

                query_stats["complexity_distribution"][complexity] = (
                    query_stats["complexity_distribution"].get(complexity, 0) + 1
                )
                query_stats["strategy_usage"][strategy] = (
                    query_stats["strategy_usage"].get(strategy, 0) + 1
                )

        return {
            "timestamp": datetime.now().isoformat(),
            "config": {
                "strategy": self.config.strategy.value,
                "k_final": self.config.k_final,
                "enable_reranking": self.config.enable_reranking,
                "enable_citations": self.config.include_citations,
            },
            "documents": doc_stats,
            "queries": query_stats,
        }

    def save_memory_store(self, path: str | None = None):
        """Save the vector store and metadata."""
        save_path = path or self.config.memory_store_path
        if save_path:
            try:
                if self.config.vector_store_type == "faiss":
                    self.vector_store.save_local(save_path)
                elif self.config.vector_store_type == "chroma":
                    # Chroma auto-persists if persist_directory is set
                    pass

                # Save document metadata
                metadata_path = f"{save_path}/document_metadata.json"
                with open(metadata_path, "w") as f:
                    json.dump(self.document_metadata, f, indent=2)

                self.logger.info(f"Memory store saved to {save_path}")
            except Exception as e:
                self.logger.exception(f"Error saving memory store: {e}")


# Example usage and factory functions
async def create_research_memory_agent() -> AdvancedRAGMemoryAgent:
    """Create a research-focused memory agent."""
    config = AdvancedRAGConfig(
        user_id="researcher",
        strategy=RetrievalStrategy.ADAPTIVE,
        k_initial=15,
        k_final=5,
        enable_reranking=True,
        enable_query_expansion=True,
        include_citations=True,
        importance_boost=1.3,
    )

    return AdvancedRAGMemoryAgent(config)


async def create_conversational_memory_agent() -> AdvancedRAGMemoryAgent:
    """Create a conversation-focused memory agent."""
    config = AdvancedRAGConfig(
        user_id="conversational_user",
        strategy=RetrievalStrategy.HYBRID,
        enable_time_weighting=True,
        recency_decay=0.02,  # Faster decay for conversations
        k_final=3,
        include_citations=False,  # Less formal for conversation
        importance_boost=1.1,
    )

    return AdvancedRAGMemoryAgent(config)


# Example usage
async def example_advanced_rag_usage():
    """Example of using Advanced RAG Memory Agent."""
    agent = await create_research_memory_agent()

    # Add memories
    memories = [
        (
            "Dr. Sarah Chen published a groundbreaking paper on Graph Neural Networks in Nature 2023.",
            "high",
        ),
        (
            "The paper introduces a new attention mechanism for graph-structured data.",
            "high",
        ),
        (
            "Sarah works at Stanford AI Lab and collaborates with Google Research.",
            "normal",
        ),
        ("Her previous work on knowledge graphs was cited over 1000 times.", "high"),
        (
            "I met Sarah at NeurIPS 2023 where she presented her latest findings.",
            "normal",
        ),
        ("She mentioned that graph transformers could revolutionize NLP.", "critical"),
    ]

    for content, importance in memories:
        await agent.add_memory(content, importance=importance)

    # Query with different complexities
    queries = [
        "Who is Dr. Sarah Chen?",  # Simple
        "What did Sarah Chen publish and where does she work?",  # Medium
        "How do Sarah Chen's graph neural network contributions relate to NLP and what impact have they had?",  # Complex
    ]

    for query in queries:
        await agent.query_memory(query, include_analysis=True)

    # Get analytics
    await agent.get_memory_analytics()


if __name__ == "__main__":
    import asyncio

    asyncio.run(example_advanced_rag_usage())
