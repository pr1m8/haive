"""
Zep Cloud Retriever implementation for the Haive framework.

This module provides a configuration class for the Zep Cloud retriever,
which retrieves conversation history and memory from Zep's cloud-hosted
memory service. Zep Cloud provides managed long-term memory storage
for conversational AI applications with enhanced features and reliability.

The ZepCloudRetriever works by:
1. Connecting to Zep Cloud service
2. Searching conversation history using semantic similarity
3. Retrieving relevant chat messages and context
4. Providing managed conversation memory

This retriever is particularly useful when:
- Building conversational AI with cloud-hosted memory
- Need reliable managed memory infrastructure
- Want enhanced Zep features and performance
- Building scalable chatbot applications
- Need conversation history across sessions

The implementation integrates with LangChain's ZepCloudRetriever while
providing a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ZEP_CLOUD)
class ZepCloudRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """
    Configuration for Zep Cloud retriever in the Haive framework.

    This retriever searches conversational memory stored in Zep Cloud and returns
    relevant chat history and context for AI applications.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ZEP_CLOUD).
        session_id (str): Zep session ID for conversation history.
        api_key (Optional[SecretStr]): Zep Cloud API key (auto-resolved from ZEP_API_KEY).
        api_url (str): Zep Cloud API URL.
        top_k (int): Number of memory entries to retrieve.
        search_type (str): Type of search to perform.

    Examples:
        >>> from haive.core.engine.retriever import ZepCloudRetrieverConfig
        >>>
        >>> # Create the Zep Cloud retriever config
        >>> config = ZepCloudRetrieverConfig(
        ...     name="zep_cloud_retriever",
        ...     session_id="user-123-session",
        ...     api_url="https://api.getzep.com",
        ...     top_k=10,
        ...     search_type="similarity"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("what did we discuss about AI?")
        >>>
        >>> # Example for MMR search
        >>> mmr_config = ZepCloudRetrieverConfig(
        ...     name="zep_cloud_mmr_retriever",
        ...     session_id="user-123-session",
        ...     api_url="https://api.getzep.com",
        ...     search_type="mmr",
        ...     mmr_lambda=0.7
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ZEP_CLOUD, description="The type of retriever"
    )

    # Zep Cloud configuration
    session_id: str = Field(..., description="Zep session ID for conversation history")

    api_url: str = Field(
        default="https://api.getzep.com", description="Zep Cloud API URL"
    )

    # API configuration with SecureConfigMixin
    api_key: Optional[SecretStr] = Field(
        default=None, description="Zep Cloud API key (auto-resolved from ZEP_API_KEY)"
    )

    # Provider for SecureConfigMixin
    provider: str = Field(
        default="zep", description="Provider name for API key resolution"
    )

    # Search configuration
    top_k: int = Field(
        default=10, ge=1, le=100, description="Number of memory entries to retrieve"
    )

    search_type: str = Field(
        default="similarity",
        description="Search type: 'similarity', 'mmr' (maximal marginal relevance)",
    )

    search_scope: str = Field(
        default="messages", description="Search scope: 'messages', 'summary', 'both'"
    )

    # Advanced search parameters
    mmr_lambda: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Lambda parameter for MMR search (diversity vs relevance)",
    )

    metadata_filter: Optional[Dict[str, Any]] = Field(
        default=None, description="Metadata filters for search"
    )

    # Cloud-specific parameters
    user_id: Optional[str] = Field(
        default=None, description="User ID for multi-user memory isolation"
    )

    project_id: Optional[str] = Field(
        default=None, description="Project ID for organizing memory across projects"
    )

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Zep Cloud retriever."""
        return {
            "query": (str, Field(description="Search query for conversation memory")),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Zep Cloud retriever."""
        return {
            "documents": (
                List[Document],
                Field(
                    default_factory=list,
                    description="Conversation history from Zep Cloud",
                ),
            ),
        }

    def instantiate(self):
        """
        Create a Zep Cloud retriever from this configuration.

        Returns:
            ZepCloudRetriever: Instantiated retriever ready for cloud memory search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If API key or session configuration is invalid.
        """
        try:
            from langchain_community.retrievers import ZepCloudRetriever
        except ImportError:
            raise ImportError(
                "ZepCloudRetriever requires langchain-community and zep-python packages. "
                "Install with: pip install langchain-community zep-python"
            )

        if not self.session_id:
            raise ValueError(
                "Zep session ID is required for conversation memory retrieval."
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()
        if not api_key:
            raise ValueError(
                "Zep Cloud API key is required. Set ZEP_API_KEY environment variable "
                "or provide api_key parameter."
            )

        # Prepare configuration
        config = {
            "session_id": self.session_id,
            "api_url": self.api_url,
            "api_key": api_key,
            "top_k": self.top_k,
        }

        # Add search configuration
        if self.search_type == "mmr":
            config["search_type"] = "mmr"
            config["mmr_lambda"] = self.mmr_lambda
        else:
            config["search_type"] = "similarity"

        # Add search scope
        config["search_scope"] = self.search_scope

        # Add metadata filter if provided
        if self.metadata_filter:
            config["metadata"] = self.metadata_filter

        # Add cloud-specific parameters
        if self.user_id:
            config["user_id"] = self.user_id

        if self.project_id:
            config["project_id"] = self.project_id

        return ZepCloudRetriever(**config)
