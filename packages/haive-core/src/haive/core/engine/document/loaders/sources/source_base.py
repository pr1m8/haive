"""Base source classes for document loaders.

Sources are data models that represent where documents come from.
They don't load documents themselves - they just hold the configuration
and metadata needed by loaders.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin


class BaseSource(BaseModel, ABC):
    """Abstract base class for all document sources.

    A source is a data model that represents where documents come from.
    It contains all the information needed by a loader to actually load documents.
    """

    # Source identification
    source_type: str | None = Field(None, description="Type identifier for registry")
    source_id: str | None = Field(None, description="Unique identifier for this source")

    # Metadata
    description: str | None = Field(None, description="Human-readable description")
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
    tags: list[str] = Field(default_factory=list, description="Tags for categorization")

    # Configuration for associated loaders
    preferred_loader: str | None = Field(None, description="Preferred loader name")
    loader_config: dict[str, Any] = Field(
        default_factory=dict, description="Config for loaders"
    )

    @abstractmethod
    def validate_source(self) -> bool:
        """Validate that the source is accessible/valid.

        Returns:
            True if source is valid and accessible
        """

    @abstractmethod
    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs to pass to the document loader.

        Returns:
            Dictionary of kwargs for the loader
        """

    def to_dict(self) -> dict[str, Any]:
        """Convert source to dictionary for serialization."""
        return self.model_dump(exclude_none=True)


class LocalSource(BaseSource):
    """Base class for local file sources."""

    file_path: str = Field(..., description="Path to local file")
    encoding: str = Field("utf-8", description="File encoding")

    # File metadata
    file_size: int | None = Field(None, description="File size in bytes")
    last_modified: str | None = Field(None, description="Last modified timestamp")

    def validate_source(self) -> bool:
        """Check if file exists and is readable."""
        from pathlib import Path

        try:
            path = Path(self.file_path)
            return path.exists() and path.is_file()
        except Exception:
            return False

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for local file loaders."""
        kwargs = {
            "file_path": self.file_path,
            "encoding": self.encoding,
        }
        kwargs.update(self.loader_config)
        return kwargs


class DirectorySource(BaseSource):
    """Source for directory of files."""

    directory_path: str = Field(..., description="Path to directory")
    glob_pattern: str = Field("**/*", description="File glob pattern")
    recursive: bool = Field(True, description="Recursive search")
    exclude_patterns: list[str] = Field(
        default_factory=list, description="Patterns to exclude"
    )

    # Directory metadata
    file_count: int | None = Field(None, description="Number of files found")

    def validate_source(self) -> bool:
        """Check if directory exists."""
        from pathlib import Path

        try:
            path = Path(self.directory_path)
            return path.exists() and path.is_dir()
        except Exception:
            return False

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for directory loaders."""
        kwargs = {
            "path": self.directory_path,
            "glob": self.glob_pattern,
            "recursive": self.recursive,
            "exclude": self.exclude_patterns,
        }
        kwargs.update(self.loader_config)
        return kwargs


class RemoteSource(BaseSource, SecureConfigMixin):
    """Base class for remote sources with credential support.

    Integrates SecureConfigMixin for secure credential handling.
    """

    url: str = Field(..., description="Remote URL")
    headers: dict[str, str] = Field(default_factory=dict, description="HTTP headers")
    timeout: int = Field(30, description="Request timeout in seconds")

    # For SecureConfigMixin - these enable automatic credential resolution
    provider: str = Field("generic", description="Provider name for credentials")
    api_key: SecretStr | None = Field(None, description="API key if required")

    # Additional auth options
    auth_type: str | None = Field(None, description="Auth type: bearer, basic, oauth")
    username: str | None = Field(None, description="Username for basic auth")
    password: SecretStr | None = Field(None, description="Password for basic auth")

    def validate_source(self) -> bool:
        """Validate URL format and optionally test connectivity."""
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
            "headers": self.headers.copy(),
            "timeout": self.timeout,
        }

        # Add authentication if available
        api_key = self.get_api_key()  # From SecureConfigMixin
        if api_key:
            if self.auth_type == "bearer":
                kwargs["headers"]["Authorization"] = f"Bearer {api_key}"
            elif self.auth_type == "basic" and self.username:
                # For basic auth, api_key is used as password
                import base64

                creds = base64.b64encode(f"{self.username}:{api_key}".encode()).decode()
                kwargs["headers"]["Authorization"] = f"Basic {creds}"
            else:
                # Default: add as api_key parameter
                kwargs["api_key"] = api_key

        kwargs.update(self.loader_config)
        return kwargs


