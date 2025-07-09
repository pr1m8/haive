# Haive Core - Foundation Package

## Overview

Haive Core is the foundational package that provides the essential building blocks for the entire Haive ecosystem. It contains the core abstractions, base classes, and utilities that power all other Haive packages.

## What Haive Core Does

### 1. Engine System - The Universal Interface

The Engine system provides a standardized way to interact with any AI component:

- **Unified API**: Every component (LLMs, retrievers, tools) shares the same interface
- **Runtime Configuration**: Dynamically adjust parameters without code changes
- **Schema Management**: Automatic input/output validation and type safety
- **Serialization**: Save and restore any engine's complete state

**Key Components:**

- `InvokableEngine`: For components that process input → output (LLMs, retrievers)
- `NonInvokableEngine`: For utility components (embeddings, loaders)
- `AugLLM`: Enhanced LLM with tools, structured output, and advanced prompting

### 2. Graph System - Dynamic Workflow Builder

Build complex AI workflows as graphs that can be modified at runtime:

- **Dynamic Graph Builder**: Compose workflows programmatically
- **Node Factory**: Create processing nodes from any engine
- **Pattern Registry**: Reusable workflow patterns (RAG, ReAct, etc.)
- **State Management**: Sophisticated state schemas with reducers

**Example Use:**

```python
graph = DynamicGraph(components=[llm, retriever])
graph.add_node("search", retriever)
graph.add_node("generate", llm)
graph.add_edge("search", "generate")
```

### 3. Schema System - Intelligent State Management

Advanced state management designed for AI workflows:

- **Field Sharing**: Share state between parent/child graphs
- **Reducers**: Define how state updates are merged
- **Auto-Generation**: Derive schemas from components
- **Serialization**: Full state persistence

**Features:**

- `StateSchema`: Base class with sharing and reducers
- `SchemaComposer`: Build schemas dynamically
- `StateSchemaManager`: Runtime schema manipulation

### 4. Configuration System - Runtime Control

Sophisticated configuration management:

- **Runnable Config**: Standardized runtime parameters
- **Engine Targeting**: Configure specific engines by ID
- **Hierarchical Config**: Cascading configuration with overrides
- **Thread Management**: Session and conversation handling

### 5. Persistence Layer - State Management

Comprehensive persistence capabilities:

- **Multiple Backends**: PostgreSQL, MongoDB, SQLite, Memory
- **Checkpointing**: Save/restore complete agent states
- **Thread Management**: Conversation history and context
- **Automatic Setup**: Database tables created as needed

### 6. Document Processing - Content Pipeline

Complete document handling system:

- **40+ Loaders**: PDF, Word, Excel, HTML, Markdown, Code files, etc.
- **Smart Splitting**: Intelligent document chunking
- **Transformers**: Document processing and enrichment
- **Source Management**: Local files, web content, databases

### 7. Model Abstractions - Provider Agnostic

Unified interfaces for AI models:

- **LLM Models**: Support for OpenAI, Anthropic, Azure, HuggingFace, etc.
- **Embeddings**: Text embedding models from various providers
- **Retrievers**: Vector search, keyword search, hybrid approaches
- **Vector Stores**: FAISS, Chroma, Pinecone, Weaviate, etc.

### 8. Common Utilities - Shared Infrastructure

Essential utilities used across Haive:

- **Mixins**: Reusable functionality (tools, state, serialization)
- **Type System**: Advanced types and protocols
- **Logging**: Sophisticated logging with UI
- **Discovery**: Automatic component discovery

## Key Capabilities

### Dynamic Composition

```python
# Create engines
llm = AugLLMConfig(model="gpt-4", tools=[SearchTool])
retriever = RetrieverConfig(vector_store=faiss_store)

# Compose into workflow
graph = DynamicGraph([llm, retriever])
```

### State Schema Generation

```python
# Auto-generate schema from components
Schema = SchemaComposer.from_components([llm, retriever])

# Add custom fields
composer = SchemaComposer()
composer.add_field("context", List[str], reducer=operator.add)
```

### Persistence

```python
# Setup persistence
from haive.core.persistence import PostgresCheckpointer
checkpointer = PostgresCheckpointer(connection_string)

# Save state
checkpointer.put(thread_id, state)

# Restore state
state = checkpointer.get(thread_id)
```

### Document Processing

```python
# Load various document types
loader = DocumentLoader()
docs = loader.load("report.pdf", "data.xlsx", "code.py")

# Smart splitting
splitter = TextSplitter(chunk_size=1000)
chunks = splitter.split_documents(docs)
```

## Integration Points

Haive Core integrates with:

- **LangChain/LangGraph**: Extended functionality
- **Pydantic v2**: Type safety and validation
- **Major LLM Providers**: OpenAI, Anthropic, etc.
- **Vector Databases**: All major providers
- **Document Formats**: 40+ file types

## Use Cases

1. **Building Custom Agents**: Use base classes to create specialized agents
2. **Workflow Orchestration**: Compose complex multi-step processes
3. **State Management**: Handle conversation history and context
4. **Document Processing**: Build RAG systems with any content
5. **Tool Integration**: Add capabilities to any LLM

\*Note: Comprehensive API documentation coming soon. Haive Core prov
