"""
Vector store provider implementations for the Haive framework.

This package contains implementations of vector store providers that extend
the base vector store configuration. Each provider configuration class
extends BaseVectorStoreConfig and provides specific implementation details
for that vector store backend.

The providers are automatically registered when imported, allowing them to be
instantiated by type through the base configuration system.
"""

from .AmazonOpenSearchVectorStoreConfig import AmazonOpenSearchVectorStoreConfig

# Approximate nearest neighbor stores
from .AnnoyVectorStoreConfig import AnnoyVectorStoreConfig

# Cloud/managed vector stores
from .AzureSearchVectorStoreConfig import AzureSearchVectorStoreConfig
from .CassandraVectorStoreConfig import CassandraVectorStoreConfig

# Import all vector store configs to register them
# Core open source vector stores
from .ChromaVectorStoreConfig import ChromaVectorStoreConfig
from .ClickHouseVectorStoreConfig import ClickHouseVectorStoreConfig

# Document-oriented vector stores
from .DocArrayVectorStoreConfig import DocArrayVectorStoreConfig

# Search engines
from .ElasticsearchVectorStoreConfig import ElasticsearchVectorStoreConfig
from .FAISSVectorStoreConfig import FAISSVectorStoreConfig

# Development and testing stores
from .InMemoryVectorStoreConfig import InMemoryVectorStoreConfig

# Columnar vector databases
from .LanceDBVectorStoreConfig import LanceDBVectorStoreConfig
from .MarqoVectorStoreConfig import MarqoVectorStoreConfig
from .MilvusVectorStoreConfig import MilvusVectorStoreConfig
from .MongoDBAtlasVectorStoreConfig import MongoDBAtlasVectorStoreConfig

# Graph databases with vector support
from .Neo4jVectorStoreConfig import Neo4jVectorStoreConfig

# Additional search engines with vector capabilities
from .OpenSearchVectorStoreConfig import OpenSearchVectorStoreConfig

# Database extensions
from .PGVectorStoreConfig import PGVectorStoreConfig
from .PineconeVectorStoreConfig import PineconeVectorStoreConfig
from .QdrantVectorStoreConfig import QdrantVectorStoreConfig

# In-memory databases
from .RedisVectorStoreConfig import RedisVectorStoreConfig

# ML integration stores
from .SKLearnVectorStoreConfig import SKLearnVectorStoreConfig
from .SupabaseVectorStoreConfig import SupabaseVectorStoreConfig

# Search engines with vector capabilities
from .TypesenseVectorStoreConfig import TypesenseVectorStoreConfig
from .USearchVectorStoreConfig import USearchVectorStoreConfig

# Managed vector search platforms
from .VectaraVectorStoreConfig import VectaraVectorStoreConfig
from .WeaviateVectorStoreConfig import WeaviateVectorStoreConfig
from .ZillizVectorStoreConfig import ZillizVectorStoreConfig

__all__ = [
    # Core open source
    "ChromaVectorStoreConfig",
    "FAISSVectorStoreConfig",
    "QdrantVectorStoreConfig",
    "WeaviateVectorStoreConfig",
    "MilvusVectorStoreConfig",
    # Cloud/managed
    "PineconeVectorStoreConfig",
    "ZillizVectorStoreConfig",
    "MongoDBAtlasVectorStoreConfig",
    "AzureSearchVectorStoreConfig",
    # Database extensions
    "PGVectorStoreConfig",
    "SupabaseVectorStoreConfig",
    "ClickHouseVectorStoreConfig",
    # Search engines
    "ElasticsearchVectorStoreConfig",
    # In-memory databases
    "RedisVectorStoreConfig",
    # Columnar vector databases
    "LanceDBVectorStoreConfig",
    # Document-oriented vector stores
    "DocArrayVectorStoreConfig",
    # Approximate nearest neighbor stores
    "AnnoyVectorStoreConfig",
    "USearchVectorStoreConfig",
    # ML integration stores
    "SKLearnVectorStoreConfig",
    # Development and testing stores
    "InMemoryVectorStoreConfig",
    # Search engines with vector capabilities
    "TypesenseVectorStoreConfig",
    # Graph databases with vector support
    "Neo4jVectorStoreConfig",
    "CassandraVectorStoreConfig",
    # Additional search engines with vector capabilities
    "OpenSearchVectorStoreConfig",
    "AmazonOpenSearchVectorStoreConfig",
    # Managed vector search platforms
    "VectaraVectorStoreConfig",
    "MarqoVectorStoreConfig",
]
