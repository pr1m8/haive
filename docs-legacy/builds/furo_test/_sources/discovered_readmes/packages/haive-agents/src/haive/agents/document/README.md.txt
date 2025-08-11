# Document Agent

The Document Agent is a comprehensive solution for processing documents through the complete pipeline: **FETCH → LOAD → TRANSFORM → SPLIT → ANNOTATE → EMBED → STORE → RETRIEVE**. It leverages the powerful Document Engine from haive-core to handle 97+ document types and sources with enterprise-grade processing capabilities.

## 🚀 Key Features

### Universal Source Support

- **97+ document sources** including files, URLs, databases, cloud storage
- **Auto-detection** of source types with intelligent processing
- **Multi-format support**: PDF, DOCX, TXT, HTML, MD, JSON, CSV, XML, and 50+ more

### Advanced Processing Pipeline

1. **FETCH**: Source discovery and validation
2. **LOAD**: Intelligent loader selection with fallback mechanisms
3. **TRANSFORM**: Content normalization, encoding detection, metadata extraction
4. **SPLIT**: 5 chunking strategies (recursive, semantic, paragraph, sentence, fixed-size)
5. **ANNOTATE**: Comprehensive metadata enrichment and content classification
6. **EMBED**: Optional vector embeddings for semantic search
7. **STORE**: Optional persistence to vector databases
8. **RETRIEVE**: Optional search and retrieval capabilities

### Enterprise-Ready Features

- **Parallel processing** with configurable worker threads
- **Error resilience** with graceful fallback and detailed reporting
- **Extensible pipeline** with optional stages
- **Performance monitoring** with comprehensive statistics
- **Configuration validation** with sensible defaults

## 📋 Requirements

```bash
# Core dependencies (included in haive-core)
poetry add haive-core

# Optional dependencies for enhanced functionality
poetry add pdfplumber  # PDF processing
poetry add beautifulsoup4  # Web scraping
poetry add requests  # URL loading
```

## 🛠 Installation

The Document Agent is included in the `haive-agents` package:

```bash
from haive.agents.document import DocumentAgent
```

## 📚 Usage Examples

### Basic Usage

```python
from haive.agents.document import DocumentAgent

# Create a basic document agent
agent = DocumentAgent()

# Process a single document
result = agent.process_sources("document.pdf")
print(f"Processed {result.total_documents} documents with {result.total_chunks} chunks")
```

### Custom Configuration

```python
from haive.agents.document import DocumentAgent
from haive.core.engine.document.config import ChunkingStrategy, ProcessingStrategy

# Create agent with custom settings
agent = DocumentAgent(
    name="Custom Document Agent",
    processing_strategy=ProcessingStrategy.PARALLEL,
    chunking_strategy=ChunkingStrategy.SEMANTIC,
    chunk_size=1500,
    chunk_overlap=300,
    max_workers=8,
    enable_embedding=True,
    enable_storage=True
)

# Process multiple sources
sources = [
    "documents/reports/",           # Directory
    "https://example.com/docs",     # Web URL
    "s3://bucket/files/",          # Cloud storage
    "postgresql://db/documents"     # Database
]

result = agent.process_sources(sources)
```

### Specialized Constructors

```python
# Optimized for PDF processing
pdf_agent = DocumentAgent.create_for_pdfs(chunk_size=1000)

# Optimized for web scraping
web_agent = DocumentAgent.create_for_web_scraping()

# Optimized for enterprise scale
enterprise_agent = DocumentAgent.create_for_enterprise()

# Optimized for research
research_agent = DocumentAgent.create_for_research()
```

### Processing Specific Source Types

```python
agent = DocumentAgent()

# Process directory with filtering
result = agent.process_directory(
    "documents/",
    recursive=True,
    include_patterns=["*.pdf", "*.docx"],
    exclude_patterns=["*backup*"]
)

# Process web URLs
result = agent.process_urls([
    "https://example.com/article1",
    "https://example.com/article2"
])

# Process cloud storage
result = agent.process_cloud_storage([
    "s3://bucket/documents/report.pdf",
    "gs://bucket/data/analysis.xlsx"
])

# Analyze source structure without full processing
analysis = agent.analyze_source_structure("large_document.pdf")
print(f"Document has {analysis['document_count']} sections")
```

## 🔧 Configuration Options

### Processing Strategies

```python
# Simple: Basic loading and chunking
agent = DocumentAgent(processing_strategy=ProcessingStrategy.SIMPLE)

# Enhanced: Full metadata extraction, normalization
agent = DocumentAgent(processing_strategy=ProcessingStrategy.ENHANCED)

# Parallel: Multi-threaded for high throughput
agent = DocumentAgent(processing_strategy=ProcessingStrategy.PARALLEL)
```

### Chunking Strategies

