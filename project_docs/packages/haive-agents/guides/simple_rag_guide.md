# SimpleRAG Agent - Dead Simple RAG Pattern

**Version**: 1.0
**Date**: 2025-01-21
**Status**: Production Ready

## 🎯 **Overview**

SimpleRAG is **exactly** what you asked for: a dead simple RAG agent that's literally just:

```python
SimpleRAGAgent = EnhancedMulti([BaseRAGAgent, SimpleAgent], mode=Sequential)
```

**Key Features:**
- **BaseRAGAgent** handles document retrieval
- **SimpleAgent** has built-in `RAG_ANSWER_STANDARD` prompt template
- **Sequential execution** via EnhancedMultiAgent V3
- **Built-in keys**: `{query}` and `{retrieved_documents}` in the prompt
- **Dead simple usage** - just pass documents and go

## 🚀 **Quick Start**

### Method 1: Direct Class (Recommended)

```python
from haive.agents.rag import SimpleRAGAgent
from langchain_core.documents import Document

# Your documents
documents = [
    Document(page_content="Python is a programming language..."),
    Document(page_content="List comprehensions provide...")
]

# Create RAG agent - done!
rag_agent = SimpleRAGAgent.from_documents(documents)

# Use it
result = await rag_agent.arun("What is Python?")
print(result)  # Gets answer using retrieved documents
```

### Method 2: Literal Pattern (What You Asked For)

```python
from haive.agents.rag import create_simple_rag_pattern

# This is literally: EnhancedMulti([BaseRAGAgent, SimpleAgent], Sequential)
rag_agent = create_simple_rag_pattern(documents)

result = await rag_agent.arun("Tell me about list comprehensions")
```

### Method 3: Function Alias (Simplest)

```python
from haive.agents.rag import SimpleRAG

# Even simpler - function call
rag_agent = SimpleRAG(documents)

result = await rag_agent.arun("How does Python work?")
```

## 📋 **The Built-in Prompt Template**

Your SimpleAgent automatically gets the `RAG_ANSWER_STANDARD` prompt with these keys:

```python
# The prompt template automatically has:
{
    "query": "User's question",
    "retrieved_documents": "Documents from BaseRAGAgent"
}
```

**Full Prompt Structure:**
```text
System: You are an expert AI assistant specialized in generating comprehensive,
accurate answers using retrieved documents. Your role is to synthesize information
from multiple sources to provide helpful, truthful, and well-structured responses.

Core Principles:
1. Accuracy First - Only use information from provided documents
2. Source Grounding - Base every claim on the provided documents
3. Comprehensiveness - Address all aspects when information is available
4. Transparency - Be clear about limitations and uncertainties
