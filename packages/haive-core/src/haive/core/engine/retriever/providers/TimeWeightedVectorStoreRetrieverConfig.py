"""Time-Weighted Vector Store Retriever implementation for the Haive framework.

This module provides a configuration class for the Time-Weighted Vector Store retriever,
which combines vector similarity search with time-based scoring to prioritize recent
documents while still considering semantic relevance.

The TimeWeightedVectorStoreRetriever works by:
1. Performing standard vector similarity search on document content
2. Applying time-based decay factors to prioritize recent documents
3. Combining similarity scores with recency scores using configurable weights
4. Returning documents that balance relevance and recency

This retriever is particularly useful when:
- Building systems where document freshness matters (news, updates, etc.)
- Need to balance between relevance and recency
- Working with time-sensitive information retrieval
- Building conversational systems that should prefer recent context

The implementation integrates with LangChain's TimeWeightedVectorStoreRetriever while
providing a consistent Haive configuration interface with flexible time weighting options.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.TIME_WEIGHTED)
class TimeWeightedVectorStoreRetrieverConfig(BaseRetrieverConfig):
    """Configuration for Time-Weighted Vector Store retriever in the Haive framework.

    This retriever combines vector similarity search with time-based scoring to
    prioritize recent documents while maintaining semantic relevance.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always TIME_WEIGHTED).
        vectorstore_config (VectorStoreConfig): Vector store for semantic search.
        decay_rate (float): Rate at which time relevance decays (higher = faster decay).
        k (int): Number of documents to return.
        fetch_k (int): Number of documents to fetch before time weighting.
        lambda_mult (float): Multiplier for time weighting vs. similarity (0.0 = only similarity, 1.0 = only time).

    Examples:
        >>> from haive.core.engine.retriever import TimeWeightedVectorStoreRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig
        >>>
        >>> # Create vector store config
        >>> vs_config = ChromaVectorStoreConfig(
        ...     name="time_weighted_store",
        ...     collection_name="time_sensitive_docs"
        ... )
        >>>
        >>> # Create time-weighted retriever
        >>> config = TimeWeightedVectorStoreRetrieverConfig(
        ...     name="time_weighted_retriever",
        ...     vectorstore_config=vs_config,
        ...     decay_rate=-0.01,  # Slow decay
        ...     lambda_mult=0.25,  # 25% time weighting, 75% similarity
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest AI developments")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.TIME_WEIGHTED, description="The type of retriever"
    )

    # Core configuration
    vectorstore_config: VectorStoreConfig = Field(
        ...,
        description="Vector store configuration for semantic search and time tracking",
    )

    # Time weighting parameters
    decay_rate: float = Field(
        default=-0.01,
        ge=-1.0,
        le=0.0,
        description="Rate at which time relevance decays (negative value, closer to 0 = slower decay)",
    )

    lambda_mult: float = Field(
        default=0.25,
        ge=0.0,
        le=1.0,
        description="Balance between time weighting and similarity (0.0 = only similarity, 1.0 = only time)",
    )

    # Retrieval parameters
    k: int = Field(
        default=4,
        ge=1,
        le=100,
        description="Number of documents to return after time weighting",
    )

    fetch_k: int = Field(
        default=20,
        ge=1,
        le=500,
        description="Number of documents to fetch before applying time weighting",
    )

    # Search configuration
    search_type: str = Field(
        default="similarity", description="Type of initial search: 'similarity', 'mmr'"
    )

    search_kwargs: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional search parameters for the vector store",
    )

    @validator("fetch_k")
    def validate_fetch_k(self, v, values):
        """Validate that fetch_k is greater than or equal to k."""
        k = values.get("k", 4)
        if v < k:
            raise ValueError(f"fetch_k ({v}) must be greater than or equal to k ({k})")
        return v

    @validator("search_type")
    def validate_search_type(self, v):
        """Validate search type."""
        valid_types = ["similarity", "mmr"]
        if v not in valid_types:
            raise ValueError(f"search_type must be one of {valid_types}, got {v}")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Time-Weighted retriever."""
        return {
            "query": (
                str,
                Field(description="Query for time-weighted semantic search"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Time-Weighted retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents ranked by combined similarity and recency",
                ),
            ),
        }

    def instantiate(self):
        """Create a Time-Weighted Vector Store retriever from this configuration.

        Returns:
            TimeWeightedVectorStoreRetriever: Instantiated retriever ready for time-weighted retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import TimeWeightedVectorStoreRetriever
        except ImportError:
            raise ImportError(
                "TimeWeightedVectorStoreRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate the vector store
        try:
            vectorstore = self.vectorstore_config.instantiate()
        except Exception as e:
            raise ValueError(f"Failed to instantiate vector store: {e}")

        # Create search kwargs
        search_kwargs = dict(self.search_kwargs)
        if self.search_type == "mmr":
            search_kwargs["search_type"] = "mmr"

        return TimeWeightedVectorStoreRetriever(
            vectorstore=vectorstore,
            decay_rate=self.decay_rate,
            k=self.k,
            other_score_keys=["relevance_score"],
            search_kwargs=search_kwargs,
        )
