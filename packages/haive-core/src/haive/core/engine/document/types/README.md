# Document Types and Enumerations

The types subsystem provides type definitions, enumerations, and constants used throughout the document processing system. This ensures type safety and consistency across all components.

## Overview

The types subsystem includes:

- **Enumerations**: Type-safe constants for strategies, formats, and options
- **Type Aliases**: Common type definitions for document processing
- **Constants**: System-wide constants and limits
- **Type Utilities**: Helper functions for type validation and conversion

## Core Enumerations

### Document Source Types

```python
from haive.core.engine.document.types import DocumentSourceType

# Available source types
source_type = DocumentSourceType.PDF
print(source_type.value)  # "pdf"

# All source types
for source in DocumentSourceType:
    print(f"{source.name}: {source.value}")

# Common source types:
# - FILE: Local file system
# - URL: Web URLs
# - S3: Amazon S3
# - GCS: Google Cloud Storage
# - DATABASE: Database sources
# - API: API endpoints
# - UNKNOWN: Unidentified sources
```

### Document Formats

```python
from haive.core.engine.document.types import DocumentFormat

# Document format detection
format = DocumentFormat.PDF
if format.is_binary:
    print("Binary format")

if format.supports_images:
    print("Can contain images")

# Format categories
text_formats = DocumentFormat.text_formats()  # [TXT, MD, RST, ...]
data_formats = DocumentFormat.data_formats()  # [CSV, JSON, XML, ...]
office_formats = DocumentFormat.office_formats()  # [DOCX, XLSX, PPTX, ...]
```

### Processing Strategies

```python
from haive.core.engine.document.types import (
    ProcessingStrategy,
    ChunkingStrategy,
    LoadingStrategy
)

# Processing modes
strategy = ProcessingStrategy.ENHANCED
print(f"Quality: {strategy.quality_level}")
print(f"Speed: {strategy.speed_level}")

# Chunking strategies
chunking = ChunkingStrategy.SEMANTIC
print(f"Requires model: {chunking.requires_model}")
print(f"Preserves context: {chunking.preserves_context}")

# Loading strategies
loading = LoadingStrategy.LAZY
print(f"Memory efficient: {loading.is_memory_efficient}")
```

### Loader Capabilities

```python
from haive.core.engine.document.types import LoaderCapability

# Check capabilities
capabilities = [
    LoaderCapability.ASYNC,
    LoaderCapability.OCR,
    LoaderCapability.TABLE_EXTRACTION
]

if LoaderCapability.OCR in capabilities:
    print("Supports OCR")

# Capability groups
extraction_caps = LoaderCapability.extraction_capabilities()
processing_caps = LoaderCapability.processing_capabilities()
```

## Type Aliases

### Common Types

```python
from haive.core.engine.document.types import (
    DocumentContent,
    DocumentMetadata,
    DocumentID,
    ChunkID,
    SourcePath
)

# Type-safe document content
content: DocumentContent = "This is document content"

# Metadata dictionary
metadata: DocumentMetadata = {
    "source": "example.pdf",
    "page": 1,
    "author": "John Doe"
}

# Unique identifiers
doc_id: DocumentID = "doc_123456"
chunk_id: ChunkID = "chunk_789"

# Source paths
source: SourcePath = "/path/to/document.pdf"
```

### Configuration Types

```python
from haive.core.engine.document.types import (
    LoaderConfig,
    SplitterConfig,
    TransformerConfig,
    EngineConfig
)

# Loader configuration
loader_config: LoaderConfig = {
    "loader_class": "PDFLoader",
    "extract_images": True,
    "ocr_languages": ["en", "es"]
}

# Splitter configuration
splitter_config: SplitterConfig = {
    "strategy": "recursive",
    "chunk_size": 1000,
    "chunk_overlap": 200
}
```

### Result Types

```python
from haive.core.engine.document.types import (
    ProcessingResult,
    LoadingResult,
    ValidationResult
)

# Processing result
result: ProcessingResult = {
    "success": True,
    "documents": [...],
    "errors": [],
    "metadata": {
        "total_time": 1.23,
        "documents_processed": 10
    }
}

# Validation result
validation: ValidationResult = {
    "valid": True,
    "errors": [],
    "warnings": ["Large file size"]
}
```

## Constants

### System Limits

```python
from haive.core.engine.document.types import (
    MAX_CHUNK_SIZE,
    MIN_CHUNK_SIZE,
    DEFAULT_CHUNK_SIZE,
    MAX_DOCUMENTS,
    MAX_FILE_SIZE
)

# Chunking limits
print(f"Max chunk size: {MAX_CHUNK_SIZE}")  # 10000
print(f"Min chunk size: {MIN_CHUNK_SIZE}")  # 100
print(f"Default size: {DEFAULT_CHUNK_SIZE}")  # 1000

# Processing limits
print(f"Max documents: {MAX_DOCUMENTS}")  # 1000
print(f"Max file size: {MAX_FILE_SIZE}")  # 100MB
```

### Default Values

```python
from haive.core.engine.document.types import (
    DEFAULT_ENCODING,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_TIMEOUT,
    DEFAULT_MAX_RETRIES
)

# Common defaults
encoding = DEFAULT_ENCODING  # "utf-8"
overlap = DEFAULT_CHUNK_OVERLAP  # 200
timeout = DEFAULT_TIMEOUT  # 30 seconds
retries = DEFAULT_MAX_RETRIES  # 3
```

