"""Remote LangChain Retriever implementation for the Haive framework.

This module provides a configuration class for the Remote LangChain retriever,
which enables retrieval from remote LangChain services and endpoints,
allowing distributed and federated retrieval architectures.

The RemoteLangChainRetriever works by:
1. Connecting to remote LangChain retrieval endpoints
2. Sending queries to distributed retrieval services
3. Receiving and processing results from remote systems
4. Providing unified access to distributed retrieval infrastructure

This retriever is particularly useful when:
- Building distributed retrieval architectures
- Need to access remote LangChain services
- Implementing federated search across multiple systems
- Building microservice-based retrieval infrastructures

The implementation integrates with LangChain Community's RemoteLangChainRetriever while
providing a consistent Haive configuration interface with secure endpoint management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from pydantic import Field, SecretStr, validator

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.REMOTE_LANGCHAIN)
class RemoteLangChainRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Remote LangChain retriever in the Haive framework.

    This retriever enables retrieval from remote LangChain services and endpoints,
    allowing distributed and federated retrieval architectures.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always REMOTE_LANGCHAIN).
        endpoint_url (str): URL of the remote LangChain retrieval endpoint.
        api_key (Optional[SecretStr]): API key for authentication (auto-resolved).
        k (int): Number of documents to return.
        timeout (int): Request timeout in seconds.

    Examples:
        >>> from haive.core.engine.retriever import RemoteLangChainRetrieverConfig
        >>>
        >>> # Create remote LangChain retriever
        >>> config = RemoteLangChainRetrieverConfig(
        ...     name="remote_retriever",
        ...     endpoint_url="https://api.example.com/retrieve",
        ...     k=5,
        ...     timeout=30
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("distributed systems architecture")
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.REMOTE_LANGCHAIN, description="The type of retriever"
    )

    # Remote endpoint configuration
    endpoint_url: str = Field(
        ..., description="URL of the remote LangChain retrieval endpoint"
    )

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None,
        description="API key for remote endpoint authentication (auto-resolved)",
    )

    # Provider for SecureConfigMixin
    provider: str = Field(default="remote_langchain", description="Provider identifier")

    # Retrieval parameters
    k: int = Field(
        default=4,
        ge=1,
        le=100,
        description="Number of documents to return from remote service",
    )

    # Connection configuration
    timeout: int = Field(
        default=30, ge=5, le=300, description="Request timeout in seconds"
    )

    max_retries: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Maximum number of retry attempts for failed requests",
    )

    # Request headers
    custom_headers: dict[str, str] = Field(
        default_factory=dict, description="Custom headers to send with requests"
    )

    # Authentication method
    auth_method: str = Field(
        default="api_key",
        description="Authentication method: 'api_key', 'bearer_token', 'basic'",
    )

    @validator("endpoint_url")
    def validate_endpoint_url(self, v):
        """Validate endpoint URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("endpoint_url must start with http:// or https://")
        return v

    @validator("auth_method")
    def validate_auth_method(self, v):
        """Validate authentication method."""
        valid_methods = ["api_key", "bearer_token", "basic", "none"]
        if v not in valid_methods:
            raise ValueError(f"auth_method must be one of {valid_methods}, got {v}")
        return v

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Remote LangChain retriever."""
        return {
            "query": (
                str,
                Field(description="Query for remote LangChain retrieval service"),
            ),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Remote LangChain retriever."""
        return {
            "documents": (
                list[Any],  # List[Document] but avoiding import
                Field(
                    default_factory=list,
                    description="Documents retrieved from remote LangChain service",
                ),
            ),
        }

    def instantiate(self):
        """Create a Remote LangChain retriever from this configuration.

        Returns:
            RemoteLangChainRetriever: Instantiated retriever ready for remote retrieval.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.retrievers import RemoteLangChainRetriever
        except ImportError:
            raise ImportError(
                "RemoteLangChainRetriever requires langchain-community package. "
                "Install with: pip install langchain-community requests"
            )

        # Prepare configuration
        kwargs = {
            "url": self.endpoint_url,
            "k": self.k,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
        }

        # Add authentication if configured
        if self.auth_method != "none":
            api_key = self.get_api_key()
            if api_key:
                if self.auth_method == "api_key":
                    kwargs["api_key"] = api_key
                elif self.auth_method == "bearer_token":
                    kwargs["headers"] = {"Authorization": f"Bearer {api_key}"}
                elif self.auth_method == "basic":
                    import base64

                    encoded = base64.b64encode(f"user:{api_key}".encode()).decode()
                    kwargs["headers"] = {"Authorization": f"Basic {encoded}"}

        # Add custom headers
        if self.custom_headers:
            headers = kwargs.get("headers", {})
            headers.update(self.custom_headers)
            kwargs["headers"] = headers

        return RemoteLangChainRetriever(**kwargs)
