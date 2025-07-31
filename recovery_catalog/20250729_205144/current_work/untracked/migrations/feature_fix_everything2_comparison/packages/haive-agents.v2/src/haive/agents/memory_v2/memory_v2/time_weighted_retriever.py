"""Time-weighted retriever for Memory V2 system.

Based on LangChain's time-weighted retriever patterns for long-term memory agents.
Combines semantic similarity with recency weighting for optimal memory retrieval.

Reference: https://python.langchain.com/docs/versions/migrating_memory/long_term_memory_agent/
"""

import logging
import math
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from langchain_core.callbacks.manager import CallbackManagerForRetrieverRun
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel, Field

from .message_document_converter import TimestampedDocument

logger = logging.getLogger(__name__)


class TimeWeightConfig(BaseModel):
    """Configuration for time-weighted retrieval."""

    # Time weighting parameters
    decay_rate: float = Field(
        default=0.01, description="How quickly relevance decays per hour"
    )
    recency_weight: float = Field(
        default=0.3, description="Weight of recency vs similarity (0.0-1.0)"
    )
    max_age_hours: float = Field(
        default=24 * 30, description="Maximum age in hours to consider"
    )

    # Retrieval parameters
    k: int = Field(default=5, description="Number of documents to retrieve")
    score_threshold: float = Field(default=0.0, description="Minimum score threshold")

    # Importance boosting
    importance_boost: dict[str, float] = Field(
        default={"critical": 1.5, "high": 1.2, "medium": 1.0, "low": 0.8},
        description="Score multipliers by importance level",
    )

    # Document type preferences
    type_preferences: dict[str, float] = Field(
        default={
            "memory": 1.3,
            "conversation_summary": 1.1,
            "human": 1.0,
            "ai": 0.9,
            "extracted_memory": 1.2,
        },
        description="Preference weights by document type",
    )


