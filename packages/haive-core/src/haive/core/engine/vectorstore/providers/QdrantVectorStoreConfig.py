"""Qdrant Vector Store implementation for the Haive framework.

This module provides a configuration class for the Qdrant vector store,
which is a vector similarity search engine with extended filtering support.

Qdrant provides:
1. High-performance vector search with filtering
2. Rich data types and payload support
3. Distributed deployment capabilities
4. Real-time updates without rebuilding indexes
5. Advanced filtering with complex conditions
6. Snapshot and collection management

This vector store is particularly useful when:
- You need production-grade vector search with filtering
- Want to combine vector similarity with attribute filtering
- Need distributed and scalable vector search
- Require real-time updates to your vector data
- Building complex search applications with metadata

The implementation integrates with LangChain's Qdrant while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.QDRANT)
class QdrantVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """Configuration for Qdrant vector store in the Haive framework.

    This vector store uses Qdrant for high-performance vector similarity search
    with advanced filtering capabilities and production-ready features.

    Attributes:
        url (Optional[str]): URL of the Qdrant instance.
        api_key (Optional[SecretStr]): API key for Qdrant Cloud (auto-resolved).
        host (Optional[str]): Host for local Qdrant instance.
        port (Optional[int]): Port for local Qdrant instance.
        grpc_port (Optional[int]): gRPC port for better performance.
        prefer_grpc (bool): Whether to prefer gRPC over HTTP.
        https (bool): Whether to use HTTPS for connections.
        distance_metric (str): Distance metric for similarity.
        vector_size (Optional[int]): Size of the embedding vectors.
        on_disk (bool): Whether to store vectors on disk.

    Examples:
        >>> from haive.core.engine.vectorstore import QdrantVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Qdrant config for cloud deployment
        >>> config = QdrantVectorStoreConfig(
        ...     name="product_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     url="https://xyz-123.aws.cloud.qdrant.io",
        ...     collection_name="products",
        ...     distance_metric="cosine"
        ... )
        >>>
        >>> # Create Qdrant config for local deployment
        >>> local_config = QdrantVectorStoreConfig(
        ...     name="local_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     host="localhost",
        ...     port=6333,
        ...     collection_name="documents"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Qdrant enables filtered search")]
        >>> vectorstore.add_documents(docs)
    """

    # Connection configuration
    url: str | None = Field(
        default=None, description="URL of the Qdrant instance (for Qdrant Cloud)"
    )

    api_key: SecretStr | None = Field(
        default=None,
        description="API key for Qdrant Cloud (auto-resolved from QDRANT_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="qdrant", description="Provider name for API key resolution"
    )

    # Local deployment configuration
    host: str | None = Field(default=None, description="Host for local Qdrant instance")

    port: int | None = Field(default=6333, description="Port for local Qdrant instance")

    grpc_port: int | None = Field(
        default=6334, description="gRPC port for better performance"
    )

    prefer_grpc: bool = Field(
        default=False, description="Whether to prefer gRPC over HTTP"
    )

    https: bool = Field(
        default=False, description="Whether to use HTTPS for local connections"
    )

    # Collection configuration
    distance_metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'euclidean', 'dot', or 'manhattan'",
    )

    vector_size: int | None = Field(
        default=None,
        description="Size of the embedding vectors (auto-detected if not specified)",
    )

    on_disk: bool = Field(
        default=False,
        description="Whether to store vectors on disk (for large collections)",
    )

    # Advanced configuration
    shard_number: int = Field(
        default=1, ge=1, description="Number of shards for the collection"
    )

    replication_factor: int = Field(
        default=1, ge=1, description="Replication factor for the collection"
    )

    write_consistency_factor: int = Field(
        default=1, ge=1, description="Write consistency factor"
    )

    timeout: int | None = Field(
        default=None, description="Timeout for operations in seconds"
    )

    @validator("distance_metric")
    def validate_distance_metric(self, v):
        """Validate distance metric is supported."""
        valid_metrics = ["cosine", "euclidean", "dot", "manhattan"]
        if v not in valid_metrics:
            raise ValueError(f"distance_metric must be one of {valid_metrics}, got {v}")
        return v

    @validator("url", "host")
    def validate_connection(self, v, values):
        """Validate that either url or host is provided."""
        if not v and not values.get("url") and not values.get("host"):
            raise ValueError("Either 'url' or 'host' must be provided")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Qdrant vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Qdrant vector store."""
        return {
            "ids": (list[str], Field(description="IDs of the added documents")),
        }

    def instantiate(self):
        """Create a Qdrant vector store from this configuration.

        Returns:
            Qdrant: Instantiated Qdrant vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_qdrant import Qdrant
        except ImportError:
            try:
                from langchain_community.vectorstores import Qdrant
            except ImportError:
                raise ImportError(
                    "Qdrant requires qdrant-client package. "
                    "Install with: pip install qdrant-client"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key if using cloud
        api_key = None
        if self.url:
            api_key = self.get_api_key()

        # Map distance metric to Qdrant's expected format
        from qdrant_client.models import Distance

        distance_mapping = {
            "cosine": Distance.COSINE,
            "euclidean": Distance.EUCLID,
            "dot": Distance.DOT,
            "manhattan": Distance.MANHATTAN,
        }

        # Prepare client kwargs
        client_kwargs = {}

        if self.url:
            client_kwargs["url"] = self.url
            if api_key:
                client_kwargs["api_key"] = api_key
        else:
            # Local deployment
            client_kwargs["host"] = self.host or "localhost"
            client_kwargs["port"] = self.port
            client_kwargs["grpc_port"] = self.grpc_port
            client_kwargs["prefer_grpc"] = self.prefer_grpc
            client_kwargs["https"] = self.https

        if self.timeout:
            client_kwargs["timeout"] = self.timeout

        # Create Qdrant client
        from qdrant_client import QdrantClient

        client = QdrantClient(**client_kwargs)

        # Check if collection exists, create if not
        try:
            client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            if self.vector_size:
                vector_size = self.vector_size
            else:
                # Try to get vector size from embedding
                try:
                    sample_embedding = embedding_function.embed_query("sample text")
                    vector_size = len(sample_embedding)
                except Exception:
                    raise ValueError(
                        "Could not determine vector size. Please specify 'vector_size' parameter."
                    )

            from qdrant_client.models import VectorParams

            client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=distance_mapping[self.distance_metric],
                    on_disk=self.on_disk,
                ),
                shard_number=self.shard_number,
                replication_factor=self.replication_factor,
                write_consistency_factor=self.write_consistency_factor,
            )

        # Create Qdrant instance
        return Qdrant(
            client=client,
            collection_name=self.collection_name,
            embeddings=embedding_function,
        )
