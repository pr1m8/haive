"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    FilteredRAGConfig: FilteredRAGConfig implementation.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.rag.base.config import BaseRAGConfig
from haive.agents.rag.filtered.state import FilteredRAGState


class FilteredRAGConfig(BaseRAGConfig):
    """Configuration for RAG agents with document filtering capabilities.

    This RAG implementation extends the base RAG with:
    1. Document filtering based on relevance to the query
    2. Configurable relevance threshold to filter out irrelevant documents
    """

    # State schema
    state_schema: type = Field(
        default=FilteredRAGState, description="State schema for filtered RAG"
    )

    # Document filtering
    document_filter_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for document relevance evaluation"
    )

    relevance_threshold: float = Field(
        default=0.7, description="Threshold for document relevance (0.0 to 1.0)"
    )

    # Optional answer generator
    answer_generator_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for answer generation"
    )
