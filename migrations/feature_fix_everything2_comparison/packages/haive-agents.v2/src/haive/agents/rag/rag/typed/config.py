"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    TypedRAGConfig: TypedRAGConfig implementation.
"""

from typing import Any

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.rag.base.config import BaseRAGConfig


class TypedRAGConfig(BaseRAGConfig):
    """Configuration for Typed-RAG with specialized handlers."""

    query_classifier_config: AugLLMConfig = Field(
        ..., description="Configuration for query classifier"
    )
    type_handlers: dict[str, AugLLMConfig] = Field(
        default_factory=dict, description="Specialized handlers for query types"
    )
    retriever_mapping: dict[str, Any] = Field(
        default_factory=dict, description="Mapping of query types to retrievers"
    )
    enable_subqueries: bool = Field(
        default=True, description="Whether to generate specialized subqueries"
    )
