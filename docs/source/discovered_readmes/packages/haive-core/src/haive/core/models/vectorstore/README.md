# Haive VectorStore Module

This module provides abstractions and implementations for vector stores, which are specialized databases for storing and searching vector embeddings. Vector stores enable semantic search and retrieval based on embedding similarity.

## Core Components

- **Base Classes**: Abstract base classes and interfaces for vector stores
- **Provider Implementations**: Concrete implementations for various vector store providers
- **Configuration System**: Type-safe configurations using Pydantic models
- **Integration**: Seamless integration with embeddings and retrievers

## Supported Vector Stores

The module supports various vector store implementations:

- **Chroma**: Open-source embedding database
- **FAISS**: Facebook AI Similarity Search
- **Pinecone**: Managed vector database service
- **Weaviate**: Vector search engine
- **Milvus**: Open-source vector database
- **Qdrant**: Vector database focused on extended filtering
- **Elasticsearch**: Full-text search with vector capabilities
- **And more**: Redis, Postgres with pgvector, Neo4j, etc.

## Usage Examples

### Creating and Using a Chroma Vector Store

```python
from haive.core.models.vectorstore.base import ChromaVectorStoreConfig
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig, create_embeddings

# Create embeddings
embedding_config = HuggingFaceEmbeddingConfig(
    model="sentence-transformers/all-MiniLM-L6-v2"
)
embeddings = create_embeddings(embedding_config)

# Configure vector store
config = ChromaVectorStoreConfig(
    persist_directory="/path/to/chroma",
    collection_name="my_documents",
    embedding_function=embeddings
)

# Create vector store
vectorstore = config.instantiate()

# Add documents
from langchain.schema import Document
documents = [
    Document(page_content="Content of document 1", metadata={"source": "doc1.txt"}),
    Document(page_content="Content of document 2", metadata={"source": "doc2.txt"})
]
vectorstore.add_documents(documents)

# Search
results = vectorstore.similarity_search("query text", k=3)
```

### Converting to a Retriever

```python
from haive.core.models.vectorstore.base import create_vectorstore

# Create vector store from configuration
vectorstore = create_vectorstore(config)

# Convert to retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Retrieve documents
docs = retriever.get_relevant_documents("What is quantum computing?")
```

## Search Types

Most vector stores support multiple search types:

- **Similarity Search**: Find documents closest to the query embedding
- **MMR (Maximum Marginal Relevance)**: Balance relevance and diversity
- **Similarity Score Search**: Similar to similarity search but with scores
- **Hybrid Search**: Combine vector and keyword search (in supported stores)

## Performance Considerations

- Choose the right vector store for your dataset size and query patterns
- Consider persistence requirements and update frequency
- For large collections, use appropriate indexing methods
- Configure embedding dimensions appropriate for your model

## Extending with New Vector Stores

To add a new vector store provider:

1. Create a new configuration class extending `BaseVectorStoreConfig`
2. Implement the `instantiate()` method to return the appropriate vector store instance

Example:

```python
class NewVectorStoreConfig(BaseVectorStoreConfig):
    """Configuration for a new vector store provider."""

    connection_string: str = Field(..., description="Connection string")
    collection: str = Field(..., description="Collection name")

    def instantiate(self, **kwargs) -> Any:
        from some_package import NewVectorStore

        return NewVectorStore(
            connection_string=self.connection_string,
            collection=self.collection,
            embedding_function=self.embedding_function,
            **kwargs
        )
```

## Additional Features

- **Metadata Filtering**: Query with metadata constraints
- **Document Deletion**: Remove documents from the store
- **Collection Management**: Create, list, and delete collections
- **Persistence**: Save and load vector stores
- **Batch Operations**: Efficient batch addition and querying
