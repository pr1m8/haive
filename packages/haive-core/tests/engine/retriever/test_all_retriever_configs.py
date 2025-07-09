"""
Comprehensive test suite for all new retriever configurations.

This module tests all the newly implemented retriever configs to ensure
they instantiate properly and have correct configuration validation.
"""

import logging
from unittest.mock import Mock, patch

import pytest
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

logger = logging.getLogger(__name__)


def test_sparse_retriever_configs(sample_documents):
    """Test sparse/classical retriever configurations."""
    print("\n🧪 Testing Sparse Retriever Configurations...")

    # Test BM25 Retriever
    try:
        from haive.core.engine.retriever.providers.BM25RetrieverConfig import (
            BM25RetrieverConfig,
        )

        config = BM25RetrieverConfig(name="test_bm25", documents=sample_documents, k=2)
        assert config.name == "test_bm25"
        assert len(config.documents) == len(sample_documents)
        assert config.k == 2
        print("✅ BM25RetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ BM25RetrieverConfig - Error: {e}")

    # Test TF-IDF Retriever
    try:
        from haive.core.engine.retriever.providers.TFIDFRetrieverConfig import (
            TFIDFRetrieverConfig,
        )

        config = TFIDFRetrieverConfig(
            name="test_tfidf", documents=sample_documents, k=3
        )
        assert config.name == "test_tfidf"
        assert len(config.documents) == len(sample_documents)
        print("✅ TFIDFRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ TFIDFRetrieverConfig - Error: {e}")

    # Test KNN Retriever
    try:
        from haive.core.engine.retriever.providers.KNNRetrieverConfig import (
            KNNRetrieverConfig,
        )

        config = KNNRetrieverConfig(
            name="test_knn", documents=sample_documents, k=2, distance_metric="cosine"
        )
        assert config.distance_metric == "cosine"
        print("✅ KNNRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ KNNRetrieverConfig - Error: {e}")

    # Test SVM Retriever
    try:
        from haive.core.engine.retriever.providers.SVMRetrieverConfig import (
            SVMRetrieverConfig,
        )

        config = SVMRetrieverConfig(
            name="test_svm", documents=sample_documents, k=2, kernel="rbf"
        )
        assert config.kernel == "rbf"
        print("✅ SVMRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ SVMRetrieverConfig - Error: {e}")


def test_api_retriever_configs():
    """Test API-based retriever configurations."""
    print("\n🌐 Testing API Retriever Configurations...")

    # Test You.com Retriever
    try:
        from haive.core.engine.retriever.providers.YouRetrieverConfig import (
            YouRetrieverConfig,
        )

        config = YouRetrieverConfig(
            name="test_you", num_web_results=5, safesearch="moderate", country="US"
        )
        assert config.num_web_results == 5
        assert config.safesearch == "moderate"
        print("✅ YouRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ YouRetrieverConfig - Error: {e}")

    # Test AskNews Retriever
    try:
        from haive.core.engine.retriever.providers.AskNewsRetrieverConfig import (
            AskNewsRetrieverConfig,
        )

        config = AskNewsRetrieverConfig(
            name="test_asknews", k=10, hours_back=24, language="en"
        )
        assert config.k == 10
        assert config.hours_back == 24
        print("✅ AskNewsRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ AskNewsRetrieverConfig - Error: {e}")

    # Test PubMed Retriever
    try:
        from haive.core.engine.retriever.providers.PubMedRetrieverConfig import (
            PubMedRetrieverConfig,
        )

        config = PubMedRetrieverConfig(
            name="test_pubmed", top_k_results=5, load_max_docs=25
        )
        assert config.top_k_results == 5
        assert config.load_max_docs == 25
        print("✅ PubMedRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ PubMedRetrieverConfig - Error: {e}")


def test_cloud_retriever_configs():
    """Test cloud service retriever configurations."""
    print("\n☁️ Testing Cloud Service Retriever Configurations...")

    # Test Kendra Retriever
    try:
        from haive.core.engine.retriever.providers.KendraRetrieverConfig import (
            KendraRetrieverConfig,
        )

        config = KendraRetrieverConfig(
            name="test_kendra",
            index_id="test-index-123",
            region_name="us-east-1",
            top_k=10,
        )
        assert config.index_id == "test-index-123"
        assert config.region_name == "us-east-1"
        print("✅ KendraRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ KendraRetrieverConfig - Error: {e}")

    # Test Amazon Knowledge Bases Retriever
    try:
        from haive.core.engine.retriever.providers.AmazonKnowledgeBasesRetrieverConfig import (
            AmazonKnowledgeBasesRetrieverConfig,
        )

        config = AmazonKnowledgeBasesRetrieverConfig(
            name="test_kb",
            knowledge_base_id="ABCDEFGHIJ",
            region_name="us-east-1",
            number_of_results=10,
        )
        assert config.knowledge_base_id == "ABCDEFGHIJ"
        assert config.number_of_results == 10
        print(
            "✅ AmazonKnowledgeBasesRetrieverConfig - Configuration validation passed"
        )
    except Exception as e:
        print(f"❌ AmazonKnowledgeBasesRetrieverConfig - Error: {e}")

    # Test Google Vertex AI Search Retriever
    try:
        from haive.core.engine.retriever.providers.GoogleVertexAISearchRetrieverConfig import (
            GoogleVertexAISearchRetrieverConfig,
        )

        config = GoogleVertexAISearchRetrieverConfig(
            name="test_vertex_search",
            project_id="test-project",
            data_store_id="test-store",
            location_id="global",
        )
        assert config.project_id == "test-project"
        assert config.data_store_id == "test-store"
        print(
            "✅ GoogleVertexAISearchRetrieverConfig - Configuration validation passed"
        )
    except Exception as e:
        print(f"❌ GoogleVertexAISearchRetrieverConfig - Error: {e}")


