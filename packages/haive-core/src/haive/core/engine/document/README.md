# Document Engine

The Document Engine is a comprehensive document processing system that provides unified access to 97+ document loaders from `langchain_community.document_loaders`. It offers intelligent loader selection, advanced processing capabilities, and seamless integration with the Haive engine framework.

## Overview

The Document Engine provides:

- **Universal Document Loading**: Support for 97+ document sources
- **Intelligent Auto-Selection**: Automatically chooses the best loader based on source type
- **Advanced Processing**: Chunking, metadata extraction, parallel processing
- **Unified Interface**: Consistent API across all document types
- **Extensible Architecture**: Easy to add new loaders and strategies

## Key Features

### 🚀 Comprehensive Loader Support

- **File Formats**: PDF, DOCX, TXT, CSV, JSON, XML, YAML, and 50+ more
- **Web Sources**: Web pages, APIs, Wikipedia, ArXiv, YouTube
- **Cloud Storage**: S3, GCS, Azure, Dropbox, Google Drive
- **Databases**: SQL, MongoDB, Elasticsearch, Cassandra
- **Chat/Messaging**: Slack, Discord, WhatsApp, Telegram
- **Knowledge Bases**: Notion, Confluence, Obsidian, Roam

### 🧠 Intelligent Processing

- **Auto-Detection**: Automatically identifies source types
- **Smart Selection**: Chooses optimal loader based on capabilities
- **Fallback Mechanisms**: Gracefully handles missing dependencies
- **Performance Options**: Balance between speed and quality

### ⚡ Advanced Capabilities

- **Parallel Processing**: Process multiple documents concurrently
- **Chunking Strategies**: Fixed size, paragraph, sentence, semantic
- **Metadata Extraction**: Preserve document structure and metadata
- **Error Handling**: Comprehensive error recovery and reporting

## Architecture

The Document Engine follows a modular architecture:

1. **Path Analysis System** (`path_analysis.py`)
   - Analyzes and classifies paths, URLs, and other source identifiers
   - Extracts metadata useful for source type detection and loader selection
   - Supports local files, URLs, cloud storage, databases, and more

2. **Loader Strategy System** (`loaders/strategy.py`)
   - 97 pre-configured loader strategies from langchain_community
   - Strategy selection based on source characteristics and quality requirements
   - Multiple loading strategies per source type
   - Optimization for different use cases (quality, speed, resource usage)

3. **Auto Loader Factory** (`factory.py`)
   - Intelligent loader selection based on source analysis
   - Fallback mechanisms for unavailable loaders
   - Credential management integration
   - Preference-based loader selection

4. **Document Engine** (`engine.py`)
   - Main entry point for document processing
   - Orchestrates the entire loading and processing pipeline
   - Provides both sync and async interfaces
   - Handles chunking, normalization, and metadata extraction

5. **Registry System** (`loaders/registry.py`)
   - Registration of loaders with metadata
   - Discovery of capabilities via decorators
   - Lookup functions for finding appropriate loaders

6. **Processing Components**
   - **Chunking** (`splitters/`): Various text splitting strategies
   - **Transformers** (`transformers/`): Document transformation utilities
   - **Processors** (`processors.py`): Content normalization and format detection

## File Structure

```
document/
├── __init__.py              # Package exports
├── README.md               # This documentation
├── engine.py               # Main DocumentEngine implementation
├── config.py               # Configuration models and enums
├── factory.py              # AutoLoaderFactory for intelligent loading
├── processors.py           # Document processing utilities
├── path_analysis.py        # Source type detection and analysis
├── universal_loader.py     # Universal document loader (experimental)
├── agents.py              # Document processing agents
├── base/                   # Base classes and schemas
│   ├── __init__.py
│   └── schema.py          # Document schemas
├── loaders/               # Loader implementations
│   ├── __init__.py
│   ├── README.md          # Loader subsystem documentation
│   ├── strategy.py        # Loader strategy registry (97 loaders)
│   ├── registry.py        # Loader registration system
│   ├── base/              # Base loader classes
│   ├── sources/           # Source type implementations
│   ├── specific/          # Specific loader implementations
│   └── utils/             # Loader utilities
├── splitters/             # Text splitting strategies
│   ├── __init__.py
│   ├── base.py           # Base splitter interface
│   └── config.py         # Splitter configuration
├── transformers/          # Document transformation utilities
│   ├── __init__.py
│   ├── base.py           # Base transformer interface
│   └── types.py          # Transformer types
├── sources/               # Legacy source implementations
└── types/                 # Type definitions
    ├── __init__.py
    └── enums.py          # Enumerations
```

## Quick Start

### Basic Usage

