"""Ensemble Retriever implementation for the Haive framework.

This module provides a configuration class for the Ensemble retriever,
which combines multiple retrieval strategies using weighted combination
to improve overall retrieval performance and coverage.

The EnsembleRetriever works by:
1. Running multiple retrievers in parallel on the same query
2. Combining results using configurable weights for each retriever
3. Re-ranking and deduplicating the combined results
4. Returning the most relevant documents from the ensemble

This retriever is particularly useful when:
- You want to combine different retrieval strategies (sparse + dense)
- Need to balance precision and recall across different approaches
- Building robust systems that work across diverse query types
- Implementing hybrid search with customizable weights

The implementation integrates with LangChain's EnsembleRetriever while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ENSEMBLE)
class EnsembleRetrieverConfig(BaseRetrieverConfig):
    """Configuration for Ensemble retriever in the Haive framework.

    This retriever combines multiple retrieval strategies using weighted combination
    to improve overall performance and coverage across different query types.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ENSEMBLE).
        retrievers (List[BaseRetrieverConfig]): List of retriever configurations to ensemble.
        weights (List[float]): Weights for each retriever (must sum to 1.0).
        k (int): Number of documents to return from the ensemble.
        normalize_scores (bool): Whether to normalize scores before combining.

    Examples:
        >>> from haive.core.engine.retriever import EnsembleRetrieverConfig
        >>> from haive.core.engine.retriever.providers.BM25RetrieverConfig import BM25RetrieverConfig
        >>> from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
        >>>
        >>> # Create individual retrievers
        >>> bm25_config = BM25RetrieverConfig(name="bm25", documents=docs, k=10)
        >>> vector_config = VectorStoreRetrieverConfig(name="vector", vectorstore_config=vs_config, k=10)
        >>>
        >>> # Create ensemble retriever
        >>> config = EnsembleRetrieverConfig(
        ...     name="hybrid_ensemble",
        ...     retrievers=[bm25_config, vector_config],
        ...     weights=[0.3, 0.7],  # 30% BM25, 70% vector
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ENSEMBLE, description="The type of retriever"
    )

    # Core ensemble configuration
    retrievers: list[BaseRetrieverConfig] = Field(
        ...,
        min_items=2,
        description="List of retriever configurations to combine in the ensemble",
    )

    weights: list[float] = Field(
        ...,
        description="Weights for each retriever (must sum to 1.0 and match number of retrievers)",
    )

    # Retrieval parameters
    k: int = Field(
        default=4,
        ge=1,
        le=100,
        description="Number of documents to return from the ensemble",
    )

    # Processing options
    normalize_scores: bool = Field(
        default=True, description="Whether to normalize scores before combining results"
    )

    c: int = Field(
        default=60,
        ge=1,
        le=1000,
        description="Parameter for score normalization (higher values reduce score variance)",
    )

    @validator("weights")
    def validate_weights(self, v, values):
        """Validate that weights sum to 1.0."""
        if abs(sum(v) - 1.0) > 1e-6:
            raise ValueError(f"Weights must sum to 1.0, got {sum(v)}")
        return v

    @validator("weights")
    def validate_weights_length(self, v, values):
        """Validate that weights match number of retrievers."""
        if "retrievers" in values and len(v) != len(values["retrievers"]):
            raise ValueError(
                f"Number of weights ({len(v)}) must match number of retrievers ({len(values['retrievers'])})"
            )
        return v

    @validator("weights", each_item=True)
    def validate_weight_values(self, v):
        """Validate that each weight is between 0 and 1."""
        if not 0 <= v <= 1:
            raise ValueError(f"Each weight must be between 0 and 1, got {v}")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Ensemble retriever."""
        return {
            "query": (str, Field(description="Query string for ensemble retrieval")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Ensemble retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved by the ensemble",
                ),
            ),
        }

    def instantiate(self):
        """Create an Ensemble retriever from this configuration.

        Returns:
            EnsembleRetriever: Instantiated retriever ready for ensemble retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import EnsembleRetriever
        except ImportError:
            raise ImportError(
                "EnsembleRetriever requires langchain package. "
                "Install with: pip install langchain"
            )

        # Instantiate all component retrievers
        instantiated_retrievers = []
        for retriever_config in self.retrievers:
            try:
                retriever = retriever_config.instantiate()
                instantiated_retrievers.append(retriever)
            except Exception as e:
                raise ValueError(
                    f"Failed to instantiate retriever {retriever_config.name}: {e}"
                )

        # Validate we have the right number of retrievers
        if len(instantiated_retrievers) != len(self.weights):
            raise ValueError(
                f"Number of instantiated retrievers ({len(instantiated_retrievers)}) "
                f"doesn't match number of weights ({len(self.weights)})"
            )

        return EnsembleRetriever(
            retrievers=instantiated_retrievers, weights=self.weights, c=self.c
        )
