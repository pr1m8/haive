"""Pinecone Vector Store implementation for the Haive framework.

This module provides a configuration class for the Pinecone vector store,
which is a fully managed vector database service designed for production workloads.

Pinecone provides:
1. Fully managed cloud-native vector database
2. Real-time data ingestion with low-latency queries
3. Metadata filtering and hybrid search
4. Automatic scaling and high availability
5. Enterprise-grade security and compliance
6. Simple API with minimal operational overhead

This vector store is particularly useful when:
- You need a production-ready managed vector database
- Want to avoid infrastructure management
- Need guaranteed performance and availability
- Require enterprise features like SSO and audit logs
- Building applications that need to scale seamlessly

The implementation integrates with LangChain's Pinecone while providing
a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.PINECONE)
class PineconeVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """Configuration for Pinecone vector store in the Haive framework.

    This vector store uses Pinecone's managed service for scalable vector
    similarity search with enterprise-grade features.

    Attributes:
        api_key (Optional[SecretStr]): Pinecone API key (auto-resolved).
        environment (Optional[str]): Pinecone environment/region.
        index_name (str): Name of the Pinecone index.
        namespace (Optional[str]): Namespace within the index.
        text_key (str): Metadata key for document text.
        distance_metric (str): Distance metric (configured at index level).

    Examples:
        >>> from haive.core.engine.vectorstore import PineconeVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Pinecone config
        >>> config = PineconeVectorStoreConfig(
        ...     name="production_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     index_name="my-index",
        ...     namespace="documents",
        ...     text_key="content"
        ... )
        >>>
        >>> # Instantiate and use the vector store
        >>> vectorstore = config.instantiate()
        >>>
        >>> # Add documents
        >>> docs = [Document(page_content="Pinecone scales automatically")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Search with metadata filtering
        >>> results = vectorstore.similarity_search(
        ...     "scalable vector search",
        ...     k=5,
        ...     filter={"category": "database"}
        ... )
    """

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None,
        description="Pinecone API key (auto-resolved from PINECONE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="pinecone", description="Provider name for API key resolution"
    )

    # Pinecone configuration
    environment: str | None = Field(
        default=None,
        description="Pinecone environment (deprecated in newer versions, optional)",
    )

    index_name: str = Field(..., description="Name of the Pinecone index to use")

    namespace: str | None = Field(
        default=None, description="Namespace within the index for data isolation"
    )

    text_key: str = Field(
        default="text", description="Metadata key where document text is stored"
    )

    # Connection pool settings
    pool_threads: int = Field(
        default=1, ge=1, description="Number of threads for connection pool"
    )

    # Timeout settings
    timeout: int | None = Field(
        default=None, description="Timeout for Pinecone operations in seconds"
    )

    # Index configuration (used only when creating new index)
    dimension: int | None = Field(
        default=None, description="Vector dimension (required only for index creation)"
    )

    metric: str = Field(
        default="cosine",
        description="Distance metric: 'cosine', 'euclidean', or 'dotproduct'",
    )

    pod_type: str = Field(
        default="p1.x1", description="Pod type for index (used only during creation)"
    )

    replicas: int = Field(
        default=1, ge=1, description="Number of replicas (used only during creation)"
    )

    @validator("metric")
    def validate_metric(self, v):
        """Validate distance metric is supported."""
        valid_metrics = ["cosine", "euclidean", "dotproduct"]
        if v not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}, got {v}")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Pinecone vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Pinecone vector store."""
        return {
            "ids": (list[str], Field(description="IDs of the added documents")),
        }

    def instantiate(self):
        """Create a Pinecone vector store from this configuration.

        Returns:
            Pinecone: Instantiated Pinecone vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_pinecone import PineconeVectorStore as Pinecone
        except ImportError:
            try:
                from langchain_community.vectorstores import Pinecone
            except ImportError:
                raise ImportError(
                    "Pinecone requires pinecone-client package. "
                    "Install with: pip install pinecone-client"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Pinecone API key is required. Set PINECONE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Initialize Pinecone
        try:
            import pinecone

            # For newer versions of pinecone-client (2.0+)
            if hasattr(pinecone, "Pinecone"):
                pc = pinecone.Pinecone(api_key=api_key, pool_threads=self.pool_threads)

                # Check if index exists
                if self.index_name not in pc.list_indexes().names():
                    # Create index if it doesn't exist
                    if not self.dimension:
                        # Try to get dimension from embedding
                        try:
                            sample_embedding = embedding_function.embed_query("sample")
                            dimension = len(sample_embedding)
                        except Exception:
                            raise ValueError(
                                "Could not determine vector dimension. "
                                "Please specify 'dimension' parameter for index creation."
                            )
                    else:
                        dimension = self.dimension

                    pc.create_index(
                        name=self.index_name,
                        dimension=dimension,
                        metric=self.metric,
                        spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"),
                    )

                # Get index
                index = pc.Index(self.index_name)

            else:
                # For older versions of pinecone-client
                pinecone.init(
                    api_key=api_key, environment=self.environment or "us-west1-gcp"
                )

                # Check if index exists
                if self.index_name not in pinecone.list_indexes():
                    # Create index if needed
                    if not self.dimension:
                        try:
                            sample_embedding = embedding_function.embed_query("sample")
                            dimension = len(sample_embedding)
                        except Exception:
                            raise ValueError(
                                "Could not determine vector dimension. "
                                "Please specify 'dimension' parameter."
                            )
                    else:
                        dimension = self.dimension

                    pinecone.create_index(
                        name=self.index_name,
                        dimension=dimension,
                        metric=self.metric,
                        pod_type=self.pod_type,
                        replicas=self.replicas,
                    )

                index = pinecone.Index(self.index_name)

        except Exception as e:
            raise ValueError(f"Failed to initialize Pinecone: {e}")

        # Create vector store kwargs
        kwargs = {
            "index": index,
            "embedding": embedding_function,
            "text_key": self.text_key,
        }

        if self.namespace:
            kwargs["namespace"] = self.namespace

        # Create Pinecone vector store
        return Pinecone(**kwargs)
