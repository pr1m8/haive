from typing import Any

from agents.react.react.state import ReactAgentState
from pydantic import Field


class ReactManyToolsState(ReactAgentState):
    """State for React Agent with many tools.

    Adds fields for tool selection, filtering, and document retrieval.
    """

    # Add fields specific to many tools
    tool_filter_query: str | None = None
    filtered_tools: list[str] = Field(default_factory=list)
    tool_categories: dict[str, list[str]] = Field(default_factory=dict)
    current_tool_category: str | None = None

    # RAG integration fields
    query: str | None = None
    retrieved_documents: list[dict[str, Any]] = Field(default_factory=list)
    retrieval_metadata: dict[str, Any] = Field(default_factory=dict)
