"""Models model module.

This module provides models functionality for the Haive framework.

Classes:
    DataSourceConfig: DataSourceConfig implementation.

Functions:
    create_retriever: Create Retriever functionality.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

from haive.agents.rag.dynamic.data_source_types import DataSourceType
from haive.core.models.retriever.base import RetrieverConfig


class DataSourceConfig(BaseModel):
    """Base configuration for a data source."""

    name: str = Field(..., description="Name of the data source")
    source_type: DataSourceType = Field(..., description="Type of data source")
    description: str = Field(default="",
                             description="Description of the data source")

    def create_retriever(self) -> RetrieverConfig:
        """Create a retriever for this data source."""
        raise NotImplementedError("Subclasses must implement create_retriever")
