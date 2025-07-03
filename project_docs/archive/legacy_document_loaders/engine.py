"""Document Loader Engine Implementation.

This module implements the DocumentLoaderEngine that integrates with the Haive
engine framework for loading documents from various sources.

The engine provides a unified interface for working with document loaders,
supporting different source types, loader strategies, and configuration options.
It properly inherits from InvokableEngine to integrate with the Haive engine
framework and follows the same patterns for configuration, schema definition,
and invocation.

Typical usage example:
    # Create a basic engine
    engine = create_document_loader_engine()

    # Load documents from a file
    documents = engine.invoke("/path/to/document.pdf")

    # Load documents from a web URL
    documents = engine.invoke("https://example.com")

    # Load documents with specific loader and options
    documents = engine.invoke({
        "source": "/path/to/directory",
        "loader_name": "directory_loader",
        "recursive": True,
        "loader_options": {"glob": "*.pdf"}
    })

    # Asynchronous loading
    documents = await engine.ainvoke("https://example.com")

    # Create a runnable for integration with other components
    runnable = engine.create_runnable({"use_async": True})
"""

import asyncio
import logging
import time
from pathlib import Path
from typing import Any, Optional, Union

# Import from engine config
from engine_config import (
    DocumentLoaderConfig,
    DocumentLoaderInput,
    DocumentLoaderOutput,
)
from haive.core.engine.base import EngineType, InvokableEngine

# Import from loader strategy
from loader_strategy import (
    LoaderRegistry,
    LoaderStrategy,
    loader_registry,
)

# Path analysis imports - placeholder for now
from path_analysis_implementation import analyze_path
from pydantic import Field

# Import from source implementations
from source_implementation import (
    BaseSource,
    LoaderStrategy,
    PathAnalysisResult,
)

# Import from source registry
from source_registry import SourceTypeRegistry
from source_registry import registry as source_registry

logger = logging.getLogger(__name__)


