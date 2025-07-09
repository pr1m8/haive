# Document Loaders Subsystem

The loaders subsystem provides a comprehensive strategy-based system for loading documents from 97+ different sources. It implements intelligent loader selection, capability-based filtering, and seamless integration with langchain_community.document_loaders.

## Overview

The loader subsystem consists of:

- **Strategy Registry**: Central registry of 97+ loader strategies
- **Auto-Selection**: Intelligent loader selection based on source characteristics
- **Capability System**: Filter loaders by specific capabilities (OCR, async, etc.)
- **Performance Profiles**: Balance between speed, quality, and resource usage
- **Fallback Mechanisms**: Graceful handling of unavailable loaders

## Architecture

### Core Components

1. **LoaderStrategy** (`strategy.py`)
   - Defines loader configurations and capabilities
   - Tracks performance characteristics (speed, quality, resource usage)
   - Specifies dependencies and authentication requirements
   - Manages priority levels for selection

2. **LoaderStrategyRegistry** (`strategy.py`)
   - Central registry for all loader strategies
   - Provides lookup and filtering capabilities
   - Handles strategy registration and management
   - Supports dynamic loader discovery

3. **LoaderRegistry** (`registry.py`)
   - Decorator-based loader registration
   - Capability discovery system
   - Metadata management for loaders
   - Integration with langchain loaders

4. **Base Classes** (`base/`)
   - Abstract interfaces for loaders
   - Common functionality and utilities
   - Type definitions and protocols

## Loader Categories

### 📄 Document Loaders (15+)

- **PDF**: PyMuPDF, PDFPlumber, PyPDF, PDFMiner, PyPDFium2, MathpixPDF
- **Office**: DOCX, XLSX, PPTX, ODT, RTF
- **Text**: Plain text, Markdown, ReStructuredText

### 🌐 Web Loaders (10+)

- **Basic**: URLLoader, WebBaseLoader
- **Advanced**: PlaywrightLoader, SeleniumLoader
- **Specific**: Wikipedia, ArXiv, YouTube, Reddit, HackerNews

### ☁️ Cloud Storage (15+)

- **AWS**: S3 files and directories
- **Google**: GCS, Google Drive, BigQuery
- **Azure**: Blob Storage, Document Intelligence
- **Others**: Dropbox, OneDrive, SharePoint

### 🗄️ Database Loaders (10+)

- **SQL**: Generic SQL, PostgreSQL, MySQL
- **NoSQL**: MongoDB, Elasticsearch, Cassandra, Couchbase
- **Analytics**: BigQuery, Snowflake, DuckDB

### 💬 Chat/Messaging (10+)

- **Business**: Slack, Microsoft Teams
- **Social**: Discord, WhatsApp, Telegram, Facebook
- **Forums**: Reddit, Mastodon

### 📝 Knowledge Management (10+)

- **Note-taking**: Notion, Obsidian, Roam, Evernote
- **Collaboration**: Confluence, Jira, Asana, Trello
- **Documentation**: GitBook, Docusaurus

### 🔧 Specialized Loaders (20+)

- **Data**: CSV, JSON, YAML, TOML, XML
- **Code**: Python, Jupyter Notebooks, Git
- **Media**: Images (OCR), EPub, Subtitles
- **Others**: Email, iMessage, Weather, News

## Usage Examples

### Basic Loader Strategy Usage

```python
from haive.core.engine.document.loaders.strategy import strategy_registry

# Get a specific strategy
pdf_strategy = strategy_registry.get_strategy("pdf_pymupdf")
print(f"Loader class: {pdf_strategy.loader_class}")
print(f"Speed: {pdf_strategy.speed}")
print(f"Quality: {pdf_strategy.quality}")

# List all available strategies
strategies = strategy_registry.list_strategies(available_only=True)
print(f"Available strategies: {len(strategies)}")

# Find strategies by capability
ocr_strategies = strategy_registry.find_by_capability("image_extraction")
async_strategies = strategy_registry.find_by_capability("async")
```

### Finding Loaders for File Types

```python
# Find best loader for a file type
pdf_loaders = strategy_registry.find_best_for("pdf")
for loader in pdf_loaders:
    print(f"{loader.strategy_name}: Priority={loader.priority.value}")

# Get loaders by performance characteristics
fast_loaders = [s for s in strategies if s.speed == "fast"]
high_quality = [s for s in strategies if s.quality == "high"]
```

### Custom Strategy Registration

