"""
Azure Cognitive Search Vector Store implementation for the Haive framework.

This module provides a configuration class for the Azure Cognitive Search vector store,
which is Microsoft's cloud search-as-a-service solution with vector search capabilities.

Azure Cognitive Search provides:
1. Enterprise search service with vector capabilities
2. Hybrid search combining keywords and vectors
3. Built-in AI enrichment and cognitive skills
4. Multi-language support with analyzers
5. Faceted navigation and filtering
6. Geo-spatial search capabilities

This vector store is particularly useful when:
- You're building on Azure infrastructure
- Need enterprise search features beyond vectors
- Require multi-language support
- Want built-in AI enrichment pipelines
- Need compliance with data residency requirements

The implementation integrates with LangChain's Azure Search while providing
a consistent Haive configuration interface with secure credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.AZURE_SEARCH)
class AzureSearchVectorStoreConfig(SecureConfigMixin, BaseVectorStoreConfig):
    """
    Configuration for Azure Cognitive Search vector store in the Haive framework.

    This vector store uses Azure Cognitive Search for enterprise-grade search
    with vector capabilities and AI enrichment.

    Attributes:
        service_name (str): Name of the Azure Search service.
        api_key (Optional[SecretStr]): Admin API key (auto-resolved).
        index_name (str): Name of the search index.
        semantic_configuration_name (Optional[str]): Semantic search config.
        fields (List[Dict]): Field definitions for the index.
        vector_search_configuration (Dict): Vector search configuration.

    Examples:
        >>> from haive.core.engine.vectorstore import AzureSearchVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Azure Search config
        >>> config = AzureSearchVectorStoreConfig(
        ...     name="enterprise_search",
        ...     embedding=OpenAIEmbeddingConfig(),
        ...     service_name="my-search-service",
        ...     index_name="documents",
        ...     semantic_configuration_name="my-semantic-config"
        ... )
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>> docs = [Document(page_content="Azure Search supports hybrid retrieval")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Hybrid search
        >>> results = vectorstore.similarity_search(
        ...     "cloud search",
        ...     k=5,
        ...     search_type="hybrid"
        ... )
    """

    # Azure Search configuration
    service_name: str = Field(
        ..., description="Name of the Azure Cognitive Search service"
    )

    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Admin API key (auto-resolved from AZURE_SEARCH_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="azure_search", description="Provider name for API key resolution"
    )

    # Index configuration
    index_name: str = Field(
        default="langchain-index", description="Name of the search index"
    )

    # Semantic search configuration
    semantic_configuration_name: Optional[str] = Field(
        default=None,
        description="Name of the semantic configuration for semantic search",
    )

    # Field configuration
    fields: Optional[List[Dict[str, Any]]] = Field(
        default=None, description="Field definitions for the index schema"
    )

    # Vector search configuration
    vector_search_configuration: Optional[Dict[str, Any]] = Field(
        default=None, description="Vector search algorithm configuration"
    )

    # Search configuration
    search_type: str = Field(
        default="similarity",
        description="Search type: 'similarity', 'hybrid', or 'semantic_hybrid'",
    )

    # Content field names
    content_key: str = Field(
        default="content", description="Field name for document content"
    )

    vector_key: str = Field(
        default="content_vector", description="Field name for embedding vectors"
    )

    # Additional configuration
    create_index_if_not_exists: bool = Field(
        default=True, description="Whether to create the index if it doesn't exist"
    )

    api_version: str = Field(
        default="2023-11-01", description="Azure Search API version"
    )

    @validator("search_type")
    def validate_search_type(cls, v):
        """Validate search type is supported."""
        valid_types = ["similarity", "hybrid", "semantic_hybrid"]
        if v not in valid_types:
            raise ValueError(f"search_type must be one of {valid_types}, got {v}")
        return v

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Azure Search vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to the vector store"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Azure Search vector store."""
        return {
            "ids": (List[str], Field(description="Document IDs in Azure Search")),
        }

    def instantiate(self):
        """
        Create an Azure Search vector store from this configuration.

        Returns:
            AzureSearch: Instantiated Azure Search vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import AzureSearch
        except ImportError:
            raise ImportError(
                "Azure Search requires azure-search-documents package. "
                "Install with: pip install azure-search-documents"
            )

        # Validate embedding
        self.validate_embedding()
        embedding_function = self.embedding.instantiate()

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Azure Search API key is required. Set AZURE_SEARCH_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Build service endpoint
        endpoint = f"https://{self.service_name}.search.windows.net"

        # Prepare field configuration if not provided
        if not self.fields:
            # Get vector dimensions
            try:
                sample_embedding = embedding_function.embed_query("sample")
                vector_dimensions = len(sample_embedding)
            except Exception:
                vector_dimensions = 1536  # Default to common dimension

            self.fields = [
                {
                    "name": "id",
                    "type": "Edm.String",
                    "key": True,
                    "filterable": True,
                },
                {
                    "name": self.content_key,
                    "type": "Edm.String",
                    "searchable": True,
                },
                {
                    "name": self.vector_key,
                    "type": "Collection(Edm.Single)",
                    "searchable": True,
                    "vector_search_dimensions": vector_dimensions,
                    "vector_search_configuration": "default",
                },
                {
                    "name": "metadata",
                    "type": "Edm.String",
                    "searchable": True,
                },
            ]

        # Prepare vector search configuration if not provided
        if not self.vector_search_configuration:
            self.vector_search_configuration = {
                "name": "default",
                "kind": "hnsw",
                "hnsw_parameters": {
                    "metric": "cosine",
                    "m": 4,
                    "ef_construction": 400,
                    "ef_search": 500,
                },
            }

        # Prepare kwargs
        kwargs = {
            "azure_search_endpoint": endpoint,
            "azure_search_key": api_key,
            "index_name": self.index_name,
            "embedding_function": embedding_function,
            "fields": self.fields,
            "vector_search": self.vector_search_configuration,
            "search_type": self.search_type,
            "api_version": self.api_version,
        }

        # Add semantic configuration if provided
        if self.semantic_configuration_name:
            kwargs["semantic_configuration_name"] = self.semantic_configuration_name

        # Create Azure Search vector store
        vectorstore = AzureSearch(**kwargs)

        # Create index if it doesn't exist
        if self.create_index_if_not_exists:
            try:
                # Check if index exists by trying to get it
                from azure.core.credentials import AzureKeyCredential
                from azure.search.documents.indexes import SearchIndexClient

                index_client = SearchIndexClient(
                    endpoint=endpoint,
                    credential=AzureKeyCredential(api_key),
                    api_version=self.api_version,
                )

                try:
                    index_client.get_index(self.index_name)
                except Exception:
                    # Index doesn't exist, create it
                    from azure.search.documents.indexes.models import (
                        HnswAlgorithmConfiguration,
                        SearchField,
                        SearchFieldDataType,
                        SearchIndex,
                        VectorSearch,
                    )

                    # Convert field definitions to SearchField objects
                    search_fields = []
                    for field in self.fields:
                        search_field = SearchField(
                            name=field["name"],
                            type=field["type"],
                            key=field.get("key", False),
                            searchable=field.get("searchable", False),
                            filterable=field.get("filterable", False),
                            sortable=field.get("sortable", False),
                            facetable=field.get("facetable", False),
                        )

                        # Add vector search properties if applicable
                        if "vector_search_dimensions" in field:
                            search_field.vector_search_dimensions = field[
                                "vector_search_dimensions"
                            ]
                            search_field.vector_search_configuration = field.get(
                                "vector_search_configuration", "default"
                            )

                        search_fields.append(search_field)

                    # Create vector search configuration
                    vector_search = VectorSearch(
                        algorithms=[
                            HnswAlgorithmConfiguration(
                                name=self.vector_search_configuration["name"],
                                parameters=self.vector_search_configuration.get(
                                    "hnsw_parameters", {}
                                ),
                            )
                        ]
                    )

                    # Create index
                    index = SearchIndex(
                        name=self.index_name,
                        fields=search_fields,
                        vector_search=vector_search,
                    )

                    index_client.create_index(index)

            except Exception as e:
                # Index creation might fail, but we can continue
                import warnings

                warnings.warn(f"Could not create search index: {e}")

        return vectorstore
