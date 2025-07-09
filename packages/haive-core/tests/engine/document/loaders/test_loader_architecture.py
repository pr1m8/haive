"""Standalone test of the document loader architecture."""

import sys
from pathlib import Path

# Direct imports to avoid cascading import issues
sys.path.insert(0, "/home/will/Projects/haive/backend/haive/packages/haive-core/src")


def test_path_analyzer():
    """Test path analyzer functionality."""
    from haive.core.engine.document.loaders.path_analyzer import (
        FileCategory,
        PathAnalyzer,
        PathType,
    )

    print("🔍 Testing PathAnalyzer...")

    # Test PDF file
    result = PathAnalyzer.analyze("/path/to/document.pdf")
    print(
        f"  ✓ PDF file - Type: {result.path_type}, Extension: {result.file_extension}"
    )
    assert result.path_type == PathType.LOCAL_FILE
    assert result.file_extension == ".pdf"
    assert result.file_category == FileCategory.DOCUMENT

    # Test GitHub URL
    result = PathAnalyzer.analyze("https://github.com/user/repo/blob/main/README.md")
    print(
        f"  ✓ GitHub URL - Service: {result.service_detected}, Extension: {result.file_extension}"
    )
    assert result.service_detected == "github"
    assert result.file_extension == ".md"

    # Test database URI
    result = PathAnalyzer.analyze("postgresql://user:pass@localhost:5432/db")
    print(f"  ✓ Database URI - Type: {result.path_type}")
    assert result.path_type == PathType.DATABASE_URI

    print("  ✅ PathAnalyzer tests passed!\n")


def test_source_classes():
    """Test source base classes."""
    from haive.core.engine.document.loaders.sources.source_base import (
        DatabaseSource,
        LocalSource,
        RemoteSource,
    )

    print("📁 Testing Source Classes...")

    # Test LocalSource
    pdf_source = LocalSource(
        source_type="pdf",
        source_id="test_pdf",
        file_path="/path/to/test.pdf",
        encoding="utf-8",
    )

    kwargs = pdf_source.get_loader_kwargs()
    print(
        f"  ✓ LocalSource - Path: {pdf_source.file_path}, Kwargs: {list(kwargs.keys())}"
    )
    assert kwargs["file_path"] == "/path/to/test.pdf"
    assert kwargs["encoding"] == "utf-8"

    # Test RemoteSource
    web_source = RemoteSource(
        source_type="web",
        source_id="test_web",
        url="https://example.com/page.html",
        provider="generic",
    )

    kwargs = web_source.get_loader_kwargs()
    print(f"  ✓ RemoteSource - URL: {web_source.url}, Kwargs: {list(kwargs.keys())}")
    assert kwargs["url"] == "https://example.com/page.html"

    # Test DatabaseSource
    db_source = DatabaseSource(
        source_type="database",
        source_id="test_db",
        connection_string="postgresql://user:pass@localhost:5432/db",
        provider="postgresql",
    )

    kwargs = db_source.get_loader_kwargs()
    print(f"  ✓ DatabaseSource - Connection: {db_source.connection_string}")
    assert kwargs["connection_string"] == "postgresql://user:pass@localhost:5432/db"

    print("  ✅ Source classes tests passed!\n")