class TimeWeightedRetriever(BaseRetriever):
    """Time-weighted retriever combining semantic similarity with recency."""

    vectorstore: VectorStore
    config: TimeWeightConfig = Field(default_factory=TimeWeightConfig)
    memory_importance_field: str = Field(default="importance")
    timestamp_field: str = Field(default="timestamp")
    document_type_field: str = Field(default="message_type")

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def __init__(
        self, vectorstore: VectorStore, config: TimeWeightConfig = None, **kwargs
    ):
        """Initialize time-weighted retriever."""
        if config is None:
            config = TimeWeightConfig()

        super().__init__(vectorstore=vectorstore, config=config, **kwargs)

        logger.info(
            f"Initialized TimeWeightedRetriever with decay_rate={config.decay_rate}, recency_weight={config.recency_weight}"
        )

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> list[Document]:
        """Retrieve documents using time-weighted scoring."""
        # Get candidate documents from vector store
        # Get more candidates than needed for reranking
        candidate_k = min(self.config.k * 3, 50)

        try:
            candidates = self.vectorstore.similarity_search_with_score(
                query, k=candidate_k
            )
        except Exception as e:
            logger.warning(f"Vector search failed: {e}, falling back to basic search")
            candidates = [
                (doc, 1.0)
                for doc in self.vectorstore.similarity_search(query, k=candidate_k)
            ]

        # Calculate time-weighted scores
        scored_docs = []
        current_time = datetime.now(UTC)

        for doc, similarity_score in candidates:
            # Calculate time decay
            time_score = self._calculate_time_score(doc, current_time)

            # Calculate importance boost
            importance_score = self._calculate_importance_score(doc)

            # Calculate document type preference
            type_score = self._calculate_type_score(doc)

            # Combined score
            final_score = self._combine_scores(
                similarity_score=similarity_score,
                time_score=time_score,
                importance_score=importance_score,
                type_score=type_score,
            )

            # Apply threshold filter
            if final_score >= self.config.score_threshold:
                scored_docs.append((doc, final_score))

        # Sort by final score and return top k
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        top_docs = [doc for doc, score in scored_docs[: self.config.k]]

        logger.debug(
            f"Retrieved {len(top_docs)} documents from {len(candidates)} candidates"
        )

        return top_docs

    def _calculate_time_score(self, doc: Document, current_time: datetime) -> float:
        """Calculate time-based relevance score."""
        timestamp_str = doc.metadata.get(self.timestamp_field)

        if not timestamp_str:
            # No timestamp, use neutral score
            return 0.5

        try:
            if isinstance(timestamp_str, str):
                timestamp = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            elif isinstance(timestamp_str, datetime):
                timestamp = timestamp_str
            else:
                return 0.5

        except (ValueError, TypeError):
            logger.warning(f"Invalid timestamp format: {timestamp_str}")
            return 0.5

        # Calculate age in hours
        age_hours = (current_time - timestamp).total_seconds() / 3600

        # Apply exponential decay
        time_score = math.exp(-self.config.decay_rate * age_hours)

        # Cap at max age
        if age_hours > self.config.max_age_hours:
            time_score *= 0.1  # Heavily penalize very old documents

        return max(0.0, min(1.0, time_score))

    def _calculate_importance_score(self, doc: Document) -> float:
        """Calculate importance-based relevance boost."""
        importance = doc.metadata.get(self.memory_importance_field, "medium")

        # Handle both string and enum values
        if hasattr(importance, "value"):
            importance = importance.value

        importance_str = str(importance).lower()
        return self.config.importance_boost.get(importance_str, 1.0)

    def _calculate_type_score(self, doc: Document) -> float:
        """Calculate document type preference score."""
        doc_type = doc.metadata.get(self.document_type_field, "unknown")

        # Handle both string and enum values
        if hasattr(doc_type, "value"):
            doc_type = doc_type.value

        type_str = str(doc_type).lower()
        return self.config.type_preferences.get(type_str, 1.0)

    def _combine_scores(
        self,
        similarity_score: float,
        time_score: float,
        importance_score: float,
        type_score: float,
    ) -> float:
        """Combine all scoring components into final score."""
        # Normalize similarity score (vector stores return different ranges)
        normalized_similarity = max(0.0, min(1.0, similarity_score))

        # Weighted combination
        semantic_component = normalized_similarity * (1 - self.config.recency_weight)
        temporal_component = time_score * self.config.recency_weight

        base_score = semantic_component + temporal_component

        # Apply importance and type boosts
        final_score = base_score * importance_score * type_score

        return final_score

    def get_relevant_documents_with_scores(
        self, query: str
    ) -> list[tuple[Document, float]]:
        """Get documents with their calculated scores for debugging."""
        current_time = datetime.now(UTC)

        # Get candidates
        candidate_k = min(self.config.k * 3, 50)

        try:
            candidates = self.vectorstore.similarity_search_with_score(
                query, k=candidate_k
            )
        except Exception:
            candidates = [
                (doc, 1.0)
                for doc in self.vectorstore.similarity_search(query, k=candidate_k)
            ]

        # Score all candidates
        scored_docs = []

        for doc, similarity_score in candidates:
            time_score = self._calculate_time_score(doc, current_time)
            importance_score = self._calculate_importance_score(doc)
            type_score = self._calculate_type_score(doc)

            final_score = self._combine_scores(
                similarity_score, time_score, importance_score, type_score
            )

            if final_score >= self.config.score_threshold:
                scored_docs.append((doc, final_score))

        # Sort and return top k with scores
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        return scored_docs[: self.config.k]

    def update_config(self, **config_updates):
        """Update retriever configuration."""
        config_dict = self.config.model_dump()
        config_dict.update(config_updates)
        self.config = TimeWeightConfig(**config_dict)

        logger.info(f"Updated config: {config_updates}")


