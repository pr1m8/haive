"""Memory store management system integrating with existing Haive store tools.

This module provides enhanced memory storage and retrieval capabilities
that build on the existing store tools with intelligent classification,
self-query retrieval, and memory lifecycle management.
"""

import logging
from datetime import datetime
from typing import Any

from haive.core.tools.store_tools import StoreManager
from pydantic import BaseModel, ConfigDict, Field

from haive.agents.memory.core.classifier import MemoryClassifier, MemoryClassifierConfig
from haive.agents.memory.core.types import (
    MemoryConsolidationResult,
    MemoryEntry,
    MemoryQueryIntent,
    MemoryType,
)

logger = logging.getLogger(__name__)


class MemoryStoreConfig(BaseModel):
    """Configuration for enhanced memory store management."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    # Store configuration
    store_manager: StoreManager = Field(..., description="Underlying store manager")
    default_namespace: tuple[str, ...] = Field(
        default=("memory", "general"), description="Default memory namespace"
    )

    # Classification configuration
    classifier_config: MemoryClassifierConfig = Field(
        default_factory=MemoryClassifierConfig, description="Memory classifier config"
    )
    auto_classify: bool = Field(
        default=True, description="Automatically classify memories on storage"
    )

    # Memory lifecycle configuration
    enable_decay: bool = Field(
        default=True, description="Enable memory importance decay over time"
    )
    consolidation_interval_hours: int = Field(
        default=24, description="Hours between memory consolidation"
    )
    max_memories_per_namespace: int = Field(
        default=1000, description="Maximum memories per namespace"
    )

    # Retrieval configuration
    default_retrieval_limit: int = Field(
        default=10, description="Default number of memories to retrieve"
    )
    similarity_threshold: float = Field(
        default=0.7, description="Minimum similarity for retrieval"
    )
    importance_boost: float = Field(
        default=0.2, description="Boost factor for high-importance memories"
    )


class MemoryStoreManager:
    """Enhanced memory store manager with intelligent classification and retrieval.

    This manager builds on the existing store tools to provide:
    - Automatic memory classification and metadata extraction
    - Self-query retrieval with memory context
    - Memory lifecycle management and consolidation
    - Multi-type memory retrieval strategies
    """

    def __init__(self, config: MemoryStoreConfig):
        """Initialize memory store manager with configuration."""
        self.config = config
        self.store_manager = config.store_manager
        self.classifier = (
            MemoryClassifier(config.classifier_config) if config.auto_classify else None
        )
        self._last_consolidation = datetime.utcnow()

    async def store_memory(
        self,
        content: str,
        namespace: tuple[str, ...] | None = None,
        user_context: dict[str, Any] | None = None,
        conversation_context: dict[str, Any] | None = None,
        force_classification: MemoryType | None = None,
        importance_override: float | None = None,
    ) -> str:
        """Store a memory with automatic classification and metadata extraction.

        Args:
            content: Memory content to store
            namespace: Memory namespace (defaults to configured default)
            user_context: User-specific context for classification
            conversation_context: Conversation context for classification
            force_classification: Override automatic classification
            importance_override: Override automatic importance scoring

        Returns:
            Memory ID for later retrieval
        """
        try:
            namespace = namespace or self.config.default_namespace

            # Create memory entry with classification
            if self.classifier and not force_classification:
                memory_entry = self.classifier.create_memory_entry(
                    content=content,
                    user_context=user_context,
                    conversation_context=conversation_context,
                    namespace="/".join(namespace),
                )
            else:
                # Manual memory entry
                memory_entry = MemoryEntry(
                    content=content,
                    memory_types=(
                        [force_classification]
                        if force_classification
                        else [MemoryType.SEMANTIC]
                    ),
                    user_context=user_context or {},
                    session_context=conversation_context or {},
                    namespace="/".join(namespace),
                )

            # Override importance if specified
            if importance_override is not None:
                memory_entry.importance_score = importance_override
                memory_entry.calculate_current_weight()

            # Store in underlying store manager
            memory_id = self.store_manager.store_memory(
                content=content,
                category=(
                    memory_entry.memory_types[0].value
                    if memory_entry.memory_types
                    else "general"
                ),
                namespace=namespace,
                metadata={
                    "memory_types": [mt.value for mt in memory_entry.memory_types],
                    "importance": memory_entry.importance.value,
                    "importance_score": memory_entry.importance_score,
                    "entities": memory_entry.entities,
                    "topics": memory_entry.topics,
                    "sentiment": memory_entry.sentiment,
                    "confidence": memory_entry.confidence,
                    "created_at": memory_entry.created_at.isoformat(),
                    "last_accessed": memory_entry.last_accessed.isoformat(),
                    "access_count": memory_entry.access_count,
                    "current_weight": memory_entry.current_weight,
                    "decay_rate": memory_entry.decay_rate,
                    "relationships": memory_entry.relationships,
                    "tags": memory_entry.tags,
                    "user_context": memory_entry.user_context,
                    "session_context": memory_entry.session_context,
                },
            )

            logger.info(
                f"Stored memory {memory_id} with types: {[mt.value for mt in memory_entry.memory_types]}"
            )

            # Check if consolidation is needed
            if self._should_consolidate():
                await self._schedule_consolidation(namespace)

            return memory_id

        except Exception as e:
            logger.exception(f"Error storing memory: {e}")
            raise

    async def retrieve_memories(
        self,
        query: str,
        namespace: tuple[str, ...] | None = None,
        memory_types: list[MemoryType] | None = None,
        limit: int | None = None,
        time_range: tuple[datetime, datetime] | None = None,
        importance_threshold: float | None = None,
    ) -> list[dict[str, Any]]:
        """Retrieve memories using intelligent query analysis and ranking.

        Args:
            query: Search query (natural language)
            namespace: Memory namespace to search
            memory_types: Specific memory types to search (if None, auto-detect)
            limit: Maximum number of results
            time_range: Optional time range filter (start, end)
            importance_threshold: Minimum importance score

        Returns:
            List of retrieved memories with metadata
        """
        try:
            namespace = namespace or self.config.default_namespace
            limit = limit or self.config.default_retrieval_limit

            # Analyze query intent if classifier is available
            query_intent = None
            if self.classifier:
                query_intent = self.classifier.classify_query_intent(query)
                if not memory_types:
                    memory_types = query_intent.memory_types

            # Search in underlying store
            results = self.store_manager.search_memories(
                query=query,
                namespace=namespace,
                limit=limit * 2,  # Get more results for re-ranking
            )

            # Filter and re-rank results
            filtered_results = []
            for result in results:
                # Convert MemoryEntry to dict format for consistency
                if hasattr(result, "to_store_value"):
                    result_dict = result.to_store_value()
                else:
                    result_dict = result

                metadata = result_dict.get("metadata", {})

                # Filter by memory types if specified
                if memory_types:
                    result_types = [
                        MemoryType(mt) for mt in metadata.get("memory_types", [])
                    ]
                    if not any(mt in memory_types for mt in result_types):
                        continue

                # Filter by time range
                if time_range:
                    created_at = datetime.fromisoformat(
                        metadata.get("created_at", datetime.utcnow().isoformat())
                    )
                    if not (time_range[0] <= created_at <= time_range[1]):
                        continue

                # Filter by importance threshold
                if importance_threshold:
                    importance_score = metadata.get("importance_score", 0.0)
                    if importance_score < importance_threshold:
                        continue

                # Update access metadata
                await self._update_access_metadata(result_dict.get("id"))

                # Add ranking score
                ranking_score = self._calculate_ranking_score(result_dict, query_intent)
                result_dict["ranking_score"] = ranking_score

                filtered_results.append(result_dict)

            # Sort by ranking score and limit results
            filtered_results.sort(
                key=lambda x: x.get("ranking_score", 0.0), reverse=True
            )

            return filtered_results[:limit]

        except Exception as e:
            logger.exception(f"Error retrieving memories: {e}")
            return []

    async def get_memory_by_id(self, memory_id: str) -> dict[str, Any] | None:
        """Retrieve a specific memory by ID and update access metadata.

        Args:
            memory_id: Unique memory identifier

        Returns:
            Memory data with metadata or None if not found
        """
        try:
            result = self.store_manager.retrieve_memory(memory_id)
            if result:
                await self._update_access_metadata(memory_id)
                return result.to_store_value()
            return None
        except Exception as e:
            logger.exception(f"Error retrieving memory {memory_id}: {e}")
            return None

    async def update_memory(
        self,
        memory_id: str,
        content: str | None = None,
        additional_metadata: dict[str, Any] | None = None,
        reclassify: bool = False,
    ) -> bool:
        """Update an existing memory with new content or metadata.

        Args:
            memory_id: Memory identifier
            content: New content (if updating content)
            additional_metadata: Additional metadata to merge
            reclassify: Whether to reclassify memory types

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get existing memory
            existing = await self.get_memory_by_id(memory_id)
            if not existing:
                return False

            # Update content if provided
            if content and reclassify and self.classifier:
                # Reclassify with new content
                memory_entry = self.classifier.create_memory_entry(content=content)
                classification_metadata = {
                    "memory_types": [mt.value for mt in memory_entry.memory_types],
                    "importance": memory_entry.importance.value,
                    "importance_score": memory_entry.importance_score,
                    "entities": memory_entry.entities,
                    "topics": memory_entry.topics,
                    "sentiment": memory_entry.sentiment,
                    "confidence": memory_entry.confidence,
                }
                additional_metadata = {
                    **(additional_metadata or {}),
                    **classification_metadata,
                }

            # Update in store
            success = self.store_manager.update_memory(
                memory_id=memory_id, content=content, metadata=additional_metadata
            )

            if success:
                logger.info(f"Updated memory {memory_id}")

            return success

        except Exception as e:
            logger.exception(f"Error updating memory {memory_id}: {e}")
            return False

    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory by ID.

        Args:
            memory_id: Memory identifier to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            return self.store_manager.delete_memory(memory_id)
        except Exception as e:
            logger.exception(f"Error deleting memory {memory_id}: {e}")
            return False

    async def consolidate_memories(
        self,
        namespace: tuple[str, ...] | None = None,
        max_age_hours: int | None = None,
        dry_run: bool = False,
    ) -> MemoryConsolidationResult:
        """Consolidate memories by removing duplicates, summarizing old memories, and cleaning up.

        Args:
            namespace: Namespace to consolidate (if None, consolidate all)
            max_age_hours: Maximum age of memories to keep (if None, use decay calculation)
            dry_run: If True, only analyze without making changes

        Returns:
            MemoryConsolidationResult with consolidation statistics
        """
        start_time = datetime.utcnow()
        result = MemoryConsolidationResult()

        try:
            namespace = namespace or self.config.default_namespace

            # Get all memories in namespace
            all_memories = self.store_manager.search_memories(
                query="",  # Empty query to get all
                namespace=namespace,
                limit=10000,  # Large limit to get all
            )

            logger.info(
                f"Consolidating {len(all_memories)} memories in namespace {namespace}"
            )

            # Find and remove duplicates
            duplicates = self._find_duplicate_memories(all_memories)
            for duplicate_group in duplicates:
                if not dry_run:
                    # Keep the most recent, delete others
                    for memory_id in duplicate_group[1:]:
                        await self.delete_memory(memory_id)
                result.duplicates_removed += len(duplicate_group) - 1

            # Find expired memories
            expired_memories = []
            for memory in all_memories:
                metadata = memory.get("metadata", {})
                importance_score = metadata.get("importance_score", 0.5)
                created_at = datetime.fromisoformat(
                    metadata.get("created_at", datetime.utcnow().isoformat())
                )

                # Calculate if memory is expired
                if max_age_hours:
                    age_hours = (datetime.utcnow() - created_at).total_seconds() / 3600
                    if age_hours > max_age_hours and importance_score < 0.3:
                        expired_memories.append(memory)
                else:
                    # Use decay calculation
                    decay_rate = metadata.get("decay_rate", 0.1)
                    current_weight = self._calculate_current_weight(
                        created_at, importance_score, decay_rate
                    )
                    if current_weight < 0.05:  # Expired threshold
                        expired_memories.append(memory)

            # Remove expired memories
            for memory in expired_memories:
                if not dry_run:
                    await self.delete_memory(memory["id"])
                result.expired_removed += 1

            # Calculate efficiency gain
            total_memories = len(all_memories)
            if total_memories > 0:
                result.storage_efficiency_gain = (
                    result.duplicates_removed + result.expired_removed
                ) / total_memories

            processing_time = (datetime.utcnow() - start_time).total_seconds()
            result.processing_time = processing_time
            result.summary = f"Consolidation complete: {result.duplicates_removed} duplicates removed, {result.expired_removed} expired memories removed"

            if not dry_run:
                self._last_consolidation = datetime.utcnow()

            logger.info(result.summary)
            return result

        except Exception as e:
            logger.exception(f"Error during memory consolidation: {e}")
            result.errors_encountered.append(str(e))
            return result

    async def get_memory_statistics(
        self, namespace: tuple[str, ...] | None = None
    ) -> dict[str, Any]:
        """Get statistics about stored memories.

        Args:
            namespace: Namespace to analyze (if None, analyze all)

        Returns:
            Dictionary with memory statistics
        """
        try:
            namespace = namespace or self.config.default_namespace

            # Get all memories
            all_memories = self.store_manager.search_memories(
                query="", namespace=namespace, limit=10000
            )

            # Analyze memories
            stats = {
                "total_memories": len(all_memories),
                "memory_types": {},
                "importance_distribution": {},
                "age_distribution": {},
                "average_importance": 0.0,
                "most_accessed": None,
                "oldest_memory": None,
                "newest_memory": None,
            }

            if not all_memories:
                return stats

            importance_scores = []
            oldest_date = datetime.utcnow()
            newest_date = datetime.min
            max_access_count = 0
            most_accessed_memory = None

            for memory in all_memories:
                metadata = memory.get("metadata", {})

                # Memory types
                memory_types = metadata.get("memory_types", [])
                for mt in memory_types:
                    stats["memory_types"][mt] = stats["memory_types"].get(mt, 0) + 1

                # Importance
                importance = metadata.get("importance", "medium")
                stats["importance_distribution"][importance] = (
                    stats["importance_distribution"].get(importance, 0) + 1
                )

                importance_score = metadata.get("importance_score", 0.5)
                importance_scores.append(importance_score)

                # Access tracking
                access_count = metadata.get("access_count", 0)
                if access_count > max_access_count:
                    max_access_count = access_count
                    most_accessed_memory = memory["id"]

                # Age analysis
                created_at = datetime.fromisoformat(
                    metadata.get("created_at", datetime.utcnow().isoformat())
                )
                if created_at < oldest_date:
                    oldest_date = created_at
                    stats["oldest_memory"] = memory["id"]
                if created_at > newest_date:
                    newest_date = created_at
                    stats["newest_memory"] = memory["id"]

            # Calculate averages
            if importance_scores:
                stats["average_importance"] = sum(importance_scores) / len(
                    importance_scores
                )

            stats["most_accessed"] = most_accessed_memory

            return stats

        except Exception as e:
            logger.exception(f"Error getting memory statistics: {e}")
            return {}

    def _should_consolidate(self) -> bool:
        """Check if memory consolidation should be triggered."""
        time_since_consolidation = datetime.utcnow() - self._last_consolidation
        return time_since_consolidation.total_seconds() > (
            self.config.consolidation_interval_hours * 3600
        )

    async def _schedule_consolidation(self, namespace: tuple[str, ...]) -> None:
        """Schedule background memory consolidation."""
        try:
            # In a production system, this would trigger a background task
            # For now, we'll just log that consolidation is needed
            logger.info(f"Memory consolidation scheduled for namespace {namespace}")

            # Could trigger consolidation in background:
            # await self.consolidate_memories(namespace=namespace)

        except Exception as e:
            logger.exception(f"Error scheduling consolidation: {e}")

    async def _update_access_metadata(self, memory_id: str) -> None:
        """Update access metadata for a memory."""
        try:
            self.store_manager.update_memory(
                memory_id=memory_id,
                metadata={
                    "last_accessed": datetime.utcnow().isoformat(),
                    "access_count": "increment",  # Special value to increment
                },
            )
        except Exception as e:
            logger.exception(f"Error updating access metadata for {memory_id}: {e}")

    def _calculate_ranking_score(
        self, memory: dict[str, Any], query_intent: MemoryQueryIntent | None = None
    ) -> float:
        """Calculate ranking score for memory retrieval."""
        metadata = memory.get("metadata", {})
        base_score = memory.get("similarity_score", 0.5)  # From search

        # Boost based on importance
        importance_score = metadata.get("importance_score", 0.5)
        importance_boost = importance_score * self.config.importance_boost

        # Boost based on access frequency
        access_count = metadata.get("access_count", 0)
        frequency_boost = min(0.1, access_count / 100.0)  # Cap at 0.1

        # Boost based on recency
        created_at = datetime.fromisoformat(
            metadata.get("created_at", datetime.utcnow().isoformat())
        )
        last_accessed = datetime.fromisoformat(
            metadata.get("last_accessed", datetime.utcnow().isoformat())
        )

        recency_boost = self._calculate_recency_boost(created_at, last_accessed)

        # Boost based on memory type match
        type_boost = 0.0
        if query_intent:
            memory_types = [MemoryType(mt) for mt in metadata.get("memory_types", [])]
            if any(mt in query_intent.memory_types for mt in memory_types):
                type_boost = 0.15

        # Calculate current weight (decay)
        decay_rate = metadata.get("decay_rate", 0.1)
        current_weight = self._calculate_current_weight(
            created_at, importance_score, decay_rate
        )

        # Combine all factors
        final_score = (
            base_score + importance_boost + frequency_boost + recency_boost + type_boost
        ) * current_weight

        return min(1.0, final_score)

    def _calculate_recency_boost(
        self, created_at: datetime, last_accessed: datetime
    ) -> float:
        """Calculate recency boost for ranking."""
        now = datetime.utcnow()

        # Boost for recent access
        hours_since_access = (now - last_accessed).total_seconds() / 3600
        access_boost = max(
            0.0, 0.1 - (hours_since_access / 1000)
        )  # Decay over ~1000 hours

        # Boost for recent creation
        hours_since_creation = (now - created_at).total_seconds() / 3600
        creation_boost = max(
            0.0, 0.05 - (hours_since_creation / 5000)
        )  # Decay over ~5000 hours

        return access_boost + creation_boost

    def _calculate_current_weight(
        self, created_at: datetime, importance_score: float, decay_rate: float
    ) -> float:
        """Calculate current weight based on age and decay."""
        time_since_creation = (
            datetime.utcnow() - created_at
        ).total_seconds() / 3600  # hours

        # Exponential decay based on importance and time
        decay_factor = max(0.0, 1.0 - (time_since_creation * decay_rate / 1000))

        # Weight by importance (higher importance decays slower)
        importance_factor = 0.5 + (importance_score * 0.5)

        return max(0.0, min(1.0, decay_factor * importance_factor))

    def _find_duplicate_memories(
        self, memories: list[dict[str, Any]]
    ) -> list[list[str]]:
        """Find groups of duplicate memories based on content similarity."""
        duplicates = []
        processed_ids = set()

        for i, memory1 in enumerate(memories):
            if memory1["id"] in processed_ids:
                continue

            duplicate_group = [memory1["id"]]
            content1 = memory1.get("content", "").lower().strip()

            for _j, memory2 in enumerate(memories[i + 1 :], i + 1):
                if memory2["id"] in processed_ids:
                    continue

                content2 = memory2.get("content", "").lower().strip()

                # Simple similarity check (could be enhanced with more sophisticated algorithms)
                if self._are_contents_similar(content1, content2):
                    duplicate_group.append(memory2["id"])
                    processed_ids.add(memory2["id"])

            if len(duplicate_group) > 1:
                duplicates.append(duplicate_group)
                processed_ids.update(duplicate_group)

        return duplicates

    def _are_contents_similar(
        self, content1: str, content2: str, threshold: float = 0.8
    ) -> bool:
        """Check if two memory contents are similar enough to be considered duplicates."""
        # Simple similarity based on common words
        words1 = set(content1.split())
        words2 = set(content2.split())

        if not words1 or not words2:
            return content1 == content2

        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))

        similarity = intersection / union if union > 0 else 0.0
        return similarity >= threshold
