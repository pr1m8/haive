"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    TypedRAGState: TypedRAGState implementation.
"""

from typing import Any

from langchain.schema import Document
from pydantic import Field

from haive.agents.rag.base.state import BaseRAGState


class TypedRAGState(BaseRAGState):
    """State for Typed-RAG."""

    query_category: str | None = Field(
        default=None, description="Classified query category"
    )
    query_metadata: dict[str, Any] = Field(
        default_factory=dict, description="Metadata about the query"
    )
    subqueries: dict[str, str] = Field(
        default_factory=dict, description="Generated subqueries by type"
    )
    subquery_results: dict[str, list[Document]] = Field(
        default_factory=dict, description="Results for each subquery"
    )
    aggregated_answer: str | None = Field(default=None, description="Aggregated answer")
