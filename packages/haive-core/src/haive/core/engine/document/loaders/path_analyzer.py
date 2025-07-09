"""Path analysis for automatic source detection.

This module provides comprehensive path analysis to automatically detect
the type of document source from a path string. Critical for auto-loading.
"""

import mimetypes
import re
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, Field


class PathType(str, Enum):
    """Primary path type classification."""

    LOCAL_FILE = "local_file"
    LOCAL_DIRECTORY = "local_directory"
    URL_HTTP = "url_http"
    URL_HTTPS = "url_https"
    DATABASE_URI = "database_uri"
    CLOUD_STORAGE = "cloud_storage"
    UNKNOWN = "unknown"


class FileCategory(str, Enum):
    """High-level file category."""

    DOCUMENT = "document"
    DATA = "data"
    CODE = "code"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


class SourceInfo(BaseModel):
    """Comprehensive information about a detected document source.

    This Pydantic model contains the complete results of source detection and analysis,
    providing all information needed for optimal loader selection and configuration.
    Created by the PathAnalyzer during the source detection phase.

    Attributes:
        source_type (str): Specific source type identifier used for loader selection.
            Examples: 'pdf', 'web', 'csv', 'postgresql', 's3', 'sharepoint'.
            This maps directly to registered loader implementations.
        category (SourceCategory): High-level classification of the source type.
            Used for capability grouping and fallback logic. Categories include:
            FILE_DOCUMENT, WEB_SCRAPING, DATABASE_SQL, CLOUD_STORAGE, etc.
        confidence (float): Detection confidence score from 0.0 to 1.0.
            Higher values indicate more certain detection. Values below 0.5
            may trigger additional validation or fallback detection methods.
        metadata (Dict[str, Any]): Rich metadata collected during analysis.
            Contains source-specific information such as:
            - file_extension: File extension for local files
            - mime_type: Detected MIME type
            - estimated_size: Estimated content size
            - url_components: Parsed URL components for web sources
            - database_type: Database system type for database sources
        capabilities (Optional[List[LoaderCapability]]): List of supported
            capabilities for this source type. Used for loader filtering
            and feature availability checks. None if not determined.

    Examples:
        PDF file detection result::

            source_info = SourceInfo(
                source_type="pdf",
                category=SourceCategory.FILE_DOCUMENT,
                confidence=0.95,
                metadata={
                    "file_extension": ".pdf",
                    "mime_type": "application/pdf",
                    "estimated_size": 1024000
                },
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA_EXTRACTION
                ]
            )

        Web source detection result::

            source_info = SourceInfo(
                source_type="web",
                category=SourceCategory.WEB_SCRAPING,
                confidence=0.90,
                metadata={
                    "protocol": "https",
                    "domain": "docs.example.com",
                    "url_components": {"scheme": "https", "host": "docs.example.com"}
                },
                capabilities=[
                    LoaderCapability.WEB_SCRAPING,
                    LoaderCapability.BULK_LOADING
                ]
            )

    Usage:
        This class is primarily used internally by the AutoLoader system
        for source detection and loader selection. Users typically don't
        create SourceInfo instances directly but receive them in LoadingResult
        objects and through the detect_source() method.

    See Also:
        - PathAnalyzer: Creates SourceInfo instances
        - LoadingResult: Contains SourceInfo for completed operations
        - SourceCategory: Enumeration of source categories
        - LoaderCapability: Enumeration of loader capabilities
    """

    source_type: str = Field(
        description="Specific source type identifier used for loader selection"
    )
    category: "SourceCategory" = Field(
        description="High-level classification of the source type"
    )
    confidence: float = Field(
        ge=0.0, le=1.0, description="Detection confidence score from 0.0 to 1.0"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Rich metadata collected during analysis"
    )
    capabilities: Optional[List["LoaderCapability"]] = Field(
        default=None, description="List of supported capabilities for this source type"
    )

    class Config:
        arbitrary_types_allowed = True


