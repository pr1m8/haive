"""
Merger Retriever implementation for the Haive framework.

This module provides a configuration class for the Merger retriever,
which combines and merges results from multiple retrievers to provide
comprehensive and deduplicated search results.

The MergerRetriever works by:
1. Running multiple retrievers in parallel on the same query
2. Collecting all results from different retrieval strategies
3. Merging and deduplicating results based on content or metadata
4. Applying optional ranking and filtering to the merged results

This retriever is particularly useful when:
- Need to combine results from different retrieval approaches
- Want comprehensive coverage across multiple data sources
- Building systems that need to deduplicate overlapping results
- Implementing federated search across different backends

The implementation integrates with LangChain's MergerRetriever while
providing a consistent Haive configuration interface with flexible merging options.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.MERGER)
class MergerRetrieverConfig(BaseRetrieverConfig):
    """
    Configuration for Merger retriever in the Haive framework.

    This retriever combines and merges results from multiple retrievers to provide
    comprehensive and deduplicated search results.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always MERGER).
        retrievers (List[BaseRetrieverConfig]): List of retriever configurations to merge.
        max_results (int): Maximum number of results to return after merging.

    Examples:
        >>> from haive.core.engine.retriever import MergerRetrieverConfig
        >>> from haive.core.engine.retriever.providers.BM25RetrieverConfig import BM25RetrieverConfig
        >>> from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
        >>>
        >>> # Create individual retrievers
        >>> bm25_config = BM25RetrieverConfig(name="bm25", documents=docs, k=10)
        >>> vector_config = VectorStoreRetrieverConfig(name="vector", vectorstore_config=vs_config, k=10)
        >>>
        >>> # Create merger retriever
        >>> config = MergerRetrieverConfig(
        ...     name="merger_retriever",
        ...     retrievers=[bm25_config, vector_config],
        ...     max_results=15
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.MERGER, description="The type of retriever"
    )

    # Core configuration
    retrievers: List[BaseRetrieverConfig] = Field(
        ...,
        min_items=2,
        description="List of retriever configurations to merge results from",
    )

    # Result limiting
    max_results: int = Field(
        default=20,
        ge=1,
        le=200,
        description="Maximum number of results to return after merging",
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Merger retriever."""
        return {
            "query": (
                str,
                Field(description="Query for merged retrieval across multiple sources"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Merger retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Merged and deduplicated documents from multiple retrievers",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Merger retriever from this configuration.

        Returns:
            MergerRetriever: Instantiated retriever ready for merging multiple retrieval results.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain.retrievers import MergerRetriever
        except ImportError:
            raise ImportError(
                "MergerRetriever requires langchain package. "
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
        if len(instantiated_retrievers) < 2:
            raise ValueError(
                f"MergerRetriever requires at least 2 retrievers, got {len(instantiated_retrievers)}"
            )

        return MergerRetriever(
            retrievers=instantiated_retrievers,
        )
