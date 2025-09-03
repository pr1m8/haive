# RAG Workflow Examples

## Overview

This directory contains RAG (Retrieval-Augmented Generation) workflow examples that need to be updated to use the latest Haive agent versions.

## Current Examples

1. **simple_rag.py** - Basic document Q&A using SimpleRAGAgent
2. **agentic_rag.py** - Advanced multi-agent RAG system

## TODO: Update to Latest Agent Versions

These examples need to be rewritten to use:

- **EnhancedMultiAgentV4** - For multi-agent coordination
- **ReactAgentV4** - For reasoning with tools
- **SimpleAgentV3** - For structured outputs
- **Enhanced Agent Base** - With hooks and recompilation

### Planned Updates

1. **Simple RAG v2**:
   - Use ReactAgentV4 for retrieval reasoning
   - SimpleAgentV3 for answer generation
   - Compose with EnhancedMultiAgentV4

2. **Agentic RAG v2**:
   - Leverage enhanced agent base features
   - Use hooks for document grading
   - Implement recompilation for dynamic tool addition
   - Full async/await patterns

3. **Test Requirements**:
   - Real vector stores (no mocks)
   - Actual document processing
   - Performance benchmarks
   - Multi-agent state management

## Running Current Examples

```bash
# Simple RAG
poetry run python simple_rag.py

# Agentic RAG
poetry run python agentic_rag.py
```

## Notes

- Current examples use placeholder imports that may need adjustment
- Focus on real component testing when updating
- Ensure compatibility with latest MetaStateSchema patterns
