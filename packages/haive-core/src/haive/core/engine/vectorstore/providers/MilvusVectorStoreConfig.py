"""Milvus Vector Store implementation for the Haive framework.

This module provides a configuration class for the Milvus vector store,
which is a cloud-native vector database built for scalable similarity search.

Milvus provides:
1. Billion-scale vector similarity search
2. Hybrid search with attribute filtering
3. Multiple index types for different scenarios
4. Distributed architecture with high availability
5. GPU acceleration support
6. Time Travel for data versioning

This vector store is particularly useful when:
- You need to handle billion-scale vector datasets
- Require high availability and horizontal scaling
- Need hybrid search with metadata filtering
- Want GPU acceleration for indexing and search
- Building large-scale recommendation or search systems

The implementation integrates with LangChain's Milvus while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.MILVUS)
class MilvusVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for Milvus vector store in the Haive framework.

    This vector store uses Milvus for billion-scale vector similarity search
    with distributed architecture and advanced indexing options.

    Attributes:
        connection_args (Dict[str, Any]): Connection parameters for Milvus.
        collection_name (str): Name of the Milvus collection.
        index_params (Dict[str, Any]): Index configuration parameters.
        search_params (Dict[str, Any]): Search configuration parameters.
        consistency_level (str): Consistency level for operations.
        drop_old (bool): Whether to drop existing collection.

    Examples:
        >>> from haive.core.engine.vectorstore import MilvusVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Milvus config for cloud deployment
        >>> config = MilvusVectorStoreConfig(
        ...     name="large_scale_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     connection_args={
        ...         "uri": "https://milvus-instance.api.aws.com",
        ...         "token": "your-token"
        ...     },
        ...     collection_name="products",
        ...     index_params={
        ...         "metric_type": "L2",
        ...         "index_type": "IVF_FLAT",
        ...         "params": {"nlist": 1024}
        ...     }
        ... )
        >>>
        >>> # Create config for local deployment
        >>> local_config = MilvusVectorStoreConfig(
        ...     name="local_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     connection_args={
        ...         "host": "localhost",
        ...         "port": "19530"
        ...     },
        ...     collection_name="documents"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Milvus handles billion-scale vectors")]
        >>> vectorstore.add_documents(docs)
    """

    # Connection configuration
    connection_args: dict[str, Any] = Field(
        ...,
        description="Connection parameters: {'host': 'localhost', 'port': '19530'} or {'uri': '...', 'token': '...'}",
    )

    # Collection configuration
    drop_old: bool = Field(
        default=False, description="Whether to drop existing collection with same name"
    )

    # Index configuration
    index_params: dict[str, Any] | None = Field(
        default=None,
        description="Index parameters: {'metric_type': 'L2', 'index_type': 'IVF_FLAT', 'params': {...}}",
    )

    search_params: dict[str, Any] | None = Field(
        default=None,
        description="Search parameters: {'metric_type': 'L2', 'params': {'nprobe': 10}}",
    )

    # Consistency configuration
    consistency_level: str = Field(
        default="Session",
        description="Consistency level: 'Strong', 'Session', 'Bounded', 'Eventually'",
    )

    # Collection schema configuration
    primary_field: str = Field(
        default="pk", description="Name of the primary key field"
    )

    text_field: str = Field(default="text", description="Name of the text field")

    vector_field: str = Field(default="vector", description="Name of the vector field")

    # Advanced configuration
    auto_id: bool = Field(default=True, description="Whether to auto-generate IDs")

    partition_key_field: str | None = Field(
        default=None, description="Field to use for partitioning"
    )

    partition_names: list[str] | None = Field(
        default=None, description="List of partition names to create"
    )

    replica_number: int = Field(default=1, ge=1, description="Number of replicas")

    timeout: float | None = Field(
        default=None, description="Timeout for operations in seconds"
    )

    @validator("consistency_level")
    def validate_consistency_level(self, v):
        """Validate consistency level is supported."""
        valid_levels = ["Strong", "Session", "Bounded", "Eventually"]
        if v not in valid_levels:
            raise ValueError(
                f"consistency_level must be one of {valid_levels}, got {v}"
            )
        return v

    @validator("connection_args")
    def validate_connection_args(self, v):
        """Validate connection arguments."""
        if not v:
            raise ValueError("connection_args must be provided")

        # Check for cloud connection (uri + token) or local connection (host + port)
        has_cloud = "uri" in v
        has_local = "host" in v and "port" in v

        if not has_cloud and not has_local:
            raise ValueError(
                "connection_args must contain either {'uri': '...', 'token': '...'} "
                "for cloud or {'host': '...', 'port': '...'} for local deployment"
            )

        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Milvus vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Milvus vector store."""
        return {
            "ids": (
                list[str | int],
                Field(description="IDs of the added documents"),
            ),
        }

    def instantiate(self):
        """Create a Milvus vector store from this configuration.

        Returns:
            Milvus: Instantiated Milvus vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_milvus import Milvus
        except ImportError:
            try:
                from langchain_community.vectorstores import Milvus
            except ImportError:
                raise ImportError(
                    "Milvus requires pymilvus package. "
                    "Install with: pip install pymilvus"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Prepare index params with defaults if not provided
        if not self.index_params:
            index_params = {
                "metric_type": "L2",
                "index_type": "IVF_FLAT",
                "params": {"nlist": 1024},
            }
        else:
            index_params = self.index_params

        # Prepare search params with defaults if not provided
        if not self.search_params:
            search_params = {
                "metric_type": index_params.get("metric_type", "L2"),
                "params": {"nprobe": 10},
            }
        else:
            search_params = self.search_params

        # Prepare kwargs
        kwargs = {
            "embedding_function": embedding_function,
            "collection_name": self.collection_name,
            "connection_args": self.connection_args,
            "consistency_level": self.consistency_level,
            "index_params": index_params,
            "search_params": search_params,
            "drop_old": self.drop_old,
            "auto_id": self.auto_id,
            "primary_field": self.primary_field,
            "text_field": self.text_field,
            "vector_field": self.vector_field,
        }

        # Add optional parameters
        if self.partition_key_field:
            kwargs["partition_key_field"] = self.partition_key_field

        if self.partition_names:
            kwargs["partition_names"] = self.partition_names

        if self.replica_number > 1:
            kwargs["replica_number"] = self.replica_number

        if self.timeout:
            kwargs["timeout"] = self.timeout

        # Create Milvus instance
        return Milvus(**kwargs)
