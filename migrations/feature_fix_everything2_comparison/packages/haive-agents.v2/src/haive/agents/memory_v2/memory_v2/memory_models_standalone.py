"""Standalone memory models to avoid broken imports."""

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class MemoryType(str, Enum):
    """Types of memory."""

    SEMANTIC = "semantic"
    EPISODIC = "episodic"
    PROCEDURAL = "procedural"
    CONVERSATIONAL = "conversational"
    FACTUAL = "factual"


class ImportanceLevel(str, Enum):
    """Importance levels for memory prioritization."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class MemoryItem(BaseModel):
    """Individual memory item."""

    content: str
    memory_type: MemoryType = MemoryType.SEMANTIC
    timestamp: datetime = Field(default_factory=datetime.now)
    importance: float = Field(default=0.5, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeTriple(BaseModel):
    """Knowledge graph triple."""

    subject: str
    predicate: str
    object: str
    confidence: float = Field(default=1.0, ge=0.0, le=1.0)
    metadata: dict[str, Any] = Field(default_factory=dict)


class EnhancedMemoryItem(MemoryItem):
    """Enhanced memory item with V2 features."""

    id: str = Field(default_factory=lambda: str(datetime.now().timestamp()))
    tags: list[str] = Field(default_factory=list)
    embedding: list[float] | None = None
    source: str | None = None
    user_id: str | None = None
    access_count: int = 0
    last_accessed: datetime | None = None
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)
    created_at: datetime = Field(default_factory=datetime.now)
    relevance_scores: dict[str, float] = Field(default_factory=dict)
    vector_id: str | None = None

    # Override importance to use ImportanceLevel enum
    importance: ImportanceLevel = Field(default=ImportanceLevel.MEDIUM)
