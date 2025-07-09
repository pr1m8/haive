"""
Zilliz Cloud Vector Store implementation for the Haive framework.

This module provides a configuration class for the Zilliz Cloud vector store,
which is a fully managed cloud-native vector database service based on Milvus.

Zilliz Cloud provides:
1. Fully managed Milvus service with zero operations
2. Auto-scaling and high availability
3. Enterprise security and compliance
4. Global deployment across multiple cloud providers
5. Pay-as-you-go pricing model
6. All Milvus features in a managed environment

This vector store is particularly useful when:
- You want Milvus capabilities without managing infrastructure
- Need enterprise-grade managed vector database
- Require global deployment and data residency
- Want automatic scaling based on workload
- Building production applications with SLA requirements

The implementation integrates with LangChain's Zilliz while providing
a consistent Haive configuration interface with secure credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.ZILLIZ)
class ZillizVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """
    Configuration for Zilliz Cloud vector store in the Haive framework.

    This vector store uses Zilliz Cloud for managed Milvus service with
    enterprise features and automatic scaling.

    Attributes:
        connection_args (Dict[str, Any]): Connection parameters including URI and token.
        api_key (Optional[SecretStr]): Zilliz Cloud API key (auto-resolved).
        collection_name (str): Name of the Zilliz collection.
        index_params (Dict[str, Any]): Index configuration parameters.
        consistency_level (str): Consistency level for operations.

    Examples:
        >>> from haive.core.engine.vectorstore import ZillizVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Zilliz config
        >>> config = ZillizVectorStoreConfig(
        ...     name="cloud_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     connection_args={
        ...         "uri": "https://your-cluster.zillizcloud.com",
        ...         "secure": True
        ...     },
        ...     collection_name="products",
        ...     index_params={
        ...         "metric_type": "L2",
        ...         "index_type": "AUTOINDEX"
        ...     }
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Zilliz Cloud manages Milvus for you")]
        >>> vectorstore.add_documents(docs)
    """

    # Connection configuration
    connection_args: Dict[str, Any] = Field(
        ...,
        description="Connection parameters: must include 'uri' and optionally 'token', 'secure'",
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Zilliz Cloud API key/token (auto-resolved from ZILLIZ_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="zilliz", description="Provider name for API key resolution"
    )

    # Collection configuration (inherits collection_name from base)
    drop_old: bool = Field(
        default=False, description="Whether to drop existing collection with same name"
    )

    # Index configuration
    index_params: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Index parameters: {'metric_type': 'L2', 'index_type': 'AUTOINDEX'}",
    )

    search_params: Optional[Dict[str, Any]] = Field(
        default=None, description="Search parameters for queries"
    )

    # Consistency configuration
    consistency_level: str = Field(
        default="Session",
        description="Consistency level: 'Strong', 'Session', 'Bounded', 'Eventually'",
    )

    # Schema configuration
    primary_field: str = Field(
        default="pk", description="Name of the primary key field"
    )

    text_field: str = Field(default="text", description="Name of the text field")

    vector_field: str = Field(default="vector", description="Name of the vector field")

    # Advanced configuration
    auto_id: bool = Field(default=True, description="Whether to auto-generate IDs")

    timeout: Optional[float] = Field(
        default=None, description="Timeout for operations in seconds"
    )

    @validator("consistency_level")
    def validate_consistency_level(cls, v):
        """Validate consistency level is supported."""
        valid_levels = ["Strong", "Session", "Bounded", "Eventually"]
        if v not in valid_levels:
            raise ValueError(
                f"consistency_level must be one of {valid_levels}, got {v}"
            )
        return v

    @validator("connection_args")
    def validate_connection_args(cls, v):
        """Validate connection arguments."""
        if not v:
            raise ValueError("connection_args must be provided")

        if "uri" not in v:
            raise ValueError(
                "connection_args must contain 'uri' for Zilliz Cloud endpoint"
            )

        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Zilliz vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Zilliz vector store."""
        return {
            "ids": (
                List[Union[str, int]],
                Field(description="IDs of the added documents"),
            ),
        }

    def instantiate(self):
        """
        Create a Zilliz vector store from this configuration.

        Returns:
            Zilliz: Instantiated Zilliz vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import Zilliz
        except ImportError:
            raise ImportError(
                "Zilliz requires pymilvus package. "
                "Install with: pip install pymilvus"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key/token using SecureConfigMixin
        api_key = self.get_api_key()

        # Update connection args with token if available
        connection_args = self.connection_args.copy()
        if api_key and "token" not in connection_args:
            connection_args["token"] = api_key

        # Ensure secure connection for Zilliz Cloud
        if "secure" not in connection_args:
            connection_args["secure"] = True

        # Prepare index params with defaults if not provided
        if not self.index_params:
            index_params = {
                "metric_type": "L2",
                "index_type": "AUTOINDEX",  # Zilliz Cloud recommends AUTOINDEX
            }
        else:
            index_params = self.index_params

        # Prepare search params with defaults if not provided
        if not self.search_params:
            search_params = {"metric_type": index_params.get("metric_type", "L2")}
        else:
            search_params = self.search_params

        # Prepare kwargs
        kwargs = {
            "embedding_function": embedding_function,
            "collection_name": self.collection_name,
            "connection_args": connection_args,
            "consistency_level": self.consistency_level,
            "index_params": index_params,
            "search_params": search_params,
            "drop_old": self.drop_old,
            "auto_id": self.auto_id,
            "primary_field": self.primary_field,
            "text_field": self.text_field,
            "vector_field": self.vector_field,
        }

        if self.timeout:
            kwargs["timeout"] = self.timeout

        # Create Zilliz instance
        return Zilliz(**kwargs)