```python
# No chunking - process as whole documents
agent = DocumentAgent(chunking_strategy=ChunkingStrategy.NONE)

# Fixed size chunks with overlap
agent = DocumentAgent(
    chunking_strategy=ChunkingStrategy.FIXED_SIZE,
    chunk_size=1000,
    chunk_overlap=200
)

# Paragraph-based chunking
agent = DocumentAgent(chunking_strategy=ChunkingStrategy.PARAGRAPH)

# Sentence-based chunking
agent = DocumentAgent(chunking_strategy=ChunkingStrategy.SENTENCE)

# Recursive chunking (recommended)
agent = DocumentAgent(chunking_strategy=ChunkingStrategy.RECURSIVE)

# Semantic chunking (experimental)
agent = DocumentAgent(chunking_strategy=ChunkingStrategy.SEMANTIC)
```

### Source Type Restrictions

```python
from haive.core.engine.document.config import DocumentSourceType

# Restrict to specific source types
agent = DocumentAgent(
    allowed_source_types=[
        DocumentSourceType.FILE,
        DocumentSourceType.URL
    ]
)
```

### Pipeline Configuration

```python
# Enable optional pipeline stages
agent = DocumentAgent(
    enable_embedding=True,    # Generate vector embeddings
    enable_storage=True,      # Store in vector database
    enable_retrieval=True,    # Enable search capabilities
    normalize_content=True,   # Content normalization
    extract_metadata=True,    # Metadata extraction
    detect_language=True      # Language detection
)
```

## 📊 Output Format

The Document Agent returns a comprehensive `DocumentProcessingResult`:

```python
result = agent.process_sources(["document.pdf"])

# Pipeline Results
print(f"Fetched sources: {result.fetched_sources}")
print(f"Loaded documents: {len(result.loaded_documents)}")
print(f"Document chunks: {len(result.document_chunks)}")
print(f"Annotated chunks: {len(result.annotated_chunks)}")

# Statistics
print(f"Total documents: {result.total_documents}")
print(f"Total chunks: {result.total_chunks}")
print(f"Processing time: {result.processing_time:.2f}s")

# Quality Metrics
print(f"Successful sources: {result.successful_sources}")
print(f"Failed sources: {result.failed_sources}")
print(f"Processing errors: {len(result.processing_errors)}")

# Content Analysis
print(f"Total characters: {result.total_characters}")
print(f"Total words: {result.total_words}")
print(f"Average chunk size: {result.average_chunk_size}")

# Source Analysis
print(f"Source types: {result.source_types}")
print(f"Document formats: {result.document_formats}")
```

## 🎯 Document Source Types Supported

### File Formats

- **Documents**: PDF, DOCX, ODT, RTF, EPUB
- **Text**: TXT, MD, HTML, RST
- **Data**: JSON, CSV, XML, YAML, TOML
- **Spreadsheets**: XLSX, XLS, ODS
- **Presentations**: PPTX, PPT, ODP
- **Code**: PY, JS, TS, JAVA, C, CPP, and 20+ more

### Remote Sources

- **Web**: HTTP/HTTPS URLs, APIs, RSS feeds
- **Cloud Storage**: AWS S3, Google Cloud Storage, Azure Blob, Dropbox, Box
- **Version Control**: Git repositories, GitHub, GitLab
- **Knowledge Bases**: Notion, Confluence, Obsidian, Roam Research

### Databases & APIs

- **SQL**: PostgreSQL, MySQL, SQLite, Oracle, SQL Server
- **NoSQL**: MongoDB, Elasticsearch, Cassandra, CouchDB
- **APIs**: REST APIs, GraphQL endpoints
- **Chat/Messaging**: Slack, Discord, WhatsApp exports

## ⚡ Performance Optimization

### Parallel Processing

```python
# Configure for high throughput
agent = DocumentAgent(
    processing_strategy=ProcessingStrategy.PARALLEL,
    parallel_processing=True,
    max_workers=16,  # Adjust based on CPU cores
    max_sources=100  # Limit concurrent sources
)
```

### Memory Management

```python
# Optimize for large documents
agent = DocumentAgent(
    chunk_size=500,        # Smaller chunks for memory efficiency
    chunk_overlap=50,      # Reduced overlap
    skip_invalid=True,     # Skip problematic documents
    normalize_content=True # Reduce content size
)
```

### Error Handling

```python
# Configure error resilience
agent = DocumentAgent(
    raise_on_error=False,  # Don't stop on individual failures
    skip_invalid=True,     # Skip corrupted documents
    max_sources=50         # Limit batch size
)

result = agent.process_sources(sources)
if result.processing_errors:
    print(f"Encountered {len(result.processing_errors)} errors:")
    for error in result.processing_errors:
        print(f"  - {error}")
```

## 🔍 Advanced Features

### Custom Processing Pipeline

