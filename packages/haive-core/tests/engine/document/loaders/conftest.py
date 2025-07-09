"""Pytest fixtures for document loader tests.

This module provides comprehensive fixtures for testing the document loader
system including mock sources, loaders, registries, and test data.

Author: Claude (Haive Document Loader System)
Version: 1.0.0
"""

import shutil
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock

import pytest
from langchain_core.documents import Document

from haive.core.engine.document.config import LoaderPreference
from haive.core.engine.document.loaders.auto_loader import (
    AutoLoader,
    AutoLoaderConfig,
    BulkLoadingResult,
    LoadingResult,
)
from haive.core.engine.document.loaders.auto_registry import (
    AutoRegistry,
    RegistrationInfo,
    RegistrationStats,
)
from haive.core.engine.document.loaders.path_analyzer import (
    PathAnalyzer,
    SourceInfo,
)
from haive.core.engine.document.loaders.sources.enhanced_registry import (
    EnhancedSourceRegistry,
)
from haive.core.engine.document.loaders.sources.source_types import (
    BaseSource,
    CredentialType,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir)


@pytest.fixture
def sample_documents():
    """Create sample Document objects for testing."""
    return [
        Document(
            page_content="This is a test document about AI.",
            metadata={
                "source": "test.pdf",
                "page": 1,
                "created_at": "2024-01-01T00:00:00Z",
            },
        ),
        Document(
            page_content="This is another test document about machine learning.",
            metadata={
                "source": "test.pdf",
                "page": 2,
                "created_at": "2024-01-01T00:00:00Z",
            },
        ),
        Document(
            page_content="Final test document about neural networks.",
            metadata={
                "source": "test.pdf",
                "page": 3,
                "created_at": "2024-01-01T00:00:00Z",
            },
        ),
    ]


@pytest.fixture
def test_files(temp_dir):
    """Create test files in the temporary directory."""
    files = {}

    # Create various test files
    test_data = {
        "test.pdf": b"PDF content here",
        "test.txt": b"Simple text content",
        "test.csv": b"col1,col2\nval1,val2\nval3,val4",
        "test.json": b'{"key": "value", "items": [1, 2, 3]}',
        "test.docx": b"DOCX content here",
        "test.xlsx": b"XLSX content here",
        "test.pptx": b"PPTX content here",
    }

    for filename, content in test_data.items():
        file_path = temp_dir / filename
        file_path.write_bytes(content)
        files[filename] = file_path

    # Create subdirectory with more files
    subdir = temp_dir / "subdocs"
    subdir.mkdir()

    sub_files = {
        "sub1.txt": b"Subdirectory file 1",
        "sub2.pdf": b"Subdirectory PDF content",
    }

    for filename, content in sub_files.items():
        file_path = subdir / filename
        file_path.write_bytes(content)
        files[f"subdocs/{filename}"] = file_path

    return files


@pytest.fixture
def mock_source_info():
    """Create a mock SourceInfo object."""
    return SourceInfo(
        source_type="pdf",
        category=SourceCategory.LOCAL_FILE,
        confidence=0.95,
        metadata={
            "file_extension": ".pdf",
            "estimated_size": 1024,
            "mime_type": "application/pdf",
        },
        capabilities=[
            LoaderCapability.TEXT_EXTRACTION,
            LoaderCapability.METADATA_EXTRACTION,
        ],
    )


@pytest.fixture
def mock_pdf_source():
    """Create a mock PDF source instance."""

    class MockPDFSource(LocalFileSource):
        source_type: str = "pdf"
        category: SourceCategory = SourceCategory.LOCAL_FILE

        def __init__(self, path: Path, **kwargs):
            self.path = path
            self.kwargs = kwargs

        def get_loader_kwargs(self) -> Dict[str, Any]:
            return {
                "file_path": str(self.path),
                "extract_images": False,
                **self.kwargs,
            }

    return MockPDFSource


@pytest.fixture
def mock_web_source():
    """Create a mock web source instance."""

    class MockWebSource(RemoteSource):
        source_type: str = "web"
        category: SourceCategory = SourceCategory.WEB

        def __init__(self, url: str, **kwargs):
            self.url = url
            self.kwargs = kwargs

        def get_loader_kwargs(self) -> Dict[str, Any]:
            return {
                "web_path": self.url,
                "header_template": {},
                **self.kwargs,
            }

        def scrape_all(self) -> Dict[str, Any]:
            return {
                "recursive": True,
                "max_depth": 3,
                "respect_robots": True,
            }

    return MockWebSource


