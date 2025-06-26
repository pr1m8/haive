# Haive VectorStore Engine - Core Concepts

## Overview

The VectorStore engine is a specialized component within the Haive framework that provides a comprehensive interface for working with vector databases and similarity search. Built on the Engine base class, it offers a consistent way to create, manage, and interact with different vector store implementations while abstracting away the underlying complexity.

## Key Concepts

### The VectorStore Engine

The `VectorStoreConfig` class extends `InvokableEngine` to provide a unified interface for vector stores. This configuration-based approach enables:

**Core Features**:

- **Provider Abstraction**: Support for multiple vector database backends (FAISS, Chroma, Pinecone, etc.)
- **Embedding Integration**: Seamless integration with embedding models
- **Document Management**: Methods for adding and retrieving documents
- **Search Configuration**: Flexible search parameters and filtering
- **Retriever Creation**: Direct creation of retrievers from vector stores

### VectorStore Providers

The system supports multiple vector store backends through the `VectorStoreProvider` enum:

| Provider      | Description                        | Notes                                       |
| ------------- | ---------------------------------- | ------------------------------------------- |
| CHROMA        | Chroma vector database             | Open source, embedding database             |
| FAISS         | Facebook AI Similarity Search      | Fast, efficient similarity search           |
| PINECONE      | Pinecone managed vector database   | Cloud-hosted, serverless                    |
| WEAVIATE      | Weaviate vector database           | Vector search engine with GraphQL API       |
| ZILLIZ        | Zilliz cloud vector database       | Managed service                             |
| MILVUS        | Milvus vector database             | Open-source vector database                 |
| QDRANT        | Qdrant vector database             | Vector similarity search engine             |
| IN_MEMORY     | In-memory vector store             | For testing/development                     |
| PGVECTOR      | PostgreSQL with pgvector extension | Adds vector similarity search to PostgreSQL |
| ELASTICSEARCH | Elasticsearch vector search        | Full-text search with vector capabilities   |
| REDIS         | Redis vector database              | In-memory data structure store              |
| SUPABASE      | Supabase vector store              | PostgreSQL-based, with pgvector             |
| MONGODB_ATLAS | MongoDB Atlas vector search        | Document database with vector search        |
| AZURE_SEARCH  | Azure Cognitive Search             | Cloud search service with vector support    |
| OPENSEARCH    | OpenSearch vector search           | Search and analytics suite                  |
| CASSANDRA     | Apache Cassandra vector store      | Wide-column store with vector support       |
| CLICKHOUSE    | ClickHouse vector database         | Column-oriented DBMS                        |
| TYPESENSE     | Typesense vector search            | Fast, typo-tolerant search engine           |
| LANCEDB       | LanceDB vector database            | Embedded vector database                    |
| NEO4J         | Neo4j vector search                | Graph database with vector capabilities     |

### Search Capabilities

The VectorStore engine provides multiple search mechanisms:

- **Similarity Search**: Find documents most similar to a query
- **MMR Search**: Maximum Marginal Relevance for diversity in results
- **Filtered Search**: Apply metadata filters to search results
- **Threshold Filtering**: Filter by similarity score threshold

### Integration with Retrievers

VectorStores can be directly converted to Retrievers for use in LangChain/LangGraph pipelines:

- **As Retriever**: Convert any vector store to a retriever
- **Search Configuration**: Configure search behavior
- **Consistent Interface**: Standardized retrieval interface

## Implementation Patterns

### Creating a VectorStore

```python
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document

# Create documents
documents = [
    Document(page_content="The capital of France is Paris."),
    Document(page_content="London is the capital of the United Kingdom."),
    Document(page_content="Berlin is the capital of Germany.")
]

# Create vector store configuration
vs_config = VectorStoreConfig(
    name="capital_facts",
    documents=documents,
    vector_store_provider=VectorStoreProvider.FAISS,
    embedding_model=HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    ),
    k=3  # Default number of results to return
)

# Create the actual vector store
vectorstore = vs_config.create_vectorstore()
```

