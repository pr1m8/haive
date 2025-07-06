# Document Loader Architecture

## 🏗️ System Architecture Overview

The document loader system implements a clean, extensible architecture for loading documents from 230+ different sources.

## Core Architecture Pattern

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              User Interface                               │
│                                                                           │
│  AutoLoader API:  load() | load_documents() | load_bulk() | load_all()  │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                           Path Analysis Layer                             │
│                                                                           │
│  PathAnalyzer: Detects source type from paths/URLs/connection strings    │
│  SourceInfo: Contains detection results and metadata                     │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Registry Layer                                 │
│                                                                           │
│  EnhancedRegistry: Maps source types to available loaders               │
│  LoaderPreference: Speed/Quality/Balanced selection                      │
│  @register_source: Decorator for easy registration                       │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Source Layer                                   │
│                                                                           │
│  BaseSource: Abstract base for all sources                              │
│  SecureConfigMixin: Credential management                                │
│  Source implementations: PDFSource, WebSource, DatabaseSource, etc.      │
└─────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                            Loader Layer                                   │
│                                                                           │
│  langchain_community loaders: PyPDFLoader, CSVLoader, etc.              │
│  Standard methods: load(), load_documents(), load_and_split()           │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. AutoLoader (Primary Interface)

**Purpose**: Provide a unified interface for loading documents from any source.

**Key Methods**:

```python
class AutoLoader:
    def load(self, path_or_url: str, **kwargs) -> List[Document]
    def load_documents(self, sources: List[Union[str, Dict]], **kwargs) -> List[Document]
    def load_bulk(self, sources: List[Union[str, Dict]], **kwargs) -> BulkLoadingResult
    def load_all(self, path_or_url: str, **kwargs) -> List[Document]
    async def aload(self, path_or_url: str, **kwargs) -> List[Document]
    async def aload_documents(self, sources: List[Union[str, Dict]], **kwargs) -> List[Document]
```

**Configuration**:

```python
class AutoLoaderConfig(BaseModel):
    preference: LoaderPreference = LoaderPreference.BALANCED
    max_concurrency: int = 10
    timeout: int = 300
    retry_attempts: int = 3
    enable_caching: bool = False
    enable_metadata: bool = True
```

### 2. PathAnalyzer

**Purpose**: Automatically detect source types from paths, URLs, or connection strings.

**Detection Logic**:

- Local files: Check file extension and existence
- URLs: Parse protocol and domain
- Databases: Identify connection string patterns
- Cloud storage: Recognize S3, GCS, Azure patterns
- APIs: Detect API endpoints

**Output**:

```python
class SourceInfo(BaseModel):
    source_type: str  # "pdf", "web", "postgresql", etc.
    category: SourceCategory  # FILE_DOCUMENT, WEB_SCRAPING, etc.
    confidence: float  # 0.0 to 1.0
    metadata: Dict[str, Any]  # Additional detection info
    capabilities: Optional[List[LoaderCapability]]
```

### 3. Enhanced Registry

**Purpose**: Manage the mapping between source types and available loaders.

**Features**:

- Multiple loaders per source type
- Preference-based selection (Speed/Quality/Balanced)
- Dynamic registration with decorators
- Capability-based filtering

**Registration**:

```python
@register_source(
    source_type="pdf",
    loader_class=PyPDFLoader,
    name="pypdf",
    capabilities=[LoaderCapability.TEXT_EXTRACTION, LoaderCapability.METADATA_EXTRACTION],
    preference=LoaderPreference.BALANCED
)
class PDFSource(BaseSource, SecureConfigMixin):
    source_type: str = "pdf"
    # ... source implementation
```

### 4. Source Abstraction

**Purpose**: Provide a consistent interface for all document sources.

**Base Classes**:

```python
class BaseSource(BaseModel):
    source_type: str
    source_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    category: SourceCategory
    capabilities: SourceCapabilities

    @abstractmethod
    def get_loader_kwargs(self) -> Dict[str, Any]:
        """Get kwargs for loader instantiation."""
        pass

class SecureConfigMixin(BaseModel):
    """Mixin for secure credential management."""
    provider: str = Field(description="Provider name")
    api_key: Optional[str] = Field(default=None, description="API key")
    # ... other credential fields
```

**Source Categories**:

