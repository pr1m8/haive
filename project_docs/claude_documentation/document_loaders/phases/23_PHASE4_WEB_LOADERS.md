# Phase 4: Web Loaders Implementation - COMPLETED

## 🎯 **Phase Overview**

Implementation of comprehensive web-based document loaders with intelligent sitemap detection, recursive crawling, browser automation, and documentation site processing. Enhanced with legacy sitemap detection logic.

---

## ✅ **Implemented Sources (10+ loaders)**

### **Base Web Loaders**

1. **`web_base`**: Foundation WebBaseLoader with multiple processing options
2. **`async_html`**: AsyncHtmlLoader for high-performance concurrent processing
3. **`unstructured_web`**: UnstructuredURLLoader for advanced content extraction

### **Browser Automation**

4. **`playwright_web`**: Playwright browser automation for JavaScript-heavy sites
5. **`selenium_web`**: Selenium browser automation for complex interactions
6. **`chromium_async`**: Async Chromium loader for high-performance automation

### **Recursive and Bulk Crawling**

7. **`recursive_web`**: RecursiveUrlLoader with depth control and filtering
8. **`sitemap_crawler`**: SitemapLoader with intelligent auto-detection

### **Documentation Sites**

9. **`readthedocs`**: Read the Docs documentation site processing
10. **`docusaurus`**: Docusaurus documentation site processing

### **Advanced Services**

11. **`firecrawl`**: FireCrawl web scraping service integration

---

## 🔍 **Intelligent Sitemap Detection**

### **Enhanced Sitemap Discovery** (from legacy system)

```python
def find_sitemap(base_url: str, keep_path_segment: Optional[str] = None) -> Optional[str]:
    """
    Find sitemap URL by checking common paths with path trimming.
    Enhanced from legacy web_loaders.py with better error handling.
    """
    common_sitemap_paths = [
        "sitemap.xml",
        "sitemap_index.xml",
        "sitemaps/sitemap.xml",
        "sitemap/sitemap.xml",
        "wp-sitemap.xml",  # WordPress
        "sitemap-index.xml"
    ]
```

### **Pre-Hook Integration**

The `sitemap_crawler` source automatically detects sitemaps before crawling:

```python
@register_bulk_source(
    name="sitemap_crawler",
    description="Sitemap-based website crawler with auto-detection"
)
class SitemapCrawlerSource(RemoteSource):
    def get_loader_kwargs(self) -> Dict[str, Any]:
        # Auto-detect sitemap if not provided
        sitemap_url = self.sitemap_url
        if not sitemap_url:
            sitemap_url = find_sitemap(self.url, self.keep_path_segment)
            if not sitemap_url:
                raise ValueError(f"No sitemap found for {self.url}")
```

### **Usage Pattern**

```python
# Automatic sitemap detection and bulk crawling
source = enhanced_registry.create_source("https://docs.python.org")
# → Auto-detects sitemap at https://docs.python.org/sitemap.xml
# → Processes entire documentation site via sitemap
```

---

## 🕷️ **Recursive Web Crawling**

### **Advanced Crawling Strategies**

```python
class CrawlStrategy(str, Enum):
    SIMPLE = "simple"           # Basic HTTP requests
    JAVASCRIPT = "javascript"   # Browser automation
    ASYNC = "async"            # Asynchronous processing
    SITEMAP = "sitemap"        # Sitemap-based crawling
    RECURSIVE = "recursive"    # Deep recursive crawling
```

### **Recursive Web Source Features**

- **Depth Control**: Configurable max_depth for crawling
- **Domain Boundaries**: prevent_outside to stay within site
- **Content Filtering**: link_regex and content_filter options
- **Error Handling**: continue_on_failure for robust crawling
- **Metadata Extraction**: Enhanced HTML metadata extraction

### **Browser Automation Options**

```python
class BrowserEngine(str, Enum):
    PLAYWRIGHT = "playwright"  # Modern, fast, reliable
    SELENIUM = "selenium"      # Mature, widely supported
    CHROMIUM = "chromium"      # Lightweight, async
```

---

## 🏗️ **Implementation Architecture**

### **Base Classes Used**

- **RemoteSource**: Foundation for all web sources with SecureConfigMixin
- **Enhanced capabilities**: Async processing, bulk loading, recursive crawling
- **Metadata extraction**: BeautifulSoup-based HTML parsing

### **Registration Patterns**

**Simple Web Source:**

```python
@register_web_source(
    name="web_base",
    url_patterns=["http", "https"],
    loaders={
        "simple": "WebBaseLoader",
        "bs4": "BSHTMLLoader",
        "unstructured": "UnstructuredURLLoader"
    },
    capabilities=[LoaderCapability.METADATA_EXTRACTION]
)
class WebBaseSource(RemoteSource):
    pass
```

**Bulk Crawling Source:**

```python
@register_bulk_source(
    name="recursive_web",
    category=SourceCategory.WEB_SCRAPING,
    loaders={"recursive": "RecursiveUrlLoader"},
    max_concurrent=6,
    supports_filtering=True,
    supports_recursive=True,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.RECURSIVE]
)
class RecursiveWebSource(RemoteSource):
    max_depth: int = 2
    prevent_outside: bool = True
    use_async: bool = True
```