### Adding Documents

```python
# Create an empty vector store
vs_config = VectorStoreConfig(
    name="growing_knowledge_base",
    vector_store_provider=VectorStoreProvider.IN_MEMORY,
    embedding_model=HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

# Add a single document
vs_config.add_document(Document(
    page_content="Machine learning is a subset of artificial intelligence."
))

# Add multiple documents
vs_config.add_documents([
    Document(page_content="Neural networks are inspired by biological neurons."),
    Document(page_content="Deep learning uses multiple layers of neural networks.")
])

# Create the vector store with the added documents
vectorstore = vs_config.create_vectorstore()
```

### Performing Searches

```python
# Basic similarity search
results = vs_config.similarity_search(
    query="What is the capital of France?",
    k=2  # Override the default k value
)

# With filter
results = vs_config.similarity_search(
    query="What is the capital of France?",
    filter={"source": "geography_facts"}
)

# Using MMR for diversity
results = vs_config.similarity_search(
    query="Tell me about European capitals",
    search_type="mmr"
)

# With score threshold
results = vs_config.similarity_search(
    query="Paris landmarks",
    score_threshold=0.8  # Only return documents with a score above this threshold
)
```

### Using the Invoke Method

```python
# Simple string query (shorthand)
results = vs_config.invoke("What is the capital of France?")

# Dictionary with search parameters
results = vs_config.invoke({
    "query": "What is the capital of France?",
    "k": 5,
    "filter": {"continent": "Europe"},
    "search_type": "mmr"
})

# With runtime configuration
runtime_config = {
    "configurable": {
        "k": 10,
        "score_threshold": 0.75
    }
}
results = vs_config.invoke("European capitals", runtime_config)
```

### Creating Retrievers

```python
# Create a basic retriever
retriever = vs_config.create_retriever()

# Create a retriever with custom search parameters
retriever = vs_config.create_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "score_threshold": 0.7,
        "fetch_k": 20  # Fetch more documents initially for MMR
    }
)

# Use the retriever
docs = retriever.get_relevant_documents("What is the capital of Germany?")
```

### Convenience Functions

```python
from haive.core.engine.vectorstore import (
    create_vs_from_documents,
    create_retriever_from_documents
)

# Create vector store directly from documents
documents = [Document(page_content="Example document")]
vectorstore = create_vs_from_documents(
    documents=documents,
    vector_store_provider=VectorStoreProvider.FAISS
)

# Create retriever directly from documents
retriever = create_retriever_from_documents(
    documents=documents,
    search_type="similarity",
    k=5
)
```

## Adding Custom Providers

Custom vector store providers can be added at runtime using the `VectorStoreProviderRegistry`:

```python
from haive.core.engine.vectorstore import VectorStoreProviderRegistry
from langchain_community.vectorstores.custom import CustomVectorStore

# Direct registration
VectorStoreProviderRegistry.register_provider("CustomStore", CustomVectorStore)

# Using a factory function for lazy loading
def get_special_vectorstore():
    from special_package import SpecialVectorStore
    return SpecialVectorStore

VectorStoreProviderRegistry.register_provider_factory("SpecialStore", get_special_vectorstore)
```

## Advanced Usage Patterns

### Custom Embedding Models

```python
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Use OpenAI embeddings with the vector store
vs_config = VectorStoreConfig(
    name="openai_vectorstore",
    embedding_model=OpenAIEmbeddingConfig(
        model="text-embedding-3-small"
    ),
    vector_store_provider=VectorStoreProvider.QDRANT
)
```

### Using in Graphs

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.engine.aug_llm import AugLLMConfig
from langgraph.graph import START, END

# Create engines
vs_config = VectorStoreConfig(
    name="knowledge_base",
    documents=documents,
    vector_store_provider=VectorStoreProvider.FAISS
)
llm_config = AugLLMConfig(name="llm_engine")

