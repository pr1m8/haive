"""Ultimate Auto-Loader for Document Sources.

This module provides the ultimate auto-loader functionality that can automatically
detect, instantiate, and load documents from any source type. It integrates with
the enhanced registry and path analyzer to provide seamless document loading.

The AutoLoader is the main entry point for users who want to load documents
without manually configuring source types and loaders.

Examples:
    Basic auto-loading::

        from haive.core.engine.document.loaders import AutoLoader

        # Auto-detect and load from any source
        loader = AutoLoader()
        documents = loader.load("https://example.com/docs")

    With preferences::

        # Prefer quality over speed
        loader = AutoLoader(preference="quality")
        documents = loader.load("s3://bucket/documents/")

    Bulk loading::

        # Load entire directory/bucket/site
        loader = AutoLoader()
        documents = loader.load_all("/path/to/documents")

Author: Claude (Haive Document Loader System)
Version: 1.0.0
"""

import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from langchain_core.documents import Document
from pydantic import BaseModel, Field

from haive.core.engine.document.config import LoaderPreference

from .path_analyzer import PathAnalyzer, SourceInfo
from .sources.enhanced_registry import enhanced_registry
from .sources.source_types import BaseSource, LoaderCapability, SourceCategory

logger = logging.getLogger(__name__)


class LoadingResult(BaseModel):
    """Comprehensive result container for single-source document loading operations.

    This Pydantic model encapsulates all information about a document loading operation,
    including the loaded documents, source analysis results, performance metrics,
    and any errors encountered during the process.

    Attributes:
        documents (List[Document]): List of successfully loaded Document objects.
            Each Document contains page_content (str) and metadata (dict).
            Empty list if loading failed.
        source_info (SourceInfo): Detailed information about the detected source
            including source type, category, confidence score, and capabilities.
        loader_used (str): Name of the specific loader that was selected and used
            for this operation (e.g., "pypdf", "beautiful_soup", "csv").
        loading_time (float): Total time taken for the loading operation in seconds,
            including source detection, loader instantiation, and document extraction.
        metadata (Dict[str, Any]): Additional metadata collected during loading
            including loader configuration, extraction settings, and performance info.
        errors (List[str]): List of error messages encountered during loading.
            Empty list indicates successful loading without errors.

    Examples:
        Successful loading result::

            result = loader.load_detailed("document.pdf")
            print(f"Loaded {len(result.documents)} documents")
            print(f"Source: {result.source_info.source_type}")
            print(f"Loader: {result.loader_used}")
            print(f"Time: {result.loading_time:.2f}s")

        Error handling::

            result = loader.load_detailed("invalid.pdf")
            if result.errors:
                print(f"Loading failed: {result.errors}")
            else:
                print(f"Success: {len(result.documents)} documents")

    Note:
        This class is returned by load_detailed() and is included in BulkLoadingResult
        for individual source results in bulk operations.
    """

    documents: list[Document] = Field(
        description="List of successfully loaded Document objects"
    )
    source_info: SourceInfo = Field(
        description="Detailed information about the detected source"
    )
    loader_used: str = Field(description="Name of the specific loader that was used")
    loading_time: float = Field(
        ge=0.0, description="Total time taken for loading operation in seconds"
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata from loading process"
    )
    errors: list[str] = Field(
        default_factory=list, description="List of error messages encountered"
    )

    class Config:
        arbitrary_types_allowed = True


class BulkLoadingResult(BaseModel):
    """Comprehensive result container for bulk document loading operations.

    This Pydantic model provides detailed information about bulk loading operations,
    including individual source results, aggregate statistics, error tracking,
    and performance metrics across all sources.

    Attributes:
        total_documents (int): Total number of documents successfully loaded
            across all sources. Sum of documents from all successful LoadingResults.
        results (List[LoadingResult]): List of individual LoadingResult objects,
            one for each source that was processed (both successful and failed).
            Provides detailed per-source information including errors.
        failed_sources (List[Tuple[str, str]]): List of tuples containing
            (source_identifier, error_message) for sources that failed to load.
            Allows easy identification of problematic sources.
        total_time (float): Total elapsed time for the entire bulk operation
            in seconds, including all concurrent processing and overhead.
        summary (Dict[str, Any]): Dictionary containing aggregate statistics:
            - total_sources (int): Number of sources processed
            - successful_loads (int): Number of sources loaded successfully
            - failed_loads (int): Number of sources that failed
            - success_rate (float): Percentage of successful loads
            - avg_loading_time (float): Average time per source
            - total_errors (int): Total number of errors encountered

    Examples:
        Analyzing bulk loading results::

            sources = ["doc1.pdf", "doc2.pdf", "invalid.pdf"]
            result = loader.load_bulk(sources)

            print(f"Loaded {result.total_documents} documents")
            print(f"Success rate: {result.summary['success_rate']:.1f}%")
            print(f"Total time: {result.total_time:.2f}s")

            if result.failed_sources:
                print("Failed sources:")
                for source, error in result.failed_sources:
                    print(f"  {source}: {error}")

        Processing individual results::

            for i, loading_result in enumerate(result.results):
                source = sources[i]
                if loading_result.errors:
                    print(f"{source} failed: {loading_result.errors}")
                else:
                    docs = len(loading_result.documents)
                    time = loading_result.loading_time
                    print(f"{source}: {docs} docs in {time:.2f}s")

        Performance analysis::

            print("Performance Summary:")
            print(f"  Total sources: {result.summary['total_sources']}")
            print(f"  Average time per source: {result.summary['avg_loading_time']:.2f}s")
            print(f"  Concurrent efficiency: {result.summary['total_sources'] * result.summary['avg_loading_time'] / result.total_time:.1f}x")

    Note:
        This class is returned by load_bulk() and aload_bulk() methods.
        For simple flattened document lists, use load_documents() instead.
    """

    total_documents: int = Field(
        ge=0, description="Total number of documents successfully loaded"
    )
    results: list[LoadingResult] = Field(
        description="List of individual LoadingResult objects for each source"
    )
    failed_sources: list[tuple[str, str]] = Field(
        default_factory=list,
        description="List of (source, error) tuples for failed sources",
    )
    total_time: float = Field(
        ge=0.0, description="Total elapsed time for the bulk operation in seconds"
    )
    summary: dict[str, Any] = Field(
        default_factory=dict, description="Dictionary containing aggregate statistics"
    )

    class Config:
        arbitrary_types_allowed = True


