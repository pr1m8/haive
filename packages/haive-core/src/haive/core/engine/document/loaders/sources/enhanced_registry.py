"""Enhanced registry system for comprehensive source management.

This module provides an advanced registry system that supports all 231 langchain_community
loaders with easy decorator-based registration, bulk capabilities, and comprehensive typing.
"""

import logging
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set, Type, TypeVar, Union

from .registry import LoaderMapping
from .source_types import (
    BaseSource,
    CredentialType,
    DatabaseSource,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCapabilities,
    SourceCategory,
)

logger = logging.getLogger(__name__)

TSource = TypeVar("TSource", bound=BaseSource)


@dataclass
class BulkLoaderInfo:
    """Information about bulk loading capabilities."""

    supports_bulk: bool = False
    supports_recursive: bool = False
    supports_filtering: bool = False
    max_concurrent: int = 1
    preferred_batch_size: int = 10
    rate_limit_delay: float = 0.0


@dataclass
class EnhancedSourceRegistration:
    """Enhanced registration information for a source type."""

    # Basic info
    name: str
    source_class: Type[BaseSource]
    category: SourceCategory
    description: str

    # Capabilities
    capabilities: SourceCapabilities
    bulk_info: BulkLoaderInfo

    # Loaders
    loaders: Dict[str, LoaderMapping]
    default_loader: str

    # Matching criteria
    file_extensions: Set[str]
    url_patterns: Set[str]
    schemes: Set[str]
    mime_types: Set[str]

    # Priority and metadata
    priority: int = 0
    author: Optional[str] = None
    version: str = "1.0.0"
    dependencies: Set[str] = field(default_factory=set)


