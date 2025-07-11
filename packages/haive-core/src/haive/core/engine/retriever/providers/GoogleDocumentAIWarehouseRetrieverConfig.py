"""
Google Document AI Warehouse Retriever implementation for the Haive framework.

This module provides a configuration class for the Google Document AI Warehouse retriever,
which uses Google Cloud's Document AI Warehouse service for intelligent document
processing and retrieval. Document AI Warehouse provides advanced document
understanding, classification, and search capabilities.

The GoogleDocumentAIWarehouseRetriever works by:
1. Connecting to a Document AI Warehouse project
2. Performing intelligent document search and retrieval
3. Leveraging ML for document understanding and classification
4. Supporting various document types and formats

This retriever is particularly useful when:
- Building document management systems
- Need intelligent document processing
- Working with complex document formats
- Want ML-powered document classification
- Building compliance and governance tools

The implementation integrates with LangChain's GoogleDocumentAIWarehouseRetriever while
providing a consistent Haive configuration interface with secure GCP credential management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.GOOGLE_DOCUMENT_AI_WAREHOUSE)
class GoogleDocumentAIWarehouseRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Google Document AI Warehouse retriever in the Haive framework.

    This retriever uses Google Cloud Document AI Warehouse to provide intelligent
    document processing and retrieval with ML-powered understanding.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always GOOGLE_DOCUMENT_AI_WAREHOUSE).
        project_number (str): Google Cloud project number.
        location (str): Google Cloud location.
        document_schema_id (str): Document schema ID for the warehouse.
        api_key (Optional[SecretStr]): Service account key (auto-resolved from GOOGLE_APPLICATION_CREDENTIALS).
        num_results (int): Number of results to retrieve.

    Examples:
        >>> from haive.core.engine.retriever import GoogleDocumentAIWarehouseRetrieverConfig
        >>>
        >>> # Create the Document AI Warehouse retriever config
        >>> config = GoogleDocumentAIWarehouseRetrieverConfig(
        ...     name="doc_ai_warehouse_retriever",
        ...     project_number="123456789012",
        ...     location="us",
        ...     document_schema_id="schema_id_123",
        ...     num_results=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("contract analysis documents")
        >>>
        >>> # Example with specific schema
        >>> contract_config = GoogleDocumentAIWarehouseRetrieverConfig(
        ...     name="contract_doc_ai_retriever",
        ...     project_number="123456789012",
        ...     location="us",
        ...     document_schema_id="contract_schema_456",
        ...     num_results=5
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.GOOGLE_DOCUMENT_AI_WAREHOUSE,
        description="The type of retriever",
    )

    # Google Cloud Document AI Warehouse configuration
    project_number: str = Field(
        ..., description="Google Cloud project number (not project ID)"
    )

    location: str = Field(
        default="us", description="Google Cloud location (e.g., 'us', 'eu')"
    )

    document_schema_id: str = Field(
        ..., description="Document schema ID for the warehouse"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None,
        description="Service account key path (auto-resolved from GOOGLE_APPLICATION_CREDENTIALS)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="google", description="Provider name for credential resolution"
    )

    # Search parameters
    num_results: int = Field(
        default=10, ge=1, le=100, description="Number of results to retrieve"
    )

    # Document filtering
    document_query: Optional[str] = Field(
        default=None, description="Structured query for document filtering"
    )

    # Advanced search parameters
    require_all_terms: bool = Field(
        default=False, description="Whether to require all search terms to match"
    )

    folder_id: Optional[str] = Field(
        default=None, description="Specific folder ID to search within"
    )

    # Request metadata
    request_metadata: Optional[Dict[str, Any]] = Field(
        default=None, description="Additional metadata for the search request"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Google Document AI Warehouse retriever."""
        return {
            "query": (str, Field(description="Document search query for AI Warehouse")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Google Document AI Warehouse retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Documents from Document AI Warehouse",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Google Document AI Warehouse retriever from this configuration.

        Returns:
            GoogleDocumentAIWarehouseRetriever: Instantiated retriever ready for document search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If GCP credentials or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import (
                GoogleDocumentAIWarehouseRetriever,
            )
        except ImportError:
            raise ImportError(
                "GoogleDocumentAIWarehouseRetriever requires langchain-community and "
                "google-cloud-documentai packages. "
                "Install with: pip install langchain-community google-cloud-documentai"
            )

        # Handle credentials
        credentials_path = self.get_api_key()
        if credentials_path:
            import os

            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # Prepare configuration
        config = {
            "project_number": self.project_number,
            "location": self.location,
            "document_schema_id": self.document_schema_id,
            "num_results": self.num_results,
        }

        # Add optional parameters
        if self.document_query:
            config["document_query"] = self.document_query

        if self.folder_id:
            config["folder_id"] = self.folder_id

        if self.request_metadata:
            config["request_metadata"] = self.request_metadata

        config["require_all_terms"] = self.require_all_terms

        return GoogleDocumentAIWarehouseRetriever(**config)