class MemoryRetrievalSession:
    """Session for managing retrieval with context and history."""

    def __init__(
        self,
        retriever: TimeWeightedRetriever,
        session_id: str = None,
        user_id: str = None,
    ):
        """Initialize retrieval session."""
        self.retriever = retriever
        self.session_id = session_id or f"session_{uuid4()}"
        self.user_id = user_id
        self.query_history: list[dict[str, Any]] = []
        self.retrieved_doc_ids: set = set()

    def retrieve_with_context(
        self, query: str, exclude_recent: bool = True, context_boost: bool = True
    ) -> list[Document]:
        """Retrieve documents with session context awareness."""
        # Get base results
        scored_docs = self.retriever.get_relevant_documents_with_scores(query)

        # Apply context-aware filtering and boosting
        if exclude_recent:
            # Avoid returning recently retrieved documents
            scored_docs = [
                (doc, score)
                for doc, score in scored_docs
                if doc.metadata.get("doc_id", "") not in self.retrieved_doc_ids
            ]

        if context_boost and self.query_history:
            # Boost documents related to previous queries
            scored_docs = self._apply_context_boost(scored_docs)

        # Track retrieved documents
        final_docs = [doc for doc, score in scored_docs]
        for doc in final_docs:
            doc_id = doc.metadata.get("doc_id", "")
            if doc_id:
                self.retrieved_doc_ids.add(doc_id)

        # Record query
        self.query_history.append(
            {
                "query": query,
                "timestamp": datetime.now(UTC).isoformat(),
                "results_count": len(final_docs),
                "doc_ids": [doc.metadata.get("doc_id", "") for doc in final_docs],
            }
        )

        return final_docs

    def _apply_context_boost(
        self, scored_docs: list[tuple[Document, float]]
    ) -> list[tuple[Document, float]]:
        """Apply context-aware score boosting."""
        if not self.query_history:
            return scored_docs

        # Get keywords from recent queries
        recent_queries = self.query_history[-3:]  # Last 3 queries
        query_keywords = set()

        for query_record in recent_queries:
            query_keywords.update(query_record["query"].lower().split())

        # Boost documents mentioning similar concepts
        boosted_docs = []

        for doc, score in scored_docs:
            content_words = set(doc.page_content.lower().split())
            keyword_overlap = len(query_keywords.intersection(content_words))

            if keyword_overlap > 0:
                context_boost = 1.0 + (
                    keyword_overlap * 0.1
                )  # 10% boost per overlapping key
                score *= context_boost

            boosted_docs.append((doc, score))

        # Re-sort by boosted scores
        boosted_docs.sort(key=lambda x: x[1], reverse=True)
        return boosted_docs

    def get_session_stats(self) -> dict[str, Any]:
        """Get session retrieval statistics."""
        return {
            "session_id": self.session_id,
            "user_id": self.user_id,
            "total_queries": len(self.query_history),
            "unique_documents_retrieved": len(self.retrieved_doc_ids),
            "recent_queries": self.query_history[-5:],  # Last 5 queries
            "avg_results_per_query": (
                sum(q["results_count"] for q in self.query_history)
                / len(self.query_history)
                if self.query_history
                else 0
            ),
        }


# ============================================================================
# RETRIEVER FACTORY
# ============================================================================


def create_time_weighted_retriever(
    vectorstore: VectorStore,
    decay_rate: float = 0.01,
    recency_weight: float = 0.3,
    k: int = 5,
) -> TimeWeightedRetriever:
    """Factory function to create configured time-weighted retriever.

    Args:
        vectorstore: Vector store containing timestamped documents
        decay_rate: How quickly relevance decays per hour
        recency_weight: Weight of recency vs similarity (0.0-1.0)
        k: Number of documents to retrieve

    Returns:
        Configured TimeWeightedRetriever
    """
    config = TimeWeightConfig(decay_rate=decay_rate, recency_weight=recency_weight, k=k)

    return TimeWeightedRetriever(vectorstore=vectorstore, config=config)


def create_memory_focused_retriever(vectorstore: VectorStore) -> TimeWeightedRetriever:
    """Create retriever optimized for memory retrieval.

    Args:
        vectorstore: Vector store with memory documents

    Returns:
        Memory-optimized TimeWeightedRetriever
    """
    config = TimeWeightConfig(
        decay_rate=0.005,  # Slower decay for memories
        recency_weight=0.2,  # Less emphasis on recency for memories
        k=8,  # More results for memory
        importance_boost={
            "critical": 2.0,  # Strong boost for critical memories
            "high": 1.5,
            "medium": 1.0,
            "low": 0.6,
        },
        type_preferences={
            "extracted_memory": 1.5,  # Prefer extracted memories
            "memory": 1.4,
            "conversation_summary": 1.2,
            "human": 1.0,
            "ai": 0.8,
        },
    )

    return TimeWeightedRetriever(vectorstore=vectorstore, config=config)


# ============================================================================
# DOCUMENT PREPARATION UTILITIES
# ============================================================================


def prepare_documents_for_time_retrieval(
    documents: list[TimestampedDocument],
) -> list[Document]:
    """Prepare timestamped documents for time-weighted retrieval.

    Args:
        documents: List of timestamped documents

    Returns:
        List of documents ready for vector store ingestion
    """
    prepared_docs = []

    for doc in documents:
        # Ensure required metadata exists
        metadata = doc.metadata.copy()

        # Standardize timestamp format
        if "timestamp" not in metadata:
            metadata["timestamp"] = datetime.now(UTC).isoformat()

        # Ensure doc_id exists
        if "doc_id" not in metadata:
            metadata["doc_id"] = str(uuid4())

        # Standardize importance
        if "importance" not in metadata:
            metadata["importance"] = "medium"

        # Standardize message type
        if "message_type" not in metadata:
            metadata["message_type"] = "unknown"

        prepared_doc = Document(page_content=doc.page_content, metadata=metadata)

        prepared_docs.append(prepared_doc)

    return prepared_docs
