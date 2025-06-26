# Document Processing System

This package implements both a document loader engine system and a document agent system for Haive. It provides a unified interface for loading, processing, and managing documents from various sources.

## Implementation Approaches

The package offers two complementary approaches to document processing:

1. **Engine-Centric Approach**: Uses the `DocumentLoaderEngine` that implements the `InvokableEngine` interface, integrating with Haive's engine framework.
2. **Agent-Centric Approach**: Uses the `DocumentAgent` that implements the `Agent` interface, following Haive's agent patterns and state-based approach.

## Engine-Centric Architecture

The document loader engine system follows a layered architecture:

1. **Engine Layer**: `DocumentLoaderEngine` - The main entry point that implements the `InvokableEngine` interface.
2. **Registry Layer**: `SourceTypeRegistry` and `LoaderRegistry` - Manage source types and loader strategies.
3. **Source Layer**: `BaseSource` hierarchy - Abstractions for different document sources.
4. **Path Analysis Layer**: Analyzes paths and URLs to determine their nature and properties.
5. **Factory Layer**: Convenience methods for creating engines for common use cases.

## Agent-Centric Architecture

The document agent system follows a state-based approach:

1. **State Layer**: `DocumentState` - State schema for document operations.
2. **Agent Layer**: `DocumentAgent` - Agent for loading and processing documents.
3. **Processor Layer**: `DocumentProcessors` - Adapters for core engine transformers and splitters.
4. **Workflow Layer**: LangGraph workflow for document processing with analyze, load, chunk, and finalize nodes.
5. **Factory Layer**: Convenience methods for creating specialized agents.

## Key Components

### Document State

The `DocumentState` schema tracks the state of document processing, including:

- Document sources to process
- Loaded documents and their chunks
- Processing statistics
- Error messages
- Default loading and chunking options

### Document Agent

The `DocumentAgent` class provides functionality for loading and processing documents using a state-based approach. It:

- Analyzes document sources to determine their type and format
- Loads documents from various sources (files, URLs, text input, etc.)
- Chunks documents into smaller pieces using different strategies
- Integrates with core engine document transformers and splitters
- Provides a LangGraph workflow for document processing

### Document Processors

The `document_processors.py` module provides adapters and factories for using the core engine's document transformers and splitters with the DocumentAgent:

- `SplitterFactory` creates appropriate text splitters based on chunking strategy and document format
- `TransformerFactory` creates document transformers based on document format
- Processing functions for transforming and splitting documents
- Fallback implementations for when core components aren't available

### Engine Configuration

The `DocumentLoaderConfig` class defines the configuration model for the document loader engine, including:

- Source type specification
- Loader selection
- Loading options
- Error handling

### Source Type System

The source type system provides abstractions for different document sources:

- `BaseSource`: Root base class for all sources
- `LocalSource`: Base for local filesystem sources
- `RemoteSource`: Base for remote/URL sources
- `DatabaseSource`: Base for database sources
- `CloudSource`: Base for cloud storage sources

### Path Analysis System

The path analysis system determines the nature of paths and URLs:

- `PathType`: Primary path type classification
- `FileCategory`: High-level file category
- `DatabaseType`: Database type classification
- `CloudProvider`: Cloud storage provider classification
- `PathAnalysisResult`: Result of path analysis

## Agent-Centric Usage Examples

### Basic Agent Usage

```python
from document_agent import DocumentAgent, create_file_document_agent
from document_state import ChunkingStrategy

# Create a file document agent
agent = create_file_document_agent(
    file_paths=["document1.txt", "document2.pdf"],
    chunking_strategy=ChunkingStrategy.PARAGRAPH
)

# Process documents
agent.process_documents()

# Access processed documents
for doc in agent.get_documents():
    print(f"Document: {doc.source_path}")
    print(f"Content length: {len(doc.content)}")
    print(f"Chunks: {doc.chunk_count}")
```

### Integration with Core Engine

