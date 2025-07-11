"""
ClickHouse Vector Store implementation for the Haive framework.

This module provides a configuration class for the ClickHouse vector store,
which is a high-performance columnar database with vector search capabilities.

ClickHouse provides:
1. High-performance columnar storage with vector support
2. SQL-based interface with vector operations
3. Support for various index types (Annoy, etc.)
4. Scalable analytics with vector search
5. Real-time data ingestion and query
6. Support for multiple distance metrics
7. Distributed architecture for large-scale deployments

This vector store is particularly useful when:
- You need analytics capabilities combined with vector search
- Working with time-series data that requires vector operations
- Building real-time analytics applications with similarity search
- Need high-performance columnar storage with vectors
- Want SQL interface for vector operations
- Require distributed processing for large datasets

The implementation integrates with LangChain's ClickHouse while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type, Union

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.CLICKHOUSE)
class ClickHouseVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for ClickHouse vector store in the Haive framework.

    This vector store uses ClickHouse's columnar database engine for
    high-performance analytics combined with vector search capabilities.

    Attributes:
        host (str): ClickHouse server hostname.
        port (int): ClickHouse server port.
        username (Optional[str]): Username for authentication.
        password (Optional[str]): Password for authentication.
        database (str): Database name.
        table (str): Table name for storing vectors.
        secure (bool): Use secure connection.
        index_type (str): Index type (e.g., 'annoy').
        metric (str): Distance metric for similarity.

    Examples:
        >>> from haive.core.engine.vectorstore import ClickHouseVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create ClickHouse config (local)
        >>> config = ClickHouseVectorStoreConfig(
        ...     name="clickhouse_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     host="localhost",
        ...     port=8123,
        ...     database="default",
        ...     table="embeddings"
        ... )
        >>>
        >>> # Create ClickHouse config (with authentication)
        >>> config = ClickHouseVectorStoreConfig(
        ...     name="clickhouse_analytics",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     host="clickhouse.example.com",
        ...     port=8443,
        ...     username="admin",
        ...     password="password",
        ...     secure=True,
        ...     database="analytics",
        ...     table="document_vectors",
        ...     metric="cosine"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="ClickHouse provides fast analytics with vectors")]
        >>> vectorstore.add_documents(docs)
    """

    # ClickHouse connection configuration
    host: str = Field(default="localhost", description="ClickHouse server hostname")

    port: int = Field(
        default=8123, ge=1, le=65535, description="ClickHouse server port"
    )

    username: Optional[str] = Field(
        default=None, description="Username for authentication"
    )

    password: Optional[str] = Field(
        default=None,
        description="Password for authentication (auto-resolved from CLICKHOUSE_PASSWORD)",
    )

    # Database configuration
    database: str = Field(default="default", description="Database name")

    table: str = Field(
        default="langchain", description="Table name for storing vectors"
    )

    # Connection settings
    secure: bool = Field(default=False, description="Use secure connection (HTTPS)")

    # Index configuration
    index_type: str = Field(default="annoy", description="Index type for vector search")

    index_param: Optional[Union[List, Dict]] = Field(
        default=["'L2Distance'", 100], description="Index build parameters"
    )

    index_query_params: Dict[str, str] = Field(
        default_factory=dict, description="Index query parameters"
    )

    # Distance metric
    metric: str = Field(
        default="angular",
        description="Distance metric: 'angular', 'euclidean', 'manhattan', 'hamming', 'dot'",
    )

    # Column mapping
    column_map: Dict[str, str] = Field(
        default_factory=lambda: {
            "id": "id",
            "uuid": "uuid",
            "document": "document",
            "embedding": "embedding",
            "metadata": "metadata",
        },
        description="Column name mapping for vector store fields",
    )

    @validator("metric")
    def validate_metric(cls, v):
        """Validate distance metric is supported."""
        valid_metrics = ["angular", "euclidean", "manhattan", "hamming", "dot"]
        if v not in valid_metrics:
            raise ValueError(f"metric must be one of {valid_metrics}, got {v}")
        return v

    @validator("password", pre=True, always=True)
    def resolve_password(cls, v, values):
        """Resolve password from value or environment."""
        if not v and values.get("username"):
            import os

            v = os.getenv("CLICKHOUSE_PASSWORD")
        return v

    @validator("index_type")
    def validate_index_type(cls, v):
        """Validate index type."""
        # Currently, ClickHouse primarily supports Annoy for vector indexing
        valid_types = ["annoy"]
        if v.lower() not in valid_types:
            raise ValueError(f"index_type must be one of {valid_types}, got {v}")
        return v.lower()

    @validator("table")
    def validate_table_name(cls, v):
        """Validate table name format."""
        if not v or len(v.strip()) == 0:
            raise ValueError("table name cannot be empty")
        # Basic validation for SQL table naming
        import re

        if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", v):
            raise ValueError(
                "table name must start with a letter or underscore and "
                "contain only letters, numbers, and underscores"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for ClickHouse vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for ClickHouse vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in ClickHouse"),
            ),
        }

    def instantiate(self):
        """
        Create a ClickHouse vector store from this configuration.

        Returns:
            Clickhouse: Instantiated ClickHouse vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import Clickhouse, ClickhouseSettings
        except ImportError as e:
            raise ImportError(
                "ClickHouse requires clickhouse-connect package. "
                "Install with: pip install clickhouse-connect"
            ) from e

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Create ClickHouse settings
        settings = ClickhouseSettings(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            secure=self.secure,
            index_type=self.index_type,
            index_param=self.index_param,
            index_query_params=self.index_query_params,
            database=self.database,
            table=self.table,
            metric=self.metric,
            column_map=self.column_map,
        )

        # Create ClickHouse vector store
        try:
            vectorstore = Clickhouse(
                embedding=embedding_function,
                config=settings,
            )
        except Exception as e:
            raise ValueError(f"Failed to create ClickHouse vector store: {e}") from e

        return vectorstore
