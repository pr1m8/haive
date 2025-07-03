# Document Agents Overview

## Overview

The haive-agents package provides specialized agents for comprehensive document processing, leveraging the Document Engine from haive-core to handle 97+ document types and sources.

## Document Agent Implementations

### 1. Document Agent (`/src/haive/agents/document/agent.py`)

**Purpose**: Implements the full document processing pipeline

**Pipeline Stages**:
1. **FETCH** - Retrieve documents from sources
2. **LOAD** - Load documents into memory
3. **TRANSFORM** - Normalize and transform documents
4. **SPLIT** - Chunk documents for processing
5. **ANNOTATE** - Add metadata and annotations
6. **EMBED** - Generate embeddings
7. **STORE** - Store in vector database
8. **RETRIEVE** - Query stored documents

**Key Classes**:
- `DocumentProcessingResult`: Comprehensive result tracking
- `DocumentProcessingState`: Pipeline state management
- `DocumentAgent`: Main agent implementation

**Features**:
- Handles 97+ document types
- Advanced chunking strategies
- Metadata extraction
- Parallel processing support
- Integration with vector stores

**Configuration Options**:
- Source types: Local files, URLs, databases, cloud storage
- Processing strategies: Sequential, parallel, batch
- Chunking strategies: Fixed, semantic, sliding window
- Output formats: JSON, structured data, embeddings

### 2. Document Loader Agent (`/src/haive/agents/document_loader/base/agent.py`)

**Purpose**: Specialized agent for loading documents from various sources

**Class**: `DocumentLoaderAgent`

**Capabilities**:
- Local files and directories
- Web pages and URLs
- Databases (with credentials)
- Cloud storage (with credentials)
- API services

**Key Features**:
- Synchronous and asynchronous operation
- Batch loading support
- Format detection
- Error handling and retry logic

**Integration**:
- Can be used standalone
- Integrates into complex workflows
- Supports the agent framework

### 3. Document Grading Agent (`/src/haive/agents/rag/document_grading/agent.py`)

**Purpose**: Evaluate document relevance and quality

**Features**:
- Binary relevance grading (yes/no)
- Comprehensive quality assessment
- Integration with RAG pipelines
- Structured output models

## Document Processing Components

### Document Engine Integration

The agents leverage `haive.core.engine.document`:
- `DocumentEngine`: Core processing engine
- `DocumentEngineConfig`: Configuration management
- Processing strategies and formats

### Supported Document Types

Through the Document Engine, agents support:
- **Text**: TXT, MD, RST, LOG
- **Office**: DOCX, XLSX, PPTX, ODT
- **PDF**: Standard, scanned (with OCR)
- **Web**: HTML, XML, RSS
- **Data**: CSV, JSON, YAML, TOML
- **Code**: PY, JS, TS, and more
- **Media**: Images (with OCR), audio transcripts
- **Archives**: ZIP, TAR, GZ

### Processing Strategies

1. **ChunkingStrategy**:
   - Fixed size chunks
   - Semantic chunking
   - Sliding window
   - Sentence-based
   - Paragraph-based

2. **ProcessingStrategy**:
   - Sequential processing
   - Parallel processing
   - Batch processing
   - Stream processing

## Usage Examples

### Basic Document Agent Usage

```python
from haive.agents.document.agent import DocumentAgent

# Create agent
agent = DocumentAgent(
    name="PDF Processor",
    source_type="local",
    processing_strategy="parallel",
    chunking_strategy="semantic"
)

# Process documents
result = agent.process_documents(
    sources=["path/to/documents/*.pdf"],
    store_embeddings=True
)
```

### Document Loader Agent Usage

```python
from haive.agents.document_loader.base.agent import DocumentLoaderAgent

# Create loader agent
loader = DocumentLoaderAgent(
    name="Web Loader",
    include_content=True,
    include_metadata=True
)

# Load documents
docs = loader.load_from_urls([
    "https://example.com/doc1",
    "https://example.com/doc2"
])
```

### Integration with RAG

```python
# Load documents
loader = DocumentLoaderAgent()
documents = loader.load_from_directory("./knowledge_base")

# Create RAG agent with loaded documents
rag_agent = SimpleRAGAgent.from_documents(documents)

# Query
response = rag_agent.invoke({"query": "What is the main topic?"})
```

## State Management

### DocumentProcessingState

Tracks the entire pipeline state:
- Source tracking
- Processing status
- Error handling
- Metrics collection
- Result aggregation

### ProcessedDocument Model

Standardized output format:
- Document ID
- Content
- Metadata
- Chunks
- Embeddings
- Processing timestamps

## Advanced Features

### 1. Parallel Processing
- Concurrent document loading
- Batch embedding generation
- Distributed processing support

### 2. Error Handling
- Retry logic for failed documents
- Partial success handling
- Detailed error reporting

### 3. Metadata Extraction
- Automatic metadata detection
- Custom metadata extractors
- Structured data parsing

### 4. Vector Store Integration
- Direct integration with popular vector databases
- Automatic indexing
- Query optimization

## Testing and Validation

Test files location:
- `/tests/document/test_document_agent.py`
- `/tests/unit/test_document_loader_agent.py`
- `/tests/fixtures/documents.py`

## Best Practices

1. **Choose the Right Agent**:
   - Use Document Agent for full pipeline
   - Use Document Loader for simple loading
   - Use Document Grading for quality assessment

2. **Configure Appropriately**:
   - Match chunking strategy to use case
   - Use parallel processing for large batches
   - Enable caching for repeated access

3. **Handle Errors Gracefully**:
   - Implement retry logic
   - Log processing failures
   - Provide fallback options

4. **Optimize Performance**:
   - Batch similar documents
   - Use appropriate chunk sizes
   - Enable concurrent processing

## Integration Points

- **With RAG Agents**: Provide document sources
- **With Vector Stores**: Store processed documents
- **With LLMs**: Generate embeddings and summaries
- **With Workflows**: Part of larger pipelines