class PathAnalysisResult(BaseModel):
    """Result of comprehensive path analysis."""

    original_path: str = Field(description="Original path that was analyzed")
    path_type: PathType = Field(description="Primary path type classification")

    # Local file info
    is_local: bool = Field(default=False, description="Whether this is a local path")
    is_file: bool = Field(default=False, description="Whether this is a file")
    is_directory: bool = Field(default=False, description="Whether this is a directory")
    file_exists: bool = Field(default=False, description="Whether the file exists")
    file_extension: Optional[str] = Field(
        default=None, description="File extension if applicable"
    )
    file_category: Optional[FileCategory] = Field(
        default=None, description="High-level file category"
    )
    mime_type: Optional[str] = Field(default=None, description="Detected MIME type")
    file_size: Optional[int] = Field(
        default=None, ge=0, description="File size in bytes"
    )

    # URL info
    is_remote: bool = Field(default=False, description="Whether this is a remote URL")
    url_components: Optional[Dict[str, Any]] = Field(
        default=None, description="Parsed URL components"
    )
    domain: Optional[str] = Field(default=None, description="Domain name for URLs")

    # Database info
    is_database: bool = Field(
        default=False, description="Whether this is a database URI"
    )
    database_type: Optional[str] = Field(default=None, description="Type of database")

    # Cloud storage info
    is_cloud: bool = Field(default=False, description="Whether this is cloud storage")
    cloud_provider: Optional[str] = Field(
        default=None, description="Cloud provider name"
    )
    bucket_name: Optional[str] = Field(default=None, description="Storage bucket name")
    object_key: Optional[str] = Field(
        default=None, description="Object key/path in storage"
    )

    # Confidence
    confidence: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Analysis confidence score"
    )

    class Config:
        arbitrary_types_allowed = True


