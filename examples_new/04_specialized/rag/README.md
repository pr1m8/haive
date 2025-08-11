# RAG (Retrieval-Augmented Generation) Examples

Build knowledge-enhanced AI systems that combine the power of large language models with specific document collections and databases.

## Purpose

RAG systems solve the fundamental problem of LLMs having limited or outdated knowledge by dynamically retrieving relevant information from external sources. These examples show how to build production-ready RAG systems with Haive.

## Prerequisites

- Understanding of vector embeddings and similarity search
- Basic knowledge of document processing
- Familiarity with databases (vector databases preferred)
- Understanding of single and multi-agent patterns

## Examples

### Basic RAG

#### `simple_rag.py`

**Your first RAG system**

- Document ingestion and embedding
- Basic vector similarity search
- Simple question-answering pattern
- In-memory vector store

#### `rag_with_sources.py`

**RAG with source attribution**

- Track document sources
- Provide citation information
- Handle multiple document types
- Source relevance scoring

#### `multi_document_rag.py`

**Handle multiple document collections**

- Separate vector stores by topic
- Collection-specific search strategies
- Cross-collection synthesis
- Dynamic collection selection

### Advanced RAG

#### `hybrid_search_rag.py`

**Combine vector and keyword search**

- Dense and sparse retrieval
- Result fusion strategies
- Query analysis and routing
- Performance optimization

#### `contextual_rag.py`

**Context-aware retrieval**

- Conversation-aware search
- Context expansion techniques
- Temporal relevance weighting
- Personalized retrieval

#### `multi_agent_rag.py`

**Collaborative RAG system**

- Specialized retrieval agents
- Cross-agent result synthesis
- Quality validation pipeline
- Distributed document processing

### Production RAG

#### `streaming_rag.py`

**Real-time document processing**

- Incremental index updates
- Live document monitoring
- Streaming response generation
- Change detection and reindexing

#### `enterprise_rag.py`

**Enterprise-grade RAG system**

- Multi-user access control
- Document security and permissions
- Audit logging and compliance
- Performance monitoring

#### `rag_evaluation.py`

**RAG system evaluation and testing**

- Retrieval quality metrics
- End-to-end evaluation
- A/B testing frameworks
- Performance benchmarking

## Key Components

### Document Processing Pipeline

```python
from haive.agents.rag.base import BaseRAGAgent
from haive.core.memory import VectorStoreMemory

# Document ingestion and processing
rag_agent = BaseRAGAgent(
    name="knowledge_base",
    vector_store=ChromaVectorStore(),
    embedding_model="sentence-transformers/all-MiniLM-L6-v2",
    chunk_size=1000,
    chunk_overlap=200
)

# Process documents
documents = load_documents("./knowledge_base/")
rag_agent.ingest_documents(documents)
```

### Query Processing

```python
from haive.agents.rag.simple import SimpleRAGAgent

# Create RAG system
rag_system = SimpleRAGAgent(
    name="qa_system",
    retrieval_k=5,  # Top 5 documents
    score_threshold=0.7  # Minimum relevance
)

# Query with context
result = await rag_system.arun(
    "What are the main benefits of renewable energy?",
    context={"domain": "environmental_science"}
)
```

### Multi-Agent RAG

```python
# Specialized agents for different aspects
research_rag = BaseRAGAgent(
    name="research_papers",
    vector_store=research_store
)

policy_rag = BaseRAGAgent(
    name="policy_documents",
    vector_store=policy_store
)

news_rag = BaseRAGAgent(
    name="recent_news",
    vector_store=news_store
)

# Synthesis agent combines results
synthesis_agent = SimpleAgent(
    name="synthesizer",
    system_message="Combine information from multiple sources"
)

# Multi-agent RAG workflow
comprehensive_rag = EnhancedMultiAgentV4([
    research_rag,
    policy_rag,
    news_rag,
    synthesis_agent
], mode="parallel_then_sequential")
```

## Running Examples

```bash
# Basic RAG patterns
poetry run python examples_new/04_specialized/rag/simple_rag.py
poetry run python examples_new/04_specialized/rag/rag_with_sources.py

# Advanced techniques
poetry run python examples_new/04_specialized/rag/hybrid_search_rag.py
poetry run python examples_new/04_specialized/rag/contextual_rag.py

# Production systems
poetry run python examples_new/04_specialized/rag/enterprise_rag.py
```

## Architecture Patterns

### Simple RAG Architecture

```
User Query → Embedding → Vector Search → Context + Query → LLM → Response
```

### Advanced RAG Architecture

```
User Query → Query Analysis → Multi-Source Retrieval → Result Fusion →
Context Assembly → LLM Generation → Post-Processing → Response
```

### Multi-Agent RAG Architecture

```
User Query → Query Router → Parallel Agents → Result Aggregation →
Synthesis Agent → Validation Agent → Final Response
```

## Vector Database Options

### ChromaDB (Recommended for Development)

```python
from langchain_community.vectorstores import Chroma

vector_store = Chroma(
    collection_name="knowledge_base",
    embedding_function=embedding_model,
    persist_directory="./vector_db"
)
```

### Pinecone (Recommended for Production)

```python
import pinecone
from langchain_community.vectorstores import Pinecone

pinecone.init(api_key="your-key", environment="us-west1-gcp")
vector_store = Pinecone.from_documents(
    documents, embedding_model, index_name="knowledge-base"
)
```

