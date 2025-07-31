# Quick Start Guide - Document Loaders

## 🚀 Getting Started with haive Document Loaders

This guide will get you up and running with the document loader system in 5 minutes.

## Installation

```bash
# Install haive-core with all extras
poetry install --all-extras
```

## Basic Usage

### 1. Simple Document Loading

```python
from haive.core.engine.document.loaders import AutoLoader

# Create a loader instance
loader = AutoLoader()

# Load a single document
documents = loader.load("path/to/document.pdf")
print(f"Loaded {len(documents)} pages")

# Access document content
for doc in documents:
    print(doc.page_content[:100])  # First 100 chars
    print(doc.metadata)  # Source info, page numbers, etc.
```

### 2. Load Multiple Documents (Standard LangChain Method)

```python
# Load from multiple sources at once
docs = loader.load_documents([
    "report.pdf",
    "data.csv",
    "https://example.com/documentation",
    "s3://my-bucket/presentations/"
])

print(f"Total documents loaded: {len(docs)}")
```

### 3. Configure for Quality vs Speed

```python
from haive.core.engine.document.loaders import AutoLoaderConfig, LoaderPreference

# Prioritize quality extraction
config = AutoLoaderConfig(
    preference=LoaderPreference.QUALITY,
    enable_metadata=True,
    enable_caching=True
)
loader = AutoLoader(config)

# Now loading will use higher quality extractors
docs = loader.load("complex_document.pdf")
```

### 4. Async Loading for Performance

```python
import asyncio

async def load_many_documents():
    loader = AutoLoader()

    # Async loading of multiple sources
    docs = await loader.aload_documents([
        "https://site1.com/docs",
        "https://site2.com/api",
        "postgres://localhost/knowledge_base"
    ])

    return docs

# Run async
docs = asyncio.run(load_many_documents())
```

### 5. Bulk Loading with Details

```python
# Get detailed results for each source
result = loader.load_bulk([
    "doc1.pdf",
    "doc2.pdf",
    "invalid.pdf"  # This will fail
])

print(f"Success rate: {result.summary['success_rate']}%")
print(f"Total documents: {result.total_documents}")

# Check failed sources
for source, error in result.failed_sources:
    print(f"Failed: {source} - {error}")
```

## Common Use Cases

### Loading from Different Sources

```python
# Local files
docs = loader.load("/path/to/document.pdf")
docs = loader.load("/directory/of/documents/")

# Web pages
docs = loader.load("https://docs.python.org/3/")

# Databases
docs = loader.load(
    "postgresql://user:pass@localhost/db",
    query="SELECT * FROM articles WHERE published = true"
)

# Cloud storage
docs = loader.load("s3://bucket/documents/")
docs = loader.load("gs://bucket/research-papers/")

# APIs
docs = loader.load("https://api.example.com/v1/documents")

# Business platforms
docs = loader.load("salesforce://contacts")
docs = loader.load("sharepoint://documents/policies")
```

### Configuring Source-Specific Options

```python
# Load with specific parameters
docs = loader.load_documents([
    # Simple string source
    "simple.pdf",

    # Dictionary with configuration
    {
        "path": "complex.pdf",
        "extract_images": True,
        "ocr_language": "eng"
    },
    {
        "url": "https://api.service.com/docs",
        "headers": {"Authorization": "Bearer token"},
        "timeout": 120
    }
])
```

### Text Splitting Options

```python
# Configure text splitting
config = AutoLoaderConfig(
    default_chunk_size=1000,
    chunk_overlap=200
)
loader = AutoLoader(config)

# Documents will be automatically split into chunks
docs = loader.load("large_document.pdf")
```

## Auto-Detection Examples

The PathAnalyzer automatically detects source types:

```python
# These are all automatically detected:
loader.load("document.pdf")          # PDF file
loader.load("data.csv")              # CSV file
loader.load("report.docx")           # Word document
loader.load("https://site.com")      # Web page
loader.load("s3://bucket/file")      # S3 storage
loader.load("postgres://db/table")   # Database
loader.load("./src/")                # Directory of code files
```

## Error Handling

```python
try:
    docs = loader.load("potentially_invalid_source")
except ValueError as e:
    print(f"Source detection failed: {e}")
except TimeoutError as e:
    print(f"Loading timed out: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

# Or use load_detailed for non-throwing approach
result = loader.load_detailed("potentially_invalid_source")
if result.errors:
    print(f"Loading failed: {result.errors}")
else:
    print(f"Success: {len(result.documents)} documents")
```

## Performance Tips

1. **Enable Caching** for repeated loads:

   ```python
   config = AutoLoaderConfig(enable_caching=True, cache_ttl=3600)
   ```

2. **Increase Concurrency** for bulk operations:

   ```python
   config = AutoLoaderConfig(max_concurrency=20)
   ```

3. **Use Async Methods** for I/O heavy workloads:

   ```python
   docs = await loader.aload_documents(sources)
   ```

4. **Prefer Speed** when quality isn't critical:
   ```python
   config = AutoLoaderConfig(preference=LoaderPreference.SPEED)
   ```

## Next Steps

- Read the [Developer Guide](./DEVELOPER_GUIDE.md) to add custom loaders
- Check [SOURCE_TYPES.md](../summaries/SOURCE_TYPES.md) for all supported sources
- See [CONFIGURATION.md](../summaries/CONFIGURATION.md) for advanced options
- Review [examples.py](../../../../../packages/haive-core/src/haive/core/engine/document/loaders/examples.py) for more examples

## Troubleshooting

### Import Errors

```python
# If you get import errors, ensure you have all dependencies:
poetry install --all-extras
```

### Source Not Detected

```python
# Check what was detected
result = loader.load_detailed("mystery_source")
print(f"Detected type: {result.source_info.source_type}")
print(f"Category: {result.source_info.category}")
```

### Performance Issues

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check loading times
result = loader.load_detailed("slow_source")
print(f"Loading took: {result.loading_time:.2f}s")
```

---

Ready to load documents? Start with the basic examples above and explore more advanced features as needed!
