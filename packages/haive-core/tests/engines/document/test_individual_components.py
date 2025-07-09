"""Test individual document loader components in isolation.

This avoids the cascading import errors from the main document module.
"""

import sys
from pathlib import Path
from unittest.mock import Mock

import pytest

# Add the source directory to path for direct imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))


def test_path_analyzer_direct():
    """Test path analyzer directly."""
    from haive.core.engine.document.loaders.path_analyzer import (
        FileCategory,
        PathAnalyzer,
        PathType,
    )

    print("Testing PathAnalyzer directly...")

    # Test PDF file
    result = PathAnalyzer.analyze("/path/to/document.pdf")
    print(f"✓ Path type: {result.path_type}")
    print(f"✓ Extension: {result.file_extension}")
    print(f"✓ Category: {result.file_category}")

    assert result.path_type == PathType.LOCAL_FILE
    assert result.file_extension == ".pdf"
    assert result.file_category == FileCategory.DOCUMENT

    # Test GitHub URL
    result = PathAnalyzer.analyze("https://github.com/user/repo/blob/main/README.md")
    print(f"✓ GitHub detected: {result.service_detected}")

    assert result.service_detected == "github"

    print("PathAnalyzer tests passed!")


def test_source_base_direct():
    """Test source base classes directly."""
    from haive.core.engine.document.loaders.sources.source_base import (
        LocalSource,
        RemoteSource,
    )

    print("Testing source base classes...")

    # Test LocalSource
    pdf_source = LocalSource(
        source_type="pdf",
        source_id="test_pdf",
        file_path="/path/to/test.pdf",
        encoding="utf-8",
    )

    assert pdf_source.source_type == "pdf"
    assert pdf_source.file_path == "/path/to/test.pdf"
    assert pdf_source.encoding == "utf-8"

    # Test get_loader_kwargs
    kwargs = pdf_source.get_loader_kwargs()
    assert "file_path" in kwargs
    assert kwargs["file_path"] == "/path/to/test.pdf"
    assert kwargs["encoding"] == "utf-8"

    print("✓ LocalSource creation and kwargs")

    # Test RemoteSource
    web_source = RemoteSource(
        source_type="web",
        source_id="test_web",
        url="https://example.com/page.html",
        provider="generic",
    )

    assert web_source.url == "https://example.com/page.html"
    assert web_source.provider == "generic"

    kwargs = web_source.get_loader_kwargs()
    assert "url" in kwargs
    assert kwargs["url"] == "https://example.com/page.html"

    print("✓ RemoteSource creation and kwargs")
    print("Source base classes tests passed!")


def test_registry_direct():
    """Test registry functionality directly."""
    from haive.core.engine.document.loaders.sources.registry import (
        SourceRegistry,
        register_source,
    )
    from haive.core.engine.document.loaders.sources.source_base import LocalSource

    print("Testing registry functionality...")

    # Create fresh registry
    registry = SourceRegistry()

    # Define test source
    class TestPDFSource(LocalSource):
        """Test PDF source."""

        pass

    # Register source
    registration = registry.register(
        name="test_pdf",
        source_class=TestPDFSource,
        file_extensions=[".pdf"],
        loaders={
            "fast": "PyPDFLoader",
            "quality": {
                "class": "UnstructuredPDFLoader",
                "quality": "high",
                "speed": "slow",
            },
        },
        default_loader="fast",
        priority=10,
    )

    assert registration.name == "test_pdf"
    assert len(registration.loaders) == 2
    assert "fast" in registration.loaders
    assert "quality" in registration.loaders

    print("✓ Source registration")

    # Test finding source
    found = registry.find_source_for_path("/path/to/test.pdf")
    assert found is not None
    assert found.name == "test_pdf"

    print("✓ Source lookup by extension")

    # Test creating source
    source = registry.create_source("/path/to/test.pdf")
    assert source is not None
    assert source.source_type == "test_pdf"
    assert source.file_path == "/path/to/test.pdf"

    print("✓ Source creation")

    # Test loader selection
    loader_mapping = registry.get_loader_for_source(source)
    assert loader_mapping is not None
    assert loader_mapping.name == "PyPDFLoader"  # default_loader

    print("✓ Loader selection")
    print("Registry tests passed!")


def test_auto_factory_direct():
    """Test auto factory directly."""
    from haive.core.engine.document.config import LoaderPreference
    from haive.core.engine.document.loaders.auto_factory import DocumentLoaderFactory
    from haive.core.engine.document.loaders.sources.registry import (
        register_source,
        source_registry,
    )
    from haive.core.engine.document.loaders.sources.source_base import LocalSource

    print("Testing auto factory...")

    # Clear registry
    source_registry._sources.clear()
    source_registry._extension_index.clear()
    source_registry._url_pattern_index.clear()
    source_registry._scheme_index.clear()
    source_registry._mime_index.clear()

    # Register test source using decorator
    @register_source(
        name="pdf",
        file_extensions=[".pdf"],
        loaders={
            "fast": "PyPDFLoader",
            "quality": {"class": "UnstructuredPDFLoader", "quality": "high"},
        },
        default_loader="fast",
    )
    class PDFSource(LocalSource):
        pass

    factory = DocumentLoaderFactory()

    # Test source creation
    source = factory.create_source("/path/to/document.pdf")
    assert source is not None
    assert source.source_type == "pdf"
    assert source.file_path == "/path/to/document.pdf"

    print("✓ Factory source creation")

    # Test path analysis
    analysis = factory.analyze_path_with_sources("/path/to/document.pdf")
    assert analysis["source"]["name"] == "pdf"
    assert "fast" in analysis["loaders"]
    assert "quality" in analysis["loaders"]

    print("✓ Factory path analysis")

    # Test find available loaders
    loaders = factory.find_available_loaders("/path/to/document.pdf")
    assert "fast" in loaders
    assert "quality" in loaders

    print("✓ Factory loader discovery")
    print("Auto factory tests passed!")


if __name__ == "__main__":
    print("Running direct component tests...\n")

    test_path_analyzer_direct()
    print()

    test_source_base_direct()
    print()

    test_registry_direct()
    print()

    test_auto_factory_direct()
    print()

    print("All component tests passed! ✅")
