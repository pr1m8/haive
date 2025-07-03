# Haive Agents Overview

This folder contains comprehensive documentation about the haive-agents package, including all document and RAG agent implementations discovered through analysis.

## Contents

- [RAG_AGENTS.md](./RAG_AGENTS.md) - Complete overview of all RAG agent implementations
- [DOCUMENT_AGENTS.md](./DOCUMENT_AGENTS.md) - Document processing agents overview
- [AGENT_ARCHITECTURE.md](./AGENT_ARCHITECTURE.md) - Architecture patterns and base classes
- [IMPLEMENTATION_GUIDE.md](./IMPLEMENTATION_GUIDE.md) - How to implement new agents

## Quick Summary

The haive-agents package contains:

### RAG Agents
- **12+ RAG strategies** implemented in `/packages/haive-agents/src/haive/agents/rag/`
- Multiple implementation styles: Traditional, Chain, and Multi-agent
- Specialized patterns like HyDE, FLARE, Corrective RAG, and more

### Document Agents
- **Document Agent** - Full document processing pipeline (fetch → load → transform → split → annotate → embed → store → retrieve)
- **Document Loader Agent** - Specialized for loading documents from various sources
- **Document Grading Agent** - Evaluates document relevance and quality

### Key Features
- Modular architecture with composable components
- Support for 97+ document types through DocumentEngine
- Integration with vector stores and embeddings
- Multi-agent workflows for complex tasks
- Built on LangGraph for state management

## Package Location
`/home/will/Projects/haive/backend/haive/packages/haive-agents/`