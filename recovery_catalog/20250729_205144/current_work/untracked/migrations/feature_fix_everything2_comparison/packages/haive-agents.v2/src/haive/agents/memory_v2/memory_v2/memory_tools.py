"""Memory tools for modular memory operations.

Provides separate tools for memory operations following proper Haive patterns.
Tools are designed to be used by memory agents and can be easily tested
and composed together.
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from langchain_core.tools import tool
from pydantic import BaseModel, Field, field_validator

from .memory_state_original import EnhancedMemoryItem as MemoryEntry


# Create MemoryMetadata as a simple class
class MemoryMetadata(BaseModel):
    memory_type: str = Field(default="general")
    importance: float = Field(default=0.5)
    tags: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)


class MemoryConfig(BaseModel):
    """Configuration for memory operations.

    Provides centralized configuration for memory storage, retrieval,
    and classification operations with proper validation.

    Attributes:
        storage_backend: Backend for memory storage (json_file, sqlite, neo4j, vector_db)
        storage_path: Path for file-based storage backends
        max_memories: Maximum number of memories to store (-1 for unlimited)
        memory_ttl: Time-to-live for memories in seconds (-1 for permanent)
        enable_embedding: Whether to generate embeddings for similarity search
        embedding_model: Model to use for embeddings
        similarity_threshold: Minimum similarity score for retrieval
        classification_enabled: Whether to automatically classify memories
        auto_cleanup: Whether to automatically clean up old/low-importance memories
        cache_size: Size of in-memory cache for frequently accessed memories
    """

    storage_backend: str = Field(
        default="json_file",
        description="Backend for memory storage",
        pattern="^(json_file|sqlite|neo4j|vector_db|in_memory)$",
    )

    storage_path: str | None = Field(
        default=None, description="Path for file-based storage backends"
    )

    max_memories: int = Field(
        default=-1, description="Maximum number of memories to store (-1 for unlimited)"
    )

    memory_ttl: int = Field(
        default=-1,
        description="Time-to-live for memories in seconds (-1 for permanent)",
    )

    enable_embedding: bool = Field(
        default=True, description="Whether to generate embeddings for similarity search"
    )

    embedding_model: str = Field(
        default="text-embedding-3-small", description="Model to use for embeddings"
    )

    similarity_threshold: float = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieval",
    )

    classification_enabled: bool = Field(
        default=True, description="Whether to automatically classify memories"
    )

    auto_cleanup: bool = Field(
        default=False,
        description="Whether to automatically clean up old/low-importance memories",
    )

    cache_size: int = Field(
        default=1000,
        ge=0,
        description="Size of in-memory cache for frequently accessed memories",
    )

    @field_validator("storage_path")
    @classmethod
    def validate_storage_path(cls, v, info):
        """Validate storage path based on backend."""
        if v is None and info.data.get("storage_backend") in ["json_file", "sqlite"]:
            return f"memory_storage.{info.data.get('storage_backend', 'json')}"
        return v


# Global memory storage for simple backends
_MEMORY_STORAGE: dict[str, list[MemoryEntry]] = {}
_MEMORY_CONFIG: MemoryConfig | None = None


def _get_storage_key(namespace: str = "default") -> str:
    """Get storage key for a namespace."""
    return f"memories_{namespace}"


def _load_memories_from_file(
    storage_path: str, namespace: str = "default"
) -> list[MemoryEntry]:
    """Load memories from JSON file."""
    try:
        path = Path(storage_path)
        if not path.exists():
            return []

        with open(path, encoding="utf-8") as f:
            data = json.load(f)

        namespace_data = data.get(namespace, [])
        return [MemoryEntry.model_validate(entry) for entry in namespace_data]
    except Exception as e:
        print(f"Error loading memories from file: {e}")
        return []


def _save_memories_to_file(
    memories: list[MemoryEntry], storage_path: str, namespace: str = "default"
) -> None:
    """Save memories to JSON file."""
    try:
        path = Path(storage_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing data
        data = {}
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)

        # Update namespace
        data[namespace] = [memory.model_dump() for memory in memories]

        # Save back
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving memories to file: {e}")


@tool
def store_memory(
    content: str,
    memory_type: str = "semantic",
    importance: str = "medium",
    tags: list[str] | None = None,
    context_id: str | None = None,
    namespace: str = "default",
    config: dict[str, Any] | None = None,
) -> str:
    """Store a memory with classification and metadata.

    Stores a memory entry with automatic classification, metadata extraction,
    and optional embedding generation for similarity search.

    Args:
        content: The memory content to store
        memory_type: Type of memory (semantic, episodic, procedural)
        importance: Importance level (critical, high, medium, low, transient)
        tags: Optional list of tags for categorization
        context_id: Optional ID to group related memories
        namespace: Namespace for memory organization
        config: Optional configuration override

    Returns:
        String indicating success and memory ID

    Examples:
        Basic usage::

            result = store_memory("I prefer coffee over tea", "semantic", "medium")
            # Returns: "Memory stored successfully with ID: uuid-string"

        With tags and context::

            result = store_memory(
                "Alice introduced herself as a researcher",
                memory_type="episodic",
                tags=["people", "introductions"],
                context_id="meeting_2024_01_15"
            )
    """
    global _MEMORY_STORAGE, _MEMORY_CONFIG

    try:
        # Initialize config if not set
        if _MEMORY_CONFIG is None:
            _MEMORY_CONFIG = MemoryConfig(**(config or {}))

        # Create memory entry
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        metadata = MemoryMetadata(
            memory_type=memory_type,
            importance=importance,
            confidence=0.8,  # Default confidence for user-provided memories
            timestamp=timestamp,
            source="user_input",
            tags=tags or [],
            context_id=context_id,
        )

        memory = MemoryEntry(id=memory_id, content=content, metadata=metadata)

        # Get storage key
        storage_key = _get_storage_key(namespace)

        # Handle different storage backends
        if _MEMORY_CONFIG.storage_backend == "json_file":
            # Load existing memories
            existing_memories = _load_memories_from_file(
                _MEMORY_CONFIG.storage_path, namespace
            )
            existing_memories.append(memory)

            # Apply memory limit if set
            if (
                _MEMORY_CONFIG.max_memories > 0
                and len(existing_memories) > _MEMORY_CONFIG.max_memories
            ):
                # Remove oldest memories
                existing_memories = existing_memories[-_MEMORY_CONFIG.max_memories :]

            # Save to file
            _save_memories_to_file(
                existing_memories, _MEMORY_CONFIG.storage_path, namespace
            )

        else:  # in_memory storage
            if storage_key not in _MEMORY_STORAGE:
                _MEMORY_STORAGE[storage_key] = []

            _MEMORY_STORAGE[storage_key].append(memory)

            # Apply memory limit if set
            if (
                _MEMORY_CONFIG.max_memories > 0
                and len(_MEMORY_STORAGE[storage_key]) > _MEMORY_CONFIG.max_memories
            ):
                _MEMORY_STORAGE[storage_key] = _MEMORY_STORAGE[storage_key][
                    -_MEMORY_CONFIG.max_memories :
                ]

        return f"Memory stored successfully with ID: {memory_id}"

    except Exception as e:
        return f"Error storing memory: {e!s}"


@tool
def retrieve_memory(
    query: str,
    memory_type: str | None = None,
    importance_filter: list[str] | None = None,
    limit: int = 5,
    namespace: str = "default",
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Retrieve memories based on query and filters.

    Searches for relevant memories using content similarity and metadata filters.
    Returns the most relevant memories sorted by relevance score.

    Args:
        query: Search query to find relevant memories
        memory_type: Filter by specific memory type
        importance_filter: Filter by importance levels
        limit: Maximum number of memories to return
        namespace: Namespace to search in
        config: Optional configuration override

    Returns:
        List of memory dictionaries with content, metadata, and similarity scores

    Examples:
        Basic retrieval::

            memories = retrieve_memory("coffee preferences")
            for memory in memories:
                print(f"Content: {memory['content']}")
                print(f"Score: {memory['similarity_score']}")

        Filtered retrieval::

            memories = retrieve_memory(
                "research work",
                memory_type="episodic",
                importance_filter=["high", "critical"]
            )
    """
    global _MEMORY_STORAGE, _MEMORY_CONFIG

    try:
        # Initialize config if not set
        if _MEMORY_CONFIG is None:
            _MEMORY_CONFIG = MemoryConfig(**(config or {}))

        # Get storage key
        storage_key = _get_storage_key(namespace)

        # Load memories based on backend
        if _MEMORY_CONFIG.storage_backend == "json_file":
            memories = _load_memories_from_file(_MEMORY_CONFIG.storage_path, namespace)
        else:  # in_memory storage
            memories = _MEMORY_STORAGE.get(storage_key, [])

        if not memories:
            return []

        # Apply filters
        filtered_memories = memories

        if memory_type:
            filtered_memories = [
                m for m in filtered_memories if m.metadata.memory_type == memory_type
            ]

        if importance_filter:
            filtered_memories = [
                m
                for m in filtered_memories
                if m.metadata.importance in importance_filter
            ]

        # Simple text-based similarity (in production, would use embeddings)
        query_lower = query.lower()
        results = []

        for memory in filtered_memories:
            content_lower = memory.content.lower()

            # Simple similarity scoring based on word overlap
            query_words = set(query_lower.split())
            content_words = set(content_lower.split())

            if query_words & content_words:  # If there's any word overlap
                overlap = len(query_words & content_words)
                total_words = len(query_words | content_words)
                similarity_score = overlap / total_words if total_words > 0 else 0.0

                # Boost score for exact phrase matches
                if query_lower in content_lower:
                    similarity_score += 0.3

                if similarity_score >= _MEMORY_CONFIG.similarity_threshold:
                    memory_dict = memory.model_dump()
                    memory_dict["similarity_score"] = min(similarity_score, 1.0)
                    results.append(memory_dict)

        # Sort by similarity score and limit results
        results.sort(key=lambda x: x["similarity_score"], reverse=True)
        return results[:limit]

    except Exception as e:
        return [{"error": f"Error retrieving memories: {e!s}"}]


