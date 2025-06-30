"""Loader Strategy System for Document Loader Engine

This module implements the loader strategy system for the document loader engine.
It provides classes for managing document loader strategies and factory methods
for creating loaders.
"""

from enum import Enum
import importlib
import logging
from typing import Any, Literal

from pydantic import BaseModel, Field

# Import from source implementation (placeholder for now)
from source_implementation import BaseSource, PathAnalysisResult


logger = logging.getLogger(__name__)


class LoaderPriority(str, Enum):
    """Priority levels for loader selection."""

    HIGHEST = "highest"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    LOWEST = "lowest"


class LoaderCapability(str, Enum):
    """Capabilities that loaders may support."""

    ASYNC = "async"
    METADATA = "metadata"
    CONTENT_EXTRACTION = "content_extraction"
    TEXT_EXTRACTION = "text_extraction"
    IMAGE_EXTRACTION = "image_extraction"
    TABLE_EXTRACTION = "table_extraction"
    STRUCTURE_PRESERVATION = "structure_preservation"
    LAZY_LOADING = "lazy_loading"
    PAGINATION = "pagination"
    CHUNKING = "chunking"
    FILTERING = "filtering"
    BATCHING = "batching"


class LoaderStrategy(BaseModel):
    """Information about a document loader strategy.

    This class represents a strategy for loading documents, including information
    about the loader class, its characteristics, and capabilities.
    """

    # Identification
    strategy_name: str = Field(..., description="Unique name for this loader strategy")

    # Loader class information
    loader_class: str = Field(..., description="Name of the loader class")

    module_path: str = Field(
        default="langchain_community.document_loaders",
        description="Import path for the loader module",
    )

    # Performance characteristics
    speed: Literal["fast", "medium", "slow"] = Field(
        default="medium", description="Relative speed of the loader"
    )

    quality: Literal["low", "medium", "high"] = Field(
        default="medium", description="Quality of document extraction"
    )

    resource_usage: Literal["low", "medium", "high"] = Field(
        default="medium", description="Resource consumption of the loader"
    )

    # Capabilities
    supports_async: bool = Field(
        default=False, description="Whether the loader supports async loading"
    )

    supports_metadata: bool = Field(
        default=True, description="Whether the loader extracts document metadata"
    )

    supports_batching: bool = Field(
        default=False, description="Whether the loader supports batch loading"
    )

    capabilities: list[LoaderCapability] = Field(
        default_factory=list, description="Special capabilities of this loader"
    )

    # Suitability indicators
    best_for: list[str] = Field(
        default_factory=list,
        description="Types of content this loader is best suited for",
    )

    priority: LoaderPriority = Field(
        default=LoaderPriority.MEDIUM,
        description="Priority of this loader when multiple are available",
    )

    # Constraints
    max_file_size: int | None = Field(
        default=None,
        description="Maximum file size in bytes this loader can handle efficiently",
    )

    # Authentication
    requires_auth: bool = Field(
        default=False, description="Whether this loader requires authentication"
    )

    required_credentials: list[str] = Field(
        default_factory=list, description="Credentials required by this loader"
    )

    # Options specification
    supported_options: dict[str, Any] = Field(
        default_factory=dict,
        description="Options supported by this loader with their default values",
    )

    def create_loader(self, source: BaseSource, options: dict[str, Any]) -> Any:
        """Create a loader instance for the given source.

        Args:
            source: The source to load documents from
            options: Options for the loader

        Returns:
            An instance of the loader

        Raises:
            ImportError: If the loader module cannot be imported
            ValueError: If the loader class cannot be found
            Exception: If the loader cannot be instantiated
        """
        try:
            # Import the module
            module = importlib.import_module(self.module_path)

            # Get the loader class
            loader_class = getattr(module, self.loader_class)

            # Prepare arguments based on source type
            init_args = self._prepare_loader_args(source, options)

            # Create the loader instance
            loader = loader_class(**init_args)

            return loader

        except ImportError as e:
            logger.error(f"Failed to import loader module {self.module_path}: {e}")
            raise ImportError(f"Loader module not found: {self.module_path}") from e

        except AttributeError as e:
            logger.error(
                f"Failed to find loader class {self.loader_class} in module {self.module_path}: {e}"
            )
            raise ValueError(f"Loader class not found: {self.loader_class}") from e

        except Exception as e:
            logger.error(f"Failed to create loader instance: {e}")
            raise

    def calculate_suitability(
        self, analysis: PathAnalysisResult, preferences: dict[str, Any]
    ) -> float:
        """Calculate the suitability score of this loader for the given source.

        Args:
            analysis: The path analysis result
            preferences: User preferences for loader selection

        Returns:
            A suitability score between 0.0 and 1.0
        """
        score = 0.5  # Base score

        # Priority boost
        if self.priority == LoaderPriority.HIGHEST:
            score += 0.3
        elif self.priority == LoaderPriority.HIGH:
            score += 0.2
        elif self.priority == LoaderPriority.LOW:
            score -= 0.1
        elif self.priority == LoaderPriority.LOWEST:
            score -= 0.2

        # Speed preference
        if preferences.get("prefer_speed", False):
            if self.speed == "fast":
                score += 0.2
            elif self.speed == "slow":
                score -= 0.2

        # Quality preference
        if preferences.get("prefer_quality", False):
            if self.quality == "high":
                score += 0.2
            elif self.quality == "low":
                score -= 0.2

        # File size considerations
        if hasattr(analysis, "file_size") and self.max_file_size and analysis.file_size:
            if analysis.file_size > self.max_file_size:
                score -= 0.3
            elif analysis.file_size < self.max_file_size / 2:
                score += 0.1

        # Async preference
        if preferences.get("use_async", False) and not self.supports_async:
            score -= 0.1

        # Batch preference
        if preferences.get("use_batching", False) and not self.supports_batching:
            score -= 0.1

        # Best for conditions - check if file category matches best_for
        if hasattr(analysis, "file_category") and analysis.file_category:
            file_category = str(analysis.file_category).lower()
            if any(bf.lower() in file_category for bf in self.best_for):
                score += 0.3

        # Normalize score to [0, 1] range
        return max(0.0, min(1.0, score))

    def check_authentication(self, credential_provider: Any) -> bool:
        """Check if required credentials are available.

        Args:
            credential_provider: Provider for retrieving credentials

        Returns:
            True if all required credentials are available, False otherwise
        """
        if not self.requires_auth:
            return True

        if not credential_provider:
            return False

        for cred_name in self.required_credentials:
            if not credential_provider.get_credential(cred_name):
                return False

        return True

    def _prepare_loader_args(
        self, source: BaseSource, options: dict[str, Any]
    ) -> dict[str, Any]:
        """Prepare arguments for the loader constructor based on source type.

        Args:
            source: The source to load documents from
            options: Additional options for the loader

        Returns:
            Dictionary of arguments for the loader constructor
        """
        args = {}

        # Add source-specific arguments
        if hasattr(source, "file_path") and source.file_path:
            args["file_path"] = str(source.file_path)

        if hasattr(source, "directory_path") and source.directory_path:
            args["directory_path"] = str(source.directory_path)

        if hasattr(source, "url") and source.url:
            args["url"] = str(source.url)

        if hasattr(source, "connection_string") and source.connection_string:
            args["connection_string"] = source.connection_string

        if hasattr(source, "bucket_name") and source.bucket_name:
            args["bucket_name"] = source.bucket_name

        if hasattr(source, "object_key") and source.object_key:
            args["object_key"] = source.object_key

        # Add all options
        args.update(options)

        return args


