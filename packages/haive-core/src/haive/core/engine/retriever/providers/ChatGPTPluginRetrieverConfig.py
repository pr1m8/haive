"""
ChatGPT Plugin Retriever implementation for the Haive framework.

This module provides a configuration class for the ChatGPT Plugin retriever,
which integrates with ChatGPT plugins to retrieve information from external
services and APIs. This enables access to real-time data and specialized
knowledge sources through the ChatGPT plugin ecosystem.

The ChatGPTPluginRetriever works by:
1. Connecting to ChatGPT plugin APIs
2. Making requests to plugin endpoints
3. Processing plugin responses into documents
4. Supporting various plugin types and formats

This retriever is particularly useful when:
- Integrating with existing ChatGPT plugins
- Need access to real-time external data
- Want to leverage specialized plugin knowledge
- Building systems that use plugin ecosystems
- Accessing services through plugin interfaces

The implementation integrates with LangChain's ChatGPTPluginRetriever while
providing a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.CHATGPT_PLUGIN)
class ChatGPTPluginRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for ChatGPT Plugin retriever in the Haive framework.

    This retriever integrates with ChatGPT plugins to access external
    services and data sources through the plugin ecosystem.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always CHATGPT_PLUGIN).
        plugin_url (str): URL of the ChatGPT plugin.
        api_key (Optional[SecretStr]): API key for plugin authentication.
        plugin_name (str): Name of the plugin.
        top_k (int): Number of results to retrieve.
        aiopg_dsn (Optional[str]): Database connection string for plugin data.

    Examples:
        >>> from haive.core.engine.retriever import ChatGPTPluginRetrieverConfig
        >>>
        >>> # Create the ChatGPT Plugin retriever config
        >>> config = ChatGPTPluginRetrieverConfig(
        ...     name="chatgpt_plugin_retriever",
        ...     plugin_url="https://api.example-plugin.com",
        ...     plugin_name="ExamplePlugin",
        ...     top_k=10
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("latest product information")
        >>>
        >>> # Example with database connection
        >>> db_config = ChatGPTPluginRetrieverConfig(
        ...     name="db_chatgpt_plugin_retriever",
        ...     plugin_url="https://api.db-plugin.com",
        ...     plugin_name="DatabasePlugin",
        ...     aiopg_dsn="postgresql://user:pass@host:port/db"
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.CHATGPT_PLUGIN, description="The type of retriever"
    )

    # Plugin configuration
    plugin_url: str = Field(..., description="URL of the ChatGPT plugin API")

    plugin_name: str = Field(..., description="Name of the ChatGPT plugin")

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="API key for plugin authentication"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="chatgpt_plugin", description="Provider name for API key resolution"
    )

    # Search parameters
    top_k: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Number of results to retrieve from plugin",
    )

    # Plugin-specific parameters
    plugin_manifest_url: Optional[str] = Field(
        default=None, description="URL to the plugin manifest file"
    )

    plugin_openapi_url: Optional[str] = Field(
        default=None, description="URL to the plugin OpenAPI specification"
    )

    # Database connection for plugin data
    aiopg_dsn: Optional[str] = Field(
        default=None, description="PostgreSQL connection string for plugin data storage"
    )

    # Request configuration
    timeout: float = Field(
        default=30.0, ge=1.0, le=300.0, description="Request timeout in seconds"
    )

    max_retries: int = Field(
        default=3, ge=0, le=10, description="Maximum number of request retries"
    )

    # Advanced parameters
    user_agent: str = Field(
        default="HaiveFramework/1.0",
        description="User agent string for plugin requests",
    )

    headers: Optional[Dict[str, str]] = Field(
        default=None, description="Additional headers for plugin requests"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for ChatGPT Plugin retriever."""
        return {
            "query": (str, Field(description="Query for ChatGPT plugin")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for ChatGPT Plugin retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list, description="Documents from ChatGPT plugin"
                ),
            ),
        }

    def instantiate(self):
        """
        Create a ChatGPT Plugin retriever from this configuration.

        Returns:
            ChatGPTPluginRetriever: Instantiated retriever ready for plugin integration.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If plugin configuration is invalid.
        """
        try:
            from langchain_community.retrievers import ChatGPTPluginRetriever
        except ImportError:
            raise ImportError(
                "ChatGPTPluginRetriever requires langchain-community package. "
                "Install with: pip install langchain-community"
            )

        if not self.plugin_url or not self.plugin_name:
            raise ValueError(
                "Plugin URL and name are required for ChatGPT plugin retrieval."
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()

        # Prepare configuration
        config = {
            "url": self.plugin_url,
            "plugin_name": self.plugin_name,
            "top_k": self.top_k,
            "timeout": self.timeout,
            "max_retries": self.max_retries,
            "user_agent": self.user_agent,
        }

        # Add API key if available
        if api_key:
            config["api_key"] = api_key

        # Add optional URLs
        if self.plugin_manifest_url:
            config["manifest_url"] = self.plugin_manifest_url

        if self.plugin_openapi_url:
            config["openapi_url"] = self.plugin_openapi_url

        # Add database connection if specified
        if self.aiopg_dsn:
            config["aiopg_dsn"] = self.aiopg_dsn

        # Add custom headers
        if self.headers:
            config["headers"] = self.headers

        return ChatGPTPluginRetriever(**config)
