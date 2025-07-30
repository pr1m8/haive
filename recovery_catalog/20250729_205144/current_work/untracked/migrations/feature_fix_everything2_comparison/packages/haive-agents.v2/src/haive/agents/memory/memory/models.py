"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    MemoryItem: MemoryItem implementation.
    for: for implementation.
    KnowledgeTriple: KnowledgeTriple implementation.
"""

from typing import Any

from pydantic import BaseModel, Field


class MemoryItem(BaseModel):
    """Base memory item class for structured and unstructured memories."""

    content: str
    source: str = Field(default="conversation")
    timestamp: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class KnowledgeTriple(BaseModel):
    """Structured knowledge triple for graph-based memory."""

    subject: str
    predicate: str
    object_: str
    confidence: float = Field(default=1.0)
    source: str = Field(default="conversation")
    timestamp: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
