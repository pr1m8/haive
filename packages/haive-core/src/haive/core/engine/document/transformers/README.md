# Document Transformers Subsystem

The transformers subsystem provides utilities for transforming and processing documents after loading. It includes text normalization, format conversion, metadata enrichment, and content enhancement capabilities.

## Overview

Document transformers are applied after loading and before/after chunking to:

- **Normalize**: Standardize text format and encoding
- **Clean**: Remove unwanted content or formatting
- **Enrich**: Add metadata or extracted information
- **Convert**: Transform between document formats
- **Enhance**: Improve content quality or structure

## Core Transformers

### Text Normalization

Standardizes text formatting across different sources.

**Features:**

- Unicode normalization
- Whitespace standardization
- Line ending normalization
- Character encoding fixes
- Smart quote conversion

**Usage:**

```python
from haive.core.engine.document.transformers import TextNormalizer

normalizer = TextNormalizer(
    fix_unicode=True,
    lowercase=False,
    remove_extra_whitespace=True,
    normalize_quotes=True
)

cleaned_text = normalizer.transform(raw_text)
```

### Metadata Enrichment

Adds computed metadata to documents.

**Features:**

- Word/character count
- Language detection
- Reading time estimation
- Content classification
- Keyword extraction

**Usage:**

```python
from haive.core.engine.document.transformers import MetadataEnricher

enricher = MetadataEnricher(
    detect_language=True,
    extract_keywords=True,
    compute_statistics=True
)

enriched_doc = enricher.transform(document)
```

### Content Cleaning

Removes unwanted content from documents.

**Features:**

- HTML tag removal
- Header/footer removal
- Advertisement filtering
- Boilerplate removal
- Format artifact cleaning

**Usage:**

```python
from haive.core.engine.document.transformers import ContentCleaner

cleaner = ContentCleaner(
    remove_html=True,
    remove_headers_footers=True,
    remove_advertisements=True,
    preserve_structure=True
)

clean_doc = cleaner.transform(document)
```

### Format Conversion

Converts between document formats.

**Features:**

- Markdown to plain text
- HTML to Markdown
- Plain text to structured format
- Table extraction and formatting
- Code block preservation

**Usage:**

```python
from haive.core.engine.document.transformers import FormatConverter

converter = FormatConverter(
    target_format="markdown",
    preserve_tables=True,
    preserve_code_blocks=True
)

converted_doc = converter.transform(document)
```

## Transformer Pipeline

### Creating Pipelines

```python
from haive.core.engine.document.transformers import TransformerPipeline

# Create a pipeline of transformers
pipeline = TransformerPipeline([
    TextNormalizer(fix_unicode=True),
    ContentCleaner(remove_html=True),
    MetadataEnricher(detect_language=True),
    FormatConverter(target_format="markdown")
])

# Apply to documents
transformed_docs = pipeline.transform_documents(documents)
```

### Conditional Transformers

```python
from haive.core.engine.document.transformers import ConditionalTransformer

# Apply transformer based on conditions
conditional = ConditionalTransformer(
    condition=lambda doc: doc.metadata.get("source_type") == "web",
    transformer=ContentCleaner(remove_advertisements=True)
)

# Only web documents will be cleaned
processed_docs = conditional.transform_documents(documents)
```

## Advanced Transformers

### Language-Specific Processing

```python
from haive.core.engine.document.transformers import LanguageProcessor

processor = LanguageProcessor(
    language="auto",  # Auto-detect
    operations=[
        "sentence_segmentation",
        "tokenization",
        "lemmatization",
        "entity_recognition"
    ]
)

processed_doc = processor.transform(document)
```

### Table Extraction

```python
from haive.core.engine.document.transformers import TableExtractor

extractor = TableExtractor(
    format="markdown",  # or "csv", "json"
    preserve_formatting=True,
    extract_headers=True
)

# Extracts tables and adds to metadata
doc_with_tables = extractor.transform(document)
tables = doc_with_tables.metadata.get("extracted_tables", [])
```

### Code Block Processing

```python
from haive.core.engine.document.transformers import CodeProcessor

processor = CodeProcessor(
    syntax_highlight=True,
    extract_imports=True,
    identify_language=True,
    remove_comments=False
)

processed_doc = processor.transform(document)
```

## Custom Transformers

### Implementing Custom Transformer

```python
from haive.core.engine.document.transformers.base import BaseTransformer
from langchain.schema import Document
from typing import List

class CustomTransformer(BaseTransformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize your transformer

    def transform_document(self, document: Document) -> Document:
        # Transform single document
        transformed_content = self.process(document.page_content)

        return Document(
            page_content=transformed_content,
            metadata={
                **document.metadata,
                "transformed_by": self.__class__.__name__
            }
        )

    def transform_documents(self, documents: List[Document]) -> List[Document]:
        # Transform multiple documents
        return [self.transform_document(doc) for doc in documents]
```

### Async Transformers

```python
from haive.core.engine.document.transformers.base import AsyncTransformer
import asyncio

class AsyncCustomTransformer(AsyncTransformer):
    async def transform_document_async(self, document: Document) -> Document:
        # Async transformation
        transformed_content = await self.process_async(document.page_content)
        return Document(
            page_content=transformed_content,
            metadata=document.metadata
        )

    async def transform_documents_async(self, documents: List[Document]) -> List[Document]:
        # Process in parallel
        tasks = [self.transform_document_async(doc) for doc in documents]
        return await asyncio.gather(*tasks)
```