class LoaderRegistry:
    """Registry for document loader strategies.

    This registry maintains a collection of loader strategies and provides
    methods for selecting appropriate loaders for different sources.
    """

    _instance = None

    def __init__(self):
        """Initialize the registry."""
        self.strategies: dict[str, LoaderStrategy] = {}
        self.strategy_by_source: dict[str, list[str]] = {}
        self.strategy_by_extension: dict[str, list[str]] = {}

    @classmethod
    def get_instance(cls) -> "LoaderRegistry":
        """Get the singleton instance of the registry."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def register_strategy(
        self,
        strategy: LoaderStrategy,
        source_types: list[str] = None,
        file_extensions: list[str] = None,
    ) -> None:
        """Register a loader strategy.

        Args:
            strategy: The loader strategy to register
            source_types: List of source types this strategy can handle
            file_extensions: List of file extensions this strategy can handle
        """
        strategy_name = strategy.strategy_name

        # Register the strategy
        self.strategies[strategy_name] = strategy

        # Register for source types
        if source_types:
            for source_type in source_types:
                if source_type not in self.strategy_by_source:
                    self.strategy_by_source[source_type] = []
                if strategy_name not in self.strategy_by_source[source_type]:
                    self.strategy_by_source[source_type].append(strategy_name)

        # Register for file extensions
        if file_extensions:
            for ext in file_extensions:
                if not ext.startswith("."):
                    ext = f".{ext}"
                if ext not in self.strategy_by_extension:
                    self.strategy_by_extension[ext] = []
                if strategy_name not in self.strategy_by_extension[ext]:
                    self.strategy_by_extension[ext].append(strategy_name)

    def get_strategy(self, strategy_name: str) -> LoaderStrategy | None:
        """Get a strategy by name.

        Args:
            strategy_name: The name of the strategy

        Returns:
            The loader strategy, or None if not found
        """
        return self.strategies.get(strategy_name)

    def get_strategies_for_source(self, source_type: str) -> list[LoaderStrategy]:
        """Get all strategies for a source type.

        Args:
            source_type: The source type

        Returns:
            List of loader strategies for the source type
        """
        strategy_names = self.strategy_by_source.get(source_type, [])
        return [
            self.strategies[name] for name in strategy_names if name in self.strategies
        ]

    def get_strategies_for_extension(self, extension: str) -> list[LoaderStrategy]:
        """Get all strategies for a file extension.

        Args:
            extension: The file extension (with or without leading dot)

        Returns:
            List of loader strategies for the extension
        """
        if not extension.startswith("."):
            extension = f".{extension}"

        strategy_names = self.strategy_by_extension.get(extension, [])
        return [
            self.strategies[name] for name in strategy_names if name in self.strategies
        ]

    def select_strategy(
        self,
        source: BaseSource,
        analysis: PathAnalysisResult,
        preferences: dict[str, Any] = None,
    ) -> LoaderStrategy | None:
        """Select the best loader strategy for a source.

        Args:
            source: The source to load documents from
            analysis: The path analysis result
            preferences: User preferences for loader selection

        Returns:
            The best loader strategy, or None if no suitable strategy is found
        """
        preferences = preferences or {}
        source_type = getattr(source, "source_type", None)

        # Get candidate strategies
        candidates = []

        # Try source type first
        if source_type and source_type in self.strategy_by_source:
            candidates.extend(self.get_strategies_for_source(source_type))

        # Try file extension
        if hasattr(analysis, "file_extension") and analysis.file_extension:
            candidates.extend(
                self.get_strategies_for_extension(analysis.file_extension)
            )

        # If no candidates found, return None
        if not candidates:
            return None

        # Calculate suitability scores
        scored_candidates = [
            (strategy, strategy.calculate_suitability(analysis, preferences))
            for strategy in candidates
        ]

        # Sort by score (descending)
        scored_candidates.sort(key=lambda x: x[1], reverse=True)

        # Return the best strategy
        if scored_candidates:
            return scored_candidates[0][0]

        return None


# Singleton instance
loader_registry = LoaderRegistry.get_instance()


# Factory functions


def create_loader(
    source: BaseSource,
    analysis: PathAnalysisResult,
    strategy_name: str | None = None,
    options: dict[str, Any] = None,
    preferences: dict[str, Any] = None,
) -> Any:
    """Create a loader for a source.

    Args:
        source: The source to load documents from
        analysis: The path analysis result
        strategy_name: Explicit strategy name to use (if not provided, best strategy is selected)
        options: Options for the loader
        preferences: Preferences for loader selection

    Returns:
        A loader instance

    Raises:
        ValueError: If no suitable loader strategy is found
    """
    options = options or {}
    preferences = preferences or {}

    # Get the strategy
    strategy = None
    if strategy_name:
        strategy = loader_registry.get_strategy(strategy_name)
        if not strategy:
            logger.warning(
                f"Strategy '{strategy_name}' not found, selecting best available"
            )

    if not strategy:
        strategy = loader_registry.select_strategy(source, analysis, preferences)

    if not strategy:
        raise ValueError(f"No suitable loader strategy found for source: {source}")

    # Create the loader
    return strategy.create_loader(source, options)


def register_langchain_loaders():
    """Register standard langchain document loaders."""
    # PDF loaders
    loader_registry.register_strategy(
        LoaderStrategy(
            strategy_name="pypdf_loader",
            loader_class="PyPDFLoader",
            speed="fast",
            quality="medium",
            best_for=["pdf", "text_heavy"],
            priority=LoaderPriority.HIGH,
        ),
        source_types=["pdf"],
        file_extensions=[".pdf"],
    )

    loader_registry.register_strategy(
        LoaderStrategy(
            strategy_name="unstructured_pdf_loader",
            loader_class="UnstructuredPDFLoader",
            speed="medium",
            quality="high",
            best_for=["pdf", "scanned", "images"],
            priority=LoaderPriority.MEDIUM,
        ),
        source_types=["pdf"],
        file_extensions=[".pdf"],
    )

    # Text loaders
    loader_registry.register_strategy(
        LoaderStrategy(
            strategy_name="text_loader",
            loader_class="TextLoader",
            speed="fast",
            quality="medium",
            best_for=["text", "plain_text"],
            priority=LoaderPriority.HIGH,
        ),
        source_types=["text"],
        file_extensions=[".txt", ".text", ".log"],
    )

    # CSV loaders
    loader_registry.register_strategy(
        LoaderStrategy(
            strategy_name="csv_loader",
            loader_class="CSVLoader",
            speed="fast",
            quality="medium",
            best_for=["csv", "tabular"],
            priority=LoaderPriority.HIGH,
        ),
        source_types=["csv"],
        file_extensions=[".csv"],
    )

    # Web loaders
    loader_registry.register_strategy(
        LoaderStrategy(
            strategy_name="web_base_loader",
            loader_class="WebBaseLoader",
            module_path="langchain_community.document_loaders.web_base",
            speed="fast",
            quality="medium",
            best_for=["web", "html"],
            priority=LoaderPriority.HIGH,
        ),
        source_types=["web", "html", "url"],
        file_extensions=[".html", ".htm"],
    )

    # More loaders can be added here


# Export all components
__all__ = [
    "LoaderCapability",
    "LoaderPriority",
    "LoaderRegistry",
    "LoaderStrategy",
    "create_loader",
    "loader_registry",
    "register_langchain_loaders",
]
