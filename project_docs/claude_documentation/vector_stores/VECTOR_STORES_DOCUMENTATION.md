# Haive Vector Store Documentation

## Overview

The Haive framework provides a comprehensive set of vector store implementations through a unified configuration interface. We currently support **27 different vector stores** across various categories.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Supported Vector Stores](#supported-vector-stores)
3. [Configuration Patterns](#configuration-patterns)
4. [Usage Examples](#usage-examples)
5. [Implementation Details](#implementation-details)

## Quick Start

### Basic Usage

```python
from haive.core.engine.vectorstore import ChromaVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Create vector store configuration
config = ChromaVectorStoreConfig(
    name="my_chroma_store",
    embedding=OpenAIEmbeddingConfig(),
    persist_directory="./chroma_db"
)

# Instantiate the vector store
vectorstore = config.instantiate()

# Use with documents
from langchain_core.documents import Document
docs = [Document(page_content="Example content")]
vectorstore.add_documents(docs)
```

## Supported Vector Stores

### Core Open Source (5)

- **Chroma** - Simple, feature-rich vector database
- **FAISS** - Facebook's efficient similarity search library
- **Milvus** - Scalable cloud-native vector database
- **Qdrant** - High-performance vector search engine (API key optional)
- **Weaviate** - GraphQL-based vector database (API key optional)

### Cloud/Managed Services (6)

- **AzureSearch** - Microsoft Azure Cognitive Search (API key required)
- **Marqo** - Multimodal tensor search with built-in models
- **MongoDBAtlas** - MongoDB's cloud vector search
- **Pinecone** - Popular managed vector database (API key required)
- **Vectara** - Managed platform with NLP capabilities (API key required)
- **Zilliz** - Managed Milvus cloud service (API key required)

### Database Extensions (4)

- **PGVector** - PostgreSQL with vector extensions
- **Supabase** - PostgreSQL-based with vector support (API key required)
- **ClickHouse** - Columnar database with vector search
- **Cassandra** - Distributed NoSQL with vector capabilities

### Search Engines (4)

- **Elasticsearch** - Popular search engine with vector support
- **Typesense** - Fast, typo-tolerant search engine (API key required)
- **OpenSearch** - Open-source Elasticsearch fork
- **AmazonOpenSearch** - AWS managed OpenSearch service

### In-Memory/Cache (2)

- **Redis** - In-memory data store with vector search
- **InMemory** - Simple in-memory vector store for testing

### Specialized Stores (5)

- **Annoy** - Approximate nearest neighbors library
- **DocArray** - Document-oriented vector store
- **LanceDB** - Serverless vector database (API key optional)
- **SKLearn** - Scikit-learn based vector store
- **USearch** - High-performance similarity search

### Graph Databases (1)

- **Neo4j** - Graph database with vector support (password required)

## Configuration Patterns

### 1. Basic Configuration

Most vector stores follow this pattern:

```python
from haive.core.engine.vectorstore import <Store>VectorStoreConfig
from haive.core.models.embeddings.base import <Embedding>Config

config = <Store>VectorStoreConfig(
    name="my_store",
    embedding=<Embedding>Config(),
    # Store-specific parameters
)
```

### 2. Stores with API Keys (SecureConfigMixin)

These stores use `SecureConfigMixin` for secure API key handling:

```python
# API key can be provided directly
config = PineconeVectorStoreConfig(
    name="my_pinecone",
    embedding=OpenAIEmbeddingConfig(),
    api_key="your-api-key",  # Or use environment variable
    index_name="my-index"
)

# Or via environment variable (automatically resolved)
# Set: PINECONE_API_KEY=your-api-key
config = PineconeVectorStoreConfig(
    name="my_pinecone",
    embedding=OpenAIEmbeddingConfig(),
    index_name="my-index"
)
```

Stores with SecureConfigMixin:

- AzureSearch (AZURE_SEARCH_API_KEY)
- LanceDB (LANCEDB_API_KEY)
- Pinecone (PINECONE_API_KEY)
- Qdrant (QDRANT_API_KEY)
- Supabase (SUPABASE_API_KEY)
- Typesense (TYPESENSE_API_KEY)
- Vectara (VECTARA_API_KEY)
- Weaviate (WEAVIATE_API_KEY)
- Zilliz (ZILLIZ_API_KEY)

### 3. Stores with Built-in Embeddings

Some stores manage their own embeddings:

```python
# Vectara - manages embeddings internally
config = VectaraVectorStoreConfig(
    name="my_vectara",
    vectara_customer_id="123456",
    vectara_corpus_id="1",
    api_key="your-api-key"
    # No embedding config needed!
)

# Marqo - uses built-in models
config = MarqoVectorStoreConfig(
    name="my_marqo",
    marqo_url="http://localhost:8882",
    index_name="documents",
    model="hf/all_datasets_v4_MiniLM-L6"  # Built-in model
)
```

## Usage Examples

### Example 1: Local Development with Chroma

```python
from haive.core.engine.vectorstore import ChromaVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
from langchain_core.documents import Document

# Configure Chroma for local persistence
config = ChromaVectorStoreConfig(
    name="local_chroma",
    embedding=OpenAIEmbeddingConfig(),
    persist_directory="./data/chroma_db",
    collection_name="my_documents"
)

# Create vector store
vectorstore = config.instantiate()

# Add documents
docs = [
    Document(page_content="Haive is an AI agent framework", metadata={"type": "intro"}),
    Document(page_content="It supports 27 vector stores", metadata={"type": "feature"})
]
vectorstore.add_documents(docs)

# Search
results = vectorstore.similarity_search("How many vector stores?", k=1)
print(results[0].page_content)
```

### Example 2: Production with Pinecone

```python
from haive.core.engine.vectorstore import PineconeVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure Pinecone (API key from environment)
config = PineconeVectorStoreConfig(
    name="production_pinecone",
    embedding=OpenAIEmbeddingConfig(model="text-embedding-3-small"),
    index_name="production-index",
    namespace="documents"
)

# Create and use
vectorstore = config.instantiate()

# Upsert documents with IDs
vectorstore.add_documents(
    documents=docs,
    ids=["doc1", "doc2"]
)
```

### Example 3: Multimodal Search with Marqo

```python
from haive.core.engine.vectorstore import MarqoVectorStoreConfig
import marqo

# Configure for multimodal search
config = MarqoVectorStoreConfig(
    name="multimodal_search",
    marqo_url="http://localhost:8882",
    index_name="multimodal_docs",
    model="open_clip/ViT-B-32/openai",
    treat_urls_and_pointers_as_images=True
)

# Create Marqo client
client = marqo.Client(url=config.marqo_url)

# Instantiate with client
vectorstore = config.instantiate(client=client)

# Add documents with image URLs
docs = [
    Document(
        page_content="A beautiful sunset",
        metadata={"image_url": "https://example.com/sunset.jpg"}
    )
]
vectorstore.add_documents(docs)
```

### Example 4: Analytics with ClickHouse

```python
from haive.core.engine.vectorstore import ClickHouseVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure ClickHouse for analytics + vectors
config = ClickHouseVectorStoreConfig(
    name="analytics_vectors",
    embedding=OpenAIEmbeddingConfig(),
    host="clickhouse.example.com",
    port=8443,
    username="admin",
    password="password",
    secure=True,
    database="analytics",
    table="document_vectors",
    metric="cosine"
)

vectorstore = config.instantiate()
```

### Example 5: Hybrid Search with OpenSearch

```python
from haive.core.engine.vectorstore import OpenSearchVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure OpenSearch for hybrid search
config = OpenSearchVectorStoreConfig(
    name="hybrid_search",
    embedding=OpenAIEmbeddingConfig(),
    opensearch_url="http://localhost:9200",
    index_name="documents",
    engine="nmslib",
    space_type="cosine"
)

vectorstore = config.instantiate()

# Hybrid search combines keyword and vector search
results = vectorstore.similarity_search(
    "machine learning frameworks",
    k=5,
    filter={"category": "technology"}
)
```

## Implementation Details

### Base Configuration

All vector stores extend `BaseVectorStoreConfig` which provides:

- Automatic registration via decorator
- Standard interface (`instantiate()`, `get_input_fields()`, `get_output_fields()`)
- Embedding validation
- LangGraph compatibility

### Registration Pattern

```python
@BaseVectorStoreConfig.register(VectorStoreType.STORE_NAME)
class StoreNameVectorStoreConfig(BaseVectorStoreConfig):
    # Implementation
```

### SecureConfigMixin

For stores requiring API keys:

```python
class MyVectorStoreConfig(BaseVectorStoreConfig, SecureConfigMixin):
    api_key: str = Field(..., description="API key")
    # Field MUST be named "api_key" for SecureConfigMixin
```

### Custom Embedding Validation

Some stores don't need external embeddings:

```python
def validate_embedding(self):
    """Override for stores with built-in embeddings."""
    pass  # No validation needed
```

## Environment Variables

Many vector stores support environment variables for configuration:

```bash
# API Keys
export PINECONE_API_KEY=your-key
export WEAVIATE_API_KEY=your-key
export AZURE_SEARCH_API_KEY=your-key
export VECTARA_API_KEY=your-key
export OPENAI_API_KEY=your-key

# Connection strings
export POSTGRES_CONNECTION_STRING=postgresql://...
export REDIS_URL=redis://localhost:6379

# Cloud credentials
export AWS_ACCESS_KEY_ID=your-key
export AWS_SECRET_ACCESS_KEY=your-secret
```

## Best Practices

1. **Choose the Right Store**
   - Development: Chroma, FAISS, InMemory
   - Production: Pinecone, Weaviate, Qdrant
   - Multimodal: Marqo, Weaviate
   - Analytics: ClickHouse, Elasticsearch
   - Existing Infrastructure: PGVector, MongoDB Atlas

2. **Configuration Management**
   - Use environment variables for sensitive data
   - Store configurations in separate config files
   - Use different stores for dev/staging/production

3. **Performance Optimization**
   - Choose appropriate embedding models
   - Configure index parameters for your use case
   - Use batch operations for large datasets
   - Consider hybrid search for better results

4. **Error Handling**
   - Always handle import errors gracefully
   - Validate configurations before instantiation
   - Implement retry logic for cloud services

## Troubleshooting

### Common Issues

1. **Import Errors**

   ```python
   # Install required packages
   pip install chromadb  # For Chroma
   pip install faiss-cpu  # For FAISS
   pip install qdrant-client  # For Qdrant
   ```

2. **API Key Issues**
   - Check environment variable names
   - Ensure keys are properly formatted
   - Verify API key permissions

3. **Connection Issues**
   - Verify URLs and ports
   - Check firewall rules
   - Ensure services are running

## Summary

The Haive framework provides a unified interface for 27 different vector stores, making it easy to:

- Switch between vector stores without changing application code
- Use the best vector store for your specific use case
- Leverage advanced features like multimodal search and hybrid queries
- Scale from development to production seamlessly

All implementations follow consistent patterns and best practices, ensuring reliability and maintainability across your AI applications.
