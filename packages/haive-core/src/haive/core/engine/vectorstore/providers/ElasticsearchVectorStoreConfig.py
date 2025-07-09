"""
Elasticsearch Vector Store implementation for the Haive framework.

This module provides a configuration class for the Elasticsearch vector store,
which combines traditional text search with vector similarity search capabilities.

Elasticsearch provides:
1. Hybrid search combining BM25 and vector similarity
2. Distributed search across multiple nodes
3. Real-time indexing and search
4. Rich query DSL with vector operations
5. Aggregations and analytics on vector data
6. Enterprise security and monitoring

This vector store is particularly useful when:
- You need both text search and vector similarity
- Want to leverage existing Elasticsearch infrastructure
- Need distributed search at scale
- Require complex queries combining multiple search types
- Building applications with rich search analytics

The implementation integrates with LangChain's Elasticsearch while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.ELASTICSEARCH)
class ElasticsearchVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for Elasticsearch vector store in the Haive framework.

    This vector store uses Elasticsearch for hybrid search combining
    traditional text search with vector similarity capabilities.

    Attributes:
        elasticsearch_url (str): Elasticsearch cluster URL.
        index_name (str): Name of the Elasticsearch index.
        embedding_field (str): Field name for storing embeddings.
        text_field (str): Field name for storing document text.
        metadata_field (str): Field name for storing metadata.
        distance_strategy (str): Distance metric for vector similarity.

    Examples:
        >>> from haive.core.engine.vectorstore import ElasticsearchVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Elasticsearch config
        >>> config = ElasticsearchVectorStoreConfig(
        ...     name="elastic_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     elasticsearch_url="http://localhost:9200",
        ...     index_name="documents",
        ...     distance_strategy="cosine"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Elasticsearch combines text and vector search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Hybrid search capabilities
        >>> results = vectorstore.similarity_search("search technology", k=5)
    """

    # Elasticsearch connection configuration
    elasticsearch_url: str = Field(
        default="http://localhost:9200", description="Elasticsearch cluster URL"
    )

    # Authentication (optional)
    username: Optional[str] = Field(
        default=None, description="Username for Elasticsearch authentication"
    )

    password: Optional[str] = Field(
        default=None, description="Password for Elasticsearch authentication"
    )

    api_key: Optional[str] = Field(
        default=None, description="API key for Elasticsearch authentication"
    )

    # Index configuration
    index_name: str = Field(
        default="langchain-index", description="Name of the Elasticsearch index"
    )

    # Field mappings
    embedding_field: str = Field(
        default="vector", description="Field name for storing embedding vectors"
    )

    text_field: str = Field(
        default="text", description="Field name for storing document text"
    )

    metadata_field: str = Field(
        default="metadata", description="Field name for storing document metadata"
    )

    # Vector configuration
    distance_strategy: str = Field(
        default="cosine",
        description="Distance strategy: 'cosine', 'euclidean', 'dot_product', or 'max_inner_product'",
    )

    # Index settings
    create_index_if_not_exists: bool = Field(
        default=True, description="Whether to create the index if it doesn't exist"
    )

    number_of_shards: int = Field(
        default=1, ge=1, description="Number of primary shards for the index"
    )

    number_of_replicas: int = Field(
        default=1, ge=0, description="Number of replica shards for the index"
    )

    # Connection settings
    timeout: int = Field(default=60, ge=1, description="Request timeout in seconds")

    max_retries: int = Field(
        default=3, ge=0, description="Maximum number of retries for failed requests"
    )

    # SSL configuration
    use_ssl: bool = Field(
        default=False, description="Whether to use SSL for connections"
    )

    verify_certs: bool = Field(
        default=True, description="Whether to verify SSL certificates"
    )

    ca_certs: Optional[str] = Field(
        default=None, description="Path to CA certificates file"
    )

    @validator("distance_strategy")
    def validate_distance_strategy(cls, v):
        """Validate distance strategy is supported."""
        valid_strategies = ["cosine", "euclidean", "dot_product", "max_inner_product"]
        if v not in valid_strategies:
            raise ValueError(
                f"distance_strategy must be one of {valid_strategies}, got {v}"
            )
        return v

    @validator("elasticsearch_url")
    def validate_elasticsearch_url(cls, v):
        """Basic validation of Elasticsearch URL."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("elasticsearch_url must start with http:// or https://")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Elasticsearch vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Elasticsearch vector store."""
        return {
            "ids": (List[str], Field(description="Document IDs in Elasticsearch")),
        }

    def instantiate(self):
        """
        Create an Elasticsearch vector store from this configuration.

        Returns:
            ElasticsearchStore: Instantiated Elasticsearch vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_elasticsearch import ElasticsearchStore
        except ImportError:
            try:
                from langchain_community.vectorstores import ElasticsearchStore
            except ImportError:
                raise ImportError(
                    "Elasticsearch requires elasticsearch package. "
                    "Install with: pip install elasticsearch"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare authentication
        auth = None
        if self.username and self.password:
            auth = (self.username, self.password)
        elif self.api_key:
            auth = {"api_key": self.api_key}

        # Prepare SSL configuration
        ssl_context = None
        if self.use_ssl:
            import ssl

            ssl_context = ssl.create_default_context()
            if not self.verify_certs:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            elif self.ca_certs:
                ssl_context.load_verify_locations(self.ca_certs)

        # Prepare Elasticsearch client configuration
        es_config = {
            "hosts": [self.elasticsearch_url],
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }

        if auth:
            if isinstance(auth, tuple):
                es_config["http_auth"] = auth
            else:
                es_config.update(auth)

        if ssl_context:
            es_config["ssl_context"] = ssl_context

        # Create Elasticsearch client
        try:
            from elasticsearch import Elasticsearch

            es_client = Elasticsearch(**es_config)

            # Test connection
            es_client.ping()

        except Exception as e:
            raise ValueError(f"Failed to connect to Elasticsearch: {e}")

        # Get vector dimensions for index mapping
        vector_dims = None
        try:
            sample_embedding = embedding_function.embed_query("sample")
            vector_dims = len(sample_embedding)
        except Exception:
            vector_dims = 1536  # Default dimension

        # Prepare vector store kwargs
        kwargs = {
            "index_name": self.index_name,
            "embedding": embedding_function,
            "es_connection": es_client,
            "vector_query_field": self.embedding_field,
            "query_field": self.text_field,
            "distance_strategy": self.distance_strategy,
        }

        # Create index if it doesn't exist
        if self.create_index_if_not_exists and not es_client.indices.exists(
            index=self.index_name
        ):
            # Create index mapping
            mapping = {
                "mappings": {
                    "properties": {
                        self.text_field: {"type": "text"},
                        self.metadata_field: {"type": "object"},
                        self.embedding_field: {
                            "type": "dense_vector",
                            "dims": vector_dims,
                            "index": True,
                            "similarity": self.distance_strategy,
                        },
                    }
                },
                "settings": {
                    "number_of_shards": self.number_of_shards,
                    "number_of_replicas": self.number_of_replicas,
                    "index": {"knn": True},
                },
            }

            try:
                es_client.indices.create(index=self.index_name, body=mapping)
            except Exception as e:
                import warnings

                warnings.warn(f"Could not create index: {e}")

        # Create Elasticsearch vector store
        return ElasticsearchStore(**kwargs)
