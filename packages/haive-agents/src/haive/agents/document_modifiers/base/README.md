# Base Module - Document Modifiers

Foundation components for document modification agents.

## Overview

The base module provides shared functionality for all document modifier agents in the Haive framework. It defines the core state schema, document handling utilities, and common models that other document processing agents build upon.

This module is essential for:

- Managing collections of documents in agent state
- Providing computed properties for document analysis
- Validating document collections
- Defining extensible base classes for custom implementations

## Key Components

### DocumentModifierState

The primary component is the `DocumentModifierState` class, which provides:

- **Document Management**: Store and manipulate document collections
- **Text Aggregation**: Access combined text from all documents
- **Validation**: Ensure non-empty document collections
- **Extensibility**: Base class for agent-specific states

### Models Submodule

The `models` submodule contains additional type definitions and utilities for document processing operations.

## Installation

This module is part of the `haive-agents` package. Install it using:

```bash
pip install haive-agents
```

## Usage Examples

### Basic Document State Usage

```python
from haive.agents.document_modifiers.base.state import DocumentModifierState
from langchain_core.documents import Document

# Create documents
docs = [
    Document(page_content="First document content"),
    Document(page_content="Second document content"),
    Document(page_content="Third document content")
]

# Initialize state
state = DocumentModifierState.from_documents(docs)

# Access properties
print(f"Document count: {state.num_documents}")
print(f"Combined text length: {len(state.documents_text)}")

# Add metadata
state.name = "research_documents"
state.description = "Documents for research analysis"
```

### Extending DocumentModifierState

```python
from haive.agents.document_modifiers.base.state import DocumentModifierState
from pydantic import Field
from typing import Dict, List

class AnalyzedDocumentState(DocumentModifierState):
    """Extended state with analysis results."""

    # Additional fields
    word_counts: Dict[str, int] = Field(default_factory=dict)
    key_phrases: List[str] = Field(default_factory=list)
    sentiment_scores: List[float] = Field(default_factory=list)

    def analyze_documents(self) -> None:
        """Perform basic analysis on documents."""
        for doc in self.documents:
            words = doc.page_content.split()
            for word in words:
                self.word_counts[word] = self.word_counts.get(word, 0) + 1

    @property
    def average_document_length(self) -> float:
        """Calculate average document length in words."""
        if not self.documents:
            return 0.0
        total_words = sum(len(doc.page_content.split()) for doc in self.documents)
        return total_words / self.num_documents

# Use extended state
state = AnalyzedDocumentState.from_documents(docs)
state.analyze_documents()
print(f"Unique words: {len(state.word_counts)}")
print(f"Avg doc length: {state.average_document_length:.1f} words")
```

### Document Validation

```python
from haive.agents.document_modifiers.base.state import DocumentModifierState
from langchain_core.documents import Document
from pydantic import ValidationError

# Validation prevents empty document collections
try:
    state = DocumentModifierState(documents=[])
except ValidationError as e:
    print("Error:", e)
    # Output: Error: At least one document is required.

# Ensure documents have content
docs_with_metadata = [
    Document(
        page_content="Content here",
        metadata={"source": "file1.txt", "page": 1}
    )
]
state = DocumentModifierState.from_documents(docs_with_metadata)
```

## Integration with Other Agents

The base module is used throughout the document modifiers:

```python
# TNT agents use it for taxonomy generation
from haive.agents.document_modifiers.tnt.state import TaxonomyGenerationState
# Inherits from DocumentModifierState

# Knowledge Graph agents extend it
from haive.agents.document_modifiers.kg.kg_map_merge.state import KnowledgeGraphState
# Builds on DocumentModifierState

# Summarizers use it for document management
from haive.agents.document_modifiers.summarizer.map_branch.state import SummaryState
# Extends DocumentModifierState with summary-specific fields
```

## Best Practices

1. **Always validate documents before processing**

   ```python
   if state.num_documents > 0 and state.documents_text.strip():
       # Safe to process
   ```

2. **Use computed properties for efficiency**

   ```python
   # Good - uses cached computed property
   text = state.documents_text

   # Avoid - recalculates each time
   text = "\n".join([doc.page_content for doc in state.documents])
   ```

3. **Extend rather than modify**
   ```python
   # Create specialized states for different use cases
   class PDFDocumentState(DocumentModifierState):
       page_numbers: List[int] = Field(default_factory=list)
       extracted_images: List[str] = Field(default_factory=list)
   ```

## Common Issues and Solutions

### Issue: Class methods don't work as expected

The `add_document`, `remove_document` methods are incorrectly implemented as class methods. Use instance manipulation instead:

```python
# Don't use these methods:
# state = DocumentModifierState.add_document(doc)  # Broken

# Instead, manipulate documents directly:
state.documents.append(new_doc)
state.documents.extend(new_docs)
state.documents = [d for d in state.documents if d != doc_to_remove]
```

### Issue: Validation errors with empty documents

```python
# Ensure documents have content
docs = [d for d in raw_docs if d.page_content.strip()]
if docs:
    state = DocumentModifierState.from_documents(docs)
else:
    raise ValueError("No valid documents to process")
```

## API Reference

For detailed API documentation, see the [API Reference](../../../../docs/source/api/document_modifiers/base/index.rst).

## See Also

- [`base.models`](./models/): Additional model definitions
- [`haive.core.schema`](../../../core/schema.py): Base StateSchema class
- [Document Modifiers Overview](../README.md): Parent module documentation
