"""Config configuration module.

This module provides config functionality for the Haive framework.

Classes:
    BaseRAGConfig: BaseRAGConfig implementation.
    attributes: attributes implementation.

Functions:
    convert_vector_store_to_retriever: Convert Vector Store To Retriever functionality.
    setup_engine: Setup Engine functionality.
"""

import uuid
from typing import Any

from haive.core.engine.agent.agent import AgentConfig
from haive.core.engine.retriever import BaseRetrieverConfig, VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig
from pydantic import BaseModel, ConfigDict, Field, model_validator

# Import state models
from haive.agents.rag.base.state import (
    BaseRAGInputState,
    BaseRAGOutputState,
    BaseRAGState,
)


class BaseRAGConfig(AgentConfig):
    """Configuration for a basic RAG agent."""

    # Configuration for Pydantic
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    name: str = Field(default_factory=lambda: f"rag_agent_{uuid.uuid4().hex[:8]}")
    description: str = Field(default="Basic Retrieval-Augmented Generation agent")

    # Allow either a VectorStoreConfig or RetrieverConfig to be provided
    retriever_config: BaseRetrieverConfig | VectorStoreConfig = Field(
        ..., description="Configuration for the retriever component"  # Required
    )

    # Use class attributes instead of ClassVar for schema references
    state_schema: type[BaseModel] = BaseRAGState
    input_schema: type[BaseModel] = BaseRAGInputState
    output_schema: type[BaseModel] = BaseRAGOutputState

    @model_validator(mode="before")
    @classmethod
    def convert_vector_store_to_retriever(cls, data: dict[str, Any]) -> dict[str, Any]:
        """Pre-validation converter from VectorStoreConfig to RetrieverConfig.
        This runs before Pydantic validation, ensuring the type checking works.
        """
        if isinstance(data, dict) and "retriever_config" in data:
            if isinstance(data["retriever_config"], VectorStoreConfig):
                vs_config = data["retriever_config"]
                data["retriever_config"] = VectorStoreRetrieverConfig(
                    name=f"retriever_for_{data.get('name', 'rag_agent')}",
                    vector_store_config=vs_config,
                )
        return data

    @model_validator(mode="after")
    def setup_engine(self) -> "BaseRAGConfig":
        """After validation, set the engine property to the retriever_config.
        This ensures the agent can use the retriever directly.
        """
        self.engine = self.retriever_config
        return self
