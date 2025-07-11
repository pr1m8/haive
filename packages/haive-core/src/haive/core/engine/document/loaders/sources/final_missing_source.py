"""Final missing source to complete 231 langchain_community loaders.

This module adds the missing Playwright Web loader that completes our
comprehensive document loader system.
"""

from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_source
from .source_types import LoaderCapability, RemoteSource, SourceCategory

# =============================================================================
# Missing Web Loader
# =============================================================================


@register_source(
    name="playwright_web",
    category=SourceCategory.WEB_SCRAPING,
    loaders={
        "playwright": {
            "class": "PlaywrightWebLoader",
            "speed": "medium",
            "quality": "very_high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["playwright"],
        }
    },
    default_loader="playwright",
    description="Playwright browser automation web scraping loader",
    capabilities=[
        LoaderCapability.WEB_SCRAPING,
        LoaderCapability.ASYNC_PROCESSING,
        LoaderCapability.FILTERING,
    ],
    priority=9,
)
class PlaywrightWebSource(RemoteSource):
    """Playwright web scraping source for dynamic content."""

    source_type: str = "playwright_web"
    headless: bool = Field(True, description="Run browser in headless mode")
    browser_type: str = Field(
        "chromium", description="Browser type (chromium, firefox, webkit)"
    )
    wait_selector: str | None = Field(None, description="CSS selector to wait for")
    timeout: int = Field(30000, description="Page load timeout in milliseconds")


# Auto-register
__all__ = ["PlaywrightWebSource"]
