"""Advanced Web Loaders for Document Engine.

This module implements advanced web loaders including HuggingFace, PubMed, RSS,
and other specialized web sources.
"""

import logging
from typing import List, Optional
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialType,
    WebUrlSource,
)

logger = logging.getLogger(__name__)


class HuggingFaceSource(WebUrlSource):
    """HuggingFace dataset, model, and space source."""

    def __init__(
        self,
        repo_id: str,
        repo_type: str = "dataset",  # "dataset", "model", or "space"
        revision: Optional[str] = None,
        use_auth_token: Optional[bool] = None,
        **kwargs,
    ):
        hf_url = f"https://huggingface.co/{repo_type}s/{repo_id}"
        super().__init__(source_path=hf_url, **kwargs)
        self.repo_id = repo_id
        self.repo_type = repo_type
        self.revision = revision
        self.use_auth_token = use_auth_token
        self.allowed_domains = ["huggingface.co"]

    def can_handle(self, path: str) -> bool:
        """Check if this is a HuggingFace URL."""
        try:
            parsed = urlparse(path)
            return "huggingface.co" in parsed.netloc
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for HuggingFace URLs."""
        if not self.can_handle(path):
            return 0.0
        return 0.95

    def requires_authentication(self) -> bool:
        """HuggingFace may require authentication for private repos."""
        return self.use_auth_token is not None

    def get_credential_requirements(self) -> List[CredentialType]:
        """HuggingFace needs API token."""
        return [CredentialType.ACCESS_TOKEN]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a HuggingFace loader."""
        try:
            if self.repo_type == "dataset":
                from langchain_community.document_loaders import (
                    HuggingFaceDatasetLoader,
                )

                # Get auth token if needed
                auth_token = None
                if self.credential_manager:
                    cred = self.credential_manager.get_credential("huggingface")
                    if cred and cred.credential_type == CredentialType.ACCESS_TOKEN:
                        auth_token = cred.value

                return HuggingFaceDatasetLoader(
                    path=self.repo_id,
                    page_content_column="text",  # Default column
                    use_auth_token=auth_token if auth_token else self.use_auth_token,
                )

            elif self.repo_type == "model":
                # For model repos, we might want to load the model card
                from langchain_community.document_loaders import TextLoader

                model_card_url = (
                    f"https://huggingface.co/{self.repo_id}/raw/main/README.md"
                )
                return TextLoader(model_card_url)

            else:
                # For spaces, load the space description
                from langchain_community.document_loaders import WebBaseLoader

                return WebBaseLoader([self.source_path])

        except ImportError:
            logger.warning(
                "HuggingFaceDatasetLoader not available. Install with: pip install datasets"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create HuggingFace loader: {e}")
            return None


class PubMedSource(WebUrlSource):
    """PubMed medical research paper source."""

    def __init__(self, query: str, max_results: int = 10, **kwargs):
        source_path = f"pubmed:search:{query}"
        super().__init__(source_path=source_path, **kwargs)
        self.query = query
        self.max_results = max_results

    def can_handle(self, path: str) -> bool:
        """Check if this is a PubMed query or URL."""
        try:
            if path.startswith("pubmed:"):
                return True
            parsed = urlparse(path)
            return "pubmed.ncbi.nlm.nih.gov" in parsed.netloc
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for PubMed sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a PubMed loader."""
        try:
            from langchain_community.document_loaders import PubMedLoader

            return PubMedLoader(
                query=self.query,
                load_max_docs=self.max_results,
            )

        except ImportError:
            logger.warning(
                "PubMedLoader not available. Install with: pip install xmltodict"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create PubMed loader: {e}")
            return None


class RSSFeedSource(WebUrlSource):
    """RSS/Atom feed source."""

    def __init__(self, feed_urls: List[str], max_items: Optional[int] = None, **kwargs):
        super().__init__(source_path=feed_urls[0] if feed_urls else "", **kwargs)
        self.feed_urls = feed_urls
        self.max_items = max_items

    def can_handle(self, path: str) -> bool:
        """Check if this is an RSS/Atom feed URL."""
        try:
            # Simple heuristic - check for common feed patterns
            return any(
                pattern in path.lower()
                for pattern in ["/feed", "/rss", "/atom", ".rss", ".xml", "feed.xml"]
            )
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for RSS feeds."""
        if not self.can_handle(path):
            return 0.0
        return 0.8

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an RSS feed loader."""
        try:
            from langchain_community.document_loaders import RSSFeedLoader

            return RSSFeedLoader(
                urls=self.feed_urls,
                max_items_per_feed=self.max_items,
            )

        except ImportError:
            logger.warning(
                "RSSFeedLoader not available. Install with: pip install feedparser"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create RSS feed loader: {e}")
            return None


class NewsURLSource(WebUrlSource):
    """News article source with specialized extraction."""

    def __init__(self, urls: List[str], **kwargs):
        super().__init__(source_path=urls[0] if urls else "", **kwargs)
        self.urls = urls

    def can_handle(self, path: str) -> bool:
        """Check if this is a news URL."""
        try:
            parsed = urlparse(path)
            # Common news domains
            news_domains = [
                "nytimes.com",
                "wsj.com",
                "bbc.com",
                "cnn.com",
                "reuters.com",
                "bloomberg.com",
                "theguardian.com",
            ]
            return any(domain in parsed.netloc for domain in news_domains)
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for news URLs."""
        if not self.can_handle(path):
            return 0.0
        return 0.85

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a news URL loader."""
        try:
            from langchain_community.document_loaders import NewsURLLoader

            return NewsURLLoader(urls=self.urls)

        except ImportError:
            logger.warning(
                "NewsURLLoader not available. Install with: pip install newspaper3k"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create news URL loader: {e}")
            return None


class SeleniumWebSource(WebUrlSource):
    """Web source using Selenium for complex JavaScript sites."""

    def __init__(self, url: str, wait_time: int = 10, headless: bool = True, **kwargs):
        super().__init__(source_path=url, **kwargs)
        self.url = url
        self.wait_time = wait_time
        self.headless = headless

    def can_handle(self, path: str) -> bool:
        """Check if this is a web URL suitable for Selenium."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["http", "https"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Selenium (lower priority)."""
        if not self.can_handle(path):
            return 0.0
        return 0.5  # Lower than other web loaders

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Selenium web loader."""
        try:
            from langchain_community.document_loaders import SeleniumURLLoader

            return SeleniumURLLoader(
                urls=[self.url],
                headless=self.headless,
            )

        except ImportError:
            logger.warning(
                "SeleniumURLLoader not available. Install with: pip install selenium"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Selenium loader: {e}")
            return None


class RecursiveURLSource(WebUrlSource):
    """Recursive web crawler source."""

    def __init__(
        self,
        url: str,
        max_depth: int = 2,
        exclude_patterns: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(source_path=url, **kwargs)
        self.url = url
        self.max_depth = max_depth
        self.exclude_patterns = exclude_patterns or []

    def can_handle(self, path: str) -> bool:
        """Check if this is a web URL suitable for recursive crawling."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["http", "https"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for recursive crawling (lower priority)."""
        if not self.can_handle(path):
            return 0.0
        return 0.4  # Lower than single-page loaders

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a recursive URL loader."""
        try:
            from langchain_community.document_loaders import RecursiveUrlLoader

            return RecursiveUrlLoader(
                url=self.url,
                max_depth=self.max_depth,
                exclude_dirs=self.exclude_patterns,
            )

        except ImportError:
            logger.warning("RecursiveUrlLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create recursive URL loader: {e}")
            return None


class SitemapSource(WebUrlSource):
    """Sitemap-based web crawler source."""

    def __init__(
        self, sitemap_url: str, filter_urls: Optional[List[str]] = None, **kwargs
    ):
        super().__init__(source_path=sitemap_url, **kwargs)
        self.sitemap_url = sitemap_url
        self.filter_urls = filter_urls

    def can_handle(self, path: str) -> bool:
        """Check if this is a sitemap URL."""
        try:
            return "sitemap" in path.lower() or path.endswith(".xml")
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for sitemap URLs."""
        if not self.can_handle(path):
            return 0.0
        return 0.9 if "sitemap" in path.lower() else 0.7

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a sitemap loader."""
        try:
            from langchain_community.document_loaders import SitemapLoader

            return SitemapLoader(
                web_path=self.sitemap_url,
                filter_urls=self.filter_urls,
            )

        except ImportError:
            logger.warning("SitemapLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create sitemap loader: {e}")
            return None


# Export advanced web sources
__all__ = [
    "HuggingFaceSource",
    "PubMedSource",
    "RSSFeedSource",
    "NewsURLSource",
    "SeleniumWebSource",
    "RecursiveURLSource",
    "SitemapSource",
]
