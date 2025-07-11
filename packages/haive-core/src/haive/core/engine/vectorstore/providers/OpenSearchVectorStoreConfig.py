"""OpenSearch Vector Store implementation for the Haive framework.

This module provides a configuration class for the OpenSearch vector store,
which provides scalable vector search capabilities with Amazon OpenSearch.

OpenSearch provides:
1. Scalable vector search with approximate nearest neighbor (ANN) algorithms
2. Multiple engine support (nmslib, faiss, lucene)
3. Hybrid search combining keyword and vector search
4. AOSS (Amazon OpenSearch Service Serverless) support
5. Advanced filtering and metadata search
6. Both synchronous and asynchronous operations

This vector store is particularly useful when:
- You need scalable vector search with enterprise features
- Want hybrid search capabilities (keyword + vector)
- Building applications with OpenSearch/Elasticsearch expertise
- Need integration with AWS OpenSearch Service
- Require advanced filtering and search features

The implementation integrates with LangChain's OpenSearch while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.OPENSEARCH)
class OpenSearchVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for OpenSearch vector store in the Haive framework.

    This vector store uses OpenSearch for scalable vector search with
    support for multiple engines and hybrid search capabilities.

    Attributes:
        opensearch_url (str): OpenSearch cluster URL.
        index_name (str): Name of the OpenSearch index.
        engine (str): Vector engine to use (nmslib, faiss, lucene).
        space_type (str): Distance metric for vector similarity.
        bulk_size (int): Bulk operation size for indexing.

    Examples:
        >>> from haive.core.engine.vectorstore import OpenSearchVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create OpenSearch config (local)
        >>> config = OpenSearchVectorStoreConfig(
        ...     name="opensearch_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     opensearch_url="http://localhost:9200",
        ...     index_name="document_vectors"
        ... )
        >>>
        >>> # Create OpenSearch config (with authentication)
        >>> config = OpenSearchVectorStoreConfig(
        ...     name="opensearch_cluster",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     opensearch_url="https://search-domain.us-west-2.es.amazonaws.com",
        ...     index_name="vectors",
        ...     username="admin",
        ...     password="password",
        ...     engine="faiss",
        ...     space_type="cosine"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="OpenSearch provides scalable vector search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Hybrid search capabilities
        >>> results = vectorstore.similarity_search("scalable search", k=5)
    """

    # OpenSearch connection configuration
    opensearch_url: str = Field(
        default="http://localhost:9200", description="OpenSearch cluster URL"
    )

    index_name: str = Field(..., description="Name of the OpenSearch index (required)")

    # Authentication
    username: str | None = Field(default=None, description="OpenSearch username")

    password: str | None = Field(
        default=None,
        description="OpenSearch password (auto-resolved from OPENSEARCH_PASSWORD)",
    )

    # Engine configuration
    engine: str = Field(
        default="nmslib", description="Vector engine: 'nmslib', 'faiss', 'lucene'"
    )

    space_type: str = Field(
        default="l2",
        description="Distance metric: 'l2', 'cosine', 'l1', 'linf', 'innerproduct'",
    )

    # Index configuration
    bulk_size: int = Field(
        default=500, ge=1, le=10000, description="Bulk operation size for indexing"
    )

    # Search configuration
    ef_search: int = Field(
        default=512,
        ge=1,
        le=10000,
        description="Size of dynamic list for k-NN searches (higher = more accurate but slower)",
    )

    ef_construction: int = Field(
        default=512,
        ge=1,
        le=10000,
        description="Size of dynamic list for k-NN graph creation (higher = more accurate but slower indexing)",
    )

    m: int = Field(
        default=16,
        ge=2,
        le=100,
        description="Number of bidirectional links for each element (impacts memory consumption)",
    )

    # Field mapping
    vector_field: str = Field(
        default="vector_field", description="Document field name for storing embeddings"
    )

    text_field: str = Field(
        default="text", description="Document field name for storing text content"
    )

    metadata_field: str = Field(
        default="metadata", description="Document field name for storing metadata"
    )

    # Hybrid search configuration
    is_appx_search: bool = Field(
        default=True,
        description="Whether to use approximate search (recommended for large datasets)",
    )

    # Connection settings
    timeout: int = Field(
        default=30, ge=1, le=300, description="Connection timeout in seconds"
    )

    max_retries: int = Field(
        default=3, ge=0, le=10, description="Maximum number of connection retries"
    )

    # Performance settings
    max_chunk_bytes: int = Field(
        default=1024 * 1024,  # 1MB
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        description="Maximum chunk size for bulk operations in bytes",
    )

    @validator("opensearch_url")
    def validate_opensearch_url(self, v):
        """Validate OpenSearch URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("opensearch_url must start with http:// or https://")
        return v

    @validator("engine")
    def validate_engine(self, v):
        """Validate vector engine is supported."""
        valid_engines = ["nmslib", "faiss", "lucene"]
        if v not in valid_engines:
            raise ValueError(f"engine must be one of {valid_engines}, got {v}")
        return v

    @validator("space_type")
    def validate_space_type(self, v):
        """Validate space type is supported."""
        valid_space_types = [
            "l2",
            "cosine",
            "l1",
            "linf",
            "innerproduct",
            "cosinesimil",
        ]
        if v not in valid_space_types:
            raise ValueError(f"space_type must be one of {valid_space_types}, got {v}")
        return v

    @validator("index_name")
    def validate_index_name(self, v):
        """Validate index name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("index_name cannot be empty")
        # Basic validation for OpenSearch index naming
        import re

        if not re.match(r"^[a-z0-9_.-]+$", v.lower()):
            raise ValueError(
                "index_name must contain only lowercase letters, numbers, dots, hyphens, and underscores"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for OpenSearch vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for OpenSearch vector store."""
        return {
            "ids": (
                list[str],
                Field(description="IDs of the added documents in OpenSearch"),
            ),
        }

    def instantiate(self):
        """Create an OpenSearch vector store from this configuration.

        Returns:
            OpenSearchVectorSearch: Instantiated OpenSearch vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import OpenSearchVectorSearch
        except ImportError as e:
            raise ImportError(
                "OpenSearch requires opensearch-py package. "
                "Install with: pip install opensearch-py"
            ) from e

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get password from config or environment
        password = self.password
        if self.username and not password:
            import os

            password = os.getenv("OPENSEARCH_PASSWORD")

        # Prepare authentication
        http_auth = None
        if self.username and password:
            http_auth = (self.username, password)

        # Prepare OpenSearch client configuration
        client_kwargs = {
            "http_auth": http_auth,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }

        # Prepare OpenSearch vector store configuration
        kwargs = {
            "engine": self.engine,
            "space_type": self.space_type,
            "ef_search": self.ef_search,
            "ef_construction": self.ef_construction,
            "m": self.m,
            "vector_field": self.vector_field,
            "text_field": self.text_field,
            "metadata_field": self.metadata_field,
            "is_appx_search": self.is_appx_search,
            "bulk_size": self.bulk_size,
            "max_chunk_bytes": self.max_chunk_bytes,
            **client_kwargs,
        }

        # Create OpenSearch vector store
        try:
            vectorstore = OpenSearchVectorSearch(
                opensearch_url=self.opensearch_url,
                index_name=self.index_name,
                embedding_function=embedding_function,
                **kwargs,
            )
        except Exception as e:
            raise ValueError(f"Failed to create OpenSearch vector store: {e}") from e

        return vectorstore
