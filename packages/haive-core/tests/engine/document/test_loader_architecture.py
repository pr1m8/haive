"""Test the document loader architecture independently."""

import sys
from pathlib import Path

import pytest

# Add src to path to test modules directly
src_path = Path(__file__).parent.parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


def test_path_analyzer():
    """Test path analyzer functionality."""
    from haive.core.engine.document.loaders.path_analyzer import PathAnalyzer, PathType

    # Test local file
    result = PathAnalyzer.analyze("/path/to/document.pdf")
    assert result.path_type == PathType.LOCAL_FILE
    assert result.is_local is True
    assert result.file_extension == ".pdf"

    # Test URL
    result = PathAnalyzer.analyze("https://github.com/user/repo")
    assert result.path_type == PathType.URL_HTTPS
    assert result.is_remote is True
    assert result.domain == "github.com"

    # Test database URI
    result = PathAnalyzer.analyze("postgresql://localhost/db")
    assert result.path_type == PathType.DATABASE_URI
    assert result.is_database is True

    # Test cloud storage
    result = PathAnalyzer.analyze("s3://bucket/file.csv")
    assert result.path_type == PathType.CLOUD_STORAGE
    assert result.is_cloud is True


def test_source_base_classes():
    """Test source base classes."""
    from haive.core.engine.document.loaders.sources.base import (
        DatabaseSource,
        LocalSource,
        RemoteSource,
    )

    # Test LocalSource
    source = LocalSource(file_path="/test/file.pdf")
    assert source.file_path == "/test/file.pdf"
    assert source.encoding == "utf-8"
    kwargs = source.get_loader_kwargs()
    assert kwargs["file_path"] == "/test/file.pdf"

    # Test RemoteSource with SecureConfigMixin
    source = RemoteSource(url="https://api.example.com", provider="openai")
    assert source.url == "https://api.example.com"
    assert hasattr(source, "get_api_key")  # From SecureConfigMixin

    # Test DatabaseSource
    source = DatabaseSource(
        host="localhost", database="testdb", username="user", table_name="documents"
    )
    assert source.database == "testdb"
    assert source.validate_source() is True


def test_source_registry():
    """Test source registration and lookup."""
    from haive.core.engine.document.loaders.sources.base import LocalSource
    from haive.core.engine.document.loaders.sources.registry import (
        register_source,
        source_registry,
    )

    # Clear registry for test
    source_registry._sources.clear()

    # Register a test source
    @register_source(
        name="test_txt",
        file_extensions=[".txt"],
        loaders={
            "basic": "TextLoader",
            "advanced": {"class": "UnstructuredTextLoader", "quality": "high"},
        },
        default_loader="basic",
    )
    class TestTextSource(LocalSource):
        pass

    # Verify registration
    assert "test_txt" in source_registry.list_sources()

    # Test source lookup
    registration = source_registry.find_source_for_path("/test.txt")
    assert registration is not None
    assert registration.name == "test_txt"
    assert len(registration.loaders) == 2

    # Test source creation
    source = source_registry.create_source("/path/to/file.txt")
    assert isinstance(source, TestTextSource)
    assert source.file_path == "/path/to/file.txt"


def test_loader_selection():
    """Test loader selection based on preferences."""
    from haive.core.engine.document.config import LoaderPreference
    from haive.core.engine.document.loaders.sources.base import LocalSource
    from haive.core.engine.document.loaders.sources.registry import (
        register_source,
        source_registry,
    )

    # Register source with multiple loaders
    @register_source(
        name="test_multi",
        file_extensions=[".multi"],
        loaders={
            "fast": {"class": "FastLoader", "speed": "fast"},
            "quality": {"class": "QualityLoader", "quality": "high"},
        },
    )
    class TestMultiSource(LocalSource):
        pass

    source = TestMultiSource(file_path="/test.multi", source_type="test_multi")

    # Test speed preference
    loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.SPEED
    )
    assert loader.name == "FastLoader"

    # Test quality preference
    loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.QUALITY
    )
    assert loader.name == "QualityLoader"


def test_auto_factory_analysis():
    """Test the auto factory document analysis."""
    from haive.core.engine.document.loaders.auto_factory import document_loader_factory
    from haive.core.engine.document.loaders.sources.base import LocalSource
    from haive.core.engine.document.loaders.sources.registry import register_source

    # Register a test source
    @register_source(
        name="test_json", file_extensions=[".json"], loaders={"json": "JSONLoader"}
    )
    class TestJSONSource(LocalSource):
        pass

    # Analyze path
    result = document_loader_factory.analyze_path_with_sources("/data.json")

    assert result["path"] == "/data.json"
    assert result["analysis"]["file_extension"] == ".json"
    assert result["source"]["name"] == "test_json"
    assert "json" in result["loaders"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
