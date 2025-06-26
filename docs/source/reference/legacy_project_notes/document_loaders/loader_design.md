# Document Loader Design for Haive Framework

## Overview

This document outlines the architecture for integrating LangChain's document loaders into the Haive Framework. We need a system that can:

1. Analyze any input path/URL to determine its type
2. Detect the appropriate source type for the input
3. Select the optimal loader strategy
4. Handle loading with appropriate configuration

## Components

### 1. Path Analysis System

The `analyze_path_comprehensive` function provides detailed analysis of:

- Local files and directories
- URLs and web resources
- Database URIs
- Cloud storage paths

This gives us detailed metadata like:

- Path type classification
- File extensions and MIME types
- Access permissions
- Domain information for URLs
- Cloud provider details for cloud storage

### 2. Source Type System

We'll use a hierarchy of source types:

```
BaseSource
├── LocalSource
│   ├── TextFileSource
│   ├── PDFSource
│   ├── CSVSource
│   └── ...
├── RemoteSource
│   ├── WebPageSource
│   ├── GitHubSource
│   ├── YouTubeSource
│   └── ...
├── DatabaseSource
│   ├── SQLSource
│   ├── MongoDBSource
│   └── ...
└── CloudSource
    ├── S3Source
    ├── GCSSource
    └── ...
```

Each source type specifies:

- Patterns for matching inputs
- Available loader strategies
- Configuration requirements

### 3. Dynamic Registry

The `DynamicSourceRegistry` provides:

- Automatic registration of source types
- Pattern matching to find appropriate sources
- Confidence scoring for source selection
- Loader strategy recommendations

### 4. Loader Strategy System

Each source type can have multiple loading strategies:

```python
@dataclass
class LoaderStrategy:
    strategy_name: str
    loader_class: str
    loader_module: str = ""
    speed: Literal["fast", "medium", "slow"] = "medium"
    quality: Literal["low", "medium", "high"] = "medium"
    resource_usage: Literal["low", "medium", "high"] = "medium"
    supports_lazy_load: bool = False
    supports_async: bool = False
    supports_batching: bool = False
    best_for: List[str] = field(default_factory=list)
    requires_auth: bool = False
    requires_network: bool = False
    max_file_size: Optional[int] = None
    estimated_time_per_mb: float = 0.1
```

This allows selecting the best loader based on:

- Performance requirements
- Quality needs
- Resource constraints
- File characteristics

### 5. LangGraph Workflow

A LangGraph workflow orchestrates the process:

1. Analyze path
2. Detect source types
3. Select best source
4. Discover loader strategies
5. Test loader performance (optional)
6. Load documents

## Implementation Plan

### Phase 1: File-based Loaders

Start with the most common file types:

- Text files
- PDFs
- CSV/Excel
- Word documents
- Markdown

### Phase 2: Web-based Loaders

Implement loaders for:

- Web pages
- GitHub repositories
- YouTube videos
- Wikipedia articles

### Phase 3: Database and Cloud Storage

Add support for:

- SQL databases
- MongoDB
- S3/GCS/Azure storage
- Google Drive/Dropbox

### Phase 4: API and Specialized Loaders

Integrate:

- API-based services (Notion, Airtable)
- Chat/messaging platforms
- Specialized data sources

## Special Considerations

### Authentication

Many loaders require authentication:

- API keys for third-party services
- OAuth credentials
- Database connection strings

We need a credential management system that:

- Securely stores credentials
- Provides them to loaders when needed
- Handles token refresh and expiration

### Error Handling

Robust error handling for:

- Invalid paths/URLs
- Authentication failures
- Rate limiting
- Network issues
- Unsupported file types

### Loader-specific Configuration

Some loaders have specialized configuration:

- JSONLoader needs a jq schema
- WebBaseLoader might need JavaScript support
- SQLDatabaseLoader needs query configuration

### Custom Methods

Some loaders have methods beyond the standard `load()`:

- GitHubIssuesLoader: `load_all_available_issues`
- PDFLoaders: OCR configuration
- Specialized parsers and extractors

## Source Type Implementation Examples

### PDF Source

```python
@auto_source
class PDFSource(LocalSource):
    """PDF document source."""
    file_path: FilePath

    class Config:
        file_extensions = ['.pdf']
        loader_strategies = {
            'fast': {
                'class': 'PyPDFLoader',
                'speed': 'fast',
                'quality': 'medium',
                'best_for': ['text_heavy']
            },
            'ocr': {
                'class': 'UnstructuredPDFLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['scanned', 'images']
            },
            'tables': {
                'class': 'PDFPlumberLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['tables', 'forms']
            }
        }
```

### GitHub Source

```python
@auto_source(domain_patterns=["github.com"])
class GitHubSource(RemoteSource):
    """GitHub repository source."""
    repo_url: HttpUrl
    include_issues: bool = True
    include_code: bool = True

    class Config:
        path_patterns = ["/*/*"]  # user/repo pattern
        loader_strategies = {
            'issues': {
                'class': 'GitHubIssuesLoader',
                'speed': 'medium',
                'quality': 'high',
                'best_for': ['issues', 'discussions'],
                'requires_auth': True
            },
            'repo': {
                'class': 'GitHubDirectoryLoader',
                'speed': 'slow',
                'quality': 'high',
                'best_for': ['code', 'documentation'],
                'requires_auth': True
            }
        }

    def authenticate(self, credentials):
        """Set GitHub authentication"""
        self.github_token = credentials.get('github_token')
```

## Next Steps

1. Complete the path analysis system
2. Implement the base source classes
3. Create the dynamic registry
4. Build loader strategies
5. Develop the LangGraph workflow
6. Implement specific source types, starting with the most commonly used ones
