"""State core module.

This module provides state functionality for the Haive framework.

Classes:
    MultiStrategyRAGState: MultiStrategyRAGState implementation.
"""

from typing import Any

from pydantic import Field

from haive.agents.rag.self_corr.state import SelfCorrectiveRAGState


class MultiStrategyRAGState(SelfCorrectiveRAGState):
    """State for multi-strategy RAG agents."""

    query_type: str | None = Field(default=None, description="Classified query type")
    strategy_name: str | None = Field(
        default=None, description="Selected retrieval strategy"
    )
    query_variations: list[str] = Field(
        default_factory=list, description="Generated query variations"
    )
    rewritten_query: str | None = Field(default=None, description="Rewritten query")
    strategy_metrics: dict[str, Any] = Field(
        default_factory=dict, description="Metrics for the selected strategy"
    )
