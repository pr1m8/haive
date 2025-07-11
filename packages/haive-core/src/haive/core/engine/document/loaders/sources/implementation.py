"""Enhanced Source Implementation for Document Engine.

This module provides enhanced source type implementations adapted from the original
project_notes with proper integration into the Haive document engine framework.
"""

import logging
import os
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class SourceType(str, Enum):
    """Enhanced source type classification."""

    # File-based sources
    LOCAL_FILE = "local_file"
    LOCAL_DIRECTORY = "local_directory"

    # Web sources
    WEB_URL = "web_url"
    WEB_API = "web_api"

    # Database sources
    DATABASE = "database"

    # Cloud sources
    CLOUD_STORAGE = "cloud_storage"

    # Text sources
    TEXT_INPUT = "text_input"


class CredentialType(str, Enum):
    """Types of credentials supported."""

    API_KEY = "api_key"
    OAUTH2 = "oauth2"
    USERNAME_PASSWORD = "username_password"
    SERVICE_ACCOUNT = "service_account"
    ACCESS_TOKEN = "access_token"
    CONNECTION_STRING = "connection_string"


class Credential(BaseModel):
    """Credential information for authenticated sources."""

    credential_type: CredentialType
    value: str = Field(..., description="The credential value")
    metadata: dict[str, Any] = Field(default_factory=dict)

    class Config:
        extra = "allow"


class CredentialManager:
    """Manages credentials for various source types."""

    def __init__(self):
        self._credentials: dict[str, Credential] = {}
        self._env_prefix = "HAIVE_CRED_"

    def add_credential(self, source_id: str, credential: Credential) -> None:
        """Add a credential for a source."""
        self._credentials[source_id] = credential

    def get_credential(self, source_id: str) -> Credential | None:
        """Get credential for a source."""
        # Try direct lookup first
        if source_id in self._credentials:
            return self._credentials[source_id]

        # Try environment variable
        env_key = f"{self._env_prefix}{source_id.upper()}"
        env_value = os.getenv(env_key)
        if env_value:
            return Credential(credential_type=CredentialType.API_KEY, value=env_value)

        return None

    def has_credential(self, source_id: str) -> bool:
        """Check if credential exists for source."""
        return self.get_credential(source_id) is not None


class EnhancedSource(BaseModel, ABC):
    """Enhanced base class for document sources."""

    source_type: SourceType
    source_path: str = Field(..., description="Path or identifier for the source")
    metadata: dict[str, Any] = Field(default_factory=dict)
    credential_manager: CredentialManager | None = Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def can_handle(self, path: str) -> bool:
        """Check if this source can handle the given path."""

    @abstractmethod
    def get_confidence_score(self, path: str) -> float:
        """Get confidence score (0.0-1.0) for handling this path."""

    def requires_authentication(self) -> bool:
        """Check if this source requires authentication."""
        return False

    def get_credential_requirements(self) -> list[CredentialType]:
        """Get required credential types."""
        return []


class LocalFileSource(EnhancedSource):
    """Source for local files."""

    source_type: SourceType = Field(default=SourceType.LOCAL_FILE)
    file_extensions: list[str] = Field(default_factory=list)

    def can_handle(self, path: str) -> bool:
        """Check if this is a local file."""
        try:
            p = Path(path)
            return p.exists() and p.is_file()
        except (OSError, ValueError):
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for local files."""
        if not self.can_handle(path):
            return 0.0

        p = Path(path)
        if self.file_extensions:
            if p.suffix.lower() in [ext.lower() for ext in self.file_extensions]:
                return 0.9
            return 0.3

        return 0.7


class LocalDirectorySource(EnhancedSource):
    """Source for local directories."""

    source_type: SourceType = Field(default=SourceType.LOCAL_DIRECTORY)
    recursive: bool = Field(default=True)
    include_patterns: list[str] = Field(default_factory=list)
    exclude_patterns: list[str] = Field(default_factory=list)

    def can_handle(self, path: str) -> bool:
        """Check if this is a local directory."""
        try:
            p = Path(path)
            return p.exists() and p.is_dir()
        except (OSError, ValueError):
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for local directories."""
        if not self.can_handle(path):
            return 0.0
        return 0.8


