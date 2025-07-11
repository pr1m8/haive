"""Web-based source registrations with sitemap detection and crawling.

This module implements comprehensive web scraping sources from langchain_community
with intelligent sitemap detection, recursive crawling, and browser automation.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests

from .enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_web_source,
)
from .source_types import CredentialType, LoaderCapability, RemoteSource, SourceCategory


class CrawlStrategy(str, Enum):
    """Web crawling strategies."""

    SIMPLE = "simple"  # Basic HTTP requests
    JAVASCRIPT = "javascript"  # Browser automation
    ASYNC = "async"  # Asynchronous processing
    SITEMAP = "sitemap"  # Sitemap-based crawling
    RECURSIVE = "recursive"  # Deep recursive crawling


class BrowserEngine(str, Enum):
    """Browser automation engines."""

    PLAYWRIGHT = "playwright"
    SELENIUM = "selenium"
    CHROMIUM = "chromium"


# =============================================================================
# Sitemap Detection and Utilities (from legacy system)
# =============================================================================


def find_sitemap(
    base_url: str, keep_path_segment: Optional[str] = None
) -> Optional[str]:
    """
    Find sitemap URL for a given base URL by checking common paths.

    Enhanced version of the legacy sitemap detection with better error handling.
    """
    # Normalize the base URL
    if base_url.endswith("/"):
        base_url = base_url[:-1]

    # Common sitemap locations (expanded from legacy)
    common_sitemap_paths = [
        "sitemap.xml",
        "sitemap_index.xml",
        "sitemaps/sitemap.xml",
        "sitemap/sitemap.xml",
        "wp-sitemap.xml",  # WordPress
        "sitemap-index.xml",
    ]

    # Try root domain first, then trim path segments
    while base_url:
        for sitemap in common_sitemap_paths:
            sitemap_url = urljoin(base_url + "/", sitemap)
            try:
                response = requests.head(sitemap_url, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    # Verify it's actually XML content
                    content_type = response.headers.get("Content-Type", "").lower()
                    if "xml" in content_type or "text" in content_type:
                        return sitemap_url
            except requests.RequestException:
                continue  # Try next path

        # Trim URL path but keep specified segment
        parsed = urlparse(base_url)
        path = parsed.path.rsplit("/", 1)[0]
        if keep_path_segment and keep_path_segment in path:
            break
        if not path or path == "/":
            break
        base_url = f"{parsed.scheme}://{parsed.netloc}{path}"

    return None


def extract_metadata_from_html(
    raw_html: str, url: str, response: Any
) -> Dict[str, Any]:
    """Extract metadata from HTML using BeautifulSoup (from legacy system)."""
    content_type = getattr(response, "headers", {}).get("Content-Type", "")
    metadata = {"source": url, "content_type": content_type}

    try:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(raw_html, "html.parser")

        if title := soup.find("title"):
            metadata["title"] = title.get_text().strip()
        if description := soup.find("meta", attrs={"name": "description"}):
            metadata["description"] = description.get("content", "").strip()
        if html := soup.find("html"):
            metadata["language"] = html.get("lang")

        # Extract additional metadata
        if keywords := soup.find("meta", attrs={"name": "keywords"}):
            metadata["keywords"] = keywords.get("content", "").strip()
        if author := soup.find("meta", attrs={"name": "author"}):
            metadata["author"] = author.get("content", "").strip()

    except ImportError:
        pass  # BeautifulSoup not available

    return metadata


# =============================================================================
# Base Web Loaders
# =============================================================================


@register_web_source(
    name="web_base",
    url_patterns=["http", "https"],
    loaders={
        "simple": {
            "class": "WebBaseLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "bs4": {
            "class": "BSHTMLLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        },
        "unstructured": {
            "class": "UnstructuredURLLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
    },
    default_loader="simple",
    description="Base web page loader with multiple processing options",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class WebBaseSource(RemoteSource):
    """Base web page source with multiple loading strategies."""

    # Processing options
    crawl_strategy: CrawlStrategy = CrawlStrategy.SIMPLE
    extract_metadata: bool = True
    clean_html: bool = True

    # Request configuration
    verify_ssl: bool = True
    user_agent: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Add web-specific configuration
        if self.user_agent:
            kwargs["headers"]["User-Agent"] = self.user_agent

        kwargs.update(
            {
                "verify": self.verify_ssl,
                "requests_kwargs": {
                    "timeout": self.timeout,
                    "headers": kwargs.get("headers", {}),
                },
            }
        )

        return kwargs


@register_web_source(
    name="async_html",
    url_patterns=["http", "https"],
    loaders={
        "async": {
            "class": "AsyncHtmlLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="async",
    description="Asynchronous HTML loader for high-performance web scraping",
    capabilities=[LoaderCapability.ASYNC_PROCESSING, LoaderCapability.BULK_LOADING],
    priority=7,
)
class AsyncHTMLSource(RemoteSource):
    """Asynchronous HTML source for concurrent processing."""

    # Async configuration
    trust_env: bool = True
    requests_per_second: int = 2

    # Processing options
    ignore_load_errors: bool = False
    default_parser: str = "html.parser"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "trust_env": self.trust_env,
                "requests_per_second": self.requests_per_second,
                "ignore_load_errors": self.ignore_load_errors,
                "default_parser": self.default_parser,
            }
        )
        return kwargs


# =============================================================================
# Browser Automation Sources
# =============================================================================


@register_web_source(
    name="playwright_web",
    url_patterns=["http", "https"],
    loaders={
        "playwright": {
            "class": "PlaywrightURLLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["playwright"],
        }
    },
    default_loader="playwright",
    description="Playwright browser automation for JavaScript-heavy sites",
    capabilities=[
        LoaderCapability.ASYNC_PROCESSING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=9,
)
class PlaywrightWebSource(RemoteSource):
    """Playwright browser automation source."""

    # Browser configuration
    browser_engine: BrowserEngine = BrowserEngine.PLAYWRIGHT
    headless: bool = True
    wait_for_selector: Optional[str] = None

    # JavaScript handling
    wait_for_js: bool = True
    js_timeout: int = 30000
    scroll_to_bottom: bool = False

    # Page interaction
    remove_selectors: List[str] = []
    evaluate_script: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "headless": self.headless,
                "remove_selectors": self.remove_selectors,
                "evaluate": self.evaluate_script,
                "timeout": self.js_timeout,
            }
        )

        if self.wait_for_selector:
            kwargs["wait_for_selector"] = self.wait_for_selector

        return kwargs


@register_web_source(
    name="selenium_web",
    url_patterns=["http", "https"],
    loaders={
        "selenium": {
            "class": "SeleniumURLLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["selenium"],
        }
    },
    default_loader="selenium",
    description="Selenium browser automation for complex web interactions",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class SeleniumWebSource(RemoteSource):
    """Selenium browser automation source."""

    # Browser configuration
    browser_name: str = "chrome"
    headless: bool = True

    # Page interaction
    wait_until: Optional[str] = None
    page_load_strategy: str = "normal"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "browser": self.browser_name,
                "headless": self.headless,
                "wait_until": self.wait_until,
                "page_load_strategy": self.page_load_strategy,
            }
        )
        return kwargs


@register_web_source(
    name="chromium_async",
    url_patterns=["http", "https"],
    loaders={
        "chromium": {
            "class": "AsyncChromiumLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["playwright"],
        }
    },
    default_loader="chromium",
    description="Async Chromium loader for high-performance browser automation",
    capabilities=[LoaderCapability.ASYNC_PROCESSING, LoaderCapability.BULK_LOADING],
    priority=8,
)
class ChromiumAsyncSource(RemoteSource):
    """Async Chromium browser source."""

    # Chromium configuration
    headless: bool = True
    user_agent: Optional[str] = None
    viewport: Dict[str, int] = {"width": 1280, "height": 720}

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "headless": self.headless,
                "user_agent": self.user_agent,
                "viewport": self.viewport,
            }
        )
        return kwargs


# =============================================================================
# Recursive and Bulk Web Crawling
# =============================================================================


@register_bulk_source(
    name="recursive_web",
    category=SourceCategory.WEB_SCRAPING,
    loaders={
        "recursive": {
            "class": "RecursiveUrlLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="recursive",
    description="Recursive web crawler with depth control and filtering",
    max_concurrent=6,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
        LoaderCapability.ASYNC_PROCESSING,
    ],
    priority=10,
)
class RecursiveWebSource(RemoteSource):
    """Recursive web crawling source with advanced filtering."""

    # Crawling configuration
    max_depth: int = 2
    max_pages: Optional[int] = None
    prevent_outside: bool = True
    exclude_dirs: List[str] = []

    # Content filtering
    link_regex: Optional[str] = None
    content_filter: Optional[str] = None

    # Processing options
    use_async: bool = True
    continue_on_failure: bool = True
    check_response_status: bool = True

    # Advanced options
    base_url: Optional[str] = None
    metadata_extractor: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Build metadata extractor if enabled
        extractor_func = None
        if self.metadata_extractor:
            extractor_func = extract_metadata_from_html

        kwargs.update(
            {
                "max_depth": self.max_depth,
                "use_async": self.use_async,
                "metadata_extractor": extractor_func,
                "exclude_dirs": self.exclude_dirs,
                "prevent_outside": self.prevent_outside,
                "link_regex": self.link_regex,
                "check_response_status": self.check_response_status,
                "continue_on_failure": self.continue_on_failure,
                "base_url": self.base_url,
            }
        )

        return kwargs


@register_bulk_source(
    name="sitemap_crawler",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "sitemap": {
            "class": "SitemapLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="sitemap",
    description="Sitemap-based website crawler with auto-detection",
    max_concurrent=8,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=10,
)
class SitemapCrawlerSource(RemoteSource):
    """Sitemap-based crawling source with auto-detection."""

    # Sitemap configuration
    sitemap_url: Optional[str] = None  # If None, will auto-detect
    keep_path_segment: Optional[str] = None

    # Filtering options
    filter_urls: List[str] = []
    exclude_patterns: List[str] = []

    # Processing options
    blocksize: Optional[int] = None
    blocknum: int = 0
    parsing_function: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Auto-detect sitemap if not provided
        sitemap_url = self.sitemap_url
        if not sitemap_url:
            sitemap_url = find_sitemap(self.url, self.keep_path_segment)
            if not sitemap_url:
                raise ValueError(f"No sitemap found for {self.url}")

        kwargs.update(
            {
                "web_path": sitemap_url,
                "filter_urls": self.filter_urls,
                "blocksize": self.blocksize,
                "blocknum": self.blocknum,
                "parsing_function": self.parsing_function,
            }
        )

        return kwargs


# =============================================================================
# Documentation Site Sources
# =============================================================================


@register_bulk_source(
    name="readthedocs",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "rtd": {
            "class": "ReadTheDocsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="rtd",
    description="Read the Docs documentation site loader",
    max_concurrent=4,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=9,
)
class ReadTheDocsSource(RemoteSource):
    """Read the Docs documentation source."""

    # RTD configuration
    project_name: str
    version: str = "latest"

    # Processing options
    features: List[str] = ["toc"]

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        # Build RTD URL if not provided
        if not self.url.startswith("http"):
            rtd_url = f"https://{self.project_name}.readthedocs.io/en/{self.version}/"
            kwargs["url"] = rtd_url

        kwargs.update({"features": self.features})

        return kwargs


@register_bulk_source(
    name="docusaurus",
    category=SourceCategory.WEB_DOCUMENTATION,
    loaders={
        "docusaurus": {
            "class": "DocusaurusLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="docusaurus",
    description="Docusaurus documentation site loader",
    max_concurrent=6,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=9,
)
class DocusaurusSource(RemoteSource):
    """Docusaurus documentation site source."""

    # Docusaurus configuration
    base_url: str
    filter_directories: List[str] = []

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"url": self.base_url, "filter_directories": self.filter_directories}
        )
        return kwargs


# =============================================================================
# Advanced Web Scraping Services
# =============================================================================


@register_web_source(
    name="firecrawl",
    url_patterns=["http", "https"],
    loaders={
        "firecrawl": {
            "class": "FireCrawlLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["firecrawl-py"],
        }
    },
    default_loader="firecrawl",
    description="FireCrawl web scraping service with advanced features",
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.METADATA_EXTRACTION,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=8,
)
class FireCrawlSource(RemoteSource):
    """FireCrawl web scraping service source."""

    # FireCrawl configuration
    mode: str = "scrape"  # scrape, crawl, map
    params: Dict[str, Any] = {}

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "api_key": self.get_api_key() if hasattr(self, "get_api_key") else None,
                "mode": self.mode,
                "params": self.params,
            }
        )
        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_web_sources_statistics() -> Dict[str, Any]:
    """Get statistics about web-based sources."""
    registry = enhanced_registry

    # Find web sources by category
    web_scraping = len(registry.find_sources_by_category(SourceCategory.WEB_SCRAPING))
    web_docs = len(registry.find_sources_by_category(SourceCategory.WEB_DOCUMENTATION))

    # Find capability-based statistics
    async_capable = len(
        registry.find_sources_with_capability(LoaderCapability.ASYNC_PROCESSING)
    )
    recursive_capable = len(
        registry.find_sources_with_capability(LoaderCapability.RECURSIVE)
    )
    browser_automation = len(
        [
            name
            for name in registry._sources.keys()
            if any(
                keyword in name for keyword in ["playwright", "selenium", "chromium"]
            )
        ]
    )

    return {
        "web_scraping_sources": web_scraping,
        "web_documentation_sources": web_docs,
        "total_web_sources": web_scraping + web_docs,
        "capabilities": {
            "async_processing": async_capable,
            "recursive_crawling": recursive_capable,
            "browser_automation": browser_automation,
        },
        "sitemap_detection": True,
        "javascript_rendering": browser_automation > 0,
    }


def validate_web_sources() -> bool:
    """Validate web source registrations."""
    registry = enhanced_registry

    required_web_sources = [
        "web_base",
        "async_html",
        "playwright_web",
        "recursive_web",
        "sitemap_crawler",
        "readthedocs",
        "docusaurus",
    ]

    missing = []
    for source_name in required_web_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing web sources: {missing}")
        return False

    print(f"✅ All {len(required_web_sources)} essential web sources registered!")
    return True


# Auto-validate on import
if __name__ == "__main__":
    validate_web_sources()
    stats = get_web_sources_statistics()
    print(f"Web Sources Statistics: {stats}")
