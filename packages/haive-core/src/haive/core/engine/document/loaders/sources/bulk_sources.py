"""Bulk loading and directory sources with "scrape all" capabilities.

This module implements comprehensive bulk loading sources that can process
entire directories, repositories, and data sources with parallel processing
and filtering capabilities.
"""

from enum import Enum
from typing import Any, Dict, List, Optional, Set

from .enhanced_registry import enhanced_registry, register_bulk_source
from .source_types import (
    CloudStorageSource,
    CredentialType,
    DirectorySource,
    LoaderCapability,
    SourceCategory,
)


class BulkProcessingMode(str, Enum):
    """Modes for bulk processing operations."""

    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONCURRENT = "concurrent"
    STREAMING = "streaming"


class FilterStrategy(str, Enum):
    """Strategies for filtering files during bulk processing."""

    EXTENSION = "extension"
    SIZE = "size"
    DATE = "date"
    PATTERN = "pattern"
    CONTENT = "content"
    COMBINED = "combined"


# =============================================================================
# Advanced Directory Sources (Scrape All)
# =============================================================================


@register_bulk_source(
    name="recursive_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "concurrent": {
            "class": "ConcurrentLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "directory": {
            "class": "DirectoryLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
    },
    default_loader="concurrent",
    description="High-performance recursive directory loader with concurrent processing",
    max_concurrent=8,
    priority=10,
)
class RecursiveDirectorySource(DirectorySource):
    """Advanced recursive directory source with concurrent processing."""

    # Processing configuration
    processing_mode: BulkProcessingMode = BulkProcessingMode.CONCURRENT
    max_workers: int = 8
    batch_size: int = 20

    # Filtering options
    file_extensions: Set[str] = set()
    exclude_patterns: List[str] = []
    include_patterns: List[str] = []
    min_file_size: int = 0
    max_file_size: Optional[int] = None

    # Advanced options
    follow_symlinks: bool = False
    ignore_hidden: bool = True
    fail_fast: bool = False
    progress_callback: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Build file filter
        if self.file_extensions:
            kwargs["glob"] = "**/*{" + ",".join(self.file_extensions) + "}"

        kwargs.update(
            {
                "use_multithreading": self.processing_mode
                == BulkProcessingMode.CONCURRENT,
                "max_concurrency": self.max_workers,
                "show_progress": bool(self.progress_callback),
                "silent_errors": not self.fail_fast,
                "exclude": self.exclude_patterns,
                "include": self.include_patterns,
            }
        )

        return kwargs


@register_bulk_source(
    name="filtered_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "smart": {
            "class": "DirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="smart",
    description="Directory loader with advanced filtering and content analysis",
    max_concurrent=6,
    priority=8,
)
class FilteredDirectorySource(DirectorySource):
    """Directory source with advanced filtering capabilities."""

    # Filter configuration
    filter_strategy: FilterStrategy = FilterStrategy.COMBINED
    content_filters: List[str] = []  # Regex patterns for content
    date_range_start: Optional[str] = None
    date_range_end: Optional[str] = None

    # Size filters
    min_file_size_mb: float = 0.0
    max_file_size_mb: Optional[float] = None

    # Content analysis
    analyze_content: bool = False
    language_detection: bool = False
    duplicate_detection: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Add filtering logic
        loader_kwargs = {}
        if self.content_filters:
            loader_kwargs["content_filters"] = self.content_filters
        if self.analyze_content:
            loader_kwargs["analyze_content"] = True

        kwargs["loader_kwargs"] = loader_kwargs
        return kwargs


# =============================================================================
# Cloud Storage Bulk Sources
# =============================================================================


