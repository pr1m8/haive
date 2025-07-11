"""Service and Application Loaders for Document Engine.

This module implements loaders for various services and applications including
Notion, Obsidian, Slack, and other productivity tools.
"""

import logging
from pathlib import Path
from typing import List, Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    CredentialType,
    EnhancedSource,
    SourceType,
)

logger = logging.getLogger(__name__)


class NotionSource(EnhancedSource):
    """Notion workspace source."""

    source_type: SourceType = SourceType.LOCAL_DIRECTORY

    def __init__(
        self,
        database_id: Optional[str] = None,
        page_ids: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(source_path="notion://workspace", **kwargs)
        self.database_id = database_id
        self.page_ids = page_ids or []

    def can_handle(self, path: str) -> bool:
        """Check if this is a Notion source."""
        return path.startswith("notion://") or "notion.so" in path

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Notion sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """Notion requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """Notion needs API key."""
        return [CredentialType.API_KEY]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Notion loader."""
        try:
            from langchain_community.document_loaders import (
                NotionDBLoader,
                NotionDirectoryLoader,
            )

            # Get Notion API key
            notion_key = None
            if self.credential_manager:
                cred = self.credential_manager.get_credential("notion")
                if cred and cred.credential_type == CredentialType.API_KEY:
                    notion_key = cred.value

            if not notion_key:
                logger.error("Notion API key required")
                return None

            if self.database_id:
                # Load from specific database
                return NotionDBLoader(
                    integration_token=notion_key,
                    database_id=self.database_id,
                )
            else:
                # Load from directory export
                # This would need a local path to Notion export
                logger.warning("NotionDirectoryLoader requires local export path")
                return None

        except ImportError:
            logger.warning(
                "Notion loaders not available. Install with: pip install notion-client"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Notion loader: {e}")
            return None


class ObsidianSource(EnhancedSource):
    """Obsidian vault source."""

    source_type: SourceType = SourceType.LOCAL_DIRECTORY

    def __init__(self, vault_path: str, encoding: str = "utf-8", **kwargs):
        super().__init__(source_path=vault_path, **kwargs)
        self.vault_path = vault_path
        self.encoding = encoding

    def can_handle(self, path: str) -> bool:
        """Check if this is an Obsidian vault."""
        try:
            p = Path(path)
            # Check for .obsidian directory
            return p.is_dir() and (p / ".obsidian").exists()
        except Exception:
            return False

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Obsidian vaults."""
        if not self.can_handle(path):
            return 0.0
        return 0.95

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Obsidian loader."""
        try:
            from langchain_community.document_loaders import ObsidianLoader

            return ObsidianLoader(
                path=self.vault_path,
                encoding=self.encoding,
            )

        except ImportError:
            logger.warning("ObsidianLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Obsidian loader: {e}")
            return None


class SlackSource(EnhancedSource):
    """Slack workspace source."""

    source_type: SourceType = SourceType.WEB_API

    def __init__(
        self,
        channel_id: Optional[str] = None,
        export_path: Optional[str] = None,
        **kwargs,
    ):
        super().__init__(source_path="slack://workspace", **kwargs)
        self.channel_id = channel_id
        self.export_path = export_path

    def can_handle(self, path: str) -> bool:
        """Check if this is a Slack source."""
        return path.startswith("slack://") or "slack.com" in path

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Slack sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def requires_authentication(self) -> bool:
        """Slack API requires authentication."""
        return self.export_path is None

    def get_credential_requirements(self) -> List[CredentialType]:
        """Slack needs OAuth token."""
        return [CredentialType.OAUTH2, CredentialType.ACCESS_TOKEN]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Slack loader."""
        try:
            if self.export_path:
                # Load from Slack export
                from langchain_community.document_loaders import SlackDirectoryLoader

                return SlackDirectoryLoader(
                    zip_path=self.export_path,
                )
            else:
                # Load via API (would need implementation)
                logger.warning("Slack API loader not yet implemented")
                return None

        except ImportError:
            logger.warning("Slack loaders not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Slack loader: {e}")
            return None


class GutenbergSource(EnhancedSource):
    """Project Gutenberg book source."""

    source_type: SourceType = SourceType.WEB_URL

    def __init__(
        self, book_url: Optional[str] = None, book_id: Optional[int] = None, **kwargs
    ):
        source_path = book_url or f"gutenberg://book/{book_id}"
        super().__init__(source_path=source_path, **kwargs)
        self.book_url = book_url
        self.book_id = book_id

    def can_handle(self, path: str) -> bool:
        """Check if this is a Gutenberg source."""
        return "gutenberg.org" in path or path.startswith("gutenberg://")

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Gutenberg sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Gutenberg loader."""
        try:
            from langchain_community.document_loaders import GutenbergLoader

            if self.book_url:
                return GutenbergLoader(self.book_url)
            else:
                # Could construct URL from book ID
                logger.warning("GutenbergLoader requires book URL")
                return None

        except ImportError:
            logger.warning("GutenbergLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Gutenberg loader: {e}")
            return None


class ConfluenceSource(EnhancedSource):
    """Atlassian Confluence source."""

    source_type: SourceType = SourceType.WEB_API

    def __init__(
        self,
        url: str,
        space_key: Optional[str] = None,
        page_ids: Optional[List[str]] = None,
        **kwargs,
    ):
        super().__init__(source_path=url, **kwargs)
        self.url = url
        self.space_key = space_key
        self.page_ids = page_ids or []

    def can_handle(self, path: str) -> bool:
        """Check if this is a Confluence URL."""
        return "confluence" in path or "atlassian.net" in path

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Confluence sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.85

    def requires_authentication(self) -> bool:
        """Confluence requires authentication."""
        return True

    def get_credential_requirements(self) -> List[CredentialType]:
        """Confluence needs username/password or API token."""
        return [CredentialType.USERNAME_PASSWORD, CredentialType.API_KEY]

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Confluence loader."""
        try:
            from langchain_community.document_loaders import ConfluenceLoader

            # Get credentials
            username = None
            api_key = None

            if self.credential_manager:
                cred = self.credential_manager.get_credential("confluence")
                if cred:
                    if cred.credential_type == CredentialType.USERNAME_PASSWORD:
                        # Assume format "username:password"
                        if ":" in cred.value:
                            username, api_key = cred.value.split(":", 1)
                    elif cred.credential_type == CredentialType.API_KEY:
                        api_key = cred.value

            if not (username and api_key):
                logger.error("Confluence credentials required")
                return None

            return ConfluenceLoader(
                url=self.url,
                username=username,
                api_key=api_key,
                space_key=self.space_key,
                page_ids=self.page_ids,
            )

        except ImportError:
            logger.warning(
                "ConfluenceLoader not available. Install with: pip install atlassian-python-api"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Confluence loader: {e}")
            return None


class ReadTheDocsSource(EnhancedSource):
    """Read the Docs documentation source."""

    source_type: SourceType = SourceType.WEB_URL

    def __init__(
        self, project_url: str, features: Optional[List[str]] = None, **kwargs
    ):
        super().__init__(source_path=project_url, **kwargs)
        self.project_url = project_url
        self.features = features or ["page_content", "metadata"]

    def can_handle(self, path: str) -> bool:
        """Check if this is a Read the Docs URL."""
        return "readthedocs.io" in path or "readthedocs.org" in path

    def get_confidence_score(self, path: str) -> float:
        """Get confidence score for Read the Docs sources."""
        if not self.can_handle(path):
            return 0.0
        return 0.9

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Read the Docs loader."""
        try:
            # Extract project name from URL
            # e.g., https://project.readthedocs.io/ -> project
            import re

            from langchain_community.document_loaders import ReadTheDocsLoader

            match = re.search(r"https?://([^.]+)\.readthedocs", self.project_url)
            if match:
                match.group(1)

                # ReadTheDocsLoader expects a local path to downloaded docs
                # This is a limitation - would need to download first
                logger.warning(
                    "ReadTheDocsLoader requires local path to downloaded docs"
                )
                return None
            else:
                logger.error("Could not extract project name from URL")
                return None

        except ImportError:
            logger.warning("ReadTheDocsLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create Read the Docs loader: {e}")
            return None


# Export service sources
__all__ = [
    "NotionSource",
    "ObsidianSource",
    "SlackSource",
    "GutenbergSource",
    "ConfluenceSource",
    "ReadTheDocsSource",
]
