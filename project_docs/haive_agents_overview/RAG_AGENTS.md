# RAG Agents Comprehensive Overview

## Overview

The haive-agents package contains a comprehensive collection of Retrieval-Augmented Generation (RAG) agents, implementing 12+ different RAG patterns and strategies. Each is optimized for specific use cases and query types.

## Directory Structure

```
/packages/haive-agents/src/haive/agents/rag/
├── base/               # Base RAG implementation and utilities
├── simple/             # Basic retrieve-and-generate pattern
├── multi_query/        # Multiple query perspectives
├── hyde/               # Hypothetical Document Embeddings
├── fusion/             # Multi-query with reciprocal rank fusion
├── flare/              # Forward-Looking Active REtrieval
├── corrective/         # Self-correcting retrieval (CRAG)
├── speculative/        # Hypothesis generation and verification
├── step_back/          # Abstract reasoning patterns
├── memory_aware/       # Conversation context integration
├── self_route/         # Dynamic routing based on query
├── adaptive/           # Adaptive tool integration
├── adaptive_tools/     # Enhanced adaptive capabilities
├── agentic_router/     # Intelligent strategy selection
├── query_planning/     # Complex query decomposition
├── multi_agent_rag/    # Multi-agent RAG workflows
├── document_grading/   # Document relevance evaluation
├── hallucination_grading/ # Answer verification
├── factories/          # Factory patterns for RAG creation
└── common/             # Shared components and utilities
```

## Core RAG Implementations

### 1. Base RAG Agent (`base/base_agent.py`)

- **Class**: `BaseRAGAgent`
- **Purpose**: Foundation for all RAG implementations
- **Key Methods**:
  - `retrieve()`: Retrieve documents based on query
  - `generate_answer()`: Generate answer from retrieved documents
- **Usage**: Extended by other RAG agents

### 2. Simple RAG Agent (`simple/agent.py`)

- **Class**: `SimpleRAGAgent`
- **Type**: SequentialAgent
- **Workflow**: Retrieval → Answer Generation
- **Best for**: Basic Q&A over documents

### 3. HyDE RAG Agent (`hyde/agent.py`)

- **Class**: `HyDERAGAgent`
- **Workflow**: Query → Generate Hypothetical Doc → Embed → Retrieve Real Docs → Generate
- **Purpose**: Bridges query-document semantic gap
- **Variants**:
  - `agent.py`: Basic implementation
  - `agent_v2.py`: Enhanced version
  - `enhanced_agent.py`: Advanced features
  - `enhanced_agent_v2.py`: Latest improvements

### 4. Corrective RAG Agent (`corrective/agent.py`)

- **Class**: `CorrectiveRAGAgent`
- **Type**: ConditionalAgent
- **Workflow**: Retrieval → Relevance Check → Knowledge Refinement/Web Search/Combine
- **Features**: Self-correcting retrieval with quality assessment
- **Variants**:
  - `agent.py`: Standard implementation
  - `agent_v2.py`: Enhanced grading

### 5. Multi-Query RAG (`multi_query/agent.py`)

- **Purpose**: Generate multiple query perspectives for comprehensive retrieval
- **Benefits**: Better coverage of user intent

### 6. Fusion RAG (`fusion/agent.py`)

- **Features**: Multi-query retrieval with reciprocal rank fusion
- **Purpose**: Combine results from multiple retrieval strategies

### 7. FLARE RAG (`flare/agent.py`)

- **Full Name**: Forward-Looking Active REtrieval
- **Features**: Iterative refinement with active retrieval
- **Use Case**: Complex queries requiring progressive understanding

### 8. Speculative RAG (`speculative/agent.py`)

- **Features**: Hypothesis generation and verification
- **Purpose**: Handle uncertain or exploratory queries

### 9. Step-Back RAG (`step_back/agent.py`)

- **Approach**: Abstract reasoning before specific answers
- **Use Case**: Questions requiring conceptual understanding

### 10. Memory-Aware RAG (`memory_aware/agent.py`)

