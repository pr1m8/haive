"""Cloud Storage Loaders for Document Engine.

This module implements cloud storage loaders for AWS S3, Google Cloud Storage,
Azure Blob Storage, and other cloud providers.
"""

import logging
from typing import List, Optional
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CloudStorageSource,
    CredentialType,
)

logger = logging.getLogger(__name__)


class S3Source(CloudStorageSource):
    """AWS S3 storage source implementation."""

    def __init__(
        self,
        bucket_name: str,
        object_key: Optional[str] = None,
        prefix: Optional[str] = None,
        region: Optional[str] = None,
        **kwargs,
    ):
        s3_path = f"s3://{bucket_name}/{object_key or prefix or ''}"
        super().__init__(source_path=s3_path, **kwargs)
        self.bucket_name = bucket_name
        self.object_key = object_key
        self.prefix = prefix
        self.region = region

    def can_handle(self, path: str) -> bool:
        """Check if this is an S3 path."""
        try:
            parsed = urlparse(path)
            return parsed.scheme == "s3"
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for S3 paths."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """S3 typically requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """S3 needs AWS credentials."""
        return [CredentialType.API_KEY, CredentialType.SERVICE_ACCOUNT]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an S3 loader."""
        try:
            from langchain_community.document_loaders import (
                S3DirectoryLoader,
                S3FileLoader,
            )

            # Get AWS credentials if needed
            aws_access_key = None
            aws_secret_key = None

            if self.credential_manager:
                cred = self.credential_manager.get_credential("aws")
                if cred and cred.credential_type == CredentialType.API_KEY:
                    # Assume format "access_key:secret_key"
                    if ":" in cred.value:
                        aws_access_key, aws_secret_key = cred.value.split(":", 1)

            # Determine if loading a single file or directory
            if self.object_key and not self.object_key.endswith("/"):
                # Single file
                return S3FileLoader(
                    bucket=self.bucket_name,
                    key=self.object_key,
                    region_name=self.region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                )
            else:
                # Directory or prefix
                prefix = self.prefix or self.object_key or ""
                return S3DirectoryLoader(
                    bucket=self.bucket_name,
                    prefix=prefix,
                    region_name=self.region,
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                )

        except ImportError:
            logger.warning("S3 loaders not available. Install with: pip install boto3")
            return None
        except Exception as e:
            logger.error(f"Failed to create S3 loader: {e}")
            return None


class GCSSource(CloudStorageSource):
    """Google Cloud Storage source implementation."""

    def __init__(
        self,
        bucket_name: str,
        object_name: Optional[str] = None,
        prefix: Optional[str] = None,
        project_id: Optional[str] = None,
        **kwargs,
    ):
        gcs_path = f"gs://{bucket_name}/{object_name or prefix or ''}"
        super().__init__(source_path=gcs_path, **kwargs)
        self.bucket_name = bucket_name
        self.object_name = object_name
        self.prefix = prefix
        self.project_id = project_id

    def can_handle(self, path: str) -> bool:
        """Check if this is a GCS path."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["gs", "gcs"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for GCS paths."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """GCS typically requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """GCS needs Google Cloud credentials."""
        return [CredentialType.SERVICE_ACCOUNT, CredentialType.API_KEY]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GCS loader."""
        try:
            from langchain_community.document_loaders import (
                GCSDirectoryLoader,
                GCSFileLoader,
            )

            # Get credentials if needed
            credentials_path = None

            if self.credential_manager:
                cred = self.credential_manager.get_credential("gcp")
                if cred and cred.credential_type == CredentialType.SERVICE_ACCOUNT:
                    # Assume this is a path to service account JSON
                    credentials_path = cred.value

            # Determine if loading a single file or directory
            if self.object_name and not self.object_name.endswith("/"):
                # Single file
                return GCSFileLoader(
                    project_name=self.project_id,
                    bucket=self.bucket_name,
                    blob=self.object_name,
                    credentials_path=credentials_path,
                )
            else:
                # Directory or prefix
                prefix = self.prefix or self.object_name or ""
                return GCSDirectoryLoader(
                    project_name=self.project_id,
                    bucket=self.bucket_name,
                    prefix=prefix,
                    credentials_path=credentials_path,
                )

        except ImportError:
            logger.warning(
                "GCS loaders not available. Install with: pip install google-cloud-storage"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create GCS loader: {e}")
            return None


class AzureBlobSource(CloudStorageSource):
    """Azure Blob Storage source implementation."""

    def __init__(
        self,
        account_name: str,
        container_name: str,
        blob_name: Optional[str] = None,
        prefix: Optional[str] = None,
        **kwargs,
    ):
        azure_path = (
            f"azure://{account_name}/{container_name}/{blob_name or prefix or ''}"
        )
        super().__init__(source_path=azure_path, **kwargs)
        self.account_name = account_name
        self.container_name = container_name
        self.blob_name = blob_name
        self.prefix = prefix

    def can_handle(self, path: str) -> bool:
        """Check if this is an Azure Blob path."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["azure", "azblob"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Azure Blob paths."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """Azure Blob typically requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """Azure Blob needs Azure credentials."""
        return [CredentialType.CONNECTION_STRING, CredentialType.API_KEY]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Azure Blob loader."""
        try:
            from langchain_community.document_loaders import (
                AzureBlobStorageContainerLoader,
                AzureBlobStorageFileLoader,
            )

            # Get credentials if needed
            connection_string = None
            account_key = None

            if self.credential_manager:
                cred = self.credential_manager.get_credential("azure")
                if cred:
                    if cred.credential_type == CredentialType.CONNECTION_STRING:
                        connection_string = cred.value
                    elif cred.credential_type == CredentialType.API_KEY:
                        account_key = cred.value

            # Determine if loading a single blob or container
            if self.blob_name:
                # Single blob
                return AzureBlobStorageFileLoader(
                    account_name=self.account_name,
                    container=self.container_name,
                    blob_name=self.blob_name,
                    connection_string=connection_string,
                    account_key=account_key,
                )
            else:
                # Container or prefix
                return AzureBlobStorageContainerLoader(
                    account_name=self.account_name,
                    container=self.container_name,
                    prefix=self.prefix,
                    connection_string=connection_string,
                    account_key=account_key,
                )

        except ImportError:
            logger.warning(
                "Azure Blob loaders not available. Install with: pip install azure-storage-blob"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Azure Blob loader: {e}")
            return None


# Export cloud sources
__all__ = [
    "S3Source",
    "GCSSource",
    "AzureBlobSource",
]
