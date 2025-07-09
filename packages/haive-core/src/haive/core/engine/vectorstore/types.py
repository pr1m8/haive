"""Vector store type definitions for the Haive framework.

This module defines the enumeration of supported vector store types.
"""

from enum import Enum


class VectorStoreType(str, Enum):
    """Enumeration of supported vector store types.

    This enum defines all the vector store implementations available in the Haive framework.
    Each type corresponds to a specific vector database or vector storage solution.
    """

    # Open source vector databases
    CHROMA = "Chroma"
    FAISS = "FAISS"
    QDRANT = "Qdrant"
    WEAVIATE = "Weaviate"
    MILVUS = "Milvus"
    LANCEDB = "LanceDB"

    # Cloud/Managed vector databases
    PINECONE = "Pinecone"
    ZILLIZ = "Zilliz"
    MONGODB_ATLAS = "MongoDBAtlas"
    AZURE_SEARCH = "AzureSearch"
    OPENSEARCH = "OpenSearch"
    AMAZON_OPENSEARCH = "AmazonOpenSearch"
    GOOGLE_VERTEX_AI_VECTOR_SEARCH = "GoogleVertexAIVectorSearch"

    # Database extensions
    PGVECTOR = "PGVector"
    SUPABASE = "Supabase"
    CASSANDRA = "Cassandra"
    CLICKHOUSE = "ClickHouse"
    NEO4J = "Neo4j"

    # Search engines with vector capabilities
    ELASTICSEARCH = "Elasticsearch"
    TYPESENSE = "Typesense"
    REDIS = "Redis"

    # Specialized vector stores
    DOCARRAY = "DocArray"
    ANNOY = "Annoy"
    SCANN = "ScaNN"
    HNSW = "HNSW"
    USEARCH = "USearch"

    # In-memory and development
    IN_MEMORY = "InMemory"
    SKLEARN = "SKLearn"

    # Graph databases with vector support
    NEBULA = "Nebula"
    MEMGRAPH = "Memgraph"

    # Other specialized stores
    VECTARA = "Vectara"
    ROCKSET = "Rockset"
    TIGRIS = "Tigris"
    UPSTASH = "Upstash"
    XATA = "Xata"
    YELLOWBRICK = "Yellowbrick"
    MARQO = "Marqo"
    VEARCH = "Vearch"
    ALIBABACLOUD_OPENSEARCH = "AlibabaCloudOpenSearch"
    TENCENT_VECTOR_DB = "TencentVectorDB"
    VERTEX_AI_FEATURE_STORE = "VertexAIFeatureStore"
