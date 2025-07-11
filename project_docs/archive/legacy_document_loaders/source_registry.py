"""Source Type Registry for Document Loader Engine.

This module implements the source type registry for the document loader engine.
It provides a centralized registry for managing document source types and their mappings.
"""

import inspect
import logging
import threading

# For now, using these placeholder imports
from source_implementation import (BaseSource, CloudSource, DatabaseSource,
                                   LoaderStrategy, LocalSource,
                                   PathAnalysisResult, RemoteSource,
                                   SourceMetadata, SourcePattern)

# Import from path analysis module - will use when it's available


logger = logging.getLogger(__name__)


class SourceTypeRegistry:
    """Registry for document source types.

    This registry maintains a mapping of source types to their metadata,
    and provides methods for finding the appropriate source type for a given input.
    """

    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        """Initialize the registry."""
        # Core mappings
        self.source_classes: dict[str, type[BaseSource]] = {}
        self.source_metadata: dict[str, SourceMetadata] = {}

        # Index mappings for faster lookups
        self.file_extension_index: dict[str, list[str]] = {}  # ext -> source_types
        self.domain_index: dict[str, list[str]] = {}  # domain -> source_types
        self.mime_type_index: dict[str, list[str]] = {}  # mime_type -> source_types
        self.scheme_index: dict[str, list[str]] = {}  # scheme -> source_types

        # Auto-registration flag to avoid circular imports
        self._auto_register_completed = False

    @classmethod
    def get_instance(cls) -> "SourceTypeRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def reset(self):
        """Reset the registry (primarily for testing)."""
        self.source_classes = {}
        self.source_metadata = {}
        self.file_extension_index = {}
        self.domain_index = {}
        self.mime_type_index = {}
        self.scheme_index = {}
        self._auto_register_completed = False

    def register(self, source_class: type[BaseSource], **kwargs) -> SourceMetadata:
        """Register a source type with the registry.

        Args:
            source_class: The source class to register
            **kwargs: Additional registration options

        Returns:
            SourceMetadata: The metadata for the registered source
        """
        # Generate source type name if not provided
        source_type = kwargs.get("source_type")
        if not source_type:
            source_type = self._generate_source_type(source_class.__name__)

        # Check if already registered
        if source_type in self.source_classes:
            logger.warning(
                f"Source type '{source_type}' already registered, overriding"
            )

        # Extract patterns - either from kwargs or from class
        patterns = kwargs.get("patterns", [])
        if not patterns:
            patterns = self._extract_patterns_from_class(source_class)

        # Extract loader strategies - either from kwargs or from class
        loader_strategies = kwargs.get("loader_strategies", [])
        if not loader_strategies:
            loader_strategies = self._extract_strategies_from_class(source_class)

        # Determine category from inheritance
        category = self._determine_category(source_class)

        # Create metadata
        metadata = SourceMetadata(
            source_type=source_type,
            source_class=f"{source_class.__module__}.{source_class.__name__}",
            category=category,
            patterns=patterns,
            loader_strategies=loader_strategies,
            description=kwargs.get("description", source_class.__doc__ or ""),
            auto_detected=kwargs.get("auto_detected", True),
        )

        # Store in registry
        self.source_classes[source_type] = source_class
        self.source_metadata[source_type] = metadata

        # Update indices
        self._update_indices(source_type, metadata)

        logger.debug(
            f"Registered source: {source_type} with {len(patterns)} patterns and {len(loader_strategies)} loaders"
        )

        return metadata

    def find_matching_sources(
        self, analysis: PathAnalysisResult
    ) -> list[tuple[str, float]]:
        """Find source types that match the analysis with confidence scores.

        Args:
            analysis: The path analysis result

        Returns:
            List of (source_type, confidence_score) tuples, sorted by confidence
        """
        matches = []

        for source_type, metadata in self.source_metadata.items():
            score = self._calculate_match_score(analysis, metadata)
            if score > 0.1:  # Minimum threshold
                matches.append((source_type, score))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def create_source(
        self, source_type: str, analysis: PathAnalysisResult
    ) -> BaseSource | None:
        """Create an instance of the specified source type.

        Args:
            source_type: The source type to create
            analysis: The path analysis result

        Returns:
            An instance of the source, or None if creation fails
        """
        if source_type not in self.source_classes:
            logger.error(f"Source type '{source_type}' not found in registry")
            return None

        source_class = self.source_classes[source_type]

        try:
            # Create instance with appropriate fields based on category
            if issubclass(source_class, LocalSource):
                if getattr(analysis, "is_file", False):
                    return source_class(file_path=analysis.original_path)
                if getattr(analysis, "is_directory", False):
                    return source_class(directory_path=analysis.original_path)
                return source_class(file_path=analysis.original_path)

            if issubclass(source_class, RemoteSource):
                return source_class(url=analysis.original_path)

            if issubclass(source_class, DatabaseSource):
                return source_class(connection_string=analysis.original_path)

            if issubclass(source_class, CloudSource):
                return source_class(
                    bucket_name=getattr(analysis, "bucket_name", None),
                    object_key=getattr(analysis, "object_key", None),
                )

            # Fallback for unknown source types
            return source_class()

        except Exception as e:
            logger.exception(f"Error creating source instance for {source_type}: {e}")
            return None

    def get_source_type(self, source_type: str) -> SourceMetadata | None:
        """Get metadata for a specific source type.

        Args:
            source_type: The source type to retrieve

        Returns:
            The source metadata, or None if not found
        """
        return self.source_metadata.get(source_type)

    def list_source_types(self) -> list[str]:
        """List all registered source types.

        Returns:
            List of registered source type names
        """
        return list(self.source_metadata.keys())

    def get_source_types_for_extension(self, extension: str) -> list[str]:
        """Get source types that can handle a specific file extension.

        Args:
            extension: The file extension (with or without leading dot)

        Returns:
            List of source type names
        """
        if not extension.startswith("."):
            extension = f".{extension}"

        return self.file_extension_index.get(extension, [])

    def get_source_types_for_domain(self, domain: str) -> list[str]:
        """Get source types that can handle a specific domain.

        Args:
            domain: The domain name

        Returns:
            List of source type names
        """
        # Check for direct match
        source_types = self.domain_index.get(domain, [])

        # Check for wildcard matches
        for indexed_domain, domain_source_types in self.domain_index.items():
            if "*" in indexed_domain:
                import fnmatch

                if fnmatch.fnmatch(domain, indexed_domain):
                    source_types.extend(domain_source_types)

        return list(set(source_types))  # Deduplicate

    def _generate_source_type(self, class_name: str) -> str:
        """Generate a source type name from a class name.

        Args:
            class_name: The class name

        Returns:
            The generated source type name
        """
        import re

        # Convert CamelCase to snake_case
        result = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

        # Remove common suffixes
        result = result.replace("_source", "").replace("_loader", "")

        return result

    def _extract_patterns_from_class(
        self, source_class: type[BaseSource]
    ) -> list[SourcePattern]:
        """Extract patterns from a source class.

        Args:
            source_class: The source class

        Returns:
            List of extracted patterns
        """
        patterns = []

        # Check for get_patterns class method
        if hasattr(source_class, "get_patterns"):
            try:
                patterns.extend(source_class.get_patterns())
            except Exception as e:
                logger.warning(
                    f"Error extracting patterns from {source_class.__name__}: {e}"
                )

        # Check for Config class with pattern attributes
        if hasattr(source_class, "Config"):
            config = source_class.Config

            # Direct patterns list
            if hasattr(config, "patterns"):
                patterns.extend(getattr(config, "patterns", []))

            # Individual pattern attributes
            pattern_data = {}
            for attr in [
                "file_extensions",
                "url_patterns",
                "domain_patterns",
                "path_patterns",
                "content_types",
                "file_categories",
            ]:
                if hasattr(config, attr):
                    value = getattr(config, attr, None)
                    if value:
                        pattern_data[attr] = value

            if pattern_data:
                patterns.append(SourcePattern(**pattern_data))

        # Infer from class name
        patterns.extend(self._infer_patterns_from_name(source_class.__name__))

        # Infer from docstring
        if source_class.__doc__:
            patterns.extend(self._infer_patterns_from_docstring(source_class.__doc__))

        return patterns

    def _extract_strategies_from_class(
        self, source_class: type[BaseSource]
    ) -> list[LoaderStrategy]:
        """Extract loader strategies from a source class.

        Args:
            source_class: The source class

        Returns:
            List of extracted loader strategies
        """
        strategies = []

        # Check for get_loader_strategies class method
        if hasattr(source_class, "get_loader_strategies"):
            try:
                strategies.extend(source_class.get_loader_strategies())
            except Exception as e:
                logger.warning(
                    f"Error extracting loader strategies from {source_class.__name__}: {e}"
                )

        # Check for Config class with loader_strategies attribute
        if hasattr(source_class, "Config") and hasattr(
            source_class.Config, "loader_strategies"
        ):
            loader_strategies = source_class.Config.loader_strategies

            if isinstance(loader_strategies, dict):
                for name, config in loader_strategies.items():
                    if isinstance(config, str):
                        # Simple string format
                        strategies.append(
                            LoaderStrategy(strategy_name=name, loader_class=config)
                        )
                    elif isinstance(config, dict):
                        # Detailed config
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=name,
                                loader_class=config.get("class", ""),
                                speed=config.get("speed", "medium"),
                                quality=config.get("quality", "medium"),
                                best_for=config.get("best_for", []),
                                **{
                                    k: v
                                    for k, v in config.items()
                                    if k
                                    not in ["class", "speed", "quality", "best_for"]
                                },
                            )
                        )

        return strategies

    def _determine_category(self, source_class: type[BaseSource]) -> str:
        """Determine the category of a source class based on inheritance.

        Args:
            source_class: The source class

        Returns:
            The category as a string ('local', 'remote', 'database', 'cloud', or 'special')
        """
        mro_names = [c.__name__ for c in source_class.__mro__]

        if "CloudSource" in mro_names:
            return "cloud"
        if "DatabaseSource" in mro_names:
            return "database"
        if "LocalSource" in mro_names:
            return "local"
        if "RemoteSource" in mro_names:
            return "remote"

        return "special"

    def _update_indices(self, source_type: str, metadata: SourceMetadata) -> None:
        """Update lookup indices for fast source type resolution.

        Args:
            source_type: The source type name
            metadata: The source metadata
        """
        # Process each pattern
        for pattern in metadata.patterns:
            # File extension index
            for ext in pattern.file_extensions:
                if ext not in self.file_extension_index:
                    self.file_extension_index[ext] = []
                if source_type not in self.file_extension_index[ext]:
                    self.file_extension_index[ext].append(source_type)

            # Domain index
            for domain in pattern.domain_patterns:
                if domain not in self.domain_index:
                    self.domain_index[domain] = []
                if source_type not in self.domain_index[domain]:
                    self.domain_index[domain].append(source_type)

            # MIME type index
            for content_type in pattern.content_types:
                if content_type not in self.mime_type_index:
                    self.mime_type_index[content_type] = []
                if source_type not in self.mime_type_index[content_type]:
                    self.mime_type_index[content_type].append(source_type)

            # Scheme index
            for scheme in pattern.scheme_patterns:
                if scheme not in self.scheme_index:
                    self.scheme_index[scheme] = []
                if source_type not in self.scheme_index[scheme]:
                    self.scheme_index[scheme].append(source_type)

    def _calculate_match_score(
        self, analysis: PathAnalysisResult, metadata: SourceMetadata
    ) -> float:
        """Calculate how well a source matches the analysis result.

        Args:
            analysis: The path analysis result
            metadata: The source metadata

        Returns:
            A confidence score between 0.0 and 1.0
        """
        score = 0.0
        total_patterns = len(metadata.patterns)

        if total_patterns == 0:
            return 0.0

        for pattern in metadata.patterns:
            pattern_score = self._score_pattern_match(analysis, pattern)
            score += pattern_score

        # Normalize by number of patterns
        score = score / total_patterns

        # Boost for explicit high-priority patterns
        high_priority_patterns = [
            p for p in metadata.patterns if getattr(p, "priority", 0) > 5
        ]
        if high_priority_patterns:
            score += 0.2

        return min(1.0, score)

    def _score_pattern_match(
        self, analysis: PathAnalysisResult, pattern: SourcePattern
    ) -> float:
        """Score how well a pattern matches the analysis result.

        Args:
            analysis: The path analysis result
            pattern: The source pattern

        Returns:
            A score between 0.0 and 1.0
        """
        score = 0.0
        total_checks = 0

        # File extension matching
        if pattern.file_extensions and getattr(analysis, "file_extension", None):
            total_checks += 1
            if analysis.file_extension in pattern.file_extensions:
                score += 1.0

        # Domain matching
        url_components = getattr(analysis, "url_components", None)
        if pattern.domain_patterns and url_components:
            total_checks += 1
            hostname = url_components.get("hostname", "")
            for domain in pattern.domain_patterns:
                if domain in hostname:
                    score += 1.0
                    break

        # Scheme matching
        if pattern.scheme_patterns and url_components:
            total_checks += 1
            scheme = url_components.get("scheme", "")
            if scheme in pattern.scheme_patterns:
                score += 1.0

        # Database type matching
        if pattern.database_types and getattr(analysis, "database_type", None):
            total_checks += 1
            if analysis.database_type in pattern.database_types:
                score += 1.0

        # Cloud provider matching
        if pattern.cloud_providers and getattr(analysis, "cloud_provider", None):
            total_checks += 1
            if analysis.cloud_provider in pattern.cloud_providers:
                score += 1.0

        # File category matching
        if pattern.file_categories and getattr(analysis, "file_category", None):
            total_checks += 1
            if analysis.file_category in pattern.file_categories:
                score += 0.5  # Lower weight for category

        # Custom matcher
        if getattr(pattern, "custom_matcher", None):
            total_checks += 1
            try:
                if pattern.custom_matcher(analysis):
                    score += 1.0
            except Exception as e:
                logger.warning(f"Custom matcher failed: {e}")

        # Normalize score
        score = score / total_checks if total_checks > 0 else 0.0

        # Apply priority boost
        priority = getattr(pattern, "priority", 0)
        if priority > 0:
            score += priority * 0.01

        return min(1.0, score)

    def _infer_patterns_from_name(self, class_name: str) -> list[SourcePattern]:
        """Infer patterns from a class name.

        Args:
            class_name: The class name

        Returns:
            List of inferred patterns
        """
        patterns = []
        name_lower = class_name.lower()

        # Service name mapping
        name_to_domain = {
            "github": ["github.com"],
            "gitlab": ["gitlab.com"],
            "bitbucket": ["bitbucket.org"],
            "youtube": ["youtube.com", "youtu.be"],
            "arxiv": ["arxiv.org"],
            "wikipedia": ["wikipedia.org"],
            "google": ["google.com", "docs.google.com", "drive.google.com"],
            "dropbox": ["dropbox.com"],
            "notion": ["notion.so"],
            "jira": ["atlassian.net"],
            "confluence": ["confluence.com"],
            "s3": ["s3.amazonaws.com"],
            "azure": ["azure.com", "blob.core.windows.net"],
            "gcs": ["storage.googleapis.com"],
        }

        # Check for known services
        for service, domains in name_to_domain.items():
            if service in name_lower:
                patterns.append(SourcePattern(domain_patterns=domains, priority=10))
                break

        # Extract file extensions from name
        file_extension_map = {
            "pdf": [".pdf"],
            "csv": [".csv"],
            "json": [".json"],
            "xml": [".xml"],
            "markdown": [".md", ".markdown"],
            "md": [".md", ".markdown"],
            "text": [".txt", ".text"],
            "txt": [".txt", ".text"],
            "html": [".html", ".htm"],
            "htm": [".html", ".htm"],
            "docx": [".docx", ".doc"],
            "doc": [".docx", ".doc"],
            "word": [".docx", ".doc"],
            "excel": [".xlsx", ".xls"],
            "xlsx": [".xlsx"],
            "xls": [".xls"],
            "ppt": [".pptx", ".ppt"],
            "powerpoint": [".pptx", ".ppt"],
            "zip": [".zip"],
            "tar": [".tar", ".tar.gz", ".tgz"],
            "yaml": [".yaml", ".yml"],
            "yml": [".yaml", ".yml"],
            "python": [".py"],
            "py": [".py"],
            "javascript": [".js"],
            "js": [".js"],
            "typescript": [".ts"],
            "ts": [".ts"],
            "notebook": [".ipynb"],
            "ipynb": [".ipynb"],
        }

        for key, extensions in file_extension_map.items():
            if key in name_lower:
                patterns.append(SourcePattern(file_extensions=extensions))

        return patterns

    def _infer_patterns_from_docstring(self, docstring: str) -> list[SourcePattern]:
        """Infer patterns from a docstring.

        Args:
            docstring: The docstring

        Returns:
            List of inferred patterns
        """
        patterns = []
        if not docstring:
            return patterns

        doc_lower = docstring.lower()

        # Service name mapping
        name_to_domain = {
            "github": ["github.com"],
            "gitlab": ["gitlab.com"],
            "bitbucket": ["bitbucket.org"],
            "youtube": ["youtube.com", "youtu.be"],
            "arxiv": ["arxiv.org"],
            "wikipedia": ["wikipedia.org"],
            "google": ["google.com", "docs.google.com", "drive.google.com"],
            "dropbox": ["dropbox.com"],
            "notion": ["notion.so"],
        }

        # Look for domain mentions
        for service, domains in name_to_domain.items():
            if service in doc_lower:
                patterns.append(SourcePattern(domain_patterns=domains))

        # Look for file extensions
        extensions = [".pdf", ".csv", ".json", ".txt", ".html", ".docx", ".xlsx", ".md"]
        for ext in extensions:
            if ext in doc_lower:
                patterns.append(SourcePattern(file_extensions=[ext]))

        return patterns


