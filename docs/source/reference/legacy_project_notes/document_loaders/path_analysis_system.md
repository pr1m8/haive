# Path Analysis System for Document Loaders

## Overview

The path analysis system is the foundation for our document loader framework. It determines what kind of input we're dealing with, which dictates the appropriate source type and loader strategy. This document outlines the design and implementation of this critical component.

## Core Components

### 1. Path Type Classification

We classify paths into primary types:

```python
class PathType(str, Enum):
    """Primary path type classification."""
    LOCAL_FILE = "local_file"
    LOCAL_DIRECTORY = "local_directory"
    LOCAL_SYMLINK = "local_symlink"
    LOCAL_NONEXISTENT = "local_nonexistent"
    URL_HTTP = "url_http"
    URL_HTTPS = "url_https"
    URL_FTP = "url_ftp"
    URL_FILE = "url_file"
    DATABASE_URI = "database_uri"
    CLOUD_STORAGE = "cloud_storage"
    NETWORK_SHARE = "network_share"
    SPECIAL_PATH = "special_path"
    UNKNOWN = "unknown"
```

### 2. File Type Classification

We classify files into categories:

```python
class FileCategory(str, Enum):
    """High-level file category."""
    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CODE = "code"
    DATA = "data"
    ARCHIVE = "archive"
    EXECUTABLE = "executable"
    TEXT = "text"
    FONT = "font"
    MODEL = "model"
    SYSTEM = "system"
    UNKNOWN_FILE = "unknown_file"
```

### 3. Specific File Type Enums

We have detailed enums for specific file types:

- `DocumentType`: PDF, DOCX, etc.
- `ImageType`: JPG, PNG, etc.
- `VideoType`: MP4, AVI, etc.
- `AudioType`: MP3, WAV, etc.
- `DataType`: CSV, JSON, etc.
- `CodeType`: PY, JS, etc.

### 4. Analysis Components

#### URL Analysis

```python
class URLComponents(BaseModel):
    """Detailed URL component analysis."""
    scheme: Optional[str] = None
    netloc: Optional[str] = None
    path: Optional[str] = None
    query: Optional[str] = None
    fragment: Optional[str] = None
    hostname: Optional[str] = None
    port: Optional[int] = None
    domain: Optional[str] = None
    subdomain: Optional[str] = None
    root_url: Optional[str] = None
    base_url: Optional[str] = None
    path_segments: List[str] = Field(default_factory=list)
    query_params: Dict[str, str] = Field(default_factory=dict)
    is_secure: bool = False
    is_local_network: bool = False
    is_ip_address: bool = False
    content_type_hint: Optional[str] = None
```

#### Domain Analysis

```python
class DomainInfo(BaseModel):
    """Domain information and classification."""
    domain: str
    subdomain: Optional[str] = None
    second_level_domain: str
    top_level_domain: str
    is_well_known: bool = False
    service_type: Optional[str] = None
```

#### Database and Cloud Analysis

```python
class DatabaseType(str, Enum):
    """Database type classification."""
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    # ...and more

class CloudProvider(str, Enum):
    """Cloud storage provider classification."""
    AWS_S3 = "aws_s3"
    AZURE_BLOB = "azure_blob"
    GOOGLE_CLOUD = "google_cloud"
    DROPBOX = "dropbox"
    # ...and more
```

### 5. Comprehensive Analysis Result

```python
class PathAnalysisResult(BaseModel):
    """Comprehensive analysis result for a given path or URL."""
    original_path: str
    path_type: PathType = PathType.UNKNOWN
    is_local: bool = False
    is_remote: bool = False
    is_absolute: bool = False
    is_relative: bool = False
    exists: bool = False
    is_readable: bool = False
    is_writable: bool = False
    is_executable: bool = False
    is_file: bool = False
    is_directory: bool = False
    is_symlink: bool = False
    file_size: Optional[int] = None
    parent_directory: Optional[str] = None
    filename: Optional[str] = None
    file_extension: Optional[str] = None
    file_stem: Optional[str] = None
    url_components: Optional[URLComponents] = None
    domain_info: Optional[DomainInfo] = None
    database_type: Optional[DatabaseType] = None
    database_name: Optional[str] = None
    cloud_provider: Optional[CloudProvider] = None
    bucket_name: Optional[str] = None
    object_key: Optional[str] = None
    file_category: Optional[FileCategory] = None
    specific_file_type: Optional[str] = None
    mime_type: Optional[str] = None
    permissions: Optional[str] = None
    resolved_path: Optional[str] = None
    canonical_path: Optional[str] = None
    analysis_errors: List[str] = Field(default_factory=list)
    analysis_warnings: List[str] = Field(default_factory=list)
```

