# Document Base Classes and Schemas

The base subsystem provides foundational classes, schemas, and interfaces that define the core structure of the document processing system. These components ensure consistency and type safety across all document operations.

## Overview

The base subsystem includes:

- **Document Schemas**: Core data structures for documents
- **Base Classes**: Abstract interfaces for loaders, splitters, and transformers
- **Type Definitions**: Type hints and protocols for document processing
- **Common Utilities**: Shared functionality across components

## Core Schemas

### Document Schema

The fundamental document structure used throughout the system:

```python
from haive.core.engine.document.base.schema import Document

# Basic document
doc = Document(
    page_content="This is the document content",
    metadata={
        "source": "example.txt",
        "page": 1,
        "total_pages": 10
    }
)

# Access properties
print(doc.page_content)
print(doc.metadata["source"])
```

### Enhanced Document Schema

Extended document with additional processing information:

```python
from haive.core.engine.document.base.schema import EnhancedDocument

enhanced_doc = EnhancedDocument(
    page_content="Content",
    metadata={...},
    embeddings=[0.1, 0.2, ...],  # Optional embeddings
    chunk_index=0,  # Position in original document
    processing_info={
        "loader": "pdf_pymupdf",
        "chunking_strategy": "paragraph",
        "transformers": ["normalizer", "cleaner"]
    }
)
```

### Document Result Schema

Container for document processing results:

```python
from haive.core.engine.document.base.schema import DocumentResult

result = DocumentResult(
    documents=[doc1, doc2, doc3],
    total_documents=3,
    has_errors=False,
    errors=[],
    metadata={
        "processing_time": 1.23,
        "source_type": "pdf",
        "strategies_used": ["pdf_pymupdf"]
    },
    operation_time=1.23
)
```

## Base Classes

### BaseLoader

Abstract interface for all document loaders:

```python
from haive.core.engine.document.base import BaseLoader
from typing import List, Iterator

class CustomLoader(BaseLoader):
    """Custom document loader implementation."""

    def load(self) -> List[Document]:
        """Load and return all documents."""
        documents = []
        # Implementation
        return documents

    def lazy_load(self) -> Iterator[Document]:
        """Load documents lazily (one at a time)."""
        # Implementation
        yield document

    @property
    def source_type(self) -> str:
        """Return the type of source this loader handles."""
        return "custom"
```

### BaseTextSplitter

Abstract interface for text splitting strategies:

```python
from haive.core.engine.document.base import BaseTextSplitter
from typing import List

class CustomSplitter(BaseTextSplitter):
    """Custom text splitting implementation."""

    def split_text(self, text: str) -> List[str]:
        """Split text into chunks."""
        chunks = []
        # Implementation
        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents preserving metadata."""
        split_docs = []
        for doc in documents:
            chunks = self.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                split_docs.append(Document(
                    page_content=chunk,
                    metadata={
                        **doc.metadata,
                        "chunk_index": i,
                        "chunk_total": len(chunks)
                    }
                ))
        return split_docs
```

### BaseTransformer

Abstract interface for document transformers:

```python
from haive.core.engine.document.base import BaseTransformer

class CustomTransformer(BaseTransformer):
    """Custom document transformer."""

    def transform_document(self, document: Document) -> Document:
        """Transform a single document."""
        # Process content
        transformed_content = self.process(document.page_content)

        return Document(
            page_content=transformed_content,
            metadata={
                **document.metadata,
                "transformed": True
            }
        )

    def transform_documents(self, documents: List[Document]) -> List[Document]:
        """Transform multiple documents."""
        return [self.transform_document(doc) for doc in documents]
```

## Type Definitions

### Common Types

```python
from haive.core.engine.document.base.types import (
    DocumentMetadata,
    ProcessingOptions,
    LoaderOptions,
    ChunkingOptions
)

# Document metadata type
metadata: DocumentMetadata = {
    "source": "file.pdf",
    "page": 1,
    "author": "John Doe",
    "created_at": "2024-01-01"
}

# Processing options
options: ProcessingOptions = {
    "normalize": True,
    "extract_metadata": True,
    "parallel": True
}
```

### Protocols

Type protocols for duck typing:

```python
from haive.core.engine.document.base.protocols import (
    Loadable,
    Splittable,
    Transformable
)

# Any class implementing these methods satisfies the protocol
class MyLoader:
    def load(self) -> List[Document]:
        return []

    def lazy_load(self) -> Iterator[Document]:
        yield Document(page_content="", metadata={})

# Type checking
def process_loader(loader: Loadable):
    documents = loader.load()
    # Process documents
```

## Utility Functions

### Document Manipulation

```python
from haive.core.engine.document.base.utils import (
    merge_documents,
    split_document,
    clone_document,
    update_metadata
)

# Merge multiple documents
merged = merge_documents([doc1, doc2], separator="\n\n")

# Split document at delimiter
parts = split_document(doc, delimiter="---")

# Clone with new metadata
cloned = clone_document(doc, metadata_update={"version": 2})

# Update metadata in place
update_metadata(doc, {"processed": True, "timestamp": "2024-01-01"})
```

