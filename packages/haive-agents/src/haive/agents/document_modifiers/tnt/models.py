"""Data models for taxonomy generation.

This module defines the core data structures used in the taxonomy generation process,
particularly the document model that represents individual pieces of content being
processed.

Example:
    Basic usage of document model::

        doc = Doc(
            id="doc1",
            content="Sample text",
            summary="Brief summary",
            explanation="Summary rationale",
            category="Technology"
        )
"""

import logging

from langchain_core.documents import Document
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger("tnt-llm")


class Doc(BaseModel):
    """Represents a single document or chat log in the taxonomy generation process.

    This class serves as the fundamental data structure for content being processed
    through the taxonomy generation workflow. It tracks both the original content
    and metadata added during processing.

    Attributes:
        id (str): Unique identifier for the document, used for tracking and reference.
        content (str): Original text content of the document or chat log.
        summary (Optional[str]): Condensed version of the content, generated in the
            first step of processing. Defaults to empty string.
        explanation (Optional[str]): Rationale for how the summary was generated,
            added alongside the summary. Defaults to empty string.
        category (Optional[str]): Taxonomy category assigned to the document in
            later stages of processing. Defaults to empty string.

    Example:
        >>> doc = Doc(
        ...     id="chat_123",
        ...     content="User asked about Python installation",
        ...     summary="Python setup inquiry",
        ...     explanation="Focused on main topic",
        ...     category="Technical Support"
        ... )
    """

    id: str = Field(description="The unique identifier for the document.")
    content: str = Field(description="The content of the document.")
    summary: str | None = Field("", description="The summary of the document.")
    explanation: str | None = Field("", description="The explanation of the document.")
    category: str | None = Field("", description="The category of the document.")
    metadata: dict | None = Field(
        {}, description="Any additional metadata for the document."
    )

    @classmethod
    def from_document(cls, document: Document) -> "Doc":
        return cls(
            id=document.id, content=document.page_content, metadata=document.metadata
        )