@pytest.fixture
def mock_document_loader():
    """Create a mock document loader class."""

    class MockDocumentLoader:
        def __init__(self, **kwargs):
            self.kwargs = kwargs
            self._documents = [
                Document(
                    page_content=f"Mock content from {kwargs.get('file_path', 'unknown')}",
                    metadata={"loader": "mock", **kwargs},
                )
            ]

        def load(self) -> List[Document]:
            return self._documents.copy()

        def load_and_split(self) -> List[Document]:
            # Split the document into smaller chunks
            return [
                Document(
                    page_content=f"Chunk {i}: {doc.page_content[:50]}...",
                    metadata={**doc.metadata, "chunk": i},
                )
                for i, doc in enumerate(self._documents)
            ]

        def lazy_load(self):
            for doc in self._documents:
                yield doc

    return MockDocumentLoader


@pytest.fixture
def mock_enhanced_registry():
    """Create a mock enhanced registry."""
    registry = Mock(spec=EnhancedSourceRegistry)

    # Mock registry data
    registry._sources = {
        "pdf": Mock(
            name="PDFSource",
            loaders={
                "pypdf": {
                    "class": "PyPDFLoader",
                    "speed": "fast",
                    "quality": "medium",
                    "module": "langchain_community.document_loaders",
                },
                "pdfplumber": {
                    "class": "PDFPlumberLoader",
                    "speed": "slow",
                    "quality": "high",
                    "module": "langchain_community.document_loaders",
                },
            },
            default_loader="pypdf",
            capabilities=[
                LoaderCapability.TEXT_EXTRACTION,
                LoaderCapability.METADATA_EXTRACTION,
            ],
        ),
        "web": Mock(
            name="WebSource",
            loaders={
                "beautiful_soup": {
                    "class": "BeautifulSoupWebLoader",
                    "speed": "medium",
                    "quality": "medium",
                    "module": "langchain_community.document_loaders",
                },
                "playwright": {
                    "class": "PlaywrightURLLoader",
                    "speed": "slow",
                    "quality": "high",
                    "module": "langchain_community.document_loaders",
                },
            },
            default_loader="beautiful_soup",
            capabilities=[
                LoaderCapability.WEB_SCRAPING,
                LoaderCapability.BULK_LOADING,
            ],
        ),
    }

    def mock_get_loader_for_source(
        source_type: str, preference=LoaderPreference.BALANCED
    ):
        if source_type == "pdf":
            if preference == LoaderPreference.SPEED:
                return "pypdf"
            elif preference == LoaderPreference.QUALITY:
                return "pdfplumber"
            else:
                return "pypdf"
        elif source_type == "web":
            if preference == LoaderPreference.QUALITY:
                return "playwright"
            else:
                return "beautiful_soup"
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    def mock_get_loader_config(source_type: str, loader_name: str):
        return registry._sources[source_type].loaders[loader_name]

    def mock_get_source_class(source_type: str):
        if source_type == "pdf":
            return mock_pdf_source
        elif source_type == "web":
            return mock_web_source
        else:
            raise ValueError(f"Unknown source type: {source_type}")

    def mock_get_loader_class(source_type: str, loader_name: str):
        return mock_document_loader

    registry.get_loader_for_source.side_effect = mock_get_loader_for_source
    registry.get_loader_config.side_effect = mock_get_loader_config
    registry.get_source_class.side_effect = mock_get_source_class
    registry.get_loader_class.side_effect = mock_get_loader_class

    return registry


@pytest.fixture
def mock_path_analyzer():
    """Create a mock path analyzer."""
    analyzer = Mock(spec=PathAnalyzer)

    def mock_analyze_path(path_or_url: str) -> SourceInfo:
        if path_or_url.endswith(".pdf"):
            return SourceInfo(
                source_type="pdf",
                category=SourceCategory.LOCAL_FILE,
                confidence=0.95,
                metadata={"file_extension": ".pdf"},
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
            )
        elif path_or_url.startswith("http"):
            return SourceInfo(
                source_type="web",
                category=SourceCategory.WEB,
                confidence=0.90,
                metadata={"protocol": "http"},
                capabilities=[LoaderCapability.WEB_SCRAPING],
            )
        else:
            return SourceInfo(
                source_type="unknown",
                category=SourceCategory.UNKNOWN,
                confidence=0.0,
                metadata={},
                capabilities=[],
            )

    analyzer.analyze_path.side_effect = mock_analyze_path
    return analyzer


@pytest.fixture
def auto_loader_config():
    """Create an AutoLoaderConfig for testing."""
    return AutoLoaderConfig(
        preference=LoaderPreference.BALANCED,
        max_concurrency=5,
        timeout=60,
        retry_attempts=2,
        enable_caching=False,
        enable_metadata=True,
    )