```python
from haive.core.engine.document.loaders.strategy import (
    LoaderStrategy,
    LoaderPriority,
    LoaderCapability
)

# Define custom strategy
custom_strategy = LoaderStrategy(
    strategy_name="my_custom_loader",
    loader_class="MyCustomLoader",
    module_path="my_package.loaders",
    speed="fast",
    quality="high",
    resource_usage="medium",
    capabilities=[
        LoaderCapability.TEXT_EXTRACTION,
        LoaderCapability.METADATA,
        LoaderCapability.ASYNC
    ],
    best_for=["myformat", "custom"],
    priority=LoaderPriority.HIGH,
    requires_dependencies=["my-custom-lib"]
)

# Register it
strategy_registry.register(custom_strategy)
```

## Loader Capabilities

### Core Capabilities

- **ASYNC**: Supports asynchronous loading
- **METADATA**: Extracts document metadata
- **TEXT_EXTRACTION**: Basic text extraction
- **CONTENT_EXTRACTION**: Advanced content extraction

### Advanced Capabilities

- **IMAGE_EXTRACTION**: Extract images from documents
- **TABLE_EXTRACTION**: Extract structured tables
- **STRUCTURE_PRESERVATION**: Maintains document structure
- **LAZY_LOADING**: Load documents on demand
- **PAGINATION**: Handle paginated sources
- **CHUNKING**: Built-in document chunking
- **FILTERING**: Filter documents during loading
- **BATCHING**: Process multiple documents efficiently

## Performance Considerations

### Speed Profiles

- **Fast**: Minimal processing, basic extraction
- **Medium**: Balanced performance and quality
- **Slow**: Comprehensive extraction, high quality

### Quality Levels

- **Low**: Basic text extraction only
- **Medium**: Text + basic formatting
- **High**: Full fidelity with structure, formatting, metadata

### Resource Usage

- **Low**: Minimal memory and CPU usage
- **Medium**: Moderate resource consumption
- **High**: Resource-intensive (OCR, complex parsing)

## Authentication Support

Many loaders require authentication:

```python
# Check if authentication required
strategy = strategy_registry.get_strategy("google_drive")
if strategy.requires_authentication:
    print("Authentication required")
    print(f"Dependencies: {strategy.requires_dependencies}")

# Loaders requiring auth include:
# - Cloud storage (S3, GCS, Azure)
# - API services (Notion, Confluence, Slack)
# - Social platforms (Twitter, Facebook)
```

## Error Handling

The loader system provides robust error handling:

1. **Missing Dependencies**: Gracefully handles unavailable loaders
2. **Authentication Failures**: Clear error messages for auth issues
3. **Format Errors**: Fallback to alternative loaders
4. **Network Issues**: Retry mechanisms for web loaders

## Best Practices

1. **Use Auto-Selection**: Let the system choose the best loader
2. **Specify Preferences**: Use quality/speed preferences when needed
3. **Handle Dependencies**: Check loader availability before use
4. **Cache Results**: Many loaders support caching for performance
5. **Batch Processing**: Use batch-capable loaders for multiple files

## Extending the System

### Adding New Strategies

1. Create strategy definition in `strategy.py`
2. Ensure loader class is available in langchain_community
3. Set appropriate capabilities and performance characteristics
4. Register with appropriate priority

### Creating Custom Loaders

1. Inherit from BaseLoader or appropriate base class
2. Implement required methods (load, lazy_load)
3. Use @register_loader decorator for auto-discovery
4. Add strategy definition to registry

## Troubleshooting

### Common Issues

1. **Loader Not Found**
   - Check if strategy exists: `strategy_registry.get_strategy(name)`
   - Verify dependencies installed
   - Check loader class name matches

2. **Authentication Errors**
   - Verify credentials provided
   - Check authentication method supported
   - Review loader-specific documentation

3. **Performance Issues**
   - Use appropriate speed/quality settings
   - Enable parallel processing
   - Consider lazy loading for large documents

### Debug Information

```python
# Get detailed loader information
strategy = strategy_registry.get_strategy("pdf_pymupdf")
print(strategy.model_dump_json(indent=2))

# Check loader availability
if strategy.is_available:
    print("Loader is available")
else:
    print(f"Missing: {strategy.requires_dependencies}")
```

## See Also

- [Document Engine Documentation](../README.md)
- [AutoLoader Factory](../factory.py)
- [Processing Strategies](../processors.py)
