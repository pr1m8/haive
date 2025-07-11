"""Base classes for document loaders.

This module provides the foundation for all document loaders in the system,
including base source classes, pattern matching, and loader strategies.
Kept under 300 lines as per code style guidelines.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional, Type

from langchain_core.document_loaders import BaseLoader
from pydantic import BaseModel, Field

from haive.core.common.mixins.secure_config import SecureConfigMixin
from haive.core.engine.document.config import LoaderPreference


class LoaderSpeed(str, Enum):
    """Loader speed classification."""

    FAST = "fast"
    MEDIUM = "medium"
    SLOW = "slow"


class LoaderQuality(str, Enum):
    """Loader quality classification."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class LoaderStrategy:
    """Information about a specific loader strategy."""

    name: str
    loader_class: str  # Fully qualified class name
    module: str = "langchain_community.document_loaders"

    # Characteristics
    speed: LoaderSpeed = LoaderSpeed.MEDIUM
    quality: LoaderQuality = LoaderQuality.MEDIUM

    # Capabilities
    supports_lazy: bool = False
    supports_async: bool = False
    requires_auth: bool = False

    # Best use cases
    best_for: list[str] = field(default_factory=list)

    # Required/optional packages
    required_packages: list[str] = field(default_factory=list)
    optional_packages: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate strategy configuration."""
        if not self.name:
            raise ValueError("Strategy name is required")
        if not self.loader_class:
            raise ValueError("Loader class is required")


@dataclass
class SourcePattern:
    """Pattern specification for source matching."""

    # File patterns
    file_extensions: list[str] = field(default_factory=list)
    mime_types: list[str] = field(default_factory=list)

    # URL patterns
    domain_patterns: list[str] = field(default_factory=list)
    url_patterns: list[str] = field(default_factory=list)
    scheme_patterns: list[str] = field(default_factory=list)

    # Content patterns
    content_types: list[str] = field(default_factory=list)

    # Priority for matching
    priority: int = 0

    # Custom matcher function
    custom_matcher: Callable[[str], bool] | None = None


class BaseSource(BaseModel, ABC):
    """Abstract base class for all document sources."""

    # Source identification
    source_type: str | None = Field(None, description="Type identifier")

    # Metadata
    description: str | None = Field(None, description="Source description")
    confidence_score: float = Field(0.0, description="Confidence in source match")

    class Config:
        """Configuration for source classes."""

        # Pattern matching
        patterns: list[SourcePattern] = []

        # Available loader strategies
        loader_strategies: dict[str, LoaderStrategy] = {}

        # Default strategy
        default_strategy: str | None = None

        # Required credentials
        required_credentials: list[str] = []

    @classmethod
    def get_patterns(cls) -> list[SourcePattern]:
        """Get all patterns for this source."""
        return getattr(cls.Config, "patterns", [])

    @classmethod
    def get_loader_strategies(cls) -> dict[str, LoaderStrategy]:
        """Get available loader strategies."""
        return getattr(cls.Config, "loader_strategies", {})

    @abstractmethod
    def create_loader(self, strategy: str | None = None, **kwargs) -> BaseLoader:
        """Create a document loader instance.

        Args:
            strategy: Name of strategy to use
            **kwargs: Additional loader arguments

        Returns:
            Configured document loader
        """

    def get_best_strategy(
        self, preference: LoaderPreference = LoaderPreference.BALANCED
    ) -> LoaderStrategy | None:
        """Get best strategy based on preference."""
        strategies = self.get_loader_strategies()
        if not strategies:
            return None

        if preference == LoaderPreference.SPEED:
            # Prefer fast loaders
            for strategy in strategies.values():
                if strategy.speed == LoaderSpeed.FAST:
                    return strategy

        elif preference == LoaderPreference.QUALITY:
            # Prefer high quality loaders
            for strategy in strategies.values():
                if strategy.quality == LoaderQuality.HIGH:
                    return strategy

        # Return first available strategy
        return next(iter(strategies.values()))

    def _import_loader_class(self, strategy: LoaderStrategy) -> type[BaseLoader]:
        """Dynamically import a loader class."""
        try:
            module = __import__(strategy.module, fromlist=[strategy.loader_class])
            return getattr(module, strategy.loader_class)
        except (ImportError, AttributeError) as e:
            raise ImportError(
                f"Failed to import {strategy.loader_class} from {strategy.module}: {e}"
            )


class LocalSource(BaseSource):
    """Base class for local file sources."""

    file_path: str | None = Field(None, description="Path to local file")
    encoding: str = Field("utf-8", description="File encoding")

    def validate_file_exists(self) -> bool:
        """Check if file exists."""
        if not self.file_path:
            return False
        from pathlib import Path

        return Path(self.file_path).exists()


class RemoteSource(BaseSource, SecureConfigMixin):
    """Base class for remote sources with credential support."""

    url: str | None = Field(None, description="Remote URL")
    provider: str = Field("generic", description="Provider name for credentials")

    # SecureConfigMixin fields
    api_key: str | None = Field(None, description="API key if required")

    def requires_authentication(self) -> bool:
        """Check if this source requires authentication."""
        return any(
            strategy.requires_auth for strategy in self.get_loader_strategies().values()
        )


class DirectorySource(LocalSource):
    """Base class for directory sources."""

    directory_path: str | None = Field(None, description="Directory path")
    glob_pattern: str = Field("**/*", description="File glob pattern")
    recursive: bool = Field(True, description="Recursive search")


class DatabaseSource(BaseSource, SecureConfigMixin):
    """Base class for database sources."""

    connection_string: str | None = Field(None, description="Database connection")
    query: str | None = Field(None, description="Query to execute")
    provider: str = Field("database", description="Database provider")


class CloudSource(RemoteSource):
    """Base class for cloud storage sources."""

    bucket_name: str | None = Field(None, description="Bucket/container name")
    prefix: str | None = Field(None, description="Object prefix")


# Helper function for creating simple loaders
def create_simple_loader(
    source_class: type[BaseSource],
    loader_class_name: str,
    module: str = "langchain_community.document_loaders",
    **loader_kwargs,
) -> BaseLoader:
    """Helper to create a simple loader instance."""
    try:
        module_obj = __import__(module, fromlist=[loader_class_name])
        loader_class = getattr(module_obj, loader_class_name)
        return loader_class(**loader_kwargs)
    except (ImportError, AttributeError) as e:
        raise ImportError(f"Failed to create loader {loader_class_name}: {e}")