@pytest.fixture
def auto_loader(auto_loader_config, mock_enhanced_registry, mock_path_analyzer):
    """Create an AutoLoader instance with mocked dependencies."""
    return AutoLoader(
        config=auto_loader_config,
        registry=mock_enhanced_registry,
        path_analyzer=mock_path_analyzer,
    )


@pytest.fixture
def mock_auto_registry():
    """Create a mock auto registry."""
    registry = Mock(spec=AutoRegistry)

    # Mock registration data
    mock_registration_info = RegistrationInfo(
        source_name="pdf",
        source_class=mock_pdf_source,
        module_name="test_module",
        category=SourceCategory.LOCAL_FILE,
        loaders=["pypdf", "pdfplumber"],
        registration_time=datetime.now(),
    )

    registry.registered_sources = {"pdf": mock_registration_info}
    registry.registration_errors = []

    def mock_register_all_sources():
        return RegistrationStats(
            total_modules_scanned=5,
            total_sources_found=10,
            total_sources_registered=8,
            registration_errors=["Error 1", "Error 2"],
            registration_time=1.5,
            categories_covered=4,
        )

    registry.register_all_sources.return_value = mock_register_all_sources()

    return registry


@pytest.fixture
def loading_result(sample_documents, mock_source_info):
    """Create a sample LoadingResult."""
    return LoadingResult(
        documents=sample_documents,
        source_info=mock_source_info,
        loader_used="pypdf",
        loading_time=2.5,
        metadata={"test": True},
        errors=[],
    )


@pytest.fixture
def bulk_loading_result(loading_result):
    """Create a sample BulkLoadingResult."""
    return BulkLoadingResult(
        total_documents=3,
        results=[loading_result],
        failed_sources=[],
        total_time=5.0,
        summary={
            "total_sources": 1,
            "successful_loads": 1,
            "failed_loads": 0,
            "success_rate": 100.0,
        },
    )


@pytest.fixture
def registration_stats():
    """Create sample RegistrationStats."""
    return RegistrationStats(
        total_modules_scanned=10,
        total_sources_found=25,
        total_sources_registered=23,
        registration_errors=["Module X failed to import", "Source Y validation failed"],
        registration_time=3.2,
        categories_covered=8,
    )


# Test data fixtures


@pytest.fixture
def test_urls():
    """Provide test URLs for web source testing."""
    return [
        "https://example.com/page.html",
        "https://docs.python.org/3/",
        "https://github.com/user/repo",
        "http://simple-site.com",
        "https://api.service.com/v1/data",
    ]


@pytest.fixture
def test_database_urls():
    """Provide test database URLs."""
    return [
        "postgresql://user:pass@localhost:5432/db",
        "mysql://user:pass@localhost:3306/db",
        "sqlite:///path/to/db.sqlite",
        "mongodb://user:pass@localhost:27017/db",
        "redis://localhost:6379/0",
    ]


@pytest.fixture
def test_cloud_urls():
    """Provide test cloud storage URLs."""
    return [
        "s3://bucket-name/path/to/file.pdf",
        "gs://bucket-name/documents/",
        "azure://container/path/file.docx",
        "https://drive.google.com/file/d/123456",
        "https://dropbox.com/s/xyz/file.pdf",
    ]


# Parametrized fixtures for comprehensive testing


@pytest.fixture(params=["speed", "quality", "balanced"])
def loader_preference(request):
    """Parametrized fixture for different loader preferences."""
    preference_map = {
        "speed": LoaderPreference.SPEED,
        "quality": LoaderPreference.QUALITY,
        "balanced": LoaderPreference.BALANCED,
    }
    return preference_map[request.param]


@pytest.fixture(params=[1, 5, 10, 20])
def concurrency_level(request):
    """Parametrized fixture for different concurrency levels."""
    return request.param


@pytest.fixture(
    params=[
        SourceCategory.LOCAL_FILE,
        SourceCategory.WEB,
        SourceCategory.DATABASE,
        SourceCategory.CLOUD_STORAGE,
        SourceCategory.API,
    ]
)
def source_category(request):
    """Parametrized fixture for different source categories."""
    return request.param


# Error simulation fixtures


@pytest.fixture
def failing_loader():
    """Create a loader that always fails."""

    class FailingLoader:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def load(self) -> List[Document]:
            raise Exception("Simulated loader failure")

        def load_and_split(self) -> List[Document]:
            raise Exception("Simulated loader failure")

    return FailingLoader


