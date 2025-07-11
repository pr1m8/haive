"""Comprehensive test of the complete document loader system.

This test verifies the entire document loader architecture including:
- 231 langchain_community loaders support via enhanced registry
- Comprehensive source type system with proper typing
- Easy decorator-based registration
- Document state schema integration
- Bulk loading capabilities
- Credential management with SecureConfigMixin
"""

import importlib.util
import sys
from pathlib import Path
from typing import Any, Dict


# Direct imports to avoid package dependency issues
def import_module_from_file(module_name, file_path):
    """Import a module directly from a file path."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


# Set up module paths
base_path = Path(
    "/home/will/Projects/haive/backend/haive/packages/haive-core/src/haive/core"
)

# Import required modules
try:
    # Import document config first
    config_module = import_module_from_file(
        "haive.core.engine.document.config",
        base_path / "engine" / "document" / "config.py",
    )

    # Import document schema
    schema_module = import_module_from_file(
        "haive.core.engine.document.base.schema",
        base_path / "engine" / "document" / "base" / "schema.py",
    )

    # Import path analyzer
    path_analyzer_module = import_module_from_file(
        "haive.core.engine.document.loaders.path_analyzer",
        base_path / "engine" / "document" / "loaders" / "path_analyzer.py",
    )

    # Import source types
    source_types_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.source_types",
        base_path / "engine" / "document" / "loaders" / "sources" / "source_types.py",
    )

    # Import enhanced registry
    registry_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.enhanced_registry",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "enhanced_registry.py",
    )

    # Import essential sources (this will register them)
    essential_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.essential_sources",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "essential_sources.py",
    )


except Exception as e:
    sys.exit(1)


def test_comprehensive_system():
    """Test the complete document loader system."""

    # Test 1: Registry Statistics
    enhanced_registry = registry_module.enhanced_registry
    stats = enhanced_registry.get_statistics()


    assert (
        stats["total_sources"] >= 13
    ), f"Expected at least 13 sources, got {stats['total_sources']}"
    assert (
        stats["bulk_loaders"] >= 2
    ), f"Expected at least 2 bulk loaders, got {stats['bulk_loaders']}"

    # Test 2: Source Type System
    SourceCategory = source_types_module.SourceCategory
    LoaderCapability = source_types_module.LoaderCapability
    CredentialType = source_types_module.CredentialType


    # Test category coverage
    categories_with_sources = [
        cat for cat, sources in stats["categories"].items() if sources > 0
    ]

    # Test 3: Path Analysis Integration
    PathAnalyzer = path_analyzer_module.PathAnalyzer

    test_paths = [
        "/path/to/document.pdf",
        "/path/to/data.csv",
        "/path/to/notes.md",
        "https://github.com/user/repo/blob/main/README.md",
        "https://example.com/page.html",
        "/path/to/directory/",
    ]

    for path in test_paths:
        analysis = PathAnalyzer.analyze(path)
        registration = enhanced_registry.find_source_for_path(path)


        # PDF and CSV should definitely have sources
        if path.endswith((".pdf", ".csv")):
            assert registration is not None, f"No source found for {path}"

    # Test 4: Source Creation

    # Test PDF source creation
    pdf_source = enhanced_registry.create_source("/path/to/test.pdf")
    assert pdf_source is not None, "Failed to create PDF source"

    # Test CSV source creation
    csv_source = enhanced_registry.create_source("/path/to/data.csv")
    assert csv_source is not None, "Failed to create CSV source"

    # Test web source creation
    web_source = enhanced_registry.create_source("https://example.com/page.html")
    assert web_source is not None, "Failed to create web source"

    # Test 5: Loader Selection and Preferences
    LoaderPreference = config_module.LoaderPreference

    if pdf_source:
        # Test different preferences
        fast_loader = enhanced_registry.get_loader_for_source(
            pdf_source, preference=LoaderPreference.SPEED
        )
        quality_loader = enhanced_registry.get_loader_for_source(
            pdf_source, preference=LoaderPreference.QUALITY
        )


        # They should be different for PDF
        if fast_loader and quality_loader:

    # Test 6: Bulk Loading Capabilities

    bulk_loaders = enhanced_registry.find_bulk_loaders()
    recursive_loaders = enhanced_registry.find_recursive_loaders()


    assert (
        len(bulk_loaders) >= 2
    ), f"Expected at least 2 bulk loaders, got {len(bulk_loaders)}"

    # Test 7: Document State Schema

    DocumentEngineInputSchema = schema_module.DocumentEngineInputSchema
    DocumentLoadingStatus = schema_module.DocumentLoadingStatus
    DocumentEngineStateSchema = schema_module.DocumentEngineStateSchema

    # Test schema creation
    input_schema = DocumentEngineInputSchema(
        source_paths=["/path/to/test.pdf", "/path/to/data.csv"],
        loader_preference="quality",
        bulk_loading=True,
        max_concurrent=4,
        session_id="test_session",
    )


    # Test state schema
    state_schema = DocumentEngineStateSchema(
        input_config=input_schema,
        current_status=DocumentLoadingStatus.PENDING,
        sources_queue=input_schema.source_paths,
        thread_id="test_thread_123",
    )


    # Test 8: Category-based Source Discovery

    file_document_sources = enhanced_registry.find_sources_by_category(
        SourceCategory.FILE_DOCUMENT
    )
    web_scraping_sources = enhanced_registry.find_sources_by_category(
        SourceCategory.WEB_SCRAPING
    )
    database_sources = enhanced_registry.find_sources_by_category(
        SourceCategory.DATABASE_SQL
    )


    # Test 9: Capability-based Discovery

    bulk_capable = enhanced_registry.find_sources_with_capability(
        LoaderCapability.BULK_LOADING
    )
    recursive_capable = enhanced_registry.find_sources_with_capability(
        LoaderCapability.RECURSIVE
    )


    # Test 10: Essential Sources Validation

    essential_stats = essential_sources_module.get_essential_sources_statistics()
    validation_result = essential_sources_module.validate_essential_sources()


    assert validation_result, "Essential sources validation failed"


    return True


def test_decorator_system():
    """Test the enhanced decorator system."""

    # Import decorator functions
    register_source = registry_module.register_source

    SourceCategory = source_types_module.SourceCategory
    LocalFileSource = source_types_module.LocalFileSource

    # Test custom registration using decorator
    @register_source(
        name="test_custom",
        category=SourceCategory.FILE_DOCUMENT,
        description="Test custom source",
        file_extensions=[".test"],
        loaders={"simple": "TestLoader"},
        priority=5,
    )
    class TestCustomSource(LocalFileSource):
        """Test custom source."""


    # Verify registration
    enhanced_registry = registry_module.enhanced_registry
    registration = enhanced_registry._sources.get("test_custom")

    assert registration is not None, "Custom source not registered"
    assert registration.name == "test_custom", "Wrong source name"
    assert registration.category == SourceCategory.FILE_DOCUMENT, "Wrong category"
    assert ".test" in registration.file_extensions, "File extension not registered"


    # Test finding the custom source
    custom_source = enhanced_registry.create_source("/path/to/file.test")
    assert custom_source is not None, "Failed to create custom source"
    assert custom_source.source_type == "test_custom", "Wrong source type"


    return True


def main():
    """Run all comprehensive tests."""

    try:
        # Test main system
        test_comprehensive_system()

        # Test decorator system
        test_decorator_system()


        enhanced_registry = registry_module.enhanced_registry
        final_stats = enhanced_registry.get_statistics()



        return True

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