```python
from document_agent import DocumentAgent, DocumentAgentOptions
from document_state import ChunkingOptions, ChunkingStrategy

# Create options with specific chunking strategy
options = DocumentAgentOptions(
    default_chunking_options=ChunkingOptions(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=500,
        chunk_overlap=100,
    )
)

# Create document agent
agent = DocumentAgent(options=options)

# Add sources with different formats
agent.add_source("document.html")  # Will use HTML transformer
agent.add_source("document.md")    # Will use Markdown splitter
agent.add_source("document.txt")   # Will use recursive splitter

# Process documents
agent.process_documents()
```

### Format-Specific Processing

```python
from document_agent import DocumentAgent
from document_state import ChunkingOptions, ChunkingStrategy

agent = DocumentAgent()

# HTML file with HTML-specific chunking
agent.add_source(
    "document.html",
    chunking_options=ChunkingOptions(
        strategy=ChunkingStrategy.PARAGRAPH
    )
)

# Markdown file with Markdown-specific chunking
agent.add_source(
    "document.md",
    chunking_options=ChunkingOptions(
        strategy=ChunkingStrategy.RECURSIVE,
        chunk_size=300
    )
)

# Process documents
agent.process_documents()
```

## Engine-Centric Usage Examples

### Loading a File

```python
from haive.core.engine.document import create_file_loader_engine

# Create engine
engine = create_file_loader_engine(file_path="document.pdf")

# Load document
documents = engine.invoke("document.pdf")

# Process documents
for doc in documents.documents:
    print(f"Content: {doc['page_content'][:100]}...")
    print(f"Metadata: {doc['metadata']}")
```

### Loading a Web Page

```python
from haive.core.engine.document import create_web_loader_engine

# Create engine
engine = create_web_loader_engine(url="https://example.com")

# Load document
documents = engine.invoke("https://example.com")

# Process documents
for doc in documents.documents:
    print(f"Content: {doc['page_content'][:100]}...")
    print(f"Metadata: {doc['metadata']}")
```

### Loading a Directory

```python
from haive.core.engine.document import create_directory_loader_engine

# Create engine
engine = create_directory_loader_engine(
    directory_path="/path/to/documents",
    recursive=True,
    include_extensions=[".pdf", ".docx", ".txt"]
)

# Load documents
documents = engine.invoke("/path/to/documents")

# Process documents
print(f"Loaded {documents.total_documents} documents")
```

## Chunking Strategies

The agent system supports different chunking strategies:

- `FIXED_SIZE`: Chunks documents into fixed-size pieces
- `RECURSIVE`: Recursively splits documents using a list of separators
- `PARAGRAPH`: Splits documents by paragraphs (double newlines)
- `SENTENCE`: Splits documents by sentences
- `SEMANTIC`: Uses semantic chunking (requires core engine)
- `NONE`: No chunking, keeps documents whole

## Core Engine Integration

The document agent integrates with the core engine's document transformers and splitters through the `document_processors.py` module. This provides:

- Enhanced document transformation (HTML to text, HTML to markdown, etc.)
- Specialized document splitting based on format (Markdown, HTML, etc.)
- Format-specific processing pipelines

The integration is designed to gracefully handle cases where the core engine components aren't available, falling back to simplified implementations.

## Running Examples

The repository includes several example scripts:

- `simplified_example.py`: Basic functionality without core dependencies
- `engine_integration_example.py`: Integration with core engine transformers and splitters

Run the examples to see the document agent in action:

```bash
python simplified_example.py
python engine_integration_example.py
```

## Extension Points

Both systems are designed to be extensible:

1. **Custom Sources**: Create new source types by extending base classes
2. **Custom Loaders**: Register new loader strategies
3. **Custom Analyzers**: Extend path analysis capabilities
4. **Custom Transformers**: Create new document transformers
5. **Custom Splitters**: Create new document splitters
6. **Engine/Agent Configuration**: Customize behavior
