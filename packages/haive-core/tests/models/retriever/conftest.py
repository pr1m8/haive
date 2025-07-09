"""Test configuration for retriever tests."""

from typing import Any, Dict, List
from unittest.mock import MagicMock, Mock

import pytest
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever


@pytest.fixture
def sample_documents():
    """Sample documents for testing."""
    return [
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


@pytest.fixture
def mock_vector_store():
    """Mock vector store for testing."""
    mock_store = Mock()
    mock_store.as_retriever = Mock()
    return mock_store


@pytest.fixture
def mock_retriever(sample_documents):
    """Mock retriever that returns sample documents."""
    mock_retriever = Mock(spec=BaseRetriever)
    mock_retriever.get_relevant_documents = Mock(return_value=sample_documents[:2])
    mock_retriever.invoke = Mock(return_value=sample_documents[:2])
    return mock_retriever


@pytest.fixture
def mock_llm():
    """Mock LLM for testing."""
    mock_llm = Mock()
    mock_llm.invoke = Mock(
        return_value="What is Python? What is programming? What is coding?"
    )
    return mock_llm


@pytest.fixture
def mock_bm25_retriever():
    """Mock BM25Retriever class."""
    mock_class = Mock()
    mock_instance = Mock(spec=BaseRetriever)
    mock_instance.get_relevant_documents = Mock(return_value=[])
    mock_class.from_documents = Mock(return_value=mock_instance)
    mock_class.from_texts = Mock(return_value=mock_instance)
    return mock_class


@pytest.fixture
def mock_vector_store_retriever():
    """Mock VectorStoreRetriever class."""
    mock_class = Mock()
    mock_instance = Mock(spec=BaseRetriever)
    mock_instance.get_relevant_documents = Mock(return_value=[])
    mock_class.return_value = mock_instance
    return mock_class


@pytest.fixture
def mock_multi_query_retriever():
    """Mock MultiQueryRetriever class."""
    mock_class = Mock()
    mock_instance = Mock(spec=BaseRetriever)
    mock_instance.get_relevant_documents = Mock(return_value=[])
    mock_class.return_value = mock_instance
    return mock_class


@pytest.fixture
def mock_ensemble_retriever():
    """Mock EnsembleRetriever class."""
    mock_class = Mock()
    mock_instance = Mock(spec=BaseRetriever)
    mock_instance.get_relevant_documents = Mock(return_value=[])
    mock_class.return_value = mock_instance
    return mock_class
