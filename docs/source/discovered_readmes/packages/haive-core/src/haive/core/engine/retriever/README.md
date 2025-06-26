# Haive Retriever Engine - Core Concepts

## Overview

The Retriever engine is a specialized component in the Haive framework designed to provide a consistent interface for retrieving relevant documents based on semantic similarity to a query. Built on the Engine base class, it offers a flexible and extensible architecture for various retrieval strategies, with a primary focus on vector store-based retrieval.

## Key Concepts

### The Retriever Engine

The `RetrieverConfig` class extends `InvokableEngine` to establish a standardized interface for retrieval operations. This configuration-driven approach enables:

**Core Features**:

- **Retriever Type Abstraction**: Support for multiple retriever implementations through a type system
- **Search Configuration**: Customizable search parameters and filtering options
- **Vector Store Integration**: Seamless integration with vector databases
- **Result Filtering**: Metadata-based filtering of search results
- **Runtime Parameter Adjustment**: Dynamic configuration of retrieval behavior

### Retriever Types

The system supports various retriever implementations through the `RetrieverType` enum:

- **Vector Store**: Fundamental retrieval from vector databases
- **Time-Weighted**: Recency-biased retrieval
- **Multi-Query**: Generate multiple query variations for better recall
- **Self-Query**: Generate structured filters from natural language
- **Parent Document**: Retrieve chunks with context from parent documents
- **Contextual Compression**: Compress retrieved documents for relevance

### Plugin Architecture

The Retriever engine uses a registration-based plugin architecture:

- **Type Registry**: Maps retriever types to configuration classes
- **Decorator-Based Registration**: Easy extension with new retriever types
- **Factory Pattern**: Convenient creation of appropriate retriever configurations
- **Type Safety**: Compile-time and runtime type checking

### Integration with Vector Stores

The most common implementation is the `VectorStoreRetrieverConfig`, which:

- **Wraps Vector Stores**: Uses vector databases for semantic search
- **Customizes Search Behavior**: Configurable search types and parameters
- **Provides Filtering**: Supports metadata filtering of results
- **Manages Result Count**: Controls the number of documents retrieved

## Implementation Patterns

### Creating a Retriever

```python
from haive.core.engine.retriever import VectorStoreRetrieverConfig
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document

# Create sample documents
documents = [
    Document(page_content="Machine learning is a subset of artificial intelligence."),
    Document(page_content="Neural networks are inspired by biological neurons."),
    Document(page_content="Deep learning models require large amounts of data.")
]

# Create a vector store config
vs_config = VectorStoreConfig(
    name="ml_knowledge_base",
    documents=documents,
    vector_store_provider=VectorStoreProvider.FAISS,
    embedding_model=HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )
)

# Create a retriever config
retriever_config = VectorStoreRetrieverConfig(
    name="ml_retriever",
    vector_store_config=vs_config,
    k=2,  # Number of documents to retrieve
    search_type="similarity"  # Search strategy
)

# Instantiate the retriever
retriever = retriever_config.instantiate()
```

### Using the Retriever

```python
# Basic retrieval with query string
docs = retriever_config.invoke("What is machine learning?")

# With search parameters as dictionary
docs = retriever_config.invoke({
    "query": "How do neural networks work?",
    "k": 3,  # Override default k
    "filter": {"topic": "neural_networks"}  # Apply metadata filter
})

# Using the retriever directly
retriever = retriever_config.instantiate()
docs = retriever.get_relevant_documents("What is deep learning?")
```

### Configuring Search Behavior

```python
# Create a retriever with similarity search
similarity_retriever = VectorStoreRetrieverConfig(
    name="similarity_retriever",
    vector_store_config=vs_config,
    search_type="similarity",
    k=4
)

# Create a retriever with MMR search for result diversity
mmr_retriever = VectorStoreRetrieverConfig(
    name="diverse_retriever",
    vector_store_config=vs_config,
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 20,  # Fetch more candidates initially
        "lambda_mult": 0.7  # Balance relevance with diversity
    }
)
```

### Applying Runtime Configuration

```python
from langchain_core.runnables import RunnableConfig

# Create runtime configuration
runtime_config = RunnableConfig(
    configurable={
        "k": 5,  # Override k parameter
        "filter": {"year": 2023},  # Add metadata filter
        "search_type": "mmr"  # Change search type
    }
)

# Apply to retrieval
docs = retriever_config.invoke("Latest AI developments", runtime_config)
```

### Using the Factory Function

```python
from haive.core.engine.retriever import create_retriever_config, RetrieverType

# Create a retriever config using the factory function
retriever_config = create_retriever_config(
    retriever_type=RetrieverType.VECTOR_STORE,
    name="factory_retriever",
    description="Created using factory function",
    vector_store_config=vs_config,
    k=3,
    search_type="similarity"
)
```

### Creating a Retriever Directly from a Vector Store

```python
from haive.core.engine.retriever import create_retriever_from_vectorstore

# Create a retriever directly from a vector store config
retriever = create_retriever_from_vectorstore(
    vector_store_config=vs_config,
    k=5,
    search_type="mmr",
    search_kwargs={"fetch_k": 20}
)
```

## Advanced Usage Patterns

### Using Different Retriever Types

```python
from haive.core.engine.retriever import RetrieverType
from haive.core.engine.augllm import AugLLMConfig

# Create an LLM config
llm_config = AugLLMConfig(
    name="query_generator",
    model="gpt-3.5-turbo"
)

# Create a multi-query retriever
multi_query_retriever = create_retriever_config(
    retriever_type=RetrieverType.MULTI_QUERY,
    name="multi_query_retriever",
    vector_store_config=vs_config,
    llm_config=llm_config,
    num_queries=3
)

# Create a self-query retriever
self_query_retriever = create_retriever_config(
    retriever_type=RetrieverType.SELF_QUERY,
    name="self_query_retriever",
    vector_store_config=vs_config,
    llm_config=llm_config,
    allowed_comparators=["==", "contains"]
)
```