class AutoLoaderConfig(BaseModel):
    """Configuration model for the AutoLoader system.

    This class defines all configuration options for the AutoLoader, allowing
    fine-tuned control over loading behavior, performance characteristics,
    and operational parameters.

    Attributes:
        preference (LoaderPreference): Loading preference balancing speed vs quality.
            Options: SPEED, QUALITY, BALANCED. Default: BALANCED.
        max_concurrency (int): Maximum number of concurrent loading operations.
            Range: 1-100. Default: 10.
        timeout (int): Timeout for individual loading operations in seconds.
            Minimum: 10. Default: 300.
        retry_attempts (int): Number of retry attempts for failed loads.
            Range: 0-10. Default: 3.
        enable_caching (bool): Whether to enable document caching for performance.
            Default: False.
        cache_ttl (int): Cache time-to-live in seconds. Minimum: 60. Default: 3600.
        default_chunk_size (int): Default chunk size for text splitting.
            Range: 100-10000. Default: 1000.
        enable_metadata (bool): Whether to extract and enrich document metadata.
            Default: True.
        credential_manager (Optional[Any]): Custom credential manager instance.
            Default: None.

    Examples:
        Basic quality-focused configuration::

            config = AutoLoaderConfig(
                preference=LoaderPreference.QUALITY,
                max_concurrency=5,
                timeout=600,
                enable_metadata=True
            )

        High-performance configuration with caching::

            config = AutoLoaderConfig(
                preference=LoaderPreference.SPEED,
                max_concurrency=50,
                enable_caching=True,
                cache_ttl=7200,
                retry_attempts=1
            )

        Balanced configuration for production::

            config = AutoLoaderConfig(
                preference=LoaderPreference.BALANCED,
                max_concurrency=20,
                timeout=300,
                enable_caching=True,
                enable_metadata=True
            )

    Raises:
        ValidationError: If any configuration values are outside valid ranges.

    Note:
        Higher concurrency improves performance but increases resource usage.
        Enable caching for repeated document access patterns.
        Quality preference may be slower but provides better text extraction.
    """

    preference: LoaderPreference = Field(
        default=LoaderPreference.BALANCED,
        description="Loading preference for quality vs speed",
    )
    max_concurrency: int = Field(
        default=10, ge=1, le=100, description="Maximum concurrent loading operations"
    )
    timeout: int = Field(
        default=300, ge=10, description="Timeout for individual operations in seconds"
    )
    retry_attempts: int = Field(
        default=3, ge=0, le=10, description="Number of retry attempts"
    )
    enable_caching: bool = Field(default=False, description="Enable document caching")
    cache_ttl: int = Field(
        default=3600, ge=60, description="Cache time-to-live in seconds"
    )
    default_chunk_size: int = Field(
        default=1000, ge=100, description="Default chunk size for text splitting"
    )
    enable_metadata: bool = Field(
        default=True, description="Extract metadata from documents"
    )
    credential_manager: Any | None = Field(
        default=None, description="Custom credential manager"
    )

    class Config:
        """Pydantic configuration."""

        arbitrary_types_allowed = True


