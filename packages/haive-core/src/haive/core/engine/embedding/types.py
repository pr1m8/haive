"""Embedding engine types and enumerations."""

from enum import Enum


class EmbeddingType(str, Enum):
    """Enumeration of supported embedding providers."""

    # Major Commercial Providers
    OPENAI = "OpenAI"
    AZURE_OPENAI = "AzureOpenAI"
    COHERE = "Cohere"
    MISTRAL = "MistralAI"
    ANTHROPIC = "Anthropic"
    VOYAGE_AI = "VoyageAI"
    TOGETHER_AI = "TogetherAI"
    FIREWORKS = "Fireworks"

    # Google Providers
    GOOGLE_VERTEX_AI = "GoogleVertexAI"
    GOOGLE_GEMINI = "GoogleGemini"

    # Cloud Providers
    AWS_BEDROCK = "AWSBedrock"
    IBM_WATSONX = "IBMWatsonx"
    NVIDIA = "NVIDIA"

    # Open Source/Local Providers
    HUGGINGFACE = "HuggingFace"
    SENTENCE_TRANSFORMERS = "SentenceTransformers"
    OLLAMA = "Ollama"
    NOMIC = "Nomic"

    # Specialized Providers
    ELASTICSEARCH = "Elasticsearch"
    WEAVIATE = "Weaviate"
    PINECONE = "Pinecone"

    # Testing/Development
    FAKE = "Fake"

    # Legacy/Deprecated (for backward compatibility)
    AZURE = "Azure"  # Alias for AzureOpenAI