### Integration with Graph Workflows

```python
from haive.core.graph.dynamic_graph_builder import DynamicGraph
from haive.core.engine.augllm import AugLLMConfig
from langgraph.graph import START, END

# Create engines
retriever_config = VectorStoreRetrieverConfig(
    name="knowledge_retriever",
    vector_store_config=vs_config
)
llm_config = AugLLMConfig(name="response_generator")

# Create graph
graph = DynamicGraph(
    name="rag_workflow",
    components=[retriever_config, llm_config]
)

# Define the workflow
graph.add_node("retrieve", retriever_config)
graph.add_node("generate", llm_config, command_goto=END)
graph.add_edge(START, "retrieve")
graph.add_edge("retrieve", "generate")

# Compile
app = graph.compile()
```

### Creating a Custom Retriever Type

```python
from haive.core.engine.retriever import RetrieverConfig, RetrieverType

# Define a new retriever type
class CustomRetrieverType(RetrieverType):
    CUSTOM = "custom"

# Register a new retriever config
@RetrieverConfig.register(CustomRetrieverType.CUSTOM)
class CustomRetrieverConfig(RetrieverConfig):
    # Custom fields
    custom_parameter: str = "default"

    def instantiate(self) -> BaseRetriever:
        # Custom implementation
        from my_package import CustomRetriever
        return CustomRetriever(
            parameter=self.custom_parameter,
            k=self.k
        )
```

## Best Practices

### 1. Choose the Right Retriever Type

Select the appropriate retriever type based on your specific requirements:

```python
# For simple semantic search
basic_retriever = VectorStoreRetrieverConfig(
    name="basic_retriever",
    vector_store_config=vs_config,
    search_type="similarity"
)

# For diverse results
diverse_retriever = VectorStoreRetrieverConfig(
    name="diverse_retriever",
    vector_store_config=vs_config,
    search_type="mmr",
    search_kwargs={"fetch_k": 20, "lambda_mult": 0.7}
)

# For complex queries that need multiple perspectives
multi_query_retriever = create_retriever_config(
    retriever_type=RetrieverType.MULTI_QUERY,
    name="multi_query_retriever",
    vector_store_config=vs_config,
    llm_config=llm_config
)
```

### 2. Configure Search Parameters Appropriately

Adjust search parameters based on your retrieval goals:

```python
# High precision: fewer, more relevant results
precision_retriever = VectorStoreRetrieverConfig(
    name="precision_retriever",
    vector_store_config=vs_config,
    k=3,
    search_type="similarity",
    score_threshold=0.8  # Only include highly similar documents
)

# High recall: more results to ensure relevant information is captured
recall_retriever = VectorStoreRetrieverConfig(
    name="recall_retriever",
    vector_store_config=vs_config,
    k=10,
    search_type="similarity"
)

# Balanced diversity: use MMR with tuned parameters
balanced_retriever = VectorStoreRetrieverConfig(
    name="balanced_retriever",
    vector_store_config=vs_config,
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 20,
        "lambda_mult": 0.5  # Equal balance between relevance and diversity
    }
)
```

### 3. Leverage Metadata Filtering

Use metadata filters to narrow down search results:

```python
# Using metadata filters in configuration
filtered_retriever = VectorStoreRetrieverConfig(
    name="filtered_retriever",
    vector_store_config=vs_config,
    filter={"category": "machine_learning"}
)

# Applying filters at runtime
docs = retriever_config.invoke({
    "query": "neural networks",
    "filter": {
        "year": {"$gte": 2020},
        "topics": {"$in": ["deep_learning", "neural_networks"]}
    }
})
```

### 4. Optimize for Performance

Configure retrievers for optimal performance:

```python
# For interactive applications: limit result count
interactive_retriever = VectorStoreRetrieverConfig(
    name="interactive_retriever",
    vector_store_config=vs_config,
    k=3  # Smaller k for faster response
)

# For comprehensive research: higher document count
research_retriever = VectorStoreRetrieverConfig(
    name="research_retriever",
    vector_store_config=vs_config,
    k=10  # Larger k for more comprehensive results
)
```

### 5. Dynamic Configuration

Use runtime configuration to adjust retriever behavior dynamically:

```python
# Define different retrieval profiles
def get_retrieval_config(query_type):
    if query_type == "factual":
        return RunnableConfig(configurable={
            "k": 3,
            "search_type": "similarity"
        })
    elif query_type == "exploratory":
        return RunnableConfig(configurable={
            "k": 7,
            "search_type": "mmr",
            "search_kwargs": {"fetch_k": 20, "lambda_mult": 0.7}
        })
    else:
        return RunnableConfig(configurable={"k": 4})

# Apply dynamically
query_type = classify_query(user_query)
config = get_retrieval_config(query_type)
docs = retriever_config.invoke(user_query, config)
```

## Conclusion

The Retriever engine in the Haive framework provides a flexible and powerful system for semantic document retrieval across various use cases. Its plugin architecture, customizable search behavior, and seamless integration with vector stores make it an essential component for knowledge-intensive AI applications.

By selecting the appropriate retriever type, configuring search parameters effectively, and leveraging runtime configurations, you can build sophisticated retrieval systems that match your specific requirements for relevance, diversity, and performance.