@register_bulk_source(
    name="s3_bucket",
    category=SourceCategory.DIRECTORY_CLOUD,
    loaders={
        "directory": {
            "class": "S3DirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["boto3"],
        }
    },
    default_loader="directory",
    description="AWS S3 bucket bulk loader with prefix filtering",
    max_concurrent=10,
    requires_credentials=True,
    credential_type=CredentialType.CLOUD_CREDENTIALS,
    priority=9,
)
class S3BucketSource(CloudStorageSource):
    """AWS S3 bucket source for bulk processing."""

    # S3 configuration
    prefix: str = ""
    suffix: str = ""
    aws_region: str = "us-east-1"

    # Processing options
    parallel_downloads: bool = True
    stream_large_files: bool = True
    max_objects: Optional[int] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "bucket": self.bucket_name,
                "prefix": self.prefix,
                "suffix": self.suffix,
                "aws_region": self.aws_region,
                "max_objects": self.max_objects,
            }
        )
        return kwargs


@register_bulk_source(
    name="gcs_bucket",
    category=SourceCategory.DIRECTORY_CLOUD,
    loaders={
        "directory": {
            "class": "GCSDirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-cloud-storage"],
        }
    },
    default_loader="directory",
    description="Google Cloud Storage bucket bulk loader",
    max_concurrent=8,
    requires_credentials=True,
    credential_type=CredentialType.CLOUD_CREDENTIALS,
    priority=9,
)
class GCSBucketSource(CloudStorageSource):
    """Google Cloud Storage bucket source."""

    prefix: str = ""
    project_id: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "bucket_name": self.bucket_name,
                "prefix": self.prefix,
                "project": self.project_id,
            }
        )
        return kwargs


@register_bulk_source(
    name="azure_container",
    category=SourceCategory.DIRECTORY_CLOUD,
    loaders={
        "container": {
            "class": "AzureBlobStorageContainerLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["azure-storage-blob"],
        }
    },
    default_loader="container",
    description="Azure Blob Storage container bulk loader",
    max_concurrent=8,
    requires_credentials=True,
    credential_type=CredentialType.CLOUD_CREDENTIALS,
    priority=9,
)
class AzureContainerSource(CloudStorageSource):
    """Azure Blob Storage container source."""

    container_name: str
    prefix: str = ""
    connection_string: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "container_name": self.container_name,
                "prefix": self.prefix,
                "conn_str": self.connection_string,
            }
        )
        return kwargs


# =============================================================================
# Specialized Bulk Processing Sources
# =============================================================================


@register_bulk_source(
    name="merged_data",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "merger": {
            "class": "MergedDataLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="merger",
    description="Multi-source data merger with deduplication",
    max_concurrent=4,
    priority=7,
)
class MergedDataSource(DirectorySource):
    """Multi-source data merger for combining different data sources."""

    # Data sources to merge
    source_paths: List[str] = []
    source_types: List[str] = []

    # Merging configuration
    deduplicate: bool = True
    merge_strategy: str = "append"  # append, interleave, priority
    conflict_resolution: str = "first"  # first, last, merge

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "sources": self.source_paths,
                "source_types": self.source_types,
                "deduplicate": self.deduplicate,
                "merge_strategy": self.merge_strategy,
            }
        )
        return kwargs


# =============================================================================
# File System Blob Sources (Advanced)
# =============================================================================


@register_bulk_source(
    name="filesystem_blob",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "blob": {
            "class": "FileSystemBlobLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="blob",
    description="File system blob loader with binary file support",
    max_concurrent=6,
    priority=8,
)
class FileSystemBlobSource(DirectorySource):
    """File system blob source for binary and mixed content."""

    # Blob configuration
    include_binary: bool = True
    encoding_detection: bool = True
    mime_type_detection: bool = True

    # Processing options
    stream_threshold_mb: float = 10.0
    buffer_size: int = 8192

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "suffixes": (
                    list(self.file_extensions)
                    if hasattr(self, "file_extensions")
                    else None
                ),
                "encoding": self.encoding if hasattr(self, "encoding") else "utf-8",
                "show_progress": True,
            }
        )
        return kwargs


