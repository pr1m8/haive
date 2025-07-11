"""Test vector store configurations."""

import pytest
from langchain_core.documents import Document

from haive.core.engine.vectorstore.base import BaseVectorStoreConfig
from haive.core.engine.vectorstore.types import VectorStoreType
from haive.core.models.embeddings.base import HuggingFaceEmbeddingConfig


@pytest.fixture
def sample_embedding_config():
    """Create a sample embedding configuration."""
    return HuggingFaceEmbeddingConfig(model="sentence-transformers/all-MiniLM-L6-v2")


@pytest.fixture
def sample_documents():
    """Create sample documents for testing."""
    return [
        Document(
            page_content="The quick brown fox jumps over the lazy dog",
            metadata={"id": 1},
        ),
        Document(
            page_content="Machine learning is transforming industries",
            metadata={"id": 2},
        ),
        Document(
            page_content="Vector databases enable semantic search", metadata={"id": 3}
        ),
    ]


def test_chroma_config(sample_embedding_config):
    """Test Chroma vector store configuration."""
    from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import (
        ChromaVectorStoreConfig,
    )

    config = ChromaVectorStoreConfig(
        name="test_chroma",
        embedding=sample_embedding_config,
        collection_name="test_collection",
        persist_directory=None,  # In-memory for testing
        distance_metric="cosine",
    )

    assert config.name == "test_chroma"
    assert config.collection_name == "test_collection"
    assert config.distance_metric == "cosine"
    assert config.engine_type.value == "vector_store"


def test_faiss_config(sample_embedding_config):
    """Test FAISS vector store configuration."""
    from haive.core.engine.vectorstore.providers.FAISSVectorStoreConfig import (
        FAISSVectorStoreConfig,
    )

    config = FAISSVectorStoreConfig(
        name="test_faiss",
        embedding=sample_embedding_config,
        index_type="Flat",
        distance_metric="cosine",
        normalize_l2=True,
    )

    assert config.name == "test_faiss"
    assert config.index_type == "Flat"
    assert config.distance_metric == "cosine"
    assert config.normalize_l2 is True


def test_qdrant_config(sample_embedding_config):
    """Test Qdrant vector store configuration."""
    from haive.core.engine.vectorstore.providers.QdrantVectorStoreConfig import (
        QdrantVectorStoreConfig,
    )

    config = QdrantVectorStoreConfig(
        name="test_qdrant",
        embedding=sample_embedding_config,
        host="localhost",
        port=6333,
        collection_name="test_collection",
        distance_metric="cosine",
    )

    assert config.name == "test_qdrant"
    assert config.host == "localhost"
    assert config.port == 6333
    assert config.distance_metric == "cosine"


def test_weaviate_config(sample_embedding_config):
    """Test Weaviate vector store configuration."""
    from haive.core.engine.vectorstore.providers.WeaviateVectorStoreConfig import (
        WeaviateVectorStoreConfig,
    )

    config = WeaviateVectorStoreConfig(
        name="test_weaviate",
        embedding=sample_embedding_config,
        use_embedded=True,
        index_name="TestDocuments",
        text_key="content",
    )

    assert config.name == "test_weaviate"
    assert config.use_embedded is True
    assert config.index_name == "TestDocuments"
    assert config.text_key == "content"


def test_milvus_config(sample_embedding_config):
    """Test Milvus vector store configuration."""
    from haive.core.engine.vectorstore.providers.MilvusVectorStoreConfig import (
        MilvusVectorStoreConfig,
    )

    config = MilvusVectorStoreConfig(
        name="test_milvus",
        embedding=sample_embedding_config,
        connection_args={"host": "localhost", "port": "19530"},
        collection_name="test_collection",
        consistency_level="Session",
    )

    assert config.name == "test_milvus"
    assert config.connection_args["host"] == "localhost"
    assert config.consistency_level == "Session"


def test_vector_store_registration():
    """Test that vector stores are properly registered."""
    # Import to trigger registration
    import haive.core.engine.vectorstore.providers

    # Check that vector stores are registered
    registered = BaseVectorStoreConfig.list_registered_types()

    expected_types = [
        VectorStoreType.CHROMA.value,
        VectorStoreType.FAISS.value,
        VectorStoreType.QDRANT.value,
        VectorStoreType.WEAVIATE.value,
        VectorStoreType.MILVUS.value,
    ]

    for expected in expected_types:
        assert expected in registered, f"Expected {expected} to be registered"


def test_invalid_distance_metrics():
    """Test validation of distance metrics."""
    from haive.core.engine.vectorstore.providers.ChromaVectorStoreConfig import (
        ChromaVectorStoreConfig,
    )

    embedding_config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    with pytest.raises(ValueError, match="distance_metric must be one of"):
        ChromaVectorStoreConfig(
            name="test", embedding=embedding_config, distance_metric="invalid_metric"
        )


if __name__ == "__main__":
    # Run basic tests
    print("Testing vector store configurations...")

    embedding_config = HuggingFaceEmbeddingConfig(
        model="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Test each vector store config
    print("✓ Testing Chroma configuration...")
    test_chroma_config(embedding_config)

    print("✓ Testing FAISS configuration...")
    test_faiss_config(embedding_config)

    print("✓ Testing Qdrant configuration...")
    test_qdrant_config(embedding_config)

    print("✓ Testing Weaviate configuration...")
    test_weaviate_config(embedding_config)

    print("✓ Testing Milvus configuration...")
    test_milvus_config(embedding_config)

    print("✓ Testing registration...")
    test_vector_store_registration()

    print("\nAll tests passed! ✅")
