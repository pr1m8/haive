# Vector Stores Quick Reference

## Complete List (27 Stores)

| Store                 | Type        | Auth       | Built-in Embeddings | Best For                         |
| --------------------- | ----------- | ---------- | ------------------- | -------------------------------- |
| **Chroma**            | Open Source | None       | No                  | Local development, persistence   |
| **FAISS**             | Open Source | None       | No                  | High-performance local search    |
| **Milvus**            | Open Source | Optional   | No                  | Scalable production deployments  |
| **Qdrant**            | Open Source | API Key\*  | No                  | Cloud-native, advanced filtering |
| **Weaviate**          | Open Source | API Key\*  | No                  | GraphQL queries, multimodal      |
| **Pinecone**          | Managed     | API Key    | No                  | Production SaaS, easy scaling    |
| **Zilliz**            | Managed     | API Key    | No                  | Managed Milvus cloud             |
| **MongoDB Atlas**     | Managed     | Connection | No                  | Existing MongoDB users           |
| **Azure Search**      | Managed     | API Key    | No                  | Azure ecosystem integration      |
| **Vectara**           | Managed     | API Key    | Yes                 | NLP features, auto-chunking      |
| **Marqo**             | Managed     | Optional   | Yes                 | Multimodal search                |
| **PGVector**          | Database    | Connection | No                  | PostgreSQL users                 |
| **Supabase**          | Database    | API Key    | No                  | Supabase ecosystem               |
| **ClickHouse**        | Database    | Password\* | No                  | Analytics + vectors              |
| **Cassandra**         | Database    | Password\* | No                  | Distributed NoSQL                |
| **Elasticsearch**     | Search      | Password\* | No                  | Full-text + vector search        |
| **Typesense**         | Search      | API Key    | No                  | Typo-tolerant search             |
| **OpenSearch**        | Search      | Password\* | No                  | Open-source Elasticsearch        |
| **Amazon OpenSearch** | Search      | AWS IAM    | No                  | AWS managed OpenSearch           |
| **Redis**             | Cache       | Password\* | No                  | Caching + vectors                |
| **InMemory**          | Cache       | None       | No                  | Testing, temporary storage       |
| **LanceDB**           | Specialized | API Key\*  | No                  | Serverless, Arrow format         |
| **DocArray**          | Specialized | None       | No                  | Document-oriented                |
| **Annoy**             | Specialized | None       | No                  | Read-heavy workloads             |
| **USearch**           | Specialized | None       | No                  | High-performance similarity      |
| **SKLearn**           | Specialized | None       | No                  | ML integration                   |
| **Neo4j**             | Graph       | Password   | No                  | Graph + vector search            |

\*Optional authentication

## Quick Setup Examples

### Minimal Configuration (No Auth)

```python
# Chroma
config = ChromaVectorStoreConfig(
    name="my_store",
    embedding=OpenAIEmbeddingConfig()
)

# FAISS
config = FAISSVectorStoreConfig(
    name="my_store",
    embedding=OpenAIEmbeddingConfig()
)

# InMemory
config = InMemoryVectorStoreConfig(
    name="my_store",
    embedding=OpenAIEmbeddingConfig()
)
```

### With API Key (SecureConfigMixin)

```python
# Pinecone
config = PineconeVectorStoreConfig(
    name="my_store",
    embedding=OpenAIEmbeddingConfig(),
    api_key="...",  # or PINECONE_API_KEY env
    index_name="my-index"
)

# Weaviate
config = WeaviateVectorStoreConfig(
    name="my_store",
    embedding=OpenAIEmbeddingConfig(),
    weaviate_url="http://localhost:8080",
    api_key="..."  # or WEAVIATE_API_KEY env
)
```

### No External Embeddings Needed

```python
# Vectara
config = VectaraVectorStoreConfig(
    name="my_store",
    vectara_customer_id="123",
    vectara_corpus_id="1",
    api_key="..."
)

# Marqo
config = MarqoVectorStoreConfig(
    name="my_store",
    marqo_url="http://localhost:8882",
    index_name="docs",
    model="hf/all_datasets_v4_MiniLM-L6"
)
```

## Environment Variables