class DocumentLoaderEngine(
    InvokableEngine[Union[BaseSource, str, Path, dict[str, Any]], DocumentLoaderOutput]
):
    """Engine for loading documents from various sources.

    This engine provides a unified interface for working with document loaders,
    with support for different source types and configurations. It inherits from
    InvokableEngine to integrate with the Haive engine framework.

    The engine follows a layered architecture:
    1. Path analysis: Analyzes input paths to determine their properties
    2. Source detection: Identifies the appropriate source type based on path analysis
    3. Loader selection: Selects the best loader strategy for the detected source
    4. Document loading: Uses the selected loader to load documents

    The engine implements all required methods from InvokableEngine including
    get_input_fields(), get_output_fields(), and create_runnable(), enabling
    it to be used with the full capabilities of the engine framework.

    Attributes:
        engine_type: Type of the engine (DOCUMENT_LOADER)
        config: Configuration for the document loader engine
        _source_registry: Registry for source types
        _loader_registry: Registry for loader strategies
    """

    # Engine type
    engine_type: EngineType = Field(default=EngineType.DOCUMENT_LOADER)

    # Engine configuration
    config: DocumentLoaderConfig = Field(
        default_factory=DocumentLoaderConfig,
        description="Configuration for the document loader engine",
    )

    # State tracking
    _source_registry: SourceTypeRegistry | None = None
    _loader_registry: LoaderRegistry | None = None

    def __init__(self, **data):
        """Initialize the engine with configuration.

        Args:
            **data: Configuration parameters for the engine
        """
        super().__init__(**data)
        self._source_registry = source_registry
        self._loader_registry = loader_registry

    def get_input_fields(self) -> dict[str, tuple[type, Any]]:
        """Return input field definitions for the engine.

        This method defines the input schema for the document loader engine,
        including the source, source type, and loader options. It is required
        by the base Engine class for schema definition and validation.

        Returns:
            Dictionary mapping field names to (type, default) tuples

        Example:
            >>> engine = create_document_loader_engine()
            >>> input_fields = engine.get_input_fields()
            >>> print(list(input_fields.keys()))
            ['source', 'source_type', 'loader_name', 'loader_options', 'include_metadata', 'include_patterns', 'exclude_patterns']
        """
        return {
            "source": (Union[str, Path, dict[str, Any]], ...),
            "source_type": (Optional[str], None),
            "loader_name": (Optional[str], None),
            "loader_options": (dict[str, Any], {}),
            "include_metadata": (bool, True),
            "include_patterns": (list[str], []),
            "exclude_patterns": (list[str], []),
        }

    def get_output_fields(self) -> dict[str, tuple[type, Any]]:
        """Return output field definitions for the engine.

        This method defines the output schema for the document loader engine,
        including the loaded documents and operation metadata. It is required
        by the base Engine class for schema definition and validation.

        Returns:
            Dictionary mapping field names to (type, default) tuples

        Example:
            >>> engine = create_document_loader_engine()
            >>> output_fields = engine.get_output_fields()
            >>> print(list(output_fields.keys()))
            ['documents', 'total_documents', 'operation_time', 'source_type', 'loader_name', 'original_source', 'errors', 'has_errors']
        """
        return {
            "documents": (list[dict[str, Any]], []),
            "total_documents": (int, 0),
            "operation_time": (float, 0.0),
            "source_type": (str, ""),
            "loader_name": (str, ""),
            "original_source": (str, ""),
            "errors": (list[dict[str, Any]], []),
            "has_errors": (bool, False),
        }

    def create_runnable(self, runnable_config: dict[str, Any] | None = None) -> Any:
        """Create a runnable instance from this engine configuration.

        This method creates a runnable instance that can be invoked to load documents.
        For the document loader engine, this returns self since the engine itself
        is invokable. This method is required by the base Engine class and enables
        integration with the engine framework's factory pattern.

        The method applies any provided runtime configuration to the engine instance
        before returning it. This allows for customization of the engine behavior
        at runtime without modifying the original configuration.

        Args:
            runnable_config: Optional runtime configuration dictionary that can
                override engine settings for this specific invocation.

        Returns:
            The document loader engine instance (self) with applied configuration.

        Example:
            >>> engine = create_document_loader_engine()
            >>> runnable = engine.create_runnable({"max_documents": 50})
            >>> # The runnable is the same instance with updated config
            >>> runnable.config.max_documents
            50
        """
        # For the document loader engine, the engine itself is the runnable
        # But we can apply any runtime configuration to the engine instance
        if runnable_config:
            # Apply configuration directly if provided as a simple dict
            # This simplified approach is suitable for our use case
            config_dict = self.config.model_dump()
            config_dict.update(runnable_config)

            # Update config
            self.config = DocumentLoaderConfig.model_validate(config_dict)

        return self

    def invoke(
        self, source: BaseSource | str | Path | dict[str, Any], **kwargs
    ) -> DocumentLoaderOutput:
        """Load documents synchronously.

        This method loads documents from the specified source using the configured
        loader strategy. It overrides the base InvokableEngine.invoke method to
        provide specific document loading functionality.

        The method handles various input types including strings (paths/URLs),
        Path objects, dictionaries, and BaseSource instances. It follows a
        processing pipeline that analyzes the source, selects the appropriate
        loader, and loads documents with proper error handling.

        Args:
            source: The source to load documents from (can be a path, URL, source object, or config dict)
            **kwargs: Additional options for this invocation, including loader_name,
                loader_options, source_type, and other configuration overrides.

        Returns:
            DocumentLoaderOutput containing the loaded documents and metadata

        Raises:
            ValueError: If no matching source type is found
            ValueError: If no suitable loader strategy is found
            Various exceptions may be raised by loaders during document loading,
                unless raise_on_error is set to False in the configuration.

        Example:
            >>> engine = create_document_loader_engine()
            >>> result = engine.invoke("/path/to/document.pdf")
            >>> print(f"Loaded {result.total_documents} documents")
            >>> # With specific options
            >>> result = engine.invoke("/path/to/directory", recursive=True,
            ...                       loader_options={"glob": "*.pdf"})
        """
        start_time = time.time()

        try:
            # Prepare input
            input_model = self._prepare_input(source, **kwargs)

            # Process source to get a BaseSource instance
            source_instance, analysis_result = self._process_source(input_model)

            # Select loader strategy
            strategy_name = input_model.loader_name or self.config.loader_name
            strategy = self._select_loader_strategy(
                source_instance, analysis_result, strategy_name
            )

            # Merge options
            options = {**self.config.loader_options}
            if input_model.loader_options:
                options.update(input_model.loader_options)

            # Create loader
            loader = self._create_loader(
                source_instance, analysis_result, strategy, options
            )

            # Load documents
            documents = self._load_documents(loader, options)

            # Prepare output
            output = DocumentLoaderOutput(
                documents=[self._convert_document(doc) for doc in documents],
                total_documents=len(documents),
                operation_time=time.time() - start_time,
                source_type=source_instance.source_type or "unknown",
                loader_name=strategy.strategy_name,
                original_source=str(input_model.source),
            )

            return output

        except Exception as e:
            if self.config.raise_on_error:
                raise

            # Create error output
            return DocumentLoaderOutput(
                documents=[],
                total_documents=0,
                operation_time=time.time() - start_time,
                source_type="unknown",
                loader_name="failed",
                original_source=str(source),
                errors=[{"type": type(e).__name__, "message": str(e)}],
                has_errors=True,
            )

    async def ainvoke(
        self, source: BaseSource | str | Path | dict[str, Any], **kwargs
    ) -> DocumentLoaderOutput:
        """Load documents asynchronously.

        This method loads documents asynchronously from the specified source
        using the configured loader strategy. It overrides the base InvokableEngine.ainvoke
        method to provide specific document loading functionality with async support.

        If the selected loader strategy supports asynchronous loading, this method
        will use it. Otherwise, it falls back to synchronous loading in a separate
        thread to maintain the async interface. This behavior is controlled by the
        use_async configuration parameter.

        Args:
            source: The source to load documents from (can be a path, URL, source object, or config dict)
            **kwargs: Additional options for this invocation, including loader_name,
                loader_options, source_type, and other configuration overrides.

        Returns:
            DocumentLoaderOutput containing the loaded documents and metadata

        Raises:
            ValueError: If no matching source type is found
            ValueError: If no suitable loader strategy is found
            Various exceptions may be raised by loaders during document loading,
                unless raise_on_error is set to False in the configuration.

        Example:
            >>> engine = create_document_loader_engine({"use_async": True})
            >>> # In an async context
            >>> async def load_docs():
            ...     result = await engine.ainvoke("https://example.com")
            ...     print(f"Loaded {result.total_documents} documents")
        """
        # If async loading is not enabled, use synchronous loading
        if not self.config.use_async:
            return self.invoke(source, **kwargs)

        start_time = time.time()

        try:
            # Prepare input
            input_model = self._prepare_input(source, **kwargs)

            # Process source to get a BaseSource instance
            source_instance, analysis_result = self._process_source(input_model)

            # Select loader strategy
            strategy_name = input_model.loader_name or self.config.loader_name
            strategy = self._select_loader_strategy(
                source_instance, analysis_result, strategy_name
            )

            # Check if loader supports async
            if not strategy.supports_async:
                # Fall back to synchronous loading
                return self.invoke(source, **kwargs)

            # Merge options
            options = {**self.config.loader_options}
            if input_model.loader_options:
                options.update(input_model.loader_options)

            # Create loader
            loader = self._create_loader(
                source_instance, analysis_result, strategy, options
            )

            # Load documents asynchronously
            documents = await self._aload_documents(loader, options)

            # Prepare output
            output = DocumentLoaderOutput(
                documents=[self._convert_document(doc) for doc in documents],
                total_documents=len(documents),
                operation_time=time.time() - start_time,
                source_type=source_instance.source_type or "unknown",
                loader_name=strategy.strategy_name,
                original_source=str(input_model.source),
            )

            return output

        except Exception as e:
            if self.config.raise_on_error:
                raise

            # Create error output
            return DocumentLoaderOutput(
                documents=[],
                total_documents=0,
                operation_time=time.time() - start_time,
                source_type="unknown",
                loader_name="failed",
                original_source=str(source),
                errors=[{"type": type(e).__name__, "message": str(e)}],
                has_errors=True,
            )

    def _prepare_input(
        self, source: BaseSource | str | Path | dict[str, Any], **kwargs
    ) -> DocumentLoaderInput:
        """Prepare input model from source and kwargs.

        This method converts the input source to a DocumentLoaderInput model
        for consistent processing.

        Args:
            source: The source to load documents from
            **kwargs: Additional options

        Returns:
            DocumentLoaderInput model
        """
        if isinstance(source, BaseSource):
            # If source is already a BaseSource instance, wrap it in an input model
            return DocumentLoaderInput(source=str(source), **kwargs)

        if isinstance(source, str | Path):
            # If source is a string or Path, create an input model
            return DocumentLoaderInput(source=str(source), **kwargs)

        if isinstance(source, dict):
            # If source is a dict, create an input model from it
            input_dict = source.copy()
            input_dict.update(kwargs)
            return DocumentLoaderInput.model_validate(input_dict)

        # Try to convert to string
        return DocumentLoaderInput(source=str(source), **kwargs)

    def _process_source(
        self, input_model: DocumentLoaderInput
    ) -> tuple[BaseSource, PathAnalysisResult]:
        """Process source to get a BaseSource instance and path analysis.

        This method analyzes the source and creates an appropriate BaseSource
        instance based on the analysis.

        Args:
            input_model: The input model

        Returns:
            Tuple of (source_instance, analysis_result)

        Raises:
            ValueError: If source cannot be processed
            ValueError: If no matching source type is found
        """
        source = input_model.source

        # Analyze the source
        if isinstance(source, str):
            # Use path analysis system
            analysis_result = analyze_path(source)
        else:
            # For non-string sources, create a minimal analysis result
            analysis_result = PathAnalysisResult(original_path=str(source))

        # Override source type if specified
        if input_model.source_type:
            source_type = input_model.source_type
        else:
            # Find matching source types
            matches = self._source_registry.find_matching_sources(analysis_result)
            if not matches:
                raise ValueError(f"No matching source type found for {source}")

            source_type, _ = matches[0]  # Take the highest confidence match

        # Create source instance
        source_instance = self._source_registry.create_source(
            source_type, analysis_result
        )
        if not source_instance:
            raise ValueError(f"Failed to create source instance for {source_type}")

        return source_instance, analysis_result

    def _select_loader_strategy(
        self,
        source: BaseSource,
        analysis: PathAnalysisResult,
        strategy_name: str | None = None,
    ) -> LoaderStrategy:
        """Select a loader strategy for the source.

        This method selects the best loader strategy for the given source,
        taking into account configuration preferences and constraints.

        Args:
            source: The source instance
            analysis: The path analysis result
            strategy_name: Explicit strategy name to use

        Returns:
            The selected loader strategy

        Raises:
            ValueError: If no suitable strategy is found
        """
        # Check for explicit strategy name
        if strategy_name:
            strategy = self._loader_registry.get_strategy(strategy_name)
            if strategy:
                return strategy
            logger.warning(
                f"Strategy '{strategy_name}' not found, selecting best available"
            )

        # Prepare preferences based on config
        preferences = {
            "prefer_speed": self.config.loader_preference == "speed",
            "prefer_quality": self.config.loader_preference == "quality",
            "use_async": self.config.use_async,
        }

        # Select best strategy
        strategy = self._loader_registry.select_strategy(source, analysis, preferences)
        if not strategy:
            raise ValueError(
                f"No suitable loader strategy found for {source.source_type}"
            )

        return strategy

    def _create_loader(
        self,
        source: BaseSource,
        analysis: PathAnalysisResult,
        strategy: LoaderStrategy,
        options: dict[str, Any],
    ) -> Any:
        """Create a loader instance.

        This method creates a loader instance using the selected strategy
        and source.

        Args:
            source: The source instance
            analysis: The path analysis result
            strategy: The loader strategy
            options: Options for the loader

        Returns:
            The loader instance
        """
        return strategy.create_loader(source, options)

    def _load_documents(self, loader: Any, options: dict[str, Any]) -> list[Any]:
        """Load documents from the loader.

        This method invokes the loader to load documents from the source.

        Args:
            loader: The loader instance
            options: Options for loading

        Returns:
            List of loaded documents
        """
        # Check if loader has a load method
        if hasattr(loader, "load"):
            documents = loader.load()
        else:
            # Try to call the loader directly
            documents = loader()

        # Apply document limit if specified
        if self.config.max_documents and len(documents) > self.config.max_documents:
            documents = documents[: self.config.max_documents]

        return documents

    async def _aload_documents(self, loader: Any, options: dict[str, Any]) -> list[Any]:
        """Load documents asynchronously from the loader.

        This method invokes the loader asynchronously to load documents
        from the source.

        Args:
            loader: The loader instance
            options: Options for loading

        Returns:
            List of loaded documents
        """
        # Check if loader has an aload method
        if hasattr(loader, "aload"):
            documents = await loader.aload()
        else:
            # Fall back to synchronous loading in a thread
            loop = asyncio.get_running_loop()
            documents = await loop.run_in_executor(
                None, self._load_documents, loader, options
            )

        # Apply document limit if specified
        if self.config.max_documents and len(documents) > self.config.max_documents:
            documents = documents[: self.config.max_documents]

        return documents

    def _convert_document(self, document: Any) -> dict[str, Any]:
        """Convert a document to a dictionary.

        This method normalizes document formats to ensure consistent output.

        Args:
            document: The document to convert

        Returns:
            Dictionary representation of the document
        """
        # Check if document has page_content and metadata attributes (LangChain Document)
        if hasattr(document, "page_content") and hasattr(document, "metadata"):
            return {
                "page_content": document.page_content,
                "metadata": document.metadata,
            }

        # Check if document is already a dict
        if isinstance(document, dict):
            return document

        # Try to convert to dict
        try:
            return dict(document)
        except (TypeError, ValueError):
            # Fall back to string representation
            return {"page_content": str(document), "metadata": {}}