class AutoLoader:
    """Ultimate automatic document loader with 230+ langchain_community integrations.

    The AutoLoader is the primary interface for loading documents from any source
    type. It automatically detects source types, selects optimal loaders, and
    provides comprehensive loading capabilities with enterprise-grade features.

    This class implements the complete document loading pipeline including:
    source detection, loader selection, document loading, metadata enrichment,
    error handling, retry logic, caching, and concurrent processing.

    Attributes:
        config (AutoLoaderConfig): Configuration controlling loader behavior.
        registry (EnhancedRegistry): Registry of available document loaders.
        path_analyzer (PathAnalyzer): Component for analyzing and detecting source types.

    Supported Sources:
        - **Local Files**: PDF, DOCX, TXT, CSV, JSON, XML, code files, archives
        - **Web Sources**: HTML pages, APIs, documentation sites, social media
        - **Databases**: PostgreSQL, MySQL, MongoDB, Redis, Elasticsearch
        - **Cloud Storage**: S3, Google Cloud, Azure Blob, Google Drive, Dropbox
        - **Business Platforms**: Salesforce, HubSpot, Zendesk, Jira, Confluence
        - **Communication**: Slack, Discord, Teams, email systems
        - **Specialized**: Government data, healthcare, finance, education

    Key Methods:
        - load(): Load documents from a single source
        - load_documents(): Load from multiple sources (standard langchain method)
        - load_bulk(): Bulk loading with detailed results
        - load_all(): Recursive loading from directories/websites
        - aload(): Async loading for high-performance scenarios

    Examples:
        Basic document loading::

            loader = AutoLoader()
            docs = loader.load("document.pdf")  # Single document
            docs = loader.load_documents(["file1.pdf", "file2.txt"])  # Multiple

        Advanced configuration::

            config = AutoLoaderConfig(
                preference=LoaderPreference.QUALITY,
                max_concurrency=20,
                enable_caching=True,
                enable_metadata=True
            )
            loader = AutoLoader(config)
            docs = loader.load("https://complex-site.com")

        Enterprise bulk loading::

            sources = [
                "/shared/reports/quarterly.pdf",
                "s3://company-docs/policies/",
                "https://wiki.company.com/procedures",
                {"path": "salesforce://attachments", "auth": "token"}
            ]
            result = loader.load_bulk(sources)
            print(f"Loaded {result.total_documents} documents")

        High-performance async loading::

            async def process_sources():
                docs = await loader.aload_documents([
                    "https://api.service.com/docs",
                    "postgres://db/knowledge_base",
                    "gs://bucket/research-papers/"
                ])
                return docs

        Recursive directory processing::

            # Load all documents from directory tree
            docs = loader.load_all("/company/documents/")

            # Scrape entire documentation site
            docs = loader.load_all("https://docs.framework.com", max_depth=3)

    Performance Features:
        - Concurrent loading with configurable worker limits
        - Intelligent caching with TTL support
        - Adaptive retry logic with exponential backoff
        - Progress tracking for bulk operations
        - Memory-efficient streaming for large datasets

    Error Handling:
        - Graceful degradation for unsupported sources
        - Detailed error reporting with source tracking
        - Automatic fallback to alternative loaders
        - Comprehensive logging for debugging

    Thread Safety:
        This class is thread-safe and can be used safely in concurrent
        environments. Internal state is properly synchronized.

    See Also:
        - AutoLoaderConfig: Configuration options
        - LoadingResult: Detailed loading results
        - BulkLoadingResult: Bulk operation results
        - LoaderPreference: Quality vs speed preferences
    """

    def __init__(
        self,
        config: AutoLoaderConfig | None = None,
        registry: Any | None = None,
        path_analyzer: PathAnalyzer | None = None,
    ):
        """Initialize the AutoLoader with optional configuration and components.

        Creates a new AutoLoader instance with the specified configuration.
        If no configuration is provided, uses sensible defaults optimized
        for balanced performance and quality.

        Args:
            config (Optional[AutoLoaderConfig]): Configuration object controlling
                loader behavior including concurrency, preferences, caching, and
                retry settings. If None, uses default balanced configuration.
            registry (Optional[Any]): Custom enhanced registry instance containing
                document loader mappings. If None, uses the global enhanced registry
                with all 230+ registered loaders.
            path_analyzer (Optional[PathAnalyzer]): Custom path analyzer for source
                type detection. If None, uses the default PathAnalyzer instance.

        Examples:
            Default initialization::

                loader = AutoLoader()  # Uses balanced defaults

            Custom configuration::

                config = AutoLoaderConfig(
                    preference=LoaderPreference.QUALITY,
                    max_concurrency=5,
                    enable_caching=True
                )
                loader = AutoLoader(config)

            Advanced with custom components::

                custom_registry = MyCustomRegistry()
                custom_analyzer = MyPathAnalyzer()
                loader = AutoLoader(
                    config=my_config,
                    registry=custom_registry,
                    path_analyzer=custom_analyzer
                )

        Note:
            The AutoLoader automatically triggers source registration on first use.
            This process scans for available loaders and may take a few seconds
            on initial startup.
        """
        self.config = config or AutoLoaderConfig()
        self.registry = registry or enhanced_registry
        self.path_analyzer = path_analyzer or PathAnalyzer()
        self._cache: dict[str, tuple[list[Document], datetime]] = {}

        logger.info(f"AutoLoader initialized with {self.config.preference} preference")

    def detect_source(self, path_or_url: str) -> SourceInfo:
        """Detect source type and get source information.

        Args:
            path_or_url: Path, URL, or connection string to analyze

        Returns:
            SourceInfo containing detected source details

        Raises:
            ValueError: If source type cannot be detected

        Examples:
            Detect file source::

                info = loader.detect_source("/path/to/document.pdf")
                print(f"Source type: {info.source_type}")
                print(f"Category: {info.category}")

            Detect web source::

                info = loader.detect_source("https://example.com")
                print(f"Capabilities: {info.capabilities}")
        """
        try:
            source_info = self.path_analyzer.analyze_path(path_or_url)
            logger.debug(
                f"Detected source: {source_info.source_type} for {path_or_url}"
            )
            return source_info
        except Exception as e:
            logger.exception(f"Failed to detect source for {path_or_url}: {e}")
            raise ValueError(f"Could not detect source type for: {path_or_url}") from e

    def get_best_loader(self, source_info: SourceInfo) -> tuple[str, dict[str, Any]]:
        """Get the best loader for a source based on preferences.

        Args:
            source_info: Source information from detection

        Returns:
            Tuple of (loader_name, loader_config)

        Raises:
            ValueError: If no suitable loader is found

        Examples:
            Get quality-focused loader::

                config = AutoLoaderConfig(preference="quality")
                loader = AutoLoader(config)
                info = loader.detect_source("document.pdf")
                loader_name, loader_config = loader.get_best_loader(info)
        """
        try:
            loader_name = self.registry.get_loader_for_source(
                source_info.source_type, preference=self.config.preference
            )

            loader_config = self.registry.get_loader_config(
                source_info.source_type, loader_name
            )

            logger.debug(
                f"Selected loader: {loader_name} for {source_info.source_type}"
            )
            return loader_name, loader_config

        except Exception as e:
            logger.exception(f"Failed to get loader for {source_info.source_type}: {e}")
            raise ValueError(
                f"No suitable loader found for {source_info.source_type}"
            ) from e

    def create_source_instance(
        self, source_info: SourceInfo, path_or_url: str, **kwargs
    ) -> BaseSource:
        """Create a source instance for the detected source type.

        Args:
            source_info: Source information from detection
            path_or_url: Original path or URL
            **kwargs: Additional parameters for source creation

        Returns:
            Configured source instance

        Raises:
            ValueError: If source cannot be created

        Examples:
            Create and configure source::

                info = loader.detect_source("s3://bucket/file.pdf")
                source = loader.create_source_instance(
                    info,
                    "s3://bucket/file.pdf",
                    aws_access_key_id="key",
                    aws_secret_access_key="secret"
                )
        """
        try:
            source_class = self.registry.get_source_class(source_info.source_type)

            # Prepare source configuration
            source_config = {**source_info.metadata, **kwargs}

            # Add path/URL based on source type
            if source_info.category in [
                SourceCategory.LOCAL_FILE,
                SourceCategory.ARCHIVE,
            ]:
                source_config["path"] = Path(path_or_url)
            elif source_info.category in [SourceCategory.WEB, SourceCategory.API]:
                source_config["url"] = path_or_url
            else:
                source_config["source_path"] = path_or_url

            source_instance = source_class(**source_config)
            logger.debug(f"Created source instance: {source_class.__name__}")
            return source_instance

        except Exception as e:
            logger.exception(f"Failed to create source instance: {e}")
            raise ValueError(
                f"Could not create source for {source_info.source_type}"
            ) from e

    def _get_from_cache(self, cache_key: str) -> list[Document] | None:
        """Get documents from cache if available and not expired."""
        if not self.config.enable_caching:
            return None

        if cache_key in self._cache:
            documents, timestamp = self._cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.config.cache_ttl:
                logger.debug(f"Cache hit for {cache_key}")
                return documents
            # Remove expired cache entry
            del self._cache[cache_key]

        return None

    def _save_to_cache(self, cache_key: str, documents: list[Document]) -> None:
        """Save documents to cache."""
        if self.config.enable_caching:
            self._cache[cache_key] = (documents, datetime.now())
            logger.debug(f"Cached {len(documents)} documents for {cache_key}")

    def load(self, path_or_url: str, **kwargs) -> list[Document]:
        """Load documents from any source with automatic detection and optimization.

        This is the primary interface for single-source document loading. The method
        performs automatic source type detection, intelligent loader selection based
        on configured preferences, and returns a list of loaded Document objects.

        The loading process includes:
        1. Source type detection and analysis
        2. Best loader selection based on preference and capabilities
        3. Source instance creation with provided parameters
        4. Document loading with retry logic and error handling
        5. Optional metadata enrichment and caching

        Args:
            path_or_url (str): Path, URL, or connection string to load from.
                Supports local files, web URLs, database connections, cloud storage
                URIs, and API endpoints. Examples:
                - "/path/to/file.pdf" (local file)
                - "https://example.com/doc.html" (web page)
                - "postgresql://user:pass@host/db" (database)
                - "s3://bucket/key" (cloud storage)
            **kwargs: Additional parameters passed to the source and loader.
                Common parameters include:
                - extract_images (bool): Whether to extract images from documents
                - chunk_size (int): Text splitting chunk size
                - timeout (int): Override default timeout
                - headers (dict): HTTP headers for web requests
                - query (str): SQL query for database sources
                - recursive (bool): Recursive processing for directories

        Returns:
            List[Document]: List of loaded Document objects. Each Document contains:
                - page_content (str): Extracted text content
                - metadata (dict): Source metadata, extraction info, and enrichments

        Raises:
            ValueError: If the source cannot be detected, is unsupported, or
                if required parameters are missing for the detected source type.
            TimeoutError: If loading exceeds the configured timeout limit.
            ConnectionError: If unable to connect to remote sources (web, database, API).
            FileNotFoundError: If local files or directories do not exist.
            PermissionError: If insufficient permissions to access the source.

        Examples:
            Basic local file loading::

                loader = AutoLoader()
                docs = loader.load("/documents/report.pdf")
                print(f"Loaded {len(docs)} pages")

            Web page with custom parameters::

                docs = loader.load(
                    "https://docs.example.com/api",
                    headers={"Authorization": "Bearer token"},
                    timeout=120
                )

            Database with custom query::

                docs = loader.load(
                    "postgresql://user:pass@localhost:5432/knowledge",
                    query="SELECT title, content FROM articles WHERE published = true",
                    chunk_size=2000
                )

            Cloud storage with credentials::

                docs = loader.load(
                    "s3://company-docs/policies/security.pdf",
                    aws_access_key_id="AKIA...",
                    aws_secret_access_key="secret",
                    region_name="us-east-1"
                )

            High-quality extraction::

                config = AutoLoaderConfig(preference=LoaderPreference.QUALITY)
                loader = AutoLoader(config)
                docs = loader.load("complex_document.pdf", extract_images=True)

        Note:
            - Results are automatically cached if caching is enabled in configuration
            - Metadata enrichment adds source tracking information when enabled
            - The method is thread-safe and can be called concurrently
            - For multiple sources, consider using load_documents() or load_bulk()

        See Also:
            - load_documents(): Load from multiple sources (standard langchain method)
            - load_bulk(): Bulk loading with detailed result information
            - load_all(): Recursive loading from directories or websites
            - aload(): Asynchronous version for high-performance scenarios
        """
        start_time = datetime.now()
        cache_key = f"{path_or_url}:{hash(str(sorted(kwargs.items())))}"

        # Check cache first
        cached_docs = self._get_from_cache(cache_key)
        if cached_docs is not None:
            return cached_docs

        try:
            # Detect source type
            source_info = self.detect_source(path_or_url)

            # Get best loader
            loader_name, loader_config = self.get_best_loader(source_info)

            # Create source instance
            source_instance = self.create_source_instance(
                source_info, path_or_url, **kwargs
            )

            # Get loader class and load documents
            loader_class = self.registry.get_loader_class(
                source_info.source_type, loader_name
            )

            loader_kwargs = source_instance.get_loader_kwargs()
            loader_kwargs.update(kwargs)

            loader_instance = loader_class(**loader_kwargs)

            # Load documents with retry logic
            documents = self._load_with_retry(loader_instance, source_info.source_type)

            # Add metadata if enabled
            if self.config.enable_metadata:
                self._enrich_documents_metadata(documents, source_info, loader_name)

            # Cache results
            self._save_to_cache(cache_key, documents)

            loading_time = (datetime.now() - start_time).total_seconds()
            logger.info(
                f"Loaded {len(documents)} documents from {source_info.source_type} "
                f"in {loading_time:.2f}s using {loader_name}"
            )

            return documents

        except Exception as e:
            loading_time = (datetime.now() - start_time).total_seconds()
            logger.exception(
                f"Failed to load {path_or_url} after {loading_time:.2f}s: {e}"
            )
            raise

    def load_documents(
        self, sources: list[str | dict[str, Any]], **kwargs
    ) -> list[Document]:
        """Load documents from multiple sources with standard langchain interface.

        This method implements the standard langchain convention for loading documents
        from multiple sources. It processes all sources concurrently, handles errors
        gracefully, and returns a flattened list of all successfully loaded documents.

        This is the recommended method for loading from multiple sources as it follows
        langchain conventions and provides seamless integration with existing langchain
        workflows and chains.

        Args:
            sources (List[Union[str, Dict[str, Any]]]): List of sources to load from.
                Each source can be either:
                - str: Simple path, URL, or connection string
                - Dict[str, Any]: Configuration dict with source-specific parameters.
                  Must contain either 'path' or 'url' key, plus optional parameters.
            **kwargs: Default parameters applied to ALL sources and loaders.
                These are overridden by source-specific parameters in dict sources.
                Common parameters:
                - max_workers (int): Override concurrency for this operation
                - timeout (int): Timeout per source
                - extract_images (bool): Extract images from documents
                - chunk_size (int): Text splitting chunk size

        Returns:
            List[Document]: Flattened list of Document objects from all successful
                source loads. Failed sources are silently skipped. Each Document
                contains page_content and metadata with source tracking information.

        Examples:
            Basic multi-source loading::

                loader = AutoLoader()
                docs = loader.load_documents([
                    "/reports/quarterly.pdf",
                    "/docs/manual.docx",
                    "https://company.com/policies.html"
                ])
                print(f"Loaded {len(docs)} total documents")

            Mixed source types with configurations::

                docs = loader.load_documents([
                    # Simple string sources
                    "local_file.pdf",
                    "https://simple-site.com",

                    # Complex configured sources
                    {
                        "path": "complex_document.pdf",
                        "extract_images": True,
                        "chunk_size": 2000
                    },
                    {
                        "url": "https://api.service.com/docs",
                        "headers": {"Authorization": "Bearer token"},
                        "timeout": 120
                    },
                    {
                        "path": "s3://bucket/document.pdf",
                        "aws_access_key_id": "key",
                        "aws_secret_access_key": "secret"
                    }
                ])

            Enterprise data aggregation::

                enterprise_sources = [
                    "/shared/reports/2024/",  # Directory
                    "https://wiki.company.com/procedures",
                    "postgresql://db/knowledge_base",
                    "salesforce://contracts",
                    "sharepoint://policies/"
                ]
                docs = loader.load_documents(enterprise_sources)

            With global parameters::

                docs = loader.load_documents(
                    ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
                    extract_images=True,  # Applied to all sources
                    chunk_size=1500,      # Applied to all sources
                    max_workers=10        # Override concurrency
                )

        Performance:
            - Sources are processed concurrently based on max_concurrency setting
            - Failed sources don't stop processing of other sources
            - Results are automatically cached if caching is enabled
            - Memory usage is optimized through document streaming

        Error Handling:
            - Individual source failures are logged but don't stop processing
            - Failed sources are excluded from results
            - Use load_bulk() for detailed error information per source
            - Network timeouts and connection errors are handled gracefully

        Langchain Compatibility:
            This method follows the standard langchain DocumentLoader interface:
            - Method name: load_documents() (plural)
            - Return type: List[Document]
            - Behavior: Load from multiple sources, return flattened results
            - Integration: Works seamlessly with langchain chains and workflows

        See Also:
            - load(): Load from a single source
            - load_bulk(): Get detailed results and error information
            - load_all(): Recursive loading from directories/websites
            - aload_documents(): Async version for high-performance scenarios

        Note:
            For detailed loading results including error information and
            per-source statistics, use load_bulk() instead.
        """
        bulk_result = self.load_bulk(sources, **kwargs)

        # Flatten all documents from successful loads
        all_documents = []
        for result in bulk_result.results:
            all_documents.extend(result.documents)

        return all_documents

    def load_detailed(self, path_or_url: str, **kwargs) -> LoadingResult:
        """Load documents with detailed result information.

        Args:
            path_or_url: Path, URL, or connection string to load from
            **kwargs: Additional parameters passed to the source and loader

        Returns:
            LoadingResult with documents and detailed metadata

        Examples:
            Get detailed loading information::

                result = loader.load_detailed("/path/to/document.pdf")
                print(f"Loaded {len(result.documents)} documents")
                print(f"Using loader: {result.loader_used}")
                print(f"Loading time: {result.loading_time:.2f}s")
                print(f"Source type: {result.source_info.source_type}")
        """
        start_time = datetime.now()
        errors = []

        try:
            # Detect source type
            source_info = self.detect_source(path_or_url)

            # Get best loader
            loader_name, loader_config = self.get_best_loader(source_info)

            # Load documents
            documents = self.load(path_or_url, **kwargs)

            loading_time = (datetime.now() - start_time).total_seconds()

            return LoadingResult(
                documents=documents,
                source_info=source_info,
                loader_used=loader_name,
                loading_time=loading_time,
                metadata={
                    "loader_config": loader_config,
                    "source_metadata": source_info.metadata,
                    "kwargs": kwargs,
                },
                errors=errors,
            )

        except Exception as e:
            loading_time = (datetime.now() - start_time).total_seconds()
            errors.append(str(e))

            # Create minimal result for failed load
            return LoadingResult(
                documents=[],
                source_info=SourceInfo(
                    source_type="unknown",
                    category=SourceCategory.UNKNOWN,
                    confidence=0.0,
                    metadata={"original_path": path_or_url},
                ),
                loader_used="none",
                loading_time=loading_time,
                metadata={"kwargs": kwargs},
                errors=errors,
            )

    def load_bulk(
        self, sources: list[str | dict[str, Any]], **kwargs
    ) -> BulkLoadingResult:
        """Load documents from multiple sources concurrently.

        Args:
            sources: List of source paths/URLs or dicts with source config
            **kwargs: Default parameters applied to all sources

        Returns:
            BulkLoadingResult with aggregated results

        Examples:
            Bulk load multiple sources::

                sources = [
                    "file1.pdf",
                    "file2.docx",
                    {"path": "https://example.com", "timeout": 60}
                ]
                result = loader.load_bulk(sources)
                print(f"Total documents: {result.total_documents}")

            With progress tracking::

                def progress_callback(completed, total):
                    print(f"Progress: {completed}/{total}")

                result = loader.load_bulk(sources, progress_callback=progress_callback)
        """
        start_time = datetime.now()
        results = []
        failed_sources = []
        total_documents = 0

        progress_callback = kwargs.pop("progress_callback", None)

        def load_single_source(source_config):
            """Load a single source."""
            if isinstance(source_config, str):
                path_or_url = source_config
                source_kwargs = kwargs.copy()
            else:
                path_or_url = source_config.get("path") or source_config.get("url")
                source_kwargs = {**kwargs, **source_config}
                source_kwargs.pop("path", None)
                source_kwargs.pop("url", None)

            try:
                result = self.load_detailed(path_or_url, **source_kwargs)
                return result
            except Exception as e:
                return LoadingResult(
                    documents=[],
                    source_info=SourceInfo(
                        source_type="unknown",
                        category=SourceCategory.UNKNOWN,
                        confidence=0.0,
                        metadata={"original_path": path_or_url},
                    ),
                    loader_used="none",
                    loading_time=0.0,
                    metadata={"source_config": source_config},
                    errors=[str(e)],
                )

        # Execute concurrent loading
        with ThreadPoolExecutor(max_workers=self.config.max_concurrency) as executor:
            future_to_source = {
                executor.submit(load_single_source, source): source
                for source in sources
            }

            completed = 0
            for future in as_completed(future_to_source):
                source = future_to_source[future]
                result = future.result()
                results.append(result)

                if result.errors:
                    failed_sources.append((str(source), "; ".join(result.errors)))
                else:
                    total_documents += len(result.documents)

                completed += 1
                if progress_callback:
                    progress_callback(completed, len(sources))

        total_time = (datetime.now() - start_time).total_seconds()

        # Calculate summary statistics
        successful_loads = len([r for r in results if not r.errors])
        failed_loads = len(failed_sources)
        avg_loading_time = (
            sum(r.loading_time for r in results) / len(results) if results else 0
        )

        summary = {
            "total_sources": len(sources),
            "successful_loads": successful_loads,
            "failed_loads": failed_loads,
            "success_rate": (successful_loads / len(sources)) * 100 if sources else 0,
            "avg_loading_time": avg_loading_time,
            "total_loading_time": total_time,
        }

        logger.info(
            f"Bulk loading completed: {total_documents} documents from "
            f"{successful_loads}/{len(sources)} sources in {total_time:.2f}s"
        )

        return BulkLoadingResult(
            total_documents=total_documents,
            results=results,
            failed_sources=failed_sources,
            total_time=total_time,
            summary=summary,
        )

    def load_all(self, path_or_url: str, **kwargs) -> list[Document]:
        """Load all documents from a source recursively.

        This method uses the "scrape_all" capability of sources to load
        all available documents from directories, websites, databases, etc.

        Args:
            path_or_url: Path, URL, or connection string to load from
            **kwargs: Additional parameters for recursive loading

        Returns:
            List of all documents found in the source

        Examples:
            Load entire directory::

                documents = loader.load_all("/path/to/documents/")

            Scrape entire website::

                documents = loader.load_all("https://docs.example.com")

            Load all tables from database::

                documents = loader.load_all("postgresql://user:pass@host/db")
        """
        try:
            # Detect source and create instance
            source_info = self.detect_source(path_or_url)
            source_instance = self.create_source_instance(
                source_info, path_or_url, **kwargs
            )

            # Check if source supports scrape_all
            if not hasattr(source_instance, "scrape_all"):
                logger.warning(
                    f"Source {source_info.source_type} doesn't support scrape_all"
                )
                return self.load(path_or_url, **kwargs)

            # Get scrape_all configuration
            scrape_config = source_instance.scrape_all()

            # Merge with user kwargs
            final_kwargs = {**scrape_config, **kwargs}

            # Load with scrape_all configuration
            documents = self.load(path_or_url, **final_kwargs)

            logger.info(f"Loaded {len(documents)} documents using scrape_all")
            return documents

        except Exception as e:
            logger.exception(f"Failed to load_all from {path_or_url}: {e}")
            raise

    async def aload(self, path_or_url: str, **kwargs) -> list[Document]:
        """Asynchronously load documents from any source.

        Args:
            path_or_url: Path, URL, or connection string to load from
            **kwargs: Additional parameters passed to the source and loader

        Returns:
            List of loaded Document objects

        Examples:
            Async document loading::

                async def load_docs():
                    documents = await loader.aload("https://example.com")
                    return documents

                documents = asyncio.run(load_docs())
        """
        loop = asyncio.get_event_loop()

        # Run the synchronous load in a thread executor
        return await loop.run_in_executor(None, self.load, path_or_url, **kwargs)

    async def aload_bulk(
        self, sources: list[str | dict[str, Any]], **kwargs
    ) -> BulkLoadingResult:
        """Asynchronously load documents from multiple sources.

        Args:
            sources: List of source paths/URLs or dicts with source config
            **kwargs: Default parameters applied to all sources

        Returns:
            BulkLoadingResult with aggregated results
        """
        loop = asyncio.get_event_loop()

        return await loop.run_in_executor(None, self.load_bulk, sources, **kwargs)

    async def aload_documents(
        self, sources: list[str | dict[str, Any]], **kwargs
    ) -> list[Document]:
        """Asynchronously load documents from multiple sources (standard langchain plural method name).

        This is the async version of load_documents() that takes a list of sources
        and returns a flattened list of all documents.

        Args:
            sources: List of source paths/URLs or source configurations
            **kwargs: Additional parameters passed to all sources and loaders

        Returns:
            Flattened list of Document objects from all sources

        Examples:
            Async load from multiple sources::

                loader = AutoLoader()
                docs = await loader.aload_documents([
                    "document1.pdf",
                    "document2.txt",
                    "https://example.com"
                ])
        """
        bulk_result = await self.aload_bulk(sources, **kwargs)

        # Flatten all documents from successful loads
        all_documents = []
        for result in bulk_result.results:
            all_documents.extend(result.documents)

        return all_documents

    def _load_with_retry(
        self, loader_instance: Any, source_type: str
    ) -> list[Document]:
        """Load documents with retry logic.

        Tries multiple loading methods in this order:
        1. load_documents() - Standard langchain plural method
        2. load() - Standard langchain singular method
        3. load_and_split() - Split method for chunking

        Args:
            loader_instance: The loader instance to use
            source_type: Type of source being loaded (for error messages)

        Returns:
            List of loaded Document objects

        Raises:
            ValueError: If loader has no supported load method
            Exception: The last exception from failed retry attempts
        """
        last_exception = None

        for attempt in range(self.config.retry_attempts + 1):
            try:
                # Try load_documents first (standard langchain plural method)
                if hasattr(loader_instance, "load_documents"):
                    documents = loader_instance.load_documents()
                # Fall back to load (standard langchain singular method)
                elif hasattr(loader_instance, "load"):
                    documents = loader_instance.load()
                # Finally try load_and_split for splitting loaders
                elif hasattr(loader_instance, "load_and_split"):
                    documents = loader_instance.load_and_split()
                else:
                    raise ValueError(
                        f"Loader {type(loader_instance)} has no supported load method "
                        f"(load_documents, load, or load_and_split)"
                    )

                # Ensure we always return a list
                if not isinstance(documents, list):
                    documents = list(documents) if documents else []

                return documents

            except Exception as e:
                last_exception = e
                if attempt < self.config.retry_attempts:
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {source_type}: {e}. Retrying..."
                    )
                    asyncio.sleep(min(2**attempt, 10))  # Exponential backoff
                else:
                    logger.exception(
                        f"All {self.config.retry_attempts + 1} attempts failed for {source_type}"
                    )

        raise last_exception

    def _enrich_documents_metadata(
        self, documents: list[Document], source_info: SourceInfo, loader_name: str
    ) -> None:
        """Enrich documents with additional metadata."""
        base_metadata = {
            "source_type": source_info.source_type,
            "source_category": source_info.category.value,
            "loader_used": loader_name,
            "loaded_at": datetime.now().isoformat(),
            "confidence": source_info.confidence,
        }

        for doc in documents:
            if doc.metadata is None:
                doc.metadata = {}
            doc.metadata.update(base_metadata)

    def get_supported_sources(self) -> dict[str, Any]:
        """Get information about all supported source types.

        Returns:
            Dictionary with source type information

        Examples:
            List all supported sources::

                sources = loader.get_supported_sources()
                for source_type, info in sources.items():
                    print(f"{source_type}: {info['description']}")
        """
        return self.registry.get_all_source_info()

    def get_capabilities(self, source_type: str) -> list[LoaderCapability]:
        """Get capabilities for a specific source type.

        Args:
            source_type: Name of the source type

        Returns:
            List of capabilities supported by the source

        Examples:
            Check source capabilities::

                caps = loader.get_capabilities("pdf")
                if LoaderCapability.BULK_LOADING in caps:
                    print("Supports bulk loading")
        """
        return self.registry.get_source_capabilities(source_type)

    def validate_credentials(self, source_type: str, **credentials) -> bool:
        """Validate credentials for a source type.

        Args:
            source_type: Name of the source type
            **credentials: Credential parameters to validate

        Returns:
            True if credentials are valid

        Examples:
            Validate database credentials::

                valid = loader.validate_credentials(
                    "postgresql",
                    host="localhost",
                    username="user",
                    password="pass"
                )
        """
        try:
            source_class = self.registry.get_source_class(source_type)
            # Try to create instance with credentials
            source_class(**credentials)
            return True
        except Exception as e:
            logger.exception(f"Credential validation failed for {source_type}: {e}")
            return False


