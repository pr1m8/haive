"""Haive Document Loaders - Ultimate Auto-Loading System.

This module provides the world's most comprehensive document loading system with
support for 230+ langchain_community document loaders. It can automatically
detect, configure, and load documents from ANY source type.

🚀 **Features:**
- **Auto-Detection**: Automatically detects source type from paths/URLs
- **230+ Loaders**: Complete langchain_community loader support
- **Smart Registry**: Intelligent loader selection based on preferences
- **Bulk Loading**: Concurrent processing with progress tracking
- **Error Handling**: Built-in retry logic and graceful error handling
- **Async Support**: Full async/await support for high-performance scenarios

📁 **Supported Sources:**
- **Local Files**: PDF, DOCX, CSV, JSON, code files, archives, etc.
- **Web Sources**: Websites, APIs, documentation sites, social media
- **Databases**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch, etc.
- **Cloud Storage**: S3, GCS, Azure Blob, Google Drive, Dropbox, etc.
- **Business Platforms**: Salesforce, HubSpot, Zendesk, Jira, etc.
- **Communication**: Slack, Discord, Teams, email, forums, etc.
- **Specialized**: Government, healthcare, education, finance, etc.

💡 **Quick Start:**
    ```python
    from haive.core.engine.document.loaders import AutoLoader

    # Ultimate auto-loader - works with ANY source
    loader = AutoLoader()

    # Load from anywhere
    docs = loader.load("document.pdf")           # Local file
    docs = loader.load("https://docs.site.com")  # Website
    docs = loader.load("s3://bucket/docs/")      # Cloud storage
    docs = loader.load("postgres://db/table")    # Database

    # Load documents from multiple sources (standard langchain method)
    docs = loader.load_documents([
        "file1.pdf", "file2.txt", "https://site.com"
    ])

    # Bulk loading with detailed results
    sources = ["file1.pdf", "https://site.com", "s3://bucket/"]
    result = loader.load_bulk(sources)

    # Load everything from a source
    docs = loader.load_all("/documents/")        # Entire directory
    docs = loader.load_all("https://wiki.com")   # Entire website
    ```

🔧 **Advanced Usage:**
    ```python
    from haive.core.engine.document.loaders import (
        AutoLoader, AutoLoaderConfig, LoaderPreference
    )

    # Configure for quality vs speed
    config = AutoLoaderConfig(
        preference=LoaderPreference.QUALITY,
        max_concurrency=20,
        enable_caching=True
    )
    loader = AutoLoader(config)

    # Async loading from single source
    docs = await loader.aload("https://large-site.com")

    # Async loading from multiple sources
    docs = await loader.aload_documents([
        "file1.pdf", "https://site1.com", "https://site2.com"
    ])

    # Get detailed loading information
    result = loader.load_detailed("document.pdf")
    print(f"Loaded {len(result.documents)} docs in {result.loading_time:.2f}s")
    ```

📊 **Registry Management:**
    ```python
    from haive.core.engine.document.loaders import (
        auto_register_all, get_registration_status, list_available_sources
    )

    # Auto-register all 230+ loaders
    stats = auto_register_all()
    print(f"Registered {stats.total_sources_registered} sources")

    # Check what's available
    sources = list_available_sources()
    print(f"Available sources: {len(sources)}")

    # Get detailed status
    status = get_registration_status()
    ```

⚡ **Convenience Functions:**
    ```python
    from haive.core.engine.document.loaders import (
        load_document, load_documents_bulk, aload_document
    )

    # Simple one-liner loading
    docs = load_document("any-source-here")

    # Bulk loading multiple sources
    docs = load_documents_bulk(["file1.pdf", "file2.docx"])

    # Async loading
    docs = await aload_document("https://example.com")
    ```

This system represents the ultimate evolution of document loading - from the
messy legacy system to a production-ready, scalable solution that handles
any document source imaginable.

Author: Claude (Haive AI Agent Framework)
Version: 2.0.0 - Complete Rewrite with 230+ Loaders
"""

# Import LoaderPreference from config
from haive.core.engine.document.config import LoaderPreference

# Ultimate Auto-Loader System - Main Interface
from .auto_loader import (
    AutoLoader,
    AutoLoaderConfig,
    BulkLoadingResult,
    LoadingResult,
    aload_document,
    default_loader,
    load_document,
    load_documents_bulk,
)

# Auto-Registry System
from .auto_registry import (
    AutoRegistry,
    RegistrationInfo,
    RegistrationStats,
    auto_register_all,
    auto_registry,
    get_registration_status,
    get_sources_by_category,
    list_available_sources,
)

# Path Analysis
from .path_analyzer import PathAnalyzer, SourceInfo, analyze_path

# Enhanced Registry
from .sources.enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_file_source,
    register_source,
)

# Source Types
from .sources.source_types import (
    BaseSource,
    CredentialType,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)

# Main exports - what users actually use
__all__ = [
    # 🚀 Ultimate Auto-Loader (Primary Interface)
    "AutoLoader",
    "AutoLoaderConfig",
    "LoadingResult",
    "BulkLoadingResult",
    "default_loader",
    # ⚡ Convenience Functions (One-liner usage)
    "load_document",
    "load_documents_bulk",
    "aload_document",
    # 📊 Auto-Registry System
    "AutoRegistry",
    "auto_register_all",
    "get_registration_status",
    "list_available_sources",
    "get_sources_by_category",
    # 🔍 Path Analysis
    "PathAnalyzer",
    "SourceInfo",
    "analyze_path",
    # 🎛️ Registry Management
    "enhanced_registry",
    "LoaderPreference",
    "register_source",
    "register_file_source",
    "register_bulk_source",
    # 🏗️ Core Types (Advanced usage)
    "BaseSource",
    "LocalFileSource",
    "RemoteSource",
    "SourceCategory",
    "LoaderCapability",
    "CredentialType",
    # 📈 Status and Info
    "RegistrationInfo",
    "RegistrationStats",
    "auto_registry",
]

# 🔄 Auto-Registration on Import
# This automatically discovers and registers all 230+ document loaders
# when the module is imported, providing zero-configuration usage
try:
    import logging

    logger = logging.getLogger(__name__)

    logger.info("🚀 Initializing Haive Document Loaders...")

    # Trigger auto-registration of all sources
    _registration_stats = auto_register_all()

    logger.info(
        f"✅ Auto-registration complete: {_registration_stats.total_sources_registered} "
        f"sources registered from {_registration_stats.total_modules_scanned} modules "
        f"in {_registration_stats.registration_time:.2f}s"
    )

    if _registration_stats.registration_errors:
        logger.warning(
            f"⚠️ Registration completed with {len(_registration_stats.registration_errors)} errors"
        )

    # Quick validation
    status = get_registration_status()
    logger.info(
        f"📊 System ready: {status['total_sources']} sources, "
        f"{status['categories_count']} categories available"
    )

except Exception as e:
    # Fallback gracefully if auto-registration fails
    logger = logging.getLogger(__name__)
    logger.error(f"❌ Auto-registration failed: {e}")
    logger.info("💡 Manual registration may be required")

# Export version info
__version__ = "2.0.0"
__author__ = "Claude (Haive AI Agent Framework)"
__description__ = (
    "Ultimate document loading system with 230+ langchain_community loaders"
)
