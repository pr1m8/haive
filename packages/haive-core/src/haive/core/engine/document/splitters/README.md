# Document Splitters Subsystem

The splitters subsystem provides various strategies for chunking documents into smaller, manageable pieces. It supports multiple splitting algorithms optimized for different use cases and document types.

## Overview

Document splitting (chunking) is crucial for:

- **LLM Processing**: Keeping chunks within token limits
- **Retrieval**: Creating searchable document segments
- **Analysis**: Processing documents in parallel
- **Memory Efficiency**: Working with large documents

## Splitting Strategies

### Fixed Size Chunking

Splits documents into chunks of a specified character count.

**Characteristics:**

- Predictable chunk sizes
- Fast performance
- May break mid-sentence or mid-word
- Best for: General text processing, when exact size matters

**Configuration:**

```python
config = {
    "chunking_strategy": "fixed_size",
    "chunk_size": 1000,
    "chunk_overlap": 200
}
```

### Paragraph Chunking

Splits documents at paragraph boundaries.

**Characteristics:**

- Preserves paragraph integrity
- Variable chunk sizes
- Natural content boundaries
- Best for: Articles, reports, narrative text

**Configuration:**

```python
config = {
    "chunking_strategy": "paragraph",
    "chunk_size": 2000,  # Max size per chunk
    "combine_small": True  # Combine small paragraphs
}
```

### Sentence Chunking

Splits documents at sentence boundaries.

**Characteristics:**

- Preserves complete sentences
- Fine-grained control
- Good for NLP tasks
- Best for: Q&A systems, summarization

**Configuration:**

```python
config = {
    "chunking_strategy": "sentence",
    "sentences_per_chunk": 5,
    "min_chunk_size": 100
}
```

### Recursive Character Splitting

Intelligently splits using multiple separators in order of preference.

**Characteristics:**

- Tries paragraph breaks first, then sentences, then words
- Adaptive to content structure
- Balanced chunk sizes
- Best for: Mixed content, general purpose

**Configuration:**

```python
config = {
    "chunking_strategy": "recursive",
    "chunk_size": 1500,
    "chunk_overlap": 100,
    "separators": ["\n\n", "\n", ". ", " "]
}
```

### Semantic Chunking (Experimental)

Splits based on semantic similarity and topic boundaries.

**Characteristics:**

- Context-aware splitting
- Preserves semantic coherence
- Requires embeddings model
- Best for: Technical documents, knowledge bases

**Configuration:**

```python
config = {
    "chunking_strategy": "semantic",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "similarity_threshold": 0.7
}
```

## Usage Examples

### Basic Usage

```python
from haive.core.engine.document import DocumentEngine

# Create engine with specific chunking
engine = DocumentEngine(config={
    "chunking_strategy": "paragraph",
    "chunk_size": 1000
})

# Process document
result = engine.invoke("document.txt")
print(f"Created {len(result.documents)} chunks")
```

### Advanced Configuration

```python
from haive.core.engine.document.splitters import (
    create_text_splitter,
    ChunkingStrategy
)

# Create custom splitter
splitter = create_text_splitter(
    strategy=ChunkingStrategy.RECURSIVE,
    chunk_size=1500,
    chunk_overlap=200,
    length_function=len,  # Use character count
    keep_separator=True
)

# Split text directly
chunks = splitter.split_text(long_text)
```

### Document-Aware Splitting

```python
# Different strategies for different document types
def get_splitter_for_document(doc_type: str):
    if doc_type == "code":
        return create_text_splitter(
            strategy="recursive",
            separators=["\n\n", "\n", " "],
            chunk_size=2000
        )
    elif doc_type == "chat":
        return create_text_splitter(
            strategy="sentence",
            sentences_per_chunk=10
        )
    else:
        return create_text_splitter(
            strategy="paragraph",
            chunk_size=1500
        )
```

## Configuration Options

### Common Parameters

| Parameter        | Type     | Default | Description                                    |
| ---------------- | -------- | ------- | ---------------------------------------------- |
| chunk_size       | int      | 1000    | Target size for each chunk                     |
| chunk_overlap    | int      | 200     | Number of characters to overlap between chunks |
| length_function  | callable | len     | Function to measure chunk size                 |
| keep_separator   | bool     | True    | Include separators in chunks                   |
| strip_whitespace | bool     | True    | Remove leading/trailing whitespace             |

### Strategy-Specific Parameters

**Fixed Size:**

- `encoding`: Token encoding for precise sizing

**Paragraph:**

- `min_paragraph_size`: Minimum size to consider as paragraph
- `combine_small`: Combine small paragraphs