```python
# Create agent with specific pipeline stages
agent = DocumentAgent(
    pipeline_stages=["fetch", "load", "transform", "split", "annotate"],
    processing_strategy=ProcessingStrategy.ENHANCED
)
```

### Content Filtering

```python
# Process with content filtering
result = agent.process_directory(
    "documents/",
    include_patterns=["*.pdf", "*.docx"],
    exclude_patterns=["*backup*", "*temp*"],
    recursive=True
)
```

### Metadata Enrichment

```python
# Enhanced metadata extraction
agent = DocumentAgent(
    extract_metadata=True,
    detect_language=True,
    normalize_content=True
)

result = agent.process_sources("document.pdf")
for doc in result.loaded_documents:
    print(f"Language: {doc.get('language', 'unknown')}")
    print(f"Format: {doc.get('format', 'unknown')}")
    print(f"Source: {doc.get('source', 'unknown')}")
```

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**

   ```python
   # Ensure haive-core is installed
   pip install haive-core

   # Check for missing optional dependencies
   pip install pdfplumber beautifulsoup4 requests
   ```

2. **Processing Failures**

   ```python
   # Enable detailed error reporting
   agent = DocumentAgent(
       raise_on_error=False,
       skip_invalid=True
   )

   result = agent.process_sources(sources)
   if result.processing_errors:
       for error in result.processing_errors:
           print(f"Error: {error}")
   ```

3. **Performance Issues**
   ```python
   # Optimize for large datasets
   agent = DocumentAgent(
       max_workers=4,        # Don't over-parallelize
       chunk_size=500,       # Smaller chunks
       max_sources=20        # Process in batches
   )
   ```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)

agent = DocumentAgent()
result = agent.process_sources("document.pdf")
```

## 📈 Performance Benchmarks

| Document Type | Size  | Processing Time | Chunks Created |
| ------------- | ----- | --------------- | -------------- |
| PDF (Text)    | 1MB   | ~2.5s           | ~50            |
| DOCX          | 500KB | ~1.2s           | ~25            |
| Web Page      | 100KB | ~0.8s           | ~10            |
| JSON Data     | 2MB   | ~1.5s           | ~80            |

_Benchmarks on Intel i7-8750H, 16GB RAM, SSD storage_

## 🔗 Integration Examples

### With Vector Databases

```python
# Enable storage for semantic search
agent = DocumentAgent(
    enable_embedding=True,
    enable_storage=True,
    enable_retrieval=True
)

result = agent.process_sources("knowledge_base/")
stored_ids = result.stored_documents
print(f"Stored {len(stored_ids)} documents for retrieval")
```

### With LangChain

```python
from langchain.vectorstores import Chroma

agent = DocumentAgent(enable_embedding=True)
result = agent.process_sources("documents/")

# Extract embeddings for LangChain
embeddings = [chunk['embedding'] for chunk in result.embedded_chunks]
texts = [chunk['content'] for chunk in result.embedded_chunks]

vectorstore = Chroma.from_texts(texts, embeddings)
```

### Batch Processing

```python
import os
from pathlib import Path

agent = DocumentAgent.create_for_enterprise()

# Process entire directory tree
for root, dirs, files in os.walk("document_repository"):
    pdf_files = [os.path.join(root, f) for f in files if f.endswith('.pdf')]
    if pdf_files:
        result = agent.process_sources(pdf_files)
        print(f"Processed {len(pdf_files)} PDFs in {root}")
```

## 📚 API Reference

### DocumentAgent Class

```python
class DocumentAgent(Agent):
    def __init__(
        self,
        name: str = "Document Agent",
        processing_strategy: ProcessingStrategy = ProcessingStrategy.ENHANCED,
        chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        parallel_processing: bool = True,
        max_workers: int = 4,
        enable_embedding: bool = False,
        enable_storage: bool = False,
        enable_retrieval: bool = False,
        **kwargs
    )
```

### Key Methods

- `process_sources(sources)` - Process single or multiple sources
- `process_directory(path, **options)` - Process directory with filtering
- `process_urls(urls)` - Process web URLs
- `process_cloud_storage(paths)` - Process cloud storage paths
- `analyze_source_structure(source)` - Analyze without full processing

### Convenience Constructors

- `DocumentAgent.create_for_pdfs()` - PDF-optimized configuration
- `DocumentAgent.create_for_web_scraping()` - Web scraping configuration
- `DocumentAgent.create_for_databases()` - Database processing configuration
- `DocumentAgent.create_for_enterprise()` - Enterprise-scale configuration
- `DocumentAgent.create_for_research()` - Research-optimized configuration

## 📄 License

This Document Agent is part of the Haive project. See the main project license for details.

## 🤝 Contributing

Contributions are welcome! Please see the main Haive project for contribution guidelines.

---

For more information about the underlying Document Engine, see the [haive-core documentation](../../../haive-core/src/haive/core/engine/document/README.md).
