"""Factory Methods for Document Loader Engine.

This module provides factory methods for creating document loader engines
for common use cases.
"""

import logging
from pathlib import Path
from typing import Any

# Import engine and config
from engine import DocumentLoaderEngine
from engine_config import DocumentLoaderConfig, EngineType
from loader_strategy import loader_registry
# Import from path integration
from path_integration import analyze_source
# Import from source to loader mapping
from source_loader_mapping import (get_best_loader_for_path,
                                   initialize_registries)
# Import source and loader registry
from source_registry import registry as source_registry

logger = logging.getLogger(__name__)


def create_document_loader_engine(
    config: dict[str, Any] | DocumentLoaderConfig | None = None,
) -> DocumentLoaderEngine:
    """Create a document loader engine with the given configuration.

    Args:
        config: Optional configuration for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Prepare config
    if config is None:
        engine_config = DocumentLoaderConfig()
    elif isinstance(config, dict):
        engine_config = DocumentLoaderConfig(**config)
    else:
        engine_config = config

    # Create engine
    return DocumentLoaderEngine(config=engine_config)


def create_file_loader_engine(
    file_path: str | Path | None = None,
    file_extension: str | None = None,
    loader_name: str | None = None,
    loader_preference: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for loading files.

    Args:
        file_path: Optional path to a file
        file_extension: Optional file extension to use for loader selection
        loader_name: Optional explicit loader name
        loader_preference: Optional preference ('speed', 'quality', or 'balanced')
        **options: Additional options for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Prepare config
    config = DocumentLoaderConfig(
        engine_type=EngineType.DOCUMENT_LOADER,
        loader_name=loader_name,
        loader_preference=loader_preference,
        loader_options=options,
    )

    # Create engine
    engine = DocumentLoaderEngine(config=config)

    # If file path is provided, analyze it to find the best loader
    if file_path:
        path_str = str(file_path)
        analyze_source(path_str)

        # Try to determine the best loader
        if not loader_name:
            strategy = get_best_loader_for_path(path_str, loader_preference)
            if strategy:
                config.loader_name = strategy.strategy_name

    # If file extension is provided but not the path
    elif file_extension and not file_path:
        if not file_extension.startswith("."):
            file_extension = f".{file_extension}"

        # Find best source type for extension
        source_types = source_registry.get_source_types_for_extension(file_extension)
        if source_types:
            # Set source type in config
            config.source_type = source_types[0]

            # Find best loader for this extension
            strategies = loader_registry.get_strategies_for_extension(file_extension)
            if strategies:
                for strategy in strategies:
                    if (
                        not loader_preference
                        or (loader_preference == "speed" and strategy.speed == "fast")
                        or (
                            loader_preference == "quality"
                            and strategy.quality == "high"
                        )
                    ):
                        config.loader_name = strategy.strategy_name
                        break
                else:
                    # Default to first strategy
                    config.loader_name = strategies[0].strategy_name

    return engine


def create_web_loader_engine(
    url: str | None = None,
    domain: str | None = None,
    dynamic_loading: bool = False,
    recursive: bool = False,
    max_depth: int = 1,
    loader_name: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for loading web content.

    Args:
        url: Optional URL to load
        domain: Optional domain name for loader selection
        dynamic_loading: Whether to use a dynamic loader (Playwright/Selenium)
        recursive: Whether to load recursively
        max_depth: Maximum recursion depth for recursive loading
        loader_name: Optional explicit loader name
        **options: Additional options for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Choose loader based on options
    if not loader_name:
        if dynamic_loading:
            loader_name = "playwright_loader"
        elif recursive:
            loader_name = "recursive_url_loader"
        else:
            loader_name = "web_base_loader"

    # Prepare loader options
    loader_options = options.copy()
    if recursive:
        loader_options["max_depth"] = max_depth

    # Prepare config
    config = DocumentLoaderConfig(
        engine_type=EngineType.DOCUMENT_LOADER,
        loader_name=loader_name,
        loader_options=loader_options,
    )

    # Create engine
    engine = DocumentLoaderEngine(config=config)

    # If URL is provided, analyze it
    if url:
        analysis = analyze_source(url)

        # If domain is in the URL, try to find domain-specific loader
        if (
            not domain
            and hasattr(analysis, "url_components")
            and analysis.url_components
        ):
            domain = analysis.url_components.get("hostname")

    # If domain is provided, find best source type
    if domain and not loader_name:
        source_types = source_registry.get_source_types_for_domain(domain)
        if source_types:
            config.source_type = source_types[0]

            # Find best loader for this domain
            strategies = loader_registry.get_strategies_for_source(config.source_type)
            if strategies:
                config.loader_name = strategies[0].strategy_name

    return engine


def create_directory_loader_engine(
    directory_path: str | Path | None = None,
    recursive: bool = True,
    glob_pattern: str | None = None,
    include_extensions: list[str] | None = None,
    exclude_extensions: list[str] | None = None,
    loader_name: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for loading directories.

    Args:
        directory_path: Optional path to a directory
        recursive: Whether to load recursively
        glob_pattern: Optional glob pattern for filtering files
        include_extensions: Optional list of file extensions to include
        exclude_extensions: Optional list of file extensions to exclude
        loader_name: Optional explicit loader name
        **options: Additional options for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Prepare loader options
    loader_options = options.copy()
    if glob_pattern:
        loader_options["glob"] = glob_pattern

    # Process include/exclude extensions
    include_patterns = []
    exclude_patterns = []

    if include_extensions:
        for ext in include_extensions:
            if not ext.startswith("."):
                ext = f".{ext}"
            include_patterns.append(f"**/*{ext}")

    if exclude_extensions:
        for ext in exclude_extensions:
            if not ext.startswith("."):
                ext = f".{ext}"
            exclude_patterns.append(f"**/*{ext}")

    # Prepare config
    config = DocumentLoaderConfig(
        engine_type=EngineType.DOCUMENT_LOADER,
        loader_name=loader_name or "directory_loader",
        recursive=recursive,
        loader_options=loader_options,
    )

    # Create engine
    engine = DocumentLoaderEngine(config=config)

    return engine


def create_database_loader_engine(
    connection_string: str | None = None,
    database_type: str | None = None,
    query: str | None = None,
    tables: list[str] | None = None,
    loader_name: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for loading from databases.

    Args:
        connection_string: Optional database connection string
        database_type: Optional database type (postgresql, mysql, sqlite, etc.)
        query: Optional SQL query to execute
        tables: Optional list of tables to load
        loader_name: Optional explicit loader name
        **options: Additional options for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Prepare loader options
    loader_options = options.copy()
    if query:
        loader_options["query"] = query
    if tables:
        loader_options["tables"] = tables

    # Determine database type from connection string if not provided
    if connection_string and not database_type:
        if connection_string.startswith("postgresql://"):
            database_type = "postgresql"
        elif connection_string.startswith("mysql://"):
            database_type = "mysql"
        elif connection_string.startswith("sqlite://") or connection_string.endswith(
            ".db"
        ):
            database_type = "sqlite"
        elif connection_string.startswith("mongodb://"):
            database_type = "mongodb"

    # Set loader name based on database type if not provided
    if not loader_name and database_type:
        loader_name = "sql_database_loader"
        if database_type == "mongodb":
            loader_name = "mongodb_loader"

    # Prepare config
    config = DocumentLoaderConfig(
        engine_type=EngineType.DOCUMENT_LOADER,
        loader_name=loader_name,
        loader_options=loader_options,
    )

    # If database type is provided, set source type
    if database_type:
        config.source_type = f"{database_type}_database"

    # Create engine
    engine = DocumentLoaderEngine(config=config)

    return engine


def create_cloud_loader_engine(
    bucket_uri: str | None = None,
    cloud_provider: str | None = None,
    bucket_name: str | None = None,
    object_key: str | None = None,
    loader_name: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine optimized for loading from cloud storage.

    Args:
        bucket_uri: Optional bucket URI (e.g., 's3://bucket/key')
        cloud_provider: Optional cloud provider (aws_s3, google_cloud, azure_blob, etc.)
        bucket_name: Optional bucket name
        object_key: Optional object key
        loader_name: Optional explicit loader name
        **options: Additional options for the engine

    Returns:
        DocumentLoaderEngine instance
    """
    # Initialize registries if needed
    if not source_registry.list_source_types():
        initialize_registries()

    # Prepare loader options
    loader_options = options.copy()

    # Parse bucket URI if provided
    if bucket_uri:
        if bucket_uri.startswith("s3://"):
            cloud_provider = "aws_s3"
            parts = bucket_uri[5:].split("/", 1)
            if parts:
                bucket_name = parts[0]
                if len(parts) > 1:
                    object_key = parts[1]
        elif bucket_uri.startswith("gs://"):
            cloud_provider = "google_cloud"
            parts = bucket_uri[5:].split("/", 1)
            if parts:
                bucket_name = parts[0]
                if len(parts) > 1:
                    object_key = parts[1]
        elif bucket_uri.startswith("azure://"):
            cloud_provider = "azure_blob"
            parts = bucket_uri[8:].split("/", 1)
            if parts:
                bucket_name = parts[0]
                if len(parts) > 1:
                    object_key = parts[1]

    # Add bucket and key to options
    if bucket_name:
        loader_options["bucket_name"] = bucket_name
    if object_key:
        loader_options["object_key"] = object_key

    # Set loader name based on cloud provider and whether it's a file or directory
    if not loader_name and cloud_provider:
        is_directory = False
        if object_key:
            is_directory = not object_key or object_key.endswith("/")

        if cloud_provider == "aws_s3":
            loader_name = "s3_directory_loader" if is_directory else "s3_file_loader"
        elif cloud_provider == "google_cloud":
            loader_name = "gcs_directory_loader" if is_directory else "gcs_file_loader"
        elif cloud_provider == "azure_blob":
            loader_name = (
                "azure_container_loader" if is_directory else "azure_blob_loader"
            )

    # Prepare config
    config = DocumentLoaderConfig(
        engine_type=EngineType.DOCUMENT_LOADER,
        loader_name=loader_name,
        loader_options=loader_options,
    )

    # If cloud provider is provided, set source type
    if cloud_provider:
        config.source_type = f"{cloud_provider}_source"

    # Create engine
    engine = DocumentLoaderEngine(config=config)

    return engine


# Export all components
__all__ = [
    "create_cloud_loader_engine",
    "create_database_loader_engine",
    "create_directory_loader_engine",
    "create_document_loader_engine",
    "create_file_loader_engine",
    "create_web_loader_engine",
]