---

## 🎯 **Key Features Implemented**

### **Sitemap Integration**

✅ **Auto-Detection**: Intelligent sitemap discovery from base URLs
✅ **Path Preservation**: keep_path_segment for complex site structures  
✅ **Multiple Formats**: Support for sitemap.xml, sitemap_index.xml, WordPress
✅ **Validation**: Content-Type verification for actual XML sitemaps
✅ **Fallback**: Graceful degradation when no sitemap found

### **Browser Automation**

✅ **JavaScript Rendering**: Full support for SPA and dynamic content
✅ **Multiple Engines**: Playwright, Selenium, Chromium options
✅ **Async Processing**: High-performance concurrent automation
✅ **Custom Interactions**: wait_for_selector, scroll_to_bottom, script execution
✅ **Error Handling**: Robust error recovery and timeout management

### **Recursive Crawling**

✅ **Depth Control**: Configurable crawling depth with safety limits
✅ **Domain Boundaries**: Prevent crawling outside target domains
✅ **Content Filtering**: Regex-based link and content filtering
✅ **Bulk Processing**: High-performance concurrent crawling
✅ **Metadata Extraction**: Rich HTML metadata with BeautifulSoup

### **Documentation Sites**

✅ **Read the Docs**: Native RTD documentation processing
✅ **Docusaurus**: Specialized Docusaurus site handling
✅ **Version Support**: Multi-version documentation crawling
✅ **Structure Preservation**: Maintain documentation hierarchy

---

## 📊 **Performance Characteristics**

### **Concurrency Levels**

- **`async_html`**: Up to 10 concurrent requests
- **`recursive_web`**: 6 workers with async processing
- **`sitemap_crawler`**: 8 workers for sitemap processing
- **`chromium_async`**: 4 workers for browser automation

### **Processing Capabilities**

- **Rate Limiting**: Configurable requests_per_second
- **Timeout Management**: Per-request and global timeouts
- **Error Recovery**: Continue-on-failure with comprehensive logging
- **Memory Efficiency**: Streaming processing for large sites

---

## 🧪 **Testing & Integration**

### **Auto-Classification Pipeline**

```python
# Test automatic web source detection
test_urls = {
    "https://docs.python.org": "sitemap_crawler",  # Has sitemap
    "https://spa-app.com": "playwright_web",       # JavaScript required
    "https://simple-blog.com": "web_base",         # Simple HTML
    "https://docs.project.io": "readthedocs"       # RTD pattern
}

for url, expected_source in test_urls.items():
    source = enhanced_registry.create_source(url)
    assert source.source_type == expected_source
```

### **Sitemap Detection Testing**

```python
def test_sitemap_detection():
    # Test sitemap auto-discovery
    sitemap_url = find_sitemap("https://langchain-ai.github.io/langgraph/")
    assert sitemap_url == "https://langchain-ai.github.io/langgraph/sitemap.xml"

    # Test with path preservation
    sitemap_url = find_sitemap("https://docs.site.com/v2/api/", keep_path_segment="v2")
    # Should find sitemap while preserving v2 in path
```

---

## 🎯 **Legacy Integration**

### **Enhanced from Backup System**

- ✅ **Sitemap Detection**: Improved from `/haive_complete_backup/.../web_loaders.py`
- ✅ **Metadata Extraction**: Enhanced BeautifulSoup HTML parsing
- ✅ **Tool Integration**: @tool decorators for easy function access
- ✅ **Error Handling**: Robust request exception handling
- ✅ **Content Cleaning**: Regex-based newline and whitespace cleanup

### **Backward Compatibility**

- ✅ **Function Signatures**: Compatible with legacy tool functions
- ✅ **Return Formats**: Maintains Dict[str, Any] return types
- ✅ **Configuration**: Same parameter names and defaults

---

## 📋 **Implementation Files**

### **Primary Implementation**

- **File**: `web_sources.py`
- **Location**: `/packages/haive-core/src/haive/core/engine/document/loaders/sources/`
- **Size**: ~600 lines
- **Sources**: 11 web-based sources

### **Key Classes**

- `WebBaseSource`: Foundation web page processing
- `RecursiveWebSource`: Advanced recursive crawling
- `SitemapCrawlerSource`: Sitemap-based bulk processing
- `PlaywrightWebSource`: Browser automation for JavaScript
- `ReadTheDocsSource`: Documentation site processing

### **Legacy Integration**

- **Source**: `/haive_complete_backup/.../web_loaders.py`
- **Enhanced Functions**: `find_sitemap()`, `extract_metadata_from_html()`
- **Tool Compatibility**: Maintains @tool decorator patterns

---

## ✅ **Phase 4 Status: COMPLETE**

All web-based loading capabilities implemented with intelligent sitemap detection, recursive crawling, browser automation, and documentation site processing. Enhanced with proven legacy sitemap detection logic.

**Next Phase**: @24_PHASE5_DATABASES - Database and data warehouse loaders

---

_Reference: @00_DOCUMENT_LOADER_INDEX for navigation_  
_Previous: @22_PHASE3_BULK_LOADING_  
_Next: @24_PHASE5_DATABASES_  
_Legacy: Enhanced from `/haive_complete_backup/.../web_loaders.py`_
