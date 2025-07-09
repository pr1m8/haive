"""
LlamaIndex Graph Retriever implementation for the Haive framework.

This module provides a configuration class for the LlamaIndex Graph retriever,
which performs graph-based retrieval using knowledge graphs and graph databases
like Neo4j, providing semantic relationships and graph traversal capabilities.

The LlamaIndexGraphRetriever works by:
1. Using a graph index (knowledge graph, Neo4j, etc.) as the underlying storage
2. Performing graph traversal queries to find related nodes and relationships
3. Converting graph nodes and edges into retrievable documents
4. Supporting both entity-based and relationship-based retrieval

This retriever is particularly useful when:
- Working with knowledge graphs and structured data
- Need to understand relationships between entities
- Building systems that require graph traversal and exploration
- Integrating with Neo4j or other graph databases
- Performing semantic retrieval over connected data

The implementation integrates with LangChain Community's LlamaIndexGraphRetriever while
providing a consistent Haive configuration interface with graph database support.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.LLAMA_INDEX_GRAPH)
class LlamaIndexGraphRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for LlamaIndex Graph retriever in the Haive framework.

    This retriever performs graph-based retrieval using knowledge graphs and
    graph databases, providing semantic relationships and graph traversal capabilities.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always LLAMA_INDEX_GRAPH).
        graph_type (str): Type of graph backend ('neo4j', 'networkx', 'knowledge_graph').
        connection_url (Optional[str]): Connection URL for graph database (for Neo4j).
        database_name (Optional[str]): Database name (for Neo4j).
        api_key (Optional[SecretStr]): API key for graph services (auto-resolved).
        query_type (str): Type of graph query ('node', 'relationship', 'path', 'subgraph').
        max_depth (int): Maximum traversal depth in the graph.
        k (int): Number of top results to return.

    Examples:
        >>> from haive.core.engine.retriever import LlamaIndexGraphRetrieverConfig
        >>>
        >>> # Create Neo4j graph retriever
        >>> config = LlamaIndexGraphRetrieverConfig(
        ...     name="neo4j_graph_retriever",
        ...     graph_type="neo4j",
        ...     connection_url="bolt://localhost:7687",
        ...     database_name="knowledge",
        ...     query_type="relationship",
        ...     max_depth=3,
        ...     k=10
        ... )
        >>>
        >>> # Create knowledge graph retriever
        >>> config = LlamaIndexGraphRetrieverConfig(
        ...     name="knowledge_graph_retriever",
        ...     graph_type="knowledge_graph",
        ...     query_type="subgraph",
        ...     max_depth=2,
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("artificial intelligence concepts")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.LLAMA_INDEX_GRAPH, description="The type of retriever"
    )

    # Graph backend configuration
    graph_type: str = Field(
        default="knowledge_graph",
        description="Type of graph backend: 'neo4j', 'networkx', 'knowledge_graph'",
    )

    connection_url: Optional[str] = Field(
        default=None,
        description="Connection URL for graph database (required for Neo4j)",
    )

    database_name: Optional[str] = Field(
        default=None, description="Database name (for Neo4j)"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[str] = (
        Field(  # Using str instead of SecretStr to avoid import issues
            default=None,
            description="API key for graph services (auto-resolved from environment)",
        )
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="llama_index", description="Graph provider identifier"
    )

    # Query configuration
    query_type: str = Field(
        default="relationship",
        description="Type of graph query: 'node', 'relationship', 'path', 'subgraph'",
    )

    max_depth: int = Field(
        default=3, ge=1, le=10, description="Maximum traversal depth in the graph"
    )

    k: int = Field(
        default=5, ge=1, le=50, description="Number of top results to return"
    )

    # Graph traversal options
    include_text: bool = Field(
        default=True, description="Whether to include text content in results"
    )

    include_relationships: bool = Field(
        default=True, description="Whether to include relationship information"
    )

    similarity_threshold: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Similarity threshold for filtering results",
    )

    @validator("graph_type")
    def validate_graph_type(cls, v):
        """Validate graph type."""
        valid_types = ["neo4j", "networkx", "knowledge_graph"]
        if v not in valid_types:
            raise ValueError(f"graph_type must be one of {valid_types}, got {v}")
        return v

    @validator("query_type")
    def validate_query_type(cls, v):
        """Validate query type."""
        valid_types = ["node", "relationship", "path", "subgraph"]
        if v not in valid_types:
            raise ValueError(f"query_type must be one of {valid_types}, got {v}")
        return v

    @validator("connection_url")
    def validate_connection_url(cls, v, values):
        """Validate connection URL for Neo4j."""
        graph_type = values.get("graph_type", "")
        if graph_type == "neo4j" and not v:
            raise ValueError("connection_url is required for Neo4j graph type")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for LlamaIndex Graph retriever."""
        return {
            "query": (str, Field(description="Query for graph-based retrieval")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for LlamaIndex Graph retriever."""
        return {
            "documents": (
                List[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved from graph traversal",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a LlamaIndex Graph retriever from this configuration.

        Returns:
            LlamaIndexGraphRetriever: Instantiated retriever ready for graph-based retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.retrievers import LlamaIndexGraphRetriever
        except ImportError:
            raise ImportError(
                "LlamaIndexGraphRetriever requires langchain-community package. "
                "Install with: pip install langchain-community llama-index"
            )

        # Prepare configuration for the retriever
        kwargs = {
            "query_type": self.query_type,
            "max_depth": self.max_depth,
            "k": self.k,
            "include_text": self.include_text,
        }

        # Add graph-specific configuration
        if self.graph_type == "neo4j":
            if not self.connection_url:
                raise ValueError("connection_url is required for Neo4j graph type")

            kwargs.update(
                {
                    "graph_type": "neo4j",
                    "connection_url": self.connection_url,
                    "database": self.database_name or "neo4j",
                }
            )

            # Add authentication if API key is provided
            api_key = (
                self.get_api_key() if hasattr(self, "get_api_key") else self.api_key
            )
            if api_key:
                kwargs["auth"] = api_key

        elif self.graph_type == "knowledge_graph":
            kwargs["graph_type"] = "knowledge_graph"

        elif self.graph_type == "networkx":
            kwargs["graph_type"] = "networkx"

        # Add optional parameters
        if self.similarity_threshold is not None:
            kwargs["similarity_threshold"] = self.similarity_threshold

        if self.include_relationships:
            kwargs["include_relationships"] = self.include_relationships

        return LlamaIndexGraphRetriever(**kwargs)
