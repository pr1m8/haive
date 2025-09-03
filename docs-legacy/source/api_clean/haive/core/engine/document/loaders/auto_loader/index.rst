
haive.core.engine.document.loaders.auto_loader
==============================================

.. py:module:: haive.core.engine.document.loaders.auto_loader

.. autoapi-nested-parse::

   Ultimate Auto-Loader for Document Sources.

   This module provides the ultimate auto-loader functionality that can automatically
   detect, instantiate, and load documents from any source type. It integrates with
   the enhanced registry and path analyzer to provide seamless document loading.

   The AutoLoader is the main entry point for users who want to load documents
   without manually configuring source types and loaders.

   .. admonition:: Examples

      Basic auto-loading::
      
          from haive.core.engine.document.loaders import AutoLoader
      
          # Auto-detect and load from any source
          loader = AutoLoader()
          documents = loader.load("https://example.com/docs")
      
      With preferences::
      
          # Prefer quality over speed
          loader = AutoLoader(preference="quality")
          documents = loader.load("s3://bucket/documents/")
      
      Bulk loading::
      
          # Load entire directory/bucket/site
          loader = AutoLoader()
          documents = loader.load_all("/path/to/documents")

   Author: Claude (Haive Document Loader System)
   Version: 1.0.0






Functions
---------

   load_document   load_documents_bulk   aload_document
.. autofunction:: load_document
.. autofunction:: load_documents_bulk
.. autofunction:: aload_document

Classes
-------

* :py:class:`LoadingResult` - Comprehensive result container for single-source document loading operations.* :py:class:`BulkLoadingResult` - Comprehensive result container for bulk document loading operations.* :py:class:`AutoLoaderConfig` - Configuration model for the AutoLoader system.* :py:class:`AutoLoader` - Ultimate automatic document loader with 230+ langchain_community integrations.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/auto_loader/LoadingResult   /api_clean/haive/core/engine/document/loaders/auto_loader/BulkLoadingResult   /api_clean/haive/core/engine/document/loaders/auto_loader/AutoLoaderConfig   /api_clean/haive/core/engine/document/loaders/auto_loader/AutoLoader

Package Contents
----------------

.. rubric:: haive.core.engine.document.loaders.auto_loader.__all__

.. autosummary::
   :nosignatures:

   AutoLoader   AutoLoaderConfig   BulkLoadingResult   LoadingResult   aload_document   default_loader   load_document   load_documents_bulk
.. automodule:: haive.core.engine.document.loaders.auto_loader
   :members:
   :show-inheritance:
