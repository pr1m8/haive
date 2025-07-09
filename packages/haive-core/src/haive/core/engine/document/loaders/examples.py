"""Comprehensive examples for the Haive Document Loaders system.

This module provides detailed examples showing how to use the ultimate auto-loading
system with all 230+ supported document loaders. Examples cover basic usage,
advanced configurations, performance optimization, and real-world scenarios.

Author: Claude (Haive Document Loader System)
Version: 1.0.0
"""

import asyncio

from .auto_loader import (
    AutoLoader,
    AutoLoaderConfig,
    aload_document,
    load_document,
    load_documents_bulk,
)
from .auto_registry import (
    auto_register_all,
    get_registration_status,
    get_sources_by_category,
    list_available_sources,
)
from .sources.enhanced_registry import LoaderPreference
from .sources.source_types import SourceCategory

# =============================================================================
# Basic Usage Examples
# =============================================================================


def example_basic_auto_loading():
    """Basic auto-loading examples for common use cases."""
    print("🚀 Basic Auto-Loading Examples")
    print("=" * 50)

    # Initialize the auto-loader
    loader = AutoLoader()

    # Example 1: Load a single PDF document
    print("\n📄 Example 1: Load PDF Document")
    try:
        documents = loader.load("/path/to/document.pdf")
        print(f"✅ Loaded {len(documents)} documents from PDF")
        for i, doc in enumerate(documents[:2]):  # Show first 2
            print(f"   Document {i+1}: {doc.page_content[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 2: Load from a website
    print("\n🌐 Example 2: Load from Website")
    try:
        documents = loader.load("https://python.org/about/")
        print(f"✅ Loaded {len(documents)} documents from website")
        print(f"   Sample content: {documents[0].page_content[:100]}...")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 3: Load from cloud storage
    print("\n☁️ Example 3: Load from S3")
    try:
        documents = loader.load(
            "s3://my-bucket/documents/report.pdf",
            aws_access_key_id="your-access-key",
            aws_secret_access_key="your-secret-key",
        )
        print(f"✅ Loaded {len(documents)} documents from S3")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Example 4: Load from database
    print("\n🗄️ Example 4: Load from Database")
    try:
        documents = loader.load(
            "postgresql://user:password@localhost:5432/mydb",
            query="SELECT content, title FROM documents WHERE category = 'research'",
        )
        print(f"✅ Loaded {len(documents)} documents from database")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_convenience_functions():
    """Examples using convenience functions for quick loading."""
    print("\n⚡ Convenience Functions Examples")
    print("=" * 50)

    # Simple one-liner loading
    print("\n📋 One-liner loading:")
    try:
        docs = load_document("document.pdf")
        print(f"✅ Loaded {len(docs)} documents with one line")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Bulk loading multiple sources
    print("\n📦 Bulk loading:")
    try:
        sources = ["file1.pdf", "file2.docx", "https://example.com"]
        docs = load_documents_bulk(sources)
        print(f"✅ Bulk loaded {len(docs)} documents from {len(sources)} sources")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Async loading
    print("\n🚀 Async loading:")

    async def async_example():
        try:
            docs = await aload_document("https://example.com")
            print(f"✅ Async loaded {len(docs)} documents")
        except Exception as e:
            print(f"❌ Error: {e}")

    asyncio.run(async_example())


# =============================================================================
# Advanced Configuration Examples
# =============================================================================


def example_configuration_options():
    """Examples of different configuration options."""
    print("\n🔧 Advanced Configuration Examples")
    print("=" * 50)

    # Speed-optimized configuration
    print("\n🏎️ Speed-optimized configuration:")
    speed_config = AutoLoaderConfig(
        preference=LoaderPreference.SPEED,
        max_concurrency=20,
        timeout=60,
        retry_attempts=1,
        enable_caching=True,
        cache_ttl=3600,
    )
    AutoLoader(speed_config)
    print(f"   Preference: {speed_config.preference.value}")
    print(f"   Max concurrency: {speed_config.max_concurrency}")
    print(f"   Caching enabled: {speed_config.enable_caching}")

    # Quality-optimized configuration
    print("\n🎯 Quality-optimized configuration:")
    quality_config = AutoLoaderConfig(
        preference=LoaderPreference.QUALITY,
        max_concurrency=5,
        timeout=300,
        retry_attempts=5,
        enable_metadata=True,
        default_chunk_size=2000,
    )
    AutoLoader(quality_config)
    print(f"   Preference: {quality_config.preference.value}")
    print(f"   Retry attempts: {quality_config.retry_attempts}")
    print(f"   Chunk size: {quality_config.default_chunk_size}")

    # Balanced configuration
    print("\n⚖️ Balanced configuration:")
    balanced_config = AutoLoaderConfig(
        preference=LoaderPreference.BALANCED,
        max_concurrency=10,
        enable_caching=True,
        enable_metadata=True,
    )
    AutoLoader(balanced_config)
    print(f"   Preference: {balanced_config.preference.value}")
    print("   Balanced settings for speed and quality")


def example_detailed_loading():
    """Examples of detailed loading with metadata."""
    print("\n📊 Detailed Loading Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Get detailed loading information
    print("\n🔍 Detailed loading with metadata:")
    try:
        result = loader.load_detailed("/path/to/document.pdf")

        print(f"   Documents loaded: {len(result.documents)}")
        print(f"   Source type: {result.source_info.source_type}")
        print(f"   Source category: {result.source_info.category.value}")
        print(f"   Loader used: {result.loader_used}")
        print(f"   Loading time: {result.loading_time:.2f} seconds")
        print(f"   Confidence: {result.source_info.confidence:.2f}")
        print(f"   Errors: {len(result.errors)}")

        if result.documents:
            doc = result.documents[0]
            print(f"   Sample metadata: {doc.metadata}")

    except Exception as e:
        print(f"❌ Error: {e}")


# =============================================================================
# Bulk and Concurrent Loading Examples
# =============================================================================


def example_bulk_loading():
    """Examples of bulk loading with different configurations."""
    print("\n📦 Bulk Loading Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Basic bulk loading
    print("\n📋 Basic bulk loading:")
    sources = [
        "/documents/report1.pdf",
        "/documents/report2.docx",
        "/documents/data.csv",
        "https://example.com/page1.html",
        "https://example.com/page2.html",
    ]

    try:
        result = loader.load_bulk(sources)

        print(f"   Total documents: {result.total_documents}")
        print(f"   Successful loads: {result.summary['successful_loads']}")
        print(f"   Failed loads: {result.summary['failed_loads']}")
        print(f"   Success rate: {result.summary['success_rate']:.1f}%")
        print(f"   Total time: {result.total_time:.2f} seconds")
        print(f"   Average time per source: {result.summary['avg_loading_time']:.2f}s")

        if result.failed_sources:
            print("   Failed sources:")
            for source, error in result.failed_sources:
                print(f"     - {source}: {error}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Bulk loading with custom configurations
    print("\n⚙️ Bulk loading with configurations:")
    mixed_sources = [
        "/local/file.pdf",
        {
            "path": "s3://bucket/file.pdf",
            "aws_access_key_id": "key",
            "aws_secret_access_key": "secret",
        },
        {
            "url": "https://api.example.com/data",
            "headers": {"Authorization": "Bearer token"},
            "timeout": 60,
        },
    ]

    try:
        result = loader.load_bulk(mixed_sources, max_workers=5)
        print(f"   Mixed sources loaded: {result.total_documents} documents")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Progress tracking
    print("\n📈 Bulk loading with progress tracking:")

    def progress_callback(completed: int, total: int):
        percentage = (completed / total) * 100
        print(f"   Progress: {completed}/{total} ({percentage:.1f}%)")

    try:
        sources = [f"/test{i}.pdf" for i in range(5)]
        result = loader.load_bulk(sources, progress_callback=progress_callback)
        print(f"   Final result: {result.total_documents} documents")
    except Exception as e:
        print(f"❌ Error: {e}")


def example_scrape_all():
    """Examples of 'scrape all' functionality for bulk processing."""
    print("\n🗂️ Scrape All Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Scrape entire directory
    print("\n📁 Scrape entire directory:")
    try:
        documents = loader.load_all("/path/to/documents/")
        print(f"   Loaded {len(documents)} documents from directory")
        print("   Recursive processing included subdirectories")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Scrape entire website
    print("\n🌐 Scrape entire website:")
    try:
        documents = loader.load_all(
            "https://docs.python.org",
            max_depth=3,
            respect_robots=True,
            include_external_links=False,
        )
        print(f"   Scraped {len(documents)} pages from documentation")
        print("   Limited to depth 3, respecting robots.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Scrape all tables from database
    print("\n🗄️ Scrape all tables from database:")
    try:
        documents = loader.load_all(
            "postgresql://user:pass@host:5432/db",
            include_system_tables=False,
            table_filter="user_*",
        )
        print(f"   Loaded {len(documents)} records from all user tables")
    except Exception as e:
        print(f"❌ Error: {e}")


# =============================================================================
# Async and Performance Examples
# =============================================================================


async def example_async_loading():
    """Examples of asynchronous loading for high performance."""
    print("\n🚀 Async Loading Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Basic async loading
    print("\n⚡ Basic async loading:")
    try:
        documents = await loader.aload("https://example.com/large-document.pdf")
        print(f"   Async loaded {len(documents)} documents")
    except Exception as e:
        print(f"❌ Error: {e}")

    # Concurrent async loading
    print("\n🔄 Concurrent async loading:")
    sources = [
        "https://site1.com/doc.pdf",
        "https://site2.com/doc.pdf",
        "https://site3.com/doc.pdf",
    ]

    try:
        tasks = [loader.aload(source) for source in sources]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        total_docs = 0
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                print(f"   Source {i+1} failed: {result}")
            else:
                total_docs += len(result)
                print(f"   Source {i+1}: {len(result)} documents")

        print(f"   Total documents loaded concurrently: {total_docs}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Async bulk loading
    print("\n📦 Async bulk loading:")
    try:
        sources = [f"https://example.com/doc{i}.pdf" for i in range(5)]
        result = await loader.aload_bulk(sources)

        print(f"   Async bulk loaded: {result.total_documents} documents")
        print(f"   Time saved with async: {result.total_time:.2f}s")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_performance_optimization():
    """Examples of performance optimization techniques."""
    print("\n🏎️ Performance Optimization Examples")
    print("=" * 50)

    # High-concurrency configuration
    print("\n⚡ High-concurrency configuration:")
    perf_config = AutoLoaderConfig(
        preference=LoaderPreference.SPEED,
        max_concurrency=50,
        timeout=30,
        retry_attempts=1,
        enable_caching=True,
        cache_ttl=7200,  # 2 hours
    )
    AutoLoader(perf_config)
    print(f"   Max concurrency: {perf_config.max_concurrency}")
    print("   Fast preference with caching enabled")

    # Caching demonstration
    print("\n💾 Caching performance:")
    cached_loader = AutoLoader(AutoLoaderConfig(enable_caching=True))

    import time

    try:
        # First load (slow)
        start = time.time()
        cached_loader.load("/test.pdf")
        first_time = time.time() - start

        # Second load (fast from cache)
        start = time.time()
        cached_loader.load("/test.pdf")
        second_time = time.time() - start

        print(f"   First load: {first_time:.3f}s")
        print(f"   Cached load: {second_time:.3f}s")
        print(f"   Speed improvement: {first_time/second_time:.1f}x faster")

    except Exception as e:
        print(f"❌ Error: {e}")


# =============================================================================
# Real-World Use Case Examples
# =============================================================================


def example_enterprise_document_processing():
    """Example of enterprise-scale document processing."""
    print("\n🏢 Enterprise Document Processing")
    print("=" * 50)

    # Enterprise configuration
    enterprise_config = AutoLoaderConfig(
        preference=LoaderPreference.QUALITY,
        max_concurrency=20,
        timeout=600,  # 10 minutes for large files
        retry_attempts=3,
        enable_caching=True,
        enable_metadata=True,
    )
    enterprise_loader = AutoLoader(enterprise_config)

    # Mixed enterprise sources
    enterprise_sources = [
        # Local file shares
        "/mnt/shared/reports/quarterly_report.pdf",
        "/mnt/shared/contracts/contract_2024_001.docx",
        # SharePoint documents
        {
            "path": "https://company.sharepoint.com/sites/docs/contract.pdf",
            "client_id": "sharepoint_client_id",
            "client_secret": "sharepoint_secret",
        },
        # Salesforce attachments
        {
            "path": "salesforce://attachments",
            "username": "sf_user",
            "password": "sf_password",
            "security_token": "sf_token",
        },
        # Google Drive documents
        {
            "path": "https://drive.google.com/folder/xyz",
            "service_account_key": "/path/to/service-account.json",
            "recursive": True,
        },
    ]

    print(f"📊 Processing {len(enterprise_sources)} enterprise sources...")

    try:
        result = enterprise_loader.load_bulk(enterprise_sources)

        print(f"   Total documents processed: {result.total_documents}")
        print(f"   Processing time: {result.total_time:.2f} seconds")
        print(f"   Success rate: {result.summary['success_rate']:.1f}%")

        # Analyze results by source type
        source_types = {}
        for loading_result in result.results:
            source_type = loading_result.source_info.source_type
            if source_type not in source_types:
                source_types[source_type] = 0
            source_types[source_type] += len(loading_result.documents)

        print("   Documents by source type:")
        for source_type, count in source_types.items():
            print(f"     - {source_type}: {count} documents")

    except Exception as e:
        print(f"❌ Error: {e}")


def example_research_paper_collection():
    """Example of collecting research papers from multiple sources."""
    print("\n🔬 Research Paper Collection")
    print("=" * 50)

    research_loader = AutoLoader(
        AutoLoaderConfig(
            preference=LoaderPreference.QUALITY,
            enable_metadata=True,
        )
    )

    # Academic sources
    research_sources = [
        # ArXiv papers
        "https://arxiv.org/abs/2024.00001",
        "https://arxiv.org/abs/2024.00002",
        # PubMed articles
        {
            "path": "pubmed://search",
            "query": "machine learning healthcare",
            "limit": 50,
        },
        # Google Scholar
        {
            "path": "scholar://search",
            "query": "neural networks 2024",
            "year_range": "2024-2024",
        },
        # Local PDF collection
        "/research/papers/ml_papers/",
        # University repository
        "https://university.edu/research/papers/",
    ]

    print(f"📚 Collecting research papers from {len(research_sources)} sources...")

    try:
        result = research_loader.load_bulk(research_sources)

        print(f"   Papers collected: {result.total_documents}")

        # Extract metadata for analysis
        papers_by_year = {}
        papers_by_venue = {}

        for loading_result in result.results:
            for doc in loading_result.documents:
                metadata = doc.metadata

                # Group by year
                year = metadata.get("year", "unknown")
                papers_by_year[year] = papers_by_year.get(year, 0) + 1

                # Group by venue/journal
                venue = metadata.get("venue", metadata.get("journal", "unknown"))
                papers_by_venue[venue] = papers_by_venue.get(venue, 0) + 1

        print(f"   Papers by year: {dict(sorted(papers_by_year.items()))}")
        print(
            f"   Top venues: {dict(sorted(papers_by_venue.items(), key=lambda x: x[1], reverse=True)[:5])}"
        )

    except Exception as e:
        print(f"❌ Error: {e}")


def example_legal_document_analysis():
    """Example of legal document processing and analysis."""
    print("\n⚖️ Legal Document Analysis")
    print("=" * 50)

    legal_config = AutoLoaderConfig(
        preference=LoaderPreference.QUALITY,
        enable_metadata=True,
        default_chunk_size=2000,  # Larger chunks for legal text
    )
    legal_loader = AutoLoader(legal_config)

    # Legal document sources
    legal_sources = [
        # Court cases
        {
            "path": "westlaw://cases",
            "jurisdiction": "federal",
            "year_range": "2020-2024",
            "topic": "intellectual property",
        },
        # Legal databases
        {
            "path": "lexis://database",
            "database": "cases",
            "query": "software patents",
        },
        # Government regulations
        "https://federalregister.gov/documents/2024/",
        # Local legal documents
        "/legal/contracts/",
        "/legal/patents/",
        # Law firm documents
        {
            "path": "sharepoint://legal.firm.com/documents",
            "practice_area": "ip",
        },
    ]

    print(f"📖 Processing legal documents from {len(legal_sources)} sources...")

    try:

        def legal_progress(completed, total):
            print(f"   Legal processing: {completed}/{total} sources")

        result = legal_loader.load_bulk(legal_sources, progress_callback=legal_progress)

        print(f"   Legal documents processed: {result.total_documents}")

        # Analyze legal content
        document_types = {}
        jurisdictions = {}

        for loading_result in result.results:
            for doc in loading_result.documents:
                metadata = doc.metadata

                # Classify document types
                doc_type = metadata.get("document_type", "unknown")
                document_types[doc_type] = document_types.get(doc_type, 0) + 1

                # Track jurisdictions
                jurisdiction = metadata.get("jurisdiction", "unknown")
                jurisdictions[jurisdiction] = jurisdictions.get(jurisdiction, 0) + 1

        print(f"   Document types: {document_types}")
        print(f"   Jurisdictions: {jurisdictions}")

    except Exception as e:
        print(f"❌ Error: {e}")


# =============================================================================
# Registry and System Management Examples
# =============================================================================


def example_registry_management():
    """Examples of managing the document loader registry."""
    print("\n📊 Registry Management Examples")
    print("=" * 50)

    # Auto-register all sources
    print("\n🔄 Auto-registering all sources:")
    try:
        stats = auto_register_all()

        print(f"   Modules scanned: {stats.total_modules_scanned}")
        print(f"   Sources found: {stats.total_sources_found}")
        print(f"   Sources registered: {stats.total_sources_registered}")
        print(f"   Registration time: {stats.registration_time:.2f}s")
        print(f"   Categories covered: {stats.categories_covered}")

        if stats.registration_errors:
            print(f"   Registration errors: {len(stats.registration_errors)}")
            for error in stats.registration_errors[:3]:  # Show first 3
                print(f"     - {error}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Get registration status
    print("\n📈 Current registration status:")
    try:
        status = get_registration_status()

        print(f"   Total sources: {status['total_sources']}")
        print(f"   Categories: {status['categories_count']}")
        print(f"   Total errors: {status['total_errors']}")

        print("   Category breakdown:")
        for category, count in status["category_breakdown"].items():
            print(f"     - {category}: {count} sources")

        print("   Recent registrations:")
        for reg in status["recent_registrations"][:3]:
            print(
                f"     - {reg['name']} ({reg['category']}) - {reg['loaders']} loaders"
            )

    except Exception as e:
        print(f"❌ Error: {e}")

    # List available sources
    print("\n📋 Available sources:")
    try:
        sources = list_available_sources()
        print(f"   Total available: {len(sources)}")
        print(f"   Sample sources: {sources[:10]}")  # Show first 10

    except Exception as e:
        print(f"❌ Error: {e}")

    # Sources by category
    print("\n🗂️ Sources by category:")
    try:
        for category in SourceCategory:
            sources = get_sources_by_category(category)
            if sources:
                print(f"   {category.value}: {len(sources)} sources")
                print(f"     Examples: {sources[:5]}")  # Show first 5

    except Exception as e:
        print(f"❌ Error: {e}")


def example_system_capabilities():
    """Examples of checking system capabilities."""
    print("\n🔧 System Capabilities Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Check supported sources
    print("\n📋 Supported sources:")
    try:
        sources_info = loader.get_supported_sources()
        print(f"   Total supported sources: {len(sources_info)}")

        for source_type, info in list(sources_info.items())[:5]:  # Show first 5
            print(f"   {source_type}: {info.get('description', 'No description')}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Check source capabilities
    print("\n⚡ Source capabilities:")
    sample_sources = ["pdf", "web", "csv", "json", "database"]

    for source_type in sample_sources:
        try:
            capabilities = loader.get_capabilities(source_type)
            print(f"   {source_type}: {[cap.value for cap in capabilities]}")
        except Exception as e:
            print(f"   {source_type}: Error - {e}")

    # Validate credentials
    print("\n🔐 Credential validation:")
    credential_tests = [
        (
            "aws_s3",
            {"aws_access_key_id": "test_key", "aws_secret_access_key": "test_secret"},
        ),
        (
            "postgresql",
            {"host": "localhost", "username": "test_user", "password": "test_password"},
        ),
        ("google_drive", {"service_account_key": "/path/to/key.json"}),
    ]

    for source_type, credentials in credential_tests:
        try:
            is_valid = loader.validate_credentials(source_type, **credentials)
            status = "✅ Valid" if is_valid else "❌ Invalid"
            print(f"   {source_type}: {status}")
        except Exception as e:
            print(f"   {source_type}: Error - {e}")


# =============================================================================
# Error Handling and Debugging Examples
# =============================================================================


def example_error_handling():
    """Examples of error handling and debugging."""
    print("\n🐛 Error Handling Examples")
    print("=" * 50)

    loader = AutoLoader()

    # Handle invalid sources
    print("\n❌ Invalid source handling:")
    invalid_sources = [
        "/nonexistent/file.pdf",
        "https://invalid-url-that-does-not-exist.com",
        "unsupported://protocol/file",
    ]

    for source in invalid_sources:
        try:
            result = loader.load_detailed(source)
            if result.errors:
                print(f"   {source}: {len(result.errors)} errors")
                for error in result.errors:
                    print(f"     - {error}")
            else:
                print(f"   {source}: Loaded {len(result.documents)} documents")
        except Exception as e:
            print(f"   {source}: Exception - {e}")

    # Bulk loading with error tolerance
    print("\n🔧 Bulk loading with error tolerance:")
    mixed_sources = [
        "/valid/file.pdf",
        "/invalid/file.pdf",
        "https://example.com",
        "invalid://source",
    ]

    try:
        result = loader.load_bulk(mixed_sources)

        print(f"   Total attempted: {len(mixed_sources)}")
        print(f"   Successful: {result.summary['successful_loads']}")
        print(f"   Failed: {result.summary['failed_loads']}")

        if result.failed_sources:
            print("   Failed sources:")
            for source, error in result.failed_sources:
                print(f"     - {source}: {error}")

    except Exception as e:
        print(f"❌ Error: {e}")

    # Retry configuration
    print("\n🔄 Retry configuration:")
    retry_config = AutoLoaderConfig(
        retry_attempts=5,
        timeout=30,
    )
    AutoLoader(retry_config)
    print(f"   Configured for {retry_config.retry_attempts} retry attempts")
    print(f"   Timeout: {retry_config.timeout} seconds")


# =============================================================================
# Main Examples Runner
# =============================================================================


def run_all_examples():
    """Run all examples to demonstrate the document loader system."""
    print("🚀 Haive Document Loaders - Complete Examples")
    print("=" * 80)
    print("This demonstrates the ultimate auto-loading system with 230+ loaders")
    print("=" * 80)

    # Basic examples
    example_basic_auto_loading()
    example_convenience_functions()

    # Advanced configuration
    example_configuration_options()
    example_detailed_loading()

    # Bulk and concurrent loading
    example_bulk_loading()
    example_scrape_all()

    # Async examples
    print("\n🚀 Running async examples...")
    asyncio.run(example_async_loading())

    # Performance examples
    example_performance_optimization()

    # Real-world use cases
    example_enterprise_document_processing()
    example_research_paper_collection()
    example_legal_document_analysis()

    # Registry management
    example_registry_management()
    example_system_capabilities()

    # Error handling
    example_error_handling()

    print("\n" + "=" * 80)
    print("🎉 ALL EXAMPLES COMPLETED!")
    print("The Haive Document Loaders system supports 230+ loaders")
    print("and can handle ANY document source imaginable!")
    print("=" * 80)


if __name__ == "__main__":
    run_all_examples()