class EnhancedSourceRegistry:
    """Enhanced registry supporting all langchain_community loaders."""

    def __init__(self):
        # Core registry data
        self._sources: Dict[str, EnhancedSourceRegistration] = {}

        # Indexing for fast lookup
        self._extension_index: Dict[str, List[str]] = {}
        self._url_pattern_index: Dict[str, List[str]] = {}
        self._scheme_index: Dict[str, List[str]] = {}
        self._mime_index: Dict[str, List[str]] = {}
        self._category_index: Dict[SourceCategory, List[str]] = {}

        # Bulk loader tracking
        self._bulk_loaders: Set[str] = set()
        self._recursive_loaders: Set[str] = set()

        # Statistics
        self._registration_count = 0
        self._bulk_loader_count = 0

    def register(
        self,
        name: str,
        source_class: Type[BaseSource],
        category: SourceCategory,
        description: str = "",
        # Capabilities
        capabilities: Optional[SourceCapabilities] = None,
        is_bulk_loader: bool = False,
        supports_recursive: bool = False,
        supports_filtering: bool = False,
        max_concurrent: int = 1,
        rate_limit_delay: float = 0.0,
        # Loaders
        loaders: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
        default_loader: str = "default",
        # Matching criteria
        file_extensions: Optional[List[str]] = None,
        url_patterns: Optional[List[str]] = None,
        schemes: Optional[List[str]] = None,
        mime_types: Optional[List[str]] = None,
        # Metadata
        priority: int = 0,
        author: Optional[str] = None,
        version: str = "1.0.0",
        dependencies: Optional[List[str]] = None,
        # Credential requirements
        requires_credentials: bool = False,
        credential_type: CredentialType = CredentialType.NONE,
    ) -> EnhancedSourceRegistration:
        """Register a source type with comprehensive metadata."""

        # Create capabilities if not provided
        if capabilities is None:
            capabilities = SourceCapabilities(
                is_bulk_loader=is_bulk_loader,
                supports_recursive=supports_recursive,
                supports_filtering=supports_filtering,
                requires_credentials=requires_credentials,
                credential_type=credential_type,
                file_extensions=set(file_extensions or []),
                url_patterns=set(url_patterns or []),
                mime_types=set(mime_types or []),
            )

        # Create bulk loader info
        bulk_info = BulkLoaderInfo(
            supports_bulk=is_bulk_loader,
            supports_recursive=supports_recursive,
            supports_filtering=supports_filtering,
            max_concurrent=max_concurrent,
            rate_limit_delay=rate_limit_delay,
        )

        # Process loaders
        processed_loaders = {}
        if loaders:
            for loader_name, loader_def in loaders.items():
                if isinstance(loader_def, str):
                    # Simple string loader
                    processed_loaders[loader_name] = LoaderMapping(
                        name=loader_def,
                        module="langchain_community.document_loaders",
                        speed="medium",
                        quality="medium",
                    )
                else:
                    # Dictionary definition
                    processed_loaders[loader_name] = LoaderMapping(
                        name=loader_def.get(
                            "class", loader_def.get("name", loader_name)
                        ),
                        module=loader_def.get(
                            "module", "langchain_community.document_loaders"
                        ),
                        speed=loader_def.get("speed", "medium"),
                        quality=loader_def.get("quality", "medium"),
                        requires_packages=loader_def.get("requires_packages", []),
                    )

        # Create registration
        registration = EnhancedSourceRegistration(
            name=name,
            source_class=source_class,
            category=category,
            description=description,
            capabilities=capabilities,
            bulk_info=bulk_info,
            loaders=processed_loaders,
            default_loader=default_loader,
            file_extensions=set(file_extensions or []),
            url_patterns=set(url_patterns or []),
            schemes=set(schemes or []),
            mime_types=set(mime_types or []),
            priority=priority,
            author=author,
            version=version,
            dependencies=set(dependencies or []),
        )

        # Store registration
        self._sources[name] = registration

        # Update indexes
        self._update_indexes(name, registration)

        # Update statistics
        self._registration_count += 1
        if is_bulk_loader:
            self._bulk_loaders.add(name)
            self._bulk_loader_count += 1
        if supports_recursive:
            self._recursive_loaders.add(name)

        logger.info(
            f"Registered source '{name}' with {len(processed_loaders)} loaders, "
            f"{len(file_extensions or [])} extensions"
        )

        return registration

    def _update_indexes(self, name: str, registration: EnhancedSourceRegistration):
        """Update all lookup indexes."""

        # File extensions
        for ext in registration.file_extensions:
            if ext not in self._extension_index:
                self._extension_index[ext] = []
            self._extension_index[ext].append(name)

        # URL patterns
        for pattern in registration.url_patterns:
            if pattern not in self._url_pattern_index:
                self._url_pattern_index[pattern] = []
            self._url_pattern_index[pattern].append(name)

        # Schemes
        for scheme in registration.schemes:
            if scheme not in self._scheme_index:
                self._scheme_index[scheme] = []
            self._scheme_index[scheme].append(name)

        # MIME types
        for mime in registration.mime_types:
            if mime not in self._mime_index:
                self._mime_index[mime] = []
            self._mime_index[mime].append(name)

        # Categories
        if registration.category not in self._category_index:
            self._category_index[registration.category] = []
        self._category_index[registration.category].append(name)

    def find_bulk_loaders(self) -> List[str]:
        """Find all sources that support bulk loading."""
        return list(self._bulk_loaders)

    def find_recursive_loaders(self) -> List[str]:
        """Find all sources that support recursive loading."""
        return list(self._recursive_loaders)

    def find_sources_by_category(self, category: SourceCategory) -> List[str]:
        """Find all sources in a specific category."""
        return self._category_index.get(category, [])

    def find_sources_with_capability(self, capability: LoaderCapability) -> List[str]:
        """Find all sources with a specific capability."""
        result = []
        for name, registration in self._sources.items():
            if capability in registration.capabilities.capabilities:
                result.append(name)
        return result

    def get_statistics(self) -> Dict[str, Any]:
        """Get registry statistics."""
        category_counts = {
            category.value: len(sources)
            for category, sources in self._category_index.items()
        }

        return {
            "total_sources": self._registration_count,
            "bulk_loaders": self._bulk_loader_count,
            "recursive_loaders": len(self._recursive_loaders),
            "categories": category_counts,
            "extensions_covered": len(self._extension_index),
            "url_patterns_covered": len(self._url_pattern_index),
            "schemes_covered": len(self._scheme_index),
        }

    def get_source_loaders(self, source_name: str) -> Dict[str, LoaderMapping]:
        """Get all loaders for a given source name."""
        registration = self._sources.get(source_name)
        if registration:
            return registration.loaders
        return {}

    def find_source_for_path(self, path: str) -> Optional[EnhancedSourceRegistration]:
        """Find the best source for a given path."""
        from ..path_analyzer import PathAnalyzer

        # Analyze the path
        analysis = PathAnalyzer.analyze(path)

        candidates = []

        # Try file extension match
        if analysis.file_extension:
            names = self._extension_index.get(analysis.file_extension.lower(), [])
            for name in names:
                registration = self._sources[name]
                candidates.append((registration.priority, registration))

        # Try URL pattern match
        if analysis.is_remote and analysis.domain:
            for pattern, names in self._url_pattern_index.items():
                if pattern in analysis.domain:
                    for name in names:
                        registration = self._sources[name]
                        candidates.append((registration.priority, registration))

        # Try scheme match
        if analysis.url_components:
            scheme = analysis.url_components.get("scheme")
            if scheme:
                names = self._scheme_index.get(scheme, [])
                for name in names:
                    registration = self._sources[name]
                    candidates.append((registration.priority, registration))

        # Return highest priority candidate
        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            return candidates[0][1]

        return None

    def create_source(self, path: str, **kwargs) -> Optional[BaseSource]:
        """Create a source instance for the given path."""
        registration = self.find_source_for_path(path)
        if not registration:
            return None

        from ..path_analyzer import PathAnalyzer

        analysis = PathAnalyzer.analyze(path)

        # Prepare source creation kwargs
        source_kwargs = {
            "source_type": registration.name,
            "source_id": f"{registration.name}:{path}",
            "category": registration.category,
            "capabilities": registration.capabilities,
            **kwargs,
        }

        # Add path-specific kwargs
        if analysis.is_local and analysis.is_file:
            source_kwargs["file_path"] = path
        elif analysis.is_remote:
            source_kwargs["url"] = path

        try:
            return registration.source_class(**source_kwargs)
        except Exception as e:
            logger.error(f"Failed to create source for {path}: {e}")
            return None