@register_bulk_source(
    name="cloud_blob",
    category=SourceCategory.DIRECTORY_CLOUD,
    loaders={
        "blob": {
            "class": "CloudBlobLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="blob",
    description="Multi-cloud blob loader supporting s3://, gs://, az:// schemes",
    max_concurrent=8,
    requires_credentials=True,
    credential_type=CredentialType.CLOUD_CREDENTIALS,
    priority=8,
)
class CloudBlobSource(CloudStorageSource):
    """Multi-cloud blob source supporting various cloud storage schemes."""

    # Cloud scheme configuration
    scheme: str  # s3://, gs://, az://, file://
    path: str

    # Blob processing
    parser_config: Dict[str, Any] = {}

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"path": f"{self.scheme}{self.path}", "parser": self.parser_config}
        )
        return kwargs


# =============================================================================
# Streaming and Real-time Sources
# =============================================================================


@register_bulk_source(
    name="streaming_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "stream": {
            "class": "DirectoryLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="stream",
    description="Streaming directory loader for real-time file processing",
    max_concurrent=4,
    priority=7,
)
class StreamingDirectorySource(DirectorySource):
    """Streaming directory source for real-time processing."""

    # Streaming configuration
    watch_for_changes: bool = True
    polling_interval: float = 1.0
    incremental_processing: bool = True

    # File change detection
    detect_modifications: bool = True
    detect_additions: bool = True
    detect_deletions: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "watch": self.watch_for_changes,
                "poll_interval": self.polling_interval,
                "incremental": self.incremental_processing,
            }
        )
        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_bulk_sources_statistics() -> Dict[str, Any]:
    """Get statistics about bulk loading sources."""
    registry = enhanced_registry

    # Find all bulk loaders
    bulk_loaders = registry.find_bulk_loaders()
    recursive_loaders = registry.find_recursive_loaders()

    # Analyze capabilities
    streaming_capable = len(
        registry.find_sources_with_capability(LoaderCapability.STREAMING)
    )
    filtering_capable = len(
        registry.find_sources_with_capability(LoaderCapability.FILTERING)
    )
    incremental_capable = len(
        registry.find_sources_with_capability(LoaderCapability.INCREMENTAL)
    )

    # Cloud vs local
    cloud_bulk = len(registry.find_sources_by_category(SourceCategory.DIRECTORY_CLOUD))
    local_bulk = len(registry.find_sources_by_category(SourceCategory.DIRECTORY_LOCAL))

    return {
        "total_bulk_loaders": len(bulk_loaders),
        "recursive_loaders": len(recursive_loaders),
        "cloud_bulk_loaders": cloud_bulk,
        "local_bulk_loaders": local_bulk,
        "capabilities": {
            "streaming": streaming_capable,
            "filtering": filtering_capable,
            "incremental": incremental_capable,
        },
        "max_concurrency_available": max(
            [
                reg.bulk_info.max_concurrent
                for reg in registry._sources.values()
                if reg.bulk_info.supports_bulk
            ],
            default=0,
        ),
    }


def get_scrape_all_sources() -> List[str]:
    """Get list of all sources with 'scrape all' capabilities."""
    registry = enhanced_registry

    scrape_all_sources = []

    # Find sources with bulk + recursive capabilities
    for name, registration in registry._sources.items():
        capabilities = registration.capabilities.capabilities
        if (
            LoaderCapability.BULK_LOADING in capabilities
            and LoaderCapability.RECURSIVE in capabilities
        ):
            scrape_all_sources.append(name)

    return scrape_all_sources


def validate_bulk_sources() -> bool:
    """Validate bulk source registrations."""
    registry = enhanced_registry

    required_bulk_sources = [
        "recursive_directory",
        "s3_bucket",
        "gcs_bucket",
        "azure_container",
        "filesystem_blob",
        "cloud_blob",
    ]

    missing = []
    for source_name in required_bulk_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing bulk sources: {missing}")
        return False

    scrape_all = get_scrape_all_sources()
    print(f"✅ All {len(required_bulk_sources)} bulk sources registered!")
    print(f"🔄 {len(scrape_all)} sources with 'scrape all' capability: {scrape_all}")
    return True


# Auto-validate on import
if __name__ == "__main__":
    validate_bulk_sources()
    stats = get_bulk_sources_statistics()
    print(f"Bulk Sources Statistics: {stats}")
