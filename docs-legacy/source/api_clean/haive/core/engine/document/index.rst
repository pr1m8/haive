
:py:mod:`haive.core.engine.document`
========================

.. py:module:: haive.core.engine.document

.. autoapi-nested-parse::

   Enhanced Document Engine Package.

   This package provides comprehensive document processing capabilities including:
   - Document loading from various sources (files, URLs, databases, cloud storage)
   - Advanced chunking and processing strategies
   - Path analysis and source type detection
   - Parallel processing and error handling
   - Integration with the Haive engine framework

   Key Components:
   - DocumentEngine: Main engine for document processing
   - DocumentEngineConfig: Configuration model for the engine
   - Path analysis system for source type detection
   - Document loaders for various source types
   - Processing strategies for chunking and transformation




Subpackages
-----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.base   haive.core.engine.document.loaders   haive.core.engine.document.sources   haive.core.engine.document.splitters   haive.core.engine.document.transformers   haive.core.engine.document.types
.. toctree::
   :maxdepth: 2
   :hidden:

   /api_clean/haive/core/engine/document/base/index   /api_clean/haive/core/engine/document/loaders/index   /api_clean/haive/core/engine/document/sources/index   /api_clean/haive/core/engine/document/splitters/index   /api_clean/haive/core/engine/document/transformers/index   /api_clean/haive/core/engine/document/types/index

Submodules
----------

.. autosummary::
   :nosignatures:
   :template: autosummary/module.rst
   :toctree: .

   haive.core.engine.document.config   haive.core.engine.document.engine   haive.core.engine.document.factory   haive.core.engine.document.path_analysis   haive.core.engine.document.processors   haive.core.engine.document.universal_loader
.. toctree::
   :maxdepth: 1
   :hidden:

   /api_clean/haive/core/engine/document/config/index   /api_clean/haive/core/engine/document/engine/index   /api_clean/haive/core/engine/document/factory/index   /api_clean/haive/core/engine/document/path_analysis/index   /api_clean/haive/core/engine/document/processors/index   /api_clean/haive/core/engine/document/universal_loader/index



Package Functions
-----------------

.. autosummary::
   :nosignatures:
   :template: autosummary/function.rst

   haive.core.engine.document.create_document_engine   haive.core.engine.document.load_documents
.. autofunction:: haive.core.engine.document.create_document_engine
.. autofunction:: haive.core.engine.document.load_documents



Package Contents
----------------

.. rubric:: haive.core.engine.document.__all__

.. autosummary::
   :nosignatures:

   haive.core.engine.document.AutoLoaderFactory   haive.core.engine.document.BaseDocumentLoader   haive.core.engine.document.ChunkingProcessor   haive.core.engine.document.ChunkingStrategy   haive.core.engine.document.CloudProvider   haive.core.engine.document.ContentNormalizer   haive.core.engine.document.CredentialManager   haive.core.engine.document.DatabaseType   haive.core.engine.document.DirectoryDocumentAgent   haive.core.engine.document.DocumentAgent   haive.core.engine.document.DocumentChunk   haive.core.engine.document.DocumentEngine   haive.core.engine.document.DocumentEngineConfig   haive.core.engine.document.DocumentFormat   haive.core.engine.document.DocumentInput   haive.core.engine.document.DocumentLoaderRegistry   haive.core.engine.document.DocumentOutput   haive.core.engine.document.DocumentProcessor   haive.core.engine.document.DocumentSourceType   haive.core.engine.document.EnhancedSource   haive.core.engine.document.FileCategory   haive.core.engine.document.FileDocumentAgent   haive.core.engine.document.FormatDetector   haive.core.engine.document.LoaderCapability   haive.core.engine.document.LoaderPreference   haive.core.engine.document.LoaderPriority   haive.core.engine.document.LoaderStrategy   haive.core.engine.document.MetadataExtractor   haive.core.engine.document.MongoDBSource   haive.core.engine.document.PathAnalysisResult   haive.core.engine.document.PathType   haive.core.engine.document.PostgreSQLSource   haive.core.engine.document.ProcessedDocument   haive.core.engine.document.ProcessingStrategy   haive.core.engine.document.SimpleDocumentLoader   haive.core.engine.document.TextDocumentLoader   haive.core.engine.document.WebDocumentAgent   haive.core.engine.document.analyze_path_comprehensive   haive.core.engine.document.analyze_source   haive.core.engine.document.create_directory_document_engine   haive.core.engine.document.create_document_engine   haive.core.engine.document.create_document_loader   haive.core.engine.document.create_file_document_engine   haive.core.engine.document.create_loader   haive.core.engine.document.create_web_document_engine   haive.core.engine.document.get_default_registry   haive.core.engine.document.get_loader   haive.core.engine.document.load_documents   haive.core.engine.document.register_loader   haive.core.engine.document.source_registry   haive.core.engine.document.strategy_registry

.. automodule:: haive.core.engine.document
   :members:
   :undoc-members:
   :show-inheritance: