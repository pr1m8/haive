"""Typesense Vector Store implementation for the Haive framework.

This module provides a configuration class for the Typesense vector store,
which combines typo-tolerant search with vector similarity.

Typesense provides:
1. Typo-tolerant full-text search
2. Vector similarity search capabilities
3. Real-time indexing and search
4. Faceted search and filtering
5. Auto-complete and suggestions
6. High availability and clustering

This vector store is particularly useful when:
- You need typo-tolerant search capabilities
- Want to combine full-text and vector search
- Building search-heavy applications
- Need real-time search with auto-complete
- Require faceted search and filtering

The implementation integrates with LangChain's Typesense while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.TYPESENSE)
class TypesenseVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """Configuration for Typesense vector store in the Haive framework.

    This vector store uses Typesense for typo-tolerant search combined
    with vector similarity capabilities.

    Attributes:
        host (str): Typesense server host.
        port (str): Typesense server port.
        protocol (str): Connection protocol (http/https).
        api_key (str): Typesense API key.
        collection_name (str): Name of the Typesense collection.
        text_key (str): Field name for storing text content.

    Examples:
        >>> from haive.core.engine.vectorstore import TypesenseVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Typesense config (local)
        >>> config = TypesenseVectorStoreConfig(
        ...     name="typesense_local",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     host="localhost",
        ...     port="8108",
        ...     protocol="http",
        ...     api_key="local-key",
        ...     collection_name="documents"
        ... )
        >>>
        >>> # Create Typesense config (cloud)
        >>> config = TypesenseVectorStoreConfig(
        ...     name="typesense_cloud",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     host="xxx.a1.typesense.net",
        ...     port="443",
        ...     protocol="https",
        ...     collection_name="vectors"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Typesense provides typo-tolerant search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Typo-tolerant vector search
        >>> results = vectorstore.similarity_search("typo tolerent serch", k=5)
    """

    # Typesense server configuration
    host: str = Field(default="localhost", description="Typesense server host")

    port: str = Field(default="8108", description="Typesense server port")

    protocol: str = Field(
        default="http", description="Connection protocol: 'http' or 'https'"
    )

    api_key: str | None = Field(
        default=None,
        description="Typesense API key (auto-resolved from TYPESENSE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="typesense", description="Provider name for API key resolution"
    )

    # Collection configuration
    collection_name: str = Field(
        default="langchain_documents", description="Name of the Typesense collection"
    )

    text_key: str = Field(
        default="text", description="Field name for storing text content"
    )

    # Connection settings
    connection_timeout_seconds: int = Field(
        default=2, ge=1, le=300, description="Connection timeout in seconds"
    )

    # Collection management
    create_collection_if_not_exists: bool = Field(
        default=True, description="Whether to create collection if it doesn't exist"
    )

    @validator("protocol")
    def validate_protocol(self, v):
        """Validate protocol is supported."""
        valid_protocols = ["http", "https"]
        if v not in valid_protocols:
            raise ValueError(f"protocol must be one of {valid_protocols}, got {v}")
        return v

    @validator("port")
    def validate_port(self, v):
        """Validate port is numeric."""
        try:
            port_num = int(v)
            if port_num < 1 or port_num > 65535:
                raise ValueError("port must be between 1 and 65535")
        except ValueError:
            raise ValueError("port must be a valid integer")
        return v

    @validator("collection_name")
    def validate_collection_name(self, v):
        """Validate collection name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("collection_name cannot be empty")
        # Basic validation - Typesense has specific naming rules
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            raise ValueError(
                "collection_name must contain only letters, numbers, underscores, and hyphens"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Typesense vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Typesense vector store."""
        return {
            "ids": (
                list[str],
                Field(description="IDs of the added documents in Typesense"),
            ),
        }

    def instantiate(self):
        """Create a Typesense vector store from this configuration.

        Returns:
            Typesense: Instantiated Typesense vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            import typesense
            from langchain_community.vectorstores import Typesense
        except ImportError:
            raise ImportError(
                "Typesense requires typesense package. "
                "Install with: pip install typesense"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            import os

            api_key = os.getenv("TYPESENSE_API_KEY")

        if not api_key:
            raise ValueError(
                "Typesense API key is required. Set TYPESENSE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Create Typesense client configuration
        node = {"host": self.host, "port": self.port, "protocol": self.protocol}

        client_config = {
            "nodes": [node],
            "api_key": api_key,
            "connection_timeout_seconds": self.connection_timeout_seconds,
        }

        # Create Typesense client
        try:
            typesense_client = typesense.Client(client_config)
        except Exception as e:
            raise ValueError(f"Failed to create Typesense client: {e}")

        # Create Typesense vector store
        try:
            vectorstore = Typesense(
                typesense_client=typesense_client,
                embedding=embedding_function,
                typesense_collection_name=self.collection_name,
                text_key=self.text_key,
            )
        except Exception as e:
            raise ValueError(f"Failed to create Typesense vector store: {e}")

        return vectorstore
