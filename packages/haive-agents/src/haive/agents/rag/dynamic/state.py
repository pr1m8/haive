from typing import Any

from langchain.schema import Document
from pydantic import Field

from haive.agents.rag.base.state import BaseRAGState


class DynamicRAGState(BaseRAGState):
    """State for Dynamic RAG."""

    selected_sources: list[str] = Field(
        default_factory=list, description="Selected data sources"
    )
    source_documents: dict[str, list[Document]] = Field(
        default_factory=dict, description="Documents by source"
    )
    source_metrics: dict[str, dict[str, Any]] = Field(
        default_factory=dict, description="Metrics by source"
    )
    routing_explanation: str | None = Field(
        default=None, description="Explanation for routing decision"
    )