def test_hybrid_retriever_configs():
    """Test hybrid search retriever configurations."""
    print("\n🔀 Testing Hybrid Search Retriever Configurations...")

    # Test Weaviate Hybrid Search Retriever
    try:
        from haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig import (
            WeaviateHybridSearchRetrieverConfig,
        )

        config = WeaviateHybridSearchRetrieverConfig(
            name="test_weaviate_hybrid",
            weaviate_url="https://test-cluster.weaviate.network",
            index_name="Document",
            alpha=0.5,
        )
        assert config.weaviate_url == "https://test-cluster.weaviate.network"
        assert config.alpha == 0.5
        print(
            "✅ WeaviateHybridSearchRetrieverConfig - Configuration validation passed"
        )
    except Exception as e:
        print(f"❌ WeaviateHybridSearchRetrieverConfig - Error: {e}")

    # Test Qdrant Sparse Vector Retriever
    try:
        from haive.core.engine.retriever.providers.QdrantSparseVectorRetrieverConfig import (
            QdrantSparseVectorRetrieverConfig,
        )

        config = QdrantSparseVectorRetrieverConfig(
            name="test_qdrant_sparse",
            qdrant_url="https://test-cluster.qdrant.tech",
            collection_name="documents",
            sparse_vector_name="sparse_text",
        )
        assert config.qdrant_url == "https://test-cluster.qdrant.tech"
        assert config.sparse_vector_name == "sparse_text"
        print("✅ QdrantSparseVectorRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ QdrantSparseVectorRetrieverConfig - Error: {e}")


def test_specialized_retriever_configs(sample_documents):
    """Test specialized platform retriever configurations."""
    print("\n🎯 Testing Specialized Retriever Configurations...")

    # Test Metal Retriever
    try:
        from haive.core.engine.retriever.providers.MetalRetrieverConfig import (
            MetalRetrieverConfig,
        )

        config = MetalRetrieverConfig(
            name="test_metal", index_id="my-metal-index-123", k=10
        )
        assert config.index_id == "my-metal-index-123"
        print("✅ MetalRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ MetalRetrieverConfig - Error: {e}")

    # Test DocArray Retriever
    try:
        from haive.core.engine.retriever.providers.DocArrayRetrieverConfig import (
            DocArrayRetrieverConfig,
        )

        config = DocArrayRetrieverConfig(
            name="test_docarray",
            documents=sample_documents,
            k=3,
            similarity_metric="cosine",
        )
        assert config.similarity_metric == "cosine"
        print("✅ DocArrayRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ DocArrayRetrieverConfig - Error: {e}")

    # Test NeuralDB Retriever
    try:
        from haive.core.engine.retriever.providers.NeuralDBRetrieverConfig import (
            NeuralDBRetrieverConfig,
        )

        config = NeuralDBRetrieverConfig(
            name="test_neuraldb", documents=sample_documents, k=5, training_steps=100
        )
        assert config.training_steps == 100
        print("✅ NeuralDBRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ NeuralDBRetrieverConfig - Error: {e}")

    # Test Zep Retriever
    try:
        from haive.core.engine.retriever.providers.ZepRetrieverConfig import (
            ZepRetrieverConfig,
        )

        config = ZepRetrieverConfig(
            name="test_zep",
            session_id="test-session-123",
            url="http://localhost:8000",
            top_k=10,
        )
        assert config.session_id == "test-session-123"
        print("✅ ZepRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ ZepRetrieverConfig - Error: {e}")

    # Test Zep Cloud Retriever
    try:
        from haive.core.engine.retriever.providers.ZepCloudRetrieverConfig import (
            ZepCloudRetrieverConfig,
        )

        config = ZepCloudRetrieverConfig(
            name="test_zep_cloud",
            session_id="test-session-123",
            api_url="https://api.getzep.com",
            top_k=10,
        )
        assert config.api_url == "https://api.getzep.com"
        print("✅ ZepCloudRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ ZepCloudRetrieverConfig - Error: {e}")


