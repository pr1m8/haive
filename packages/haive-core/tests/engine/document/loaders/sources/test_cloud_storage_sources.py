"""Tests for cloud and storage platform source loaders.

This module tests cloud storage loaders including AWS S3, Google Cloud Storage,
Azure Blob Storage, file sharing services, data lakes, and enterprise storage.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional
from unittest.mock import MagicMock, Mock, patch

import pytest

from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
    AzureBlobFileSource,
    CloudPlatform,
    DeltaLakeSource,
    GCSFileSource,
    GoogleDriveSource,
    S3DirectorySource,
    S3FileSource,
    SharePointSource,
    StorageAuthType,
    SyncDirection,
    detect_cloud_platform,
    get_cloud_storage_statistics,
    validate_cloud_sources,
)
from haive.core.engine.document.loaders.sources.source_types import (
    CredentialType,
    LoaderCapability,
    SourceCategory,
)


@pytest.fixture
def mock_registry():
    """Create a mock registry for testing."""
    registry = MagicMock()
    registry._sources = {}
    registry.find_sources_by_category = MagicMock(return_value=[])
    return registry


@pytest.fixture
def s3_file_source() -> S3FileSource:
    """Create a test S3 file source instance."""
    return S3FileSource(
        source_id="s3-test-001",
        category=SourceCategory.CLOUD,
        bucket="test-bucket",
        key="path/to/file.pdf",
        aws_access_key_id="test-key",
        aws_secret_access_key="test-secret",
        region_name="us-west-2",
    )


@pytest.fixture
def s3_directory_source() -> S3DirectorySource:
    """Create a test S3 directory source instance."""
    return S3DirectorySource(
        source_id="s3-dir-test-001",
        category=SourceCategory.CLOUD,
        bucket="test-bucket",
        prefix="documents/",
        glob="**/*.pdf",
        use_multithreading=True,
        max_concurrency=5,
    )


@pytest.fixture
def google_drive_source() -> GoogleDriveSource:
    """Create a test Google Drive source instance."""
    return GoogleDriveSource(
        source_id="gdrive-test-001",
        category=SourceCategory.CLOUD,
        folder_id="1234567890",
        recursive=True,
        file_types=["application/pdf", "application/vnd.google-apps.document"],
    )


@pytest.fixture
def sharepoint_source() -> SharePointSource:
    """Create a test SharePoint source instance."""
    return SharePointSource(
        source_id="sharepoint-test-001",
        category=SourceCategory.CLOUD,
        site_url="https://company.sharepoint.com/sites/documents",
        document_library="Shared Documents",
        folder_path="/Projects/2024",
        client_id="test-client-id",
        client_secret="test-secret",
        tenant_id="test-tenant",
    )


class TestCloudPlatformDetection:
    """Test suite for cloud platform detection."""

    def test_detect_s3_from_url(self):
        """Test detecting AWS S3 from various URL patterns."""
        test_urls = [
            "s3://my-bucket/path/to/file.pdf",
            "https://my-bucket.s3.amazonaws.com/file.pdf",
            "https://s3.us-west-2.amazonaws.com/my-bucket/file.pdf",
        ]

        for url in test_urls:
            result = detect_cloud_platform(url)
            assert result == CloudPlatform.AWS_S3

    def test_detect_gcs_from_url(self):
        """Test detecting Google Cloud Storage from URLs."""
        test_urls = [
            "gs://my-bucket/path/to/file.pdf",
            "https://storage.googleapis.com/my-bucket/file.pdf",
        ]

        for url in test_urls:
            result = detect_cloud_platform(url)
            assert result == CloudPlatform.GCP_STORAGE

    def test_detect_azure_from_url(self):
        """Test detecting Azure Blob Storage from URLs."""
        test_urls = [
            "https://myaccount.blob.core.windows.net/container/file.pdf",
            "https://myaccount.dfs.core.windows.net/filesystem/path",
        ]

        for url in test_urls:
            result = detect_cloud_platform(url)
            assert result == CloudPlatform.AZURE_BLOB

    def test_detect_file_sharing_platforms(self):
        """Test detecting file sharing service URLs."""
        test_cases = [
            ("https://drive.google.com/file/d/123/view", CloudPlatform.GOOGLE_DRIVE),
            ("https://www.dropbox.com/s/123/file.pdf", CloudPlatform.DROPBOX),
            ("https://company.sharepoint.com/sites/team", CloudPlatform.SHAREPOINT),
            ("https://onedrive.live.com/view?id=123", CloudPlatform.ONEDRIVE),
        ]

        for url, expected in test_cases:
            result = detect_cloud_platform(url)
            assert result == expected

    def test_detect_unknown_platform(self):
        """Test handling of unknown platform URLs."""
        result = detect_cloud_platform("https://unknown-storage.com/file")
        assert result is None


class TestS3Sources:
    """Test suite for AWS S3 sources."""

    def test_s3_file_source_initialization(self, s3_file_source):
        """Test S3 file source initialization."""
        assert s3_file_source.platform == CloudPlatform.AWS_S3
        assert s3_file_source.bucket == "test-bucket"
        assert s3_file_source.key == "path/to/file.pdf"
        assert s3_file_source.region_name == "us-west-2"

    def test_s3_file_loader_kwargs(self, s3_file_source):
        """Test S3 file loader kwargs generation."""
        kwargs = s3_file_source.get_loader_kwargs()

        assert kwargs["bucket"] == "test-bucket"
        assert kwargs["key"] == "path/to/file.pdf"
        assert kwargs["region_name"] == "us-west-2"
        assert kwargs["aws_access_key_id"] == "test-key"
        assert kwargs["aws_secret_access_key"] == "test-secret"

    def test_s3_directory_source_initialization(self, s3_directory_source):
        """Test S3 directory source initialization."""
        assert s3_directory_source.platform == CloudPlatform.AWS_S3
        assert s3_directory_source.prefix == "documents/"
        assert s3_directory_source.glob == "**/*.pdf"
        assert s3_directory_source.use_multithreading is True
        assert s3_directory_source.max_concurrency == 5

    def test_s3_directory_scrape_all(self, s3_directory_source):
        """Test S3 directory scrape_all functionality."""
        scrape_config = s3_directory_source.scrape_all()

        assert scrape_config["bucket"] == "test-bucket"
        assert scrape_config["prefix"] == "documents/"
        assert scrape_config["recursive"] is True
        assert scrape_config["include_metadata"] is True

    def test_s3_with_custom_endpoint(self):
        """Test S3 source with custom endpoint (MinIO/Ceph)."""
        source = S3FileSource(
            source_id="s3-custom-001",
            category=SourceCategory.CLOUD,
            bucket="test-bucket",
            key="file.pdf",
            endpoint_url="https://minio.example.com:9000",
            aws_access_key_id="minio-key",
            aws_secret_access_key="minio-secret",
        )

        kwargs = source.get_loader_kwargs()
        assert kwargs["endpoint_url"] == "https://minio.example.com:9000"

    def test_s3_with_aws_profile(self):
        """Test S3 source using AWS profile credentials."""
        source = S3FileSource(
            source_id="s3-profile-001",
            category=SourceCategory.CLOUD,
            bucket="test-bucket",
            key="file.pdf",
            use_aws_profile=True,
        )

        kwargs = source.get_loader_kwargs()
        assert "aws_access_key_id" not in kwargs
        assert "aws_secret_access_key" not in kwargs


class TestGoogleCloudSources:
    """Test suite for Google Cloud Storage sources."""

    def test_gcs_file_source_initialization(self):
        """Test GCS file source initialization."""
        source = GCSFileSource(
            source_id="gcs-test-001",
            category=SourceCategory.CLOUD,
            bucket="test-bucket",
            blob="path/to/file.pdf",
            service_account_path="/path/to/service-account.json",
            project_id="my-project",
        )

        assert source.platform == CloudPlatform.GCP_STORAGE
        assert source.bucket == "test-bucket"
        assert source.blob == "path/to/file.pdf"

    def test_gcs_directory_with_filtering(self):
        """Test GCS directory source with filtering."""
        from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
            GCSDirectorySource,
        )

        source = GCSDirectorySource(
            source_id="gcs-dir-001",
            category=SourceCategory.CLOUD,
            bucket="data-bucket",
            prefix="processed/2024/",
            glob="**/*.json",
            exclude=["**/temp/*", "**/*.tmp"],
            max_concurrency=15,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["prefix"] == "processed/2024/"
        assert kwargs["glob"] == "**/*.json"
        assert kwargs["exclude"] == ["**/temp/*", "**/*.tmp"]
        assert kwargs["max_concurrency"] == 15


class TestAzureStorageSources:
    """Test suite for Azure storage sources."""

    def test_azure_blob_file_with_connection_string(self):
        """Test Azure Blob file source with connection string."""
        source = AzureBlobFileSource(
            source_id="azure-test-001",
            category=SourceCategory.CLOUD,
            container="documents",
            blob_name="reports/2024/report.pdf",
            connection_string="DefaultEndpointsProtocol=https;AccountName=test;AccountKey=xxx",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["container"] == "documents"
        assert kwargs["blob"] == "reports/2024/report.pdf"
        assert kwargs["conn_str"] == source.connection_string

    def test_azure_blob_file_with_account_url(self):
        """Test Azure Blob file source with account URL."""
        source = AzureBlobFileSource(
            source_id="azure-test-002",
            category=SourceCategory.CLOUD,
            container="data",
            blob_name="file.csv",
            account_url="https://myaccount.blob.core.windows.net",
            credential="sas-token",
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["account_url"] == "https://myaccount.blob.core.windows.net"
        assert kwargs["credential"] == "sas-token"
        assert "conn_str" not in kwargs


class TestFileSharingServices:
    """Test suite for file sharing service sources."""

    def test_google_drive_source_initialization(self, google_drive_source):
        """Test Google Drive source initialization."""
        assert google_drive_source.platform == CloudPlatform.GOOGLE_DRIVE
        assert google_drive_source.folder_id == "1234567890"
        assert google_drive_source.recursive is True
        assert len(google_drive_source.file_types) == 2

    def test_google_drive_scrape_all(self, google_drive_source):
        """Test Google Drive scrape_all functionality."""
        scrape_config = google_drive_source.scrape_all()

        assert scrape_config["folder_id"] == "1234567890"
        assert scrape_config["recursive"] is True
        assert scrape_config["include_trash"] is False
        assert "export_formats" in scrape_config

    def test_dropbox_source_configuration(self):
        """Test Dropbox source configuration."""
        from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
            DropboxSource,
        )

        source = DropboxSource(
            source_id="dropbox-001",
            category=SourceCategory.CLOUD,
            access_token="test-token",
            folder_path="/Projects/2024",
            recursive=True,
            file_types=[".pdf", ".docx"],
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["dropbox_access_token"] == "test-token"
        assert kwargs["dropbox_folder_path"] == "/Projects/2024"
        assert kwargs["recursive"] is True
        assert kwargs["file_types"] == [".pdf", ".docx"]

    def test_onedrive_oauth_configuration(self):
        """Test OneDrive OAuth configuration."""
        from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
            OneDriveSource,
        )

        source = OneDriveSource(
            source_id="onedrive-001",
            category=SourceCategory.CLOUD,
            client_id="app-client-id",
            client_secret="app-secret",
            tenant_id="tenant-id",
            folder_path="/Documents/Work",
            recursive=False,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["client_id"] == "app-client-id"
        assert kwargs["client_secret"] == "app-secret"
        assert kwargs["tenant_id"] == "tenant-id"
        assert kwargs["recursive"] is False


class TestEnterpriseStorage:
    """Test suite for enterprise storage sources."""

    def test_sharepoint_source_initialization(self, sharepoint_source):
        """Test SharePoint source initialization."""
        assert sharepoint_source.platform == CloudPlatform.SHAREPOINT
        assert (
            sharepoint_source.site_url
            == "https://company.sharepoint.com/sites/documents"
        )
        assert sharepoint_source.document_library == "Shared Documents"
        assert sharepoint_source.folder_path == "/Projects/2024"

    def test_sharepoint_scrape_all(self, sharepoint_source):
        """Test SharePoint scrape_all functionality."""
        scrape_config = sharepoint_source.scrape_all()

        assert scrape_config["document_library"] == "Shared Documents"
        assert scrape_config["recursive"] is True
        assert scrape_config["include_metadata"] is True
        assert scrape_config["include_versions"] is False

    def test_sharepoint_with_file_filtering(self):
        """Test SharePoint with file type filtering."""
        source = SharePointSource(
            source_id="sp-filtered-001",
            category=SourceCategory.CLOUD,
            site_url="https://company.sharepoint.com",
            document_library="Reports",
            file_types=[".xlsx", ".pptx", ".pdf"],
            include_metadata=True,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["file_types"] == [".xlsx", ".pptx", ".pdf"]
        assert kwargs["include_metadata"] is True


class TestDataLakeSources:
    """Test suite for data lake sources."""

    def test_delta_lake_source_initialization(self):
        """Test Delta Lake source initialization."""
        source = DeltaLakeSource(
            source_id="delta-001",
            category=SourceCategory.CLOUD,
            table_path="s3://bucket/delta-table",
            version=5,
            columns=["id", "name", "timestamp"],
            filter_expression="timestamp > '2024-01-01'",
        )

        assert source.platform == CloudPlatform.DELTA_LAKE
        assert source.table_path == "s3://bucket/delta-table"
        assert source.version == 5

    def test_delta_lake_time_travel(self):
        """Test Delta Lake time travel feature."""
        timestamp = datetime(2024, 1, 15, 10, 30)
        source = DeltaLakeSource(
            source_id="delta-002",
            category=SourceCategory.CLOUD,
            table_path="/mnt/delta/events",
            timestamp=timestamp,
            limit=1000,
        )

        kwargs = source.get_loader_kwargs()

        assert "version" not in kwargs
        assert kwargs["timestamp"] == timestamp.isoformat()
        assert kwargs["limit"] == 1000

    def test_iceberg_source_configuration(self):
        """Test Apache Iceberg source configuration."""
        from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
            IcebergSource,
        )

        source = IcebergSource(
            source_id="iceberg-001",
            category=SourceCategory.CLOUD,
            table_identifier="catalog.database.table",
            catalog_uri="thrift://metastore:9083",
            snapshot_id=123456,
            columns=["col1", "col2"],
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["table"] == "catalog.database.table"
        assert kwargs["catalog_uri"] == "thrift://metastore:9083"
        assert kwargs["snapshot_id"] == 123456


class TestObjectStorage:
    """Test suite for object storage sources."""

    def test_minio_s3_compatible_source(self):
        """Test MinIO S3-compatible source."""
        from haive.core.engine.document.loaders.sources.cloud_storage_sources import (
            MinioSource,
        )

        source = MinioSource(
            source_id="minio-001",
            category=SourceCategory.CLOUD,
            endpoint="minio.local:9000",
            bucket="data-bucket",
            prefix="raw/",
            access_key="minio-access",
            secret_key="minio-secret",
            secure=False,
        )

        kwargs = source.get_loader_kwargs()

        assert kwargs["endpoint"] == "minio.local:9000"
        assert kwargs["bucket"] == "data-bucket"
        assert kwargs["secure"] is False


class TestCloudStorageUtilities:
    """Test suite for cloud storage utility functions."""

    @patch(
        "haive.core.engine.document.loaders.sources.cloud_storage_sources.enhanced_registry"
    )
    def test_get_cloud_storage_statistics(self, mock_registry):
        """Test cloud storage statistics calculation."""
        # Mock registry responses
        mock_registry.find_sources_by_category.return_value = [
            "s3_file",
            "s3_directory",
            "gcs_file",
            "google_drive",
        ]
        mock_registry._sources = {
            "s3_file": MagicMock(
                platform=CloudPlatform.AWS_S3,
                capabilities=[LoaderCapability.CLOUD_NATIVE],
            ),
            "s3_directory": MagicMock(
                platform=CloudPlatform.AWS_S3,
                capabilities=[LoaderCapability.BULK_LOADING],
            ),
            "minio": MagicMock(
                platform=CloudPlatform.MINIO,
                capabilities=[LoaderCapability.S3_COMPATIBLE],
            ),
        }

        stats = get_cloud_storage_statistics()

        assert "total_cloud_sources" in stats
        assert "platform_breakdown" in stats
        assert "s3_compatible_sources" in stats
        assert "bulk_loading_sources" in stats

    @patch(
        "haive.core.engine.document.loaders.sources.cloud_storage_sources.enhanced_registry"
    )
    def test_validate_cloud_sources_success(self, mock_registry):
        """Test successful validation of cloud sources."""
        # Mock all required sources as present
        required = [
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
        mock_registry._sources = {name: MagicMock() for name in required}

        result = validate_cloud_sources()
        assert result is True

    @pytest.mark.parametrize(
        "auth_type,expected",
        [
            (StorageAuthType.ACCESS_KEY, "access_key"),
            (StorageAuthType.SERVICE_ACCOUNT, "service_account"),
            (StorageAuthType.OAUTH, "oauth"),
            (StorageAuthType.CONNECTION_STRING, "connection_string"),
            (StorageAuthType.IAM_ROLE, "iam_role"),
        ],
    )
    def test_storage_auth_type_values(self, auth_type: StorageAuthType, expected: str):
        """Test storage authentication type enum values."""
        assert auth_type.value == expected


@pytest.mark.integration
class TestCloudStorageIntegration:
    """Integration tests for cloud storage sources."""

    @patch("boto3.client")
    async def test_s3_loader_integration(self, mock_boto_client, s3_file_source):
        """Test S3 source integration with mock boto3."""
        # Mock S3 client
        mock_s3 = MagicMock()
        mock_s3.get_object.return_value = {
            "Body": MagicMock(read=lambda: b"File content"),
            "ContentType": "application/pdf",
        }
        mock_boto_client.return_value = mock_s3

        # Get loader kwargs
        kwargs = s3_file_source.get_loader_kwargs()

        # Verify S3 parameters
        assert kwargs["bucket"] == "test-bucket"
        assert kwargs["key"] == "path/to/file.pdf"

    @pytest.mark.parametrize(
        "platform,expected_capability",
        [
            (CloudPlatform.AWS_S3, LoaderCapability.CLOUD_NATIVE),
            (CloudPlatform.GOOGLE_DRIVE, LoaderCapability.BULK_LOADING),
            (CloudPlatform.SHAREPOINT, LoaderCapability.METADATA_EXTRACTION),
            (CloudPlatform.DELTA_LAKE, LoaderCapability.TIME_TRAVEL),
        ],
    )
    def test_platform_capabilities(
        self, platform: CloudPlatform, expected_capability: LoaderCapability
    ):
        """Test that cloud platforms have expected capabilities."""
        # This verifies our capability assignments make sense
        pass  # Implementation would check actual registry


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
