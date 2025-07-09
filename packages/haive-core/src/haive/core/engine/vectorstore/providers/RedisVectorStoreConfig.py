"""
Redis Vector Store implementation for the Haive framework.

This module provides a configuration class for the Redis vector store,
which combines in-memory caching with vector similarity search capabilities.

Redis provides:
1. Ultra-fast in-memory vector operations
2. Real-time vector search with sub-millisecond latency
3. Hybrid data structures (vectors + traditional Redis types)
4. Distributed caching and session storage
5. Pub/Sub for real-time vector updates
6. Enterprise clustering and persistence

This vector store is particularly useful when:
- You need extremely low-latency vector search
- Want to cache vector embeddings for performance
- Building real-time recommendation systems
- Need to combine vectors with session data
- Require high-throughput vector operations

The implementation integrates with LangChain's Redis while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.REDIS)
class RedisVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for Redis vector store in the Haive framework.

    This vector store uses Redis for ultra-fast in-memory vector
    similarity search with caching capabilities.

    Attributes:
        redis_url (str): Redis connection URL.
        index_name (str): Name of the Redis search index.
        distance_metric (str): Distance metric for vector similarity.
        vector_field_name (str): Field name for storing vectors.
        content_field_name (str): Field name for storing content.

    Examples:
        >>> from haive.core.engine.vectorstore import RedisVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Redis config
        >>> config = RedisVectorStoreConfig(
        ...     name="redis_cache",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     redis_url="redis://localhost:6379",
        ...     index_name="doc_embeddings",
        ...     distance_metric="COSINE"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Redis provides fast vector search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Ultra-fast vector search
        >>> results = vectorstore.similarity_search("fast search", k=5)
    """

    # Redis connection configuration
    redis_url: str = Field(
        default="redis://localhost:6379", description="Redis connection URL"
    )

    # Alternative connection parameters
    host: Optional[str] = Field(
        default=None, description="Redis host (alternative to redis_url)"
    )

    port: Optional[int] = Field(
        default=None, description="Redis port (alternative to redis_url)"
    )

    password: Optional[str] = Field(default=None, description="Redis password")

    db: int = Field(default=0, ge=0, description="Redis database number")

    # Index configuration
    index_name: str = Field(
        default="langchain_redis_index", description="Name of the Redis search index"
    )

    # Field configuration
    vector_field_name: str = Field(
        default="content_vector", description="Field name for storing embedding vectors"
    )

    content_field_name: str = Field(
        default="content", description="Field name for storing document content"
    )

    metadata_field_name: str = Field(
        default="metadata", description="Field name for storing document metadata"
    )

    # Vector configuration
    distance_metric: str = Field(
        default="COSINE",
        description="Distance metric: 'COSINE', 'L2', or 'IP' (inner product)",
    )

    vector_algorithm: str = Field(
        default="HNSW", description="Vector indexing algorithm: 'HNSW' or 'FLAT'"
    )

    # HNSW specific parameters
    m: int = Field(
        default=16,
        ge=2,
        description="HNSW M parameter (number of bi-directional links)",
    )

    ef_construction: int = Field(
        default=200, ge=1, description="HNSW ef_construction parameter"
    )

    ef_runtime: int = Field(
        default=10, ge=1, description="HNSW ef_runtime parameter for search"
    )

    # Index management
    drop_index_if_exists: bool = Field(
        default=False,
        description="Whether to drop existing index before creating new one",
    )

    # Connection settings
    socket_timeout: float = Field(
        default=30.0, ge=0.1, description="Socket timeout in seconds"
    )

    socket_connect_timeout: float = Field(
        default=30.0, ge=0.1, description="Socket connect timeout in seconds"
    )

    retry_on_timeout: bool = Field(
        default=True, description="Whether to retry on timeout"
    )

    @validator("distance_metric")
    def validate_distance_metric(cls, v):
        """Validate distance metric is supported."""
        valid_metrics = ["COSINE", "L2", "IP"]
        if v not in valid_metrics:
            raise ValueError(f"distance_metric must be one of {valid_metrics}, got {v}")
        return v

    @validator("vector_algorithm")
    def validate_vector_algorithm(cls, v):
        """Validate vector algorithm is supported."""
        valid_algorithms = ["HNSW", "FLAT"]
        if v not in valid_algorithms:
            raise ValueError(
                f"vector_algorithm must be one of {valid_algorithms}, got {v}"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Redis vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Redis vector store."""
        return {
            "ids": (List[str], Field(description="Redis document IDs")),
        }

    def instantiate(self):
        """
        Create a Redis vector store from this configuration.

        Returns:
            Redis: Instantiated Redis vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores.redis import Redis
        except ImportError:
            raise ImportError(
                "Redis requires redis package. " "Install with: pip install redis"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare Redis connection arguments
        if self.host and self.port:
            # Use individual connection parameters
            redis_args = {
                "host": self.host,
                "port": self.port,
                "db": self.db,
                "socket_timeout": self.socket_timeout,
                "socket_connect_timeout": self.socket_connect_timeout,
                "retry_on_timeout": self.retry_on_timeout,
            }
            if self.password:
                redis_args["password"] = self.password
        else:
            # Use Redis URL
            redis_args = {
                "url": self.redis_url,
                "socket_timeout": self.socket_timeout,
                "socket_connect_timeout": self.socket_connect_timeout,
                "retry_on_timeout": self.retry_on_timeout,
            }

        # Create Redis client
        try:
            import redis

            redis_client = redis.Redis(**redis_args)

            # Test connection
            redis_client.ping()

        except Exception as e:
            raise ValueError(f"Failed to connect to Redis: {e}")

        # Get vector dimensions
        try:
            sample_embedding = embedding_function.embed_query("sample")
            vector_dim = len(sample_embedding)
        except Exception:
            vector_dim = 1536  # Default dimension

        # Prepare vector store kwargs
        kwargs = {
            "redis_client": redis_client,
            "embedding": embedding_function,
            "index_name": self.index_name,
            "content_key": self.content_field_name,
            "metadata_key": self.metadata_field_name,
            "vector_key": self.vector_field_name,
            "distance_metric": self.distance_metric,
        }

        # Add algorithm-specific parameters
        index_schema = {
            "algorithm": self.vector_algorithm,
            "vector_data_type": "FLOAT32",
            "vector_dim": vector_dim,
            "distance_metric": self.distance_metric,
        }

        if self.vector_algorithm == "HNSW":
            index_schema.update(
                {
                    "m": self.m,
                    "ef_construction": self.ef_construction,
                    "ef_runtime": self.ef_runtime,
                }
            )

        kwargs["index_schema"] = index_schema

        # Handle index creation/deletion
        if self.drop_index_if_exists:
            try:
                # Drop index if it exists
                redis_client.ft(self.index_name).dropindex(delete_documents=True)
            except Exception:
                # Index might not exist
                pass

        # Create Redis vector store
        try:
            vectorstore = Redis.from_existing_index(
                embedding=embedding_function,
                index_name=self.index_name,
                redis_url=self.redis_url if not (self.host and self.port) else None,
                **(
                    {k: v for k, v in redis_args.items() if k != "url"}
                    if self.host and self.port
                    else {}
                ),
            )
        except Exception:
            # If index doesn't exist, create new one
            vectorstore = Redis(
                redis_url=self.redis_url if not (self.host and self.port) else None,
                index_name=self.index_name,
                embedding_function=embedding_function,
                **kwargs,
            )

        return vectorstore