### Validation Utilities

```python
from haive.core.engine.document.base.validators import (
    validate_document,
    validate_metadata,
    is_valid_source
)

# Validate document structure
if validate_document(doc):
    print("Document is valid")

# Validate metadata
errors = validate_metadata(metadata, required_fields=["source", "page"])

# Check source validity
if is_valid_source(source_path):
    print("Source is accessible")
```

## Creating Custom Components

### Custom Document Type

```python
from haive.core.engine.document.base.schema import Document
from pydantic import Field

class ResearchDocument(Document):
    """Document with research-specific metadata."""

    # Additional fields
    citations: List[str] = Field(default_factory=list)
    abstract: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)
    doi: Optional[str] = None

    def add_citation(self, citation: str):
        """Add a citation to the document."""
        self.citations.append(citation)

    @property
    def has_citations(self) -> bool:
        """Check if document has citations."""
        return len(self.citations) > 0
```

### Custom Result Type

```python
from haive.core.engine.document.base.schema import DocumentResult
from typing import Dict, Any

class AnalysisResult(DocumentResult):
    """Result with analysis information."""

    # Analysis results
    statistics: Dict[str, Any] = Field(default_factory=dict)
    insights: List[str] = Field(default_factory=list)
    confidence_scores: Dict[str, float] = Field(default_factory=dict)

    def add_insight(self, insight: str, confidence: float = 1.0):
        """Add an analysis insight."""
        self.insights.append(insight)
        self.confidence_scores[insight] = confidence
```

## Error Handling

### Custom Exceptions

```python
from haive.core.engine.document.base.exceptions import (
    DocumentError,
    LoaderError,
    SplitterError,
    TransformerError
)

# Raise specific errors
try:
    loader.load()
except LoaderError as e:
    print(f"Loading failed: {e}")
except DocumentError as e:
    print(f"Document error: {e}")

# Create custom exceptions
class CustomLoaderError(LoaderError):
    """Error specific to custom loader."""
    pass
```

### Error Context

```python
from haive.core.engine.document.base.exceptions import ErrorContext

# Provide detailed error context
try:
    process_document(doc)
except Exception as e:
    context = ErrorContext(
        operation="document_processing",
        source=doc.metadata.get("source"),
        details={"step": "transformation", "transformer": "cleaner"}
    )
    raise DocumentError("Processing failed", context=context) from e
```

## Best Practices

### 1. Type Safety

Always use type hints and validate inputs:

```python
from typing import List, Optional
from haive.core.engine.document.base import Document, BaseLoader

class TypedLoader(BaseLoader):
    def __init__(self, source: str, encoding: str = "utf-8"):
        self.source: str = source
        self.encoding: str = encoding

    def load(self) -> List[Document]:
        # Implementation with guaranteed return type
        return []
```

### 2. Metadata Management

Preserve and extend metadata appropriately:

```python
def process_document(doc: Document) -> Document:
    # Preserve original metadata
    new_metadata = doc.metadata.copy()

    # Add processing information
    new_metadata.update({
        "processed_at": datetime.now().isoformat(),
        "processor_version": "1.0.0"
    })

    return Document(
        page_content=processed_content,
        metadata=new_metadata
    )
```

### 3. Error Handling

Provide informative error messages:

```python
class CustomLoader(BaseLoader):
    def load(self) -> List[Document]:
        try:
            # Loading logic
            pass
        except FileNotFoundError:
            raise LoaderError(
                f"Source file not found: {self.source}",
                source=self.source,
                loader_type=self.__class__.__name__
            )
        except Exception as e:
            raise LoaderError(
                f"Unexpected error during loading: {str(e)}",
                source=self.source,
                original_error=e
            )
```

## Testing Support

### Mock Classes

```python
from haive.core.engine.document.base.testing import (
    MockLoader,
    MockSplitter,
    MockTransformer,
    create_test_document
)

# Create test documents
test_doc = create_test_document(
    content="Test content",
    metadata={"source": "test.txt"}
)

# Use mock components
mock_loader = MockLoader(documents=[test_doc])
loaded = mock_loader.load()

mock_splitter = MockSplitter(chunk_size=100)
chunks = mock_splitter.split_documents(loaded)
```

### Validation Testing

```python
from haive.core.engine.document.base.testing import validate_loader_interface

# Ensure loader implements interface correctly
def test_custom_loader():
    loader = CustomLoader()
    errors = validate_loader_interface(loader)
    assert len(errors) == 0, f"Interface errors: {errors}"
```

## See Also

- [Document Engine Documentation](../README.md)
- [Schema Definitions](./schema.py)
- [Type Definitions](./types.py)
- [Base Class Implementations](./base.py)
