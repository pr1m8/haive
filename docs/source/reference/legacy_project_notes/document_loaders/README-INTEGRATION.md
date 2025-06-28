# Document Models and Agent Integration Plan

We have developed a comprehensive document processing system that includes:

1. A modular document state schema with specialized model classes
2. A document agent that follows the Haive agent patterns
3. LangChain integration for document processing
4. Document transformers and splitters with core engine integration

## Current Implementation

The current implementation in `project_notes/document_loaders/` includes:

- `document_state.py`: State schema for document operations
- `document_agent.py`: Agent for document processing
- `document_processors.py`: Integration with core engine transformers and splitters
- `document_models.py`: Comprehensive model classes for documents and related entities
- `modular_models_example.py`: Example of using the modular models
- `runnable_example.py`: Self-contained example that can run without dependencies
- Various example and test files

## Integration Plan

To properly integrate these components into the Haive framework, we should:

1. **Move Core Schema Components to haive-core**
   - Base document models and enums go to `haive-core/src/haive/core/schema/prebuilt/documents/`
   - Document state schema extends the core StateSchema

2. **Move Agent and Processing to haive-prebuilt**
   - Document agent goes to `haive-prebuilt/src/haive/prebuilt/content/`
   - Specialized loaders go to `haive-prebuilt/src/haive/prebuilt/content/loaders/`

3. **Update Engine Components in haive-core**
   - Ensure document engine components in `haive-core/src/haive/core/engine/document/` work with our models
   - Add registry and factory methods for document processing

## Next Steps

1. **Create Core Schema Package**

   ```bash
   mkdir -p haive-core/src/haive/core/schema/prebuilt/documents/
   ```

   - Implement base.py with enums and base models
   - Implement state.py with DocumentState extending StateSchema
   - Add conversion utilities for LangChain integration

2. **Create Prebuilt Package**

   ```bash
   mkdir -p haive-prebuilt/src/haive/prebuilt/content/loaders/
   ```

   - Implement document_agent.py with the agent implementation
   - Implement document_processors.py with transformer and splitter integration
   - Add specialized loaders for different document types

3. **Add Tests**

   ```bash
   mkdir -p haive-core/tests/schema/prebuilt/documents/
   mkdir -p haive-prebuilt/tests/content/loaders/
   ```

   - Implement test_base.py, test_state.py, etc.
   - Add tests for document agent and processors
   - Add tests for specialized loaders

4. **Update Documentation**
   - Create usage examples for document models and agent
   - Add API documentation for the document processing system
   - Include integration examples with other Haive components

## Migration Strategy

1. **Phase 1: Core Schema**
   - Migrate core models to haive-core
   - Update imports and ensure backward compatibility
   - Add tests for core models

2. **Phase 2: Agent Implementation**
   - Migrate agent to haive-prebuilt
   - Update to use core schema models
   - Add tests for agent functionality

3. **Phase 3: Loaders and Processors**
   - Migrate loaders to haive-prebuilt
   - Update processors to integrate with core engine
   - Add specialized loaders for different document types

4. **Phase 4: Examples and Documentation**
   - Create comprehensive examples
   - Document API and usage patterns
   - Add integration examples with other Haive components

## Dependencies

- `haive-core`: For core schema and engine components
- `haive-agents`: For agent base classes and patterns
- `langchain-core`: For LangChain document models
- Various document processing libraries (e.g., PyPDF2, BeautifulSoup)

## Usage Examples

Once integrated, the document processing system will be used like this:

```python
from haive.prebuilt.content import create_document_agent
from haive.core.schema.prebuilt.documents import ChunkingStrategy

# Create a document agent
agent = create_document_agent(
    file_paths=["document1.pdf", "document2.txt"],
    chunking_strategy=ChunkingStrategy.PARAGRAPH
)

# Process documents
agent.process_documents()

# Access processed documents
for doc in agent.state.documents:
    print(f"Document: {doc.source_path}")
    print(f"Content: {doc.content[:100]}...")
    print(f"Chunks: {doc.chunk_count}")
```

## Conclusion

The document models and agent system we've developed provides a powerful foundation for document processing in the Haive framework. By integrating it properly into the haive-core and haive-prebuilt packages, we'll make it available as a reusable component for building document-centric applications and agents.

The modular design, with proper inheritance and LangChain integration, makes it flexible and extensible for various document processing needs.
