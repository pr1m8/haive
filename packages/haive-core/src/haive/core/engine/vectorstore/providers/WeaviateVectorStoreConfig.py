"""Weaviate Vector Store implementation for the Haive framework.

This module provides a configuration class for the Weaviate vector store,
which is an open-source vector database with built-in modules for ML.

Weaviate provides:
1. GraphQL and RESTful APIs for querying
2. Built-in vectorization modules
3. Hybrid search combining vector and keyword search
4. Real-time data updates
5. Horizontal scalability
6. Multi-tenancy support

This vector store is particularly useful when:
- You need a full-featured vector database with GraphQL support
- Want built-in ML modules for vectorization
- Need hybrid search capabilities
- Require multi-tenancy or access control
- Building knowledge graphs with vector search

The implementation integrates with LangChain's Weaviate while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.WEAVIATE)
class WeaviateVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """Configuration for Weaviate vector store in the Haive framework.

    This vector store uses Weaviate for advanced vector search with
    GraphQL support and built-in ML capabilities.

    Attributes:
        url (str): URL of the Weaviate instance.
        api_key (Optional[SecretStr]): API key for Weaviate Cloud (auto-resolved).
        index_name (str): Name of the Weaviate class/index.
        text_key (str): Property name for document text.
        use_embedded (bool): Use embedded Weaviate instance.
        additional_headers (Dict[str, str]): Additional HTTP headers.

    Examples:
        >>> from haive.core.engine.vectorstore import WeaviateVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Weaviate config for cloud deployment
        >>> config = WeaviateVectorStoreConfig(
        ...     name="knowledge_base",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     url="https://my-cluster.weaviate.network",
        ...     index_name="Documents",
        ...     text_key="content"
        ... )
        >>>
        >>> # Create config for local embedded instance
        >>> local_config = WeaviateVectorStoreConfig(
        ...     name="local_kb",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     use_embedded=True,
        ...     index_name="LocalDocs"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Weaviate supports GraphQL queries")]
        >>> vectorstore.add_documents(docs)
    """

    # Connection configuration
    url: str | None = Field(default=None, description="URL of the Weaviate instance")

    api_key: SecretStr | None = Field(
        default=None,
        description="API key for Weaviate Cloud (auto-resolved from WEAVIATE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="weaviate", description="Provider name for API key resolution"
    )

    # Weaviate configuration
    index_name: str = Field(
        default="LangChain", description="Name of the Weaviate class/index"
    )

    text_key: str = Field(
        default="text", description="Property name for storing document text"
    )

    # Embedded instance configuration
    use_embedded: bool = Field(
        default=False, description="Use embedded Weaviate instance (for development)"
    )

    embedded_options: dict[str, Any] | None = Field(
        default=None, description="Options for embedded Weaviate instance"
    )

    # Authentication
    auth_client_secret: dict[str, Any] | None = Field(
        default=None, description="Authentication client secret configuration"
    )

    additional_headers: dict[str, str] | None = Field(
        default=None, description="Additional HTTP headers for requests"
    )

    # Batch configuration
    batch_size: int = Field(
        default=100, ge=1, le=10000, description="Batch size for bulk operations"
    )

    # Timeout configuration
    timeout_config: dict[str, int] | None = Field(
        default=None, description="Timeout configuration for operations"
    )

    # Additional properties
    additional_properties: list[str] | None = Field(
        default=None, description="Additional properties to store with documents"
    )

    @validator("url")
    def validate_url_or_embedded(self, v, values):
        """Validate that either URL is provided or embedded is True."""
        if not v and not values.get("use_embedded"):
            raise ValueError(
                "Either 'url' must be provided or 'use_embedded' must be True"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Weaviate vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Weaviate vector store."""
        return {
            "ids": (list[str], Field(description="IDs of the added documents")),
        }

    def instantiate(self):
        """Create a Weaviate vector store from this configuration.

        Returns:
            Weaviate: Instantiated Weaviate vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_weaviate import WeaviateVectorStore as Weaviate
        except ImportError:
            try:
                from langchain_community.vectorstores import Weaviate
            except ImportError:
                raise ImportError(
                    "Weaviate requires weaviate-client package. "
                    "Install with: pip install weaviate-client"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Create Weaviate client
        import weaviate

        if self.use_embedded:
            # Use embedded instance
            if self.embedded_options:
                client = weaviate.EmbeddedOptions(**self.embedded_options)
            else:
                client = weaviate.EmbeddedOptions()

            # Create client with embedded options
            client = weaviate.Client(embedded_options=client)
        else:
            # Use external instance
            if not self.url:
                raise ValueError(
                    "URL must be provided when not using embedded instance"
                )

            # Prepare auth configuration
            auth_config = None
            api_key = self.get_api_key()

            if api_key:
                auth_config = weaviate.AuthApiKey(api_key=api_key)
            elif self.auth_client_secret:
                auth_config = weaviate.AuthClientPassword(**self.auth_client_secret)

            # Prepare additional headers
            additional_headers = self.additional_headers or {}

            # Create client
            client = weaviate.Client(
                url=self.url,
                auth_client_secret=auth_config,
                additional_headers=additional_headers,
                timeout_config=self.timeout_config,
            )

        # Create schema if it doesn't exist
        try:
            schema = client.schema.get()
            class_exists = any(
                c["class"] == self.index_name for c in schema.get("classes", [])
            )

            if not class_exists:
                # Create class schema
                class_obj = {
                    "class": self.index_name,
                    "vectorizer": "none",  # We're providing our own embeddings
                    "properties": [{"name": self.text_key, "dataType": ["text"]}],
                }

                # Add additional properties if specified
                if self.additional_properties:
                    for prop in self.additional_properties:
                        class_obj["properties"].append(
                            {"name": prop, "dataType": ["text"]}
                        )

                client.schema.create_class(class_obj)
        except Exception as e:
            # Schema might already exist or there might be permission issues
            import warnings

            warnings.warn(f"Could not create schema: {e}", stacklevel=2)

        # Create Weaviate vector store
        return Weaviate(
            client=client,
            index_name=self.index_name,
            text_key=self.text_key,
            embedding=embedding_function,
        )
