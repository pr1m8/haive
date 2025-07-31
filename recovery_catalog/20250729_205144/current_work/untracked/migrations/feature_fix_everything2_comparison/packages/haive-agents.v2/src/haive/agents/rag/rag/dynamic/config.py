"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    DynamicRAGConfig: DynamicRAGConfig implementation.
"""

from haive.core.engine.aug_llm import AugLLMConfig
from pydantic import Field

from haive.agents.rag.base.config import BaseRAGConfig
from haive.agents.rag.dynamic.data_source_types import DataSourceConfig


class DynamicRAGConfig(BaseRAGConfig):
    """Configuration for Dynamic RAG with multiple data sources."""

    data_sources: dict[str, DataSourceConfig] = Field(
        default_factory=dict, description="Map of data source names to configurations"
    )
    query_router_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for query router"
    )
    result_merger_config: AugLLMConfig | None = Field(
        default=None, description="Configuration for result merger"
    )
    default_source: str | None = Field(
        default=None, description="Default data source if routing fails"
    )
    enable_parallel_retrieval: bool = Field(
        default=False,
        description="Whether to retrieve from multiple sources in parallel",
    )
    max_sources_per_query: int = Field(
        default=3, description="Maximum number of sources to query simultaneously"
    )
