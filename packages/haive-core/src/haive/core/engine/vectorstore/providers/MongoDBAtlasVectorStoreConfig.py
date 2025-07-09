"""
MongoDB Atlas Vector Store implementation for the Haive framework.

This module provides a configuration class for the MongoDB Atlas vector store,
which combines document database capabilities with vector search functionality.

MongoDB Atlas Vector Search provides:
1. Unified database for documents and vectors
2. Rich query capabilities combining vector and metadata
3. ACID transactions and consistency guarantees
4. Global clusters with automatic failover
5. Built-in full-text search alongside vector search
6. Flexible document model with nested structures

This vector store is particularly useful when:
- You need both document storage and vector search
- Want to leverage existing MongoDB infrastructure
- Require complex queries combining vectors and metadata
- Need ACID transactions for your vector data
- Building applications with rich document structures

The implementation integrates with LangChain's MongoDB Atlas while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.MONGODB_ATLAS)
class MongoDBAtlasVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for MongoDB Atlas vector store in the Haive framework.

    This vector store uses MongoDB Atlas Vector Search for combining
    document database capabilities with vector similarity search.

    Attributes:
        connection_string (str): MongoDB connection string.
        database_name (str): Name of the MongoDB database.
        collection_name (str): Name of the MongoDB collection.
        index_name (str): Name of the Atlas Search index.
        text_key (str): Field name for document text.
        embedding_key (str): Field name for embedding vectors.
        relevance_score_fn (str): Scoring function to use.

    Examples:
        >>> from haive.core.engine.vectorstore import MongoDBAtlasVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create MongoDB Atlas config
        >>> config = MongoDBAtlasVectorStoreConfig(
        ...     name="document_store",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     connection_string="mongodb+srv://user:pass@cluster.mongodb.net",
        ...     database_name="my_database",
        ...     collection_name="documents",
        ...     index_name="vector_index"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="MongoDB combines documents and vectors")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Search with metadata filtering
        >>> results = vectorstore.similarity_search(
        ...     "document database",
        ...     k=5,
        ...     pre_filter={"category": {"$eq": "database"}}
        ... )
    """

    # MongoDB connection configuration
    connection_string: str = Field(
        ..., description="MongoDB connection string (mongodb+srv://...)"
    )

    database_name: str = Field(..., description="Name of the MongoDB database")

    # Collection configuration (overrides base collection_name)
    collection_name: str = Field(
        default="langchain", description="Name of the MongoDB collection"
    )

    # Atlas Search configuration
    index_name: str = Field(
        default="default", description="Name of the Atlas Search index"
    )

    # Field mappings
    text_key: str = Field(
        default="text", description="Field name for storing document text"
    )

    embedding_key: str = Field(
        default="embedding", description="Field name for storing embedding vectors"
    )

    # Search configuration
    relevance_score_fn: str = Field(
        default="cosine",
        description="Relevance scoring function: 'cosine', 'euclidean', or 'dotProduct'",
    )

    # Advanced configuration
    create_index_if_not_exists: bool = Field(
        default=True,
        description="Whether to create the search index if it doesn't exist",
    )

    # Index configuration for creation
    index_config: Optional[Dict[str, Any]] = Field(
        default=None, description="Custom index configuration for Atlas Search"
    )

    @validator("relevance_score_fn")
    def validate_relevance_score_fn(cls, v):
        """Validate relevance score function is supported."""
        valid_functions = ["cosine", "euclidean", "dotProduct"]
        if v not in valid_functions:
            raise ValueError(
                f"relevance_score_fn must be one of {valid_functions}, got {v}"
            )
        return v

    @validator("connection_string")
    def validate_connection_string(cls, v):
        """Basic validation of MongoDB connection string."""
        if not v.startswith(("mongodb://", "mongodb+srv://")):
            raise ValueError(
                "connection_string must start with mongodb:// or mongodb+srv://"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for MongoDB Atlas vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for MongoDB Atlas vector store."""
        return {
            "ids": (
                List[str],
                Field(description="MongoDB ObjectIds of the added documents"),
            ),
        }

    def instantiate(self):
        """
        Create a MongoDB Atlas vector store from this configuration.

        Returns:
            MongoDBAtlasVectorSearch: Instantiated MongoDB Atlas vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_mongodb import MongoDBAtlasVectorSearch
        except ImportError:
            try:
                from langchain_community.vectorstores import MongoDBAtlasVectorSearch
            except ImportError:
                raise ImportError(
                    "MongoDB Atlas requires pymongo package. "
                    "Install with: pip install pymongo"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Create MongoDB client
        try:
            from pymongo import MongoClient

            client = MongoClient(self.connection_string)

            # Get database and collection
            db = client[self.database_name]
            collection = db[self.collection_name]

        except Exception as e:
            raise ValueError(f"Failed to connect to MongoDB: {e}")

        # Prepare kwargs
        kwargs = {
            "collection": collection,
            "embedding": embedding_function,
            "index_name": self.index_name,
            "text_key": self.text_key,
            "embedding_key": self.embedding_key,
            "relevance_score_fn": self.relevance_score_fn,
        }

        # Create vector store
        vectorstore = MongoDBAtlasVectorSearch(**kwargs)

        # Create index if requested and it doesn't exist
        if self.create_index_if_not_exists:
            try:
                # Check if index exists
                indexes = list(collection.list_search_indexes())
                index_exists = any(
                    idx.get("name") == self.index_name for idx in indexes
                )

                if not index_exists:
                    # Create default index configuration if not provided
                    if not self.index_config:
                        # Get vector dimensions
                        try:
                            sample_embedding = embedding_function.embed_query("sample")
                            dimensions = len(sample_embedding)
                        except Exception:
                            dimensions = 1536  # Default to common dimension

                        self.index_config = {
                            "mappings": {
                                "dynamic": True,
                                "fields": {
                                    self.embedding_key: {
                                        "dimensions": dimensions,
                                        "similarity": self.relevance_score_fn,
                                        "type": "knnVector",
                                    }
                                },
                            }
                        }

                    # Create the search index
                    collection.create_search_index(
                        {"definition": self.index_config, "name": self.index_name}
                    )

            except Exception as e:
                # Index creation might fail due to permissions or other issues
                import warnings

                warnings.warn(f"Could not create search index: {e}")

        return vectorstore
