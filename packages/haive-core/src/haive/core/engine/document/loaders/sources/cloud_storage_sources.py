"""Cloud and storage platform source registrations.

This module implements comprehensive cloud storage and data platform loaders including:
- Cloud storage services (AWS, GCP, Azure, Dropbox, Box)
- Data lakes and warehouses (Delta Lake, Apache Iceberg)
- Object storage systems (MinIO, Ceph)
- Backup and sync services
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_bulk_source, register_source
from .source_types import CredentialType, LoaderCapability, RemoteSource, SourceCategory


class CloudPlatform(str, Enum):
    """Cloud storage platforms."""

    # Major Cloud Providers
    AWS_S3 = "aws_s3"
    GCP_STORAGE = "gcp_storage"
    AZURE_BLOB = "azure_blob"
    AZURE_FILES = "azure_files"

    # File Sharing Services
    DROPBOX = "dropbox"
    BOX = "box"
    ONEDRIVE = "onedrive"
    GOOGLE_DRIVE = "google_drive"

    # Data Lakes
    DELTA_LAKE = "delta_lake"
    APACHE_ICEBERG = "iceberg"
    HUDI = "hudi"

    # Object Storage
    MINIO = "minio"
    CEPH = "ceph"
    OPENSTACK_SWIFT = "swift"

    # Specialized Storage
    SHAREPOINT = "sharepoint"
    EGNYTE = "egnyte"
    NEXTCLOUD = "nextcloud"


class StorageAuthType(str, Enum):
    """Storage authentication types."""

    ACCESS_KEY = "access_key"
    SERVICE_ACCOUNT = "service_account"
    OAUTH = "oauth"
    API_TOKEN = "api_token"
    CONNECTION_STRING = "connection_string"
    IAM_ROLE = "iam_role"


class SyncDirection(str, Enum):
    """Synchronization directions."""

    DOWNLOAD = "download"
    UPLOAD = "upload"
    BIDIRECTIONAL = "bidirectional"


# =============================================================================
# AWS Storage Sources
# =============================================================================


@register_bulk_source(
    name="s3_file",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "s3_file": {
            "class": "S3FileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["boto3"],
        }
    },
    default_loader="s3_file",
    description="AWS S3 single file loader",
    requires_credentials=True,
    credential_type=CredentialType.ACCESS_KEY,
    capabilities=[LoaderCapability.CLOUD_NATIVE, LoaderCapability.STREAMING],
    priority=9,
)
class S3FileSource(RemoteSource):
    """AWS S3 single file source."""

    source_type: str = "s3_file"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.AWS_S3

    # S3 configuration
    bucket: str = Field(..., description="S3 bucket name")
    key: str = Field(..., description="S3 object key")

    # AWS credentials
    aws_access_key_id: Optional[str] = Field(None, description="AWS access key")
    aws_secret_access_key: Optional[str] = Field(None, description="AWS secret key")
    region_name: str = Field("us-east-1", description="AWS region")

    # Options
    use_aws_profile: bool = Field(False, description="Use AWS profile credentials")
    endpoint_url: Optional[str] = Field(None, description="Custom endpoint URL")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {"bucket": self.bucket, "key": self.key, "region_name": self.region_name}
        )

        if not self.use_aws_profile:
            kwargs["aws_access_key_id"] = self.aws_access_key_id
            kwargs["aws_secret_access_key"] = self.aws_secret_access_key

        if self.endpoint_url:
            kwargs["endpoint_url"] = self.endpoint_url

        return kwargs


@register_bulk_source(
    name="s3_directory",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "s3_dir": {
            "class": "S3DirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["boto3"],
        }
    },
    default_loader="s3_dir",
    description="AWS S3 directory bulk loader",
    requires_credentials=True,
    credential_type=CredentialType.ACCESS_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ],
    max_concurrent=10,
    supports_scrape_all=True,
    priority=10,
)
class S3DirectorySource(RemoteSource):
    """AWS S3 directory bulk source."""

    source_type: str = "s3_directory"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.AWS_S3

    # S3 configuration
    bucket: str = Field(..., description="S3 bucket name")
    prefix: str = Field("", description="S3 prefix (directory path)")

    # Filtering
    glob: str = Field("**/*", description="Glob pattern for files")
    exclude: Optional[List[str]] = Field(None, description="Patterns to exclude")
    max_files: Optional[int] = Field(None, description="Maximum files to load")

    # Processing
    use_multithreading: bool = Field(True, description="Enable parallel loading")
    max_concurrency: int = Field(10, ge=1, le=50, description="Max concurrent loads")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "bucket": self.bucket,
                "prefix": self.prefix,
                "glob": self.glob,
                "use_multithreading": self.use_multithreading,
                "max_concurrency": self.max_concurrency,
            }
        )

        if self.exclude:
            kwargs["exclude"] = self.exclude
        if self.max_files:
            kwargs["max_files"] = self.max_files

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire S3 bucket or prefix."""
        return {
            "bucket": self.bucket,
            "prefix": self.prefix or "/",
            "recursive": True,
            "include_metadata": True,
        }