@tool
def search_memory(
    query: str | None = None,
    filters: dict[str, Any] | None = None,
    sort_by: str = "timestamp",
    sort_order: str = "desc",
    limit: int = 10,
    namespace: str = "default",
    config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Search memories with flexible filtering and sorting options.

    Provides advanced search capabilities with multiple filter options
    and sorting criteria for comprehensive memory exploration.

    Args:
        query: Optional text query for content search
        filters: Dictionary of filters to apply
        sort_by: Field to sort by (timestamp, importance, retrieval_count)
        sort_order: Sort order (asc, desc)
        limit: Maximum number of results
        namespace: Namespace to search in
        config: Optional configuration override

    Returns:
        List of memory dictionaries matching the search criteria

    Examples:
        Search by filters::

            memories = search_memory(
                filters={
                    "memory_type": "semantic",
                    "importance": ["high", "critical"],
                    "tags": ["work", "projects"]
                }
            )

        Search with query and sorting::

            memories = search_memory(
                query="coffee",
                sort_by="retrieval_count",
                sort_order="desc"
            )
    """
    global _MEMORY_STORAGE, _MEMORY_CONFIG

    try:
        # Initialize config if not set
        if _MEMORY_CONFIG is None:
            _MEMORY_CONFIG = MemoryConfig(**(config or {}))

        # Get storage key
        storage_key = _get_storage_key(namespace)

        # Load memories based on backend
        if _MEMORY_CONFIG.storage_backend == "json_file":
            memories = _load_memories_from_file(_MEMORY_CONFIG.storage_path, namespace)
        else:  # in_memory storage
            memories = _MEMORY_STORAGE.get(storage_key, [])

        if not memories:
            return []

        results = memories.copy()

        # Apply text query if provided
        if query:
            query_lower = query.lower()
            filtered_results = []
            for memory in results:
                if query_lower in memory.content.lower() or any(
                    query_lower in tag.lower() for tag in memory.metadata.tags
                ):
                    filtered_results.append(memory)
            results = filtered_results

        # Apply filters
        if filters:
            for filter_key, filter_value in filters.items():
                if filter_key == "memory_type":
                    results = [
                        m for m in results if m.metadata.memory_type == filter_value
                    ]
                elif filter_key == "importance":
                    if isinstance(filter_value, list):
                        results = [
                            m for m in results if m.metadata.importance in filter_value
                        ]
                    else:
                        results = [
                            m for m in results if m.metadata.importance == filter_value
                        ]
                elif filter_key == "tags":
                    if isinstance(filter_value, list):
                        results = [
                            m
                            for m in results
                            if any(tag in m.metadata.tags for tag in filter_value)
                        ]
                    else:
                        results = [
                            m for m in results if filter_value in m.metadata.tags
                        ]
                elif filter_key == "context_id":
                    results = [
                        m for m in results if m.metadata.context_id == filter_value
                    ]
                elif filter_key == "source":
                    results = [m for m in results if m.metadata.source == filter_value]

        # Sort results
        reverse_order = sort_order.lower() == "desc"

        if sort_by == "timestamp":
            results.sort(
                key=lambda x: x.metadata.timestamp or "", reverse=reverse_order
            )
        elif sort_by == "importance":
            importance_order = {
                "critical": 5,
                "high": 4,
                "medium": 3,
                "low": 2,
                "transient": 1,
            }
            results.sort(
                key=lambda x: importance_order.get(x.metadata.importance, 0),
                reverse=reverse_order,
            )
        elif sort_by == "retrieval_count":
            results.sort(
                key=lambda x: x.metadata.retrieval_count, reverse=reverse_order
            )
        elif sort_by == "confidence":
            results.sort(key=lambda x: x.metadata.confidence, reverse=reverse_order)

        # Convert to dictionaries and limit results
        result_dicts = [memory.model_dump() for memory in results[:limit]]

        return result_dicts

    except Exception as e:
        return [{"error": f"Error searching memories: {e!s}"}]


@tool
def classify_memory(
    content: str, context: str | None = None, config: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Classify memory type and extract metadata.

    Analyzes memory content to automatically determine memory type,
    importance level, and extract relevant metadata like entities and tags.

    Args:
        content: Memory content to classify
        context: Optional context for better classification
        config: Optional configuration override

    Returns:
        Dictionary with classification results and extracted metadata

    Examples:
        Basic classification::

            result = classify_memory("I met Alice at the conference")
            print(result["memory_type"])  # "episodic"
            print(result["entities"])     # ["Alice"]

        With context::

            result = classify_memory(
                "The project deadline is next Friday",
                context="work meeting discussion"
            )
    """
    try:
        # Simple rule-based classification (in production, would use LLM)
        content_lower = content.lower()

        # Determine memory type
        memory_type = "semantic"  # default

        # Episodic indicators
        episodic_keywords = [
            "i met",
            "i talked to",
            "yesterday",
            "today",
            "last",
            "went to",
            "happened",
            "said",
            "told me",
            "we discussed",
            "meeting",
            "event",
        ]
        if any(key in content_lower for key in episodic_keywords):
            memory_type = "episodic"

        # Procedural indicators
        procedural_keywords = [
            "how to",
            "steps to",
            "process",
            "method",
            "procedure",
            "algorithm",
            "instructions",
            "workflow",
            "best practice",
        ]
        if any(key in content_lower for key in procedural_keywords):
            memory_type = "procedural"

        # Determine importance
        importance = "medium"  # default

        high_importance_keywords = [
            "important",
            "critical",
            "urgent",
            "deadline",
            "must",
            "required",
            "essential",
            "priority",
            "project",
            "work",
            "decision",
        ]
        if any(key in content_lower for key in high_importance_keywords):
            importance = "high"

        low_importance_keywords = [
            "maybe",
            "perhaps",
            "casual",
            "small talk",
            "weather",
            "minor",
        ]
        if any(key in content_lower for key in low_importance_keywords):
            importance = "low"

        # Extract simple entities (names - words that start with capital letters)
        words = content.split()
        entities = []
        for word in words:
            # Simple name detection - starts with capital, not at sentence start
            if word and word[0].isupper() and word.isalpha():
                # Check if it's not the first word or after punctuation
                word_index = words.index(word)
                if word_index > 0:
                    prev_word = words[word_index - 1]
                    if not prev_word.endswith((".", "!", "?")):
                        entities.append(word)

        # Generate tags from content
        common_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "is",
            "are",
            "was",
            "were",
            "be",
            "been",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "could",
            "should",
            "may",
            "might",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
            "me",
            "him",
            "her",
            "us",
            "them",
        }

        tags = []
        for word in words:
            clean_word = word.lower().strip(".,!?();:\"'")
            if (
                len(clean_word) > 3
                and clean_word not in common_words
                and clean_word.isalpha()
            ):
                tags.append(clean_word)

        # Remove duplicates and limit tags
        tags = list(set(tags))[:5]
        entities = list(set(entities))[:5]

        # Calculate confidence based on classification certainness
        confidence = 0.6  # base confidence
        if memory_type != "semantic":  # We had specific indicators
            confidence += 0.2
        if importance != "medium":  # We had specific indicators
            confidence += 0.1
        if entities:  # We found entities
            confidence += 0.1

        return {
            "memory_type": memory_type,
            "importance": importance,
            "confidence": min(confidence, 1.0),
            "entities": entities,
            "tags": tags,
            "source": "classification_tool",
            "classification_method": "rule_based",
        }

    except Exception as e:
        return {
            "error": f"Error classifying memory: {e!s}",
            "memory_type": "semantic",
            "importance": "medium",
            "confidence": 0.1,
            "entities": [],
            "tags": [],
        }


