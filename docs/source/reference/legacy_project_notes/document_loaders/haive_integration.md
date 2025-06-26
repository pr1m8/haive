# Haive Integration Plan for Document Models

This document outlines the plan for integrating the document models and document processing system into the Haive framework structure.

## Integration Structure

The document models will be integrated in two main locations:

1. **Core Schema Components** - Basic document models in haive-core
2. **Prebuilt Implementation** - Document agent and processing in haive-prebuilt

### Core Schema Components

Location: `haive-core/src/haive/core/schema/prebuilt/documents/`

Files to create:

- `__init__.py` - Package exports
- `base.py` - Base document models and enums
- `metadata.py` - Document metadata models
- `collection.py` - Document collection models
- `state.py` - Document state schema

### Prebuilt Implementation

Location: `haive-prebuilt/src/haive/prebuilt/content/`

Files to create:

- `document_models.py` - Extended document models
- `document_agent.py` - Document agent implementation
- `document_processors.py` - Transformer and splitter adapters
- `loaders/` - Directory for specialized loaders
  - `__init__.py` - Package exports
  - `file_loaders.py` - File document loaders
  - `web_loaders.py` - Web document loaders
  - `pdf_loaders.py` - PDF document loaders
  - `text_loaders.py` - Text document loaders
  - `database_loaders.py` - Database document loaders
- `factories.py` - Factory functions for creating agents and loaders

## Migration Steps

1. **Core Schema Components**

   a. **Base Document Models**
   - Create basic model definitions in `base.py`
   - Include enums for DocumentSourceType, DocumentFormat, ProcessingStage, etc.
   - Implement base document models like BaseDocumentModel, Document, DocumentChunk

   b. **Metadata Models**
   - Move metadata models to `metadata.py`
   - Include DocumentSourceMetadata, MetadataModel, etc.

   c. **Collection Models**
   - Implement DocumentCollection in `collection.py`
   - Add collection utilities and interfaces

   d. **State Schema**
   - Implement DocumentState in `state.py`
   - Ensure it extends StateSchema

2. **Prebuilt Implementation**

   a. **Document Models**
   - Extend core models in `document_models.py`
   - Add specialized document types and functionality

   b. **Document Agent**
   - Implement DocumentAgent in `document_agent.py`
   - Include workflow nodes and graph definition
   - Add factory functions for specialized agents

   c. **Document Processors**
   - Implement transformer and splitter adapters in `document_processors.py`
   - Add integration with core engine components

   d. **Specialized Loaders**
   - Implement file loaders in `loaders/file_loaders.py`
   - Implement web loaders in `loaders/web_loaders.py`
   - Implement other specialized loaders

   e. **Factories**
   - Implement factory functions in `factories.py`
   - Add convenience methods for creating document agents

3. **Engine Integration**

   a. **Engine Configuration**
   - Define engine configurations in `haive-core/src/haive/core/engine/loaders/config.py`
   - Implement registry for loader types

   b. **Engine Implementation**
   - Implement document loader engine in `haive-core/src/haive/core/engine/loaders/engine.py`
   - Add integration with other engine components

## Core Components Overview

The core schema components will include:

```python
# Base models
class BaseDocumentModel(BaseModel):
    """Base model for document-related models."""
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime

class Document(BaseDocumentModel):
    """A document loaded from a source."""
    content: str
    source_path: str
    source_type: DocumentSourceType
    format: DocumentFormat
    metadata: Dict[str, Any]
    chunks: List[DocumentChunk]

class DocumentChunk(BaseDocumentModel):
    """A chunk of a document."""
    content: str
    document_id: str
    chunk_index: int
    metadata: Dict[str, Any]

# State schema
class DocumentState(StateSchema):
    """State schema for document operations."""
    sources: List[DocumentSource]
    documents: List[Document]
    collections: Dict[str, DocumentCollection]
```

## Prebuilt Components Overview

The prebuilt components will include:

```python
# Document agent
class DocumentAgent(Agent):
    """Agent for loading and processing documents."""
    def __init__(self, state_schema: Optional[StateSchema] = None, options: Optional[DocumentAgentOptions] = None):
        # Initialize agent

    def build_graph(self) -> StateGraph:
        # Create workflow graph

    @node
    def analyze_source(self, state: DocumentState) -> DocumentState:
        # Analyze document sources

    @node
    def load_documents(self, state: DocumentState) -> DocumentState:
        # Load documents from sources

    @node
    def chunk_documents(self, state: DocumentState) -> DocumentState:
        # Chunk documents into smaller pieces

# Factory functions
def create_file_document_agent(file_paths: List[str], chunking_strategy: ChunkingStrategy = ChunkingStrategy.FIXED_SIZE) -> DocumentAgent:
    """Create a document agent optimized for file loading."""

def create_web_document_agent(urls: List[str], chunking_strategy: ChunkingStrategy = ChunkingStrategy.PARAGRAPH) -> DocumentAgent:
    """Create a document agent optimized for web loading."""
```

## LangChain Integration

The document models will integrate with LangChain through:

1. **Conversion Methods**
   - `Document.to_langchain()` - Convert to LangChain Document
   - `Document.from_langchain()` - Create from LangChain Document
   - `chunks_to_langchain()` - Convert chunks to LangChain Documents

2. **Collection Utilities**
   - `lc_documents_to_document_collection()` - Create collection from LangChain Documents
   - `collection.to_langchain_documents()` - Convert collection to LangChain Documents

3. **State Utilities**
   - `state.get_all_langchain_documents()` - Get all documents as LangChain Documents
   - `state.get_all_chunks_as_langchain()` - Get all chunks as LangChain Documents

## Implementation Plan

1. **Create Core Schema Components (Week 1)**
   - Implement base models and enums
   - Develop document state schema
   - Add LangChain integration

2. **Implement Prebuilt Components (Week 2)**
   - Develop document agent with workflow
   - Add specialized loaders
   - Implement processors for transformers and splitters

3. **Engine Integration (Week 3)**
   - Create engine configurations
   - Implement registry and factories
   - Add engine implementation

4. **Testing and Documentation (Week 4)**
   - Write comprehensive tests
   - Create usage examples
   - Document API and components

## Usage Examples

The integrated components will be used like this:

```python
# Using the document agent
from haive.prebuilt.content.document_agent import create_file_document_agent
from haive.core.schema.prebuilt.documents.base import ChunkingStrategy

agent = create_file_document_agent(
    file_paths=["document1.txt", "document2.pdf"],
    chunking_strategy=ChunkingStrategy.PARAGRAPH
)

agent.process_documents()

# Using with LangChain
from langchain_core.documents import Document as LCDocument

lc_docs = agent.state.get_all_chunks_as_langchain()

# For RAG pipelines
from langchain_core.retrievers import Retriever
from haive.prebuilt.content.document_processors import DocumentRetriever

retriever = DocumentRetriever(documents=agent.get_documents())
relevant_docs = retriever.get_relevant_documents("What is the main topic?")
```

## Conclusion

This integration plan provides a structured approach to incorporate the document processing system into the Haive framework. By following the Haive architecture patterns and leveraging the existing components, we can create a seamless integration that enhances the framework with powerful document processing capabilities.
