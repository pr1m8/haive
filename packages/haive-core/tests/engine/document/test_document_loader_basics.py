"""Basic tests for document loader system.

Tests the source-loader-engine relationship and auto-detection.
"""

from pathlib import Path

import pytest

from haive.core.engine.document.loaders.auto_factory import (
    analyze_document_source,
    create_loader,
    document_loader_factory,
)
from haive.core.engine.document.loaders.path_analyzer import PathAnalyzer, PathType
from haive.core.engine.document.loaders.sources.base import LocalSource, RemoteSource
from haive.core.engine.document.loaders.sources.registry import (
    register_source,
    source_registry,
)


class TestPathAnalyzer:
    """Test path analysis functionality."""

    def test_local_file_analysis(self):
        """Test analyzing local file paths."""
        result = PathAnalyzer.analyze("/path/to/document.pdf")

        assert result.path_type == PathType.LOCAL_FILE
        assert result.is_local is True
        assert result.is_file is True
        assert result.file_extension == ".pdf"
        assert result.file_category == "document"

    def test_url_analysis(self):
        """Test analyzing URLs."""
        result = PathAnalyzer.analyze("https://github.com/user/repo")

        assert result.path_type == PathType.URL_HTTPS
        assert result.is_remote is True
        assert result.domain == "github.com"
        assert result.url_components["service"] == "github"

    def test_database_uri_analysis(self):
        """Test analyzing database URIs."""
        result = PathAnalyzer.analyze("postgresql://user:pass@localhost:5432/mydb")

        assert result.path_type == PathType.DATABASE_URI
        assert result.is_database is True
        assert result.database_type == "postgresql"

    def test_cloud_storage_analysis(self):
        """Test analyzing cloud storage URIs."""
        result = PathAnalyzer.analyze("s3://my-bucket/path/to/file.csv")

        assert result.path_type == PathType.CLOUD_STORAGE
        assert result.is_cloud is True
        assert result.cloud_provider == "aws"
        assert result.bucket_name == "my-bucket"
        assert result.object_key == "path/to/file.csv"


class TestSourceRegistry:
    """Test source registration and lookup."""

    def test_source_registration(self):
        """Test registering a source with decorator."""

        @register_source(
            name="test_pdf",
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
        class TestPDFSource(LocalSource):
            """Test PDF source."""

            pass

        # Check registration
        assert "test_pdf" in source_registry.list_sources()

        # Check source lookup by path
        registration = source_registry.find_source_for_path("/test/doc.pdf")
        assert registration is not None
        assert registration.name == "test_pdf"
        assert len(registration.loaders) == 2
        assert "fast" in registration.loaders
        assert "quality" in registration.loaders

    def test_source_creation(self):
        """Test creating source instances."""

        # Register a test source first
        @register_source(
            name="test_text",
            file_extensions=[".txt", ".text"],
            loaders={"basic": "TextLoader"},
        )
        class TestTextSource(LocalSource):
            pass

        # Create source from path
        source = source_registry.create_source("/path/to/file.txt")
        assert source is not None
        assert isinstance(source, TestTextSource)
        assert source.file_path == "/path/to/file.txt"
        assert source.source_type == "test_text"

    def test_loader_selection(self):
        """Test loader selection logic."""

        # Register source with multiple loaders
        @register_source(
            name="test_multi",
            file_extensions=[".multi"],
            loaders={
                "fast": {"class": "FastLoader", "speed": "fast", "quality": "low"},
                "quality": {
                    "class": "QualityLoader",
                    "speed": "slow",
                    "quality": "high",
                },
                "balanced": {
                    "class": "BalancedLoader",
                    "speed": "medium",
                    "quality": "medium",
                },
            },
            default_loader="balanced",
        )
        class TestMultiSource(LocalSource):
            pass

        source = TestMultiSource(file_path="/test.multi", source_type="test_multi")

        # Test speed preference
        from haive.core.engine.document.config import LoaderPreference

        loader = source_registry.get_loader_for_source(
            source, preference=LoaderPreference.SPEED
        )
        assert loader.name == "FastLoader"

        # Test quality preference
        loader = source_registry.get_loader_for_source(
            source, preference=LoaderPreference.QUALITY
        )
        assert loader.name == "QualityLoader"

        # Test default
        loader = source_registry.get_loader_for_source(
            source, preference=LoaderPreference.BALANCED
        )
        assert loader.name == "BalancedLoader"


class TestAutoFactory:
    """Test the auto factory functionality."""

    def test_analyze_document_source(self):
        """Test analyzing paths with source detection."""

        # Register a test source
        @register_source(
            name="test_csv",
            file_extensions=[".csv"],
            loaders={
                "pandas": {"class": "CSVLoader", "requires_packages": ["pandas"]},
                "basic": "UnstructuredCSVLoader",
            },
        )
        class TestCSVSource(LocalSource):
            pass

        # Analyze path
        result = analyze_document_source("/data/file.csv")

        assert result["path"] == "/data/file.csv"
        assert result["analysis"]["file_extension"] == ".csv"
        assert result["source"]["name"] == "test_csv"
        assert "pandas" in result["loaders"]
        assert "basic" in result["loaders"]

    def test_source_with_secure_config(self):
        """Test sources that use SecureConfigMixin."""

        @register_source(
            name="test_api",
            url_patterns=["api.example.com"],
            loaders={
                "api": {
                    "class": "APILoader",
                    "requires_auth": True,
                }
            },
        )
        class TestAPISource(RemoteSource):
            """Test API source with auth."""

            provider: str = "example"  # For SecureConfigMixin

        # Create source
        source = TestAPISource(
            url="https://api.example.com/data",
            source_type="test_api",
            provider="example",
        )

        # Test that it's a RemoteSource with SecureConfigMixin
        assert hasattr(source, "get_api_key")
        assert source.provider == "example"

        # Test loader kwargs include auth
        kwargs = source.get_loader_kwargs()
        assert "url" in kwargs
        assert kwargs["url"] == "https://api.example.com/data"


@pytest.mark.integration
class TestIntegration:
    """Integration tests requiring actual loaders."""

    def test_create_loader_mock(self):
        """Test creating a loader (mocked since we don't have langchain)."""
        # This would fail without langchain_community installed
        # but shows the interface

        @register_source(
            name="test_integration",
            file_extensions=[".test"],
            loaders={"mock": "MockLoader"},
        )
        class TestIntegrationSource(LocalSource):
            pass

        # Try to create loader (will fail without the actual loader class)
        with pytest.raises((ImportError, AttributeError)):
            loader = create_loader("/test/file.test")

    def test_factory_error_handling(self):
        """Test factory error handling."""
        # Try unknown file type
        result = document_loader_factory.analyze_path_with_sources(
            "/unknown/file.xyz123"
        )
        assert result["source"] is None
        assert result["loaders"] == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
