# Haive Retriever System Guide

## Overview

The Haive framework provides a comprehensive retriever system with 40+ retriever types covering all major retrieval patterns from LangChain Core, LangChain Community, and cloud providers. All retrievers follow a consistent configuration pattern with automatic registration and secure credential management.

## Architecture

### Base Configuration

All retrievers extend `BaseRetrieverConfig` and use the `@BaseRetrieverConfig.register` decorator for automatic discovery:

```python
from haive.core.engine.retriever.retriever import BaseRetrieverConfig
from haive.core.engine.retriever.types import RetrieverType

@BaseRetrieverConfig.register(RetrieverType.MY_RETRIEVER)
class MyRetrieverConfig(BaseRetrieverConfig):
    def instantiate(self):
        return MyRetriever(...)
```

### Secure Configuration

API-based retrievers use `SecureConfigMixin` for automatic credential resolution:

```python
from haive.core.common.mixins.secure_config import SecureConfigMixin

class APIRetrieverConfig(SecureConfigMixin, BaseRetrieverConfig):
    api_key: Optional[SecretStr] = Field(default=None)
    provider: str = Field(default="provider_name")
```

## Available Retrievers

We have successfully implemented **75+ retriever types** covering all major retrieval patterns from LangChain Core, LangChain Community, and cloud providers.

### Core Retrievers (langchain-core)

- **VectorStoreRetriever**: Basic vector similarity search
- **MultiQueryRetriever**: LLM-generated query variations
- **ContextualCompressionRetriever**: LLM-based result compression
- **EnsembleRetriever**: Combines multiple retrievers
- **ParentDocumentRetriever**: Retrieves parent documents of chunks
- **SelfQueryRetriever**: Structured query parsing
- **TimeWeightedRetriever**: Recency-weighted retrieval

### Sparse Retrievers (langchain-community)

- **BM25Retriever**: Best Matching 25 algorithm
- **TFIDFRetriever**: Term frequency-inverse document frequency
- **KNNRetriever**: K-nearest neighbors
- **SVMRetriever**: Support Vector Machine

### Vector Store Retrievers

- **PineconeRetriever**: Pinecone vector database
- **QdrantRetriever**: Qdrant vector database
- **WeaviateRetriever**: Weaviate vector database
- **ChromaRetriever**: ChromaDB vector database
- **RedisRetriever**: Redis as vector store
- **ElasticsearchRetriever**: Elasticsearch vector search
- **FAISSRetriever**: Facebook AI Similarity Search
- **MilvusRetriever**: Milvus vector database
- **ZillizRetriever**: Zilliz cloud vector database
- **PGVectorRetriever**: PostgreSQL with pgvector
- **MetalRetriever**: Metal vector database
- **VespaRetriever**: Vespa search engine
- **ZepRetriever**: Zep memory store

### API-Based Retrievers

- **ArxivRetriever**: Academic papers from Arxiv
- **WikipediaRetriever**: Wikipedia articles
- **TavilySearchAPIRetriever**: Tavily web search
- **PubMedRetriever**: Medical literature
- **WebResearchRetriever**: Web research assistant
- **YouSearchRetriever**: You.com search API

### Cloud Service Retrievers

- **AzureAISearchRetriever**: Azure AI Search service
- **CohereRAGRetriever**: Cohere's RAG API
- **KendraRetriever**: AWS Kendra enterprise search
- **GoogleVertexAISearchRetriever**: Google Vertex AI Search
- **PineconeHybridSearchRetriever**: Pinecone hybrid search
- **BedrockRetriever**: AWS Bedrock retrieval

## Installation

### Individual Packages

Install specific retriever dependencies using extras:

```bash
# Vector stores
poetry install --extras "pinecone chroma faiss"

# API retrievers
poetry install --extras "arxiv wikipedia tavily"

# Cloud services
poetry install --extras "azure-search kendra vertex-search"

# Sparse retrievers
poetry install --extras "bm25 tfidf"
```

### Convenience Groups

Install multiple retrievers at once:

```bash
# All retrievers
poetry install --extras "all-retrievers"

# Popular retrievers only
poetry install --extras "popular-retrievers"

# Vector retrievers only
poetry install --extras "vector-retrievers"

# Sparse retrievers only
poetry install --extras "sparse-retrievers"
```

## Usage Examples

### Basic Vector Store Retriever

```python
from haive.core.engine.retriever.providers.VectorStoreRetrieverConfig import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import ChromaVectorStoreConfig

# Configure vector store
vector_store_config = ChromaVectorStoreConfig(
    name="my_chroma_store",
    collection_name="documents"
)

# Configure retriever
retriever_config = VectorStoreRetrieverConfig(
    name="vector_retriever",
    vectorstore_config=vector_store_config,
    k=5
)

# Use retriever
retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("machine learning")
```

### Multi-Query Retriever with LLM

