# RAG (Retrieval Augmented Generation) Agents

This directory contains various RAG agent implementations that combine document retrieval with generation for accurate, grounded responses.

## Available RAG Agents

### SimpleRAGAgent

The base RAG agent that performs simple retrieval operations. It now includes enhanced functionality through the `RetrieverMixin`:

- **Automatic VectorStoreConfig conversion**: Accepts both `BaseRetrieverConfig` and `VectorStoreConfig`
- **Multiple initialization methods**: Create from documents, vector stores, or retriever configs
- **Field validation**: Automatically converts configurations as needed

#### Usage Examples

```python
from haive.agents.rag.base.agent import SimpleRAGAgent
from haive.core.engine.vectorstore import VectorStoreConfig
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig
from langchain_core.documents import Document

# Method 1: Simplest - just documents (uses default embedding model and FAISS)
SIMPLE_RAG_AGENT = SimpleRAGAgent.from_documents([conversation_documents])

# Method 2: Direct initialization with VectorStoreConfig
vector_store_config = VectorStoreConfig(
    name="my_knowledge_base",
    documents=[Document(page_content="Important information...")],
    vector_store_provider="FAISS"
)
agent = SimpleRAGAgent(engine=vector_store_config)

# Method 3: Create from documents with custom embedding
agent = SimpleRAGAgent.from_documents(
    documents=[
        Document(page_content="Document 1 content"),
        Document(page_content="Document 2 content")
    ],
    embedding_model=HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    ),
    name="document_rag_agent"
)

# Method 4: Create from existing vector store
agent = SimpleRAGAgent.from_vectorstore(
    vector_store_config=vector_store_config,
    retriever_kwargs={"k": 5, "search_type": "mmr"},
    name="custom_rag_agent"
)

# Method 5: Use with BaseRetrieverConfig
from haive.core.engine.retriever import VectorStoreRetrieverConfig

retriever_config = VectorStoreRetrieverConfig(
    name="my_retriever",
    vector_store_config=vector_store_config,
    k=4,
    search_type="similarity"
)
agent = SimpleRAGAgent(engine=retriever_config)

# Use the agent
result = await agent.ainvoke({"messages": [{"role": "user", "content": "What information do you have?"}]})
```

### Other RAG Agents

- **Agentic RAG**: Makes intelligent decisions about when and how to retrieve
- **Dynamic RAG**: Adapts retrieval strategy based on query complexity
- **Self-Correcting RAG**: Validates retrieved info and self-corrects errors
- **Multi-Strategy RAG**: Combines multiple retrieval approaches
- **HYDE RAG**: Generates hypothetical documents to improve retrieval
- **Filtered RAG**: Advanced filtering based on metadata and relevance
- **DB RAG**: Specialized for structured data (SQL, GraphDB)
- **Typed RAG**: Enforces type safety on inputs and outputs
- **LLM RAG**: Enhanced RAG with LLM-powered retrieval strategies

## RetrieverMixin

The `RetrieverMixin` (located in `haive.core.engine.retriever.mixins`) provides shared functionality for RAG agents:

### Features

1. **Field Validation**: Automatically converts `VectorStoreConfig` to `VectorStoreRetrieverConfig`
2. **Class Methods**:
   - `from_vectorstore()`: Create agent from vector store configuration
   - `from_documents()`: Create agent from raw documents
   - `from_retriever()`: Create agent from retriever configuration

### Using RetrieverMixin in Custom Agents

```python
from haive.core.engine.retriever.mixins import RetrieverMixin
from haive.agents.base.agent import Agent

class MyCustomRAGAgent(RetrieverMixin, Agent):
    """Custom RAG agent with retriever capabilities."""

    name: str = "My Custom RAG Agent"
    engine: Union[BaseRetrieverConfig, VectorStoreConfig] = Field(...)

    def build_graph(self) -> BaseGraph:
        # Your custom graph implementation
        pass
```

## Common Patterns

### Creating Vector Stores

```python
from haive.core.engine.vectorstore import VectorStoreConfig, VectorStoreProvider

# Using different providers
config = VectorStoreConfig(
    name="my_store",
    documents=documents,
    vector_store_provider=VectorStoreProvider.CHROMA,  # or FAISS, PINECONE, etc.
    embedding_model=embedding_config
)
```

### Configuring Retrievers

```python
# Configure search parameters
retriever_kwargs = {
    "k": 5,                    # Number of documents to retrieve
    "search_type": "mmr",      # or "similarity"
    "score_threshold": 0.7,    # Minimum similarity score
    "fetch_k": 20,            # For MMR: number of docs to fetch before reranking
    "lambda_mult": 0.5        # For MMR: diversity vs relevance trade-off
}

agent = SimpleRAGAgent.from_vectorstore(
    vector_store_config=vs_config,
    retriever_kwargs=retriever_kwargs
)
```

## Testing

See the test files in the `tests/` directory for comprehensive examples:

- `test_base_rag_agent.py`: Basic SimpleRAGAgent tests
- `test_llm_rag_agent.py`: LLM-enhanced RAG tests
- Various other agent-specific test files

## Examples

Example implementations can be found in:

- `llm_rag/example.py`: LLM RAG agent examples
- `db_rag/graph_db/example.py`: Graph database RAG examples
- `db_rag/sql_rag/example.py`: SQL database RAG examples
