"""Test the complete web loaders system with sitemap detection.

This test validates:
- Sitemap auto-detection from legacy system
- Browser automation capabilities
- Recursive web crawling
- Documentation site processing
- Auto-classification for web sources
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

    # Import essential sources first
    essential_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.essential_sources",
        base_path
        / "engine"
        / "document"
        / "loaders"
        / "sources"
        / "essential_sources.py",
    )

    # Import web sources (this registers all web-based sources)
    web_sources_module = import_module_from_file(
        "haive.core.engine.document.loaders.sources.web_sources",
        base_path / "engine" / "document" / "loaders" / "sources" / "web_sources.py",
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


def test_web_loaders_system():
    """Test the complete web loaders system."""

    enhanced_registry = registry_module.enhanced_registry
    LoaderCapability = source_types_module.LoaderCapability
    SourceCategory = source_types_module.SourceCategory

    # Test 1: Web Sources Registration
    web_stats = web_sources_module.get_web_sources_statistics()
    web_validation = web_sources_module.validate_web_sources()


    assert web_validation, "Web source validation failed"
    assert (
        web_stats["total_web_sources"] >= 8
    ), f"Expected at least 8 web sources, got {web_stats['total_web_sources']}"
    assert (
        web_stats["capabilities"]["browser_automation"] >= 3
    ), "Expected browser automation support"

    # Test 2: Sitemap Detection (Legacy Integration)

    find_sitemap = web_sources_module.find_sitemap

    # Test sitemap detection function

    # Test with known sites (these should work if network available)
    test_sitemap_sites = [
        "https://python.org",
        "https://docs.python.org",
        "https://langchain-ai.github.io/langgraph",
    ]

    sitemap_found_count = 0
    for site in test_sitemap_sites:
        try:
            sitemap_url = find_sitemap(site)
            if sitemap_url:
                sitemap_found_count += 1
            else:
                passnd")
        except Exception as e:
            pass {e}")


    # Test 3: Web Source Auto-Classification

    web_test_urls = {
        "https://example.com": "web_base",  # Simple site
        "https://docs.python.org": "sitemap_crawler",  # Has sitemap
        "https://spa-app.example.com": "playwright_web",  # JavaScript heavy
        "https://api.example.com": "web_base",  # API endpoint
    }

    classification_success = 0
    for url, _expected_type in web_test_urls.items():
        try:
            source = enhanced_registry.create_source(url)
            if source:
                actual_type = source.source_type
                if "web" in actual_type or "sitemap" in actual_type:
                    classification_success += 1
            else:
                passed")
        except Exception as e:
            pass {e}")


    # Test 4: Browser Automation Sources

    browser_sources = ["playwright_web", "selenium_web", "chromium_async"]

    for source_name in browser_sources:
        registration = enhanced_registry._sources.get(source_name)
        if registration:
            capabilities = registration.capabilities.capabilities
            has_async = LoaderCapability.ASYNC_PROCESSING in capabilities
            requires_packages = any(
                loader.requires_packages
                for loader in registration.loaders.values()
                if hasattr(loader, "requires_packages") and loader.requires_packages
            )
        else:
            pass")

    # Test 5: Recursive Crawling Configuration

    # Test recursive web source
    try:
        recursive_source = enhanced_registry.create_source("https://example.com")
        if recursive_source and hasattr(recursive_source, "source_type"):

            # Test with different configuration
            recursive_registration = enhanced_registry._sources.get("recursive_web")
            if recursive_registration:
                bulk_info = recursive_registration.bulk_info
        else:
            passce")
    except Exception as e:
        passe}")

    # Test 6: Documentation Site Sources

    doc_sources = ["readthedocs", "docusaurus", "sitemap_crawler"]

    for source_name in doc_sources:
        registration = enhanced_registry._sources.get(source_name)
        if registration:
            category = registration.category
            is_bulk = registration.bulk_info.supports_bulk
        else:
            pass")

    # Test 7: Metadata Extraction

    extract_metadata = web_sources_module.extract_metadata_from_html

    # Test metadata extraction function
    sample_html = """
    <html lang="en">
    <head>
        <title>Test Page</title>
        <meta name="description" content="Test description">
        <meta name="keywords" content="test, sample">
        <meta name="author" content="Test Author">
    </head>
    <body>Content</body>
    </html>
    """

    class MockResponse:
        headers = {"Content-Type": "text/html"}

    metadata = extract_metadata(sample_html, "https://example.com", MockResponse())

    assert "title" in metadata, "Title not extracted"
    assert "description" in metadata, "Description not extracted"
    assert metadata["title"] == "Test Page", "Incorrect title extraction"

    # Test 8: Web Crawler Capabilities

    # Check for bulk web crawling capabilities
    web_bulk_sources = []
    for name, registration in enhanced_registry._sources.items():
        if (
            registration.category
            in [SourceCategory.WEB_SCRAPING, SourceCategory.WEB_DOCUMENTATION]
            and registration.bulk_info.supports_bulk
        ):
            web_bulk_sources.append(name)


    assert (
        len(web_bulk_sources) >= 3
    ), f"Expected at least 3 bulk web sources, got {len(web_bulk_sources)}"

    # Test 9: Advanced Web Features

    # Check for advanced capabilities
    async_web_sources = []
    filtering_web_sources = []

    for name, registration in enhanced_registry._sources.items():
        if registration.category in [
            SourceCategory.WEB_SCRAPING,
            SourceCategory.WEB_DOCUMENTATION,
        ]:
            capabilities = registration.capabilities.capabilities
            if LoaderCapability.ASYNC_PROCESSING in capabilities:
                async_web_sources.append(name)
            if LoaderCapability.FILTERING in capabilities:
                filtering_web_sources.append(name)


    # Test 10: Integration with Overall System

    # Check overall statistics
    overall_stats = enhanced_registry.get_statistics()
    web_percentage = (
        web_stats["total_web_sources"] / overall_stats["total_sources"]
    ) * 100


    assert (
        web_percentage >= 15
    ), f"Web sources should be at least 15% of total, got {web_percentage:.1f}%"


    return True


def display_web_system_summary():
    """Display comprehensive summary of the web loader system."""

    web_stats = web_sources_module.get_web_sources_statistics()








def main():
    """Run comprehensive web loaders tests."""
    try:
        # Test the web system
        success = test_web_loaders_system()

        if success:
            # Display comprehensive summary
            display_web_system_summary()
            return True
        print("❌ Web system tests failed")
        return False

    except Exception as e:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
