"""Zep Retriever implementation for the Haive framework.

This module provides a configuration class for the Zep retriever,
which retrieves conversation history and memory from Zep's long-term memory store.
Zep is designed for storing, searching, and enriching conversational AI chat histories
with metadata, summaries, and semantic search capabilities.

The ZepRetriever works by:
1. Connecting to a Zep memory store
2. Searching conversation history using semantic similarity
3. Retrieving relevant chat messages and context
4. Providing conversation memory for AI applications

This retriever is particularly useful when:
- Building conversational AI applications with long-term memory
- Need to retrieve relevant conversation history
- Want to maintain context across multiple chat sessions
- Building customer support or chatbot applications
- Creating personalized AI assistants with memory

The implementation integrates with LangChain's ZepRetriever while providing
a consistent Haive configuration interface with secure API key management.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType


@BaseRetrieverConfig.register(RetrieverType.ZEP)
class ZepRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    """Configuration for Zep retriever in the Haive framework.

    This retriever searches conversational memory stored in Zep and returns
    relevant chat history and context for AI applications.

    Attributes:
        retriever_type (RetrieverType): The type of retriever (always ZEP).
        session_id (str): Zep session ID for conversation history.
        url (str): Zep server URL.
        api_key (Optional[SecretStr]): Zep API key (auto-resolved from ZEP_API_KEY).
        top_k (int): Number of memory entries to retrieve.
        search_type (str): Type of search to perform.
        search_scope (str): Scope of search (messages, summary, etc.).

    Examples:
        >>> from haive.core.engine.retriever import ZepRetrieverConfig
        >>>
        >>> # Create the Zep retriever config
        >>> config = ZepRetrieverConfig(
        ...     name="zep_retriever",
        ...     session_id="user-123-session",
        ...     url="http://localhost:8000",
        ...     top_k=10,
        ...     search_type="similarity",
        ...     search_scope="messages"
        ... )
        >>>
        >>> # Instantiate and use the retriever
        >>> retriever = config.instantiate()
        >>> docs = retriever.get_relevant_documents("what did we discuss about machine learning?")
        >>>
        >>> # Example for summary search
        >>> summary_config = ZepRetrieverConfig(
        ...     name="zep_summary_retriever",
        ...     session_id="user-123-session",
        ...     url="http://localhost:8000",
        ...     search_scope="summary",
        ...     top_k=5
        ... )
    """

    retriever_type: RetrieverType = Field(
        default=RetrieverType.ZEP, description="The type of retriever"
    )

    # Zep connection configuration
    session_id: str = Field(..., description="Zep session ID for conversation history")

    url: str = Field(..., description="Zep server URL (e.g., 'http://localhost:8000')")

    # API configuration with SecureConfigMixin
    api_key: SecretStr | None = Field(
        default=None, description="Zep API key (auto-resolved from ZEP_API_KEY)"
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

    metadata_filter: dict[str, Any] | None = Field(
        default=None, description="Metadata filters for search"
    )

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for Zep retriever."""
        return {
            "query": (str, Field(description="Search query for conversation memory")),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for Zep retriever."""
        return {
            "documents": (
                list[Document],
                Field(
                    default_factory=list,
                    description="Conversation history from Zep memory",
                ),
            ),
        }

    def instantiate(self):
        """Create a Zep retriever from this configuration.

        Returns:
            ZepRetriever: Instantiated retriever ready for memory search.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If session configuration is invalid.
        """
        try:
            from langchain_community.retrievers import ZepRetriever
        except ImportError:
            raise ImportError(
                "ZepRetriever requires langchain-community and zep-python packages. "
                "Install with: pip install langchain-community zep-python"
            )

        if not self.session_id:
            raise ValueError(
                "Zep session ID is required for conversation memory retrieval."
            )

        # Get API key using SecureConfigMixin
        api_key = self.get_api_key()

        # Prepare configuration
        config = {"session_id": self.session_id, "url": self.url, "top_k": self.top_k}

        # Add API key if available
        if api_key:
            config["api_key"] = api_key

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

        return ZepRetriever(**config)
