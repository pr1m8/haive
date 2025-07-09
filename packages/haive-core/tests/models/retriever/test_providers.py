"""Tests for retriever providers."""

from typing import Any, Dict
from unittest.mock import MagicMock, Mock, patch

import pytest

from haive.core.models.retriever.provider_types import RetrieverProvider
from haive.core.models.retriever.providers.bm25 import Bm25Provider
from haive.core.models.retriever.providers.ensemble import EnsembleProvider
from haive.core.models.retriever.providers.multi_query import MultiQueryProvider
from haive.core.models.retriever.providers.vector_store import VectorStoreProvider


class TestVectorStoreProvider:
    """Test VectorStoreProvider."""

    def test_initialization(self, mock_vector_store):
        """Test provider initialization."""
        provider = VectorStoreProvider(
            vector_store=mock_vector_store, k=5, search_type="mmr"
        )

        assert provider.provider == RetrieverProvider.VECTOR_STORE
        assert provider.vector_store == mock_vector_store
        assert provider.k == 5
        assert provider.search_type == "mmr"

    def test_get_default_params(self, mock_vector_store):
        """Test getting default parameters."""
        provider = VectorStoreProvider(
            vector_store=mock_vector_store, k=3, filter={"source": "test"}
        )

        params = provider._get_default_params()

        assert params["vectorstore"] == mock_vector_store
        assert params["search_type"] == "similarity"
        assert params["search_kwargs"]["k"] == 3
        assert params["search_kwargs"]["filter"] == {"source": "test"}

    def test_prepare_params(self, mock_vector_store):
        """Test parameter preparation."""
        provider = VectorStoreProvider(
            vector_store=mock_vector_store, k=4, search_kwargs={"fetch_k": 20}
        )

        params = provider._prepare_params(k=10, search_type="mmr")

        assert params["search_kwargs"]["k"] == 10
        assert params["search_kwargs"]["fetch_k"] == 20
        assert params["search_type"] == "mmr"

    def test_instantiate_success(self, mock_vector_store, mock_vector_store_retriever):
        """Test successful instantiation."""
        with patch(
            "haive.core.models.retriever.providers.vector_store.VectorStoreProvider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.return_value = mock_vector_store_retriever

            provider = VectorStoreProvider(vector_store=mock_vector_store)
            result = provider.instantiate()

            mock_vector_store_retriever.assert_called_once()
            assert result is not None

    def test_import_error(self, mock_vector_store):
        """Test handling of import errors."""
        with patch(
            "haive.core.models.retriever.providers.vector_store.VectorStoreProvider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.side_effect = ImportError("Package not found")

            provider = VectorStoreProvider(vector_store=mock_vector_store)

            with pytest.raises(ImportError, match="langchain-core is required"):
                provider.instantiate()


class TestMultiQueryProvider:
    """Test MultiQueryProvider."""

    def test_initialization(self, mock_retriever, mock_llm):
        """Test provider initialization."""
        provider = MultiQueryProvider(
            retriever=mock_retriever,
            llm=mock_llm,
            query_count=5,
            include_original=False,
        )

        assert provider.provider == RetrieverProvider.MULTI_QUERY
        assert provider.retriever == mock_retriever
        assert provider.llm == mock_llm
        assert provider.query_count == 5
        assert provider.include_original is False

    def test_get_default_params(self, mock_retriever, mock_llm):
        """Test getting default parameters."""
        provider = MultiQueryProvider(
            retriever=mock_retriever,
            llm=mock_llm,
            include_original=False,
            parser_key="queries",
        )

        params = provider._get_default_params()

        assert params["retriever"] == mock_retriever
        assert params["llm_chain"] == mock_llm
        assert params["include_original"] is False
        assert params["parser_key"] == "queries"

    def test_prepare_params(self, mock_retriever, mock_llm):
        """Test parameter preparation."""
        provider = MultiQueryProvider(retriever=mock_retriever, llm=mock_llm)

        params = provider._prepare_params()

        # Should convert llm to llm_chain
        assert "llm_chain" in params
        assert "llm" not in params
        assert params["llm_chain"] == mock_llm

    def test_instantiate_success(
        self, mock_retriever, mock_llm, mock_multi_query_retriever
    ):
        """Test successful instantiation."""
        with patch(
            "haive.core.models.retriever.providers.multi_query.MultiQueryProvider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.return_value = mock_multi_query_retriever

            provider = MultiQueryProvider(retriever=mock_retriever, llm=mock_llm)
            result = provider.instantiate()

            mock_multi_query_retriever.assert_called_once()
            assert result is not None


class TestEnsembleProvider:
    """Test EnsembleProvider."""

    def test_initialization(self, mock_retriever):
        """Test provider initialization."""
        retriever2 = Mock()
        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2], weights=[0.6, 0.4], c=100
        )

        assert provider.provider == RetrieverProvider.ENSEMBLE
        assert len(provider.retrievers) == 2
        assert provider.weights == [0.6, 0.4]
        assert provider.c == 100

    def test_weights_validation(self, mock_retriever):
        """Test weights validation."""
        retriever2 = Mock()

        # Valid weights
        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2], weights=[0.7, 0.3]
        )
        assert provider.weights == [0.7, 0.3]

        # Invalid weights (don't sum to 1.0)
        with pytest.raises(ValueError, match="Weights must sum to 1.0"):
            EnsembleProvider(
                retrievers=[mock_retriever, retriever2], weights=[0.5, 0.6]
            )

    def test_retrievers_validation(self):
        """Test retrievers validation."""
        # Too few retrievers
        with pytest.raises(ValueError, match="At least 2 retrievers are required"):
            EnsembleProvider(retrievers=[Mock()], weights=[1.0])

    def test_add_retriever(self, mock_retriever):
        """Test adding a retriever."""
        retriever2 = Mock()
        retriever3 = Mock()

        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2], weights=[0.6, 0.4]
        )

        provider.add_retriever(retriever3, 0.2)

        assert len(provider.retrievers) == 3
        assert len(provider.weights) == 3
        assert abs(sum(provider.weights) - 1.0) < 1e-6  # Should still sum to 1.0
        assert provider.retrievers[2] == retriever3

    def test_remove_retriever(self, mock_retriever):
        """Test removing a retriever."""
        retriever2 = Mock()
        retriever3 = Mock()

        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2, retriever3], weights=[0.4, 0.3, 0.3]
        )

        provider.remove_retriever(1)  # Remove middle retriever

        assert len(provider.retrievers) == 2
        assert len(provider.weights) == 2
        assert abs(sum(provider.weights) - 1.0) < 1e-6  # Should still sum to 1.0
        assert provider.retrievers == [mock_retriever, retriever3]

    def test_remove_retriever_errors(self, mock_retriever):
        """Test remove retriever error cases."""
        retriever2 = Mock()

        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2], weights=[0.6, 0.4]
        )

        # Can't remove from ensemble with only 2 retrievers
        with pytest.raises(
            ValueError, match="ensemble must have at least 2 retrievers"
        ):
            provider.remove_retriever(0)

        # Add third retriever to test index error
        provider.add_retriever(Mock(), 0.2)

        # Index out of range
        with pytest.raises(IndexError):
            provider.remove_retriever(10)

    def test_get_ensemble_info(self, mock_retriever):
        """Test getting ensemble info."""
        retriever2 = Mock()
        retriever2.__class__.__name__ = "MockRetriever2"
        mock_retriever.__class__.__name__ = "MockRetriever1"

        provider = EnsembleProvider(
            retrievers=[mock_retriever, retriever2], weights=[0.7, 0.3], c=50
        )

        info = provider.get_ensemble_info()

        assert info["num_retrievers"] == 2
        assert info["weights"] == [0.7, 0.3]
        assert info["rrf_constant"] == 50
        assert len(info["retriever_types"]) == 2