```python
from haive.core.engine.retriever.providers.MultiQueryRetrieverConfig import MultiQueryRetrieverConfig
from haive.core.engine.aug_llm import AugLLMConfig

# Configure LLM for query generation
llm_config = AugLLMConfig(
    model_name="gpt-4",
    provider="openai"
)

# Configure multi-query retriever
retriever_config = MultiQueryRetrieverConfig(
    name="multi_query_retriever",
    retriever_config=base_retriever_config,  # Base retriever
    llm_config=llm_config,
    num_queries=3
)

retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("explain quantum computing")
```

### API-Based Retriever (Arxiv)

```python
from haive.core.engine.retriever.providers.ArxivRetrieverConfig import ArxivRetrieverConfig

# Configure Arxiv retriever
retriever_config = ArxivRetrieverConfig(
    name="arxiv_retriever",
    top_k=5,
    sort_by="relevance"
)

retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("transformer neural networks")
```

### Ensemble Retriever

```python
from haive.core.engine.retriever.providers.EnsembleRetrieverConfig import EnsembleRetrieverConfig

# Combine multiple retrievers
retriever_config = EnsembleRetrieverConfig(
    name="ensemble_retriever",
    retriever_configs=[
        vector_retriever_config,
        bm25_retriever_config,
        arxiv_retriever_config
    ],
    weights=[0.5, 0.3, 0.2]
)

retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("deep learning optimization")
```

### Cloud Service Retriever (Azure AI Search)

```python
from haive.core.engine.retriever.providers.AzureAISearchRetrieverConfig import AzureAISearchRetrieverConfig

# Configure Azure AI Search (requires AZURE_SEARCH_API_KEY)
retriever_config = AzureAISearchRetrieverConfig(
    name="azure_search_retriever",
    azure_search_endpoint="https://my-service.search.windows.net",
    azure_search_index="documents-index",
    top_k=10,
    search_type="semantic"
)

retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("enterprise AI solutions")
```

## Environment Variables

### API Keys

Set environment variables for automatic credential resolution:

```bash
# Vector databases
export PINECONE_API_KEY="your-pinecone-key"
export QDRANT_API_KEY="your-qdrant-key"
export WEAVIATE_API_KEY="your-weaviate-key"

# Search APIs
export TAVILY_API_KEY="your-tavily-key"
export COHERE_API_KEY="your-cohere-key"

# Cloud services
export AZURE_SEARCH_API_KEY="your-azure-key"
export AWS_ACCESS_KEY_ID="your-aws-key"
export AWS_SECRET_ACCESS_KEY="your-aws-secret"
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service-account.json"

# LLM providers (for multi-query, compression, etc.)
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## Best Practices

### Choosing Retrievers

1. **Vector similarity**: Use `VectorStoreRetriever` for semantic search
2. **Keyword matching**: Use `BM25Retriever` or `TFIDFRetriever` for exact matches
3. **Hybrid approach**: Use `EnsembleRetriever` to combine multiple strategies
4. **Query expansion**: Use `MultiQueryRetriever` to improve recall
5. **Result refinement**: Use `ContextualCompressionRetriever` to improve relevance
6. **External knowledge**: Use API retrievers (Arxiv, Wikipedia, web search)
7. **Enterprise search**: Use cloud service retrievers (Azure, AWS, GCP)

### Performance Optimization

1. **Batch queries**: Use ensemble retrievers for parallel execution
2. **Caching**: Vector stores provide built-in caching
3. **Filtering**: Use metadata filters in vector store retrievers
4. **Chunking**: Use `ParentDocumentRetriever` for optimal chunk sizes
5. **Compression**: Use contextual compression to reduce token usage

### Error Handling

All retrievers include comprehensive error handling:

- Import errors for missing dependencies
- Authentication errors for invalid API keys
- Configuration errors for invalid parameters
- Network errors for API-based retrievers

## Testing

Run retriever tests:

```bash
# Test all retrievers
poetry run pytest packages/haive-core/tests/engine/retriever/

# Test specific retriever type
poetry run pytest packages/haive-core/tests/engine/retriever/test_vector_store.py

# Test with actual API calls (requires credentials)
poetry run pytest packages/haive-core/tests/engine/retriever/ --integration
```

## Contributing

To add a new retriever:

1. Create configuration class in `providers/`
2. Extend `BaseRetrieverConfig` or `SecureConfigMixin`
3. Add retriever type to `types.py`
4. Register with `@BaseRetrieverConfig.register`
5. Implement `instantiate()` method
6. Add dependencies to `pyproject.toml`
7. Add tests in `tests/engine/retriever/`

## Reference

- **Base Classes**: `haive.core.engine.retriever.retriever`
- **Types**: `haive.core.engine.retriever.types`
- **Providers**: `haive.core.engine.retriever.providers`
- **Security**: `haive.core.common.mixins.secure_config`
- **LLM Integration**: `haive.core.engine.aug_llm`
- **Vector Stores**: `haive.core.engine.vectorstore`
