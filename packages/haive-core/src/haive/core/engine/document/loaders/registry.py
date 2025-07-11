"""
Document loader registry system.

This module provides a registry for document loaders, allowing them to be
registered, looked up, and managed throughout the application.
"""

import inspect
import logging
from typing import Any, Callable, Dict, List, Optional, Type

from langchain_core.document_loaders.base import BaseLoader
from pydantic import BaseModel, ConfigDict, Field, create_model

from haive.core.engine.document.loaders.sources.source_types import (
    SourceCategory as SourceType,
)
from haive.core.registry.base import AbstractRegistry

logger = logging.getLogger(__name__)


class LoaderMetadata(BaseModel):
    """Metadata for a document loader."""

    name: str = Field(description="Name of the loader")
    source_type: SourceType = Field(description="Type of source this loader handles")
    description: str = Field(default="", description="Description of the loader")
    requires_async: bool = Field(
        default=False, description="Whether this loader requires async operations"
    )
    file_extensions: List[str] = Field(
        default_factory=list,
        description="List of file extensions this loader can handle",
    )
    url_patterns: List[str] = Field(
        default_factory=list, description="List of URL patterns this loader can handle"
    )
    has_config_schema: bool = Field(
        default=False, description="Whether this loader has a configuration schema"
    )
    config_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Pydantic model for loader configuration"
    )

    model_config = {"arbitrary_types_allowed": True}


