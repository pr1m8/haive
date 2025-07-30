"""Enhanced Self-Query Retriever with Memory Context.

This module implements Phase 2 of the incremental memory system: Enhanced Self-Query
retriever that integrates memory classification with sophisticated retrieval strategies.

The enhanced retriever builds on the memory classification system to provide:
- Memory-type aware retrieval (semantic, episodic, procedural, etc.)
- Context-aware query expansion
- Memory importance weighting
- Time-based relevance scoring
- Self-query with metadata filtering

This is the next phase after the foundational memory classification system,
bridging toward full Graph RAG implementation.
"""

import logging
from datetime import datetime
from typing import Any

from haive.core.tools.store_tools import StoreManager
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory.core.classifier import MemoryClassifier, MemoryClassifierConfig
from haive.agents.memory.core.stores import MemoryStoreConfig, MemoryStoreManager
from haive.agents.memory.core.types import (
    MemoryQueryIntent,
    MemoryType,
    Optional,
    from,
    import,
    typing,
)

logger = logging.getLogger(__name__)


class EnhancedRetrieverConfig(BaseModel):
    """Configuration for enhanced memory retriever with self-query capabilities.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Core components
    memory_store_manager: MemoryStoreManager = Field(
        ..., description="Memory store manager"
    )
    memory_classifier: MemoryClassifier = Field(
        ..., description="Memory classifier for query analysis"
    )

    # Retrieval configuration
    default_limit: int = Field(
        default=10, description="Default number of memories to retrieve"
    )
    max_limit: int = Field(
        default=50, description="Maximum number of memories to retrieve"
    )
    similarity_threshold: float = Field(
        default=0.7, description="Minimum similarity threshold"
    )

    # Memory type weighting
    memory_type_weights: dict[str, float] = Field(
        default_factory=lambda: {
            MemoryType.SEMANTIC.value: 1.0,
            MemoryType.EPISODIC.value: 1.2,  # Boost episodic memories
            MemoryType.PROCEDURAL.value: 1.1,
            MemoryType.CONTEXTUAL.value: 0.9,
            MemoryType.PREFERENCE.value: 0.8,
            MemoryType.META.value: 0.7,
            MemoryType.EMOTIONAL.value: 0.8,
            MemoryType.TEMPORAL.value: 0.9,
            MemoryType.ERROR.value: 1.3,  # Boost error memories for learning
            MemoryType.FEEDBACK.value: 1.2,  # Boost feedback for improvement
            MemoryType.SYSTEM.value: 0.6,
        },
        description="Weight multipliers for different memory types",
    )

    # Time-based scoring
    enable_temporal_scoring: bool = Field(
        default=True, description="Enable time-based relevance scoring"
    )
    recency_decay_hours: float = Field(
        default=168, description="Hours for recency decay (default: 1 week)"
    )
    recency_weight: float = Field(
        default=0.2, description="Weight for recency in final scoring"
    )

    # Query expansion
    enable_query_expansion: bool = Field(
        default=True, description="Enable automatic query expansion"
    )
    expansion_terms_limit: int = Field(
        default=5, description="Maximum expansion terms to add"
    )

    # Self-query filtering
    enable_metadata_filtering: bool = Field(
        default=True, description="Enable metadata-based filtering"
    )
    enable_importance_filtering: bool = Field(
        default=True, description="Enable importance-based filtering"
    )


class EnhancedQueryResult(BaseModel):
    """Result of enhanced memory retrieval with detailed metadata.
    """

    # Core results
    memories: list[dict[str, Any]] = Field(
        default_factory=list, description="Retrieved memories"
    )
    total_found: int = Field(
        default=0, description="Total memories found before limiting"
    )

    # Query analysis
    query_intent: Optional[MemoryQueryIntent] = Field(
        default=None, description="Analyzed query intent"
    )
    expanded_query: Optional[str] = Field(
        default=None, description="Query after expansion"
    )
    memory_types_targeted: list[MemoryType] = Field(
        default_factory=list, description="Memory types targeted"
    )

    # Retrieval metadata
    similarity_scores: list[float] = Field(
        default_factory=list, description="Similarity scores for each result"
    )
    importance_scores: list[float] = Field(
        default_factory=list, description="Importance scores for each result"
    )
    recency_scores: list[float] = Field(
        default_factory=list, description="Recency scores for each result"
    )
    final_scores: list[float] = Field(
        default_factory=list, description="Combined final scores"
    )

    # Performance metrics
    retrieval_time_ms: float = Field(
        default=0.0, description="Retrieval time in milliseconds"
    )
    classification_time_ms: float = Field(
        default=0.0, description="Query classification time"
    )
    total_time_ms: float = Field(
        default=0.0, description="Total processing time")


class EnhancedMemoryRetriever:
    """Enhanced self-query retriever with memory-aware context and sophisticated scoring.

    This retriever implements Phase 2 of the incremental memory system, building on
    the memory classification foundation to provide intelligent, context-aware retrieval.

    Key features:
    - Memory type classification and targeting
    - Query intent analysis and expansion
    - Multi-factor scoring (similarity + importance + recency + type)
    - Metadata filtering and self-query capabilities
    - Performance monitoring and optimization
    """

    def __init__(self, config: EnhancedRetrieverConfig):
        """Initialize enhanced memory retriever.
        """
        self.config = config
        self.memory_store = config.memory_store_manager
        self.classifier = config.memory_classifier

        # Performance tracking
        self._retrieval_stats = {
            "total_queries": 0,
            "avg_retrieval_time": 0.0,
            "avg_results_returned": 0.0,
            "memory_type_distribution": {mt.value: 0 for mt in MemoryType},
        }

    async def retrieve_memories(
        self,
        query: str,
        memory_types: list[MemoryType] | None = None,
        importance_threshold: Optional[float] = None,
        time_range: tuple[datetime, datetime] | None = None,
        limit: Optional[int] = None,
        include_metadata: bool = True,
        namespace: tuple[str, ...] | None = None,
    ) -> EnhancedQueryResult:
        """Retrieve memories using enhanced self-query with memory context.

        Args:
            query: Natural language query
            memory_types: Specific memory types to target (auto-detected if None)
            importance_threshold: Minimum importance score filter
            time_range: Optional time range filter
            limit: Maximum results to return
            include_metadata: Whether to include detailed metadata
            namespace: Memory namespace to search

        Returns:
            EnhancedQueryResult with memories and detailed metadata
        """
        start_time = datetime.utcnow()

        try:
            # Phase 1: Query Analysis and Intent Classification
            classification_start = datetime.utcnow()
            query_intent = self.classifier.classify_query_intent(query)
            classification_time = (
                datetime.utcnow() - classification_start
            ).total_seconds() * 1000

            # Use detected memory types if not explicitly provided
            if memory_types is None:
                memory_types = query_intent.memory_types

            # Phase 2: Query Expansion
            expanded_query = query
            if self.config.enable_query_expansion:
                expanded_query = await self._expand_query(query, query_intent)

            # Phase 3: Memory Retrieval with Filtering
            retrieval_start = datetime.utcnow()

            raw_memories = await self.memory_store.retrieve_memories(
                query=expanded_query,
                namespace=namespace,
                memory_types=memory_types,
                limit=limit or self.config.max_limit,  # Retrieve more for re-ranking
                time_range=time_range,
                importance_threshold=importance_threshold,
            )

            retrieval_time = (
                datetime.utcnow() - retrieval_start
            ).total_seconds() * 1000

            # Phase 4: Enhanced Scoring and Re-ranking
            scored_memories = await self._apply_enhanced_scoring(
                memories=raw_memories,
                query=query,
                query_intent=query_intent,
                memory_types=memory_types,
            )

            # Phase 5: Final Limiting and Metadata Assembly
            final_limit = limit or self.config.default_limit
            final_memories = scored_memories[:final_limit]

            # Extract metadata for result
            similarity_scores = [m.get("similarity_score", 0.0)
                                 for m in final_memories]
            importance_scores = [
                m.get("metadata", {}).get("importance_score", 0.0)
                for m in final_memories
            ]
            recency_scores = [m.get("recency_score", 0.0)
                              for m in final_memories]
            final_scores = [m.get("final_score", 0.0) for m in final_memories]

            # Performance tracking
            total_time = (
                datetime.utcnow() - start_time).total_seconds() * 1000
            self._update_stats(total_time, len(final_memories), memory_types)

            # Build result
            result = EnhancedQueryResult(
                memories=final_memories,
                total_found=len(raw_memories),
                query_intent=query_intent,
                expanded_query=expanded_query,
                memory_types_targeted=memory_types,
                similarity_scores=similarity_scores,
                importance_scores=importance_scores,
                recency_scores=recency_scores,
                final_scores=final_scores,
                retrieval_time_ms=retrieval_time,
                classification_time_ms=classification_time,
                total_time_ms=total_time,
            )

            logger.info(
                f"Enhanced retrieval completed: {
                    len(final_memories)} memories in {
                    total_time:.1f}ms")
            return result

        except Exception as e:
            logger.exception(f"Error in enhanced memory retrieval: {e}")
            # Return empty result on error
            return EnhancedQueryResult(
                total_time_ms=(
                    datetime.utcnow() -
                    start_time).total_seconds() *
                1000)

    async def _expand_query(
            self,
            query: str,
            query_intent: MemoryQueryIntent) -> str:
        """Expand query with related terms and context.
        """
        try:
            # Simple expansion based on entities and topics
            expansion_terms = []

            # Add entities from query intent
            expansion_terms.extend(query_intent.entities[:2])  # Top 2 entities

            # Add topics from query intent
            expansion_terms.extend(query_intent.topics[:2])  # Top 2 topics

            # Memory type specific expansions
            if MemoryType.PROCEDURAL in query_intent.memory_types:
                if any(word in query.lower()
                       for word in ["how", "process", "step"]):
                    expansion_terms.extend(["workflow", "procedure", "method"])

            if MemoryType.EPISODIC in query_intent.memory_types and any(
                word in query.lower() for word in ["when", "conversation", "meeting"]
            ):
                expansion_terms.extend(["discussion", "event", "interaction"])

            # Limit expansion terms
            expansion_terms = expansion_terms[:
                                              self.config.expansion_terms_limit]

            if expansion_terms:
                expanded = f"{query} {' '.join(expansion_terms)}"
                logger.debug(f"Query expanded: '{query}' -> '{expanded}'")
                return expanded

            return query

        except Exception as e:
            logger.exception(f"Error expanding query: {e}")
            return query

    async def _apply_enhanced_scoring(
        self,
        memories: list[dict[str, Any]],
        query: str,
        query_intent: MemoryQueryIntent,
        memory_types: list[MemoryType],
    ) -> list[dict[str, Any]]:
        """Apply enhanced multi-factor scoring to memories.
        """
        try:
            scored_memories = []

            for memory in memories:
                metadata = memory.get("metadata", {})

                # Base similarity score (from vector search)
                similarity_score = memory.get("similarity_score", 0.5)

                # Importance score
                importance_score = metadata.get("importance_score", 0.5)

                # Memory type scoring
                memory_memory_types = [
                    MemoryType(mt) for mt in metadata.get("memory_types", [])
                ]
                type_score = self._calculate_type_score(
                    memory_memory_types, memory_types
                )

                # Recency scoring
                recency_score = 0.0
                if self.config.enable_temporal_scoring:
                    recency_score = self._calculate_recency_score(metadata)

                # Combine scores
                final_score = (
                    similarity_score * 0.4  # 40% similarity
                    + importance_score * 0.3  # 30% importance
                    + type_score * 0.2  # 20% type relevance
                    + recency_score * self.config.recency_weight  # Configurable recency
                )

                # Add scores to memory
                memory["importance_score"] = importance_score
                memory["type_score"] = type_score
                memory["recency_score"] = recency_score
                memory["final_score"] = final_score

                scored_memories.append(memory)

            # Sort by final score
            scored_memories.sort(
                key=lambda x: x.get(
                    "final_score", 0.0), reverse=True)

            return scored_memories

        except Exception as e:
            logger.exception(f"Error in enhanced scoring: {e}")
            return memories

    def _calculate_type_score(
        self, memory_types: list[MemoryType], target_types: list[MemoryType]
    ) -> float:
        """Calculate memory type relevance score.
        """
        if not memory_types or not target_types:
            return 0.5  # Neutral score

        # Check for exact matches
        matches = set(memory_types) & set(target_types)
        if not matches:
            return 0.3  # Low score for no matches

        # Calculate weighted score based on memory type weights
        total_weight = 0.0
        for memory_type in matches:
            weight = self.config.memory_type_weights.get(
                memory_type.value, 1.0)
            total_weight += weight

        # Normalize by number of target types
        normalized_score = total_weight / len(target_types)

        return min(1.0, normalized_score)

    def _calculate_recency_score(self, metadata: dict[str, Any]) -> float:
        """Calculate time-based recency score.
        """
        try:
            created_at_str = metadata.get(
                "created_at", datetime.utcnow().isoformat())
            created_at = datetime.fromisoformat(created_at_str)

            last_accessed_str = metadata.get("last_accessed", created_at_str)
            last_accessed = datetime.fromisoformat(last_accessed_str)

            now = datetime.utcnow()

            # Use the more recent of creation or last access
            most_recent = max(created_at, last_accessed)
            hours_since = (now - most_recent).total_seconds() / 3600

            # Exponential decay over configured period
            decay_factor = max(
                0.0, 1.0 - (hours_since / self.config.recency_decay_hours)
            )

            return decay_factor

        except Exception as e:
            logger.exception(f"Error calculating recency score: {e}")
            return 0.5

    def _update_stats(
            self,
            retrieval_time: float,
            results_count: int,
            memory_types: list[MemoryType]) -> None:
        """Update retrieval performance statistics.
        """
        try:
            self._retrieval_stats["total_queries"] += 1

            # Update running averages
            total_queries = self._retrieval_stats["total_queries"]
            self._retrieval_stats["avg_retrieval_time"] = (
                self._retrieval_stats["avg_retrieval_time"] * (
                    total_queries - 1) + retrieval_time) / total_queries
            self._retrieval_stats["avg_results_returned"] = (
                self._retrieval_stats["avg_results_returned"] * (
                    total_queries - 1) + results_count) / total_queries

            # Update memory type distribution
            for memory_type in memory_types:
                self._retrieval_stats["memory_type_distribution"][
                    memory_type.value
                ] += 1

        except Exception as e:
            logger.exception(f"Error updating stats: {e}")

    def get_performance_stats(self) -> dict[str, Any]:
        """Get retrieval performance statistics.
        """
        return dict(self._retrieval_stats)

    async def optimize_for_usage_patterns(self) -> dict[str, Any]:
        """Analyze usage patterns and suggest optimizations.
        """
        stats = self.get_performance_stats()

        recommendations = []

        # Performance recommendations
        if stats["avg_retrieval_time"] > 1000:  # >1 second
            recommendations.append(
                "Consider increasing similarity threshold to reduce candidates"
            )

        if stats["avg_results_returned"] < 3:
            recommendations.append(
                "Consider lowering similarity threshold to return more results"
            )

        # Memory type usage analysis
        type_distribution = stats["memory_type_distribution"]
        most_used_type = max(type_distribution.items(), key=lambda x: x[1])

        if most_used_type[1] > stats["total_queries"] * 0.6:
            recommendations.append(
                f"Consider optimizing for {most_used_type[0]} memory type"
            )

        return {
            "performance_stats": stats,
            "recommendations": recommendations,
            "optimization_suggestions": {
                "similarity_threshold": self.config.similarity_threshold,
                "memory_type_weights": self.config.memory_type_weights,
                "recency_weight": self.config.recency_weight,
            },
        }


# Factory function for easy creation
async def create_enhanced_memory_retriever(
    store_manager: StoreManager,
    namespace: tuple[str, ...] = ("memory", "enhanced"),
    classifier_config: Optional[MemoryClassifierConfig] = None,
    **retriever_kwargs,
) -> EnhancedMemoryRetriever:
    """Factory function to create an enhanced memory retriever.

    Args:
        store_manager: Store manager for memory persistence
        namespace: Default memory namespace
        classifier_config: Optional classifier configuration
        **retriever_kwargs: Additional retriever configuration options

    Returns:
        Configured EnhancedMemoryRetriever ready for use
    """
    # Create memory store manager
    memory_store_config = MemoryStoreConfig(
        store_manager=store_manager,
        default_namespace=namespace,
        classifier_config=classifier_config or MemoryClassifierConfig(),
        **{
            k: v
            for k, v in retriever_kwargs.items()
            if k in MemoryStoreConfig.__fields__
        },
    )

    memory_store_manager = MemoryStoreManager(memory_store_config)

    # Create memory classifier
    classifier = MemoryClassifier(
        classifier_config or MemoryClassifierConfig())

    # Create retriever configuration
    retriever_config = EnhancedRetrieverConfig(
        memory_store_manager=memory_store_manager,
        memory_classifier=classifier,
        **{
            k: v
            for k, v in retriever_kwargs.items()
            if k in EnhancedRetrieverConfig.__fields__
        },
    )

    return EnhancedMemoryRetriever(retriever_config)