# =============================================================================
# Google Cloud Storage Sources
# =============================================================================


@register_bulk_source(
    name="gcs_file",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "gcs_file": {
            "class": "GCSFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-cloud-storage"],
        }
    },
    default_loader="gcs_file",
    description="Google Cloud Storage file loader",
    requires_credentials=True,
    credential_type=CredentialType.SERVICE_ACCOUNT,
    capabilities=[LoaderCapability.CLOUD_NATIVE, LoaderCapability.STREAMING],
    priority=9,
)
class GCSFileSource(RemoteSource):
    """Google Cloud Storage file source."""

    source_type: str = "gcs_file"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.GCP_STORAGE

    # GCS configuration
    bucket: str = Field(..., description="GCS bucket name")
    blob: str = Field(..., description="Blob name (file path)")

    # Credentials
    service_account_path: Optional[str] = Field(
        None, description="Service account JSON path"
    )
    project_id: Optional[str] = Field(None, description="GCP project ID")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"bucket": self.bucket, "blob": self.blob})

        if self.service_account_path:
            kwargs["service_account_path"] = self.service_account_path
        if self.project_id:
            kwargs["project"] = self.project_id

        return kwargs


@register_bulk_source(
    name="gcs_directory",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "gcs_dir": {
            "class": "GCSDirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-cloud-storage"],
        }
    },
    default_loader="gcs_dir",
    description="Google Cloud Storage directory bulk loader",
    requires_credentials=True,
    credential_type=CredentialType.SERVICE_ACCOUNT,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ],
    max_concurrent=10,
    supports_scrape_all=True,
    priority=10,
)
class GCSDirectorySource(RemoteSource):
    """Google Cloud Storage directory source."""

    source_type: str = "gcs_directory"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.GCP_STORAGE

    # GCS configuration
    bucket: str = Field(..., description="GCS bucket name")
    prefix: str = Field("", description="Prefix (directory path)")
    delimiter: str = Field("/", description="Path delimiter")

    # Filtering
    glob: str = Field("**/*", description="Glob pattern")
    exclude: Optional[List[str]] = Field(None, description="Exclude patterns")

    # Processing
    max_concurrency: int = Field(10, ge=1, le=50, description="Max concurrent loads")
    continue_on_failure: bool = Field(True, description="Continue if file fails")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "bucket": self.bucket,
                "prefix": self.prefix,
                "delimiter": self.delimiter,
                "glob": self.glob,
                "max_concurrency": self.max_concurrency,
                "continue_on_failure": self.continue_on_failure,
            }
        )

        if self.exclude:
            kwargs["exclude"] = self.exclude

        return kwargs


# =============================================================================
# Azure Storage Sources
# =============================================================================


@register_bulk_source(
    name="azure_blob_file",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "azure_blob": {
            "class": "AzureBlobStorageFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["azure-storage-blob"],
        }
    },
    default_loader="azure_blob",
    description="Azure Blob Storage file loader",
    requires_credentials=True,
    credential_type=CredentialType.CONNECTION_STRING,
    capabilities=[LoaderCapability.CLOUD_NATIVE, LoaderCapability.STREAMING],
    priority=9,
)
class AzureBlobFileSource(RemoteSource):
    """Azure Blob Storage file source."""

    source_type: str = "azure_blob_file"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.AZURE_BLOB

    # Azure configuration
    container: str = Field(..., description="Container name")
    blob_name: str = Field(..., description="Blob name")

    # Authentication
    connection_string: Optional[str] = Field(
        None, description="Azure connection string"
    )
    account_url: Optional[str] = Field(None, description="Storage account URL")
    credential: Optional[str] = Field(None, description="Azure credential")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"container": self.container, "blob": self.blob_name})

        if self.connection_string:
            kwargs["conn_str"] = self.connection_string
        elif self.account_url:
            kwargs["account_url"] = self.account_url
            if self.credential:
                kwargs["credential"] = self.credential

        return kwargs


