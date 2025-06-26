# Haive Retriever Module

This module provides implementations and abstractions for retrievers, which are components that fetch relevant information from various sources. Retrievers are essential for Retrieval-Augmented Generation (RAG) and other information retrieval tasks.

## Core Components

- **Base Classes**: Abstract base classes and interfaces for retrievers
- **Vector Retrievers**: Implementations for similarity-based document retrieval
- **Specialized Retrievers**: Enhanced retrievers with specific capabilities
- **Community Retrievers**: Community-contributed retriever implementations

## Retriever Types

The module includes various retriever implementations:

- **VectorStore Retriever**: Retrieves documents based on vector similarity
- **Ensemble Retriever**: Combines results from multiple retrievers
- **MultiQuery Retriever**: Generates and uses multiple queries for better recall
- **Parent Document Retriever**: Retrieves parent documents along with chunks
- **Self Query Retriever**: Allows filtering based on document metadata
- **Time Weighted Retriever**: Weights results based on recency
- **AskNews Retriever**: Specialized retriever for news content

## Usage Examples

### Basic Vector Retriever

```python
from haive.core.models.retriever.vectorstore_retriever import VectorStoreRetriever
from haive.core.models.vectorstore.base import create_vectorstore

# Create a vector store
vectorstore = create_vectorstore(config)

# Create a retriever
retriever = VectorStoreRetriever(
    vectorstore=vectorstore,
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Retrieve documents
docs = retriever.get_relevant_documents("What is quantum computing?")
```

### Ensemble Retriever

```python
from haive.core.models.retriever.retrievers.ensemble import EnsembleRetriever

# Create an ensemble of retrievers
ensemble = EnsembleRetriever(
    retrievers=[retriever1, retriever2, retriever3],
    weights=[0.5, 0.3, 0.2]
)

# Retrieve documents from all retrievers
docs = ensemble.get_relevant_documents("What is quantum computing?")
```

### MultiQuery Retriever

```python
from haive.core.models.retriever.retrievers.multiqery import MultiQueryRetriever

# Create a multi-query retriever
multi_query = MultiQueryRetriever(
    retriever=base_retriever,
    llm_chain=llm_chain,  # For generating alternative queries
    num_queries=3
)

# Retrieve with multiple queries
docs = multi_query.get_relevant_documents("What is quantum computing?")
```

## Performance Considerations

- Choose the right retriever for your use case
- Configure appropriate search parameters (k, score threshold)
- For large document collections, consider using filters when available
- Ensemble retrievers can improve recall but increase latency

## Extending the Retriever System

To create a custom retriever:

1. Extend the `BaseRetriever` class
2. Implement the `_get_relevant_documents` method
3. Optionally implement `get_relevant_documents` if you need custom behavior

Example:

```python
from haive.core.models.retriever.base import BaseRetriever
from typing import List

class CustomRetriever(BaseRetriever):
    """Custom retriever implementation."""

    def _get_relevant_documents(self, query: str) -> List[Document]:
        # Implement your custom retrieval logic
        # ...
        return documents
```

## Integration with Vector Stores

Retrievers typically work with vector stores for similarity search. The module provides seamless integration with:

- Chroma
- FAISS
- Pinecone
- Weaviate
- Milvus
- And more

## Additional Features

- **Filtering**: Support for metadata filtering in compatible retrievers
- **Scoring**: Relevance scoring for ranking and filtering results
- **Streaming**: Support for streaming retrieval in supported implementations
- **Customizable Search Types**: Similarity, MMR, and other search methods