### 6. Path Analyzers

We use specialized analyzers for different path types:

```python
class BasePathAnalyzer(ABC):
    """Abstract base class for path analyzers."""

    @abstractmethod
    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        pass

    @abstractmethod
    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Perform analysis and update the result object."""
        pass
```

Implementations include:

- `LocalPathAnalyzer`: For filesystem paths
- `URLAnalyzer`: For web URLs
- `DatabaseURIAnalyzer`: For database connections
- `CloudStorageAnalyzer`: For cloud storage paths

### 7. Main Analysis Function

```python
def analyze_path_comprehensive(path_input: Union[str, Path]) -> PathAnalysisResult:
    """Comprehensively analyze a path or URL to determine its nature, type, and properties."""
    # Convert input to string for consistent processing
    original_path = str(path_input)

    # Initialize result object
    result = PathAnalysisResult(original_path=original_path)

    # Available analyzers in order of priority
    analyzers = [
        DatabaseURIAnalyzer(),
        CloudStorageAnalyzer(),
        URLAnalyzer(),
        LocalPathAnalyzer(),  # Should be last as it's most permissive
    ]

    # Find the appropriate analyzer
    analyzer_found = False
    for analyzer in analyzers:
        if analyzer.can_analyze(original_path):
            try:
                analyzer.analyze(original_path, result)
                analyzer_found = True
                break
            except Exception as e:
                result.analysis_errors.append(f"Analyzer {analyzer.__class__.__name__} failed: {str(e)}")

    if not analyzer_found:
        result.analysis_errors.append("No suitable analyzer found for this path")
        result.path_type = PathType.UNKNOWN

    return result
```

## Implementation Details

### Local Path Analysis

For local paths, we check:

- Existence
- File vs. directory
- Symlink status
- Permissions
- File extension and type
- Size
- Parent directory

### URL Analysis

For URLs, we examine:

- Scheme (http, https, etc.)
- Domain and subdomain
- Path and query parameters
- Accessibility
- File extension if present in path
- Content type from headers

### Database URI Analysis

For database URIs, we identify:

- Database type (PostgreSQL, MySQL, etc.)
- Connection parameters (host, port)
- Database name
- Authentication information

### Cloud Storage Analysis

For cloud storage paths, we extract:

- Cloud provider (AWS S3, GCS, Azure, etc.)
- Bucket or container name
- Object key
- Access permissions

## Extended Path Analysis System

To enhance the core path analysis, we've developed a LangGraph workflow that:

1. Performs initial path analysis
2. Routes to specialized subgraphs based on path type:
   - Local file subgraph
   - URL subgraph
   - Database subgraph
   - Cloud storage subgraph
3. Applies specialized analysis for each path type
4. Consolidates results into an enriched output

### Enhancements

The LangGraph workflow adds:

- More detailed analysis for each path type
- File content sampling (where applicable)
- Metadata extraction
- Recommendations for handling the path
- Error recovery and fallbacks

## Integration with Source Detection

The path analysis result is used to match appropriate source types through the `DynamicSourceRegistry`:

```python
# Find matching source types with confidence scores
matches = registry.find_matching_sources(analysis_result)

# Select the best source type
best_source = max(matches, key=lambda x: x[1])  # (source_type, confidence)
```

## Next Steps

1. Complete implementation of all analyzer types
2. Add support for more specific file types
3. Enhance metadata extraction
4. Improve error handling and recovery
5. Optimize performance for large file systems
6. Integrate with source type detection system
