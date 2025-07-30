"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    MultiStrategyRAGConfig: MultiStrategyRAGConfig implementation.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.rag.multi_strategy.state import MultiStrategyRAGState
from haive.agents.rag.self_corr.config import SelfCorrectiveRAGConfig


class MultiStrategyRAGConfig(SelfCorrectiveRAGConfig):
    """Configuration for multi-strategy RAG agents."""

    state_schema: type[MultiStrategyRAGState] = Field(
        default=MultiStrategyRAGState, description="State schema"
    )
    query_analyzer_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for query analysis"
    )
    query_rewriter_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for query rewriting"
    )
    retriever_strategies: dict[str, Any] = Field(
        default_factory=dict, description="Specialized retriever configurations"
    )
