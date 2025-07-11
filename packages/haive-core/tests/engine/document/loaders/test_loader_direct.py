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

    # Test PDF file
    result = PathAnalyzer.analyze("/path/to/document.pdf")
    assert result.path_type == PathType.LOCAL_FILE
    assert result.file_extension == ".pdf"
    assert result.file_category == FileCategory.DOCUMENT

    # Test GitHub URL
    result = PathAnalyzer.analyze("https://github.com/user/repo/blob/main/README.md")
    service = result.url_components.get("service") if result.url_components else None
    assert service == "github"
    assert result.file_extension == ".md"

    # Test database URI
    result = PathAnalyzer.analyze("postgresql://user:pass@localhost:5432/db")
    assert result.path_type == PathType.DATABASE_URI


def test_source_classes():
    """Test source base classes."""
    LocalSource = source_base_module.LocalSource
    RemoteSource = source_base_module.RemoteSource
    DatabaseSource = source_base_module.DatabaseSource

    # Test LocalSource
    pdf_source = LocalSource(
        source_type="pdf",
        source_id="test_pdf",
        file_path="/path/to/test.pdf",
        encoding="utf-8",
    )

    kwargs = pdf_source.get_loader_kwargs()
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
    assert kwargs["url"] == "https://example.com/page.html"

    # Test DatabaseSource
    db_source = DatabaseSource(
        source_type="database",
        source_id="test_db",
        connection_string="postgresql://user:pass@localhost:5432/db",
        provider="postgresql",
    )

    kwargs = db_source.get_loader_kwargs()
    assert kwargs["connection_string"] == "postgresql://user:pass@localhost:5432/db"


def test_registry():
    """Test source registry and registration."""
    register_source = registry_module.register_source
    source_registry = registry_module.source_registry
    LocalSource = source_base_module.LocalSource
    LoaderPreference = config_module.LoaderPreference

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

    # Test finding source by path
    registration = source_registry.find_source_for_path("/path/to/document.pdf")
    assert registration.name == "pdf"
    assert len(registration.loaders) == 2

    # Test creating source
    source = source_registry.create_source("/path/to/document.pdf")
    assert source.source_type == "pdf"
    assert source.file_path == "/path/to/document.pdf"

    # Test loader selection
    fast_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.SPEED
    )
    quality_loader = source_registry.get_loader_for_source(
        source, preference=LoaderPreference.QUALITY
    )

    # Debug loader mapping
    registration = source_registry._sources["pdf"]
    for _name, _loader in registration.loaders.items():
        pass

    assert fast_loader.name == "PyPDFLoader"
    # The quality preference should select the high quality loader
    assert quality_loader.name == "UnstructuredPDFLoader"


def test_auto_factory():
    """Test the document loader factory."""
    DocumentLoaderFactory = auto_factory_module.DocumentLoaderFactory

    factory = DocumentLoaderFactory()

    # Test path analysis with sources
    analysis = factory.analyze_path_with_sources("/path/to/document.pdf")

    assert analysis["source"]["name"] == "pdf"
    assert "fast" in analysis["loaders"]
    assert "quality" in analysis["loaders"]

    # Test available loaders lookup
    loaders = factory.find_available_loaders("/path/to/document.pdf")
    assert "fast" in loaders
    assert "quality" in loaders

    # Test source creation via factory
    source = factory.create_source("/path/to/document.pdf")
    assert source.source_type == "pdf"


def test_complete_workflow():
    """Test the complete workflow end-to-end."""
    analyze_document_source = auto_factory_module.analyze_document_source

    # Test the convenience function
    result = analyze_document_source("/path/to/document.pdf")

    assert result["source"]["name"] == "pdf"
    assert result["analysis"]["file_extension"] == ".pdf"
    assert len(result["loaders"]) == 2


def main():
    """Run all tests."""
    try:
        test_path_analyzer()
        test_source_classes()
        test_registry()
        test_auto_factory()
        test_complete_workflow()

        return True

    except Exception:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
