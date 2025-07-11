"""Haive Embeddings Module.

This module provides comprehensive abstractions and implementations for working with
text embedding models from various providers. Embeddings are vector representations
of text that capture semantic meaning, enabling similarity search, clustering,
and other NLP applications.

The module supports a wide range of embedding providers with a consistent interface
for configuration and use.

Supported Cloud Providers:
    - Azure OpenAI: Microsoft's hosted OpenAI embedding models
    - OpenAI: Direct OpenAI embedding models
    - Cohere: Specialized embedding models from Cohere
    - Jina AI: Jina AI embedding models
    - Google Vertex AI: Google Cloud's machine learning platform
    - AWS Bedrock: Amazon's foundation model service
    - Cloudflare Workers AI: Cloudflare's AI model hosting
    - Voyage AI: Specialized embedding models from Voyage AI
    - Anyscale: Anyscale embedding models

Supported Local/Self-hosted Providers:
    - HuggingFace: Open-source embedding models from the HuggingFace model hub
    - SentenceTransformers: Efficient sentence embedding models
    - FastEmbed: Lightweight embedding models optimized for CPU
    - Ollama: Local embedding models via Ollama
    - LlamaCpp: Local embedding models via llama.cpp

Key Components:
    - Base Classes: Abstract base classes for embedding configurations
    - Provider Types: Enumeration of supported embedding providers
    - Provider Implementations: Provider-specific configuration classes
    - Factory Functions: Simplified creation of embedding instances
    - Security: Secure handling of API keys with environment variable resolution
    - Caching: Efficient caching of embeddings for performance optimization

Typical usage example:
    ```python
    from haive.core.models.embeddings import create_embeddings, OpenAIEmbeddingConfig

    # Configure an embedding model
    config = OpenAIEmbeddingConfig(
        model="text-embedding-3-small"
    )

    # Create the embeddings
    embeddings = create_embeddings(config)

    # Generate embeddings
    doc_vectors = embeddings.embed_documents(["Document text"])
    query_vector = embeddings.embed_query("Query text")
    ```
"""

from haive.core.models.embeddings.base import (  # Base classes; Cloud providers; Local providers; Factory function
    AnyscaleEmbeddingConfig,
    AzureEmbeddingConfig,
    BaseEmbeddingConfig,
    BedrockEmbeddingConfig,
    CloudflareEmbeddingConfig,
    CohereEmbeddingConfig,
    FastEmbedEmbeddingConfig,
    HuggingFaceEmbeddingConfig,
    JinaEmbeddingConfig,
    LlamaCppEmbeddingConfig,
    OllamaEmbeddingConfig,
    OpenAIEmbeddingConfig,
    SentenceTransformerEmbeddingConfig,
    VertexAIEmbeddingConfig,
    VoyageAIEmbeddingConfig,
    create_embeddings,
)
from haive.core.models.embeddings.provider_types import EmbeddingProvider

__all__ = [
    "AnyscaleEmbeddingConfig",
    # Cloud providers
    "AzureEmbeddingConfig",
    # Base class
    "BaseEmbeddingConfig",
    "BedrockEmbeddingConfig",
    "CloudflareEmbeddingConfig",
    "CohereEmbeddingConfig",
    # Enum
    "EmbeddingProvider",
    "FastEmbedEmbeddingConfig",
    # Local providers
    "HuggingFaceEmbeddingConfig",
    "JinaEmbeddingConfig",
    "LlamaCppEmbeddingConfig",
    "OllamaEmbeddingConfig",
    "OpenAIEmbeddingConfig",
    "SentenceTransformerEmbeddingConfig",
    "VertexAIEmbeddingConfig",
    "VoyageAIEmbeddingConfig",
    # Factory function
    "create_embeddings",
]
