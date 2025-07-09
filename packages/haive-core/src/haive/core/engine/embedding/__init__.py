"""Embedding engine module for the Haive framework.

This module provides comprehensive embedding functionality with support for
multiple providers including OpenAI, Azure OpenAI, HuggingFace, Cohere,
Google Vertex AI, Ollama, and more.

Examples:
    Basic usage::

        from haive.core.engine.embedding import BaseEmbeddingConfig
        from haive.core.engine.embedding.providers import OpenAIEmbeddingConfig

        # Create configuration
        config = OpenAIEmbeddingConfig(
            name="my_embeddings",
            model="text-embedding-3-large"
        )

        # Instantiate embeddings
        embeddings = config.instantiate()

        # Embed text
        vectors = embeddings.embed_documents(["Hello world", "How are you?"])
        query_vector = embeddings.embed_query("Hello")

    Configuration discovery::

        from haive.core.engine.embedding import BaseEmbeddingConfig

        # List all providers
        providers = BaseEmbeddingConfig.list_registered_types()

        # Get specific provider
        provider_class = BaseEmbeddingConfig.get_config_class("OpenAI")

    Using the factory::

        from haive.core.engine.embedding import create_embedding_config

        config = create_embedding_config(
            provider="OpenAI",
            model="text-embedding-3-large",
            name="my_embeddings"
        )

        embeddings = config.instantiate()

"""

# Import providers to trigger registration
from . import providers
from .base import BaseEmbeddingConfig
from .config import EmbeddingConfigFactory, create_embedding_config
from .types import EmbeddingType

__all__ = [
    "BaseEmbeddingConfig",
    "EmbeddingType",
    "create_embedding_config",
    "EmbeddingConfigFactory",
    "providers",
]