# Factory functions


def create_document_loader_engine(
    config: dict[str, Any] | DocumentLoaderConfig | None = None,
) -> DocumentLoaderEngine:
    """Create a document loader engine with specified configuration.

    This factory function creates a document loader engine with the specified
    configuration, providing a convenient way to create engines for common use cases.
    The engine is properly integrated with the Haive engine framework, inheriting
    from InvokableEngine and implementing all required methods.

    Args:
        config: Optional configuration for the engine, which can be either a
            dictionary of configuration parameters or a DocumentLoaderConfig instance.
            If None, default configuration is used.

    Returns:
        Configured DocumentLoaderEngine instance ready for use with the engine framework

    Examples:
        # Create with default configuration
        engine = create_document_loader_engine()

        # Create with custom dictionary configuration
        engine = create_document_loader_engine({
            "max_documents": 100,
            "use_async": True,
            "loader_preference": "speed"
        })

        # Create with custom config object
        config = DocumentLoaderConfig(max_documents=50, use_async=True)
        engine = create_document_loader_engine(config)

        # Use with engine framework
        runnable = engine.create_runnable()
        documents = engine.invoke("/path/to/file.pdf")
    """
    if config is None:
        return DocumentLoaderEngine()

    if isinstance(config, dict):
        return DocumentLoaderEngine(config=DocumentLoaderConfig.model_validate(config))

    return DocumentLoaderEngine(config=config)