**Sentence:**

- `sentences_per_chunk`: Number of sentences per chunk
- `language`: Language for sentence detection

**Recursive:**

- `separators`: List of separators to try in order
- `is_separator_regex`: Treat separators as regex

**Semantic:**

- `embedding_model`: Model for semantic similarity
- `similarity_threshold`: Threshold for splitting

## Performance Optimization

### Chunk Size Selection

```python
# For OpenAI GPT models
chunk_size = 2000  # ~500 tokens

# For Anthropic Claude
chunk_size = 4000  # ~1000 tokens

# For embedding models
chunk_size = 500   # Optimal for most embedding models
```

### Overlap Strategies

```python
# Minimal overlap (fast, less context)
chunk_overlap = 0

# Standard overlap (balanced)
chunk_overlap = int(chunk_size * 0.1)  # 10% overlap

# High overlap (better context, more tokens)
chunk_overlap = int(chunk_size * 0.2)  # 20% overlap
```

### Parallel Processing

```python
# Enable parallel chunk processing
engine = DocumentEngine(config={
    "parallel_processing": True,
    "max_workers": 4,
    "chunking_strategy": "recursive",
    "chunk_size": 1000
})
```

## Best Practices

### 1. Choose Strategy by Content Type

| Content Type   | Recommended Strategy | Chunk Size |
| -------------- | -------------------- | ---------- |
| Articles       | Paragraph            | 1000-2000  |
| Code           | Recursive            | 2000-4000  |
| Chat/Dialog    | Sentence             | 500-1000   |
| Technical Docs | Semantic             | 1000-1500  |
| Mixed Content  | Recursive            | 1000-2000  |

### 2. Consider Downstream Tasks

**For Retrieval:**

- Smaller chunks (500-1000 chars)
- Higher overlap (20%)
- Semantic or paragraph splitting

**For Summarization:**

- Larger chunks (2000-4000 chars)
- Lower overlap (10%)
- Paragraph or recursive splitting

**For Q&A:**

- Medium chunks (1000-1500 chars)
- Medium overlap (15%)
- Sentence or semantic splitting

### 3. Handle Edge Cases

```python
# Configure for edge cases
config = {
    "chunking_strategy": "recursive",
    "chunk_size": 1000,
    "chunk_overlap": 200,
    "min_chunk_size": 100,  # Don't create tiny chunks
    "max_chunk_size": 2000,  # Hard limit
    "strip_whitespace": True,
    "keep_separator": True
}
```

## Custom Splitters

### Implementing Custom Splitter

```python
from haive.core.engine.document.splitters.base import BaseTextSplitter
from typing import List

class CustomSplitter(BaseTextSplitter):
    def split_text(self, text: str) -> List[str]:
        # Custom splitting logic
        chunks = []
        # ... your implementation
        return chunks

    def split_documents(self, documents: List[Document]) -> List[Document]:
        # Split and preserve metadata
        split_docs = []
        for doc in documents:
            chunks = self.split_text(doc.page_content)
            for i, chunk in enumerate(chunks):
                split_docs.append(
                    Document(
                        page_content=chunk,
                        metadata={**doc.metadata, "chunk": i}
                    )
                )
        return split_docs
```

### Registering Custom Splitter

```python
from haive.core.engine.document.splitters import register_splitter

@register_splitter("custom_splitter")
class CustomSplitter(BaseTextSplitter):
    # Implementation
    pass

# Use it
engine = DocumentEngine(config={
    "chunking_strategy": "custom_splitter",
    "chunk_size": 1000
})
```

## Troubleshooting

### Common Issues

1. **Chunks Too Large**
   - Reduce chunk_size
   - Use more aggressive splitting strategy
   - Check separator configuration

2. **Losing Context**
   - Increase chunk_overlap
   - Use semantic splitting
   - Consider paragraph boundaries

3. **Poor Split Quality**
   - Adjust separators for content type
   - Try different strategies
   - Preprocess text (normalize whitespace)

### Debug Chunking

```python
# Enable debug logging
import logging
logging.getLogger("haive.splitters").setLevel(logging.DEBUG)

# Inspect chunks
result = engine.invoke("document.txt")
for i, doc in enumerate(result.documents):
    print(f"Chunk {i}: {len(doc.page_content)} chars")
    print(f"Metadata: {doc.metadata}")
    print(f"Preview: {doc.page_content[:100]}...")
```

## See Also

- [Document Engine Documentation](../README.md)
- [Text Splitter Configuration](./config.py)
- [LangChain Splitters Documentation](https://python.langchain.com/docs/modules/data_connection/document_transformers/)
