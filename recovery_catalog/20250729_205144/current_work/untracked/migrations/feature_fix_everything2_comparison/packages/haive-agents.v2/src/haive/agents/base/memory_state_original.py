"""Memory state models for Memory V2 system using original Haive memory models.

This module integrates the proven memory models from haive.agents.memory.models and
haive.agents.ltm.memory_schemas with our V2 enhancements for token tracking, graph
integration, and advanced memory management.
"""

import logging
from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field

# Import original proven memory models
from .memory_models_standalone import (
    EnhancedMemoryItem,
    ImportanceLevel,
    KnowledgeTriple,
    MemoryItem,
)

# Commenting out broken imports
# from haive.agents.ltm.memory_schemas import (
#     Memory, UserPreference, FactualMemory, PersonalContext, ConversationalMemory,
#     DEFAULT_MEMORY_SCHEMAS, EXTENDED_MEMORY_SCHEMAS, MINIMAL_MEMORY_SCHEMAS
# )

logger = logging.getLogger(__name__)


# ============================================================================
# ENHANCED MEMORY TYPES (extending originals)
# ============================================================================


class MemoryType(str, Enum):
    """Memory types compatible with original models plus V2 enhancements."""

    # Original memory types (compatible with existing schemas)
    CONVERSATIONAL = "conversational"  # ConversationalMemory
    PREFERENCE = "preference"  # UserPreference
    FACTUAL = "factual"  # FactualMemory
    PERSONAL_CONTEXT = "personal_context"  # PersonalContext
    BASIC = "basic"  # Basic Memory schema

    # V2 Enhanced types
    EPISODIC = "episodic"  # Specific events and experiences
    SEMANTIC = "semantic"  # Facts and general knowledge
    PROCEDURAL = "procedural"  # Skills and procedures
    META = "meta"  # Memory about memory management
    SUMMARY = "summary"  # Compressed/summarized memories
    GRAPH_TRIPLE = "graph_triple"  # KnowledgeTriple memories


# ImportanceLevel is now imported from memory_models_standalone


# ============================================================================
# ENHANCED MEMORY MODELS (extending originals)
# ============================================================================

# EnhancedMemoryItem is now imported from memory_models_standalone

# Method commented out due to missing schema dependencies
# @classmethod
# def from_schema_memory(cls, schema_memory: BaseModel, memory_type: MemoryType) -> "EnhancedMemoryItem":
#     """Create EnhancedMemoryItem from original schema memory."""
#     pass


class EnhancedKnowledgeTriple(KnowledgeTriple):
    """Enhanced KnowledgeTriple with V2 capabilities."""

    # V2 enhancements
    id: str = Field(default_factory=lambda: str(uuid4()))
    importance: ImportanceLevel = Field(default=ImportanceLevel.MEDIUM)
    created_at: datetime = Field(default_factory=datetime.now)

    # Enhanced graph fields
    supporting_evidence: str | None = Field(default=None)
    context: str | None = Field(default=None)

    # Retrieval tracking
    access_count: int = Field(default=0)
    last_accessed: datetime | None = Field(default=None)


# ============================================================================
# UNIFIED MEMORY ENTRY (combining both models)
# ============================================================================


class UnifiedMemoryEntry(BaseModel):
    """Unified memory entry that can hold both MemoryItem and KnowledgeTriple data."""

    # Core identification
    id: str = Field(default_factory=lambda: str(uuid4()))
    entry_type: str = Field(...)  # "memory_item" or "knowledge_triple"

    # Memory item fields (when entry_type == "memory_item")
    memory_item: EnhancedMemoryItem | None = Field(default=None)

    # Knowledge triple fields (when entry_type == "knowledge_triple")
    knowledge_triple: EnhancedKnowledgeTriple | None = Field(default=None)

    # Common V2 fields
    memory_type: MemoryType = Field(default=MemoryType.CONVERSATIONAL)
    importance: ImportanceLevel = Field(default=ImportanceLevel.MEDIUM)
    created_at: datetime = Field(default_factory=datetime.now)

    @property
    def content(self) -> str:
        """Get content regardless of entry type."""
        if self.entry_type == "memory_item" and self.memory_item:
            return self.memory_item.content
        if self.entry_type == "knowledge_triple" and self.knowledge_triple:
            return f"{self.knowledge_triple.subject} {self.knowledge_triple.predicate} {self.knowledge_triple.object}"
        return ""

    @classmethod
    def from_memory_item(cls, memory_item: EnhancedMemoryItem) -> "UnifiedMemoryEntry":
        """Create from memory item."""
        return cls(
            entry_type="memory_item",
            memory_item=memory_item,
            memory_type=memory_item.memory_type,
            importance=memory_item.importance,
        )

    @classmethod
    def from_knowledge_triple(
        cls, triple: EnhancedKnowledgeTriple
    ) -> "UnifiedMemoryEntry":
        """Create from knowledge triple."""
        return cls(
            entry_type="knowledge_triple",
            knowledge_triple=triple,
            memory_type=MemoryType.GRAPH_TRIPLE,
            importance=triple.importance,
        )