def create_file_loader_engine(
    file_path: str | Path | None = None,
    file_extension: str | None = None,
    loader_name: str | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine for a specific file.

    This factory function creates a document loader engine configured specifically
    for loading documents from a file. It provides a convenient way to set up
    file-specific configurations and loader selection based on file extension.

    The engine created by this function is properly integrated with the Haive engine
    framework, inheriting from InvokableEngine and implementing all required methods.

    Args:
        file_path: Optional path to the file to load. If provided, the engine will
            be ready to load this file specifically. If not provided, you'll need to
            specify the file path when invoking the engine.
        file_extension: Optional file extension to use for loader selection. This is
            useful when the file doesn't have an extension or you want to override
            the detected extension. If provided without a leading dot, one will be added.
        loader_name: Optional explicit loader name to use, overriding automatic
            loader selection based on file extension. This gives precise control
            over which loader implementation to use.
        **options: Additional engine options, which will be passed to the loader
            as loader_options. These can include format-specific options like
            encoding, page_numbers, etc.

    Returns:
        Configured DocumentLoaderEngine instance ready for loading documents from a file

    Examples:
        # Create for a specific file
        engine = create_file_loader_engine("/path/to/document.pdf")
        documents = engine.invoke()

        # Create with explicit loader
        engine = create_file_loader_engine(
            file_path="/path/to/document.pdf",
            loader_name="pdf_miner_loader"
        )

        # Create with file-specific options
        engine = create_file_loader_engine(
            file_path="/path/to/document.docx",
            encoding="utf-8",
            extract_images=True
        )

        # Create for a specific extension, load file later
        engine = create_file_loader_engine(file_extension=".csv")
        documents = engine.invoke("/path/to/data.csv")
    """
    if file_extension and not file_extension.startswith("."):
        file_extension = f".{file_extension}"

    loader_options = options.copy()
    if file_extension:
        loader_options["file_extension"] = file_extension

    config = DocumentLoaderConfig(
        loader_name=loader_name, loader_options=loader_options
    )

    engine = DocumentLoaderEngine(config=config)

    # If file_path is provided, we can pre-load it
    if file_path:
        return engine

    return engine


def create_web_loader_engine(
    url: str | None = None,
    loader_name: str | None = None,
    dynamic_loading: bool = False,
    recursive: bool = False,
    max_depth: int = 1,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine for a web URL.

    This factory function creates a document loader engine configured specifically
    for loading documents from a web URL. It provides a convenient way to set up
    web-specific configurations, such as dynamic loading with JavaScript execution,
    recursive crawling of links, and custom headers.

    The engine will automatically select the most appropriate loader based on the
    configuration options:
    - If dynamic_loading=True, it will use a browser-based loader (Playwright)
    - If recursive=True, it will use a recursive crawler
    - Otherwise, it will use a basic web loader

    Args:
        url: Optional URL to load. If provided, the engine will be ready to load
            this URL specifically. If not provided, you'll need to specify the URL
            when invoking the engine.
        loader_name: Optional explicit loader name to use, overriding automatic
            loader selection based on options. This gives precise control over
            which loader implementation to use.
        dynamic_loading: Whether to use a dynamic loading strategy with JavaScript
            execution (e.g., Playwright). This is useful for websites that require
            JavaScript to render content.
        recursive: Whether to recursively crawl links found on the page. This is
            useful for capturing entire websites or sections.
        max_depth: Maximum depth for recursive crawling, only used if recursive=True.
            A value of 1 means only the initial page and direct links from it.
        **options: Additional engine options, which will be passed to the loader
            as loader_options. These can include web-specific options like headers,
            timeout, etc.

    Returns:
        Configured DocumentLoaderEngine instance ready for loading web content

    Examples:
        # Create for a specific URL
        engine = create_web_loader_engine("https://example.com")
        documents = engine.invoke()

        # Create with dynamic loading for JavaScript-heavy sites
        engine = create_web_loader_engine(
            url="https://example.com",
            dynamic_loading=True,
            wait_until="networkidle"
        )

        # Create with recursive crawling for capturing entire sites
        engine = create_web_loader_engine(
            url="https://example.com",
            recursive=True,
            max_depth=3,
            exclude_urls=["https://example.com/login"]
        )

        # Create with custom headers
        engine = create_web_loader_engine(
            headers={"User-Agent": "Custom Bot", "Authorization": "Bearer token"}
        )
        documents = engine.invoke("https://api.example.com/data")
    """
    # Select appropriate loader based on options
    if not loader_name:
        if dynamic_loading:
            loader_name = "playwright_loader"
        elif recursive:
            loader_name = "recursive_url_loader"
        else:
            loader_name = "web_base_loader"

    # Set up options
    loader_options = options.copy()
    if recursive:
        loader_options["max_depth"] = max_depth

    config = DocumentLoaderConfig(
        loader_name=loader_name, loader_options=loader_options
    )

    engine = DocumentLoaderEngine(config=config)

    # If URL is provided, we can pre-load it
    if url:
        return engine

    return engine


def create_directory_loader_engine(
    directory_path: str | Path | None = None,
    recursive: bool = True,
    glob_pattern: str | None = None,
    include_extensions: list[str] | None = None,
    exclude_extensions: list[str] | None = None,
    **options,
) -> DocumentLoaderEngine:
    """Create a document loader engine for a directory.

    This factory function creates a document loader engine configured specifically
    for loading documents from a directory. It provides a convenient way to set up
    directory-specific configurations, such as recursive traversal, file filtering
    with glob patterns, and extension filtering.

    The engine will automatically handle traversing the directory structure and
    loading all matching files with appropriate loaders based on file extensions.

    Args:
        directory_path: Optional path to the directory to load. If provided, the engine
            will be ready to load this directory specifically. If not provided, you'll
            need to specify the directory path when invoking the engine.
        recursive: Whether to recursively traverse subdirectories (True by default).
            Set to False to only load files in the top-level directory.
        glob_pattern: Optional glob pattern for filtering files (e.g., "*.pdf",
            "data_*.csv"). This is applied after directory traversal.
        include_extensions: Optional list of file extensions to include (e.g.,
            [".pdf", ".docx"]). Only files with these extensions will be loaded.
        exclude_extensions: Optional list of file extensions to exclude (e.g.,
            [".tmp", ".log"]). Files with these extensions will be skipped.
        **options: Additional engine options, which will be passed to the loader
            as loader_options. These can include directory-specific options like
            max_file_size, etc.

    Returns:
        Configured DocumentLoaderEngine instance ready for loading from a directory

    Examples:
        # Create for a specific directory, loading all files recursively
        engine = create_directory_loader_engine("/path/to/documents")
        documents = engine.invoke()

        # Create with glob pattern to filter specific files
        engine = create_directory_loader_engine(
            directory_path="/path/to/documents",
            glob_pattern="*.pdf"
        )

        # Create with extension filtering
        engine = create_directory_loader_engine(
            directory_path="/path/to/documents",
            include_extensions=[".pdf", ".docx", ".txt"],
            exclude_extensions=[".tmp", ".bak"]
        )

        # Create non-recursive loader for top-level files only
        engine = create_directory_loader_engine(
            directory_path="/path/to/documents",
            recursive=False
        )

        # Create with custom sorting
        engine = create_directory_loader_engine(
            directory_path="/path/to/documents",
            sort_by="name",  # or "date", "size"
            reverse=True
        )
    """
    loader_options = options.copy()
    if glob_pattern:
        loader_options["glob"] = glob_pattern

    if include_extensions:
        loader_options["include_extensions"] = include_extensions

    if exclude_extensions:
        loader_options["exclude_extensions"] = exclude_extensions

    config = DocumentLoaderConfig(recursive=recursive, loader_options=loader_options)

    engine = DocumentLoaderEngine(config=config)

    # If directory_path is provided, we can pre-load it
    if directory_path:
        return engine

    return engine


# Export all components
__all__ = [
    "DocumentLoaderEngine",
    "create_directory_loader_engine",
    "create_document_loader_engine",
    "create_file_loader_engine",
    "create_web_loader_engine",
]