@tool
def get_memory_stats(
    namespace: str = "default", config: dict[str, Any] | None = None
) -> dict[str, Any]:
    """Get comprehensive statistics about stored memories.

    Provides detailed analytics about memory storage, including
    counts by type and importance, performance metrics, and usage patterns.

    Args:
        namespace: Namespace to analyze
        config: Optional configuration override

    Returns:
        Dictionary with comprehensive memory statistics

    Examples:
        Get basic stats::

            stats = get_memory_stats()
            print(f"Total memories: {stats['total_memories']}")
            print(f"Memory types: {stats['memory_types']}")
    """
    global _MEMORY_STORAGE, _MEMORY_CONFIG

    try:
        # Initialize config if not set
        if _MEMORY_CONFIG is None:
            _MEMORY_CONFIG = MemoryConfig(**(config or {}))

        # Get storage key
        storage_key = _get_storage_key(namespace)

        # Load memories based on backend
        if _MEMORY_CONFIG.storage_backend == "json_file":
            memories = _load_memories_from_file(_MEMORY_CONFIG.storage_path, namespace)
        else:  # in_memory storage
            memories = _MEMORY_STORAGE.get(storage_key, [])

        if not memories:
            return {
                "total_memories": 0,
                "memory_types": {},
                "importance_levels": {},
                "average_confidence": 0.0,
                "most_common_tags": [],
                "recent_memories": 0,
            }

        # Calculate statistics
        total_memories = len(memories)
        memory_types = {}
        importance_levels = {}
        confidences = []
        all_tags = []
        recent_count = 0

        # Current time for recency calculation
        current_time = datetime.now()

        for memory in memories:
            # Memory type counts
            mem_type = memory.metadata.memory_type
            memory_types[mem_type] = memory_types.get(mem_type, 0) + 1

            # Importance level counts
            importance = memory.metadata.importance
            importance_levels[importance] = importance_levels.get(importance, 0) + 1

            # Confidence scores
            confidences.append(memory.metadata.confidence)

            # Tags
            all_tags.extend(memory.metadata.tags)

            # Recent memories (last 24 hours)
            if memory.metadata.timestamp:
                try:
                    memory_time = datetime.fromisoformat(memory.metadata.timestamp)
                    if (current_time - memory_time).total_seconds() < 86400:  # 24 hours
                        recent_count += 1
                except:
                    pass  # Skip invalid timestamps

        # Calculate averages
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        # Most common tags
        from collections import Counter

        tag_counts = Counter(all_tags)
        most_common_tags = [
            {"tag": tag, "count": count} for tag, count in tag_counts.most_common(10)
        ]

        return {
            "total_memories": total_memories,
            "memory_types": memory_types,
            "importance_levels": importance_levels,
            "average_confidence": round(avg_confidence, 3),
            "most_common_tags": most_common_tags,
            "recent_memories": recent_count,
            "namespace": namespace,
            "storage_backend": _MEMORY_CONFIG.storage_backend,
            "storage_path": _MEMORY_CONFIG.storage_path,
        }

    except Exception as e:
        return {"error": f"Error getting memory stats: {e!s}"}
