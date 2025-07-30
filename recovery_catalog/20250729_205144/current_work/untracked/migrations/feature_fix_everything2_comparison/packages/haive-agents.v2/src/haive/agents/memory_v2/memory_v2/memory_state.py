"""Memory state models for Memory V2 system using original Haive memory models.

This module integrates the proven memory models from haive.agents.memory.models
and haive.agents.ltm.memory_schemas with our V2 enhancements for token tracking,
graph integration, and advanced memory management.
"""

import logging
from typing import Any

from pydantic import BaseModel, Field

# Import original proven memory models

logger = logging.getLogger(__name__)


class MemoryMetadata(BaseModel):
    """Metadata for a single memory entry.

    Tracks essential information about stored memories including
    type classification, importance, timestamps, and source information.

    Attributes:
        memory_type: Type of memory (semantic, episodic, procedural)
        importance: Importance level (critical, high, medium, low, transient)
        confidence: Confidence score for the memory (0.0-1.0)
        timestamp: When the memory was created
        source: Source of the memory (user_input, agent_inference, system)
        tags: List of tags for categorization
        entities: Named entities mentioned in the memory
        relationships: Relationships extracted from the memory
        context_id: ID linking related memories
        retrieval_count: How many times this memory has been retrieved
        last_accessed: When the memory was last accessed
    """

    memory_type: str = Field(
        default="semantic",
        description="Type of memory: semantic, episodic, procedural",
        pattern="^(semantic|episodic|procedural|contextual|preference|meta|emotional|temporal|error|feedback|system)$",
    )

    importance: str = Field(
        default="medium",
        description="Importance level: critical, high, medium, low, transient",
        pattern="^(critical|high|medium|low|transient)$",
    )

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score for the memory accuracy",
    )

    timestamp: str | None = Field(
        default=None, description="ISO timestamp when memory was created"
    )

    source: str = Field(
        default="user_input",
        description="Source of the memory",
        pattern="^(user_input|agent_inference|system|reflection|improvement)$",
    )

    tags: list[str] = Field(
        default_factory=list, description="Tags for categorization and search"
    )

    entities: list[str] = Field(
        default_factory=list, description="Named entities extracted from the memory"
    )

    relationships: list[dict[str, str]] = Field(
        default_factory=list,
        description="Relationships in format [{'subject': 'A', 'predicate': 'relates_to', 'object': 'B'}]",
    )

    context_id: str | None = Field(
        default=None, description="ID linking related memories in the same context"
    )

    retrieval_count: int = Field(
        default=0, ge=0, description="Number of times this memory has been retrieved"
    )

    last_accessed: str | None = Field(
        default=None, description="ISO timestamp when memory was last accessed"
    )


class MemoryEntry(BaseModel):
    """A single memory entry with content and metadata.

    Represents a complete memory item that can be stored, retrieved,
    and analyzed by memory agents.

    Attributes:
        id: Unique identifier for the memory
        content: The actual memory content
        metadata: Structured metadata about the memory
        embedding: Optional vector embedding for similarity search
        similarity_score: Similarity score when retrieved (populated during retrieval)
    """

    id: str = Field(..., description="Unique identifier for the memory")

    content: str = Field(..., min_length=1, description="The actual memory content")

    metadata: MemoryMetadata = Field(
        default_factory=MemoryMetadata,
        description="Structured metadata about the memory",
    )

    embedding: list[float] | None = Field(
        default=None, description="Vector embedding for similarity search"
    )

    similarity_score: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Similarity score when retrieved (populated during retrieval)",
    )


class MemoryStats(BaseModel):
    """Statistics about memory operations and performance.

    Tracks memory system performance, usage patterns, and optimization metrics.
    """

    total_memories: int = Field(default=0, ge=0)
    memories_by_type: dict[str, int] = Field(default_factory=dict)
    memories_by_importance: dict[str, int] = Field(default_factory=dict)

    # Performance metrics
    avg_storage_time: float = Field(default=0.0, ge=0.0)
    avg_retrieval_time: float = Field(default=0.0, ge=0.0)
    avg_search_time: float = Field(default=0.0, ge=0.0)

    # Usage metrics
    total_retrievals: int = Field(default=0, ge=0)
    total_searches: int = Field(default=0, ge=0)
    cache_hit_rate: float = Field(default=0.0, ge=0.0, le=1.0)

    # Token usage
    total_tokens_used: int = Field(default=0, ge=0)
    tokens_for_storage: int = Field(default=0, ge=0)
    tokens_for_retrieval: int = Field(default=0, ge=0)
    tokens_for_classification: int = Field(default=0, ge=0)


