
:py:mod:`haive.core.engine.document.loaders`
========================

.. py:module:: haive.core.engine.document.loaders

.. autoapi-nested-parse::

   Haive Document Loaders - Ultimate Auto-Loading System.

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




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.loaders.adapters   haive.core.engine.document.loaders.base   haive.core.engine.document.loaders.sources   haive.core.engine.document.loaders.specific   haive.core.engine.document.loaders.utils
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/document/loaders/adapters/index   /api_clean/haive/core/engine/document/loaders/base/index   /api_clean/haive/core/engine/document/loaders/sources/index   /api_clean/haive/core/engine/document/loaders/specific/index   /api_clean/haive/core/engine/document/loaders/utils/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.loaders.auto_factory   haive.core.engine.document.loaders.auto_loader   haive.core.engine.document.loaders.auto_registry   haive.core.engine.document.loaders.base_new   haive.core.engine.document.loaders.cache_manager   haive.core.engine.document.loaders.engine   haive.core.engine.document.loaders.examples   haive.core.engine.document.loaders.path_analyzer   haive.core.engine.document.loaders.registry   haive.core.engine.document.loaders.source_base   haive.core.engine.document.loaders.strategy
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/document/loaders/auto_factory/index   /api_clean/haive/core/engine/document/loaders/auto_loader/index   /api_clean/haive/core/engine/document/loaders/auto_registry/index   /api_clean/haive/core/engine/document/loaders/base_new/index   /api_clean/haive/core/engine/document/loaders/cache_manager/index   /api_clean/haive/core/engine/document/loaders/engine/index   /api_clean/haive/core/engine/document/loaders/examples/index   /api_clean/haive/core/engine/document/loaders/path_analyzer/index   /api_clean/haive/core/engine/document/loaders/registry/index   /api_clean/haive/core/engine/document/loaders/source_base/index   /api_clean/haive/core/engine/document/loaders/strategy/index





Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.document.loaders.AutoLoader   haive.core.engine.document.loaders.AutoLoaderConfig   haive.core.engine.document.loaders.AutoRegistry   haive.core.engine.document.loaders.BaseSource   haive.core.engine.document.loaders.BulkLoadingResult   haive.core.engine.document.loaders.CredentialType   haive.core.engine.document.loaders.LoaderCapability   haive.core.engine.document.loaders.LoaderPreference   haive.core.engine.document.loaders.LoadingResult   haive.core.engine.document.loaders.LocalFileSource   haive.core.engine.document.loaders.PathAnalyzer   haive.core.engine.document.loaders.RegistrationInfo   haive.core.engine.document.loaders.RegistrationStats   haive.core.engine.document.loaders.RemoteSource   haive.core.engine.document.loaders.SourceCategory   haive.core.engine.document.loaders.SourceInfo   haive.core.engine.document.loaders.aload_document   haive.core.engine.document.loaders.analyze_path   haive.core.engine.document.loaders.auto_register_all   haive.core.engine.document.loaders.auto_registry   haive.core.engine.document.loaders.default_loader   haive.core.engine.document.loaders.enhanced_registry   haive.core.engine.document.loaders.get_registration_status   haive.core.engine.document.loaders.get_sources_by_category   haive.core.engine.document.loaders.list_available_sources   haive.core.engine.document.loaders.load_document   haive.core.engine.document.loaders.load_documents_bulk   haive.core.engine.document.loaders.register_bulk_source   haive.core.engine.document.loaders.register_file_source   haive.core.engine.document.loaders.register_source

.. automodule:: haive.core.engine.document.loaders
   :members:
   :undoc-members:
   :show-inheritance: