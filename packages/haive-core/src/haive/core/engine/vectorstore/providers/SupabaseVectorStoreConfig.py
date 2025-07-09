"""
Supabase Vector Store implementation for the Haive framework.

This module provides a configuration class for the Supabase vector store,
which is a managed PostgreSQL service with built-in pgvector support.

Supabase provides:
1. Managed PostgreSQL with pgvector extension
2. Real-time subscriptions for vector data changes
3. Built-in authentication and row-level security
4. Edge functions for vector processing
5. Dashboard for database management
6. Global CDN and auto-scaling

This vector store is particularly useful when:
- You want managed PostgreSQL without infrastructure overhead
- Need real-time capabilities with vector data
- Want built-in authentication and security
- Building full-stack applications with vector search
- Need global distribution and edge compute

The implementation integrates with LangChain's Supabase while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.SUPABASE)
class SupabaseVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """
    Configuration for Supabase vector store in the Haive framework.

    This vector store uses Supabase's managed PostgreSQL with pgvector
    for vector similarity search with real-time capabilities.

    Attributes:
        supabase_url (str): Supabase project URL.
        supabase_key (Optional[SecretStr]): Supabase API key (auto-resolved).
        table_name (str): Name of the table to store vectors.
        query_name (str): Name of the RPC function for similarity search.
        chunk_size (int): Batch size for bulk operations.

    Examples:
        >>> from haive.core.engine.vectorstore import SupabaseVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Supabase config
        >>> config = SupabaseVectorStoreConfig(
        ...     name="supabase_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     supabase_url="https://your-project.supabase.co",
        ...     table_name="documents",
        ...     query_name="match_documents"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Supabase with real-time vectors")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Real-time vector search
        >>> results = vectorstore.similarity_search("managed postgres", k=5)
    """

    # Supabase configuration
    supabase_url: str = Field(
        ..., description="Supabase project URL (https://your-project.supabase.co)"
    )

    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Supabase API key (auto-resolved from SUPABASE_KEY or SUPABASE_SERVICE_KEY)",
    )

    # Provider for SecureConfigMixin (maps to supabase_key)
    provider: str = Field(
        default="supabase", description="Provider name for API key resolution"
    )

    # Table configuration
    table_name: str = Field(
        default="documents", description="Name of the Supabase table to store vectors"
    )

    query_name: str = Field(
        default="match_documents",
        description="Name of the RPC function for similarity search",
    )

    # Vector column configuration
    vector_column: str = Field(
        default="embedding", description="Name of the vector column in the table"
    )

    content_column: str = Field(
        default="content", description="Name of the content column in the table"
    )

    metadata_column: str = Field(
        default="metadata", description="Name of the metadata column in the table"
    )

    # Performance configuration
    chunk_size: int = Field(
        default=500, ge=1, le=10000, description="Batch size for bulk operations"
    )

    # Search configuration
    similarity_threshold: Optional[float] = Field(
        default=None, description="Similarity threshold for search results"
    )

    # Advanced configuration
    create_table: bool = Field(
        default=True, description="Whether to create the table if it doesn't exist"
    )

    @validator("supabase_url")
    def validate_supabase_url(cls, v):
        """Validate Supabase URL format."""
        if not v.startswith("https://") or not v.endswith(".supabase.co"):
            raise ValueError("supabase_url must be a valid Supabase project URL")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Supabase vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Supabase vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in Supabase"),
            ),
        }

    def instantiate(self):
        """
        Create a Supabase vector store from this configuration.

        Returns:
            SupabaseVectorStore: Instantiated Supabase vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import SupabaseVectorStore
        except ImportError:
            raise ImportError(
                "Supabase requires supabase package. "
                "Install with: pip install supabase"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key using SecureConfigMixin
        # Try multiple environment variable names for Supabase
        api_key = self.get_api_key()
        if not api_key:
            import os

            # Try alternative environment variable names
            api_key = (
                os.getenv("SUPABASE_SERVICE_KEY")
                or os.getenv("SUPABASE_ANON_KEY")
                or os.getenv("SUPABASE_API_KEY")
            )

        if not api_key:
            raise ValueError(
                "Supabase API key is required. Set SUPABASE_KEY, SUPABASE_SERVICE_KEY, "
                "or SUPABASE_ANON_KEY environment variable, or provide api_key parameter."
            )

        # Create Supabase client
        try:
            from supabase import Client, create_client

            supabase_client: Client = create_client(self.supabase_url, api_key)

        except Exception as e:
            raise ValueError(f"Failed to create Supabase client: {e}")

        # Prepare kwargs
        kwargs = {
            "client": supabase_client,
            "embedding": embedding_function,
            "table_name": self.table_name,
            "query_name": self.query_name,
            "chunk_size": self.chunk_size,
        }

        # Create the vector store
        vectorstore = SupabaseVectorStore(**kwargs)

        # Create table and function if requested
        if self.create_table:
            try:
                self._create_table_and_function(supabase_client)
            except Exception as e:
                import warnings

                warnings.warn(f"Could not create table or function: {e}")

        return vectorstore

    def _create_table_and_function(self, client):
        """Create the table and similarity search function if they don't exist."""

        # Create table SQL
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id BIGSERIAL PRIMARY KEY,
            {self.content_column} TEXT,
            {self.metadata_column} JSONB,
            {self.vector_column} VECTOR(1536)
        );
        """

        # Create function SQL for similarity search
        create_function_sql = f"""
        CREATE OR REPLACE FUNCTION {self.query_name}(
            query_embedding VECTOR(1536),
            match_count INT DEFAULT 10,
            filter JSONB DEFAULT '{{}}'
        )
        RETURNS TABLE(
            id BIGINT,
            {self.content_column} TEXT,
            {self.metadata_column} JSONB,
            similarity FLOAT
        )
        LANGUAGE plpgsql
        AS $$
        #variable_conflict use_column
        BEGIN
            RETURN QUERY
            SELECT
                {self.table_name}.id,
                {self.table_name}.{self.content_column},
                {self.table_name}.{self.metadata_column},
                1 - ({self.table_name}.{self.vector_column} <=> query_embedding) AS similarity
            FROM {self.table_name}
            WHERE {self.table_name}.{self.metadata_column} @> filter
            ORDER BY {self.table_name}.{self.vector_column} <=> query_embedding
            LIMIT match_count;
        END;
        $$;
        """

        # Create index SQL for better performance
        create_index_sql = f"""
        CREATE INDEX IF NOT EXISTS {self.table_name}_{self.vector_column}_idx 
        ON {self.table_name} 
        USING ivfflat ({self.vector_column} vector_cosine_ops)
        WITH (lists = 100);
        """

        try:
            # Execute table creation
            client.rpc("exec_sql", {"sql": create_table_sql}).execute()

            # Execute function creation
            client.rpc("exec_sql", {"sql": create_function_sql}).execute()

            # Execute index creation
            client.rpc("exec_sql", {"sql": create_index_sql}).execute()

        except Exception:
            # If exec_sql RPC doesn't exist, the setup needs to be done manually
            pass