class MemoryState(MessagesState):
    """State schema for memory agent operations.

    Extends MessagesState with memory-specific fields for tracking
    current memories, metadata, statistics, and operation results.

    This state schema is used by all memory agents to maintain
    consistent state management and enable proper coordination
    between different memory strategies.

    Attributes:
        current_memories: List of memory entries currently being processed
        retrieved_memories: List of memories retrieved in the last operation
        memory_metadata: General metadata about the memory session
        memory_stats: Performance and usage statistics
        token_usage: Token usage tracking for memory operations
        last_operation: Information about the last memory operation performed
        memory_context: Context information for memory operations
        active_filters: Currently active filters for memory search/retrieval
    """

    # Core memory data
    current_memories: list[MemoryEntry] = Field(
        default_factory=list, description="Memory entries currently being processed"
    )

    retrieved_memories: list[MemoryEntry] = Field(
        default_factory=list, description="Memories retrieved in the last operation"
    )

    # Metadata and tracking
    memory_metadata: dict[str, Any] = Field(
        default_factory=dict, description="General metadata about the memory session"
    )

    memory_stats: MemoryStats = Field(
        default_factory=MemoryStats, description="Performance and usage statistics"
    )

    token_usage: dict[str, Any] = Field(
        default_factory=dict, description="Token usage tracking for memory operations"
    )

    # Operation tracking
    last_operation: dict[str, Any] = Field(
        default_factory=dict,
        description="Information about the last memory operation performed",
    )

    memory_context: dict[str, Any] = Field(
        default_factory=dict, description="Context information for memory operations"
    )

    # Search and filtering
    active_filters: dict[str, Any] = Field(
        default_factory=dict,
        description="Currently active filters for memory search/retrieval",
    )

    # Memory management
    memory_storage_path: str | None = Field(
        default=None, description="Path to persistent memory storage"
    )

    memory_cache: dict[str, Any] = Field(
        default_factory=dict,
        description="In-memory cache for frequently accessed memories",
    )

    def add_memory(self, memory: MemoryEntry) -> None:
        """Add a memory entry to current memories."""
        self.current_memories.append(memory)
        self.memory_stats.total_memories += 1

        # Update statistics
        memory_type = memory.metadata.memory_type
        if memory_type in self.memory_stats.memories_by_type:
            self.memory_stats.memories_by_type[memory_type] += 1
        else:
            self.memory_stats.memories_by_type[memory_type] = 1

        importance = memory.metadata.importance
        if importance in self.memory_stats.memories_by_importance:
            self.memory_stats.memories_by_importance[importance] += 1
        else:
            self.memory_stats.memories_by_importance[importance] = 1

    def update_retrieval_stats(
        self, memories: list[MemoryEntry], retrieval_time: float
    ) -> None:
        """Update statistics after memory retrieval."""
        self.retrieved_memories = memories
        self.memory_stats.total_retrievals += 1

        # Update average retrieval time
        total_time = (
            self.memory_stats.avg_retrieval_time
            * (self.memory_stats.total_retrievals - 1)
            + retrieval_time
        )
        self.memory_stats.avg_retrieval_time = (
            total_time / self.memory_stats.total_retrievals
        )

        # Update retrieval counts for individual memories
        for memory in memories:
            memory.metadata.retrieval_count += 1

    def get_memory_summary(self) -> dict[str, Any]:
        """Get a comprehensive summary of the current memory state."""
        return {
            "total_memories": len(self.current_memories),
            "retrieved_count": len(self.retrieved_memories),
            "memory_types": dict(self.memory_stats.memories_by_type),
            "importance_levels": dict(self.memory_stats.memories_by_importance),
            "performance": {
                "avg_storage_time": self.memory_stats.avg_storage_time,
                "avg_retrieval_time": self.memory_stats.avg_retrieval_time,
                "total_retrievals": self.memory_stats.total_retrievals,
                "cache_hit_rate": self.memory_stats.cache_hit_rate,
            },
            "token_usage": self.token_usage,
            "last_operation": self.last_operation,
        }