## Integration with Document Engine

### Configure Transformers in Engine

```python
from haive.core.engine.document import DocumentEngine

engine = DocumentEngine(config={
    "transformers": [
        {"name": "normalizer", "type": "text_normalizer"},
        {"name": "cleaner", "type": "content_cleaner", "remove_html": True},
        {"name": "enricher", "type": "metadata_enricher"}
    ],
    "apply_transformers": "before_chunking"  # or "after_chunking", "both"
})
```

### Transformer Configuration

```python
# Full configuration example
config = {
    "transformers": [
        {
            "name": "normalizer",
            "type": "text_normalizer",
            "enabled": True,
            "config": {
                "fix_unicode": True,
                "remove_extra_whitespace": True,
                "normalize_quotes": True
            }
        },
        {
            "name": "cleaner",
            "type": "content_cleaner",
            "enabled": True,
            "config": {
                "remove_html": True,
                "remove_headers_footers": False,
                "preserve_structure": True
            }
        },
        {
            "name": "enricher",
            "type": "metadata_enricher",
            "enabled": True,
            "config": {
                "detect_language": True,
                "extract_keywords": True,
                "max_keywords": 10
            }
        }
    ]
}
```

## Performance Optimization

### Batch Processing

```python
# Process documents in batches
from haive.core.engine.document.transformers import BatchTransformer

batch_transformer = BatchTransformer(
    transformer=ContentCleaner(),
    batch_size=100,
    parallel=True,
    max_workers=4
)

# Efficient for large document sets
transformed = batch_transformer.transform_documents(large_document_set)
```

### Caching Transformations

```python
from haive.core.engine.document.transformers import CachedTransformer

# Cache transformation results
cached_transformer = CachedTransformer(
    transformer=expensive_transformer,
    cache_size=1000,
    cache_ttl=3600  # 1 hour
)

# Subsequent calls with same input are cached
result = cached_transformer.transform(document)
```

## Best Practices

### 1. Order Matters

```python
# Recommended order
pipeline = TransformerPipeline([
    TextNormalizer(),      # First: normalize encoding
    ContentCleaner(),      # Second: remove unwanted content
    FormatConverter(),     # Third: convert format
    MetadataEnricher()     # Last: enrich with metadata
])
```

### 2. Choose Appropriate Transformers

| Document Type   | Recommended Transformers                         |
| --------------- | ------------------------------------------------ |
| Web Pages       | ContentCleaner, HTMLToMarkdown, AdRemover        |
| PDFs            | TextNormalizer, TableExtractor, MetadataEnricher |
| Code Files      | CodeProcessor, SyntaxHighlighter                 |
| Chat Logs       | MessageParser, TimestampNormalizer               |
| Academic Papers | CitationExtractor, AbstractExtractor             |

### 3. Handle Errors Gracefully

```python
from haive.core.engine.document.transformers import SafeTransformer

# Wrap transformer for error handling
safe_transformer = SafeTransformer(
    transformer=potentially_failing_transformer,
    on_error="skip",  # or "log", "raise"
    default_value=""
)
```

## Troubleshooting

### Common Issues

1. **Encoding Errors**

   ```python
   # Use TextNormalizer with aggressive settings
   normalizer = TextNormalizer(
       fix_unicode=True,
       encoding="utf-8",
       errors="ignore"  # or "replace"
   )
   ```

2. **Performance Issues**

   ```python
   # Enable parallel processing
   transformer = BatchTransformer(
       transformer=slow_transformer,
       parallel=True,
       batch_size=50
   )
   ```

3. **Memory Usage**

   ```python
   # Use streaming transformer for large documents
   from haive.core.engine.document.transformers import StreamingTransformer

   streaming = StreamingTransformer(
       transformer=memory_intensive_transformer,
       chunk_size=1000
   )
   ```

### Debug Transformations

```python
# Enable debug logging
import logging
logger = logging.getLogger("haive.transformers")
logger.setLevel(logging.DEBUG)

# Inspect transformation steps
from haive.core.engine.document.transformers import DebugTransformer

debug = DebugTransformer(
    transformer=your_transformer,
    log_input=True,
    log_output=True,
    log_metadata=True
)

result = debug.transform(document)
```

## Available Transformers

### Text Processing

- TextNormalizer
- WhitespaceNormalizer
- EncodingFixer
- SmartQuoteConverter

### Content Cleaning

- HTMLCleaner
- AdvertisementRemover
- BoilerplateRemover
- HeaderFooterRemover

### Format Conversion

- MarkdownConverter
- HTMLToMarkdown
- PlainTextConverter
- TableFormatter

### Metadata Enrichment

- LanguageDetector
- KeywordExtractor
- StatisticsComputer
- ReadabilityAnalyzer

### Specialized

- CodeProcessor
- CitationExtractor
- EmailParser
- URLExtractor

## See Also

- [Document Engine Documentation](../README.md)
- [Transformer Base Classes](./base.py)
- [Transformer Types](./types.py)