class TestBm25Provider:
    """Test Bm25Provider."""

    def test_initialization_with_documents(self, sample_documents):
        """Test provider initialization with documents."""
        provider = Bm25Provider(documents=sample_documents, k=5, b=0.8, k1=1.5)

        assert provider.provider == RetrieverProvider.BM25
        assert provider.documents == sample_documents
        assert provider.k == 5
        assert provider.b == 0.8
        assert provider.k1 == 1.5

    def test_initialization_with_texts(self):
        """Test provider initialization with texts."""
        texts = ["text 1", "text 2", "text 3"]
        metadatas = [{"id": 1}, {"id": 2}, {"id": 3}]

        provider = Bm25Provider(texts=texts, metadatas=metadatas, k=3)

        assert provider.texts == texts
        assert provider.metadatas == metadatas
        assert provider.k == 3

    def test_get_default_params(self, sample_documents):
        """Test getting default parameters."""
        provider = Bm25Provider(
            documents=sample_documents,
            b=0.9,
            k1=1.8,
            preprocess_func=lambda x: x.lower(),
        )

        params = provider._get_default_params()

        assert params["k"] == 4  # default k
        assert params["b"] == 0.9
        assert params["k1"] == 1.8
        assert "preprocess_func" in params

    def test_instantiate_with_documents(self, sample_documents, mock_bm25_retriever):
        """Test instantiation with documents."""
        with patch(
            "haive.core.models.retriever.providers.bm25.Bm25Provider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.return_value = mock_bm25_retriever

            provider = Bm25Provider(documents=sample_documents, k=3)
            result = provider.instantiate()

            mock_bm25_retriever.from_documents.assert_called_once()
            assert result is not None

    def test_instantiate_with_texts(self, mock_bm25_retriever):
        """Test instantiation with texts."""
        with patch(
            "haive.core.models.retriever.providers.bm25.Bm25Provider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.return_value = mock_bm25_retriever

            texts = ["text 1", "text 2"]
            provider = Bm25Provider(texts=texts, k=2)
            result = provider.instantiate()

            mock_bm25_retriever.from_texts.assert_called_once()
            assert result is not None

    def test_instantiate_without_data(self):
        """Test instantiation without documents or texts."""
        provider = Bm25Provider(k=4)

        with pytest.raises(
            ValueError, match="Either 'documents' or 'texts' must be provided"
        ):
            provider.instantiate()

    def test_get_corpus_info(self, sample_documents):
        """Test getting corpus information."""
        # Test with documents
        provider = Bm25Provider(documents=sample_documents)
        info = provider.get_corpus_info()

        assert info["source"] == "documents"
        assert info["count"] == len(sample_documents)
        assert info["has_metadata"] is True

        # Test with texts
        provider = Bm25Provider(texts=["text1", "text2"])
        info = provider.get_corpus_info()

        assert info["source"] == "texts"
        assert info["count"] == 2
        assert info["has_metadata"] is False

        # Test with no data
        provider = Bm25Provider()
        info = provider.get_corpus_info()

        assert info["source"] == "none"
        assert info["count"] == 0

    def test_get_bm25_params(self):
        """Test getting BM25 parameters."""
        provider = Bm25Provider(b=0.85, k1=1.3)
        params = provider.get_bm25_params()

        assert params["b"] == 0.85
        assert params["k1"] == 1.3


class TestProviderErrorHandling:
    """Test error handling across providers."""

    def test_validation_config_import_error(self, mock_vector_store):
        """Test validate_config with import error."""
        with patch(
            "haive.core.models.retriever.providers.vector_store.VectorStoreProvider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.side_effect = ImportError("Package not available")

            provider = VectorStoreProvider(vector_store=mock_vector_store)

            with pytest.raises(ValueError, match="requires package"):
                provider.validate_config()

    def test_validation_config_success(
        self, mock_vector_store, mock_vector_store_retriever
    ):
        """Test successful config validation."""
        with patch(
            "haive.core.models.retriever.providers.vector_store.VectorStoreProvider._get_retriever_class"
        ) as mock_get_class:
            mock_get_class.return_value = mock_vector_store_retriever

            provider = VectorStoreProvider(vector_store=mock_vector_store)
            result = provider.validate_config()

            assert result is True

    def test_get_config_dict(self, mock_vector_store):
        """Test getting configuration dictionary."""
        provider = VectorStoreProvider(
            vector_store=mock_vector_store,
            k=5,
            name="test_retriever",
            tags={"env": "test"},
        )

        config = provider.get_config_dict()

        assert "vector_store" in config
        assert config["k"] == 5
        assert config["name"] == "test_retriever"
        assert "tags" not in config  # Should be excluded