@register_bulk_source(
    name="azure_blob_directory",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "azure_dir": {
            "class": "AzureBlobStorageContainerLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["azure-storage-blob"],
        }
    },
    default_loader="azure_dir",
    description="Azure Blob Storage container bulk loader",
    requires_credentials=True,
    credential_type=CredentialType.CONNECTION_STRING,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ],
    max_concurrent=10,
    supports_scrape_all=True,
    priority=10,
)
class AzureBlobDirectorySource(RemoteSource):
    """Azure Blob Storage container source."""

    source_type: str = "azure_blob_directory"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.AZURE_BLOB

    # Azure configuration
    container: str = Field(..., description="Container name")
    prefix: str = Field("", description="Blob prefix")

    # Filtering
    name_starts_with: Optional[str] = Field(None, description="Filter by name prefix")
    include: Optional[List[str]] = Field(None, description="Include patterns")
    exclude: Optional[List[str]] = Field(None, description="Exclude patterns")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"container": self.container, "prefix": self.prefix})

        if self.name_starts_with:
            kwargs["name_starts_with"] = self.name_starts_with
        if self.include:
            kwargs["include"] = self.include
        if self.exclude:
            kwargs["exclude"] = self.exclude

        return kwargs


# =============================================================================
# File Sharing Services
# =============================================================================


@register_source(
    name="dropbox",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "dropbox": {
            "class": "DropboxLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["dropbox"],
        }
    },
    default_loader="dropbox",
    description="Dropbox file and folder loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=8,
)
class DropboxSource(RemoteSource):
    """Dropbox file sharing source."""

    source_type: str = "dropbox"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.DROPBOX

    # Dropbox configuration
    access_token: Optional[str] = Field(None, description="Dropbox access token")
    folder_path: str = Field("/", description="Folder path to load from")

    # Options
    recursive: bool = Field(True, description="Load recursively")
    include_shared: bool = Field(True, description="Include shared files")
    file_types: Optional[List[str]] = Field(None, description="Filter by file types")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "dropbox_access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "dropbox_folder_path": self.folder_path,
                "recursive": self.recursive,
            }
        )

        if self.file_types:
            kwargs["file_types"] = self.file_types

        return kwargs