class DatabaseSource(BaseSource, SecureConfigMixin):
    """Base class for database sources."""

    connection_string: str | None = Field(None, description="Full connection string")

    # Connection components (alternative to connection string)
    host: str | None = Field(None, description="Database host")
    port: int | None = Field(None, description="Database port")
    database: str | None = Field(None, description="Database name")
    username: str | None = Field(None, description="Database username")
    password: SecretStr | None = Field(None, description="Database password")

    # Query configuration
    query: str | None = Field(None, description="SQL query to execute")
    table_name: str | None = Field(None, description="Table to load from")
    schema_name: str | None = Field(None, description="Schema name")

    # For SecureConfigMixin - DatabaseSource uses password instead of api_key
    provider: str = Field("database", description="Database provider")
    api_key: SecretStr | None = Field(None, description="Not used for databases")

    def validate_source(self) -> bool:
        """Basic validation of connection parameters."""
        if self.connection_string:
            return bool(self.connection_string)
        return bool(self.host and self.database)

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for database loaders."""
        kwargs = {}

        # Use connection string or build it
        if self.connection_string:
            kwargs["connection_string"] = self.connection_string
        elif self.username and self.password:
            pwd = self.password.get_secret_value() if self.password else ""
            conn_str = f"{self.provider}://{self.username}:{pwd}@{self.host}"
            if self.port:
                conn_str += f":{self.port}"
            conn_str += f"/{self.database}"
            kwargs["connection_string"] = conn_str
        else:
            kwargs["host"] = self.host
            kwargs["port"] = self.port
            kwargs["database"] = self.database

        if self.query:
            kwargs["query"] = self.query
        elif self.table_name:
            kwargs["table_name"] = self.table_name
            if self.schema_name:
                kwargs["schema_name"] = self.schema_name

        kwargs.update(self.loader_config)
        return kwargs


class CloudSource(RemoteSource):
    """Base class for cloud storage sources.

    Extends RemoteSource with cloud-specific fields.
    """

    bucket_name: str = Field(..., description="Bucket/container name")
    object_key: str | None = Field(None, description="Specific object key")
    prefix: str | None = Field(None, description="Object prefix for listing")
    region: str | None = Field(None, description="Cloud region")

    # Cloud-specific auth (in addition to SecureConfigMixin)
    access_key_id: str | None = Field(None, description="Access key ID")
    secret_access_key: SecretStr | None = Field(None, description="Secret access key")
    session_token: SecretStr | None = Field(None, description="Session token")

    # Override provider default with cloud-specific values
    provider: str = Field("aws", description="Cloud provider: aws, gcp, azure")

    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for cloud storage loaders."""
        # Start with base remote kwargs
        kwargs = super().get_loader_kwargs()

        # Add cloud-specific parameters
        kwargs.update(
            {
                "bucket": self.bucket_name,
                "region": self.region,
            }
        )

        if self.object_key:
            kwargs["key"] = self.object_key
        if self.prefix:
            kwargs["prefix"] = self.prefix

        # Add cloud credentials if provided
        if self.access_key_id and self.secret_access_key:
            kwargs["aws_access_key_id"] = self.access_key_id
            kwargs["aws_secret_access_key"] = self.secret_access_key.get_secret_value()
            if self.session_token:
                kwargs["aws_session_token"] = self.session_token.get_secret_value()

        return kwargs


# Specialized source types can be created by extending these base classes
__all__ = [
    "BaseSource",
    "CloudSource",
    "DatabaseSource",
    "DirectorySource",
    "LocalSource",
    "RemoteSource",
]