class WebUrlSource(EnhancedSource):
    """Source for web URLs."""

    source_type: SourceType = Field(default=SourceType.WEB_URL)
    allowed_schemes: list[str] = Field(default=["http", "https"])
    allowed_domains: list[str] = Field(default_factory=list)

    def can_handle(self, path: str) -> bool:
        """Check if this is a valid web URL."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in self.allowed_schemes and bool(parsed.netloc)
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for web URLs."""
        if not self.can_handle(path):
            return 0.0

        parsed = urlparse(path)

        # Higher confidence for known domains
        if self.allowed_domains:
            for domain in self.allowed_domains:
                if domain in parsed.netloc:
                    return 0.9
            return 0.4

        return 0.7


class DatabaseSource(EnhancedSource):
    """Source for database connections."""

    source_type: SourceType = Field(default=SourceType.DATABASE)
    supported_schemes: list[str] = Field(
        default=["postgresql", "mysql", "sqlite", "mongodb"]
    )

    def can_handle(self, path: str) -> bool:
        """Check if this is a database URI."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in self.supported_schemes
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for database URIs."""
        if not self.can_handle(path):
            return 0.0
        return 0.8

    def requires_authentication(self) -> bool:
        """Database sources typically require authentication."""
        return True

    def get_credential_requirements(self) -> list[CredentialType]:
        """Database sources need connection credentials."""
        return [CredentialType.USERNAME_PASSWORD, CredentialType.CONNECTION_STRING]


class CloudStorageSource(EnhancedSource):
    """Source for cloud storage."""

    source_type: SourceType = Field(default=SourceType.CLOUD_STORAGE)
    supported_providers: list[str] = Field(default=["s3", "gcs", "azure", "dropbox"])

    def can_handle(self, path: str) -> bool:
        """Check if this is a cloud storage path."""
        try:
            parsed = urlparse(path)
            return any(
                provider in parsed.scheme for provider in self.supported_providers
            )
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for cloud storage."""
        if not self.can_handle(path):
            return 0.0
        return 0.8

    def requires_authentication(self) -> bool:
        """Cloud storage typically requires authentication."""
        return True

    def get_credential_requirements(self) -> list[CredentialType]:
        """Cloud storage needs API credentials."""
        return [CredentialType.API_KEY, CredentialType.SERVICE_ACCOUNT]


class TextInputSource(EnhancedSource):
    """Source for direct text input."""

    source_type: SourceType = Field(default=SourceType.TEXT_INPUT)

    def can_handle(self, path: str) -> bool:
        """Text input can handle anything as fallback."""
        return True

    def get_confidence_score(self, path: str) -> float:
        """Low confidence - fallback option."""
        # Only use as fallback if it looks like direct text
        if not any(char in path for char in ["/", "\\", ":", "."]):
            return 0.2
        return 0.1


class SourceRegistry:
    """Registry for managing source types."""

    def __init__(self):
        self._sources: list[EnhancedSource] = []
        self._register_default_sources()

    def _register_default_sources(self):
        """Register default source types."""
        self.register(LocalFileSource(source_path=""))
        self.register(LocalDirectorySource(source_path=""))
        self.register(WebUrlSource(source_path=""))
        self.register(DatabaseSource(source_path=""))
        self.register(CloudStorageSource(source_path=""))
        self.register(TextInputSource(source_path=""))

    def register(self, source: EnhancedSource):
        """Register a new source type."""
        self._sources.append(source)

    def find_best_source(self, path: str) -> EnhancedSource | None:
        """Find the best source for a given path."""
        candidates = []

        for source in self._sources:
            if source.can_handle(path):
                confidence = source.get_confidence_score(path)
                candidates.append((source, confidence))

        if not candidates:
            return None

        # Sort by confidence (highest first)
        candidates.sort(key=lambda x: x[1], reverse=True)
        best_source, _ = candidates[0]

        # Create a new instance with the specific path
        source_class = type(best_source)
        return source_class(
            source_path=path,
            metadata=best_source.metadata.copy(),
            credential_manager=best_source.credential_manager,
        )

    def find_all_sources(self, path: str) -> list[tuple[EnhancedSource, float]]:
        """Find all sources that can handle a path with confidence scores."""
        candidates = []

        for source in self._sources:
            if source.can_handle(path):
                confidence = source.get_confidence_score(path)
                candidates.append((source, confidence))

        # Sort by confidence (highest first)
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates


# Global registry instance
source_registry = SourceRegistry()


# Export key components
__all__ = [
    "CloudStorageSource",
    "Credential",
    "CredentialManager",
    "CredentialType",
    "DatabaseSource",
    "EnhancedSource",
    "LocalDirectorySource",
    "LocalFileSource",
    "SourceRegistry",
    "SourceType",
    "TextInputSource",
    "WebUrlSource",
    "source_registry",
]
