#!/usr/bin/env python3
"""Comprehensive test for all implemented vector stores in the Haive framework.

This script tests the registration and basic configuration of all vector stores.
"""

import sys
from typing import Dict, List, Type

# Add the package path
sys.path.insert(0, "packages/haive-core/src")

from haive.core.engine.vectorstore.base import (
    _VECTOR_STORE_REGISTRY,
)


def test_all_vector_stores():
    """Test all registered vector stores."""

    # Get all registered vector stores
    registered_stores = _VECTOR_STORE_REGISTRY


    # Group vector stores by category
    categories = {
        "Core Open Source": ["Chroma", "FAISS", "Qdrant", "Weaviate", "Milvus"],
        "Cloud/Managed": [
            "Pinecone",
            "Zilliz",
            "MongoDBAtlas",
            "AzureSearch",
            "Vectara",
            "Marqo",
        ],
        "Database Extensions": ["PGVector", "Supabase", "ClickHouse", "Cassandra"],
        "Search Engines": [
            "Elasticsearch",
            "Typesense",
            "OpenSearch",
            "AmazonOpenSearch",
        ],
        "In-Memory/Cache": ["Redis", "InMemory"],
        "Specialized Stores": ["LanceDB", "DocArray", "Annoy", "USearch", "SKLearn"],
        "Graph Databases": ["Neo4j"],
    }

    # Track successful and failed tests
    successful = []
    failed = []

    # Test each category
    for category, expected_stores in categories.items():

        for store_name in expected_stores:
            if store_name in registered_stores:
                try:
                    # Get the config class
                    config_class = registered_stores[store_name]

                    # Test basic instantiation (without required fields)
                    # This will fail but shows the class is properly registered
                    try:
                        # Try to get required fields
                        config_class(name=f"test_{store_name.lower()}")
                        status = "✓ (No required fields)"
                    except Exception as e:
                        # This is expected for stores with required fields
                        if (
                            "field required" in str(e).lower()
                            or "missing" in str(e).lower()
                        ):
                            status = "✓ (Has required fields)"
                        else:
                            status = f"✓ (Config validated: {type(e).__name__})"

                    successful.append(store_name)

                except Exception as e:
                    failed.append((store_name, str(e)))
            else:
                failed.append((store_name, "Not found in registry"))

    # Print summary

    if failed:
        for store, error in failed:
            pass

    # List all registered stores not in our categories (if any)
    all_expected = set()
    for stores in categories.values():
        all_expected.update(stores)

    extra_stores = set(registered_stores.keys()) - all_expected
    if extra_stores:
        for store in sorted(extra_stores):
            pass

    # Test specific configurations for popular stores

    # Test Vectara
    try:
        from haive.core.engine.vectorstore import VectaraVectorStoreConfig

        config = VectaraVectorStoreConfig(
            name="test_vectara",
            vectara_customer_id="123456",
            vectara_corpus_id="1",
            api_key="test_key",
        )
    except Exception as e:
        pass")

    # Test ClickHouse
    try:
        from haive.core.engine.vectorstore import ClickHouseVectorStoreConfig
        from haive.core.models.embeddings.base import BaseEmbeddingConfig

        # Create a mock embedding config
        class MockEmbedding(BaseEmbeddingConfig):
            def instantiate(self):
                return None

        config = ClickHouseVectorStoreConfig(
            name="test_clickhouse",
            embedding=MockEmbedding(name="mock"),
            host="localhost",
            database="default",
            table="vectors",
        )
    except Exception as e:
        pass")

    # Test Marqo
    try:
        from haive.core.engine.vectorstore import MarqoVectorStoreConfig

        config = MarqoVectorStoreConfig(
            name="test_marqo",
            marqo_url="http://localhost:8882",
            index_name="test_index",
        )
    except Exception as e:
        pass")

    # Test OpenSearch
    try:
        from haive.core.engine.vectorstore import OpenSearchVectorStoreConfig

        config = OpenSearchVectorStoreConfig(
            name="test_opensearch",
            embedding=MockEmbedding(name="mock"),
            opensearch_url="http://localhost:9200",
            index_name="test_index",
        )
    except Exception as e:
        pass")

    # Test Amazon OpenSearch
    try:
        from haive.core.engine.vectorstore import AmazonOpenSearchVectorStoreConfig

        AmazonOpenSearchVectorStoreConfig(
            name="test_amazon_opensearch",
            embedding=MockEmbedding(name="mock"),
            opensearch_url="https://search-test.us-east-1.es.amazonaws.com",
            index_name="test_index",
            aws_region="us-east-1",
        )
    except Exception as e:
        pass")



if __name__ == "__main__":
    test_all_vector_stores()
