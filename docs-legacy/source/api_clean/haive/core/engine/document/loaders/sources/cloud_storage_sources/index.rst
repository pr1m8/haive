
haive.core.engine.document.loaders.sources.cloud_storage_sources
================================================================

.. py:module:: haive.core.engine.document.loaders.sources.cloud_storage_sources

.. autoapi-nested-parse::

   Cloud and storage platform source registrations.

   This module implements comprehensive cloud storage and data platform loaders including:
   - Cloud storage services (AWS, GCP, Azure, Dropbox, Box)
   - Data lakes and warehouses (Delta Lake, Apache Iceberg)
   - Object storage systems (MinIO, Ceph)
   - Backup and sync services






Functions
---------

   get_cloud_storage_statistics   validate_cloud_sources   detect_cloud_platform
.. autofunction:: get_cloud_storage_statistics
.. autofunction:: validate_cloud_sources
.. autofunction:: detect_cloud_platform

Classes
-------

* :py:class:`CloudPlatform` - Cloud storage platforms.* :py:class:`StorageAuthType` - Storage authentication types.* :py:class:`SyncDirection` - Synchronization directions.* :py:class:`S3FileSource` - AWS S3 single file source.* :py:class:`S3DirectorySource` - AWS S3 directory bulk source.* :py:class:`GCSFileSource` - Google Cloud Storage file source.* :py:class:`GCSDirectorySource` - Google Cloud Storage directory source.* :py:class:`AzureBlobFileSource` - Azure Blob Storage file source.* :py:class:`AzureBlobDirectorySource` - Azure Blob Storage container source.* :py:class:`DropboxSource` - Dropbox file sharing source.* :py:class:`GoogleDriveSource` - Google Drive source.* :py:class:`OneDriveSource` - Microsoft OneDrive source.* :py:class:`DeltaLakeSource` - Delta Lake data source.* :py:class:`IcebergSource` - Apache Iceberg data source.* :py:class:`SharePointSource` - Microsoft SharePoint source.* :py:class:`MinioSource` - MinIO object storage source.
.. toctree::
   :hidden:
   :maxdepth: 1

   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/CloudPlatform   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/StorageAuthType   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/SyncDirection   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/S3FileSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/S3DirectorySource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/GCSFileSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/GCSDirectorySource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/AzureBlobFileSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/AzureBlobDirectorySource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/DropboxSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/GoogleDriveSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/OneDriveSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/DeltaLakeSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/IcebergSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/SharePointSource   /api_clean/haive/core/engine/document/loaders/sources/cloud_storage_sources/MinioSource

Package Contents
----------------