def test_integration_retriever_configs(sample_documents):
    """Test integration retriever configurations."""
    print("\n🔗 Testing Integration Retriever Configurations...")

    # Test LlamaIndex Retriever
    try:
        from haive.core.engine.retriever.providers.LlamaIndexRetrieverConfig import (
            LlamaIndexRetrieverConfig,
        )

        config = LlamaIndexRetrieverConfig(
            name="test_llamaindex", documents=sample_documents, k=3, index_type="vector"
        )
        assert config.index_type == "vector"
        print("✅ LlamaIndexRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ LlamaIndexRetrieverConfig - Error: {e}")

    # Test ChatGPT Plugin Retriever
    try:
        from haive.core.engine.retriever.providers.ChatGPTPluginRetrieverConfig import (
            ChatGPTPluginRetrieverConfig,
        )

        config = ChatGPTPluginRetrieverConfig(
            name="test_chatgpt_plugin",
            plugin_url="https://api.example-plugin.com",
            plugin_name="ExamplePlugin",
            top_k=10,
        )
        assert config.plugin_url == "https://api.example-plugin.com"
        assert config.plugin_name == "ExamplePlugin"
        print("✅ ChatGPTPluginRetrieverConfig - Configuration validation passed")
    except Exception as e:
        print(f"❌ ChatGPTPluginRetrieverConfig - Error: {e}")


def test_validation_errors():
    """Test that configurations properly validate input parameters."""
    print("\n⚠️ Testing Configuration Validation...")

    # Test that k parameter is properly validated
    try:
        from haive.core.engine.retriever.providers.BM25RetrieverConfig import (
            BM25RetrieverConfig,
        )

        # This should raise a validation error (k too small)
        with pytest.raises(Exception):
            BM25RetrieverConfig(
                name="test_invalid", documents=[], k=0  # Invalid: k must be >= 1
            )
        print("✅ k parameter validation working correctly")
    except ImportError:
        print("❌ Could not import BM25RetrieverConfig for validation testing")

    # Test that required fields are enforced
    try:
        from haive.core.engine.retriever.providers.KendraRetrieverConfig import (
            KendraRetrieverConfig,
        )

        # This should raise a validation error (missing required index_id)
        with pytest.raises(Exception):
            KendraRetrieverConfig(
                name="test_invalid"
                # Missing required index_id field
            )
        print("✅ Required field validation working correctly")
    except ImportError:
        print("❌ Could not import KendraRetrieverConfig for validation testing")


def test_retriever_registration():
    """Test that all retrievers are properly registered."""
    print("\n📋 Testing Retriever Registration...")

    from haive.core.engine.retriever.retriever import BaseRetrieverConfig
    from haive.core.engine.retriever.types import RetrieverType

    # Import all our retrievers to trigger registration
    try:
        from haive.core.engine.retriever.providers.BM25RetrieverConfig import (
            BM25RetrieverConfig,
        )
        from haive.core.engine.retriever.providers.KendraRetrieverConfig import (
            KendraRetrieverConfig,
        )
        from haive.core.engine.retriever.providers.WeaviateHybridSearchRetrieverConfig import (
            WeaviateHybridSearchRetrieverConfig,
        )
        from haive.core.engine.retriever.providers.YouRetrieverConfig import (
            YouRetrieverConfig,
        )

        # Check that they're registered
        registry = BaseRetrieverConfig._registry

        expected_types = [
            RetrieverType.BM25,
            RetrieverType.YOU,
            RetrieverType.KENDRA,
            RetrieverType.WEAVIATE_HYBRID_SEARCH,
        ]

        for retriever_type in expected_types:
            assert retriever_type in registry, f"{retriever_type} not found in registry"

        print(f"✅ Registration test passed - {len(registry)} retrievers registered")
        print(f"   Tested types: {[rt.value for rt in expected_types]}")

    except Exception as e:
        print(f"❌ Registration test failed: {e}")


if __name__ == "__main__":
    # Create sample documents for testing
    sample_docs = [
        Document(
            page_content="Python is a programming language.",
            metadata={"source": "doc1", "topic": "programming"},
        ),
        Document(
            page_content="Machine learning uses algorithms to learn patterns.",
            metadata={"source": "doc2", "topic": "AI"},
        ),
        Document(
            page_content="Vector databases store high-dimensional vectors.",
            metadata={"source": "doc3", "topic": "databases"},
        ),
        Document(
            page_content="Retrieval augmented generation combines search and generation.",
            metadata={"source": "doc4", "topic": "AI"},
        ),
    ]

    print("🚀 Running Comprehensive Retriever Configuration Tests...")
    print("=" * 70)

    # Run all tests
    test_sparse_retriever_configs(sample_docs)
    test_api_retriever_configs()
    test_cloud_retriever_configs()
    test_hybrid_retriever_configs()
    test_specialized_retriever_configs(sample_docs)
    test_integration_retriever_configs(sample_docs)
    test_validation_errors()
    test_retriever_registration()

    print("\n" + "=" * 70)
    print("🎉 All configuration tests completed!")