class DocumentLoaderRegistry(AbstractRegistry[Type[BaseLoader]]):
    """
    Registry for document loaders.

    This registry keeps track of document loader classes and their metadata,
    allowing for discovery and instantiation of loaders based on source types.
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "DocumentLoaderRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """Initialize the registry with empty storage."""
        self.loaders_by_source: Dict[SourceType, Dict[str, Type[BaseLoader]]] = {
            source_type: {} for source_type in SourceType
        }
        self.loaders_by_name: Dict[str, Type[BaseLoader]] = {}
        self.loader_metadata: Dict[str, LoaderMetadata] = {}

    def register(
        self, loader_class: Type[BaseLoader], metadata: LoaderMetadata
    ) -> Type[BaseLoader]:
        """
        Register a document loader with metadata.

        Args:
            loader_class: Loader class to register
            metadata: Metadata for the loader

        Returns:
            The registered loader class
        """
        name = metadata.name
        source_type = metadata.source_type

        self.loaders_by_source[source_type][name] = loader_class
        self.loaders_by_name[name] = loader_class
        self.loader_metadata[name] = metadata

        logger.debug(
            f"Registered document loader: {name} for source type {source_type}"
        )
        return loader_class

    def get(self, item_type: SourceType, name: str) -> Optional[Type[BaseLoader]]:
        """
        Get a loader by source type and name.

        Args:
            item_type: Source type
            name: Loader name

        Returns:
            Loader class if found, None otherwise
        """
        return self.loaders_by_source[item_type].get(name)

    def find_by_id(self, id: str) -> Optional[Type[BaseLoader]]:
        """
        Find a loader by name (used for compatibility with AbstractRegistry).

        Args:
            id: Loader name

        Returns:
            Loader class if found, None otherwise
        """
        return self.loaders_by_name.get(id)

    def find_by_name(self, name: str) -> Optional[Type[BaseLoader]]:
        """
        Find a loader by name.

        Args:
            name: Loader name

        Returns:
            Loader class if found, None otherwise
        """
        return self.loaders_by_name.get(name)

    def get_metadata(self, name: str) -> Optional[LoaderMetadata]:
        """
        Get metadata for a specific loader.

        Args:
            name: Loader name

        Returns:
            Loader metadata if found, None otherwise
        """
        return self.loader_metadata.get(name)

    def list(self, item_type: SourceType) -> List[str]:
        """
        List all loader names for a specific source type.

        Args:
            item_type: Source type

        Returns:
            List of loader names
        """
        return list(self.loaders_by_source[item_type].keys())

    def get_all(self, item_type: SourceType) -> Dict[str, Type[BaseLoader]]:
        """
        Get all loaders for a specific source type.

        Args:
            item_type: Source type

        Returns:
            Dictionary mapping loader names to loader classes
        """
        return self.loaders_by_source[item_type]

    def get_all_metadata(self) -> Dict[str, LoaderMetadata]:
        """
        Get metadata for all registered loaders.

        Returns:
            Dictionary mapping loader names to metadata
        """
        return self.loader_metadata

    def find_loader_for_file(self, file_path: str) -> List[Type[BaseLoader]]:
        """
        Find loaders that can handle a specific file extension.

        Args:
            file_path: Path to the file

        Returns:
            List of loader classes that can handle this file
        """
        import os

        _, ext = os.path.splitext(file_path)
        if not ext:
            return []

        ext = ext.lstrip(".")

        matching_loaders = []
        for name, metadata in self.loader_metadata.items():
            if ext in metadata.file_extensions:
                matching_loaders.append(self.loaders_by_name[name])

        return matching_loaders

    def find_loader_for_url(self, url: str) -> List[Type[BaseLoader]]:
        """
        Find loaders that can handle a specific URL pattern.

        Args:
            url: URL to handle

        Returns:
            List of loader classes that can handle this URL
        """
        import re

        matching_loaders = []
        for name, metadata in self.loader_metadata.items():
            for pattern in metadata.url_patterns:
                if re.search(pattern, url):
                    matching_loaders.append(self.loaders_by_name[name])
                    break

        return matching_loaders

    def clear(self) -> None:
        """Clear all registrations."""
        self.loaders_by_source = {source_type: {} for source_type in SourceType}
        self.loaders_by_name = {}
        self.loader_metadata = {}


def register_loader(
    source_type: SourceType,
    name: Optional[str] = None,
    description: Optional[str] = None,
    requires_async: bool = False,
    file_extensions: Optional[List[str]] = None,
    url_patterns: Optional[List[str]] = None,
    config_schema: Optional[Type[BaseModel]] = None,
) -> Callable[[Type[BaseLoader]], Type[BaseLoader]]:
    """
    Decorator to register a document loader.

    Args:
        source_type: Type of source this loader handles
        name: Optional custom name for the loader
        description: Optional description of the loader
        requires_async: Whether this loader requires async operations
        file_extensions: List of file extensions this loader can handle
        url_patterns: List of URL patterns this loader can handle
        config_schema: Optional Pydantic model for configuration

    Returns:
        Decorator function
    """

    def decorator(loader_class: Type[BaseLoader]) -> Type[BaseLoader]:
        registry = DocumentLoaderRegistry.get_instance()

        # Generate a name if not provided
        loader_name = name or loader_class.__name__

        # Create and attach a configuration schema if not provided
        if not hasattr(loader_class, "Config") and config_schema is None:
            # Extract init parameters
            sig = inspect.signature(loader_class.__init__)
            params = {}

            for param_name, param in sig.parameters.items():
                if param_name == "self":
                    continue

                # Get parameter type hint and default value
                annotation = param.annotation
                if annotation == inspect.Parameter.empty:
                    annotation = Any

                default = (
                    ... if param.default == inspect.Parameter.empty else param.default
                )
                params[param_name] = (annotation, default)

            # Create config model dynamically
            config_model = create_model(
                f"{loader_name}Config",
                **params,
                __config__=ConfigDict(extra="allow"),
            )

            # Attach to loader class
            loader_class.Config = config_model

        final_config_schema = config_schema or getattr(loader_class, "Config", None)

        # Create metadata
        metadata = LoaderMetadata(
            name=loader_name,
            source_type=source_type,
            description=description or loader_class.__doc__ or "",
            requires_async=requires_async,
            file_extensions=file_extensions or [],
            url_patterns=url_patterns or [],
            has_config_schema=final_config_schema is not None,
            config_schema=final_config_schema,
        )

        # Register the loader
        return registry.register(loader_class, metadata)

    return decorator


# Instantiate registry singleton
document_loader_registry = DocumentLoaderRegistry.get_instance()


# Convenience functions
def get_default_registry() -> DocumentLoaderRegistry:
    """Get the default document loader registry."""
    return document_loader_registry


def get_loader(loader_name: str) -> Optional[Type[BaseLoader]]:
    """Get a loader by name from the default registry."""
    return document_loader_registry.find_by_name(loader_name)


def create_loader(loader_name: str, **kwargs) -> Optional[BaseLoader]:
    """Create a loader instance by name."""
    loader_class = get_loader(loader_name)
    if loader_class:
        return loader_class(**kwargs)
    return None
