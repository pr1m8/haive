"""Base classes for document sources.

This module provides base classes for different types of document sources.
Sources represent the location/type of documents, while loaders handle the actual loading.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin


class BaseSource(BaseModel, ABC):
    """Abstract base class for all document sources."""

    # Source identification
    source_type: str | None = Field(None, description="Type identifier")
    source_path: str | None = Field(None, description="Path or URL to source")

    # Metadata
    description: str | None = Field(None, description="Source description")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @abstractmethod
    def validate_source(self) -> bool:
        """Validate that the source is accessible/valid."""

    @abstractmethod
    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs to pass to the loader."""


class LocalSource(BaseSource):
    """Base class for local file sources."""

    file_path: str = Field(..., description="Path to local file")
    encoding: str = Field("utf-8", description="File encoding")

    def validate_source(self) -> bool:
        """Check if file exists."""
        from pathlib import Path

        return Path(self.file_path).exists()

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for local file loaders."""
        return {
            "file_path": self.file_path,
            "encoding": self.encoding,
        }


class DirectorySource(LocalSource):
    """Source for directory of files."""

    file_path: str | None = Field(None, description="Not used for directories")
    directory_path: str = Field(..., description="Path to directory")
    glob_pattern: str = Field("**/*", description="File glob pattern")
    recursive: bool = Field(True, description="Recursive search")
    exclude_patterns: list[str] = Field(
        default_factory=list, description="Patterns to exclude"
    )

    def validate_source(self) -> bool:
        """Check if directory exists."""
        from pathlib import Path

        return Path(self.directory_path).exists()

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for directory loaders."""
        return {
            "path": self.directory_path,
            "glob": self.glob_pattern,
            "recursive": self.recursive,
            "exclude": self.exclude_patterns,
        }


class RemoteSource(BaseSource, SecureConfigMixin):
    """Base class for remote sources with credential support."""

    url: str = Field(..., description="Remote URL")
    headers: dict[str, str] = Field(default_factory=dict, description="HTTP headers")

    # For SecureConfigMixin
    provider: str = Field("generic", description="Provider name for credentials")
    api_key: SecretStr | None = Field(None, description="API key if required")

    def validate_source(self) -> bool:
        """Validate URL format."""
        from urllib.parse import urlparse

        try:
            result = urlparse(self.url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for remote loaders."""
        kwargs = {
            "url": self.url,
            "headers": self.headers,
        }

        # Add API key if available
        api_key = self.get_api_key()
        if api_key:
            kwargs["api_key"] = api_key

        return kwargs


class DatabaseSource(BaseSource, SecureConfigMixin):
    """Base class for database sources."""

    connection_string: str = Field(..., description="Database connection string")
    query: str | None = Field(None, description="Query to execute")
    table_name: str | None = Field(None, description="Table to load from")

    # For SecureConfigMixin
    provider: str = Field("database", description="Database provider")

    def validate_source(self) -> bool:
        """Basic validation of connection string."""
        return bool(self.connection_string)

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for database loaders."""
        kwargs = {
            "connection_string": self.connection_string,
        }

        if self.query:
            kwargs["query"] = self.query
        if self.table_name:
            kwargs["table_name"] = self.table_name

        return kwargs


class CloudSource(RemoteSource):
    """Base class for cloud storage sources."""

    bucket_name: str = Field(..., description="Bucket/container name")
    object_key: str | None = Field(None, description="Specific object key")
    prefix: str | None = Field(None, description="Object prefix for listing")

    # Override provider default
    provider: str = Field("aws", description="Cloud provider")

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for cloud storage loaders."""
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "bucket": self.bucket_name,
            }
        )

        if self.object_key:
            kwargs["key"] = self.object_key
        if self.prefix:
            kwargs["prefix"] = self.prefix

        return kwargs


# Concrete source implementations can be registered
__all__ = [
    "BaseSource",
    "CloudSource",
    "DatabaseSource",
    "DirectorySource",
    "LocalSource",
    "RemoteSource",
]