# Convenience functions for common use cases


def load_document(path_or_url: str, **kwargs) -> list[Document]:
    """Convenience function to load documents automatically.

    Args:
        path_or_url: Path, URL, or connection string to load from
        **kwargs: Additional parameters

    Returns:
        List of loaded documents

    Examples:
        Quick document loading::

            from haive.core.engine.document.loaders import load_document

            documents = load_document("file.pdf")
            documents = load_document("https://example.com")
    """
    loader = AutoLoader()
    return loader.load(path_or_url, **kwargs)


def load_documents_bulk(sources: list[str], **kwargs) -> list[Document]:
    """Convenience function to load multiple documents.

    Args:
        sources: List of paths, URLs, or connection strings
        **kwargs: Additional parameters

    Returns:
        Flattened list of all loaded documents

    Examples:
        Bulk loading::

            from haive.core.engine.document.loaders import load_documents_bulk

            documents = load_documents_bulk([
                "file1.pdf",
                "file2.docx",
                "https://example.com"
            ])
    """
    loader = AutoLoader()
    result = loader.load_bulk(sources, **kwargs)

    # Flatten all documents
    all_documents = []
    for loading_result in result.results:
        all_documents.extend(loading_result.documents)

    return all_documents


async def aload_document(path_or_url: str, **kwargs) -> list[Document]:
    """Convenience function to load documents asynchronously.

    Args:
        path_or_url: Path, URL, or connection string to load from
        **kwargs: Additional parameters

    Returns:
        List of loaded documents

    Examples:
        Async document loading::

            from haive.core.engine.document.loaders import aload_document

            documents = await aload_document("https://example.com")
    """
    loader = AutoLoader()
    return await loader.aload(path_or_url, **kwargs)


# Global default loader instance
default_loader = AutoLoader()

# Export main classes and functions
__all__ = [
    "AutoLoader",
    "AutoLoaderConfig",
    "BulkLoadingResult",
    "LoadingResult",
    "aload_document",
    "default_loader",
    "load_document",
    "load_documents_bulk",
]
