# src/haive/core/persistence/store/types.py
"""Store type definitions and configuration for Haive persistence.

This module provides the foundational types and configurations for the Haive
store system, which wraps LangGraph's native store implementations while
providing serialization, connection management, and embedding integration.

The store system is designed to be fully serializable, support connection
sharing, and seamlessly integrate with Haive's embedding system.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, PrivateAttr


class StoreType(str, Enum):
    """Available store backend types.

    Attributes:
        MEMORY: In-memory store using LangGraph's InMemoryStore
        POSTGRES_SYNC: Synchronous PostgreSQL using PostgresStore
        POSTGRES_ASYNC: Asynchronous PostgreSQL using AsyncPostgresStore
    """

    MEMORY = "memory"
    POSTGRES_SYNC = "postgres_sync"
    POSTGRES_ASYNC = "postgres_async"


class StoreConfig(BaseModel):
    """Serializable configuration for LangGraph stores.

    This configuration is designed to be fully serializable and can be
    stored/loaded from disk, passed between processes, or configured
    via environment variables.

    Attributes:
        type: Store backend type
        namespace_prefix: Optional prefix for all namespaces
        connection_id: Unique ID for connection sharing
        connection_params: Backend-specific connection parameters
        embedding_provider: Provider string for embeddings (e.g., "openai:text-embedding-3-small")
        embedding_dims: Dimension of embeddings
        embedding_fields: Fields to embed from stored values
        pool_config: Connection pool configuration
        setup_on_init: Whether to run setup/migrations
    """

    type: StoreType = Field(default=StoreType.MEMORY, description="Store backend type")
    namespace_prefix: str | None = Field(
        default=None, description="Optional prefix for all namespaces"
    )
    connection_id: str | None = Field(
        default=None, description="Unique ID for connection sharing"
    )

    # Connection settings
    connection_params: dict[str, Any] = Field(
        default_factory=dict, description="Backend-specific connection parameters"
    )

    # Embedding configuration
    embedding_provider: str | None = Field(
        default=None,
        description="Embedding provider string (e.g., 'openai:text-embedding-3-small')",
    )
    embedding_dims: int | None = Field(default=None, description="Embedding dimensions")
    embedding_fields: list[str] | None = Field(
        default=None, description="Fields to embed from stored values"
    )

    # Pool configuration
    pool_config: dict[str, Any] | None = Field(
        default=None, description="Connection pool configuration"
    )

    # Setup behavior
    setup_on_init: bool = Field(
        default=True, description="Run setup/migrations on initialization"
    )

    # Private attributes for runtime state (not serialized)
    _store_instance: Any = PrivateAttr(default=None)
    _connection_pool: Any = PrivateAttr(default=None)
    _embeddings: Any = PrivateAttr(default=None)

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True
        json_encoders = {
            # Add custom encoders if needed
        }
