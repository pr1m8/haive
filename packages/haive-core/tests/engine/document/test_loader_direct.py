"""Direct tests for document loader modules without main imports."""

import pytest


def test_path_analyzer_direct():
    """Test path analyzer directly."""
    # Import directly to avoid document module init
    import sys
    from pathlib import Path

    # Add path
    src_path = Path(__file__).parent.parent.parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    # Now import directly
    from haive.core.engine.document.loaders import path_analyzer

    # Test local file
    result = path_analyzer.PathAnalyzer.analyze("/path/to/document.pdf")
    assert result.path_type == path_analyzer.PathType.LOCAL_FILE
    assert result.is_local is True
    assert result.file_extension == ".pdf"
    assert result.file_category == path_analyzer.FileCategory.DOCUMENT

    # Test URL
    result = path_analyzer.PathAnalyzer.analyze("https://github.com/user/repo")
    assert result.path_type == path_analyzer.PathType.URL_HTTPS
    assert result.is_remote is True
    assert result.domain == "github.com"
    assert result.url_components["service"] == "github"

    # Test database
    result = path_analyzer.PathAnalyzer.analyze("postgresql://user:pass@localhost/db")
    assert result.path_type == path_analyzer.PathType.DATABASE_URI
    assert result.is_database is True
    assert result.database_type == "postgresql"

    # Test cloud
    result = path_analyzer.PathAnalyzer.analyze("s3://bucket/file.csv")
    assert result.path_type == path_analyzer.PathType.CLOUD_STORAGE
    assert result.is_cloud is True
    assert result.cloud_provider == "aws"
    assert result.bucket_name == "bucket"
    assert result.object_key == "file.csv"


def test_source_classes_direct():
    """Test source base classes directly."""
    import sys
    from pathlib import Path

    src_path = Path(__file__).parent.parent.parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from haive.core.engine.document.loaders.sources import base

    # Test LocalSource
    source = base.LocalSource(file_path="/test/document.pdf")
    assert source.file_path == "/test/document.pdf"
    assert source.encoding == "utf-8"
    assert source.validate_source() is False  # File doesn't exist

    kwargs = source.get_loader_kwargs()
    assert kwargs["file_path"] == "/test/document.pdf"
    assert kwargs["encoding"] == "utf-8"

    # Test RemoteSource with SecureConfigMixin
    source = base.RemoteSource(url="https://api.openai.com/v1/data", provider="openai")
    assert source.url == "https://api.openai.com/v1/data"
    assert source.provider == "openai"
    assert hasattr(source, "get_api_key")  # From SecureConfigMixin
    assert source.validate_source() is True

    # Test DatabaseSource
    source = base.DatabaseSource(
        host="localhost",
        port=5432,
        database="testdb",
        username="user",
        table_name="documents",
    )
    assert source.database == "testdb"
    assert source.validate_source() is True

    kwargs = source.get_loader_kwargs()
    assert kwargs["host"] == "localhost"
    assert kwargs["database"] == "testdb"

    # Test CloudSource
    source = base.CloudSource(
        url="s3://my-bucket/path/to/file.pdf",
        bucket_name="my-bucket",
        object_key="path/to/file.pdf",
        provider="aws",
    )
    assert source.bucket_name == "my-bucket"
    assert source.object_key == "path/to/file.pdf"

    kwargs = source.get_loader_kwargs()
    assert kwargs["bucket"] == "my-bucket"
    assert kwargs["key"] == "path/to/file.pdf"


def test_source_registry_direct():
    """Test source registry directly."""
    import sys
    from pathlib import Path

    src_path = Path(__file__).parent.parent.parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from haive.core.engine.document.loaders.sources import base, registry

    # Clear registry for clean test
    registry.source_registry._sources.clear()
    registry.source_registry._extension_index.clear()

    # Test decorator registration
    @registry.register_source(
        name="test_csv",
        file_extensions=[".csv"],
        mime_types=["text/csv"],
        loaders={
            "basic": "CSVLoader",
            "pandas": {
                "class": "PandasCSVLoader",
                "speed": "fast",
                "quality": "high",
                "requires_packages": ["pandas"],
            },
        },
        default_loader="basic",
        priority=5,
    )
    class TestCSVSource(base.LocalSource):
        """Test CSV source."""

        delimiter: str = ","
        has_header: bool = True

    # Verify registration
    assert "test_csv" in registry.source_registry.list_sources()

    # Test finding by path
    reg = registry.source_registry.find_source_for_path("/data/file.csv")
    assert reg is not None
    assert reg.name == "test_csv"
    assert len(reg.loaders) == 2
    assert "basic" in reg.loaders
    assert "pandas" in reg.loaders

    # Test creating source
    source = registry.source_registry.create_source("/data/test.csv")
    assert isinstance(source, TestCSVSource)
    assert source.file_path == "/data/test.csv"
    assert source.source_type == "test_csv"

    # Test loader selection
    from haive.core.engine.document.config import LoaderPreference

    # Get fast loader
    loader_info = registry.source_registry.get_loader_for_source(
        source, preference=LoaderPreference.SPEED
    )
    assert loader_info.name == "PandasCSVLoader"
    assert loader_info.speed == "fast"

    # Get default loader
    loader_info = registry.source_registry.get_loader_for_source(
        source, preference=LoaderPreference.BALANCED
    )
    assert loader_info.name == "CSVLoader"  # default


def test_auto_factory_direct():
    """Test auto factory directly."""
    import sys
    from pathlib import Path

    src_path = Path(__file__).parent.parent.parent.parent / "src"
    if str(src_path) not in sys.path:
        sys.path.insert(0, str(src_path))

    from haive.core.engine.document.loaders import auto_factory
    from haive.core.engine.document.loaders.sources import base, registry

    # Register a test source
    @registry.register_source(
        name="test_txt",
        file_extensions=[".txt", ".text"],
        loaders={"text": "TextLoader"},
        priority=1,
    )
    class TestTextSource(base.LocalSource):
        pass

    # Test analysis
    result = auto_factory.document_loader_factory.analyze_path_with_sources("/test.txt")

    assert result["path"] == "/test.txt"
    assert result["analysis"]["file_extension"] == ".txt"
    assert result["source"]["name"] == "test_txt"
    assert "text" in result["loaders"]

    # Test source creation
    source = auto_factory.document_loader_factory.create_source("/readme.txt")
    assert isinstance(source, TestTextSource)
    assert source.file_path == "/readme.txt"

    # Test finding available loaders
    loaders = auto_factory.document_loader_factory.find_available_loaders("/test.txt")
    assert "text" in loaders


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
