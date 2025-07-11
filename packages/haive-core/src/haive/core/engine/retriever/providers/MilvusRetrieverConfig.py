"""Milvus Retriever implementation for the Haive framework.

This module provides a configuration class for the Milvus retriever,
which uses Milvus vector database for high-performance similarity search.
Milvus is an open-source vector database built for scalable similarity search
and AI applications with support for various indexing algorithms.

The MilvusRetriever works by:
1. Connecting to a Milvus server instance
2. Performing vector similarity search using various metrics
3. Supporting advanced indexing and search parameters
4. Providing high-performance retrieval for large-scale datasets

This retriever is particularly useful when:
- Working with large-scale vector datasets (millions+ vectors)
- Need high-performance similarity search
- Require advanced indexing capabilities (IVF, HNSW, etc.)
- Building production vector search applications
- Need distributed and scalable vector storage

The implementation integrates with LangChain's Milvus retriever while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field

from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType
from haive.core.engine.vectorstore.vectorstore import VectorStoreConfig


@BaseRetrieverConfig.register(RetrieverType.MILVUS)
class MilvusRetrieverConfig(BaseRetrieverConfig):
    """Configuration for Milvus retriever in the Haive framework.

    This retriever uses Milvus vector database to perform high-performance
    similarity search with support for various indexing and search parameters.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always MILVUS).
        vectorstore_config (VectorStoreConfig): Milvus vector store configuration.
        k (int): Number of documents to retrieve.
        search_params (Optional[Dict]): Milvus search parameters.
        consistency_level (str): Consistency level for search.
        timeout (Optional[float]): Search timeout in seconds.

    Examples:
        >>> from haive.core.engine.retriever import MilvusRetrieverConfig
        >>> from haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig import MilvusVectorStoreConfig
        >>>
        >>> # Configure Milvus vector store
        >>> vectorstore_config = MilvusVectorStoreConfig(
        ...     name="milvus_store",
        ...     host="localhost",
        ...     port=19530,
        ...     collection_name="documents",
        ...     index_params={"metric_type": "IP", "index_type": "IVF_FLAT"}
        ... )
        >>>
        >>> # Create the Milvus retriever config
        >>> config = MilvusRetrieverConfig(
        ...     name="milvus_retriever",
        ...     vectorstore_config=vectorstore_config,
        ...     k=10,
        ...     search_params={"nprobe": 16},
        ...     consistency_level="Strong"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("machine learning algorithms")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.MILVUS, description="The type of retriever"
    )

    # Vector store configuration
    vectorstore_config: VectorStoreConfig = Field(
        ..., description="Milvus vector store configuration"
    )

    # Search parameters
    k: int = Field(
        default=10, ge=1, le=1000, description="Number of documents to retrieve"
    )

    search_params: dict[str, Any] | None = Field(
        default=None,
        description="Milvus search parameters (nprobe, ef, search_k, etc.)",
    )

    # Milvus-specific parameters
    consistency_level: str = Field(
        default="Bounded",
        description="Consistency level: 'Strong', 'Session', 'Bounded', 'Eventually'",
    )

    timeout: float | None = Field(
        default=None, ge=0.1, le=300.0, description="Search timeout in seconds"
    )

    # Expression filter
    expr: str | None = Field(
        default=None, description="Boolean expression for metadata filtering"
    )

    # Partition names
    partition_names: list[str] | None = Field(
        default=None, description="List of partition names to search"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Milvus retriever."""
        return {
            "query": (str, Field(description="Vector search query for Milvus")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Milvus retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Documents from Milvus vector search",
                ),
            ),
        }

    def instantiate(self):
        """Create a Milvus retriever from this configuration.

        Returns:
            MilvusRetriever: Instantiated retriever ready for vector search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_milvus import Milvus
        except ImportError:
            raise ImportError(
                "MilvusRetriever requires langchain-milvus package. "
                "Install with: pip install langchain-milvus"
            )

        # Instantiate the vector store
        vectorstore = self.vectorstore_config.instantiate()

        if not isinstance(vectorstore, Milvus):
            raise ValueError(
                "MilvusRetrieverConfig requires a Milvus vector store configuration"
            )

        # Prepare search kwargs
        search_kwargs = {"k": self.k}

        if self.search_params:
            search_kwargs["param"] = self.search_params

        if self.consistency_level:
            search_kwargs["consistency_level"] = self.consistency_level

        if self.timeout:
            search_kwargs["timeout"] = self.timeout

        if self.expr:
            search_kwargs["expr"] = self.expr

        if self.partition_names:
            search_kwargs["partition_names"] = self.partition_names

        # Return the vector store as retriever with search kwargs
        return vectorstore.as_retriever(search_kwargs=search_kwargs)
