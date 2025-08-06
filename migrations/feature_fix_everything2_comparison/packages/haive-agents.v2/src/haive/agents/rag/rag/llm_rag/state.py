"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    LLMRAGInputState: LLMRAGInputState implementation.
    LLMRAGOutputState: LLMRAGOutputState implementation.
    LLMRAGState: LLMRAGState implementation.
"""

from __future__ import annotations

from haive.agents.rag.base.state import BaseRAGInputState
from haive.agents.rag.base.state import BaseRAGOutputState
from haive.agents.rag.base.state import BaseRAGState
from pydantic import Field


class LLMRAGInputState(BaseRAGInputState):
    """Input state for LLM RAG agents."""


class LLMRAGOutputState(BaseRAGOutputState):
    """Output state for LLM RAG agents."""

    answer: str = Field(
        default="",
        description="The generated answer based on retrieved documents",
    )
    is_relevant: bool = Field(
        default=False,
        description="Whether the retrieved documents are relevant to the query",
    )


class LLMRAGState(BaseRAGState, LLMRAGOutputState):
    """State for LLM RAG agents."""
