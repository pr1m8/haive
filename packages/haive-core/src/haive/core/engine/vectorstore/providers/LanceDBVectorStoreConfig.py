"""LanceDB Vector Store implementation for the Haive framework.

This module provides a configuration class for the LanceDB vector store,
which is a modern, high-performance vector database built on Lance format.

LanceDB provides:
1. Columnar storage format optimized for vector search
2. ACID transactions and versioning
3. Efficient disk-based storage with memory mapping
4. Hybrid search combining vector and full-text search
5. Automatic indexing and query optimization
6. Multi-modal data support (vectors, text, images)

This vector store is particularly useful when:
- You need high-performance vector search at scale
- Want persistent storage with ACID guarantees
- Need to handle large datasets that don't fit in memory
- Building applications requiring hybrid search capabilities
- Want modern columnar storage with versioning support

The implementation integrates with LangChain's LanceDB while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.LANCEDB)
class LanceDBVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """Configuration for LanceDB vector store in the Haive framework.

    This vector store uses LanceDB for high-performance vector search
    with columnar storage and ACID transactions.

    Attributes:
        uri (str): LanceDB connection URI.
        table_name (str): Name of the LanceDB table.
        vector_key (str): Key for storing vectors.
        text_key (str): Key for storing text content.
        id_key (str): Key for storing document IDs.
        distance (str): Distance metric for vector similarity.
        mode (str): Mode for adding data to the table.

    Examples:
        >>> from haive.core.engine.vectorstore import LanceDBVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create LanceDB config (local)
        >>> config = LanceDBVectorStoreConfig(
        ...     name="lancedb_local",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     uri="/tmp/lancedb",
        ...     table_name="documents",
        ...     distance="cosine"
        ... )
        >>>
        >>> # Create LanceDB config (cloud)
        >>> config = LanceDBVectorStoreConfig(
        ...     name="lancedb_cloud",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     uri="db://my-database",
        ...     table_name="vectors",
        ...     api_key="lance-api-key",
        ...     region="us-west-2"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="LanceDB provides fast columnar vectors")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # High-performance vector search
        >>> results = vectorstore.similarity_search("columnar database", k=5)
    """

    # LanceDB connection configuration
    uri: str = Field(
        default="/tmp/lancedb",
        description="LanceDB connection URI (local path or cloud URI like 'db://database-name')",
    )

    # Cloud configuration (SecureConfigMixin)
    api_key: str | None = Field(
        default=None,
        description="LanceDB API key for cloud connections (auto-resolved from LANCE_API_KEY)",
    )

    region: str | None = Field(
        default=None,
        description="LanceDB region for cloud connections (e.g., 'us-west-2')",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="lancedb", description="Provider name for API key resolution"
    )

    # Table configuration
    table_name: str = Field(
        default="vectorstore", description="Name of the LanceDB table"
    )

    # Field configuration
    vector_key: str = Field(
        default="vector", description="Key to use for storing vectors in the table"
    )

    text_key: str = Field(
        default="text", description="Key to use for storing text content in the table"
    )

    id_key: str = Field(
        default="id", description="Key to use for storing document IDs in the table"
    )

    # Vector configuration
    distance: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'l2', 'dot', or 'hamming'",
    )

    # Table management
    mode: str = Field(
        default="overwrite", description="Mode for adding data: 'overwrite' or 'append'"
    )

    # Performance configuration
    limit: int = Field(
        default=10, ge=1, le=10000, description="Default limit for search results"
    )

    # Advanced options
    nprobes: int | None = Field(
        default=None, ge=1, description="Number of probes for IVF index search"
    )

    refine_factor: int | None = Field(
        default=None, ge=1, description="Refine factor for improving search quality"
    )

    @validator("distance")
    def validate_distance(self, v):
        """Validate distance metric is supported."""
        valid_distances = ["cosine", "l2", "dot", "hamming"]
        if v not in valid_distances:
            raise ValueError(f"distance must be one of {valid_distances}, got {v}")
        return v

    @validator("mode")
    def validate_mode(self, v):
        """Validate mode is supported."""
        valid_modes = ["overwrite", "append"]
        if v not in valid_modes:
            raise ValueError(f"mode must be one of {valid_modes}, got {v}")
        return v

    @validator("uri")
    def validate_uri(self, v):
        """Basic validation of LanceDB URI."""
        if v.startswith("db://") and len(v) < 6:
            raise ValueError(
                "Cloud URI must include database name: 'db://database-name'"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for LanceDB vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for LanceDB vector store."""
        return {
            "ids": (
                list[str],
                Field(description="IDs of the added documents in LanceDB"),
            ),
        }

    def instantiate(self):
        """Create a LanceDB vector store from this configuration.

        Returns:
            LanceDB: Instantiated LanceDB vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import LanceDB
        except ImportError:
            raise ImportError(
                "LanceDB requires lancedb package. Install with: pip install lancedb"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key using SecureConfigMixin for cloud connections
        api_key = None
        if self.uri.startswith("db://"):
            api_key = self.get_api_key()
            if not api_key:
                import os

                api_key = os.getenv("LANCE_API_KEY")

            if not api_key:
                raise ValueError(
                    "LanceDB cloud connection requires API key. "
                    "Set LANCE_API_KEY environment variable or provide api_key parameter."
                )

        # Prepare kwargs
        kwargs = {
            "uri": self.uri,
            "embedding": embedding_function,
            "vector_key": self.vector_key,
            "id_key": self.id_key,
            "text_key": self.text_key,
            "table_name": self.table_name,
            "distance": self.distance,
            "mode": self.mode,
            "limit": self.limit,
        }

        # Add cloud-specific parameters
        if api_key:
            kwargs["api_key"] = api_key

        if self.region:
            kwargs["region"] = self.region

        # Add performance parameters if specified
        if self.nprobes is not None:
            kwargs["nprobes"] = self.nprobes

        if self.refine_factor is not None:
            kwargs["refine_factor"] = self.refine_factor

        # Create LanceDB vector store
        try:
            vectorstore = LanceDB(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create LanceDB vector store: {e}")

        return vectorstore
