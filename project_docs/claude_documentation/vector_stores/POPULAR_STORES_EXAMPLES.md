# Popular Vector Store Examples

This guide provides detailed examples for the most popular vector stores in the Haive framework.

## Table of Contents

1. [Pinecone - Production Vector Database](#pinecone)
2. [Chroma - Local Development](#chroma)
3. [Weaviate - GraphQL Vector Database](#weaviate)
4. [FAISS - High-Performance Local Search](#faiss)
5. [Qdrant - Cloud-Native Vector Database](#qdrant)
6. [Vectara - Managed Search Platform](#vectara)
7. [OpenSearch - Hybrid Search](#opensearch)
8. [Marqo - Multimodal Search](#marqo)
9. [ClickHouse - Analytics + Vectors](#clickhouse)
10. [Supabase - PostgreSQL with Vectors](#supabase)

## Pinecone

### Basic Setup

```python
from haive.core.engine.vectorstore import PineconeVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig
from langchain_core.documents import Document

# Configure Pinecone
config = PineconeVectorStoreConfig(
    name="pinecone_prod",
    embedding=OpenAIEmbeddingConfig(
        model="text-embedding-3-small",
        dimensions=1536
    ),
    api_key="your-api-key",  # Or use PINECONE_API_KEY env var
    index_name="production-index",
    namespace="documents",
    metric="cosine"
)

# Create vector store
vectorstore = config.instantiate()

# Add documents with metadata
docs = [
    Document(
        page_content="Pinecone is a vector database for production",
        metadata={"source": "docs", "category": "database"}
    ),
    Document(
        page_content="It offers high performance and scalability",
        metadata={"source": "blog", "category": "features"}
    )
]

# Add with IDs for updates
vectorstore.add_documents(docs, ids=["doc1", "doc2"])

# Search with metadata filtering
results = vectorstore.similarity_search(
    "scalable vector database",
    k=5,
    filter={"category": "database"}
)
```

### Advanced Features

```python
# Hybrid search with scores
results_with_scores = vectorstore.similarity_search_with_score(
    "production database",
    k=10
)

# Delete vectors
vectorstore.delete(ids=["doc1"])

# Update vectors (delete + add)
vectorstore.delete(ids=["doc2"])
vectorstore.add_documents([updated_doc], ids=["doc2"])
```

## Chroma

### Local Persistent Store

```python
from haive.core.engine.vectorstore import ChromaVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure with persistence
config = ChromaVectorStoreConfig(
    name="local_chroma",
    embedding=OpenAIEmbeddingConfig(),
    persist_directory="./data/chroma_db",
    collection_name="my_documents",
    collection_metadata={"project": "haive"}
)

vectorstore = config.instantiate()

# Add documents
docs = [
    Document(page_content="Local vector store with Chroma"),
    Document(page_content="Perfect for development and testing")
]
vectorstore.add_documents(docs)

# The data persists between sessions
# Next time you instantiate with same config, data is still there
```

### Memory-Only Mode

```python
# No persist_directory = in-memory only
config = ChromaVectorStoreConfig(
    name="temp_chroma",
    embedding=OpenAIEmbeddingConfig(),
    collection_name="temp_collection"
)
```

## Weaviate

### Basic Setup with GraphQL

```python
from haive.core.engine.vectorstore import WeaviateVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure Weaviate
config = WeaviateVectorStoreConfig(
    name="weaviate_store",
    embedding=OpenAIEmbeddingConfig(),
    weaviate_url="http://localhost:8080",
    index_name="Documents",
    text_key="content",
    api_key="your-api-key"  # Optional for auth
)

vectorstore = config.instantiate()

# Weaviate supports complex queries via GraphQL
# The vectorstore handles this for you
results = vectorstore.similarity_search(
    "AI frameworks",
    k=5,
    where_filter={
        "path": ["category"],
        "operator": "Equal",
        "valueString": "technology"
    }
)
```

### Multimodal with Weaviate

```python
# Weaviate supports multimodal (with proper modules)
config = WeaviateVectorStoreConfig(
    name="multimodal_weaviate",
    embedding=OpenAIEmbeddingConfig(),  # For text
    weaviate_url="http://localhost:8080",
    index_name="MultimodalDocuments"
)
# Additional configuration needed in Weaviate for images
```

## FAISS

### High-Performance Local Search

```python
from haive.core.engine.vectorstore import FAISSVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure FAISS
config = FAISSVectorStoreConfig(
    name="faiss_search",
    embedding=OpenAIEmbeddingConfig(),
    index_path="./data/faiss_index",  # Optional persistence
    index_type="IndexFlatL2",  # Or IndexFlatIP, IndexIVFFlat, etc.
    normalize_L2=True
)

vectorstore = config.instantiate()

# FAISS is extremely fast for similarity search
docs = [Document(page_content=f"Document {i}") for i in range(10000)]
vectorstore.add_documents(docs)

# Fast search even with many documents
results = vectorstore.similarity_search("Document 500", k=10)

# Save index to disk
vectorstore.save_local("./data/faiss_index")

# Load later
from langchain_community.vectorstores import FAISS
loaded = FAISS.load_local(
    "./data/faiss_index",
    embeddings=config.embedding.instantiate()
)
```

## Qdrant

### Cloud-Native Setup

```python
from haive.core.engine.vectorstore import QdrantVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure Qdrant
config = QdrantVectorStoreConfig(
    name="qdrant_store",
    embedding=OpenAIEmbeddingConfig(),
    url="http://localhost:6333",  # Or Qdrant Cloud URL
    collection_name="documents",
    api_key="your-api-key",  # For Qdrant Cloud
    distance="Cosine",
    vector_size=1536
)

vectorstore = config.instantiate()

# Qdrant supports advanced filtering
results = vectorstore.similarity_search(
    "machine learning",
    k=5,
    filter={
        "must": [
            {"key": "metadata.year", "range": {"gte": 2023}},
            {"key": "metadata.category", "match": {"value": "AI"}}
        ]
    }
)
```

## Vectara

### Managed Search Platform

```python
from haive.core.engine.vectorstore import VectaraVectorStoreConfig

# Vectara manages embeddings internally
config = VectaraVectorStoreConfig(
    name="vectara_search",
    vectara_customer_id="123456789",
    vectara_corpus_id="1",
    api_key="your-api-key"
    # No embedding config needed!
)

vectorstore = config.instantiate()

# Add documents - Vectara handles chunking
docs = [
    Document(
        page_content="Long document that Vectara will chunk automatically...",
        metadata={"source": "manual"}
    )
]
vectorstore.add_documents(docs)

# Advanced search with Vectara features
results = vectorstore.similarity_search(
    "search query",
    k=10,
    lambda_val=0.5,  # Hybrid search weight
    n_sentence_context=2,  # Context sentences
    filter="doc.source = 'manual'"  # Metadata filter
)

# Add files directly (Vectara processes them)
file_ids = vectorstore.add_files([
    "document.pdf",
    "report.docx",
    "data.html"
])
```

## OpenSearch

### Hybrid Search Setup

```python
from haive.core.engine.vectorstore import OpenSearchVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure OpenSearch
config = OpenSearchVectorStoreConfig(
    name="opensearch_hybrid",
    embedding=OpenAIEmbeddingConfig(),
    opensearch_url="http://localhost:9200",
    index_name="hybrid_docs",
    username="admin",
    password="admin",
    engine="nmslib",  # or "faiss", "lucene"
    space_type="cosine",
    ef_search=512,  # Higher = more accurate but slower
    ef_construction=512,
    m=16
)

vectorstore = config.instantiate()

# OpenSearch supports hybrid search (keyword + vector)
# This is handled automatically by the similarity_search method
results = vectorstore.similarity_search(
    "python programming tutorials",
    k=10,
    search_type="hybrid"  # Combines BM25 and vector search
)
```

### Amazon OpenSearch Service

```python
from haive.core.engine.vectorstore import AmazonOpenSearchVectorStoreConfig

# AWS managed version
config = AmazonOpenSearchVectorStoreConfig(
    name="aws_opensearch",
    embedding=OpenAIEmbeddingConfig(),
    opensearch_url="https://my-domain.us-east-1.es.amazonaws.com",
    index_name="documents",
    aws_region="us-east-1",
    use_aws_auth=True,  # Uses IAM authentication
    is_aoss=False,  # Set True for serverless
    engine="faiss"
)
```

## Marqo

### Multimodal Search

```python
from haive.core.engine.vectorstore import MarqoVectorStoreConfig
import marqo

# Configure for multimodal
config = MarqoVectorStoreConfig(
    name="marqo_multimodal",
    marqo_url="http://localhost:8882",
    index_name="multimodal_index",
    model="open_clip/ViT-B-32/openai",  # CLIP model
    treat_urls_and_pointers_as_images=True
)

# Create client and vector store
client = marqo.Client(url=config.marqo_url)
vectorstore = config.instantiate(client=client)

# Add multimodal documents
docs = [
    Document(
        page_content="A beautiful sunset over the ocean",
        metadata={
            "image_url": "https://example.com/sunset.jpg",
            "tags": ["nature", "sunset"]
        }
    ),
    Document(
        page_content="Modern architecture with glass facades",
        metadata={
            "image_url": "https://example.com/building.jpg",
            "tags": ["architecture", "modern"]
        }
    )
]
vectorstore.add_documents(docs)

# Search with text
text_results = vectorstore.similarity_search("sunset photography", k=5)

# Weighted search
weighted_results = vectorstore.similarity_search(
    {"sunset": 1.0, "ocean": 0.7, "photography": 0.5},
    k=5
)
```

## ClickHouse

### Analytics + Vector Search

```python
from haive.core.engine.vectorstore import ClickHouseVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure ClickHouse
config = ClickHouseVectorStoreConfig(
    name="clickhouse_analytics",
    embedding=OpenAIEmbeddingConfig(),
    host="clickhouse.example.com",
    port=8443,
    username="default",
    password="password",
    secure=True,
    database="analytics",
    table="document_vectors",
    index_type="annoy",
    index_param=["'L2Distance'", 100],
    metric="euclidean"
)

vectorstore = config.instantiate()

# ClickHouse excels at combining analytics with vector search
# You can run SQL queries on the same data
docs = [
    Document(
        page_content="Sales report Q1 2024",
        metadata={
            "quarter": "Q1",
            "year": 2024,
            "revenue": 1500000,
            "department": "sales"
        }
    )
]
vectorstore.add_documents(docs)

# Vector search with analytics filters
results = vectorstore.similarity_search(
    "quarterly sales performance",
    k=10,
    where="year = 2024 AND revenue > 1000000"
)
```

## Supabase

### PostgreSQL with Vectors

```python
from haive.core.engine.vectorstore import SupabaseVectorStoreConfig
from haive.core.models.embeddings.base import OpenAIEmbeddingConfig

# Configure Supabase
config = SupabaseVectorStoreConfig(
    name="supabase_vectors",
    embedding=OpenAIEmbeddingConfig(),
    supabase_url="https://your-project.supabase.co",
    api_key="your-supabase-key",  # Or SUPABASE_API_KEY env var
    table_name="documents",
    query_name="match_documents"  # Function name for similarity search
)

vectorstore = config.instantiate()

# Supabase uses PostgreSQL with pgvector
docs = [
    Document(
        page_content="Supabase combines PostgreSQL with vector search",
        metadata={"category": "database", "public": True}
    )
]
vectorstore.add_documents(docs)

# Search with RLS (Row Level Security) if configured
results = vectorstore.similarity_search(
    "PostgreSQL vectors",
    k=5,
    filter={"public": True}
)

# Direct SQL queries are also possible through Supabase client
```

## Best Practices by Use Case

### Development & Testing

- **Chroma**: Persistent, easy to use, good for development
- **FAISS**: Fast, local, great for testing algorithms
- **InMemory**: Simple, no dependencies, perfect for unit tests

### Production - Cloud

- **Pinecone**: Fully managed, reliable, easy scaling
- **Weaviate**: Feature-rich, GraphQL, good community
- **Qdrant**: Cloud-native, advanced filtering, high performance

### Production - Self-Hosted

- **OpenSearch**: Mature, hybrid search, AWS compatible
- **Milvus**: Scalable, cloud-native architecture
- **ClickHouse**: When you need analytics + vectors

### Specialized Needs

- **Vectara**: When you want managed NLP and search
- **Marqo**: For multimodal search (text + images)
- **Supabase**: If you're already using Supabase/PostgreSQL

### Performance Considerations

- **FAISS**: Fastest for local similarity search
- **Annoy**: Good for read-heavy workloads
- **ScaNN**: Google's solution for large-scale search

## Common Patterns

### 1. Environment-Based Configuration

```python
import os

# Development
if os.getenv("ENVIRONMENT") == "development":
    config = ChromaVectorStoreConfig(
        name="dev_store",
        embedding=OpenAIEmbeddingConfig(),
        persist_directory="./dev_data"
    )
# Production
else:
    config = PineconeVectorStoreConfig(
        name="prod_store",
        embedding=OpenAIEmbeddingConfig(),
        index_name="production"
    )

vectorstore = config.instantiate()
```

### 2. Fallback Strategy

```python
def create_vectorstore(preferred="pinecone"):
    """Create vector store with fallback options."""
    try:
        if preferred == "pinecone":
            return PineconeVectorStoreConfig(...).instantiate()
    except Exception:
        pass

    # Fallback to Chroma
    return ChromaVectorStoreConfig(...).instantiate()
```

### 3. Batch Processing

```python
# Process large datasets in batches
def add_documents_in_batches(vectorstore, documents, batch_size=100):
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        vectorstore.add_documents(batch)
        print(f"Processed {i + len(batch)}/{len(documents)} documents")
```

This guide covers the most popular vector stores in the Haive framework. Each store has unique strengths, so choose based on your specific requirements for performance, features, and deployment constraints.
