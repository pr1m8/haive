"""Web Loaders for Document Engine.

This module implements specialized web loaders for different types of web content
including GitHub, ArXiv, Wikipedia, and general web pages.
"""

import logging
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialType,
    WebUrlSource,
)

logger = logging.getLogger(__name__)


class GitHubSource(WebUrlSource):
    """GitHub repository and content source."""

    def __init__(
        self,
        repo_url: str,
        file_filter: Optional[List[str]] = None,
        include_issues: bool = False,
        include_pull_requests: bool = False,
        **kwargs,
    ):
        super().__init__(source_path=repo_url, **kwargs)
        self.repo_url = repo_url
        self.file_filter = file_filter or []
        self.include_issues = include_issues
        self.include_pull_requests = include_pull_requests
        self.allowed_domains = ["github.com", "api.github.com"]

    def can_handle(self, path: str) -> bool:
        """Check if this is a GitHub URL."""
        try:
            parsed = urlparse(path)
            return "github.com" in parsed.netloc
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for GitHub URLs."""
        if not self.can_handle(path):
            return 0.0
        return 0.95

    def requires_authentication(self) -> bool:
        """GitHub may require authentication for private repos."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """GitHub needs API token."""
        return [CredentialType.ACCESS_TOKEN, CredentialType.API_KEY]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a GitHub loader."""
        try:
            from langchain_community.document_loaders import (
                GitHubIssuesLoader,
                GitLoader,
            )

            # Get GitHub token if available
            github_token = None
            if self.credential_manager:
                cred = self.credential_manager.get_credential("github")
                if cred and cred.credential_type in [
                    CredentialType.ACCESS_TOKEN,
                    CredentialType.API_KEY,
                ]:
                    github_token = cred.value

            # Parse GitHub URL to extract repo info
            parsed = urlparse(self.repo_url)
            path_parts = parsed.path.strip("/").split("/")

            if len(path_parts) >= 2:
                repo_owner = path_parts[0]
                repo_name = path_parts[1]

                if self.include_issues:
                    return GitHubIssuesLoader(
                        repo=f"{repo_owner}/{repo_name}",
                        access_token=github_token,
                        include_prs=self.include_pull_requests,
                    )
                else:
                    # Use GitLoader for repository content
                    return GitLoader(
                        clone_url=self.repo_url,
                        repo_path=f"/tmp/git_repos/{repo_owner}_{repo_name}",
                        file_filter=lambda file_path: (
                            any(pattern in file_path for pattern in self.file_filter)
                            if self.file_filter
                            else True
                        ),
                    )
            else:
                raise ValueError(f"Invalid GitHub URL format: {self.repo_url}")

        except ImportError:
            logger.warning(
                "GitHub loaders not available. Install with: pip install pygithub gitpython"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create GitHub loader: {e}")
            return None


class ArXivSource(WebUrlSource):
    """ArXiv research paper source."""

    def __init__(
        self,
        query: Optional[str] = None,
        paper_id: Optional[str] = None,
        max_results: int = 10,
        **kwargs,
    ):
        source_path = f"arxiv:{paper_id}" if paper_id else f"arxiv:search:{query}"
        super().__init__(source_path=source_path, **kwargs)
        self.query = query
        self.paper_id = paper_id
        self.max_results = max_results

    def can_handle(self, path: str) -> bool:
        """Check if this is an ArXiv identifier or URL."""
        try:
            if path.startswith("arxiv:"):
                return True
            parsed = urlparse(path)
            return "arxiv.org" in parsed.netloc
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for ArXiv sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an ArXiv loader."""
        try:
            from langchain_community.document_loaders import ArxivLoader

            if self.paper_id:
                # Load specific paper
                return ArxivLoader(query=self.paper_id, load_max_docs=1)
            elif self.query:
                # Search for papers
                return ArxivLoader(query=self.query, load_max_docs=self.max_results)
            else:
                raise ValueError("Either paper_id or query must be provided")

        except ImportError:
            logger.warning("ArxivLoader not available. Install with: pip install arxiv")
            return None
        except Exception as e:
            logger.error(f"Failed to create ArXiv loader: {e}")
            return None


class WikipediaSource(WebUrlSource):
    """Wikipedia article source."""

    def __init__(
        self,
        query: Optional[str] = None,
        page_title: Optional[str] = None,
        lang: str = "en",
        load_max_docs: int = 1,
        **kwargs,
    ):
        source_path = f"wikipedia:{lang}:{page_title or query}"
        super().__init__(source_path=source_path, **kwargs)
        self.query = query
        self.page_title = page_title
        self.lang = lang
        self.load_max_docs = load_max_docs

    def can_handle(self, path: str) -> bool:
        """Check if this is a Wikipedia URL or identifier."""
        try:
            if path.startswith("wikipedia:"):
                return True
            parsed = urlparse(path)
            return "wikipedia.org" in parsed.netloc
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Wikipedia sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Wikipedia loader."""
        try:
            from langchain_community.document_loaders import WikipediaLoader

            search_query = self.page_title or self.query
            if not search_query:
                raise ValueError("Either page_title or query must be provided")

            return WikipediaLoader(
                query=search_query,
                lang=self.lang,
                load_max_docs=self.load_max_docs,
            )

        except ImportError:
            logger.warning(
                "WikipediaLoader not available. Install with: pip install wikipedia"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Wikipedia loader: {e}")
            return None


class PlaywrightWebSource(WebUrlSource):
    """Advanced web source using Playwright for JavaScript-heavy sites."""

    def __init__(
        self,
        urls: List[str],
        wait_until: str = "networkidle",
        headless: bool = True,
        **kwargs,
    ):
        super().__init__(source_path=urls[0] if urls else "", **kwargs)
        self.urls = urls
        self.wait_until = wait_until
        self.headless = headless

    def can_handle(self, path: str) -> bool:
        """Check if this is a web URL suitable for Playwright."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["http", "https"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for web URLs (lower priority than basic web)."""
        if not self.can_handle(path):
            return 0.0
        return 0.6  # Lower than basic web loader for auto-selection

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Playwright web loader."""
        try:
            from langchain_community.document_loaders import PlaywrightURLLoader

            return PlaywrightURLLoader(
                urls=self.urls,
                remove_selectors=["header", "footer", "nav", ".sidebar"],
                continue_on_failure=True,
                headless=self.headless,
            )

        except ImportError:
            logger.warning(
                "PlaywrightURLLoader not available. Install with: pip install playwright"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Playwright loader: {e}")
            return None


class BasicWebSource(WebUrlSource):
    """Basic web source for simple HTML pages."""

    def __init__(
        self,
        web_paths: List[str],
        requests_kwargs: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(source_path=web_paths[0] if web_paths else "", **kwargs)
        self.web_paths = web_paths
        self.requests_kwargs = requests_kwargs or {}

    def can_handle(self, path: str) -> bool:
        """Check if this is a web URL."""
        try:
            parsed = urlparse(path)
            return parsed.scheme in ["http", "https"]
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for web URLs."""
        if not self.can_handle(path):
            return 0.0
        return 0.7

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a basic web loader."""
        try:
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(
                web_paths=self.web_paths,
                requests_kwargs=self.requests_kwargs,
            )

        except ImportError:
            logger.warning("WebBaseLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create web loader: {e}")
            return None


# Export web sources
__all__ = [
    "GitHubSource",
    "ArXivSource",
    "WikipediaSource",
    "PlaywrightWebSource",
    "BasicWebSource",
]