def test_registry():
    """Test source registry and registration."""
    from haive.core.engine.document.config import LoaderPreference
    from haive.core.engine.document.loaders.sources.registry import (
        SourceRegistry,
        register_source,
        source_registry,
    )
    from haive.core.engine.document.loaders.sources.source_base import LocalSource

    print("📋 Testing Registry...")

    # Clear the global registry
    source_registry._sources.clear()
    source_registry._extension_index.clear()
    source_registry._url_pattern_index.clear()
    source_registry._scheme_index.clear()
    source_registry._mime_index.clear()

    # Register a PDF source using decorator
    @register_source(
        name="pdf",
        file_extensions=[".pdf"],
        mime_types=["application/pdf"],
        loaders={
            "fast": "PyPDFLoader",
            "quality": {
                "class": "UnstructuredPDFLoader",
                "quality": "high",
                "speed": "slow",
                "requires_packages": ["unstructured"],
            },
        },
        default_loader="fast",
        priority=10,
    )
    class PDFSource(LocalSource):
        """PDF source for testing."""

        pass

    print(f"  ✓ Registered PDF source")

    # Test finding source by path
    registration = source_registry.find_source_for_path("/path/to/document.pdf")
    print(
        f"  ✓ Found source: {registration.name} with {len(registration.loaders)} loaders"
    )
    assert registration.name == "pdf"
    assert len(registration.loaders) == 2

    # Test creating source
    source = source_registry.create_source("/path/to/document.pdf")
    print(f"  ✓ Created source: {source.source_type} for {source.file_path}")
    assert source.source_type == "pdf"
    assert source.file_path == "/path/to/document.pdf"

    # Test loader selection
    fast_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.SPEED
    )
    quality_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.QUALITY
    )

    print(f"  ✓ Speed preference: {fast_loader.name} ({fast_loader.speed})")
    print(f"  ✓ Quality preference: {quality_loader.name} ({quality_loader.quality})")

    assert fast_loader.name == "PyPDFLoader"
    assert quality_loader.name == "UnstructuredPDFLoader"

    print("  ✅ Registry tests passed!\n")


def test_auto_factory():
    """Test the document loader factory."""
    from haive.core.engine.document.loaders.auto_factory import DocumentLoaderFactory

    print("🏭 Testing Auto Factory...")

    factory = DocumentLoaderFactory()

    # Test path analysis with sources
    analysis = factory.analyze_path_with_sources("/path/to/document.pdf")

    print(f"  ✓ Analyzed path: {analysis['path']}")
    print(f"  ✓ Source found: {analysis['source']['name']}")
    print(f"  ✓ Available loaders: {list(analysis['loaders'].keys())}")

    assert analysis["source"]["name"] == "pdf"
    assert "fast" in analysis["loaders"]
    assert "quality" in analysis["loaders"]

    # Test available loaders lookup
    loaders = factory.find_available_loaders("/path/to/document.pdf")
    print(f"  ✓ Available loaders for PDF: {loaders}")
    assert "fast" in loaders
    assert "quality" in loaders

    # Test source creation via factory
    source = factory.create_source("/path/to/document.pdf")
    print(f"  ✓ Factory created source: {source.source_type}")
    assert source.source_type == "pdf"

    print("  ✅ Auto factory tests passed!\n")


def test_complete_workflow():
    """Test the complete workflow end-to-end."""
    from haive.core.engine.document.loaders.auto_factory import analyze_document_source

    print("🔄 Testing Complete Workflow...")

    # Test the convenience function
    result = analyze_document_source("/path/to/document.pdf")

    print(f"  ✓ Complete analysis:")
    print(f"    - Path: {result['path']}")
    print(f"    - Path type: {result['analysis']['path_type']}")
    print(f"    - File extension: {result['analysis']['file_extension']}")
    print(f"    - Source: {result['source']['name']}")
    print(f"    - Loaders: {list(result['loaders'].keys())}")

    assert result["source"]["name"] == "pdf"
    assert result["analysis"]["file_extension"] == ".pdf"
    assert len(result["loaders"]) == 2

    print("  ✅ Complete workflow tests passed!\n")


def main():
    """Run all tests."""
    print("🚀 Testing Document Loader Architecture\n")
    print("=" * 50)

    try:
        test_path_analyzer()
        test_source_classes()
        test_registry()
        test_auto_factory()
        test_complete_workflow()

        print("=" * 50)
        print(
            "🎉 ALL TESTS PASSED! The document loader architecture is working correctly!"
        )
        print("\n✨ Key features verified:")
        print("  • Path analysis and auto-detection")
        print("  • Source registration with decorators")
        print("  • Loader mapping and selection")
        print("  • Auto factory for easy usage")
        print("  • Complete end-to-end workflow")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
