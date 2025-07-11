"""
Vectara Vector Store implementation for the Haive framework.

This module provides a configuration class for the Vectara vector store,
which is a managed vector search platform with advanced NLP capabilities.

Vectara provides:
1. Fully managed vector search platform
2. Built-in text processing and chunking
3. Advanced query understanding and semantic search
4. Automatic summarization with grounded generation
5. Reranking capabilities (MMR, multilingual, custom)
6. Hybrid search with lexical and semantic matching
7. Support for various file formats (PDF, DOCX, HTML, etc.)

This vector store is particularly useful when:
- You need a fully managed solution with minimal setup
- Want advanced NLP features like query understanding
- Require automatic document processing and chunking
- Need summarization and grounded generation
- Want built-in reranking capabilities
- Building applications requiring high-quality semantic search

The implementation integrates with LangChain's Vectara while providing
a consistent Haive configuration interface.
"""

from typing import Any, Dict, List, Optional, Tuple, Type

from langchain_core.documents import Document
from pydantic import Field, validator

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig, SecureConfigMixin
from haive.core.engine.vectorstore.types import VectorStoreType


@BaseVectorStoreConfig.register(VectorStoreType.VECTARA)
class VectaraVectorStoreConfig(BaseVectorStoreConfig, SecureConfigMixin):
    """
    Configuration for Vectara vector store in the Haive framework.

    This vector store uses Vectara's managed platform for advanced semantic search
    with built-in NLP capabilities and document processing.

    Attributes:
        vectara_customer_id (str): Vectara customer ID.
        vectara_corpus_id (str): Vectara corpus ID.
        api_key (str): Vectara API key (SecureConfigMixin field).
        source (str): Source identifier for tracking.

    Examples:
        >>> from haive.core.engine.vectorstore import VectaraVectorStoreConfig
        >>> from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
        >>>
        >>> # Create Vectara config
        >>> config = VectaraVectorStoreConfig(
        ...     name="vectara_search",
        ...     vectara_customer_id="123456789",
        ...     vectara_corpus_id="1",
        ...     api_key="your_api_key"
        ... )
        >>>
        >>> # Note: Vectara manages embeddings internally, so embedding config is optional
        >>> # If provided, it's only used for compatibility but not actually used by Vectara
        >>>
        >>> # Instantiate and use
        >>> vectorstore = config.instantiate()
        >>>
        >>> # Add documents - Vectara handles chunking internally
        >>> docs = [Document(page_content="Vectara provides advanced semantic search")]
        >>> vectorstore.add_documents(docs)
        >>>
        >>> # Search with advanced features
        >>> results = vectorstore.similarity_search(
        ...     "semantic search platform",
        ...     k=5,
        ...     filter="doc.lang = 'eng'",
        ...     n_sentence_context=2
        ... )
        >>>
        >>> # Add files directly (Vectara processes them internally)
        >>> file_ids = vectorstore.add_files(["document.pdf", "report.docx"])
    """

    # Vectara configuration
    vectara_customer_id: str = Field(
        ...,
        description="Vectara customer ID (required, or set VECTARA_CUSTOMER_ID env var)",
    )

    vectara_corpus_id: str = Field(
        ...,
        description="Vectara corpus ID (required, or set VECTARA_CORPUS_ID env var)",
    )

    api_key: str = Field(
        ..., description="Vectara API key (required, or set VECTARA_API_KEY env var)"
    )

    # Optional configuration
    source: str = Field(
        default="langchain", description="Source identifier for tracking requests"
    )

    vectara_api_timeout: int = Field(
        default=120, ge=1, le=600, description="API timeout in seconds"
    )

    # Note: Vectara manages its own embeddings, so the embedding field from base class
    # is optional and not used, but kept for interface compatibility

    @validator("vectara_customer_id", pre=True, always=True)
    def resolve_customer_id(cls, v):
        """Resolve customer ID from value or environment."""
        if not v:
            import os

            v = os.getenv("VECTARA_CUSTOMER_ID")
            if not v:
                raise ValueError(
                    "vectara_customer_id must be provided or "
                    "VECTARA_CUSTOMER_ID environment variable must be set"
                )
        return v

    @validator("vectara_corpus_id", pre=True, always=True)
    def resolve_corpus_id(cls, v):
        """Resolve corpus ID from value or environment."""
        if not v:
            import os

            v = os.getenv("VECTARA_CORPUS_ID")
            if not v:
                raise ValueError(
                    "vectara_corpus_id must be provided or "
                    "VECTARA_CORPUS_ID environment variable must be set"
                )
        return v

    @validator("api_key", pre=True, always=True)
    def resolve_api_key(cls, v):
        """Resolve API key from value or environment."""
        if not v:
            import os

            v = os.getenv("VECTARA_API_KEY")
            if not v:
                raise ValueError(
                    "api_key must be provided or "
                    "VECTARA_API_KEY environment variable must be set"
                )
        return v

    def validate_embedding(self):
        """
        Override to make embedding optional for Vectara.

        Vectara manages its own embeddings internally, so we don't require
        an embedding configuration.
        """
        # Vectara doesn't need external embeddings
        pass

    def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return input field definitions for Vectara vector store."""
        return {
            "documents": (
                List[Document],
                Field(description="Documents to add to Vectara"),
            ),
        }

    def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]:
        """Return output field definitions for Vectara vector store."""
        return {
            "ids": (List[str], Field(description="Document IDs in Vectara")),
        }

    def instantiate(self):
        """
        Create a Vectara vector store from this configuration.

        Returns:
            Vectara: Instantiated Vectara vector store.

        Raises:
            ImportError: If required packages are not available.
            ValueError: If configuration is invalid.
        """
        try:
            from langchain_community.vectorstores import Vectara
        except ImportError as e:
            raise ImportError(
                "Vectara requires additional packages. "
                "Install with: pip install langchain-community"
            ) from e

        # Create Vectara vector store
        # Note: Vectara doesn't use embeddings parameter in constructor
        try:
            vectorstore = Vectara(
                vectara_customer_id=self.vectara_customer_id,
                vectara_corpus_id=self.vectara_corpus_id,
                vectara_api_key=self.api_key,
                source=self.source,
                vectara_api_timeout=self.vectara_api_timeout,
            )
        except Exception as e:
            raise ValueError(f"Failed to create Vectara vector store: {e}") from e

        return vectorstore