# Singleton instance
registry = SourceTypeRegistry.get_instance()


def auto_source(
    source_type: str | None = None,
    patterns: list[SourcePattern] | None = None,
    loaders: list[str] | None = None,
    **pattern_kwargs,
):
    """Auto-registration decorator for source classes.

    This decorator automatically registers a source class with the registry.
    It can be used with or without arguments.

    Usage:
        @auto_source
        class MySource(LocalSource):
            pass

        @auto_source(domain_patterns=["example.com"])
        class APISource(RemoteSource):
            pass

    Args:
        source_type: Optional explicit source type name
        patterns: Optional list of source patterns
        loaders: Optional list of preferred loader names
        **pattern_kwargs: Additional pattern attributes

    Returns:
        Decorated class
    """

    def decorator(cls):
        # Create a new Config class if needed
        if not hasattr(cls, "Config"):
            cls.Config = type("Config", (), {})

        # Add explicit patterns if provided
        if patterns:
            cls.Config.patterns = patterns

        if loaders:
            cls.Config.preferred_loaders = loaders

        # Add pattern kwargs as Config attributes
        for key, value in pattern_kwargs.items():
            setattr(cls.Config, key, value)

        # Register with the global registry
        metadata = registry.register(cls, source_type=source_type)

        # Add metadata to class
        cls.source_metadata = metadata

        return cls

    # Handle both @auto_source and @auto_source()
    if inspect.isclass(source_type) and issubclass(source_type, BaseSource):
        cls = source_type
        source_type = None
        return decorator(cls)

    return decorator


# Export all components
__all__ = ["SourceTypeRegistry", "auto_source", "registry"]
