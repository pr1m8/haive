"""Embedding Provider Types Module.

This module defines the supported embedding model providers as an enumeration,
ensuring consistent identification and type safety when configuring embedding models.

These provider types are used throughout the Haive embedding framework to identify
the source of embedding models and apply appropriate configuration patterns.

Typical usage example:
    ```python
    from haive.core.models.embeddings.provider_types import EmbeddingProvider

    # Check if a provider is supported
    if provider == EmbeddingProvider.HUGGINGFACE:
        # Use HuggingFace-specific configuration
        pass
    ```
"""

from enum import Enum


class EmbeddingProvider(str, Enum):
    """Enumeration of supported embedding model providers.

    This enum inherits from str to allow string comparison and serialization
    while maintaining type safety and providing autocompletion support.

    Attributes:
        AZURE: Microsoft Azure OpenAI embedding models
        HUGGINGFACE: HuggingFace model hub embedding models
        OPENAI: OpenAI embedding models
        COHERE: Cohere embedding models
        OLLAMA: Ollama local embedding models
        SENTENCE_TRANSFORMERS: Sentence Transformers embedding models
        FASTEMBED: FastEmbed lightweight embedding models
        JINA: Jina AI embedding models
        VERTEXAI: Google Vertex AI embedding models
        BEDROCK: AWS Bedrock embedding models
        CLOUDFLARE: Cloudflare Workers AI embedding models
        LLAMACPP: LlamaCPP local embedding models
        VOYAGEAI: Voyage AI embedding models
        ANYSCALE: Anyscale embedding models
        NOVITA: NovitaAI embedding models
    """

    AZURE = "azure"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    COHERE = "cohere"
    OLLAMA = "ollama"
    SENTENCE_TRANSFORMERS = "sentence_transformers"
    FASTEMBED = "fastembed"
    JINA = "jina"
    VERTEXAI = "vertexai"
    BEDROCK = "bedrock"
    CLOUDFLARE = "cloudflare"
    LLAMACPP = "llamacpp"
    VOYAGEAI = "voyageai"
    ANYSCALE = "anyscale"
    NOVITA = "novita"
