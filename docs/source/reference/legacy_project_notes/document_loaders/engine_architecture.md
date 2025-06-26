# Document Loader Engine Architecture

## Overview

This document describes the architecture for integrating the document loader system with Haive's engine framework. The system will transform the existing document loader designs into an engine-based architecture that follows the patterns established in the haive-core package.

## Architecture Goals

1. Implement the document loader as an `InvokableEngine` subclass
2. Maintain the flexible source detection and loader selection capabilities
3. Follow the engine patterns used in other haive-core components
4. Provide clean interfaces for extension and customization
5. Support both synchronous and asynchronous operations

## Core Components

### 1. DocumentLoaderEngine

The central component is the `DocumentLoaderEngine` class that implements the `InvokableEngine` interface:

```python
class DocumentLoaderEngine(InvokableEngine[Union[BaseSource, str, Path, Dict[str, Any]], List[Document]]):
    """
    Engine for loading documents from various sources.

    This engine provides a unified interface for working with document loaders from
    langchain_community, with support for different source types and configurations.
    """

    # Engine type
    engine_type: EngineType = Field(default=EngineType.DOCUMENT_LOADER)

    # Source settings
    source_type: Optional[str] = Field(
        default=None,
        description="Explicit source type to use (auto-detected if not provided)"
    )

    # Loader settings
    loader_name: Optional[str] = Field(
        default=None,
        description="Name of the document loader to use (auto-detected if not provided)"
    )

    # Loading options
    recursive: bool = Field(
        default=True, description="Whether to recursively load from directory sources"
    )
    max_documents: Optional[int] = Field(
        default=None,
        description="Maximum number of documents to load (None for unlimited)"
    )
    use_async: bool = Field(
        default=False, description="Whether to use async loading if available"
    )

    # Additional configuration
    loader_options: Dict[str, Any] = Field(
        default_factory=dict,
        description="Configuration parameters for the loader"
    )

    # Invocation methods
    def invoke(self, source: Union[BaseSource, str, Path, Dict[str, Any]], **kwargs) -> List[Document]:
        """Load documents synchronously."""
        pass

    async def ainvoke(self, source: Union[BaseSource, str, Path, Dict[str, Any]], **kwargs) -> List[Document]:
        """Load documents asynchronously."""
        pass
```

### 2. Path Analysis System

The path analysis system will be implemented as a standalone component within the engine system:

```python
class PathAnalyzer:
    """
    Analyzes paths and URLs to determine their nature and properties.
    """

    @staticmethod
    def analyze(path: Union[str, Path]) -> PathAnalysisResult:
        """Analyze a path to determine its type, properties, and metadata."""
        pass

    @staticmethod
    def detect_mime_type(file_path: str) -> Optional[str]:
        """Detect the MIME type of a file."""
        pass
```

### 3. Source Type Registry

The source type registry is responsible for managing source types and their mappings:

```python
class SourceTypeRegistry:
    """
    Registry for document source types.

    This registry maintains a mapping of source types to their metadata,
    and provides methods for finding the appropriate source type for a given input.
    """

    @classmethod
    def get_instance(cls) -> 'SourceTypeRegistry':
        """Get the singleton instance of the registry."""
        pass

    def register(self, source_class: Type[BaseSource]) -> None:
        """Register a source type."""
        pass

    def find_matching_sources(self, analysis: PathAnalysisResult) -> List[Tuple[str, float]]:
        """Find source types that match the analysis with confidence scores."""
        pass

    def create_source(self, source_type: str, analysis: PathAnalysisResult) -> BaseSource:
        """Create an instance of the specified source type."""
        pass
```

### 4. Loader Strategy System

The loader strategy system manages the available loader implementations:

```python
class LoaderStrategy(BaseModel):
    """
    Information about a document loader strategy.
    """

    strategy_name: str
    loader_class: str
    module_path: str = "langchain_community.document_loaders"

    # Performance characteristics
    speed: Literal["fast", "medium", "slow"] = "medium"
    quality: Literal["low", "medium", "high"] = "medium"
    resource_usage: Literal["low", "medium", "high"] = "medium"

    # Capabilities
    supports_async: bool = False
    supports_metadata: bool = True

    # Suitability
    best_for: List[str] = Field(default_factory=list)
    max_file_size: Optional[int] = None

    def create_loader(self, source: BaseSource, options: Dict[str, Any]) -> Any:
        """Create a loader instance for the given source."""
        pass
```

## Integration with Engine Framework

The document loader engine will integrate with the broader Haive engine framework:

1. **Registration**: The engine will auto-register with the engine registry
2. **Configuration**: The engine will support configuration through the standard engine configuration system
3. **Input/Output Schema**: The engine will define its input and output schemas for validation
4. **State Tracking**: The engine will support state tracking for long-running operations

## Factory Methods

For ease of use, we'll provide factory methods to create engines for common use cases:

```python
def create_file_loader_engine(
    file_path: Union[str, Path],
    loader_name: Optional[str] = None,
    **options
) -> DocumentLoaderEngine:
    """Create a document loader engine for a specific file."""
    pass

def create_web_loader_engine(
    url: str,
    loader_name: Optional[str] = None,
    **options
) -> DocumentLoaderEngine:
    """Create a document loader engine for a web URL."""
    pass

def create_directory_loader_engine(
    directory_path: Union[str, Path],
    recursive: bool = True,
    glob_pattern: Optional[str] = None,
    **options
) -> DocumentLoaderEngine:
    """Create a document loader engine for a directory."""
    pass
```

## Workflow

The typical workflow for using the document loader engine is:

1. Create engine instance (using factory methods or direct instantiation)
2. Configure the engine with any specific options
3. Invoke the engine with a source (path, URL, etc.)
4. Process the returned documents

Example usage:

```python
# Create engine for a specific file type
pdf_engine = create_file_loader_engine("document.pdf", strategy="ocr")

# Load documents
documents = pdf_engine.invoke("path/to/document.pdf")

# Process documents
for doc in documents:
    print(f"Content: {doc.page_content[:100]}...")
    print(f"Metadata: {doc.metadata}")
```

## Future Extensions

The architecture is designed to support future extensions:

1. **Document Transformers**: Add transformers for post-processing documents
2. **Document Splitters**: Integrate with text splitters for chunking
3. **Custom Loaders**: Allow for registration of custom loaders
4. **Caching**: Add document caching for performance optimization
5. **Batch Processing**: Support batch processing of multiple sources

## Implementation Plan

1. Implement the path analysis system
2. Create the source type system with base classes
3. Implement the source type registry
4. Build the loader strategy system
5. Create the DocumentLoaderEngine class
6. Implement factory methods and utilities
7. Add documentation and examples
