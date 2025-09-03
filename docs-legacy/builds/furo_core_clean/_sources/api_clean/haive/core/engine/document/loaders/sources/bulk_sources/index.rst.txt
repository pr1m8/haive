
haive.core.engine.document.loaders.sources.bulk_sources
=======================================================

.. py:module:: haive.core.engine.document.loaders.sources.bulk_sources

.. autoapi-nested-parse::

   Bulk loading and directory sources with "scrape all" capabilities.

   This module implements comprehensive bulk loading sources that can process
   entire directories, repositories, and data sources with parallel processing
   and filtering capabilities.






Functions
---------

   get_bulk_sources_statistics   get_scrape_all_sources   validate_bulk_sources
.. autofunction:: get_bulk_sources_statistics
.. autofunction:: get_scrape_all_sources
.. autofunction:: validate_bulk_sources

Classes
-------

* :py:class:`BulkProcessingMode` - Modes for bulk processing operations.* :py:class:`FilterStrategy` - Strategies for filtering files during bulk processing.* :py:class:`RecursiveDirectorySource` - Advanced recursive directory source with concurrent processing.* :py:class:`FilteredDirectorySource` - Directory source with advanced filtering capabilities.* :py:class:`S3BucketSource` - AWS S3 bucket source for bulk processing.* :py:class:`GCSBucketSource` - Google Cloud Storage bucket source.* :py:class:`AzureContainerSource` - Azure Blob Storage container source.* :py:class:`MergedDataSource` - Multi-source data merger for combining different data sources.* :py:class:`FileSystemBlobSource` - File system blob source for binary and mixed content.* :py:class:`CloudBlobSource` - Multi-cloud blob source supporting various cloud storage schemes.* :py:class:`StreamingDirectorySource` - Streaming directory source for real-time processing.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/BulkProcessingMode   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/FilterStrategy   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/RecursiveDirectorySource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/FilteredDirectorySource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/S3BucketSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/GCSBucketSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/AzureContainerSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/MergedDataSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/FileSystemBlobSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/CloudBlobSource   /api_clean/haive/core/engine/document/loaders/sources/bulk_sources/StreamingDirectorySource

Package Contents
----------------

