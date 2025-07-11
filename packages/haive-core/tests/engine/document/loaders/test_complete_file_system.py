"""Comprehensive test of the complete file and bulk loading system.

This test validates:
- All file-based sources with unstructured processing
- Generic and fallback loaders
- Code language auto-detection
- Bulk loading with "scrape all" capabilities
- Cloud storage integration
- Advanced filtering and processing
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


try:
    # Import all required modules

    # Import essential sources first (this registers basic sources)
    essential_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.essential_sources",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "essential_sources.py",
    )

    # Import file sources (this registers all file-based sources)
    file_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.file_sources",
        base_path / "engine" / "document" / "loaders" / "sources" / "file_sources.py",
    )

    # Import bulk sources (this registers all bulk loading sources)
    bulk_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.bulk_sources",
        base_path / "engine" / "document" / "loaders" / "sources" / "bulk_sources.py",
    )

    # Import registry for testing
    registry_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.enhanced_registry",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "enhanced_registry.py",
    )

    # Import source types for testing
    source_types_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.source_types",
        base_path / "engine" / "document" / "loaders" / "sources" / "source_types.py",
    )


except Exception as e:
    import traceback

    traceback.print_exc()
    sys.exit(1)


def test_complete_file_system():
    """Test the complete file and bulk loading system."""

    enhanced_registry = registry_module.enhanced_registry
    LoaderCapability = source_types_module.LoaderCapability
    SourceCategory = source_types_module.SourceCategory

    # Test 1: Overall Registry Statistics
    stats = enhanced_registry.get_statistics()


    # Should have significantly more sources now
    assert (
        stats["total_sources"] >= 30
    ), f"Expected at least 30 sources, got {stats['total_sources']}"
    assert (
        stats["bulk_loaders"] >= 8
    ), f"Expected at least 8 bulk loaders, got {stats['bulk_loaders']}"
    assert (
        stats["extensions_covered"] >= 25
    ), f"Expected at least 25 extensions, got {stats['extensions_covered']}"

    # Test 2: File Source Validation
    file_stats = file_sources_module.get_file_sources_statistics()
    file_validation = file_sources_module.validate_file_sources()


    assert file_validation, "File source validation failed"
    assert (
        file_stats["unstructured_loaders"] >= 5
    ), "Expected at least 5 unstructured loaders"

    # Test 3: Bulk Loading System
    bulk_stats = bulk_sources_module.get_bulk_sources_statistics()
    bulk_validation = bulk_sources_module.validate_bulk_sources()
    scrape_all_sources = bulk_sources_module.get_scrape_all_sources()


    assert bulk_validation, "Bulk source validation failed"
    assert (
        len(scrape_all_sources) >= 6
    ), f"Expected at least 6 'scrape all' sources, got {len(scrape_all_sources)}"
    assert (
        bulk_stats["max_concurrency_available"] >= 8
    ), "Expected high concurrency support"

    # Test 4: Unstructured File Processing

    unstructured_sources = [
        "unstructured_file",
        "powerpoint",
        "email",
        "epub",
        "image_document",
        "xml_data",
        "chm_help",
    ]

    for source_name in unstructured_sources:
        registration = enhanced_registry._sources.get(source_name)
        if registration:
            # Check for unstructured capabilities
            has_unstructured = any(
                "unstructured" in loader.name.lower()
                for loader in registration.loaders.values()
            )
            if has_unstructured:
                pass")
        else:
            pass")

    # Test 5: Generic and Fallback Loaders

    # Test generic file source
    generic_source = enhanced_registry.create_source("/path/to/unknown.xyz")
    if generic_source:
        pass")
    else:
        pass")

    # Test known file types
    test_files = {
        "/path/to/code.py": "python_code",
        "/path/to/notebook.ipynb": "notebook",
        "/path/to/presentation.pptx": "powerpoint",
        "/path/to/email.eml": "email",
        "/path/to/book.epub": "epub",
        "/path/to/config.toml": "toml_config",
        "/path/to/data.xml": "xml_data",
    }

    for file_path, expected_source in test_files.items():
        source = enhanced_registry.create_source(file_path)
        if source and source.source_type == expected_source:
            passe}")
        else:
            actual = source.source_type if source else "None"

    # Test 6: Code Language Detection

    code_files = [
        "/path/to/script.py",
        "/path/to/analysis.ipynb",
        "/path/to/config.yaml",
        "/path/to/settings.toml",
    ]

    for code_file in code_files:
        source = enhanced_registry.create_source(code_file)
        if source:
            passe}")
        else:
            pass")

    # Test 7: Bulk Processing Capabilities

    bulk_test_sources = [
        ("recursive_directory", "Advanced recursive processing"),
        ("pdf_directory", "Bulk PDF processing"),
        ("s3_bucket", "AWS S3 bulk loading"),
        ("gcs_bucket", "Google Cloud bulk loading"),
        ("azure_container", "Azure Blob bulk loading"),
        ("filesystem_blob", "Binary file processing"),
        ("streaming_directory", "Real-time processing"),
    ]

    for source_name, description in bulk_test_sources:
        registration = enhanced_registry._sources.get(source_name)
        if registration:
            capabilities = registration.capabilities.capabilities
            is_bulk = LoaderCapability.BULK_LOADING in capabilities
            is_recursive = LoaderCapability.RECURSIVE in capabilities
            max_concurrent = registration.bulk_info.max_concurrent

        else:
            pass")

    # Test 8: Advanced Filtering and Processing

    # Check OCR capabilities
    ocr_sources = enhanced_registry.find_sources_with_capability(LoaderCapability.OCR)

    # Check metadata extraction
    metadata_sources = enhanced_registry.find_sources_with_capability(
        LoaderCapability.METADATA_EXTRACTION
    )

    # Check streaming capabilities
    streaming_sources = enhanced_registry.find_sources_with_capability(
        LoaderCapability.STREAMING
    )

    # Check async processing
    async_sources = enhanced_registry.find_sources_with_capability(
        LoaderCapability.ASYNC_PROCESSING
    )

    # Test 9: Category Coverage

    category_coverage = {}
    for category in SourceCategory:
        sources = enhanced_registry.find_sources_by_category(category)
        if sources:
            category_coverage[category.value] = len(sources)

    # Should have good coverage across categories
    assert (
        len(category_coverage) >= 8
    ), f"Expected coverage of at least 8 categories, got {len(category_coverage)}"

    # Test 10: Performance and Concurrency

    # Find highest concurrency sources
    max_concurrency = 0
    fastest_sources = []
    quality_sources = []

    for name, registration in enhanced_registry._sources.items():
        if registration.bulk_info.supports_bulk:
            concurrency = registration.bulk_info.max_concurrent
            max_concurrency = max(max_concurrency, concurrency)

            # Find fast loaders
            for loader in registration.loaders.values():
                if loader.speed == "fast":
                    fastest_sources.append(name)
                if loader.quality == "high":
                    quality_sources.append(name)


    assert (
        max_concurrency >= 8
    ), f"Expected high concurrency support, got {max_concurrency}"


    return True


def display_comprehensive_summary():
    """Display comprehensive summary of the complete system."""

    enhanced_registry = registry_module.enhanced_registry

    # Get all statistics
    overall_stats = enhanced_registry.get_statistics()
    file_stats = file_sources_module.get_file_sources_statistics()
    bulk_stats = bulk_sources_module.get_bulk_sources_statistics()
    scrape_all_sources = bulk_sources_module.get_scrape_all_sources()






    for source in scrape_all_sources:
        registration = enhanced_registry._sources[source]
        concurrency = registration.bulk_info.max_concurrent



def main():
    """Run comprehensive file and bulk loading tests."""
    try:
        # Test the complete system
        success = test_complete_file_system()

        if success:
            # Display comprehensive summary
            display_comprehensive_summary()
            return True
        print("❌ System tests failed")
        return False

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
