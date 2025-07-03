"""Path Analysis Integration for Document Loader Engine.

This module integrates the path analysis system with the document loader engine.
It provides functions for analyzing paths and creating appropriate source instances.
"""

import logging
import os
from pathlib import Path
from typing import Any

# Import path analysis - placeholder for now
# Import the actual path analysis when available
try:
    from path_analysis_implementation import (
        CloudProvider,
        DatabaseType,
        FileCategory,
        PathAnalysisResult,
        PathType,
        analyze_cloud_path,
        analyze_database_uri,
        analyze_path_comprehensive,
        analyze_url,
    )

    _HAS_PATH_ANALYSIS = True
except ImportError:
    _HAS_PATH_ANALYSIS = False

    # Define placeholder types
    class PathType:
        LOCAL_FILE = "local_file"
        LOCAL_DIRECTORY = "local_directory"
        URL_HTTP = "url_http"
        URL_HTTPS = "url_https"
        DATABASE_URI = "database_uri"
        CLOUD_STORAGE = "cloud_storage"
        UNKNOWN = "unknown"

    class FileCategory:
        DOCUMENT = "document"
        TEXT = "text"
        UNKNOWN_FILE = "unknown_file"

    class DatabaseType:
        POSTGRESQL = "postgresql"
        MYSQL = "mysql"
        SQLITE = "sqlite"
        UNKNOWN_DB = "unknown_db"

    class CloudProvider:
        AWS_S3 = "aws_s3"
        AZURE_BLOB = "azure_blob"
        GOOGLE_CLOUD = "google_cloud"
        UNKNOWN_CLOUD = "unknown_cloud"

    class PathAnalysisResult:
        """Placeholder PathAnalysisResult class."""

        def __init__(self, original_path: str):
            self.original_path = original_path
            self.path_type = PathType.UNKNOWN
            self.is_local = False
            self.is_remote = False
            self.is_file = False
            self.is_directory = False
            self.file_extension = None
            self.file_category = None
            self.database_type = None
            self.cloud_provider = None
            self.url_components = None

    def analyze_path_comprehensive(path: str) -> PathAnalysisResult:
        """Placeholder implementation."""
        result = PathAnalysisResult(path)

        # Basic detection based on path format
        if path.startswith(("http://", "https://")):
            result.path_type = (
                PathType.URL_HTTPS if path.startswith("https://") else PathType.URL_HTTP
            )
            result.is_remote = True
            result.url_components = {
                "hostname": path.split("/")[2],
                "scheme": path.split("://")[0],
            }
        elif path.startswith("s3://"):
            result.path_type = PathType.CLOUD_STORAGE
            result.is_remote = True
            result.cloud_provider = CloudProvider.AWS_S3
        elif path.startswith(("postgresql://", "mysql://", "sqlite://")):
            result.path_type = PathType.DATABASE_URI
            result.is_remote = True
            if path.startswith("postgresql://"):
                result.database_type = DatabaseType.POSTGRESQL
            elif path.startswith("mysql://"):
                result.database_type = DatabaseType.MYSQL
            else:
                result.database_type = DatabaseType.SQLITE
        # Try to determine if it's a local file or directory
        elif os.path.exists(path):
            if os.path.isfile(path):
                result.path_type = PathType.LOCAL_FILE
                result.is_local = True
                result.is_file = True
                result.file_extension = os.path.splitext(path)[1].lower()

                # Basic category detection
                if result.file_extension in [
                    ".pdf",
                    ".docx",
                    ".doc",
                    ".odt",
                    ".rtf",
                ]:
                    result.file_category = FileCategory.DOCUMENT
                elif result.file_extension in [
                    ".txt",
                    ".md",
                    ".rst",
                    ".csv",
                    ".json",
                    ".xml",
                    ".html",
                    ".htm",
                ]:
                    result.file_category = FileCategory.TEXT
                else:
                    result.file_category = FileCategory.UNKNOWN_FILE
            elif os.path.isdir(path):
                result.path_type = PathType.LOCAL_DIRECTORY
                result.is_local = True
                result.is_directory = True
        # Try to infer from path format
        elif "." in os.path.basename(path):
            result.path_type = PathType.LOCAL_FILE
            result.is_local = True
            result.is_file = True
            result.file_extension = os.path.splitext(path)[1].lower()
        else:
            result.path_type = PathType.LOCAL_DIRECTORY
            result.is_local = True
            result.is_directory = True

        return result

    def analyze_url(url: str) -> PathAnalysisResult:
        """Placeholder for URL analysis."""
        result = PathAnalysisResult(url)
        result.path_type = (
            PathType.URL_HTTPS if url.startswith("https://") else PathType.URL_HTTP
        )
        result.is_remote = True
        result.url_components = {
            "hostname": url.split("/")[2],
            "scheme": url.split("://")[0],
        }
        return result

    def analyze_database_uri(uri: str) -> PathAnalysisResult:
        """Placeholder for database URI analysis."""
        result = PathAnalysisResult(uri)
        result.path_type = PathType.DATABASE_URI
        result.is_remote = True

        if uri.startswith("postgresql://"):
            result.database_type = DatabaseType.POSTGRESQL
        elif uri.startswith("mysql://"):
            result.database_type = DatabaseType.MYSQL
        elif uri.startswith("sqlite://"):
            result.database_type = DatabaseType.SQLITE
        else:
            result.database_type = DatabaseType.UNKNOWN_DB

        return result

    def analyze_cloud_path(path: str) -> PathAnalysisResult:
        """Placeholder for cloud path analysis."""
        result = PathAnalysisResult(path)
        result.path_type = PathType.CLOUD_STORAGE
        result.is_remote = True

        if path.startswith("s3://"):
            result.cloud_provider = CloudProvider.AWS_S3
        elif path.startswith("gs://"):
            result.cloud_provider = CloudProvider.GOOGLE_CLOUD
        elif path.startswith("azure://"):
            result.cloud_provider = CloudProvider.AZURE_BLOB
        else:
            result.cloud_provider = CloudProvider.UNKNOWN_CLOUD

        return result


