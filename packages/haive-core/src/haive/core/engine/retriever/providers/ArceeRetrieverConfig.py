"""Arcee Retriever implementation for the Haive framework.

This module provides a configuration class for the Arcee retriever,
which provides AI/ML focused retrieval capabilities through the Arcee service
for domain-specific artificial intelligence and machine learning content.

The ArceeRetriever works by:
1. Connecting to the Arcee API service for AI/ML domain retrieval
2. Performing specialized search across AI/ML focused content
3. Retrieving relevant documents with domain-specific understanding
4. Providing high-quality results for technical AI/ML queries

This retriever is particularly useful when:
- Building AI/ML focused applications and research tools
- Need specialized retrieval for technical AI/ML content
- Working with domain-specific artificial intelligence queries
- Building systems that require expert-level AI/ML knowledge retrieval

The implementation integrates with LangChain Community's ArceeRetriever while
providing a consistent Haive configuration interface with secure API management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ARCEE)
class ArceeRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Arcee retriever in the Haive framework.

    This retriever provides AI/ML focused retrieval capabilities through the Arcee
    service for domain-specific artificial intelligence and machine learning content.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ARCEE).
        api_key (Optional[SecretStr]): API key for Arcee service (auto-resolved).
        model_name (str): Arcee model name to use for retrieval.
        k (int): Number of documents to return.
        endpoint_url (Optional[str]): Custom endpoint URL for Arcee service.

    Examples:
        >>> from haive.core.engine.retriever import ArceeRetrieverConfig
        >>>
        >>> # Create Arcee retriever
        >>> config = ArceeRetrieverConfig(
        ...     name="arcee_retriever",
        ...     model_name="arcee-ai/AI-Retriever-v1",
        ...     k=5
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest transformer architectures")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ARCEE, description="The type of retriever"
    )

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None,
        description="API key for Arcee service (auto-resolved from ARCEE_API_KEY)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(default="arcee", description="Provider identifier for Arcee")

    # Model configuration
    model_name: str = Field(
        default="arcee-ai/AI-Retriever-v1",
        description="Arcee model name to use for AI/ML focused retrieval",
    )

    # Retrieval parameters
    k: int = Field(default=4, ge=1, le=100, description="Number of documents to return")

    # Service configuration
    endpoint_url: str | None = Field(
        default=None,
        description="Custom endpoint URL for Arcee service (uses default if None)",
    )

    # Additional parameters
    temperature: float = Field(
        default=0.0,
        ge=0.0,
        le=2.0,
        description="Temperature for retrieval (affects result diversity)",
    )

    max_tokens: int | None = Field(
        default=None, ge=1, le=8192, description="Maximum tokens per retrieved document"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Arcee retriever."""
        return {
            "query": (
                str,
                Field(description="AI/ML focused query for specialized retrieval"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Arcee retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="AI/ML focused documents from Arcee service",
                ),
            ),
        }

    def instantiate(self):
        """Create an Arcee retriever from this configuration.

        Returns:
            ArceeRetriever: Instantiated retriever ready for AI/ML focused retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or configuration is invalid.
        """
        try:
            from langchain_community.retrievers import ArceeRetriever
        except ImportError:
            raise ImportError(
                "ArceeRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        # Get API key
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Arcee API key is required. Set ARCEE_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare configuration
        kwargs = {
            "model": self.model_name,
            "api_key": api_key,
            "k": self.k,
            "temperature": self.temperature,
        }

        # Add optional parameters
        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url

        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        return ArceeRetriever(**kwargs)
