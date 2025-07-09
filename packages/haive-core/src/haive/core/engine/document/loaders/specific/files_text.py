"""Text and Document File Loaders.

This module contains loaders for text formats like plain text, Markdown,
ReStructuredText, LaTeX, and other document formats.
"""

import logging
from typing import Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

logger = logging.getLogger(__name__)


class TextFileSource(LocalFileSource):
    """Plain text file source."""

    def __init__(self, file_path: str, encoding: str = "utf-8", **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".txt", ".text", ".log"], **kwargs
        )
        self.file_path = file_path
        self.encoding = encoding

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a text file loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(
                file_path=self.file_path,
                encoding=self.encoding,
            )

        except Exception as e:
            logger.error(f"Failed to create text loader: {e}")
            return None


class MarkdownSource(LocalFileSource):
    """Markdown file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".md", ".markdown"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Markdown loader."""
        try:
            from langchain_community.document_loaders import UnstructuredMarkdownLoader

            return UnstructuredMarkdownLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("UnstructuredMarkdownLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create Markdown loader: {e}")
            return None


class ReStructuredTextSource(LocalFileSource):
    """ReStructuredText (RST) file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".rst", ".rest"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a ReStructuredText loader."""
        try:
            from langchain_community.document_loaders import UnstructuredRSTLoader

            return UnstructuredRSTLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredRSTLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create RST loader: {e}")
            return None


class LaTeXSource(LocalFileSource):
    """LaTeX file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".tex", ".latex"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a LaTeX loader."""
        try:
            # Use UnstructuredFileLoader for LaTeX
            from langchain_community.document_loaders import UnstructuredFileLoader

            return UnstructuredFileLoader(file_path=self.file_path, mode="single")

        except ImportError:
            logger.warning("UnstructuredFileLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create LaTeX loader: {e}")
            return None


class OrgModeSource(LocalFileSource):
    """Org Mode file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".org"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Org Mode loader."""
        try:
            from langchain_community.document_loaders import UnstructuredOrgModeLoader

            return UnstructuredOrgModeLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredOrgModeLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Org Mode loader: {e}")
            return None


class AsciiDocSource(LocalFileSource):
    """AsciiDoc file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".adoc", ".asciidoc", ".asc"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an AsciiDoc loader."""
        try:
            # Use UnstructuredFileLoader for AsciiDoc
            from langchain_community.document_loaders import UnstructuredFileLoader

            return UnstructuredFileLoader(file_path=self.file_path, mode="single")

        except ImportError:
            logger.warning("UnstructuredFileLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create AsciiDoc loader: {e}")
            return None


# Export text file sources
__all__ = [
    "TextFileSource",
    "MarkdownSource",
    "ReStructuredTextSource",
    "LaTeXSource",
    "OrgModeSource",
    "AsciiDocSource",
]
