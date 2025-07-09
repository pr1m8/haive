# Document Sources Subsystem

The sources subsystem provides legacy source type implementations and utilities for working with different document sources. This subsystem works in conjunction with the newer path analysis system to identify and handle various document sources.

## Overview

The sources subsystem includes:

- **Base Source Classes**: Abstract interfaces for different source types
- **Local Sources**: File system-based document sources
- **Web Sources**: URL and web-based document sources
- **Source Detection**: Utilities for identifying source types

> **Note**: This is a legacy subsystem. New implementations should use the path_analysis.py system and the loaders/strategy.py registry for source handling.

## Source Types

### Local File Sources

Handles documents from the local file system:

```python
from haive.core.engine.document.sources.local import LocalSource

# Create local source
source = LocalSource(
    path="/path/to/document.pdf",
    encoding="utf-8",
    glob_pattern=None
)

# Check if source exists
if source.exists():
    # Get source metadata
    metadata = source.get_metadata()
    print(f"File size: {metadata['size']}")
    print(f"Modified: {metadata['modified']}")
```

### Web Sources

Handles documents from web URLs:

```python
from haive.core.engine.document.sources.web import WebSource

# Create web source
source = WebSource(
    url="https://example.com/document.pdf",
    headers={"User-Agent": "DocumentLoader/1.0"},
    verify_ssl=True
)

# Check if accessible
if source.is_accessible():
    # Get content type
    content_type = source.get_content_type()
    print(f"Content type: {content_type}")
```

## Base Source Interface

All source implementations follow this interface:

```python
from haive.core.engine.document.sources.base import BaseSource
from typing import Dict, Any, Optional

class CustomSource(BaseSource):
    """Custom source implementation."""

    def __init__(self, identifier: str, **kwargs):
        self.identifier = identifier
        self.options = kwargs

    def exists(self) -> bool:
        """Check if source exists/is accessible."""
        # Implementation
        return True

    def get_metadata(self) -> Dict[str, Any]:
        """Get source metadata."""
        return {
            "source_type": "custom",
            "identifier": self.identifier,
            # Additional metadata
        }

    def get_loader_hints(self) -> Dict[str, Any]:
        """Provide hints for loader selection."""
        return {
            "preferred_loader": "custom_loader",
            "encoding": "utf-8",
            "format": "custom"
        }

    @property
    def source_type(self) -> str:
        """Return the source type identifier."""
        return "custom"
```

## Source Detection

### Automatic Detection

```python
from haive.core.engine.document.sources import detect_source_type

# Detect source type from path/URL
source_info = detect_source_type("https://example.com/doc.pdf")
print(f"Type: {source_info['type']}")  # 'web'
print(f"Format: {source_info['format']}")  # 'pdf'

# Local file
source_info = detect_source_type("/path/to/data.csv")
print(f"Type: {source_info['type']}")  # 'local'
print(f"Format: {source_info['format']}")  # 'csv'
```

### Source Factory

```python
from haive.core.engine.document.sources import create_source

# Create appropriate source instance
source = create_source("s3://bucket/file.json")
print(f"Source type: {source.source_type}")  # 's3'

# With options
source = create_source(
    "https://api.example.com/data",
    headers={"Authorization": "Bearer token"},
    timeout=30
)
```

## Integration with Document Engine

The sources subsystem integrates with the document engine through:

1. **Path Analysis**: Modern path analysis system in `path_analysis.py`
2. **Loader Selection**: Strategy-based loader selection
3. **Metadata Extraction**: Source metadata passed to documents

### Example Integration

```python
from haive.core.engine.document import DocumentEngine
from haive.core.engine.document.sources import LocalSource

# Sources are handled automatically by the engine
engine = DocumentEngine()

# Direct source handling (legacy)
source = LocalSource("/path/to/file.txt")
if source.exists():
    metadata = source.get_metadata()
    # Engine uses this metadata for processing
```

## Legacy vs Modern Approach

### Legacy Approach (This Subsystem)

