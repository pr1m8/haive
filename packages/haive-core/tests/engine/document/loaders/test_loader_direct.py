"""Direct test of document loader components without package imports."""

import importlib.util
import sys
from pathlib import Path


# Direct file imports to avoid package __init__.py issues
def import_module_from_file(module_name, file_path):
    """Import a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Import modules directly
base_path = Path(
    "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core"
)

# Import required dependencies first
config_module = import_module_from_file(
    "haive.core.engine.document.config", base_path / "engine" / "document" / "config.py"
)

path_analyzer_module = import_module_from_file(
    "haive.core.engine.document.loaders.path_analyzer",
    base_path / "engine" / "document" / "loaders" / "path_analyzer.py",
)

source_base_module = import_module_from_file(
    "haive.core.engine.document.loaders.sources.source_base",
    base_path / "engine" / "document" / "loaders" / "sources" / "source_base.py",
)

registry_module = import_module_from_file(
    "haive.core.engine.document.loaders.sources.registry",
    base_path / "engine" / "document" / "loaders" / "sources" / "registry.py",
)

auto_factory_module = import_module_from_file(
    "haive.core.engine.document.loaders.auto_factory",
    base_path / "engine" / "document" / "loaders" / "auto_factory.py",
)


def test_path_analyzer():
    """Test path analyzer functionality."""
    PathAnalyzer = path_analyzer_module.PathAnalyzer
    PathType = path_analyzer_module.PathType
    FileCategory = path_analyzer_module.FileCategory

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
    service = result.url_components.get("service") if result.url_components else None
    print(f"  ✓ GitHub URL - Service: {service}, Extension: {result.file_extension}")
    assert service == "github"
    assert result.file_extension == ".md"

    # Test database URI
    result = PathAnalyzer.analyze("postgresql://user:pass@localhost:5432/db")
    print(f"  ✓ Database URI - Type: {result.path_type}")
    assert result.path_type == PathType.DATABASE_URI

    print("  ✅ PathAnalyzer tests passed!\n")


def test_source_classes():
    """Test source base classes."""
    LocalSource = source_base_module.LocalSource
    RemoteSource = source_base_module.RemoteSource
    DatabaseSource = source_base_module.DatabaseSource

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
    SourceRegistry = registry_module.SourceRegistry
    register_source = registry_module.register_source
    source_registry = registry_module.source_registry
    LocalSource = source_base_module.LocalSource
    LoaderPreference = config_module.LoaderPreference

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
            "fast": {"class": "PyPDFLoader", "speed": "fast", "quality": "medium"},
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

    # Debug loader mapping
    registration = source_registry._sources["pdf"]
    print(f"  ✓ Debug - Available loaders: {list(registration.loaders.keys())}")
    for name, loader in registration.loaders.items():
        print(
            f"      {name}: {loader.name} (speed={loader.speed}, quality={loader.quality})"
        )

    assert fast_loader.name == "PyPDFLoader"
    # The quality preference should select the high quality loader
    assert quality_loader.name == "UnstructuredPDFLoader"

    print("  ✅ Registry tests passed!\n")


def test_auto_factory():
    """Test the document loader factory."""
    DocumentLoaderFactory = auto_factory_module.DocumentLoaderFactory

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
    analyze_document_source = auto_factory_module.analyze_document_source

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
    print("🚀 Testing Document Loader Architecture (Direct Import)\n")
    print("=" * 55)

    try:
        test_path_analyzer()
        test_source_classes()
        test_registry()
        test_auto_factory()
        test_complete_workflow()

        print("=" * 55)
        print(
            "🎉 ALL TESTS PASSED! The document loader architecture is working correctly!"
        )
        print("\n✨ Key features verified:")
        print("  • Path analysis and auto-detection")
        print("  • Source registration with decorators")
        print("  • Loader mapping and selection")
        print("  • Auto factory for easy usage")
        print("  • Complete end-to-end workflow")

        return True

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILURE'}")
    exit(0 if success else 1)