class PathAnalyzer:
    """Analyzes paths to determine source type and characteristics."""

    # File extension to category mapping
    EXTENSION_CATEGORIES = {
        # Documents
        ".pdf": FileCategory.DOCUMENT,
        ".doc": FileCategory.DOCUMENT,
        ".docx": FileCategory.DOCUMENT,
        ".odt": FileCategory.DOCUMENT,
        ".rtf": FileCategory.DOCUMENT,
        ".tex": FileCategory.DOCUMENT,
        ".txt": FileCategory.DOCUMENT,
        ".md": FileCategory.DOCUMENT,
        ".markdown": FileCategory.DOCUMENT,
        ".rst": FileCategory.DOCUMENT,
        # Data
        ".csv": FileCategory.DATA,
        ".json": FileCategory.DATA,
        ".jsonl": FileCategory.DATA,
        ".xml": FileCategory.DATA,
        ".yaml": FileCategory.DATA,
        ".yml": FileCategory.DATA,
        ".toml": FileCategory.DATA,
        ".xls": FileCategory.DATA,
        ".xlsx": FileCategory.DATA,
        ".parquet": FileCategory.DATA,
        # Code
        ".py": FileCategory.CODE,
        ".js": FileCategory.CODE,
        ".ts": FileCategory.CODE,
        ".java": FileCategory.CODE,
        ".cpp": FileCategory.CODE,
        ".c": FileCategory.CODE,
        ".h": FileCategory.CODE,
        ".go": FileCategory.CODE,
        ".rs": FileCategory.CODE,
        ".rb": FileCategory.CODE,
        # Images
        ".jpg": FileCategory.IMAGE,
        ".jpeg": FileCategory.IMAGE,
        ".png": FileCategory.IMAGE,
        ".gif": FileCategory.IMAGE,
        ".bmp": FileCategory.IMAGE,
        ".svg": FileCategory.IMAGE,
        ".webp": FileCategory.IMAGE,
        # Archive
        ".zip": FileCategory.ARCHIVE,
        ".tar": FileCategory.ARCHIVE,
        ".gz": FileCategory.ARCHIVE,
        ".rar": FileCategory.ARCHIVE,
        ".7z": FileCategory.ARCHIVE,
    }

    # URL patterns for specific services
    SERVICE_PATTERNS = {
        "github.com": "github",
        "gitlab.com": "gitlab",
        "youtube.com": "youtube",
        "youtu.be": "youtube",
        "wikipedia.org": "wikipedia",
        "arxiv.org": "arxiv",
        "huggingface.co": "huggingface",
        "kaggle.com": "kaggle",
    }

    # Database URI patterns
    DATABASE_SCHEMES = {
        "postgresql": "postgresql",
        "postgres": "postgresql",
        "mysql": "mysql",
        "sqlite": "sqlite",
        "mongodb": "mongodb",
        "redis": "redis",
        "clickhouse": "clickhouse",
    }

    # Cloud storage patterns
    CLOUD_SCHEMES = {
        "s3": "aws",
        "gs": "gcp",
        "azure": "azure",
        "wasb": "azure",
        "wasbs": "azure",
    }

    @classmethod
    def analyze(cls, path: Union[str, Path]) -> PathAnalysisResult:
        """Perform comprehensive path analysis."""
        path_str = str(path)

        # Try URL analysis first
        if cls._looks_like_url(path_str):
            return cls._analyze_url(path_str)

        # Try database URI
        if cls._looks_like_database_uri(path_str):
            return cls._analyze_database_uri(path_str)

        # Try cloud storage
        if cls._looks_like_cloud_storage(path_str):
            return cls._analyze_cloud_storage(path_str)

        # Default to local path
        return cls._analyze_local_path(path_str)

    @classmethod
    def _looks_like_url(cls, path: str) -> bool:
        """Check if path looks like a URL."""
        return bool(re.match(r"^https?://", path, re.IGNORECASE))

    @classmethod
    def _looks_like_database_uri(cls, path: str) -> bool:
        """Check if path looks like a database URI."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in cls.DATABASE_SCHEMES
        except Exception:
            return False

    @classmethod
    def _looks_like_cloud_storage(cls, path: str) -> bool:
        """Check if path looks like cloud storage."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in cls.CLOUD_SCHEMES
        except Exception:
            return False

    @classmethod
    def _analyze_local_path(cls, path: str) -> PathAnalysisResult:
        """Analyze a local file system path."""
        path_obj = Path(path)

        result = PathAnalysisResult(
            original_path=path,
            path_type=PathType.LOCAL_FILE,
            is_local=True,
            confidence=0.9,
        )

        # Check if exists
        if path_obj.exists():
            result.file_exists = True

            if path_obj.is_file():
                result.is_file = True
                result.path_type = PathType.LOCAL_FILE

                # Get file info
                result.file_extension = path_obj.suffix.lower()
                result.file_size = path_obj.stat().st_size

                # Determine category
                result.file_category = cls.EXTENSION_CATEGORIES.get(
                    result.file_extension, FileCategory.UNKNOWN
                )

                # Get MIME type
                mime_type, _ = mimetypes.guess_type(path)
                result.mime_type = mime_type

            elif path_obj.is_dir():
                result.is_directory = True
                result.path_type = PathType.LOCAL_DIRECTORY
                result.confidence = 1.0
        else:
            # File doesn't exist, analyze based on extension
            if "." in path_obj.name:
                result.is_file = True
                result.file_extension = path_obj.suffix.lower()
                result.file_category = cls.EXTENSION_CATEGORIES.get(
                    result.file_extension, FileCategory.UNKNOWN
                )
                result.confidence = 0.7
            else:
                # Assume directory if no extension
                result.is_directory = True
                result.path_type = PathType.LOCAL_DIRECTORY
                result.confidence = 0.6

        return result

    @classmethod
    def _analyze_url(cls, url: str) -> PathAnalysisResult:
        """Analyze a URL."""
        parsed = urlparse(url)

        result = PathAnalysisResult(
            original_path=url,
            path_type=(
                PathType.URL_HTTPS if parsed.scheme == "https" else PathType.URL_HTTP
            ),
            is_remote=True,
            confidence=1.0,
        )

        # Extract URL components
        result.url_components = {
            "scheme": parsed.scheme,
            "netloc": parsed.netloc,
            "path": parsed.path,
            "params": parsed.params,
            "query": parse_qs(parsed.query),
            "fragment": parsed.fragment,
        }

        result.domain = parsed.netloc

        # Check for known services
        for pattern, service in cls.SERVICE_PATTERNS.items():
            if pattern in parsed.netloc:
                result.url_components["service"] = service
                break

        # Try to determine file type from URL path
        if parsed.path:
            path_obj = Path(parsed.path)
            if path_obj.suffix:
                result.file_extension = path_obj.suffix.lower()
                result.file_category = cls.EXTENSION_CATEGORIES.get(
                    result.file_extension, FileCategory.UNKNOWN
                )

        return result

    @classmethod
    def _analyze_database_uri(cls, uri: str) -> PathAnalysisResult:
        """Analyze a database URI."""
        parsed = urlparse(uri)

        result = PathAnalysisResult(
            original_path=uri,
            path_type=PathType.DATABASE_URI,
            is_database=True,
            confidence=1.0,
        )

        result.database_type = cls.DATABASE_SCHEMES.get(parsed.scheme, parsed.scheme)

        # Extract components
        result.url_components = {
            "scheme": parsed.scheme,
            "host": parsed.hostname,
            "port": parsed.port,
            "database": parsed.path.lstrip("/") if parsed.path else None,
            "username": parsed.username,
        }

        return result

    @classmethod
    def _analyze_cloud_storage(cls, uri: str) -> PathAnalysisResult:
        """Analyze a cloud storage URI."""
        parsed = urlparse(uri)

        result = PathAnalysisResult(
            original_path=uri,
            path_type=PathType.CLOUD_STORAGE,
            is_cloud=True,
            confidence=1.0,
        )

        result.cloud_provider = cls.CLOUD_SCHEMES.get(parsed.scheme, parsed.scheme)

        # Extract bucket and key
        if parsed.netloc:
            result.bucket_name = parsed.netloc

        if parsed.path:
            result.object_key = parsed.path.lstrip("/")

        return result