- **Features**: Conversation context integration
- **Purpose**: Multi-turn conversations with context retention

## Advanced RAG Systems

### Multi-Agent RAG (`multi_agent_rag/`)

Complex workflows combining multiple agents:

#### Key Files:

- `graded_rag_workflows.py`: RAG with comprehensive grading
- `enhanced_multi_rag.py`: Enhanced multi-agent patterns
- `complete_rag_workflows.py`: Full pipeline implementations
- `agents.py`: Individual agent components

#### Available Workflows:

1. **FullyGradedRAGAgent**: Comprehensive grading at every step
2. **Document grading agents**: Evaluate relevance
3. **Hallucination detection**: Verify answer accuracy
4. **Priority ranking**: Optimize retrieval results

### Agentic Router (`agentic_router/`)

- **Purpose**: Intelligent strategy selection based on query analysis
- **Files**:
  - `agent.py`: Basic routing
  - `agent_v2.py`: Enhanced routing logic
  - `agent_chain.py`: Chain-based implementation

### Query Planning (`query_planning/`)

- **Purpose**: Decompose complex queries into sub-queries
- **Features**: Strategic query execution planning

## Factory Patterns

### RAG Workflow Factory (`factories/rag_workflow_factory.py`)

- Centralized creation of RAG workflows
- Consistent interface across all RAG types

### Compatible RAG Factory (`factories/compatible_rag_factory.py`)

- Backward-compatible RAG creation
- Simple interface for common use cases

## Common Components (`common/`)

### Answer Generators (`common/answer_generators/`)

- Standardized prompts for answer generation
- Consistent formatting across RAG types

### Document Graders (`common/document_graders/`)

- Binary grading for relevance
- Comprehensive grading with detailed metrics
- Models for structured output

### Hallucination Graders (`common/hallucination_graders/`)

- Verify answer accuracy against sources
- Detect and flag potential hallucinations

### Query Constructors (`common/query_constructors/`)

- **FLARE**: Forward-looking query construction
- **HyDE**: Hypothetical document generation

## Database RAG (`db_rag/`)

### SQL RAG (`db_rag/sql_rag/`)

- Query databases using natural language
- SQL generation and execution

### Graph DB RAG (`db_rag/graph_db/`)

- Graph database integration
- Complex relationship queries

## Specialized Implementations

### Dynamic RAG (`dynamic/`)

- Adapt retrieval strategy based on data source
- Support for multiple data source types

### Filtered RAG (`filtered/`)

- Apply filters during retrieval
- Metadata-based filtering

### LLM RAG (`llm_rag/`)

- Pure LLM-based retrieval without vector stores
- Direct language model querying

### Self-Correcting RAG (`self_corr/`)

- Automatic error detection and correction
- Iterative improvement

### Self-RAG v2 (`self_rag2/`)

- Advanced self-reflective architecture
- Node-based workflow with:
  - Document grading
  - Answer generation decisions
  - Query transformation

## Usage Patterns

### Three Implementation Styles

1. **Traditional Style**: Direct agent instantiation
2. **Chain Style**: Sequential workflows using ChainAgent
3. **Multi Style**: Parallel/conditional execution using MultiAgent

### Example Usage

```python
from haive.agents.rag.chain_collection import RAGChainCollection
from langchain_core.documents import Document

# Create documents
docs = [Document(page_content="...")]

# Create RAG agent
collection = RAGChainCollection()
agent = collection.create_hyde_rag(docs, llm_config)

# Invoke
response = agent.invoke({"query": "What is machine learning?"})
```

## Key Features

- **Modular Architecture**: Composable components
- **Type Safety**: Pydantic models for validation
- **Flexibility**: Multiple implementation styles
- **Extensibility**: Easy to add new RAG patterns
- **Integration**: Works with various vector stores and LLMs

## Testing

Comprehensive test coverage in:

- `/packages/haive-agents/tests/rag/`
- Unit tests for each RAG type
- Integration tests for workflows
- Performance benchmarks
