# Haive Core Models

This module provides the core model abstractions used throughout the Haive framework for working with large language models (LLMs), embeddings, retrievers, and vector stores.

## Architecture

The models module is organized into several key submodules:

- **LLM**: Large Language Models for text generation
- **Embeddings**: Models for converting text to vector representations
- **Retrievers**: Components that search and retrieve relevant information
- **Vectorstores**: Storage systems for embedding vectors with similarity search
- **Metadata**: Utilities for working with model metadata

Each submodule follows a consistent architecture:

1. **Base Classes**: Abstract base classes defining common interfaces
2. **Provider Types**: Enumerations of supported model providers
3. **Configurations**: Pydantic models for type-safe configuration
4. **Factory Functions**: Simplified creation of model instances
5. **Implementations**: Concrete implementations for specific providers

## Key Features

### Provider Support

The framework supports a comprehensive range of providers:

- **LLM Providers**: OpenAI, Anthropic, Google, Azure, Mistral, and many more
- **Embedding Providers**: OpenAI, HuggingFace, Azure, Cohere
- **Vector Stores**: Chroma, FAISS, Pinecone, Weaviate, and others

### Model Metadata

Comprehensive metadata support for models:

- Context window sizes and token limits
- Pricing information
- Capability tracking (vision, function calling, etc.)
- Modality support (text, images, audio)

### Security Features

- Secure API key handling with environment variable fallbacks
- Credential management using SecretStr to prevent accidental exposure
- Configuration validation to ensure secure defaults

### Configuration System

- Type-safe configuration using Pydantic models
- Environment variable resolution
- Sensible defaults with clear override patterns

## Usage Examples

### Working with LLMs

```python
from haive.core.models.llm.base import OpenAILLMConfig

# Configure an OpenAI model
config = OpenAILLMConfig(
    model="gpt-4o",
    cache_enabled=True
)

# Create the LLM
llm = config.instantiate()

# Generate text
response = llm.generate("Explain quantum computing")
```

### Using Embeddings

```python
from haive.core.models.embeddings.base import create_embeddings, HuggingFaceEmbeddingConfig

# Configure embeddings
config = HuggingFaceEmbeddingConfig(
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Create embeddings
embeddings = create_embeddings(config)

# Generate embeddings
vectors = embeddings.embed_documents(["Document text"])
```

### Setting Up a Retrieval System

```python
# Create vector store with embeddings
from haive.core.models.vectorstore.base import ChromaVectorStoreConfig

vectorstore_config = ChromaVectorStoreConfig(
    persist_directory="/path/to/db",
    embedding_function=embeddings
)
vectorstore = vectorstore_config.instantiate()

# Add documents
vectorstore.add_documents(documents)

# Create retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

# Retrieve relevant documents
docs = retriever.get_relevant_documents("What is quantum computing?")
```

## Extension Points

The framework is designed to be extensible:

1. **New Providers**: Add new LLM, embedding, or vector store providers by extending base classes
2. **Custom Capabilities**: Extend capability tracking with new features
3. **Specialized Retrievers**: Create custom retrievers for specific retrieval patterns
4. **Metadata Enhancement**: Add new metadata attributes for tracking model capabilities

## Best Practices

- **API Key Management**: Store API keys in environment variables
- **Context Window Awareness**: Use metadata to avoid token limit errors
- **Caching**: Enable caching for performance improvement
- **Provider Selection**: Choose the right provider for your specific needs
- **Configuration Reuse**: Create reusable configurations for consistent behavior
- **Metadata Validation**: Validate model capabilities before using advanced features
