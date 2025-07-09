"""Test the new document loader architecture end-to-end.

This test verifies that the source-loader-registry architecture works correctly
for automatic document loading from various path types.
"""

from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from haive.core.engine.document.config import LoaderPreference
from haive.core.engine.document.loaders.auto_factory import DocumentLoaderFactory
from haive.core.engine.document.loaders.path_analyzer import (
    FileCategory,
    PathAnalyzer,
    PathType,
)
from haive.core.engine.document.loaders.sources.registry import (
    register_source,
    source_registry,
)
from haive.core.engine.document.loaders.sources.source_base import (
    BaseSource,
    LocalSource,
    RemoteSource,
)


class TestPathAnalyzer:
    """Test path analysis functionality."""

    def test_pdf_file_analysis(self):
        """Test analysis of PDF file path."""
        result = PathAnalyzer.analyze("/path/to/document.pdf")

        assert result.path_type == PathType.LOCAL_FILE
        assert result.file_extension == ".pdf"
        assert result.file_category == FileCategory.DOCUMENT
        assert result.is_local is True
        assert result.is_remote is False

    def test_github_url_analysis(self):
        """Test analysis of GitHub URL."""
        result = PathAnalyzer.analyze(
            "https://github.com/user/repo/blob/main/README.md"
        )

        assert result.path_type == PathType.URL_HTTPS
        assert result.is_remote is True
        assert result.domain == "github.com"
        assert result.service_detected == "github"
        assert result.file_extension == ".md"

    def test_database_uri_analysis(self):
        """Test analysis of database URI."""
        result = PathAnalyzer.analyze("postgresql://user:pass@localhost:5432/db")

        assert result.path_type == PathType.DATABASE_URI
        assert result.is_remote is True
        assert result.url_components["scheme"] == "postgresql"

    def test_cloud_storage_analysis(self):
        """Test analysis of cloud storage path."""
        result = PathAnalyzer.analyze("s3://bucket/path/file.txt")

        assert result.path_type == PathType.CLOUD_STORAGE
        assert result.is_remote is True
        assert result.cloud_provider == "aws"


class TestSourceRegistration:
    """Test source registration and lookup."""

    def setup_method(self):
        """Clear registry before each test."""
        source_registry._sources.clear()
        source_registry._extension_index.clear()
        source_registry._url_pattern_index.clear()
        source_registry._scheme_index.clear()
        source_registry._mime_index.clear()

    def test_register_pdf_source(self):
        """Test registering a PDF source."""

        @register_source(
            name="pdf",
            file_extensions=[".pdf"],
            mime_types=["application/pdf"],
            loaders={
                "fast": "PyPDFLoader",
                "quality": {
                    "class": "UnstructuredPDFLoader",
                    "quality": "high",
                    "requires_packages": ["unstructured"],
                },
            },
            default_loader="fast",
            priority=10,
        )
        class PDFSource(LocalSource):
            """Source for PDF documents."""

            pass

        # Verify registration
        assert "pdf" in source_registry._sources
        registration = source_registry._sources["pdf"]

        assert registration.name == "pdf"
        assert registration.source_class == PDFSource
        assert ".pdf" in registration.file_extensions
        assert "application/pdf" in registration.mime_types
        assert len(registration.loaders) == 2
        assert registration.default_loader == "fast"
        assert registration.priority == 10

    def test_find_source_by_extension(self):
        """Test finding source by file extension."""

        @register_source(
            name="text",
            file_extensions=[".txt", ".text"],
            loaders={"simple": "TextLoader"},
        )
        class TextSource(LocalSource):
            pass

        # Test finding by extension
        registration = source_registry.find_source_for_path("/path/to/file.txt")
        assert registration is not None
        assert registration.name == "text"

        # Test with different extension
        registration = source_registry.find_source_for_path("/path/to/file.text")
        assert registration is not None
        assert registration.name == "text"

    def test_find_source_by_url_pattern(self):
        """Test finding source by URL pattern."""

        @register_source(
            name="github",
            url_patterns=["github.com"],
            schemes=["https"],
            loaders={"github": "GitHubLoader"},
        )
        class GitHubSource(RemoteSource):
            pass

        # Test finding by URL pattern
        registration = source_registry.find_source_for_path(
            "https://github.com/user/repo"
        )
        assert registration is not None
        assert registration.name == "github"


