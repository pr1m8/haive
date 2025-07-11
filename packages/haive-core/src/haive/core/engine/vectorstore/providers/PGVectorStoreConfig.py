"""
PGVector Vector Store implementation for the Haive framework.

This module provides a configuration class for the PGVector vector store,
which adds vector similarity search capabilities to PostgreSQL databases.

PGVector provides:
1. Native PostgreSQL extension for vector operations
2. Exact and approximate nearest neighbor search
3. Multiple distance functions (L2, inner product, cosine)
4. SQL-compatible vector operations
5. ACID transactions with vector data
6. Indexing with IVFFlat and HNSW algorithms

This vector store is particularly useful when:
- You want to add vector search to existing PostgreSQL infrastructure
- Need ACID transactions with vector operations
- Want to combine relational and vector data in SQL queries
- Require mature database features (backup, replication, etc.)
- Building applications that need both structured and vector data

The implementation integrates with LangChain's PGVector while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.PGVECTOR)
class PGVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for PGVector vector store in the Haive framework.

    This vector store uses PostgreSQL with the pgvector extension for
    SQL-compatible vector similarity search operations.

    Attributes:
        connection_string (str): PostgreSQL connection string.
        table_name (str): Name of the table to store vectors.
        distance_strategy (str): Distance function to use.
        pre_delete_collection (bool): Whether to drop existing table.
        use_jsonb (bool): Whether to use JSONB for metadata storage.

    Examples:
        >>> from haive.core.engine.vectorstore import PGVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create PGVector config
        >>> config = PGVectorStoreConfig(
        ...     name="postgres_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     connection_string="postgresql://user:pass@localhost:5432/vectordb",
        ...     table_name="document_embeddings",
        ...     distance_strategy="cosine"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="PostgreSQL with vector search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # SQL-compatible vector queries
        >>> results = vectorstore.similarity_search("database vectors", k=5)
    """

    # PostgreSQL connection configuration
    connection_string: str = Field(
        ...,
        description="PostgreSQL connection string (postgresql://user:pass@host:port/db)",
    )

    # Table configuration
    table_name: str = Field(
        default="langchain_pg_embedding",
        description="Name of the PostgreSQL table to store vectors",
    )

    # Vector configuration
    distance_strategy: str = Field(
        default="cosine",
        description="Distance strategy: 'cosine', 'l2', or 'inner_product'",
    )

    # Schema configuration
    pre_delete_collection: bool = Field(
        default=False,
        description="Whether to drop existing table before creating new one",
    )

    use_jsonb: bool = Field(
        default=True,
        description="Whether to use JSONB for metadata storage (recommended)",
    )

    # Index configuration
    create_extension: bool = Field(
        default=True, description="Whether to create pgvector extension if not exists"
    )

    # Advanced configuration
    vector_dimension: Optional[int] = Field(
        default=None, description="Vector dimension (auto-detected if not specified)"
    )

    # Connection pool settings
    pool_size: int = Field(default=5, ge=1, le=50, description="Connection pool size")

    max_overflow: int = Field(
        default=10, ge=0, le=100, description="Maximum connection pool overflow"
    )

    pool_timeout: int = Field(
        default=30, ge=1, le=300, description="Connection pool timeout in seconds"
    )

    @validator("distance_strategy")
    def validate_distance_strategy(cls, v):
        """Validate distance strategy is supported."""
        valid_strategies = ["cosine", "l2", "inner_product"]
        if v not in valid_strategies:
            raise ValueError(
                f"distance_strategy must be one of {valid_strategies}, got {v}"
            )
        return v

    @validator("connection_string")
    def validate_connection_string(cls, v):
        """Basic validation of PostgreSQL connection string."""
        if not v.startswith(("postgresql://", "postgres://")):
            raise ValueError(
                "connection_string must start with postgresql:// or postgres://"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for PGVector vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for PGVector vector store."""
        return {
            "ids": (List[str], Field(description="UUIDs of the added documents")),
        }

    def instantiate(self):
        """
        Create a PGVector vector store from this configuration.

        Returns:
            PGVector: Instantiated PGVector vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_postgres import PGVector
        except ImportError:
            try:
                from langchain_community.vectorstores import PGVector
            except ImportError:
                raise ImportError(
                    "PGVector requires psycopg2 or psycopg2-binary package. "
                    "Install with: pip install psycopg2-binary"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Map distance strategy to PGVector constants
        try:
            from langchain_postgres.vectorstores import DistanceStrategy

            distance_mapping = {
                "cosine": DistanceStrategy.COSINE,
                "l2": DistanceStrategy.EUCLIDEAN,
                "inner_product": DistanceStrategy.MAX_INNER_PRODUCT,
            }
            distance_strategy = distance_mapping[self.distance_strategy]

        except ImportError:
            # Fallback for older versions
            from langchain_community.vectorstores.pgvector import DistanceStrategy

            distance_mapping = {
                "cosine": DistanceStrategy.COSINE,
                "l2": DistanceStrategy.EUCLIDEAN,
                "inner_product": DistanceStrategy.MAX_INNER_PRODUCT,
            }
            distance_strategy = distance_mapping[self.distance_strategy]

        # Prepare kwargs
        kwargs = {
            "connection_string": self.connection_string,
            "embedding_function": embedding_function,
            "collection_name": self.table_name,
            "distance_strategy": distance_strategy,
            "pre_delete_collection": self.pre_delete_collection,
            "use_jsonb": self.use_jsonb,
        }

        # Add vector dimension if specified
        if self.vector_dimension:
            kwargs["vector_dimension"] = self.vector_dimension

        # Create connection with pool settings
        if "pool_size" in PGVector.__init__.__code__.co_varnames:
            kwargs.update(
                {
                    "pool_size": self.pool_size,
                    "max_overflow": self.max_overflow,
                    "pool_timeout": self.pool_timeout,
                }
            )

        # Create PGVector instance
        vectorstore = PGVector(**kwargs)

        # Create extension if requested
        if self.create_extension:
            try:
                # Try to create the extension
                with vectorstore._make_sync_session() as session:
                    session.execute("CREATE EXTENSION IF NOT EXISTS vector;")
                    session.commit()
            except Exception:
                # Extension creation might fail due to permissions
                import warnings

                warnings.warn(
                    "Could not create pgvector extension. "
                    "Please ensure it's installed: CREATE EXTENSION vector;"
                )

        return vectorstore