@pytest.fixture
def slow_loader():
    """Create a loader that takes a long time."""
    import time

    class SlowLoader:
        def __init__(self, delay: float = 2.0, **kwargs):
            self.delay = delay
            self.kwargs = kwargs

        def load(self) -> List[Document]:
            time.sleep(self.delay)
            return [
                Document(
                    page_content="Slow loading content",
                    metadata={"loader": "slow", "delay": self.delay},
                )
            ]

    return SlowLoader


# Utility fixtures


@pytest.fixture
def assert_documents_equal():
    """Utility function to assert that two document lists are equal."""

    def _assert_equal(docs1: List[Document], docs2: List[Document]):
        assert len(docs1) == len(
            docs2
        ), f"Document count mismatch: {len(docs1)} vs {len(docs2)}"

        for i, (doc1, doc2) in enumerate(zip(docs1, docs2)):
            assert (
                doc1.page_content == doc2.page_content
            ), f"Content mismatch at index {i}"
            assert doc1.metadata == doc2.metadata, f"Metadata mismatch at index {i}"

    return _assert_equal


@pytest.fixture
def assert_loading_result_valid():
    """Utility function to validate LoadingResult objects."""

    def _assert_valid(result: LoadingResult):
        assert isinstance(result.documents, list)
        assert isinstance(result.source_info, SourceInfo)
        assert isinstance(result.loader_used, str)
        assert isinstance(result.loading_time, (int, float))
        assert result.loading_time >= 0
        assert isinstance(result.metadata, dict)
        assert isinstance(result.errors, list)

        if result.errors:
            assert len(result.documents) == 0, "Failed loads should have no documents"
        else:
            assert len(result.documents) > 0, "Successful loads should have documents"

    return _assert_valid


@pytest.fixture
def mock_credentials():
    """Provide mock credentials for testing."""
    return {
        "aws": {
            "aws_access_key_id": "test_access_key",
            "aws_secret_access_key": "test_secret_key",
            "region_name": "us-east-1",
        },
        "gcp": {
            "credentials_path": "/path/to/service-account.json",
            "project_id": "test-project",
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "username": "test_user",
            "password": "test_password",
            "database": "test_db",
        },
        "api": {
            "api_key": "test_api_key",
            "api_secret": "test_api_secret",
            "base_url": "https://api.test.com",
        },
    }


# Integration test fixtures


@pytest.fixture
def integration_test_sources(test_files, test_urls):
    """Provide sources for integration testing."""
    return {
        "local_files": list(test_files.values())[:3],  # First 3 files
        "web_urls": test_urls[:2],  # First 2 URLs
        "mixed": [
            str(list(test_files.values())[0]),  # One file
            test_urls[0],  # One URL
        ],
    }


@pytest.fixture(scope="session")
def performance_test_data():
    """Generate data for performance testing."""
    # Create a larger dataset for performance testing
    large_content = "Lorem ipsum dolor sit amet. " * 1000

    return {
        "large_documents": [
            Document(
                page_content=f"{large_content} Document {i}",
                metadata={"doc_id": i, "size": "large"},
            )
            for i in range(100)
        ],
        "many_small_documents": [
            Document(
                page_content=f"Small document {i}",
                metadata={"doc_id": i, "size": "small"},
            )
            for i in range(1000)
        ],
    }


# Cleanup fixtures


@pytest.fixture(autouse=True)
def cleanup_cache():
    """Automatically cleanup any caches after each test."""
    yield
    # Add cache cleanup logic here if needed
    pass


@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset any global state between tests."""
    yield
    # Add global state reset logic here if needed
    pass


# Documentation and examples


@pytest.fixture
def example_usage_patterns():
    """Provide examples of common usage patterns for testing."""
    return {
        "simple_load": {
            "description": "Load a single document",
            "code": 'loader.load("/path/to/document.pdf")',
            "expected_calls": [
                "detect_source",
                "get_best_loader",
                "create_source_instance",
            ],
        },
        "bulk_load": {
            "description": "Load multiple documents concurrently",
            "code": 'loader.load_bulk(["file1.pdf", "file2.txt"])',
            "expected_calls": ["load_detailed"] * 2,
        },
        "load_all": {
            "description": "Recursively load all documents from a source",
            "code": 'loader.load_all("/path/to/directory/")',
            "expected_calls": ["detect_source", "create_source_instance", "scrape_all"],
        },
        "async_load": {
            "description": "Asynchronously load documents",
            "code": 'await loader.aload("https://example.com")',
            "expected_calls": ["load"],
        },
    }
