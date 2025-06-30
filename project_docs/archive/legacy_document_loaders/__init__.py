"""Document Loader Engine System

This package provides a comprehensive document loader engine system for Haive.
It integrates with the engine framework to provide a unified interface for
loading documents from various sources.

Key components:
- DocumentLoaderEngine: The main engine for loading documents
- Source type registry: Registry for document source types
- Loader strategy system: System for managing document loader strategies
- Path analysis system: System for analyzing paths and URLs
- Factory methods: Convenience methods for creating engines

Example usage:

```python
from haive.core.engine.document import (
    create_file_loader_engine,
    create_web_loader_engine,
    create_directory_loader_engine
)

# Load a PDF file
pdf_engine = create_file_loader_engine("document.pdf")
documents = pdf_engine.invoke("document.pdf")

# Load a web page
web_engine = create_web_loader_engine("https://example.com")
documents = web_engine.invoke("https://example.com")

# Load a directory of files
dir_engine = create_directory_loader_engine("/path/to/documents", recursive=True)
documents = dir_engine.invoke("/path/to/documents")
```
"""

from .engine import DocumentLoaderEngine

# Import core components
from .engine_config import (
    DocumentLoaderConfig,
    DocumentLoaderInput,
    DocumentLoaderOutput,
    DocumentMetadata,
    EngineType,
)

# Import factory methods
from .factory import (
    create_cloud_loader_engine,
    create_database_loader_engine,
    create_directory_loader_engine,
    create_document_loader_engine,
    create_file_loader_engine,
    create_web_loader_engine,
)

# Import loader components
from .loader_strategy import (
    LoaderCapability,
    LoaderPriority,
    LoaderRegistry,
    LoaderStrategy,
    loader_registry,
)

# Import path analysis
from .path_integration import (
    CloudProvider,
    DatabaseType,
    FileCategory,
    PathAnalysisResult,
    PathType,
    analyze_and_resolve_source,
    analyze_source,
)

# Import source components
from .source_implementation import (
    BaseSource,
    CloudSource,
    DatabaseSource,
    LoaderStrategy,
    LocalSource,
    RemoteSource,
    SourceMetadata,
    SourcePattern,
)

# Import source-to-loader mapping
from .source_loader_mapping import (
    get_best_loader_for_path,
    get_loader_for_source,
    get_loaders_for_file_extension,
    initialize_registries,
)
from .source_registry import SourceTypeRegistry, auto_source, registry


# Export components
__all__ = [
    # Engine components
    "EngineType",
    "DocumentLoaderConfig",
    "DocumentLoaderInput",
    "DocumentLoaderOutput",
    "DocumentMetadata",
    "DocumentLoaderEngine",
    # Source components
    "BaseSource",
    "LocalSource",
    "RemoteSource",
    "DatabaseSource",
    "CloudSource",
    "SourcePattern",
    "SourceMetadata",
    "SourceTypeRegistry",
    "registry",
    "auto_source",
    # Loader components
    "LoaderPriority",
    "LoaderCapability",
    "LoaderStrategy",
    "LoaderRegistry",
    "loader_registry",
    # Path analysis
    "PathType",
    "FileCategory",
    "DatabaseType",
    "CloudProvider",
    "PathAnalysisResult",
    "analyze_source",
    "analyze_and_resolve_source",
    # Factory methods
    "create_document_loader_engine",
    "create_file_loader_engine",
    "create_web_loader_engine",
    "create_directory_loader_engine",
    "create_database_loader_engine",
    "create_cloud_loader_engine",
    # Source-to-loader mapping
    "initialize_registries",
    "get_loader_for_source",
    "get_loaders_for_file_extension",
    "get_best_loader_for_path",
]

# Initialize registries
initialize_registries()
