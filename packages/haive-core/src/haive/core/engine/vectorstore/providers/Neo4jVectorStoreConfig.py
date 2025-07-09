"""
Neo4j Vector Store implementation for the Haive framework.

This module provides a configuration class for the Neo4j vector store,
which combines graph database capabilities with vector similarity search.

Neo4j provides:
1. Native graph database with vector search capabilities
2. Vector indexing on nodes and relationships
3. Hybrid search combining graph traversal and vector similarity
4. Cypher query language for complex graph operations
5. ACID transactions with vector operations
6. Scalable graph analytics with vector data

This vector store is particularly useful when:
- You need graph database capabilities with vector search
- Want to combine knowledge graphs with semantic search
- Building recommendation systems with graph relationships
- Need complex graph queries with vector similarity
- Require ACID transactions with graph and vector data

The implementation integrates with LangChain's Neo4j while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

# Note: Not using SecureConfigMixin since Neo4j uses 'password' not 'api_key'
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.NEO4J)
class Neo4jVectorStoreConfig(BaseVectorStoreConfig):
    """
    Configuration for Neo4j vector store in the Haive framework.

    This vector store uses Neo4j graph database with vector search
    capabilities for knowledge graphs and semantic search.

    Attributes:
        url (str): Neo4j database URL.
        username (str): Neo4j username.
        password (str): Neo4j password.
        database (str): Neo4j database name.
        index_name (str): Name of the vector index.
        node_label (str): Label for nodes storing vectors.

    Examples:
        >>> from haive.core.engine.vectorstore import Neo4jVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Neo4j config
        >>> config = Neo4jVectorStoreConfig(
        ...     name="neo4j_vectors",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     url="bolt://localhost:7687",
        ...     username="neo4j",
        ...     password="password",
        ...     index_name="vector_index"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Neo4j combines graphs with vectors")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Graph-aware vector search
        >>> results = vectorstore.similarity_search("graph database", k=5)
    """

    # Neo4j connection configuration
    url: str = Field(default="bolt://localhost:7687", description="Neo4j database URL")

    username: str = Field(default="neo4j", description="Neo4j username")

    password: Optional[str] = Field(
        default=None, description="Neo4j password (auto-resolved from NEO4J_PASSWORD)"
    )

    # Database configuration
    database: str = Field(default="neo4j", description="Neo4j database name")

    # Vector index configuration
    index_name: str = Field(
        default="vector_index", description="Name of the Neo4j vector index"
    )

    node_label: str = Field(
        default="Document", description="Label for nodes storing vector data"
    )

    embedding_node_property: str = Field(
        default="embedding", description="Node property name for storing embeddings"
    )

    text_node_property: str = Field(
        default="text", description="Node property name for storing text content"
    )

    # Search configuration
    search_type: str = Field(
        default="vector", description="Search type: 'vector' or 'hybrid'"
    )

    distance_strategy: str = Field(
        default="cosine", description="Distance strategy: 'cosine' or 'euclidean'"
    )

    # Performance parameters
    ef: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="HNSW ef parameter for search quality vs speed trade-off",
    )

    # Index creation settings
    create_index_if_not_exists: bool = Field(
        default=True, description="Whether to create index if it doesn't exist"
    )

    @validator("url")
    def validate_url(cls, v):
        """Validate Neo4j URL format."""
        valid_schemes = ["bolt://", "neo4j://", "bolt+s://", "neo4j+s://"]
        if not any(v.startswith(scheme) for scheme in valid_schemes):
            raise ValueError(f"url must start with one of {valid_schemes}")
        return v

    @validator("search_type")
    def validate_search_type(cls, v):
        """Validate search type is supported."""
        valid_types = ["vector", "hybrid"]
        if v not in valid_types:
            raise ValueError(f"search_type must be one of {valid_types}, got {v}")
        return v

    @validator("distance_strategy")
    def validate_distance_strategy(cls, v):
        """Validate distance strategy is supported."""
        valid_strategies = ["cosine", "euclidean"]
        if v not in valid_strategies:
            raise ValueError(
                f"distance_strategy must be one of {valid_strategies}, got {v}"
            )
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Neo4j vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Neo4j vector store."""
        return {
            "ids": (
                List[str],
                Field(description="IDs of the added documents in Neo4j"),
            ),
        }

    def instantiate(self):
        """
        Create a Neo4j vector store from this configuration.

        Returns:
            Neo4jVector: Instantiated Neo4j vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_neo4j import Neo4jVector
        except ImportError:
            try:
                from langchain_community.vectorstores import Neo4jVector
            except ImportError:
                raise ImportError(
                    "Neo4j requires neo4j package. " "Install with: pip install neo4j"
                )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get password from config or environment
        password = self.password
        if not password:
            import os

            password = os.getenv("NEO4J_PASSWORD")

        if not password:
            raise ValueError(
                "Neo4j password is required. Set NEO4J_PASSWORD environment variable "
                "or provide password parameter."
            )

        # Map distance strategy to Neo4j format
        try:
            from langchain_neo4j.vectorstores.utils import DistanceStrategy

            distance_mapping = {
                "cosine": DistanceStrategy.COSINE,
                "euclidean": DistanceStrategy.EUCLIDEAN_DISTANCE,
            }
            distance_strategy = distance_mapping[self.distance_strategy]

        except ImportError:
            # Fallback for older versions
            distance_strategy = self.distance_strategy

        # Map search type to Neo4j format
        try:
            from langchain_neo4j.vectorstores.neo4j_vector import SearchType

            search_type_mapping = {
                "vector": SearchType.VECTOR,
                "hybrid": SearchType.HYBRID,
            }
            search_type = search_type_mapping[self.search_type]

        except (ImportError, AttributeError):
            # Fallback for older versions
            search_type = self.search_type

        # Prepare kwargs for Neo4j vector store
        kwargs = {
            "url": self.url,
            "username": self.username,
            "password": password,
            "database": self.database,
            "embedding": embedding_function,
            "index_name": self.index_name,
            "node_label": self.node_label,
            "embedding_node_property": self.embedding_node_property,
            "text_node_property": self.text_node_property,
            "distance_strategy": distance_strategy,
            "search_type": search_type,
        }

        # Add performance parameters if supported
        try:
            kwargs["ef"] = self.ef
        except Exception:
            # Older versions might not support ef parameter
            pass

        # Create Neo4j vector store
        try:
            vectorstore = Neo4jVector.from_existing_index(
                embedding=embedding_function,
                url=self.url,
                username=self.username,
                password=password,
                database=self.database,
                index_name=self.index_name,
                **{
                    k: v
                    for k, v in kwargs.items()
                    if k
                    not in [
                        "url",
                        "username",
                        "password",
                        "database",
                        "embedding",
                        "index_name",
                    ]
                },
            )
        except Exception:
            # If index doesn't exist, create new one
            vectorstore = Neo4jVector(**kwargs)

        return vectorstore
