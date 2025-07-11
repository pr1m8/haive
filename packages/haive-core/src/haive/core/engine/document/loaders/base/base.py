"""Base Document Loader Classes.

This module provides base classes for document loaders used by the document engine.
"""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from langchain_core.documents import Document
from pydantic import BaseModel

# Removed unused imports

logger = logging.getLogger(__name__)


class BaseDocumentLoader(ABC):
    """Abstract base class for document loaders."""

    def __init__(
        self, source: str | Path, loader_options: dict[str, Any] | None = None
    ):
        """Initialize the loader.

        Args:
            source: Source to load from
            loader_options: Optional loader-specific options
        """
        self.source = source
        self.loader_options = loader_options or {}

    @abstractmethod
    def load(self) -> list[Document]:
        """Load documents from the source.

        Returns:
            List of loaded documents
        """

    @abstractmethod
    def lazy_load(self) -> list[Document]:
        """Lazily load documents from the source.

        Returns:
            Iterator of loaded documents
        """


class SimpleDocumentLoader(BaseDocumentLoader):
    """Simple document loader for basic file types."""

    def load(self) -> list[Document]:
        """Load documents from the source."""
        try:
            if isinstance(self.source, dict):
                # Handle dict sources as text input
                content = str(self.source)
                return [
                    Document(
                        page_content=content,
                        metadata={
                            "source": "dict_input",
                            "loader_name": "SimpleDocumentLoader",
                        },
                    )
                ]

            source_path = Path(self.source)

            if source_path.is_file():
                return self._load_file(source_path)
            if source_path.is_dir():
                return self._load_directory(source_path)
            # Assume it's a URL or other remote source
            return self._load_remote(str(self.source))

        except Exception as e:
            logger.exception(f"Failed to load from {self.source}: {e}")
            return []

    def lazy_load(self) -> list[Document]:
        """Lazily load documents (same as load for this simple implementation)."""
        return self.load()

    def _load_file(self, file_path: Path) -> list[Document]:
        """Load a single file."""
        try:
            # Read file content
            if file_path.suffix.lower() in [
                ".txt",
                ".md",
                ".py",
                ".js",
                ".html",
                ".csv",
            ]:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
            else:
                # For binary files, just include metadata
                content = f"[Binary file: {file_path.name}]"

            metadata = {
                "source": str(file_path),
                "file_name": file_path.name,
                "file_extension": file_path.suffix,
                "file_size": file_path.stat().st_size,
                "loader_name": "SimpleDocumentLoader",
            }

            return [Document(page_content=content, metadata=metadata)]

        except Exception as e:
            logger.exception(f"Failed to load file {file_path}: {e}")
            return []

    def _load_directory(self, dir_path: Path) -> list[Document]:
        """Load all files from a directory."""
        documents = []

        try:
            # Get file patterns from options
            include_patterns = self.loader_options.get("include_patterns", ["*"])
            exclude_patterns = self.loader_options.get("exclude_patterns", [])
            recursive = self.loader_options.get("recursive", True)

            # Find files
            if recursive:
                files = []
                for pattern in include_patterns:
                    files.extend(dir_path.rglob(pattern))
            else:
                files = []
                for pattern in include_patterns:
                    files.extend(dir_path.glob(pattern))

            # Filter out excluded files
            for exclude_pattern in exclude_patterns:
                if recursive:
                    excluded = set(dir_path.rglob(exclude_pattern))
                else:
                    excluded = set(dir_path.glob(exclude_pattern))
                files = [f for f in files if f not in excluded]

            # Load each file
            for file_path in files:
                if file_path.is_file():
                    file_docs = self._load_file(file_path)
                    documents.extend(file_docs)

            logger.info(f"Loaded {len(documents)} documents from {dir_path}")
            return documents

        except Exception as e:
            logger.exception(f"Failed to load directory {dir_path}: {e}")
            return []

    def _load_remote(self, url: str) -> list[Document]:
        """Load from a remote URL (placeholder implementation)."""
        try:
            if url.startswith(("http://", "https://")):
                # Simple web content loading
                try:
                    import requests

                    response = requests.get(url, timeout=30)
                    response.raise_for_status()

                    content = response.text
                    metadata = {
                        "source": url,
                        "content_type": response.headers.get("content-type", ""),
                        "status_code": response.status_code,
                        "loader_name": "SimpleDocumentLoader",
                    }

                    return [Document(page_content=content, metadata=metadata)]

                except ImportError:
                    logger.warning("requests library not available for URL loading")
                    return []
                except Exception as e:
                    logger.exception(f"Failed to load URL {url}: {e}")
                    return []
            else:
                # Handle other protocols as text
                content = f"[Unsupported source: {url}]"
                metadata = {
                    "source": url,
                    "loader_name": "SimpleDocumentLoader",
                    "note": "Unsupported source type",
                }
                return [Document(page_content=content, metadata=metadata)]

        except Exception as e:
            logger.exception(f"Failed to load remote source {url}: {e}")
            return []


class TextDocumentLoader(BaseDocumentLoader):
    """Document loader for plain text input."""

    def load(self) -> list[Document]:
        """Load documents from text input."""
        content = str(self.source)
        metadata = {
            "source": "text_input",
            "loader_name": "TextDocumentLoader",
            "character_count": len(content),
        }

        return [Document(page_content=content, metadata=metadata)]

    def lazy_load(self) -> list[Document]:
        """Lazily load documents (same as load for text)."""
        return self.load()


class LoaderConfig(ABC):
    """Config for a loader (legacy interface)."""

    # loader
    @abstractmethod
    def load(self, input: dict[str, Any]) -> dict[str, Any]:
        """Load the data from the input."""
        raise NotImplementedError("Subclasses must implement this method.")

    @classmethod
    def from_config(cls, config: BaseModel) -> "LoaderConfig":
        """Create a loader from a config."""
        return cls(**config.model_dump())

    @classmethod
    def from_dict(cls, config: dict) -> "LoaderConfig":
        """Create a loader from a dict."""
        return cls(**config)

    @classmethod
    def create_runnable(cls, config: BaseModel) -> "LoaderConfig":
        """Create a runnable from a config."""
        return cls.from_config(config)


# Export base classes
__all__ = [
    "BaseDocumentLoader",
    "LoaderConfig",  # Legacy
    "SimpleDocumentLoader",
    "TextDocumentLoader",
]