```bash
# API Keys (auto-resolved if not provided)
PINECONE_API_KEY=...
WEAVIATE_API_KEY=...
QDRANT_API_KEY=...
AZURE_SEARCH_API_KEY=...
SUPABASE_API_KEY=...
TYPESENSE_API_KEY=...
VECTARA_API_KEY=...
ZILLIZ_API_KEY=...
LANCEDB_API_KEY=...

# Vectara specific
VECTARA_CUSTOMER_ID=...
VECTARA_CORPUS_ID=...

# Database passwords
CLICKHOUSE_PASSWORD=...
NEO4J_PASSWORD=...
OPENSEARCH_PASSWORD=...

# Connection strings
POSTGRES_CONNECTION_STRING=...
REDIS_URL=...

# AWS
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
```

## Decision Matrix

### By Deployment Type

- **Local Development**: Chroma, FAISS, InMemory
- **Self-Hosted**: Milvus, Weaviate, OpenSearch, ClickHouse
- **Fully Managed**: Pinecone, Vectara, Zilliz, Azure Search
- **Serverless**: LanceDB, Upstash (coming soon)

### By Features

- **Multimodal**: Marqo, Weaviate
- **Hybrid Search**: OpenSearch, Elasticsearch, Vectara
- **Advanced Filtering**: Qdrant, MongoDB Atlas, Neo4j
- **Built-in NLP**: Vectara
- **Analytics**: ClickHouse, Elasticsearch

### By Scale

- **Small (<1M vectors)**: Chroma, FAISS, Redis
- **Medium (1M-100M)**: Pinecone, Weaviate, Qdrant
- **Large (100M+)**: Milvus, Elasticsearch, ClickHouse
- **Unlimited**: Vectara, Azure Search (managed)

### By Performance

- **Fastest Local**: FAISS, Annoy, USearch
- **Fastest Cloud**: Pinecone, Qdrant
- **Best Latency**: Redis, InMemory
- **Best Throughput**: Milvus, ClickHouse

## Common Patterns

### 1. Development to Production

```python
# Development
dev_config = ChromaVectorStoreConfig(
    name="dev",
    embedding=embedding,
    persist_directory="./dev_db"
)

# Staging
staging_config = QdrantVectorStoreConfig(
    name="staging",
    embedding=embedding,
    url="http://qdrant-staging:6333"
)

# Production
prod_config = PineconeVectorStoreConfig(
    name="prod",
    embedding=embedding,
    index_name="production"
)
```

### 2. Multi-Store Strategy

```python
# Fast cache
cache = RedisVectorStoreConfig(...)

# Main store
main = PineconeVectorStoreConfig(...)

# Archive
archive = ClickHouseVectorStoreConfig(...)
```

### 3. Fallback Chain

```python
stores = [
    ("pinecone", PineconeVectorStoreConfig),
    ("weaviate", WeaviateVectorStoreConfig),
    ("chroma", ChromaVectorStoreConfig),
]

for name, ConfigClass in stores:
    try:
        return ConfigClass(...).instantiate()
    except Exception:
        continue
```

## Performance Tips

1. **Batch Operations**: Add documents in batches of 100-1000
2. **Index Selection**: Choose appropriate index type (IVF, HNSW, etc.)
3. **Embedding Dimensions**: Use smaller dimensions when possible
4. **Distance Metrics**: Cosine for normalized, L2 for Euclidean
5. **Caching**: Use Redis/InMemory for frequently accessed data

## Migration Guide

### From Raw LangChain

```python
# Before (LangChain)
from langchain_community.vectorstores import Chroma
vectorstore = Chroma(
    embedding_function=embeddings,
    persist_directory="./db"
)

# After (Haive)
from haive.core.engine.vectorstore import ChromaVectorStoreConfig
config = ChromaVectorStoreConfig(
    name="my_chroma",
    embedding=OpenAIEmbeddingConfig(),
    persist_directory="./db"
)
vectorstore = config.instantiate()
```

### Benefits of Haive Approach

1. Consistent configuration interface
2. Automatic environment variable resolution
3. Built-in validation
4. Easy switching between stores
5. LangGraph compatibility

---

_Last updated with 27 vector store implementations_