### PostgreSQL with pgvector (Self-hosted)

```python
from langchain_community.vectorstores import PGVector

vector_store = PGVector(
    collection_name="documents",
    connection_string="postgresql://user:pass@localhost/db",
    embedding_function=embedding_model
)
```

## Optimization Strategies

### Retrieval Optimization

1. **Embedding Model Selection**
   - General: `all-MiniLM-L6-v2` (fast, decent quality)
   - High Quality: `all-mpnet-base-v2` (slower, better quality)
   - Multilingual: `multilingual-e5-large`

2. **Chunking Strategies**

   ```python
   # Semantic chunking
   chunks = semantic_chunker.split_documents(documents)

   # Fixed-size chunking with overlap
   chunks = text_splitter.split_documents(
       documents,
       chunk_size=1000,
       chunk_overlap=200
   )
   ```

3. **Query Enhancement**

   ```python
   # Query expansion
   expanded_query = query_expander.expand(user_query)

   # Multi-query retrieval
   queries = query_generator.generate_variants(user_query)
   ```

### Generation Optimization

1. **Context Management**

   ```python
   # Limit context size
   relevant_docs = retriever.get_relevant_documents(
       query, k=5, max_tokens=2000
   )
   ```

2. **Response Streaming**
   ```python
   async for chunk in rag_agent.astream(query):
       yield chunk
   ```

## Common Use Cases

### Knowledge Base QA

```python
# Company knowledge base
kb_rag = SimpleRAGAgent(
    name="company_kb",
    documents=["policies/", "procedures/", "faqs/"],
    system_message="Answer based on company documentation"
)
```

### Research Assistant

```python
# Academic research assistant
research_rag = MultiAgentRAG([
    PaperRetrievalAgent(),
    CitationAgent(),
    SummaryAgent()
])
```

### Customer Support

```python
# Support ticket system with RAG
support_rag = ContextualRAG(
    knowledge_base=support_docs,
    user_context=customer_history,
    escalation_rules=escalation_config
)
```

### Legal Document Analysis

```python
# Legal document assistant
legal_rag = EnterpriseRAG(
    documents=legal_corpus,
    access_control=user_permissions,
    audit_logging=True,
    compliance_mode="legal"
)
```

## Performance Metrics

### Retrieval Quality

- **Precision@K**: Relevant documents in top K results
- **Recall@K**: Fraction of relevant documents retrieved
- **MRR (Mean Reciprocal Rank)**: Average reciprocal rank of first relevant result

### Generation Quality

- **Faithfulness**: Generated answer matches retrieved context
- **Answer Relevance**: Answer addresses the question
- **Context Relevance**: Retrieved context is relevant to question

### System Performance

- **Query Latency**: End-to-end response time
- **Throughput**: Queries per second
- **Index Size**: Storage requirements
- **Update Latency**: Time to index new documents

## Best Practices

### Document Preparation

1. **Clean Data**: Remove noise, standardize format
2. **Metadata**: Include source, date, author, topic tags
3. **Structure**: Maintain document hierarchy and relationships
4. **Version Control**: Track document versions and updates

### Retrieval Strategy

1. **Hybrid Search**: Combine dense and sparse retrieval
2. **Reranking**: Use cross-encoder for final ranking
3. **Filtering**: Apply metadata filters before vector search
4. **Caching**: Cache frequent queries and embeddings

### Quality Assurance

1. **Evaluation Pipeline**: Automated quality testing
2. **Human Feedback**: Collect user ratings and corrections
3. **A/B Testing**: Compare different configurations
4. **Monitoring**: Track performance metrics continuously

## Common Challenges

### Retrieval Issues

- **Poor Chunk Quality**: Optimize chunking strategy
- **Embedding Mismatch**: Align query and document embeddings
- **Context Length**: Balance context size vs. relevance

### Generation Issues

- **Hallucination**: Strong source grounding, fact verification
- **Inconsistency**: Standardize response formats
- **Bias**: Diverse training data, bias detection

### Scale Issues

- **Index Size**: Efficient vector storage and compression
- **Update Frequency**: Incremental indexing strategies
- **Query Load**: Caching and load balancing

## Troubleshooting

### Low Retrieval Quality

1. Check embedding model alignment with domain
2. Optimize chunking parameters
3. Tune similarity thresholds
4. Add query preprocessing

### Slow Performance

1. Optimize vector database configuration
2. Implement result caching
3. Use approximate search algorithms
4. Consider embedding dimensionality reduction

### Poor Answer Quality

1. Improve context selection and ranking
2. Optimize prompt engineering
3. Add answer validation steps
4. Implement confidence scoring

## Next Steps

1. **[Planning Agents](../planning/)** - Add task planning to RAG systems
2. **[Business Applications](../business/)** - Enterprise RAG deployments
3. **[Advanced Examples](../../05_advanced/)** - Custom RAG architectures

## Resources

- [LangChain Retrieval Guide](https://python.langchain.com/docs/modules/data_connection/)
- [Vector Database Comparison](https://github.com/vector-databases/awesome-vector-databases)
- [RAG Papers and Research](https://github.com/hymie122/RAG-Survey)
- [Evaluation Frameworks](https://github.com/explodinggradients/ragas)