- FILE_DOCUMENT: Local files (PDF, DOCX, CSV, etc.)
- WEB_SCRAPING: Websites and web APIs
- DATABASE_SQL: SQL databases
- DATABASE_NOSQL: NoSQL databases
- CLOUD_STORAGE: S3, GCS, Azure, etc.
- MESSAGING: Slack, Discord, Teams
- BUSINESS_PLATFORMS: Salesforce, HubSpot, etc.
- And more...

### 5. Loader Integration

**Purpose**: Wrap langchain_community loaders with consistent interface.

**Standard Methods**:

1. `load_documents()` - New standard (plural)
2. `load()` - Classic method
3. `load_and_split()` - With text splitting
4. `lazy_load()` - Iterator for large files

**Enhanced Loading**:

```python
def _load_with_retry(self, loader_instance: Any, source_type: str) -> List[Document]:
    """Try multiple loading methods with retry logic."""
    # 1. Try load_documents() first (standard langchain plural)
    # 2. Fall back to load() (standard langchain singular)
    # 3. Finally try load_and_split() for splitting loaders
```

## Design Principles

### 1. Separation of Concerns

- **Sources**: Know about source-specific details
- **Loaders**: Handle actual document extraction
- **Registry**: Manages mappings and selection
- **AutoLoader**: Provides unified interface

### 2. Extensibility

- Add new sources via `@register_source` decorator
- Implement BaseSource for custom sources
- Register multiple loaders per source type
- Plugin architecture for future extensions

### 3. Type Safety

- All models use Pydantic BaseModel
- Field validation and constraints
- Type hints throughout
- Runtime validation

### 4. Security

- SecureConfigMixin for credential management
- No hardcoded secrets
- Environment variable support
- Secure credential passing

### 5. Performance

- Concurrent loading with ThreadPoolExecutor
- Async support for I/O operations
- Caching layer for repeated loads
- Lazy loading for large files

## Data Flow

```
1. User Input
   └─> "s3://bucket/document.pdf"

2. Path Analysis
   └─> SourceInfo(source_type="s3", category=CLOUD_STORAGE, ...)

3. Registry Lookup
   └─> Available loaders: [S3FileLoader, S3DirectoryLoader]
   └─> Selected: S3FileLoader (based on preference)

4. Source Creation
   └─> S3Source(bucket="bucket", key="document.pdf", ...)

5. Loader Instantiation
   └─> S3FileLoader(bucket="bucket", key="document.pdf", ...)

6. Document Loading
   └─> loader.load() -> List[Document]

7. Result Enhancement
   └─> Add metadata, cache results, return to user
```

## Extension Points

### Adding a New Source Type

1. Create source class:

```python
@register_source(
    source_type="newsource",
    loader_class=NewSourceLoader,
    name="newsource_loader"
)
class NewSource(BaseSource, SecureConfigMixin):
    source_type: str = "newsource"
    # Add source-specific fields

    def get_loader_kwargs(self) -> Dict[str, Any]:
        return {"param": self.param}
```

2. Update PathAnalyzer to detect it:

```python
# Add detection logic in PathAnalyzer
if "newsource://" in path:
    return SourceInfo(source_type="newsource", ...)
```

3. The loader is automatically available!

### Adding a New Loader for Existing Source

```python
@register_source(
    source_type="pdf",  # Existing source type
    loader_class=AdvancedPDFLoader,
    name="advanced_pdf",
    preference=LoaderPreference.QUALITY  # Higher quality option
)
class PDFAdvancedSource(PDFSource):
    # Inherits from existing source
    pass
```

## Error Handling Strategy

1. **Graceful Degradation**: Try multiple loaders if one fails
2. **Detailed Error Reporting**: Include source info in errors
3. **Retry Logic**: Automatic retry with exponential backoff
4. **Fallback Options**: Use alternative loaders if available
5. **User-Friendly Messages**: Clear error descriptions

## Performance Considerations

1. **Concurrent Loading**: Up to max_concurrency workers
2. **Caching**: TTL-based cache for repeated loads
3. **Streaming**: Support for large files via lazy_load
4. **Resource Management**: Proper cleanup of connections
5. **Memory Efficiency**: Stream processing where possible

---

This architecture provides a robust, extensible foundation for document loading while maintaining clean separation of concerns and excellent user experience.