# Global enhanced registry instance
enhanced_registry = EnhancedSourceRegistry()


# =============================================================================
# Enhanced Decorator System
# =============================================================================


def register_source(
    name: str,
    category: SourceCategory,
    description: str = "",
    # Quick setup for common cases
    file_extensions: Optional[List[str]] = None,
    url_patterns: Optional[List[str]] = None,
    schemes: Optional[List[str]] = None,
    mime_types: Optional[List[str]] = None,
    # Loader definitions
    loaders: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None,
    default_loader: str = "default",
    # Capabilities
    is_bulk_loader: bool = False,
    supports_recursive: bool = False,
    supports_filtering: bool = False,
    supports_scrape_all: bool = False,
    capabilities: Optional[List[LoaderCapability]] = None,
    # Performance characteristics
    max_concurrent: int = 1,
    rate_limit_delay: float = 0.0,
    typical_speed: str = "medium",
    typical_quality: str = "medium",
    memory_usage: str = "medium",
    # Credentials
    requires_credentials: bool = False,
    credential_type: CredentialType = CredentialType.NONE,
    # Metadata
    priority: int = 0,
    author: Optional[str] = None,
    version: str = "1.0.0",
    dependencies: Optional[List[str]] = None,
) -> Callable[[Type[TSource]], Type[TSource]]:
    """Enhanced decorator for registering source types."""

    def decorator(source_class: Type[TSource]) -> Type[TSource]:

        # Create capabilities
        source_capabilities = SourceCapabilities(
            is_bulk_loader=is_bulk_loader,
            supports_recursive=supports_recursive,
            supports_filtering=supports_filtering,
            requires_credentials=requires_credentials,
            credential_type=credential_type,
            typical_speed=typical_speed,
            typical_quality=typical_quality,
            memory_usage=memory_usage,
            file_extensions=set(file_extensions or []),
            url_patterns=set(url_patterns or []),
            mime_types=set(mime_types or []),
            capabilities=set(capabilities or []),
        )

        # Register the source
        enhanced_registry.register(
            name=name,
            source_class=source_class,
            category=category,
            description=description,
            capabilities=source_capabilities,
            is_bulk_loader=is_bulk_loader,
            supports_recursive=supports_recursive,
            supports_filtering=supports_filtering,
            max_concurrent=max_concurrent,
            rate_limit_delay=rate_limit_delay,
            loaders=loaders,
            default_loader=default_loader,
            file_extensions=file_extensions,
            url_patterns=url_patterns,
            schemes=schemes,
            mime_types=mime_types,
            priority=priority,
            author=author,
            version=version,
            dependencies=dependencies,
            requires_credentials=requires_credentials,
            credential_type=credential_type,
        )

        return source_class

    return decorator