class TestDocumentLoaderFactory:
    """Test the document loader factory."""

    def setup_method(self):
        """Clear registry and setup test sources."""
        source_registry._sources.clear()
        source_registry._extension_index.clear()
        source_registry._url_pattern_index.clear()
        source_registry._scheme_index.clear()
        source_registry._mime_index.clear()

        # Register test sources
        @register_source(
            name="pdf",
            file_extensions=[".pdf"],
            loaders={
                "fast": "PyPDFLoader",
                "quality": {
                    "class": "UnstructuredPDFLoader",
                    "module": "langchain_community.document_loaders",
                    "speed": "slow",
                    "quality": "high",
                },
            },
            default_loader="fast",
        )
        class PDFSource(LocalSource):
            pass

        @register_source(
            name="text", file_extensions=[".txt"], loaders={"simple": "TextLoader"}
        )
        class TextSource(LocalSource):
            pass

    def test_create_source_from_path(self):
        """Test creating source from path."""
        factory = DocumentLoaderFactory()

        # Test PDF source creation
        source = factory.create_source("/path/to/document.pdf")
        assert source is not None
        assert source.source_type == "pdf"
        assert source.file_path == "/path/to/document.pdf"

        # Test text source creation
        source = factory.create_source("/path/to/file.txt")
        assert source is not None
        assert source.source_type == "text"
        assert source.file_path == "/path/to/file.txt"

    @patch("haive.core.engine.document.loaders.auto_factory.__import__")
    def test_create_loader_from_source(self, mock_import):
        """Test creating loader from source."""
        # Mock the loader class
        mock_loader_class = Mock()
        mock_loader_instance = Mock()
        mock_loader_class.return_value = mock_loader_instance

        mock_module = Mock()
        mock_module.PyPDFLoader = mock_loader_class
        mock_import.return_value = mock_module

        factory = DocumentLoaderFactory()

        # Create source
        source = factory.create_source("/path/to/document.pdf")
        assert source is not None

        # Create loader
        loader = factory.create_loader_from_source(
            source, preference=LoaderPreference.SPEED
        )

        # Verify loader creation
        mock_import.assert_called_with(
            "langchain_community.document_loaders", fromlist=["PyPDFLoader"]
        )
        mock_loader_class.assert_called_once()
        assert loader == mock_loader_instance

    @patch("haive.core.engine.document.loaders.auto_factory.__import__")
    def test_create_loader_with_preference(self, mock_import):
        """Test loader selection based on preference."""
        # Mock loader classes
        mock_fast_loader = Mock()
        mock_quality_loader = Mock()

        mock_module = Mock()
        mock_module.PyPDFLoader = mock_fast_loader
        mock_module.UnstructuredPDFLoader = mock_quality_loader
        mock_import.return_value = mock_module

        factory = DocumentLoaderFactory()
        source = factory.create_source("/path/to/document.pdf")

        # Test speed preference (should use fast loader)
        loader = factory.create_loader_from_source(
            source, preference=LoaderPreference.SPEED
        )
        mock_fast_loader.assert_called()

        # Reset mocks
        mock_fast_loader.reset_mock()
        mock_quality_loader.reset_mock()

        # Test quality preference (should use quality loader)
        loader = factory.create_loader_from_source(
            source, preference=LoaderPreference.QUALITY
        )
        mock_quality_loader.assert_called()

    def test_analyze_path_with_sources(self):
        """Test path analysis with source information."""
        factory = DocumentLoaderFactory()

        result = factory.analyze_path_with_sources("/path/to/document.pdf")

        assert result["path"] == "/path/to/document.pdf"
        assert result["analysis"]["path_type"] == PathType.LOCAL_FILE
        assert result["analysis"]["file_extension"] == ".pdf"
        assert result["source"]["name"] == "pdf"
        assert "fast" in result["loaders"]
        assert "quality" in result["loaders"]
        assert result["loaders"]["fast"]["class"] == "PyPDFLoader"
        assert result["loaders"]["quality"]["class"] == "UnstructuredPDFLoader"


class TestEndToEndIntegration:
    """Test complete end-to-end document loading workflow."""

    def setup_method(self):
        """Setup test environment."""
        source_registry._sources.clear()
        source_registry._extension_index.clear()
        source_registry._url_pattern_index.clear()
        source_registry._scheme_index.clear()
        source_registry._mime_index.clear()

        # Register comprehensive source
        @register_source(
            name="pdf",
            file_extensions=[".pdf"],
            mime_types=["application/pdf"],
            loaders={
                "fast": {"class": "PyPDFLoader", "speed": "fast", "quality": "medium"},
                "quality": {
                    "class": "UnstructuredPDFLoader",
                    "speed": "slow",
                    "quality": "high",
                    "requires_packages": ["unstructured"],
                },
            },
            default_loader="fast",
            priority=10,
        )
        class PDFSource(LocalSource):
            pass

    def test_full_workflow_pdf_document(self):
        """Test complete workflow for PDF document."""
        factory = DocumentLoaderFactory()

        # Step 1: Analyze path
        analysis = factory.analyze_path_with_sources("/path/to/document.pdf")

        assert analysis["source"]["name"] == "pdf"
        assert len(analysis["loaders"]) == 2

        # Step 2: Create source
        source = factory.create_source("/path/to/document.pdf")

        assert source.source_type == "pdf"
        assert source.file_path == "/path/to/document.pdf"
        assert source.source_id == "pdf:/path/to/document.pdf"

        # Step 3: Get loader mapping
        loader_mapping = source_registry.get_loader_for_source(
            source, preference=LoaderPreference.SPEED
        )

        assert loader_mapping.name == "PyPDFLoader"
        assert loader_mapping.speed == "fast"
        assert loader_mapping.quality == "medium"

    def test_unknown_file_type_handling(self):
        """Test handling of unknown file types."""
        factory = DocumentLoaderFactory()

        # Try to create source for unknown file type
        source = factory.create_source("/path/to/unknown.xyz")

        # Should return None since no source registered for .xyz files
        assert source is None

        # Analysis should still work
        analysis = factory.analyze_path_with_sources("/path/to/unknown.xyz")
        assert analysis["source"] is None
        assert analysis["loaders"] == {}

    def test_convenience_functions(self):
        """Test convenience functions in auto_factory."""
        from haive.core.engine.document.loaders.auto_factory import (
            analyze_document_source,
            create_loader,
        )

        # Test analyze function
        result = analyze_document_source("/path/to/document.pdf")
        assert result["source"]["name"] == "pdf"

        # Test create_loader convenience function
        # This would normally create a real loader, but since we're not mocking
        # the import, it will fail. That's expected in this test.
        with pytest.raises((ImportError, AttributeError)):
            loader = create_loader("/path/to/document.pdf")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
