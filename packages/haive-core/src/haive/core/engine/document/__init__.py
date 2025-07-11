"""Enhanced Document Engine Package.

This package provides comprehensive document processing capabilities including:
- Document loading from various sources (files, URLs, databases, cloud storage)
- Advanced chunking and processing strategies
- Path analysis and source type detection
- Parallel processing and error handling
- Integration with the Haive engine framework

Key Components:
- DocumentEngine: Main engine for document processing
- DocumentEngineConfig: Configuration model for the engine
- Path analysis system for source type detection
- Document loaders for various source types
- Processing strategies for chunking and transformation
"""

# Configuration models
from haive.core.engine.document.config import (
    ChunkingStrategy,
    DocumentChunk,
    DocumentEngineConfig,
    DocumentFormat,
    DocumentInput,
    DocumentOutput,
    DocumentSourceType,
    LoaderPreference,
    ProcessedDocument,
    ProcessingStrategy,
)

# Core engine components
from haive.core.engine.document.engine import (
    DocumentEngine,
    create_directory_document_engine,
    create_file_document_engine,
    create_web_document_engine,
)

# Loader components
from haive.core.engine.document.loaders.base.base import (
    BaseDocumentLoader,
    SimpleDocumentLoader,
    TextDocumentLoader,
)
from haive.core.engine.document.loaders.registry import (
    DocumentLoaderRegistry,
    create_loader,
    get_default_registry,
    get_loader,
    register_loader,
)

# Path analysis
from haive.core.engine.document.path_analysis import (
    CloudProvider,
    DatabaseType,
    FileCategory,
    PathAnalysisResult,
    PathType,
    analyze_path_comprehensive,
)


# Factory functions for convenience
def create_document_engine(name: str = "document_engine", **kwargs) -> DocumentEngine:
    """Create a basic document engine with default configuration.

    Args:
        name: Name for the engine instance
        **kwargs: Additional configuration options

    Returns:
        Configured DocumentEngine instance
    """
    config = DocumentEngineConfig(name=name, **kwargs)
    return DocumentEngine(config=config)


def load_documents(
    source,
    chunking_strategy: ChunkingStrategy = ChunkingStrategy.RECURSIVE,
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    **kwargs
) -> DocumentOutput:
    """Quick function to load and process documents.

    Args:
        source: Source to load from (path, URL, etc.)
        chunking_strategy: Strategy for chunking documents
        chunk_size: Size of chunks in characters
        chunk_overlap: Overlap between chunks
        **kwargs: Additional processing options

    Returns:
        DocumentOutput with processed documents
    """
    engine = create_document_engine(
        chunking_strategy=chunking_strategy,
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        **kwargs
    )

    return engine.invoke(source)


# Agents (conditional import - only if agents package available)
try:
    from haive.core.engine.document.agents import (
        DirectoryDocumentAgent,
        DocumentAgent,
        FileDocumentAgent,
        WebDocumentAgent,
    )
except ImportError:
    # Agents not available - they depend on haive-agents package
    DirectoryDocumentAgent = None
    DocumentAgent = None
    FileDocumentAgent = None
    WebDocumentAgent = None

# Factory and enhanced loaders
from haive.core.engine.document.factory import (
    AutoLoaderFactory,
    analyze_source,
    create_document_loader,
)
from haive.core.engine.document.loaders.sources.implementation import (
    CredentialManager,
    EnhancedSource,
)
from haive.core.engine.document.loaders.sources.implementation import (
    SourceType as EnhancedSourceType,
)
from haive.core.engine.document.loaders.sources.implementation import (
    source_registry,
)

# Specific loader implementations - only import what exists
from haive.core.engine.document.loaders.specific import (  # Database sources
    MongoDBSource,
    PostgreSQLSource,
)
from haive.core.engine.document.loaders.strategy import (
    LoaderCapability,
    LoaderPriority,
    LoaderStrategy,
    strategy_registry,
)

# Processors
from haive.core.engine.document.processors import (
    ChunkingProcessor,
    ContentNormalizer,
    DocumentProcessor,
    FormatDetector,
    MetadataExtractor,
)

# Universal loader system - temporarily commented out until dependencies are fixed
# from .universal_loader import (
#     UniversalDocumentLoader,
#     SmartSourceRegistry,
#     load_document,
#     analyze_document_source,
# )


# Export all public components
__all__ = [
    # Core engine
    "DocumentEngine",
    "create_document_engine",
    "load_documents",
    # Factory functions
    "create_file_document_engine",
    "create_web_document_engine",
    "create_directory_document_engine",
    # Configuration
    "DocumentEngineConfig",
    "DocumentInput",
    "DocumentOutput",
    "ProcessedDocument",
    "DocumentChunk",
    # Enums
    "DocumentFormat",
    "DocumentSourceType",
    "LoaderPreference",
    "ProcessingStrategy",
    "ChunkingStrategy",
    # Path analysis
    "analyze_path_comprehensive",
    "PathAnalysisResult",
    "PathType",
    "FileCategory",
    "DatabaseType",
    "CloudProvider",
    # Loaders
    "BaseDocumentLoader",
    "SimpleDocumentLoader",
    "TextDocumentLoader",
    # Registry
    "DocumentLoaderRegistry",
    "get_default_registry",
    "register_loader",
    "get_loader",
    "create_loader",
    # Agents
    "DocumentAgent",
    "FileDocumentAgent",
    "WebDocumentAgent",
    "DirectoryDocumentAgent",
    # Processors
    "DocumentProcessor",
    "ChunkingProcessor",
    "ContentNormalizer",
    "FormatDetector",
    "MetadataExtractor",
    # Factory and enhanced loaders
    "AutoLoaderFactory",
    "create_document_loader",
    "analyze_source",
    # Universal loader system - commented out temporarily
    # "UniversalDocumentLoader",
    # "SmartSourceRegistry",
    # "load_document",
    # "analyze_document_source",
    # Enhanced source system
    "EnhancedSourceType",
    "CredentialManager",
    "EnhancedSource",
    "source_registry",
    # Strategy system
    "LoaderStrategy",
    "LoaderCapability",
    "LoaderPriority",
    "strategy_registry",
    # Specific loader implementations - only what exists
    # Database sources
    "MongoDBSource",
    "PostgreSQLSource",
]
