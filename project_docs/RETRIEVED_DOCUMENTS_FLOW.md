# Retrieved Documents Flow in SimpleRAG V3

**Date**: 2025-01-21
**Topic**: How "retrieved_documents" are passed between agents

## Overview

In SimpleRAG V3, documents retrieved by the RetrieverAgent are passed to the SimpleAnswerAgent through a structured dictionary. The system handles both "documents" and "retrieved_documents" field names for compatibility.

## Document Flow

### 1. RetrieverAgent Output Structure

```python
# RetrieverAgent returns this structure:
{
    "query": "original user query",
    "documents": [Document, Document, ...],  # List of retrieved documents
    "metadata": {
        "retrieval_method": "similarity_search",
        "score_threshold": 0.5,
        "num_documents": 3,
        "search_time": 0.123
    }
}
```

### 2. Document Field Compatibility

The RetrieverAgent's `_extract_documents()` method handles multiple formats:

```python
def _extract_documents(self, retrieval_result: Any) -> List[Document]:
    """Extract documents from various result formats."""
    if isinstance(retrieval_result, dict):
        # Handles both field names
        if "documents" in retrieval_result:
            return retrieval_result["documents"]
        if "retrieved_documents" in retrieval_result:
            return retrieval_result["retrieved_documents"]
```

So whether the vector store returns "documents" or "retrieved_documents", the RetrieverAgent normalizes it to "documents" in its output.

### 3. SimpleAnswerAgent Input Processing

The SimpleAnswerAgent's `_parse_retriever_input()` method extracts the documents:

```python
def _parse_retriever_input(self, input_data: Any) -> Dict[str, Any]:
    """Parse input from RetrieverAgent or direct query."""
    if isinstance(input_data, dict):
        # Input from RetrieverAgent
        return {
            "query": input_data.get("query", ""),
            "documents": input_data.get("documents", []),  # Extracts documents
            "metadata": input_data.get("metadata", {}),
        }
```

### 4. Document Context Building

SimpleAnswerAgent then builds context from the documents:

```python
def _build_context_from_documents(
    self, documents: List[Document], query: str, debug: bool = False
) -> Dict[str, Any]:
    """Build formatted context from retrieved documents."""
    # Process each document
    for i, doc in enumerate(documents):
        content = doc.page_content.strip()
        source = doc.metadata.get("source", f"Document {i+1}")

        # Format with citations if enabled
        if self.include_citations:
            if self.citation_style == "inline":
                doc_text = f"[Source: {source}]\n{content}"
        # ... builds context
```

## Complete Flow Diagram

```
User Query: "What is machine learning?"
    ↓
RetrieverAgent
    ├─ Searches vector store
    ├─ Vector store returns:
    │   - "documents" OR "retrieved_documents"
    ├─ Normalizes to "documents" field
    └─ Returns: {
          "query": "What is machine learning?",
          "documents": [
              Document(page_content="ML is...", metadata={...}),
              Document(page_content="AI subset...", metadata={...})
          ],
          "metadata": {...}
        }
    ↓
SimpleAnswerAgent
    ├─ Receives RetrieverAgent output
    ├─ Extracts "documents" field
    ├─ Builds context from documents
    ├─ Formats prompt: "Based on the following documents..."
    ├─ Sends to LLM
    └─ Returns: "Machine learning is... [Source: AI Basics Guide]"
```

## Key Points

1. **Field Name Flexibility**: The system handles both "documents" and "retrieved_documents"
2. **Normalization**: RetrieverAgent always outputs "documents" (not "retrieved_documents")
3. **Type Safety**: Documents are passed as List[Document] objects
4. **Metadata Preservation**: Document metadata flows through the entire pipeline
5. **Citation Tracking**: Sources are preserved for citation generation

## Example Document Object

```python
Document(
    page_content="Machine learning is a subset of artificial intelligence...",
    metadata={
        "source": "AI Basics Guide",
        "page": 1,
        "score": 0.89,  # Similarity score from vector store
        "retrieval_agent": "my_rag_retriever",
        "retrieval_timestamp": 1234567890.123,
        "quality_score": 0.95  # If quality scoring enabled
    }
)
```

## Testing Document Flow

To test the document flow:

```python
# 1. Create RetrieverAgent output
retriever_output = {
    "query": "test query",
    "documents": [Document(...)],  # Your retrieved docs
    "metadata": {}
}

# 2. Pass to SimpleAnswerAgent
answer_agent = SimpleAnswerAgent(...)
result = await answer_agent.arun(retriever_output)

# 3. Result includes answer with citations from documents
```

## Summary

The "retrieved_documents" you mentioned are:

1. Retrieved by the vector store (may be called "documents" or "retrieved_documents")
2. Normalized to "documents" by RetrieverAgent
3. Passed to SimpleAnswerAgent in the output dictionary
4. Extracted and processed to build context
5. Used to generate the final answer with citations

This design ensures compatibility with different vector store implementations while maintaining a clean interface between agents.
