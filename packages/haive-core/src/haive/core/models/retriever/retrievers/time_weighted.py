import logging
from typing import Optional

from langchain_core.retrievers import BaseRetriever
from pydantic import Field

from haive.core.models.retriever.base import RetrieverConfig, RetrieverType
from haive.core.models.vectorstore.base import VectorStoreConfig

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@RetrieverConfig.register(RetrieverType.TIME_WEIGHTED)
class TimeWeightedRetrieverConfig(RetrieverConfig):
    """Configuration for time-weighted retrievers."""

    vector_store_config: Optional[VectorStoreConfig] = Field(
        default=None, description="Configuration for the vector store"
    )
    decay_rate: float = Field(
        default=0.01, description="Rate at which document relevance decays with time"
    )
    decay_offset: float = Field(default=1, description="Offset for decay calculation")
    importance_weight: float = Field(
        default=0.5, description="Weight of importance vs recency"
    )
    include_metadata: bool = Field(
        default=True, description="Whether to include metadata in results"
    )

    def instantiate(self) -> BaseRetriever:
        """Create the time-weighted retriever."""
        if not self.vector_store_config:
            raise ValueError("vector_store_config is required")

        # Import the specific retriever class
        from langchain_community.retrievers import TimeWeightedVectorStoreRetriever

        # Create the vector store
        vector_store = self.vector_store_config.create_vectorstore()

        # Create and return the retriever
        return TimeWeightedVectorStoreRetriever(
            vectorstore=vector_store,
            decay_rate=self.decay_rate,
            decay_offset=self.decay_offset,
            importance_weight=self.importance_weight,
            k=self.k,
            search_kwargs=self.search_kwargs,
            filter=self.search_kwargs.get("filter"),
        )
