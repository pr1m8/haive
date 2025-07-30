"""Memory type definitions and core data structures.

This module defines the fundamental memory types, entry structures,
and metadata schemas used throughout the Haive memory system.
"""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Enhanced memory type classifications following cognitive science patterns."""

    # Core memory types
    SEMANTIC = "semantic"  # Facts, concepts, knowledge triples
    EPISODIC = "episodic"  # Specific events, conversations, temporal context
    PROCEDURAL = "procedural"  # How-to knowledge, workflows, patterns

    # Hidden/Advanced memory types
    CONTEXTUAL = "contextual"  # Relationship mappings, social graphs
    PREFERENCE = "preference"  # User patterns, choices, behavioral tendencies
    META = "meta"  # Memory about memory (self-awareness)
    EMOTIONAL = "emotional"  # Sentiment patterns, emotional context
    TEMPORAL = "temporal"  # Time-based patterns, recency weights

    # System memory types
    ERROR = "error"  # Error patterns and recovery strategies
    FEEDBACK = "feedback"  # User feedback and corrections
    SYSTEM = "system"  # System configuration and settings


class MemoryImportance(str, Enum):
    """Memory importance levels for retention and retrieval prioritization."""

    CRITICAL = "critical"  # Never forget (0.9-1.0)
    HIGH = "high"  # Important long-term (0.7-0.9)
    MEDIUM = "medium"  # Standard retention (0.4-0.7)
    LOW = "low"  # Short-term relevance (0.1-0.4)
    TRANSIENT = "transient"  # Temporary/disposable (0.0-0.1)


class MemoryEntry(BaseModel):
    """Enhanced memory entry with multi-modal classification and lifecycle management.

    This represents a single memory with all necessary metadata for
    classification, retrieval, and lifecycle management.
    """

    # Core content
    content: str = Field(..., description="Memory content")
    memory_types: list[MemoryType] = Field(
        ..., description="Memory type classifications"
    )
    importance: MemoryImportance = Field(
        default=MemoryImportance.MEDIUM, description="Memory importance level"
    )

    # Temporal metadata
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Creation timestamp"
    )
    last_accessed: datetime = Field(
        default_factory=datetime.utcnow, description="Last access timestamp"
    )
    access_count: int = Field(default=0, description="Number of times accessed")

    # Importance and decay
    importance_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Numerical importance (0.0-1.0)"
    )
    decay_rate: float = Field(
        default=0.1, ge=0.0, le=1.0, description="Rate of importance decay over time"
    )
    current_weight: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Current relevance weight"
    )

    # Contextual metadata
    entities: list[str] = Field(
        default_factory=list, description="Named entities mentioned"
    )
    relationships: list[dict[str, str]] = Field(
        default_factory=list, description="Entity relationships"
    )
    topics: list[str] = Field(default_factory=list, description="Key topics/themes")
    sentiment: float | None = Field(
        default=None, ge=-1.0, le=1.0, description="Sentiment score (-1 to 1)"
    )

    # Conversational context
    conversation_id: str | None = Field(
        default=None, description="Source conversation ID"
    )
    user_context: dict[str, Any] = Field(
        default_factory=dict, description="User-specific context"
    )
    session_context: dict[str, Any] = Field(
        default_factory=dict, description="Session-specific context"
    )

    # Quality metadata
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Confidence in memory accuracy"
    )
    source_quality: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Quality of information source"
    )
    validation_status: str = Field(
        default="unverified", description="Validation status"
    )

    # System metadata
    namespace: str | None = Field(
        default=None, description="Memory namespace for organization"
    )
    tags: list[str] = Field(default_factory=list, description="User-defined tags")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    def update_access(self) -> None:
        """Update access metadata when memory is retrieved."""
        self.last_accessed = datetime.utcnow()
        self.access_count += 1

    def calculate_current_weight(self) -> float:
        """Calculate current relevance weight based on age and decay."""
        time_since_creation = (
            datetime.utcnow() - self.created_at
        ).total_seconds() / 3600  # hours
        time_since_access = (
            datetime.utcnow() - self.last_accessed
        ).total_seconds() / 3600  # hours

        # Combine creation age, access recency, and importance
        creation_factor = max(0.0, 1.0 - (time_since_creation * self.decay_rate / 1000))
        access_factor = max(0.0, 1.0 - (time_since_access * self.decay_rate / 100))

        # Weight by importance and access frequency
        importance_factor = self.importance_score
        frequency_factor = min(1.0, self.access_count / 10.0)  # Normalize access count

        # Combine all factors
        weight = (
            creation_factor * 0.3
            + access_factor * 0.3
            + importance_factor * 0.3
            + frequency_factor * 0.1
        )

        self.current_weight = max(0.0, min(1.0, weight))
        return self.current_weight

    def is_expired(self, expiration_threshold: float = 0.05) -> bool:
        """Check if memory should be considered expired."""
        current_weight = self.calculate_current_weight()
        return current_weight < expiration_threshold

    def add_relationship(self, subject: str, predicate: str, object: str) -> None:
        """Add an entity relationship to this memory."""
        relationship = {"subject": subject, "predicate": predicate, "object": object}
        if relationship not in self.relationships:
            self.relationships.append(relationship)


class MemoryClassificationResult(BaseModel):
    """Result of memory classification analysis."""

    memory_types: list[MemoryType] = Field(..., description="Identified memory types")
    importance: MemoryImportance = Field(..., description="Assessed importance level")
    importance_score: float = Field(
        ..., ge=0.0, le=1.0, description="Numerical importance score"
    )

    # Extracted metadata
    entities: list[str] = Field(default_factory=list, description="Extracted entities")
    topics: list[str] = Field(default_factory=list, description="Identified topics")
    sentiment: float | None = Field(
        default=None, description="Sentiment analysis result"
    )

    # Classification confidence
    confidence: float = Field(
        default=1.0, ge=0.0, le=1.0, description="Classification confidence"
    )
    reasoning: str = Field(
        default="", description="Explanation of classification logic"
    )


class MemoryQueryIntent(BaseModel):
    """Analysis of user query intent for memory retrieval."""

    memory_types: list[MemoryType] = Field(..., description="Required memory types")
    complexity: str = Field(
        default="simple", description="Query complexity: simple, moderate, complex"
    )
    temporal_scope: str = Field(
        default="recent", description="Time scope: recent, historical, all"
    )
    requires_reasoning: bool = Field(
        default=False, description="Whether complex reasoning is needed"
    )

    # Extracted query elements
    entities: list[str] = Field(
        default_factory=list, description="Entities mentioned in query"
    )
    topics: list[str] = Field(
        default_factory=list, description="Topics mentioned in query"
    )
    intent_keywords: list[str] = Field(
        default_factory=list, description="Intent-indicating keywords"
    )

    # Retrieval strategy hints
    preferred_retrieval_strategy: str = Field(
        default="semantic", description="Suggested retrieval approach"
    )
    max_results: int = Field(default=5, description="Suggested maximum results")
    confidence_threshold: float = Field(
        default=0.7, description="Minimum confidence for results"
    )


class MemoryConsolidationResult(BaseModel):
    """Result of memory consolidation process."""

    consolidated_count: int = Field(
        default=0, description="Number of memories consolidated"
    )
    duplicates_removed: int = Field(
        default=0, description="Number of duplicate memories removed"
    )
    memories_summarized: int = Field(
        default=0, description="Number of memories summarized"
    )
    expired_removed: int = Field(
        default=0, description="Number of expired memories removed"
    )

    # Quality metrics
    storage_efficiency_gain: float = Field(
        default=0.0, description="Storage space saved (0.0-1.0)"
    )
    retrieval_accuracy_change: float = Field(
        default=0.0, description="Change in retrieval accuracy"
    )

    # Processing details
    processing_time: float = Field(
        default=0.0, description="Consolidation processing time in seconds"
    )
    errors_encountered: list[str] = Field(
        default_factory=list, description="Any errors during consolidation"
    )
    summary: str = Field(default="", description="Human-readable consolidation summary")