@register_bulk_source(
    name="google_drive",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "gdrive": {
            "class": "GoogleDriveLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-api-python-client", "google-auth"],
        }
    },
    default_loader="gdrive",
    description="Google Drive file and folder loader",
    requires_credentials=True,
    credential_type=CredentialType.SERVICE_ACCOUNT,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    supports_scrape_all=True,
    priority=9,
)
class GoogleDriveSource(RemoteSource):
    """Google Drive source."""

    source_type: str = "google_drive"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.GOOGLE_DRIVE

    # Drive configuration
    folder_id: Optional[str] = Field(None, description="Specific folder ID")
    file_ids: Optional[List[str]] = Field(None, description="Specific file IDs")

    # Authentication
    service_account_key: Optional[str] = Field(
        None, description="Service account key path"
    )
    credentials_path: Optional[str] = Field(None, description="OAuth credentials path")

    # Options
    recursive: bool = Field(True, description="Load folders recursively")
    file_types: Optional[List[str]] = Field(None, description="Filter by MIME types")
    max_files: Optional[int] = Field(None, description="Maximum files to load")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.folder_id:
            kwargs["folder_id"] = self.folder_id
        elif self.file_ids:
            kwargs["file_ids"] = self.file_ids

        if self.service_account_key:
            kwargs["service_account_key"] = self.service_account_key
        elif self.credentials_path:
            kwargs["credentials_path"] = self.credentials_path

        kwargs.update({"recursive": self.recursive})

        if self.file_types:
            kwargs["file_types"] = self.file_types
        if self.max_files:
            kwargs["max_files"] = self.max_files

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire Google Drive or folder."""
        return {
            "folder_id": self.folder_id or "root",
            "recursive": True,
            "include_trash": False,
            "export_formats": {
                "application/vnd.google-apps.document": "text/plain",
                "application/vnd.google-apps.spreadsheet": "text/csv",
            },
        }


@register_source(
    name="onedrive",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "onedrive": {
            "class": "OneDriveLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["msal", "requests"],
        }
    },
    default_loader="onedrive",
    description="Microsoft OneDrive file and folder loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=8,
)
class OneDriveSource(RemoteSource):
    """Microsoft OneDrive source."""

    source_type: str = "onedrive"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.ONEDRIVE

    # OneDrive configuration
    client_id: Optional[str] = Field(None, description="Azure app client ID")
    client_secret: Optional[str] = Field(None, description="Azure app client secret")
    tenant_id: Optional[str] = Field(None, description="Azure tenant ID")

    # Path options
    folder_path: str = Field("/", description="Folder path")
    recursive: bool = Field(True, description="Load recursively")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "tenant_id": self.tenant_id,
                "folder_path": self.folder_path,
                "recursive": self.recursive,
            }
        )

        return kwargs


# =============================================================================
# Data Lake Sources
# =============================================================================


@register_source(
    name="delta_lake",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "delta": {
            "class": "DeltaLakeLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["deltalake"],
        }
    },
    default_loader="delta",
    description="Delta Lake table loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.FILTERING,
        LoaderCapability.TIME_TRAVEL,
    ],
    priority=9,
)
class DeltaLakeSource(RemoteSource):
    """Delta Lake data source."""

    source_type: str = "delta_lake"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.DELTA_LAKE

    # Delta Lake configuration
    table_path: str = Field(..., description="Path to Delta table")
    version: Optional[int] = Field(None, description="Table version to read")
    timestamp: Optional[datetime] = Field(None, description="Read table at timestamp")

    # Query options
    columns: Optional[List[str]] = Field(None, description="Columns to select")
    filter_expression: Optional[str] = Field(None, description="Filter expression")
    limit: Optional[int] = Field(None, description="Row limit")

    # Storage options
    storage_options: Optional[Dict[str, str]] = Field(
        None, description="Storage options"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"table_path": self.table_path})

        if self.version is not None:
            kwargs["version"] = self.version
        elif self.timestamp:
            kwargs["timestamp"] = self.timestamp.isoformat()

        if self.columns:
            kwargs["columns"] = self.columns
        if self.filter_expression:
            kwargs["filter"] = self.filter_expression
        if self.limit:
            kwargs["limit"] = self.limit
        if self.storage_options:
            kwargs["storage_options"] = self.storage_options

        return kwargs


@register_source(
    name="apache_iceberg",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "iceberg": {
            "class": "IcebergLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyiceberg"],
        }
    },
    default_loader="iceberg",
    description="Apache Iceberg table loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.FILTERING,
        LoaderCapability.TIME_TRAVEL,
        LoaderCapability.SCHEMA_EVOLUTION,
    ],
    priority=9,
)
class IcebergSource(RemoteSource):
    """Apache Iceberg data source."""

    source_type: str = "apache_iceberg"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.APACHE_ICEBERG

    # Iceberg configuration
    table_identifier: str = Field(..., description="Table identifier")
    catalog_uri: str = Field(..., description="Catalog URI")

    # Query options
    snapshot_id: Optional[int] = Field(None, description="Snapshot ID to read")
    as_of_timestamp: Optional[datetime] = Field(
        None, description="Read as of timestamp"
    )

    # Scan options
    columns: Optional[List[str]] = Field(None, description="Columns to select")
    filter_expression: Optional[str] = Field(None, description="Filter expression")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"table": self.table_identifier, "catalog_uri": self.catalog_uri})

        if self.snapshot_id:
            kwargs["snapshot_id"] = self.snapshot_id
        elif self.as_of_timestamp:
            kwargs["as_of_timestamp"] = self.as_of_timestamp

        if self.columns:
            kwargs["columns"] = self.columns
        if self.filter_expression:
            kwargs["filter"] = self.filter_expression

        return kwargs


# =============================================================================
# Enterprise Storage Sources
# =============================================================================


@register_bulk_source(
    name="sharepoint",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "sharepoint": {
            "class": "SharePointLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["Office365-REST-Python-Client"],
        }
    },
    default_loader="sharepoint",
    description="Microsoft SharePoint document library loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    supports_scrape_all=True,
    priority=9,
)
class SharePointSource(RemoteSource):
    """Microsoft SharePoint source."""

    source_type: str = "sharepoint"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.SHAREPOINT

    # SharePoint configuration
    site_url: str = Field(..., description="SharePoint site URL")
    document_library: str = Field("Documents", description="Document library name")
    folder_path: str = Field("/", description="Folder path within library")

    # Authentication
    client_id: Optional[str] = Field(None, description="Azure app client ID")
    client_secret: Optional[str] = Field(None, description="Azure app client secret")
    tenant_id: Optional[str] = Field(None, description="Azure tenant ID")

    # Options
    recursive: bool = Field(True, description="Load folders recursively")
    file_types: Optional[List[str]] = Field(None, description="Filter by extensions")
    include_metadata: bool = Field(True, description="Include file metadata")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "site_url": self.site_url,
                "document_library": self.document_library,
                "folder_path": self.folder_path,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "tenant_id": self.tenant_id,
                "recursive": self.recursive,
                "include_metadata": self.include_metadata,
            }
        )

        if self.file_types:
            kwargs["file_types"] = self.file_types

        return kwargs

    def scrape_all(self) -> Dict[str, Any]:
        """Scrape entire SharePoint library."""
        return {
            "document_library": self.document_library,
            "recursive": True,
            "include_versions": False,
            "include_metadata": True,
        }


# =============================================================================
# Object Storage Sources
# =============================================================================


@register_bulk_source(
    name="minio",
    category=SourceCategory.CLOUD_STORAGE,
    loaders={
        "minio": {
            "class": "MinioLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["minio"],
        }
    },
    default_loader="minio",
    description="MinIO object storage loader",
    requires_credentials=True,
    credential_type=CredentialType.ACCESS_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
        LoaderCapability.S3_COMPATIBLE,
    ],
    max_concurrent=20,
    supports_scrape_all=True,
    priority=8,
)
class MinioSource(RemoteSource):
    """MinIO object storage source."""

    source_type: str = "minio"
    category: SourceCategory = SourceCategory.CLOUD_STORAGE
    platform: CloudPlatform = CloudPlatform.MINIO

    # MinIO configuration
    endpoint: str = Field(..., description="MinIO endpoint URL")
    bucket: str = Field(..., description="Bucket name")
    prefix: str = Field("", description="Object prefix")

    # Authentication
    access_key: Optional[str] = Field(None, description="Access key")
    secret_key: Optional[str] = Field(None, description="Secret key")
    secure: bool = Field(True, description="Use HTTPS")

    # Options
    recursive: bool = Field(True, description="List recursively")
    include_version: bool = Field(False, description="Include object versions")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "endpoint": self.endpoint,
                "bucket": self.bucket,
                "prefix": self.prefix,
                "access_key": (
                    self.access_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "secret_key": self.secret_key,
                "secure": self.secure,
                "recursive": self.recursive,
                "include_version": self.include_version,
            }
        )

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_cloud_storage_statistics() -> Dict[str, Any]:
    """Get statistics about cloud storage sources."""
    registry = enhanced_registry

    # Count by platform
    platform_counts = {}
    for platform in CloudPlatform:
        count = len(
            [
                name
                for name, reg in registry._sources.items()
                if hasattr(reg, "platform")
                and getattr(reg, "platform", None) == platform
            ]
        )
        if count > 0:
            platform_counts[platform.value] = count

    # Category statistics
    cloud_sources = registry.find_sources_by_category(SourceCategory.CLOUD_STORAGE)

    # S3-compatible sources
    s3_compatible = len(
        [
            name
            for name, reg in registry._sources.items()
            if hasattr(reg, "capabilities")
            and LoaderCapability.S3_COMPATIBLE in getattr(reg, "capabilities", [])
        ]
    )

    # Bulk capable sources
    bulk_cloud = len(
        [
            name
            for name in cloud_sources
            if registry._sources[name].capabilities
            and LoaderCapability.BULK_LOADING in registry._sources[name].capabilities
        ]
    )

    return {
        "total_cloud_sources": len(cloud_sources),
        "platform_breakdown": platform_counts,
        "s3_compatible_sources": s3_compatible,
        "bulk_loading_sources": bulk_cloud,
        "auth_types": len(StorageAuthType),
    }


def validate_cloud_sources() -> bool:
    """Validate cloud source registrations."""
    registry = enhanced_registry

    required_sources = [
        "s3_file",
        "s3_directory",
        "gcs_file",
        "gcs_directory",
        "azure_blob_file",
        "azure_blob_directory",
        "google_drive",
        "sharepoint",
        "delta_lake",
    ]

    missing = []
    for source_name in required_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing cloud sources: {missing}")
        return False

    print("✅ All essential cloud storage sources registered!")
    return True


def detect_cloud_platform(url_or_path: str) -> Optional[CloudPlatform]:
    """Auto-detect cloud platform from URL or path."""
    lower = url_or_path.lower()

    patterns = {
        CloudPlatform.AWS_S3: ["s3://", ".s3.amazonaws.com", "s3."],
        CloudPlatform.GCP_STORAGE: ["gs://", "storage.googleapis.com"],
        CloudPlatform.AZURE_BLOB: ["blob.core.windows.net", "dfs.core.windows.net"],
        CloudPlatform.GOOGLE_DRIVE: ["drive.google.com", "docs.google.com"],
        CloudPlatform.DROPBOX: ["dropbox.com", "dropboxusercontent.com"],
        CloudPlatform.SHAREPOINT: ["sharepoint.com", ".sharepoint.com"],
        CloudPlatform.ONEDRIVE: ["onedrive.live.com", "1drv.ms"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_cloud_sources()
    stats = get_cloud_storage_statistics()
    print(f"Cloud Storage Statistics: {stats}")