```python
from haive.core.engine.document import DocumentEngine

# Create engine with default configuration
engine = DocumentEngine()

# Load a single document
result = engine.invoke("document.pdf")
print(f"Loaded {result.total_documents} documents")

# Load from URL
result = engine.invoke("https://example.com/article")

# Load with specific configuration
result = engine.invoke({
    "source": "data.csv",
    "chunking_strategy": "fixed_size",
    "chunk_size": 500
})
```

### Using AutoLoader

```python
from haive.core.engine.document import create_document_loader, AutoLoaderFactory

# Simple auto-loading
loader = create_document_loader("report.docx")
documents = loader.load()

# With specific strategy
loader = create_document_loader(
    "complex.pdf",
    strategy="pdf_pdfplumber",  # Better for tables
    options={"extract_tables": True}
)

# Using factory directly
factory = AutoLoaderFactory()
loader = factory.create_loader(
    "s3://bucket/file.pdf",
    preferences={"prefer_quality": True}
)
```

### Advanced Configuration

```python
from haive.core.engine.document import (
    DocumentEngine,
    DocumentEngineConfig,
    ChunkingStrategy,
    ProcessingStrategy
)

# Configure engine
config = DocumentEngineConfig(
    name="my_engine",
    processing_strategy=ProcessingStrategy.ENHANCED,
    chunking_strategy=ChunkingStrategy.SEMANTIC,
    chunk_size=1000,
    chunk_overlap=200,
    parallel_processing=True,
    max_workers=4,
    normalize_content=True,
    extract_metadata=True
)

engine = DocumentEngine(config=config)

# Process multiple documents in parallel
sources = ["doc1.pdf", "doc2.docx", "https://example.com"]
results = [engine.invoke(source) for source in sources]
```

## Supported Sources

The Document Engine supports 97+ document sources, including:

### File Formats

- **Documents**: PDF (6 loaders), DOCX, ODT, RTF, TXT
- **Data**: CSV, TSV, JSON, YAML, TOML, XML
- **Code**: Python, Jupyter Notebooks
- **Markup**: HTML, Markdown, ReStructuredText, Org Mode
- **Media**: Images (with OCR), EPub, Subtitles

### Web Sources

- Web pages (standard and JavaScript-enabled)
- Wikipedia, ArXiv, YouTube
- Reddit, Hacker News, Mastodon
- RSS feeds, Sitemaps

### Cloud Storage

- AWS S3
- Google Cloud Storage
- Azure Blob Storage
- Dropbox, OneDrive, SharePoint

### Databases

- SQL databases (PostgreSQL, MySQL, etc.)
- MongoDB, Elasticsearch, Cassandra
- BigQuery, Snowflake, DuckDB

### Collaboration Tools

- Notion, Confluence, Obsidian, Roam
- Slack, Discord, WhatsApp, Telegram
- GitHub, GitLab, Jira, Asana
- Trello, Airtable, Figma

## Performance Optimization

### Parallel Processing

```python
engine = DocumentEngine(config={
    "parallel_processing": True,
    "max_workers": 8  # Adjust based on system
})
```

### Chunking Strategies

- **Fixed Size**: Fast, predictable chunks
- **Paragraph**: Preserves natural boundaries
- **Sentence**: Good for NLP tasks
- **Recursive**: Intelligent splitting
- **Semantic**: Context-aware (experimental)

### Loader Selection

```python
# Prefer speed over quality
loader = create_document_loader(path, preferences={"prefer_speed": True})

# Prefer quality over speed
loader = create_document_loader(path, preferences={"prefer_quality": True})
```

## Extending the System

### Adding Custom Loaders

```python
from haive.core.engine.document.loaders.strategy import (
    LoaderStrategy,
    LoaderPriority,
    strategy_registry
)

# Define custom strategy
strategy = LoaderStrategy(
    strategy_name="my_custom_loader",
    loader_class="MyCustomLoader",
    module_path="my_package.loaders",
    speed="fast",
    quality="high",
    best_for=["myformat"],
    priority=LoaderPriority.HIGH
)

# Register it
strategy_registry.register(strategy)
```

## Error Handling

The Document Engine provides comprehensive error handling:

```python
# Configure error behavior
engine = DocumentEngine(config={
    "raise_on_error": False,  # Continue on errors
    "skip_invalid": True      # Skip invalid documents
})

result = engine.invoke("potentially_problematic.pdf")
if result.has_errors:
    for error in result.errors:
        print(f"Error: {error['error']} in {error['source']}")
```

## See Also

- [Loaders Documentation](./loaders/README.md) - Detailed loader system documentation
- [Examples](../../../../examples/) - Working examples and demos
- [API Reference](./api.md) - Complete API documentation