def analyze_path(path: Union[str, Path]) -> PathAnalysisResult:
    """Convenience function for path analysis."""
    return PathAnalyzer.analyze(path)


def convert_to_source_info(analysis: PathAnalysisResult) -> "SourceInfo":
    """Convert PathAnalysisResult to SourceInfo for compatibility.

    Args:
        analysis: PathAnalysisResult from path analysis

    Returns:
        SourceInfo object with detected information
    """
    # Import here to avoid circular imports
    from .sources.source_types import LoaderCapability, SourceCategory

    # Map PathType to SourceCategory
    category_mapping = {
        PathType.LOCAL_FILE: SourceCategory.FILE_DOCUMENT,
        PathType.LOCAL_DIRECTORY: SourceCategory.FILE_DOCUMENT,
        PathType.URL_HTTP: SourceCategory.WEB_SCRAPING,
        PathType.URL_HTTPS: SourceCategory.WEB_SCRAPING,
        PathType.DATABASE_URI: SourceCategory.DATABASE_SQL,
        PathType.CLOUD_STORAGE: SourceCategory.CLOUD_STORAGE,
        PathType.UNKNOWN: SourceCategory.UNKNOWN,
    }

    # Determine source type from file extension or path type
    source_type = "unknown"
    if analysis.file_extension:
        ext = analysis.file_extension.lower().lstrip(".")
        source_type = ext
    elif (
        analysis.path_type == PathType.URL_HTTP
        or analysis.path_type == PathType.URL_HTTPS
    ):
        source_type = "web"
    elif analysis.path_type == PathType.DATABASE_URI:
        source_type = getattr(analysis, "database_type", "database")
    elif analysis.path_type == PathType.CLOUD_STORAGE:
        source_type = getattr(analysis, "cloud_provider", "cloud")

    # Basic capabilities based on source type
    capabilities = []
    if source_type in ["pdf", "doc", "docx", "txt"]:
        capabilities.extend(
            [LoaderCapability.TEXT_EXTRACTION, LoaderCapability.METADATA_EXTRACTION]
        )
    elif source_type == "web":
        capabilities.extend(
            [LoaderCapability.WEB_SCRAPING, LoaderCapability.BULK_LOADING]
        )
    elif "database" in source_type:
        capabilities.extend([LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING])

    return SourceInfo(
        source_type=source_type,
        category=category_mapping.get(analysis.path_type, SourceCategory.UNKNOWN),
        confidence=analysis.confidence,
        metadata={
            "original_path": analysis.original_path,
            "path_type": analysis.path_type.value,
            "file_extension": analysis.file_extension,
            "estimated_size": getattr(analysis, "estimated_size", None),
            "mime_type": getattr(analysis, "mime_type", None),
        },
        capabilities=capabilities,
    )


# Add method to PathAnalyzer class to return SourceInfo directly
def analyze_path_to_source_info(path: Union[str, Path]) -> "SourceInfo":
    """Analyze path and return SourceInfo directly.

    Args:
        path: Path to analyze

    Returns:
        SourceInfo object with detected source information
    """
    analysis = PathAnalyzer.analyze(path)
    return convert_to_source_info(analysis)


# Monkey patch the PathAnalyzer to add analyze_path method
PathAnalyzer.analyze_path = classmethod(
    lambda cls, path: convert_to_source_info(cls.analyze(path))
)


__all__ = [
    "PathAnalyzer",
    "PathAnalysisResult",
    "SourceInfo",
    "PathType",
    "FileCategory",
    "analyze_path",
    "convert_to_source_info",
    "analyze_path_to_source_info",
]