# =============================================================================
# Convenience Decorators for Common Cases
# =============================================================================


def register_file_source(
    name: str,
    extensions: List[str],
    loaders: Dict[str, Union[str, Dict[str, Any]]],
    **kwargs,
) -> Callable[[Type[LocalFileSource]], Type[LocalFileSource]]:
    """Convenience decorator for file-based sources."""

    # Determine category from extensions
    doc_extensions = {".pdf", ".doc", ".docx", ".odt", ".rtf"}
    data_extensions = {".csv", ".json", ".xml", ".yaml", ".yml"}
    code_extensions = {".py", ".js", ".ts", ".java", ".cpp", ".c"}

    ext_set = set(ext.lower() for ext in extensions)
    if ext_set & doc_extensions:
        category = SourceCategory.FILE_DOCUMENT
    elif ext_set & data_extensions:
        category = SourceCategory.FILE_DATA
    elif ext_set & code_extensions:
        category = SourceCategory.FILE_CODE
    else:
        category = SourceCategory.FILE_DOCUMENT  # default

    return register_source(
        name=name,
        category=category,
        file_extensions=extensions,
        loaders=loaders,
        **kwargs,
    )


def register_web_source(
    name: str,
    url_patterns: List[str],
    loaders: Dict[str, Union[str, Dict[str, Any]]],
    is_documentation: bool = False,
    **kwargs,
) -> Callable[[Type[RemoteSource]], Type[RemoteSource]]:
    """Convenience decorator for web-based sources."""

    category = (
        SourceCategory.WEB_DOCUMENTATION
        if is_documentation
        else SourceCategory.WEB_SCRAPING
    )

    return register_source(
        name=name,
        category=category,
        url_patterns=url_patterns,
        schemes=["http", "https"],
        loaders=loaders,
        requires_credentials=True,
        credential_type=CredentialType.API_KEY,
        **kwargs,
    )


def register_bulk_source(
    name: str,
    category: SourceCategory,
    loaders: Dict[str, Union[str, Dict[str, Any]]],
    max_concurrent: int = 4,
    **kwargs,
) -> Callable[[Type[BaseSource]], Type[BaseSource]]:
    """Convenience decorator for bulk loading sources."""

    # Merge capabilities instead of overriding
    default_capabilities = [
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ]

    if "capabilities" in kwargs:
        # Merge with existing capabilities
        existing_capabilities = kwargs.pop("capabilities")
        merged_capabilities = list(set(default_capabilities + existing_capabilities))
        kwargs["capabilities"] = merged_capabilities
    else:
        kwargs["capabilities"] = default_capabilities

    return register_source(
        name=name,
        category=category,
        loaders=loaders,
        is_bulk_loader=True,
        supports_recursive=True,
        supports_filtering=True,
        max_concurrent=max_concurrent,
        **kwargs,
    )


def register_database_source(
    name: str,
    database_type: str,
    loaders: Dict[str, Union[str, Dict[str, Any]]],
    **kwargs,
) -> Callable[[Type[DatabaseSource]], Type[DatabaseSource]]:
    """Convenience decorator for database sources."""

    # Determine category
    sql_types = {"postgresql", "mysql", "sqlite", "mssql", "oracle"}
    nosql_types = {"mongodb", "cassandra", "couchbase", "redis"}

    if database_type.lower() in sql_types:
        category = SourceCategory.DATABASE_SQL
    elif database_type.lower() in nosql_types:
        category = SourceCategory.DATABASE_NOSQL
    else:
        category = SourceCategory.DATABASE_SQL  # default

    return register_source(
        name=name,
        category=category,
        schemes=[database_type],
        loaders=loaders,
        is_bulk_loader=True,
        requires_credentials=True,
        credential_type=CredentialType.CONNECTION_STRING,
        **kwargs,
    )