# ============================================================================
# MEMORY STATS AND STATE
# ============================================================================


class MemoryStats(BaseModel):
    """Statistics about memory usage and performance."""

    total_memories: int = Field(default=0)
    total_memory_items: int = Field(default=0)
    total_knowledge_triples: int = Field(default=0)

    memories_by_type: dict[MemoryType, int] = Field(default_factory=dict)
    memories_by_importance: dict[ImportanceLevel, int] = Field(default_factory=dict)

    # Usage stats
    total_retrievals: int = Field(default=0)
    total_operations: int = Field(default=0)
    average_relevance_score: float = Field(default=0.0)

    # Performance stats
    last_update: datetime = Field(default_factory=datetime.now)
    processing_times: dict[str, float] = Field(default_factory=dict)


class MemoryState(BaseModel):
    """Memory state using original models with V2 enhancements."""

    # Core memory storage using unified entries
    memories: list[UnifiedMemoryEntry] = Field(default_factory=list)

    # Organizational fields
    user_id: str | None = Field(default=None)
    session_id: str | None = Field(default=None)

    # Stats and metadata
    stats: MemoryStats = Field(default_factory=MemoryStats)

    # Schema support
    supported_schemas: list[type] = Field(default_factory=list)

    # Configuration
    max_memories: int = Field(default=1000)
    auto_cleanup: bool = Field(default=True)

    def add_memory_item(self, memory_item: EnhancedMemoryItem) -> None:
        """Add a memory item to the state."""
        entry = UnifiedMemoryEntry.from_memory_item(memory_item)
        self.memories.append(entry)
        self._update_stats()

    def add_knowledge_triple(self, triple: EnhancedKnowledgeTriple) -> None:
        """Add a knowledge triple to the state."""
        entry = UnifiedMemoryEntry.from_knowledge_triple(triple)
        self.memories.append(entry)
        self._update_stats()

    def add_schema_memory(
        self, schema_memory: BaseModel, memory_type: MemoryType
    ) -> None:
        """Add memory from original schema."""
        enhanced_memory = EnhancedMemoryItem.from_schema_memory(
            schema_memory, memory_type
        )
        self.add_memory_item(enhanced_memory)

    def get_memory_items(self) -> list[EnhancedMemoryItem]:
        """Get all memory items."""
        return [
            entry.memory_item
            for entry in self.memories
            if entry.entry_type == "memory_item" and entry.memory_item
        ]

    def get_knowledge_triples(self) -> list[EnhancedKnowledgeTriple]:
        """Get all knowledge triples."""
        return [
            entry.knowledge_triple
            for entry in self.memories
            if entry.entry_type == "knowledge_triple" and entry.knowledge_triple
        ]

    def get_memories_by_type(self, memory_type: MemoryType) -> list[UnifiedMemoryEntry]:
        """Get memories of specific type."""
        return [m for m in self.memories if m.memory_type == memory_type]

    def search_memories(self, query: str, limit: int = 10) -> list[UnifiedMemoryEntry]:
        """Simple text-based memory search."""
        results = []
        query_lower = query.lower()

        for memory in self.memories:
            if query_lower in memory.content.lower():
                results.append(memory)

            if len(results) >= limit:
                break

        return results

    def _update_stats(self) -> None:
        """Update memory statistics."""
        self.stats.total_memories = len(self.memories)
        self.stats.total_memory_items = len(
            [m for m in self.memories if m.entry_type == "memory_item"]
        )
        self.stats.total_knowledge_triples = len(
            [m for m in self.memories if m.entry_type == "knowledge_triple"]
        )

        # Count by type
        type_counts = {}
        importance_counts = {}

        for memory in self.memories:
            # Type counts
            mem_type = memory.memory_type
            type_counts[mem_type] = type_counts.get(mem_type, 0) + 1

            # Importance counts
            importance = memory.importance
            importance_counts[importance] = importance_counts.get(importance, 0) + 1

        self.stats.memories_by_type = type_counts
        self.stats.memories_by_importance = importance_counts
        self.stats.last_update = datetime.now()


# ============================================================================
# COMPATIBILITY EXPORTS
# ============================================================================

# Export original models for compatibility
__all__ = [
    # Original models
    "MemoryItem",
    "KnowledgeTriple",
    # Commented out undefined models: "Memory", "UserPreference", "FactualMemory", "PersonalContext", "ConversationalMemory",
    # Enhanced V2 models
    "EnhancedMemoryItem",
    "EnhancedKnowledgeTriple",
    "UnifiedMemoryEntry",
    # V2 infrastructure
    "MemoryType",
    "ImportanceLevel",
    "MemoryStats",
    "MemoryState",
    # Schema collections removed as they're undefined
    # "DEFAULT_MEMORY_SCHEMAS", "EXTENDED_MEMORY_SCHEMAS", "MINIMAL_MEMORY_SCHEMAS"
]
