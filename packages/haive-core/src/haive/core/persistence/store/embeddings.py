# src/haive/core/persistence/store/embeddings.py
"""Embedding adapter for integrating Haive embeddings with LangGraph stores.

This module provides adapters to convert Haive's embedding configurations
to the format expected by LangGraph stores.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class EmbeddingAdapter:
    """Adapts Haive embedding configs to LangGraph embedding functions.

    This adapter handles the conversion between Haive's rich embedding
    configuration system and the simpler embedding functions expected
    by LangGraph stores.
    """

    @staticmethod
    def create_embedding_function(
        provider: str, dims: int, config: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """Create an embedding function from provider string.

        Args:
            provider: Provider string (e.g., "openai:text-embedding-3-small")
            dims: Embedding dimensions
            config: Additional configuration

        Returns:
            Embedding function or None if creation fails
        """
        try:
            # Try to use Haive's embedding system
            from haive.core.models.embeddings.base import (
                EmbeddingProvider,
                HuggingFaceEmbeddingConfig,
                OpenAIEmbeddingConfig,
                create_embeddings,
            )

            # Parse provider string
            if ":" in provider:
                provider_type, model = provider.split(":", 1)
            else:
                provider_type = provider
                model = None

            # Create appropriate config
            if provider_type.lower() == "openai":
                embedding_config = OpenAIEmbeddingConfig(
                    provider=EmbeddingProvider.OPENAI,
                    model=model or "text-embedding-3-small",
                    dimensions=dims,
                )
            elif provider_type.lower() == "huggingface":
                embedding_config = HuggingFaceEmbeddingConfig(
                    provider=EmbeddingProvider.HUGGINGFACE,
                    model=model or "sentence-transformers/all-MiniLM-L6-v2",
                )
            else:
                # Try generic langchain embeddings
                from langchain.embeddings import init_embeddings

                return init_embeddings(provider)

            # Create embeddings instance
            embeddings = create_embeddings(embedding_config)

            # Return a function that matches LangGraph's expected signature
            def embed_texts(texts: List[str]) -> List[List[float]]:
                """Embed texts using Haive embeddings."""
                if hasattr(embeddings, "embed_documents"):
                    return embeddings.embed_documents(texts)
                else:
                    # Fallback for single text embedding
                    return [embeddings.embed_query(text) for text in texts]

            return embed_texts

        except Exception as e:
            logger.warning(f"Failed to create embedding function: {e}")

            # Try fallback to langchain
            try:
                from langchain.embeddings import init_embeddings

                embeddings = init_embeddings(provider)

                def embed_texts(texts: List[str]) -> List[List[float]]:
                    return embeddings.embed_documents(texts)

                return embed_texts
            except Exception as e2:
                logger.error(f"Failed to create any embedding function: {e2}")
                return None

    @staticmethod
    def create_async_embedding_function(
        provider: str, dims: int, config: Optional[Dict[str, Any]] = None
    ) -> Optional[Any]:
        """Create an async embedding function from provider string.

        Args:
            provider: Provider string
            dims: Embedding dimensions
            config: Additional configuration

        Returns:
            Async embedding function or None if creation fails
        """
        # First try to get sync function
        sync_func = EmbeddingAdapter.create_embedding_function(provider, dims, config)
        if not sync_func:
            return None

        # Check if we have async support
        try:
            from haive.core.models.embeddings.base import (
                EmbeddingProvider,
                OpenAIEmbeddingConfig,
                create_embeddings,
            )

            # Parse provider
            if ":" in provider:
                provider_type, model = provider.split(":", 1)
            else:
                provider_type = provider
                model = None

            # Create config and embeddings
            if provider_type.lower() == "openai":
                embedding_config = OpenAIEmbeddingConfig(
                    provider=EmbeddingProvider.OPENAI,
                    model=model or "text-embedding-3-small",
                    dimensions=dims,
                )
                embeddings = create_embeddings(embedding_config)

                # Check for async support
                if hasattr(embeddings, "aembed_documents"):

                    async def aembed_texts(texts: List[str]) -> List[List[float]]:
                        """Async embed texts using Haive embeddings."""
                        return await embeddings.aembed_documents(texts)

                    return aembed_texts
        except Exception as e:
            logger.debug(f"No async embedding support: {e}")

        # Fallback to sync wrapper
        async def aembed_texts(texts: List[str]) -> List[List[float]]:
            """Async wrapper around sync embedding function."""
            return sync_func(texts)

        return aembed_texts
