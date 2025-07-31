# Retriever Implementation Memory & Methodology

## 🎯 Successfully Implemented 43 Retrievers

### Key Patterns Learned

1. **Configuration Pattern**
   - All retrievers extend `BaseRetrieverConfig`
   - Use `@BaseRetrieverConfig.register(RetrieverType.NAME)` decorator
   - Implement `instantiate()` method that returns the actual retriever
   - Use `SecureConfigMixin` for API-based retrievers

2. **Naming Convention**
   - Always use `*Config.py` suffix (e.g., `BM25RetrieverConfig.py`)
   - Class names follow pattern: `{Name}RetrieverConfig`
   - Keep consistent with RetrieverType enum entries

3. **Required Methods**

   ```python
   def get_input_fields(self) -> Dict[str, Tuple[Type, Any]]
   def get_output_fields(self) -> Dict[str, Tuple[Type, Any]]
   def instantiate(self)
   ```

4. **Field Validation**
   - Use Pydantic Field() with proper constraints
   - Add descriptive help text for all fields
   - Set sensible defaults where appropriate

### Implementation Categories

1. **Sparse/Classical** (4): BM25, TF-IDF, KNN, SVM
2. **API-based** (13): You, AskNews, Arxiv, PubMed, Wikipedia, etc.
3. **Cloud/Enterprise** (5): Kendra, Bedrock, Google Vertex AI, etc.
4. **Vector Database** (9): Pinecone, Weaviate, Qdrant, Milvus, etc.
5. **Framework/Advanced** (12): Ensemble, MultiQuery, Compression, etc.

### Common Pitfalls Avoided

1. **Import Issues**
   - Always lazy import in `instantiate()` method
   - Provide helpful error messages for missing dependencies
   - Check imports match pyproject.toml extras

2. **SecureConfigMixin Usage**
   - Field must be named `api_key` (not `password`, `token`, etc.)
   - Include `provider` field for key resolution
   - Use `get_api_key()` method in instantiate()

3. **Configuration Objects**
   - When retriever needs LLM, use `llm: AugLLMConfig`
   - When needs embeddings, use `embedding: BaseEmbeddingConfig`
   - When needs vector store, use `vectorstore: VectorStoreConfig`
   - Always call `.instantiate()` on these configs

### Testing Approach

```python
# Basic instantiation test pattern
config = RetrieverConfig(
    name="test",
    # required fields
)
retriever = config.instantiate()
assert retriever is not None
```

### File Organization

```
packages/haive-core/src/haive/core/engine/retriever/
├── retriever.py          # BaseRetrieverConfig
├── types.py             # RetrieverType enum
└── providers/
    ├── __init__.py
    ├── BM25RetrieverConfig.py
    ├── ...
    └── ZepRetrieverConfig.py
```

### Cleanup Process

1. Identified duplicates by normalizing names
2. Kept \*Config.py files over non-Config versions
3. Chose implementations with better validation/features
4. Removed 8 duplicate files
5. Verified all 43 remaining retrievers work

## Vector Store Engine Implementation Plan

Based on retriever experience, for vector stores:

1. **Base Pattern**
   - Create `BaseVectorStoreConfig` in `engine/vectorstore/vectorstore.py`
   - Add registration decorator pattern
   - Create `VectorStoreType` enum in `types.py`

2. **Categories to Implement**
   - **Open Source**: Chroma, FAISS, Qdrant, Weaviate, Milvus
   - **Cloud/Managed**: Pinecone, AWS OpenSearch, Azure Search
   - **Specialized**: Cassandra, ScaNN, Annoy, DocArray
   - **In-Memory**: SimpleVectorStore, SKLearnVectorStore

3. **Common Fields**
   - `embedding: BaseEmbeddingConfig` (required)
   - `collection_name: str`
   - `distance_metric: str`
   - API keys via SecureConfigMixin where needed

4. **Testing Strategy**
   - Create shared fixtures with sample embeddings
   - Test instantiation and basic operations
   - Verify configuration validation

This methodology ensures consistency and quality across all implementations.
