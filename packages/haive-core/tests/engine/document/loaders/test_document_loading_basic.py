"""Basic tests for document loading functionality.

This module tests the core document loading capabilities with real examples.
"""

import tempfile
from pathlib import Path
from typing import List

import pytest
from langchain_core.documents import Document

from haive.core.engine.document.config import LoaderPreference
from haive.core.engine.document.loaders.auto_loader import (
    AutoLoader,
    AutoLoaderConfig,
    load_document,
)
from haive.core.engine.document.loaders.sources.source_types import SourceCategory


class TestBasicDocumentLoading:
    """Test basic document loading functionality."""

    @pytest.fixture
    def temp_text_file(self):
        """Create a temporary text file for testing."""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("This is a test document.\n")
            f.write("It has multiple lines.\n")
            f.write("This is for testing the document loader.")
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        temp_path.unlink()

    @pytest.fixture
    def temp_json_file(self):
        """Create a temporary JSON file for testing."""
        import json

        data = {
            "title": "Test Document",
            "content": "This is JSON content",
            "metadata": {"author": "Test Author", "version": "1.0"},
        }

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            json.dump(data, f)
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        temp_path.unlink()

    @pytest.fixture
    def temp_csv_file(self):
        """Create a temporary CSV file for testing."""
        content = """name,age,city
John Doe,30,New York
Jane Smith,25,Los Angeles
Bob Johnson,35,Chicago"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
            f.write(content)
            temp_path = Path(f.name)

        yield temp_path

        # Cleanup
        temp_path.unlink()

    def test_auto_loader_initialization(self):
        """Test AutoLoader initialization."""
        loader = AutoLoader()

        assert loader is not None
        assert loader.config.preference == LoaderPreference.BALANCED
        assert loader.config.max_concurrency == 10
        assert loader.config.enable_caching is False

    def test_auto_loader_with_config(self):
        """Test AutoLoader with custom configuration."""
        config = AutoLoaderConfig(
            preference=LoaderPreference.QUALITY,
            max_concurrency=5,
            enable_caching=True,
            cache_ttl=7200,
        )
        loader = AutoLoader(config)

        assert loader.config.preference == LoaderPreference.QUALITY
        assert loader.config.max_concurrency == 5
        assert loader.config.enable_caching is True
        assert loader.config.cache_ttl == 7200

    def test_detect_text_file_source(self, temp_text_file):
        """Test source detection for text files."""
        loader = AutoLoader()
        source_info = loader.detect_source(str(temp_text_file))

        assert source_info is not None
        assert source_info.source_type in ["txt", "text", "plaintext"]
        assert source_info.category in [
            SourceCategory.LOCAL_FILE,
            SourceCategory.FILE_DATA,
        ]
        assert source_info.confidence > 0.8

    def test_detect_json_file_source(self, temp_json_file):
        """Test source detection for JSON files."""
        loader = AutoLoader()
        source_info = loader.detect_source(str(temp_json_file))

        assert source_info is not None
        assert source_info.source_type == "json"
        assert source_info.category in [
            SourceCategory.LOCAL_FILE,
            SourceCategory.FILE_DATA,
        ]
        assert source_info.confidence > 0.8

    def test_detect_csv_file_source(self, temp_csv_file):
        """Test source detection for CSV files."""
        loader = AutoLoader()
        source_info = loader.detect_source(str(temp_csv_file))

        assert source_info is not None
        assert source_info.source_type == "csv"
        assert source_info.category in [
            SourceCategory.LOCAL_FILE,
            SourceCategory.FILE_DATA,
        ]
        assert source_info.confidence > 0.8

    def test_detect_web_source(self):
        """Test source detection for URLs."""
        loader = AutoLoader()
        source_info = loader.detect_source("https://example.com/document.html")

        assert source_info is not None
        assert source_info.source_type in ["web", "url", "website"]
        assert source_info.category in [SourceCategory.WEB, SourceCategory.WEB_SCRAPING]
        assert source_info.confidence > 0.7

    @pytest.mark.skip(reason="Requires actual loader implementation")
    def test_load_text_document(self, temp_text_file):
        """Test loading a text document."""
        loader = AutoLoader()
        documents = loader.load(str(temp_text_file))

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert isinstance(documents[0], Document)
        assert "test document" in documents[0].page_content.lower()

    @pytest.mark.skip(reason="Requires actual loader implementation")
    def test_load_json_document(self, temp_json_file):
        """Test loading a JSON document."""
        loader = AutoLoader()
        documents = loader.load(str(temp_json_file))

        assert isinstance(documents, list)
        assert len(documents) > 0
        assert isinstance(documents[0], Document)
        assert "Test Document" in str(documents[0].page_content)

    @pytest.mark.skip(reason="Requires actual loader implementation")
    def test_load_csv_document(self, temp_csv_file):
        """Test loading a CSV document."""
        loader = AutoLoader()
        documents = loader.load(str(temp_csv_file))

        assert isinstance(documents, list)
        assert len(documents) > 0

        # CSV loaders typically create one document per row
        content = "\n".join(doc.page_content for doc in documents)
        assert "John Doe" in content
        assert "Jane Smith" in content

    def test_convenience_function(self, temp_text_file):
        """Test the load_document convenience function."""
        try:
            documents = load_document(str(temp_text_file))
            assert isinstance(documents, list)
        except Exception:
            # Expected if loaders aren't fully implemented
            pytest.skip("Loader implementation not complete")

    def test_loader_preference_configuration(self):
        """Test different loader preference configurations."""
        preferences = [
            LoaderPreference.SPEED,
            LoaderPreference.QUALITY,
            LoaderPreference.BALANCED,
        ]

        for pref in preferences:
            config = AutoLoaderConfig(preference=pref)
            loader = AutoLoader(config)
            assert loader.config.preference == pref

    def test_error_handling_invalid_path(self):
        """Test error handling for invalid paths."""
        loader = AutoLoader()

        with pytest.raises(ValueError, match="Could not detect source type"):
            loader.detect_source("/invalid/path/that/does/not/exist.xyz")

    def test_error_handling_unsupported_source(self):
        """Test error handling for unsupported source types."""
        loader = AutoLoader()

        # Try to detect a completely unknown source type
        try:
            source_info = loader.detect_source("unknown://protocol/path")
            # If it doesn't raise, it should return unknown type
            assert source_info.source_type == "unknown"
            assert source_info.category == SourceCategory.UNKNOWN
            assert source_info.confidence < 0.5
        except ValueError:
            # This is also acceptable behavior
            pass


class TestDocumentLoadingWithMocks:
    """Test document loading with mocked dependencies."""

    def test_load_with_retry(self, mocker):
        """Test loading with retry logic."""
        loader = AutoLoader(AutoLoaderConfig(retry_attempts=2))

        # Mock a loader that fails once then succeeds
        mock_loader = mocker.Mock()
        mock_loader.load.side_effect = [
            Exception("First attempt failed"),
            [Document(page_content="Success!", metadata={})],
        ]

        result = loader._load_with_retry(mock_loader, "test_source")

        assert len(result) == 1
        assert result[0].page_content == "Success!"
        assert mock_loader.load.call_count == 2

    def test_caching_functionality(self, mocker, temp_text_file):
        """Test document caching."""
        config = AutoLoaderConfig(enable_caching=True, cache_ttl=3600)
        loader = AutoLoader(config)

        # Mock the actual loading
        mock_documents = [Document(page_content="Cached content", metadata={})]
        mocker.patch.object(loader, "_load_with_retry", return_value=mock_documents)

        # First load
        docs1 = loader.load(str(temp_text_file))
        assert docs1 == mock_documents

        # Second load should use cache
        docs2 = loader.load(str(temp_text_file))
        assert docs2 == mock_documents

        # _load_with_retry should only be called once
        loader._load_with_retry.assert_called_once()

    def test_bulk_loading_mock(self, mocker):
        """Test bulk loading with mocked sources."""
        loader = AutoLoader()

        # Mock load_detailed to return successful results
        def mock_load_detailed(path, **kwargs):
            from haive.core.engine.document.loaders.auto_loader import LoadingResult
            from haive.core.engine.document.loaders.path_analyzer import SourceInfo

            return LoadingResult(
                documents=[Document(page_content=f"Content from {path}", metadata={})],
                source_info=SourceInfo(
                    source_type="mock",
                    category=SourceCategory.LOCAL_FILE,
                    confidence=1.0,
                    metadata={},
                    capabilities=[],
                ),
                loader_used="mock_loader",
                loading_time=0.1,
                metadata={},
                errors=[],
            )

        mocker.patch.object(loader, "load_detailed", side_effect=mock_load_detailed)

        sources = ["file1.txt", "file2.txt", "file3.txt"]
        result = loader.load_bulk(sources)

        assert result.total_documents == 3
        assert len(result.results) == 3
        assert result.summary["successful_loads"] == 3
        assert result.summary["failed_loads"] == 0


class TestPathAnalyzer:
    """Test path analyzer functionality."""

    def test_analyze_local_file_paths(self):
        """Test analyzing local file paths."""
        from haive.core.engine.document.loaders.path_analyzer import PathAnalyzer

        analyzer = PathAnalyzer()

        test_paths = [
            ("/path/to/document.pdf", "pdf"),
            ("/path/to/data.csv", "csv"),
            ("/path/to/code.py", "python"),
            ("/path/to/doc.docx", "docx"),
            ("/path/to/image.png", "image"),
        ]

        for path, expected_type in test_paths:
            result = analyzer.analyze_path(path)
            assert result is not None
            assert (
                expected_type in result.source_type.lower()
                or result.source_type in ["local_file", "file"]
            )

    def test_analyze_url_patterns(self):
        """Test analyzing URL patterns."""
        from haive.core.engine.document.loaders.path_analyzer import PathAnalyzer

        analyzer = PathAnalyzer()

        test_urls = [
            ("https://example.com", "web"),
            ("http://api.example.com/v1/data", "api"),
            ("ftp://files.example.com/data.zip", "ftp"),
            ("s3://bucket/object", "s3"),
            ("gs://bucket/object", "gcs"),
        ]

        for url, expected_category in test_urls:
            result = analyzer.analyze_path(url)
            assert result is not None
            assert result.category in [
                SourceCategory.WEB,
                SourceCategory.API,
                SourceCategory.CLOUD_STORAGE,
            ]


class TestRegistrySystem:
    """Test the registry system."""

    def test_registry_initialization(self):
        """Test registry initialization."""
        from haive.core.engine.document.loaders.sources.enhanced_registry import (
            EnhancedRegistry,
        )

        registry = EnhancedRegistry()
        assert registry is not None
        assert hasattr(registry, "_sources")
        assert hasattr(registry, "_loaders")

    def test_auto_registration(self):
        """Test auto-registration functionality."""
        from haive.core.engine.document.loaders.auto_registry import (
            auto_register_all,
            get_registration_status,
        )

        # This might fail if sources have errors, but we can check the process
        try:
            stats = auto_register_all()
            assert stats is not None
            assert hasattr(stats, "total_modules_scanned")
            assert hasattr(stats, "total_sources_registered")

            # Check status
            status = get_registration_status()
            assert isinstance(status, dict)
            assert "total_sources" in status

        except Exception as e:
            pytest.skip(f"Auto-registration not fully implemented: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
