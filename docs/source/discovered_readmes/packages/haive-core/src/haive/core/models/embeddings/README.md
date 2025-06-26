# Haive Embeddings Module

This module provides a comprehensive framework for working with text embedding models from various providers. Embeddings are vector representations of text that capture semantic meaning, enabling similarity search, clustering, and other NLP applications.

## Core Components

- **Base Classes**: Abstract base classes and interfaces for embedding models
- **Provider Support**: Implementations for various embedding providers (Azure, HuggingFace, etc.)
- **Configuration System**: Pydantic models for type-safe configuration
- **Security Features**: Secure handling of API keys and credentials
- **Caching System**: Efficient caching of embeddings for performance optimization

## Supported Providers

### Cloud Providers

- **Azure OpenAI**: Microsoft's hosted OpenAI embedding models
- **OpenAI**: Direct OpenAI embedding models
- **Cohere**: Specialized embedding models from Cohere
- **Jina AI**: Jina AI embedding models
- **Google Vertex AI**: Google Cloud's machine learning platform
- **AWS Bedrock**: Amazon's foundation model service
- **Cloudflare Workers AI**: Cloudflare's AI model hosting
- **Voyage AI**: Specialized embedding models from Voyage AI
- **Anyscale**: Anyscale embedding models

### Local/Self-hosted Providers

- **HuggingFace**: Open-source embedding models from the HuggingFace model hub
- **SentenceTransformers**: Efficient sentence embedding models
- **FastEmbed**: Lightweight embedding models optimized for CPU
- **Ollama**: Local embedding models via Ollama
- **LlamaCpp**: Local embedding models via llama.cpp

## Usage Examples

### Creating Embeddings with HuggingFace

```python
from haive.core.models.embeddings.base import create_embeddings, HuggingFaceEmbeddingConfig

# Configure the embedding model
config = HuggingFaceEmbeddingConfig(
    model="sentence-transformers/all-MiniLM-L6-v2",
    cache_folder="/path/to/cache",
    use_cache=True
)

# Create the embeddings model
embeddings = create_embeddings(config)

# Generate embeddings for texts
doc_vectors = embeddings.embed_documents(
    ["This is a sample document", "Another document to embed"]
)

# Generate embeddings for a query
query_vector = embeddings.embed_query("What is this document about?")
```

### Using Azure OpenAI Embeddings

```python
from haive.core.models.embeddings.base import create_embeddings, AzureEmbeddingConfig

config = AzureEmbeddingConfig(
    model="text-embedding-ada-002",
    api_version="2024-02-15-preview",
    api_base="https://your-resource.openai.azure.com/"
)

embeddings = create_embeddings(config)
vectors = embeddings.embed_documents(["Text to embed"])
```

## Performance Considerations

- HuggingFace models will use GPU acceleration if available (CUDA)
- Caching is enabled by default to avoid redundant computations
- GPU memory is cleaned up if initialization fails on the first attempt
- For large documents, consider chunking before embedding

## Extending with New Providers

To add a new embedding provider:

1. Add the provider to the `EmbeddingProvider` enum in `provider_types.py`
2. Create a new configuration class extending `BaseEmbeddingConfig`
3. Implement the `instantiate()` method to return the appropriate model instance

Example:

```python
class NewProviderEmbeddingConfig(BaseEmbeddingConfig):
    provider: EmbeddingProvider = EmbeddingProvider.NEW_PROVIDER
    model: str = Field(default="default-model")

    def instantiate(self, **kwargs) -> Any:
        # Instantiate and return the embedding model
        return NewProviderEmbeddings(
            model=self.model,
            **kwargs
        )
```

## Security

API keys are handled securely via:

- Environment variable resolution with fallbacks
- SecretStr type for preventing accidental exposure
- Support for custom credential providers
