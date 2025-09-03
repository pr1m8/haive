"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    BaseRAGInputState: BaseRAGInputState implementation.
    BaseRAGOutputState: BaseRAGOutputState implementation.
    BaseRAGState: BaseRAGState implementation.
"""

from __future__ import annotations

from langchain.schema import Document
from pydantic import BaseModel
from pydantic import Field


class BaseRAGInputState(BaseModel):
    """Input state for RAG agents."""

    query: str = Field(..., description="The query to search the RAG database with.")


class BaseRAGOutputState(BaseModel):
    """Output state for RAG agents."""

    retrieved_documents: list[Document] | list[str] | None = Field(
        default=[],
        description="The results of the RAG search.",
    )


class BaseRAGState(BaseRAGInputState, BaseRAGOutputState):
    """State for RAG agents."""