# Import source registry
from source_registry import registry

logger = logging.getLogger(__name__)


def analyze_source(source: str | Path | dict[str, Any]) -> PathAnalysisResult:
    """Analyze a source to determine its type and properties.

    Args:
        source: The source to analyze (path, URL, or dict with source information)

    Returns:
        PathAnalysisResult with analysis information
    """
    # Convert to string if Path
    if isinstance(source, Path):
        source = str(source)

    # Handle dictionary input
    if isinstance(source, dict):
        if "path" in source:
            source_str = str(source["path"])
        elif "url" in source:
            source_str = str(source["url"])
        elif "source" in source:
            source_str = str(source["source"])
        else:
            raise ValueError(f"Cannot extract source from dictionary: {source}")
    else:
        source_str = str(source)

    # Analyze the source
    try:
        return analyze_path_comprehensive(source_str)
    except Exception as e:
        logger.warning(f"Error analyzing path {source_str}: {e}")
        # Create basic result
        result = PathAnalysisResult(source_str)

        # Try to infer basic properties
        if source_str.startswith(("http://", "https://")):
            result.path_type = (
                PathType.URL_HTTPS
                if source_str.startswith("https://")
                else PathType.URL_HTTP
            )
            result.is_remote = True
        elif os.path.exists(source_str):
            if os.path.isfile(source_str):
                result.path_type = PathType.LOCAL_FILE
                result.is_local = True
                result.is_file = True
                result.file_extension = os.path.splitext(source_str)[1].lower()
            elif os.path.isdir(source_str):
                result.path_type = PathType.LOCAL_DIRECTORY
                result.is_local = True
                result.is_directory = True

        return result


def analyze_and_resolve_source(
    source: str | Path | dict[str, Any], source_type: str | None = None
) -> tuple[Any, PathAnalysisResult]:
    """Analyze a source and resolve it to a source instance.

    Args:
        source: The source to analyze
        source_type: Optional explicit source type

    Returns:
        Tuple of (source_instance, analysis_result)

    Raises:
        ValueError: If source cannot be resolved
    """
    # Analyze the source
    analysis = analyze_source(source)

    # If explicit source type is provided, use it
    if source_type:
        source_instance = registry.create_source(source_type, analysis)
        if not source_instance:
            raise ValueError(f"Failed to create source instance for {source_type}")
        return source_instance, analysis

    # Find matching source types
    matches = registry.find_matching_sources(analysis)
    if not matches:
        raise ValueError(f"No matching source type found for {source}")

    # Use the best match
    best_source_type, confidence = matches[0]
    source_instance = registry.create_source(best_source_type, analysis)

    if not source_instance:
        raise ValueError(f"Failed to create source instance for {best_source_type}")

    return source_instance, analysis


def detect_source_from_path(path: str | Path) -> str | None:
    """Detect the most appropriate source type for a path.

    Args:
        path: The path to analyze

    Returns:
        Source type name, or None if no match found
    """
    try:
        # Analyze the path
        analysis = analyze_source(path)

        # Find matching source types
        matches = registry.find_matching_sources(analysis)
        if matches:
            best_source_type, _ = matches[0]
            return best_source_type
    except Exception as e:
        logger.warning(f"Error detecting source type for {path}: {e}")

    return None


def get_best_source_for_file_extension(extension: str) -> str | None:
    """Get the best source type for a file extension.

    Args:
        extension: The file extension (with or without leading dot)

    Returns:
        Source type name, or None if no match found
    """
    if not extension.startswith("."):
        extension = f".{extension}"

    source_types = registry.get_source_types_for_extension(extension)
    return source_types[0] if source_types else None


def get_best_source_for_domain(domain: str) -> str | None:
    """Get the best source type for a domain.

    Args:
        domain: The domain name

    Returns:
        Source type name, or None if no match found
    """
    source_types = registry.get_source_types_for_domain(domain)
    return source_types[0] if source_types else None


# Export all components
__all__ = [
    "CloudProvider",
    "DatabaseType",
    "FileCategory",
    "PathAnalysisResult",
    "PathType",
    "analyze_and_resolve_source",
    "analyze_source",
    "detect_source_from_path",
    "get_best_source_for_domain",
    "get_best_source_for_file_extension",
]
