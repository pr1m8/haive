"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    RAGAnswer: RAGAnswer implementation.
"""

#!/usr/bin/env python3
"""Answer generator models for SimpleRAG."""


from pydantic import BaseModel, Field


class RAGAnswer(BaseModel):
    """Structured output model for RAG answer generation."""

    answer: str = Field(
        ..., min_length=1, description="Generated answer based on retrieved context"
    )

    sources: list[str] = Field(
        default_factory=list, description="List of source references used in the answer"
    )

    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence score for the answer quality (0.0=low, 1.0=high)",
    )

    reasoning: str = Field(
        default="",
        description="Brief explanation of how the answer was derived from the context",
    )


__all__ = ["RAGAnswer"]