# Create graph
graph = DynamicGraph(
    name="rag_workflow",
    components=[vs_config, llm_config]
)

# Add nodes (retrieve and generate)
graph.add_node("retrieve", vs_config)
graph.add_node("generate", llm_config, command_goto=END)

# Add edges
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")

# Compile
app = graph.compile()
```

### Runtime Configuration Override

```python
from haive.core.config.runnable import RunnableConfigManager

# Create base configuration
config = RunnableConfigManager.create(thread_id="conversation-123")

# Add vector store specific configuration
config = RunnableConfigManager.add_engine_config(
    config,
    vs_config.id,  # Target by ID for most specific override
    k=10,
    score_threshold=0.8,
    search_type="mmr"
)

# Use with the configuration
results = vs_config.invoke("Capital cities", config)
```

### Asynchronous Vector Stores

```python
# Create vector store in async mode
async_vectorstore = vs_config.create_vectorstore(async_mode=True)

# Use ainvoke for asynchronous operation
import asyncio

async def search_documents():
    results = await vs_config.ainvoke("Capital cities")
    return results

results = asyncio.run(search_documents())
```

## Best Practices

### 1. Use Appropriate Embedding Models

Select embedding models that match your domain and requirements:

```python
# Domain-specific embedding for medical text
vs_config = VectorStoreConfig(
    name="medical_knowledge",
    embedding_model=HuggingFaceEmbeddingConfig(
        model="pritamdeka/BioBERT-large-cased-v1.1-mnli"
    )
)
```

### 2. Set Appropriate Defaults

Configure appropriate defaults based on your use case:

```python
# Configuring for FAQ retrieval with higher precision
vs_config = VectorStoreConfig(
    name="faq_database",
    k=3,  # Return fewer, more relevant results
    score_threshold=0.75,  # Higher threshold for better precision
    search_type="similarity"  # Use basic similarity search
)
```

### 3. Manage Document Lifecycle

Implement proper document management:

```python
# Store documents with metadata for better filtering
vs_config.add_documents([
    Document(
        page_content="Paris is known for the Eiffel Tower.",
        metadata={"city": "Paris", "country": "France", "topic": "landmarks"}
    ),
    Document(
        page_content="The Louvre Museum houses the Mona Lisa.",
        metadata={"city": "Paris", "country": "France", "topic": "museums"}
    )
])

# Use metadata for filtering
results = vs_config.similarity_search(
    "What can I see in Paris?",
    filter={"topic": "landmarks"}
)
```

### 4. Use Appropriate Search Types

Choose the right search type for your use case:

```python
# Use similarity search for factual retrieval
factual_results = vs_config.similarity_search(
    "What is the capital of France?",
    search_type="similarity"
)

# Use MMR for exploratory queries
diverse_results = vs_config.similarity_search(
    "Tell me about European cities",
    search_type="mmr",
    search_kwargs={"fetch_k": 20, "k": 5, "lambda_mult": 0.5}
)
```

### 5. Leverage Runtime Configuration

Use runtime configuration for dynamic search behavior:

```python
# Create configurations for different search profiles
detailed_config = {
    "configurable": {
        "k": 10,
        "score_threshold": 0.5
    }
}

precise_config = {
    "configurable": {
        "k": 3,
        "score_threshold": 0.8
    }
}

# Use based on query context
if is_exploratory_query(query):
    results = vs_config.invoke(query, detailed_config)
else:
    results = vs_config.invoke(query, precise_config)
```

## Testing

The vector store system includes comprehensive tests to ensure proper functionality:

```bash
python -m unittest packages/haive-core/src/haive/core/engine/vectorstore/test_vectorstore_providers.py
```

## Conclusion

The VectorStore engine in Haive provides a powerful abstraction for working with vector databases and similarity search. Its flexible configuration, provider support, and integration capabilities enable sophisticated retrieval applications with minimal boilerplate. By following the best practices and leveraging the patterns outlined in this document, you can efficiently incorporate vector search into your AI workflows.