```python
# Manual source creation and handling
from haive.core.engine.document.sources import create_source

source = create_source("document.pdf")
metadata = source.get_metadata()
loader_hints = source.get_loader_hints()
# Manually select loader based on hints
```

### Modern Approach (Recommended)

```python
# Automatic handling via path analysis
from haive.core.engine.document import DocumentEngine

engine = DocumentEngine()
result = engine.invoke("document.pdf")
# Source detection, loader selection, and processing handled automatically
```

## Extending Sources

### Creating Custom Source Types

```python
from haive.core.engine.document.sources.base import BaseSource
from typing import Dict, Any
import requests

class APISource(BaseSource):
    """Source for API endpoints."""

    def __init__(self, endpoint: str, api_key: str = None):
        self.endpoint = endpoint
        self.api_key = api_key

    def exists(self) -> bool:
        """Check if API endpoint is accessible."""
        try:
            response = requests.head(
                self.endpoint,
                headers=self._get_headers(),
                timeout=5
            )
            return response.status_code < 400
        except:
            return False

    def get_metadata(self) -> Dict[str, Any]:
        """Get API metadata."""
        return {
            "source_type": "api",
            "endpoint": self.endpoint,
            "requires_auth": bool(self.api_key),
            "protocol": "https" if self.endpoint.startswith("https") else "http"
        }

    def _get_headers(self) -> Dict[str, str]:
        """Get request headers."""
        headers = {"User-Agent": "DocumentLoader/1.0"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers
```

### Registering Custom Sources

```python
from haive.core.engine.document.sources import register_source_type

# Register custom source
register_source_type(
    pattern=r"^api://",
    source_class=APISource,
    priority=10
)

# Now it works with detection
source = create_source("api://example.com/data")
```

## Source Utilities

### Path Utilities

```python
from haive.core.engine.document.sources.utils import (
    normalize_path,
    is_url,
    is_local_path,
    extract_extension
)

# Normalize paths
normalized = normalize_path("~/Documents/../file.txt")

# Check path types
if is_url("https://example.com"):
    print("It's a URL")

if is_local_path("/path/to/file"):
    print("It's a local path")

# Extract extensions
ext = extract_extension("document.pdf.gz")  # Returns ".gz"
```

### Metadata Utilities

```python
from haive.core.engine.document.sources.utils import (
    merge_metadata,
    sanitize_metadata,
    extract_common_metadata
)

# Merge metadata from multiple sources
merged = merge_metadata(
    source_metadata,
    loader_metadata,
    {"custom": "value"}
)

# Sanitize metadata for storage
clean = sanitize_metadata(raw_metadata)

# Extract common fields
common = extract_common_metadata(full_metadata)
```

## Best Practices

### 1. Use Modern Path Analysis

For new implementations, use the path analysis system:

```python
from haive.core.engine.document.path_analysis import analyze_path

# Modern approach
analysis = analyze_path("s3://bucket/file.pdf")
# Use analysis results for loader selection
```

### 2. Handle Source Errors

Always handle source access errors:

```python
try:
    if source.exists():
        metadata = source.get_metadata()
    else:
        # Handle missing source
        pass
except SourceError as e:
    # Log and handle appropriately
    logger.error(f"Source error: {e}")
```

### 3. Preserve Source Metadata

Pass source metadata through the processing pipeline:

```python
# Source metadata should be preserved in documents
document = Document(
    page_content=content,
    metadata={
        **source.get_metadata(),
        "processing_timestamp": datetime.now().isoformat()
    }
)
```

## Migration Guide

If you're using the legacy sources system, consider migrating:

### From Legacy

```python
# Old approach
from haive.core.engine.document.sources import LocalSource
source = LocalSource("file.pdf")
metadata = source.get_metadata()
```

### To Modern

```python
# New approach
from haive.core.engine.document import DocumentEngine
engine = DocumentEngine()
result = engine.invoke("file.pdf")
# Metadata automatically included in result.documents[0].metadata
```

## See Also

- [Document Engine Documentation](../README.md)
- [Path Analysis System](../path_analysis.py)
- [Loader Strategy System](../loaders/strategy.py)
- [Source Base Classes](./base.py)