## Type Utilities

### Type Validation

```python
from haive.core.engine.document.types.utils import (
    is_valid_source_type,
    is_valid_format,
    validate_config
)

# Validate source type
if is_valid_source_type("pdf"):
    print("Valid source type")

# Validate format
if is_valid_format("docx"):
    print("Valid format")

# Validate configuration
errors = validate_config(config, schema=LoaderConfig)
if not errors:
    print("Configuration is valid")
```

### Type Conversion

```python
from haive.core.engine.document.types.utils import (
    to_source_type,
    to_format,
    normalize_capability
)

# Convert strings to enums
source_type = to_source_type("pdf")  # DocumentSourceType.PDF
format = to_format("docx")  # DocumentFormat.DOCX

# Normalize capability strings
capability = normalize_capability("ocr")  # LoaderCapability.OCR
```

### Type Inference

```python
from haive.core.engine.document.types.utils import (
    infer_format,
    infer_source_type,
    infer_encoding
)

# Infer from file path
format = infer_format("document.pdf")  # DocumentFormat.PDF
source_type = infer_source_type("/path/to/file")  # DocumentSourceType.FILE

# Infer encoding from content
encoding = infer_encoding(byte_content)  # "utf-8"
```

## Creating Custom Types

### Custom Enumerations

```python
from enum import Enum
from haive.core.engine.document.types import DocumentEnum

class CustomProcessingMode(DocumentEnum):
    """Custom processing modes."""

    FAST = "fast"
    BALANCED = "balanced"
    THOROUGH = "thorough"

    @property
    def quality_score(self) -> int:
        """Get quality score for mode."""
        scores = {
            "fast": 1,
            "balanced": 5,
            "thorough": 10
        }
        return scores.get(self.value, 5)
```

### Custom Type Aliases

```python
from typing import TypedDict, Literal, Union, Dict, Any

# Custom metadata type
class ResearchMetadata(TypedDict):
    title: str
    authors: list[str]
    doi: str
    publication_date: str
    citations: int

# Custom configuration
ProcessingMode = Literal["fast", "balanced", "thorough"]
CustomConfig = Dict[str, Union[str, int, bool, ProcessingMode]]
```

### Type Guards

```python
from typing import TypeGuard
from haive.core.engine.document.types import DocumentMetadata

def is_research_document(metadata: DocumentMetadata) -> TypeGuard[ResearchMetadata]:
    """Check if metadata is for research document."""
    required_fields = ["title", "authors", "doi"]
    return all(field in metadata for field in required_fields)

# Usage
if is_research_document(doc.metadata):
    # Type checker knows this is ResearchMetadata
    print(f"DOI: {doc.metadata['doi']}")
```

## Best Practices

### 1. Use Enums for Constants

```python
# Good: Type-safe enum
from haive.core.engine.document.types import ChunkingStrategy
strategy = ChunkingStrategy.RECURSIVE

# Bad: String literal
strategy = "recursive"  # No type safety
```

### 2. Validate User Input

```python
from haive.core.engine.document.types import DocumentFormat
from haive.core.engine.document.types.utils import to_format

# Always validate user input
user_format = "pdf"
try:
    format = to_format(user_format)
except ValueError:
    print(f"Invalid format: {user_format}")
```

### 3. Use Type Aliases

```python
from haive.core.engine.document.types import DocumentMetadata

# Good: Clear type indication
def process_metadata(metadata: DocumentMetadata) -> DocumentMetadata:
    return {**metadata, "processed": True}

# Less clear: Generic dict
def process_metadata(metadata: dict) -> dict:
    return {**metadata, "processed": True}
```

### 4. Leverage Type Information

```python
from haive.core.engine.document.types import DocumentFormat

# Use enum properties
format = DocumentFormat.PDF
if format.requires_special_handling:
    # Apply special processing
    pass

if format.average_size > 1_000_000:  # 1MB
    # Handle large format
    pass
```

## Type Reference

### Quick Reference

```python
# Common imports
from haive.core.engine.document.types import (
    # Enums
    DocumentSourceType,
    DocumentFormat,
    ProcessingStrategy,
    ChunkingStrategy,
    LoaderCapability,

    # Type aliases
    DocumentContent,
    DocumentMetadata,
    DocumentID,

    # Constants
    MAX_CHUNK_SIZE,
    DEFAULT_ENCODING,

    # Utilities
    is_valid_format,
    to_source_type
)
```

### Type Hierarchy

```
DocumentEnum (base)
├── DocumentSourceType
├── DocumentFormat
├── ProcessingStrategy
├── ChunkingStrategy
├── LoadingStrategy
├── LoaderCapability
├── LoaderPriority
└── TransformationType

TypedDict Types
├── DocumentMetadata
├── LoaderConfig
├── SplitterConfig
├── TransformerConfig
└── ProcessingResult
```

## See Also

- [Document Engine Documentation](../README.md)
- [Enumeration Definitions](./enums.py)
- [Type Utilities](./utils.py)
- [Base Types](../base/types.py)
