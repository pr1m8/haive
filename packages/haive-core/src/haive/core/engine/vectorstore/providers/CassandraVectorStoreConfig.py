"""Cassandra Vector Store implementation for the Haive framework.

This module provides a configuration class for the Cassandra vector store,
which provides distributed vector storage with Apache Cassandra.

Cassandra provides:
1. Distributed vector storage across multiple nodes
2. High availability and fault tolerance
3. Linear scalability for vector workloads
4. Native vector search capabilities
5. Integration with DataStax Astra DB
6. ACID transactions with vector operations

This vector store is particularly useful when:
- You need distributed vector storage at scale
- Want high availability for vector data
- Building applications requiring linear scalability
- Need integration with existing Cassandra infrastructure
- Require fault-tolerant vector operations

The implementation integrates with LangChain's Cassandra while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.CASSANDRA)
class CassandraVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for Cassandra vector store in the Haive framework.

    This vector store uses Apache Cassandra for distributed vector
    storage with high availability and scalability.

    Attributes:
        hosts (List[str]): List of Cassandra host addresses.
        port (int): Cassandra port number.
        keyspace (str): Cassandra keyspace name.
        table_name (str): Name of the Cassandra table.
        username (str): Cassandra username.
        password (str): Cassandra password.

    Examples:
        >>> from haive.core.engine.vectorstore import CassandraVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Cassandra config (local)
        >>> config = CassandraVectorStoreConfig(
        ...     name="cassandra_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     hosts=["localhost"],
        ...     keyspace="vector_keyspace",
        ...     table_name="document_vectors"
        ... )
        >>>
        >>> # Create Cassandra config (cluster)
        >>> config = CassandraVectorStoreConfig(
        ...     name="cassandra_cluster",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     hosts=["node1.example.com", "node2.example.com", "node3.example.com"],
        ...     keyspace="production",
        ...     table_name="vectors",
        ...     username="cassandra_user",
        ...     password="cassandra_pass"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Cassandra provides distributed vectors")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Distributed vector search
        >>> results = vectorstore.similarity_search("distributed storage", k=5)
    """

    # Cassandra cluster configuration
    hosts: list[str] = Field(
        default=["localhost"], description="List of Cassandra host addresses"
    )

    port: int = Field(default=9042, ge=1, le=65535, description="Cassandra port number")

    # Authentication
    username: str | None = Field(default=None, description="Cassandra username")

    password: str | None = Field(
        default=None,
        description="Cassandra password (auto-resolved from CASSANDRA_PASSWORD)",
    )

    # Database configuration
    keyspace: str = Field(..., description="Cassandra keyspace name (required)")

    table_name: str = Field(
        default="langchain_vector_store", description="Name of the Cassandra table"
    )

    # TTL configuration
    ttl_seconds: int | None = Field(
        default=None, ge=1, description="Time-to-live for added texts in seconds"
    )

    # Setup configuration
    setup_mode: str = Field(
        default="SYNC", description="Setup mode: 'SYNC', 'ASYNC', or 'OFF'"
    )

    # Metadata indexing
    metadata_indexing: str = Field(
        default="all", description="Metadata indexing policy: 'all', 'none', or custom"
    )

    # Connection settings
    connection_timeout: int = Field(
        default=30, ge=1, le=300, description="Connection timeout in seconds"
    )

    request_timeout: int = Field(
        default=30, ge=1, le=300, description="Request timeout in seconds"
    )

    @validator("hosts")
    def validate_hosts(self, v):
        """Validate hosts list is not empty."""
        if not v or len(v) == 0:
            raise ValueError("hosts list cannot be empty")
        return v

    @validator("setup_mode")
    def validate_setup_mode(self, v):
        """Validate setup mode is supported."""
        valid_modes = ["SYNC", "ASYNC", "OFF"]
        if v not in valid_modes:
            raise ValueError(f"setup_mode must be one of {valid_modes}, got {v}")
        return v

    @validator("metadata_indexing")
    def validate_metadata_indexing(self, v):
        """Validate metadata indexing policy."""
        valid_policies = ["all", "none"]
        if v not in valid_policies:
            # Allow custom policies but warn
            import warnings

            warnings.warn(
                f"metadata_indexing '{v}' is custom - ensure it's properly formatted",
                stacklevel=2,
            )
        return v

    @validator("keyspace")
    def validate_keyspace(self, v):
        """Validate keyspace name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("keyspace cannot be empty")
        # Basic validation - Cassandra has specific naming rules
        import re

        if not re.match(r"^[a-zA-Z0-9_]+$", v):
            raise ValueError(
                "keyspace must contain only letters, numbers, and underscores"
            )
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Cassandra vector store."""
        return {
            "documents": (
                list[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Cassandra vector store."""
        return {
            "ids": (
                list[str],
                Field(description="IDs of the added documents in Cassandra"),
            ),
        }

    def instantiate(self):
        """Create a Cassandra vector store from this configuration.

        Returns:
            Cassandra: Instantiated Cassandra vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from cassandra.auth import PlainTextAuthProvider
            from cassandra.cluster import Cluster
            from langchain_community.vectorstores import Cassandra
        except ImportError:
            raise ImportError(
                "Cassandra requires cassandra-driver and cassio packages. "
                "Install with: pip install cassandra-driver cassio"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get password from config or environment
        password = self.password
        if not password and self.username:
            import os

            password = os.getenv("CASSANDRA_PASSWORD")

        # Create Cassandra cluster connection
        try:
            # Prepare cluster configuration
            cluster_kwargs = {
                "contact_points": self.hosts,
                "port": self.port,
                "connect_timeout": self.connection_timeout,
                "control_connection_timeout": self.request_timeout,
            }

            # Add authentication if provided
            if self.username and password:
                auth_provider = PlainTextAuthProvider(
                    username=self.username, password=password
                )
                cluster_kwargs["auth_provider"] = auth_provider

            # Create cluster and session
            cluster = Cluster(**cluster_kwargs)
            session = cluster.connect()

            # Set keyspace
            session.set_keyspace(self.keyspace)

        except Exception as e:
            raise ValueError(f"Failed to connect to Cassandra: {e}")

        # Map setup mode to cassio format
        try:
            from langchain_community.utilities.cassandra import SetupMode

            setup_mode_mapping = {
                "SYNC": SetupMode.SYNC,
                "ASYNC": SetupMode.ASYNC,
                "OFF": SetupMode.OFF,
            }
            setup_mode = setup_mode_mapping[self.setup_mode]

        except ImportError:
            # Fallback for older versions
            setup_mode = self.setup_mode

        # Prepare kwargs for Cassandra vector store
        kwargs = {
            "embedding": embedding_function,
            "session": session,
            "keyspace": self.keyspace,
            "table_name": self.table_name,
            "setup_mode": setup_mode,
            "metadata_indexing": self.metadata_indexing,
        }

        # Add optional TTL if specified
        if self.ttl_seconds:
            kwargs["ttl_seconds"] = self.ttl_seconds

        # Create Cassandra vector store
        try:
            vectorstore = Cassandra(**kwargs)
        except Exception as e:
            raise ValueError(f"Failed to create Cassandra vector store: {e}")

        return vectorstore
