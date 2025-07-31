"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    FilteredRAGState: FilteredRAGState implementation.
"""

from langchain_core.documents import Document
from pydantic import Field

from haive.agents.rag.base.state import BaseRAGState


class FilteredRAGState(BaseRAGState):
    """State for filtered RAG agents.

    This state extends the base RAG state with:
    1. Filtered documents - a subset of retrieved documents that passed relevance filtering
    2. Relevance scores - numerical scores indicating how relevant each document is to the query
    3. Error tracking - any errors encountered during the filtering process

    The filtering process helps to:
    - Improve answer quality by focusing on the most relevant information
    - Reduce noise and hallucinations from irrelevant content
    - Provide transparency through relevance scoring
    """

    # Document filtering results
    filtered_documents: list[Document] | list[str] | None = Field(
        default=[],
        description="The filtered documents that passed the relevance threshold.",
    )

    # Relevance scoring
    relevance_scores: dict[str, float] = Field(
        default={},
        description="Mapping of document IDs to relevance scores (0.0 to 1.0).",
    )

    # Error handling
    error: str | None = Field(
        default=None,
        description="Error message if something went wrong during filtering.",
    )
