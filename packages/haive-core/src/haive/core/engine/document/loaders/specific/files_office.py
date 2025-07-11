"""Microsoft Office and Office-like File Loaders.

This module contains loaders for Office formats like Word, Excel, PowerPoint,
and their open-source equivalents.
"""

import logging
from typing import Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

logger = logging.getLogger(__name__)


class WordDocumentSource(LocalFileSource):
    """Microsoft Word document source."""

    def __init__(self, file_path: str, strategy: str = "docx2txt", **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".docx", ".doc", ".dot", ".dotx"],
            **kwargs,
        )
        self.file_path = file_path
        self.strategy = strategy

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Word document loader."""
        try:
            if self.strategy == "docx2txt":
                from langchain_community.document_loaders import Docx2txtLoader

                return Docx2txtLoader(file_path=self.file_path)

            elif self.strategy == "unstructured":
                from langchain_community.document_loaders import (
                    UnstructuredWordDocumentLoader,
                )

                return UnstructuredWordDocumentLoader(file_path=self.file_path)

            else:
                # Default to docx2txt
                from langchain_community.document_loaders import Docx2txtLoader

                return Docx2txtLoader(file_path=self.file_path)

        except ImportError as e:
            logger.warning(f"Word document loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create Word document loader: {e}")
            return None


class ExcelSource(LocalFileSource):
    """Microsoft Excel document source."""

    def __init__(self, file_path: str, sheet_name: Optional[str] = None, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".xlsx", ".xls", ".xlsm", ".xlt", ".xltx"],
            **kwargs,
        )
        self.file_path = file_path
        self.sheet_name = sheet_name

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an Excel loader."""
        try:
            from langchain_community.document_loaders import UnstructuredExcelLoader

            return UnstructuredExcelLoader(
                file_path=self.file_path, mode="elements"  # Extract structured elements
            )

        except ImportError as e:
            logger.warning(f"Excel loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create Excel loader: {e}")
            return None


class PowerPointSource(LocalFileSource):
    """Microsoft PowerPoint document source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".pptx", ".ppt", ".pps", ".ppsx"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a PowerPoint loader."""
        try:
            from langchain_community.document_loaders import (
                UnstructuredPowerPointLoader,
            )

            return UnstructuredPowerPointLoader(file_path=self.file_path)

        except ImportError as e:
            logger.warning(f"PowerPoint loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create PowerPoint loader: {e}")
            return None


class OpenDocumentTextSource(LocalFileSource):
    """OpenDocument Text (ODT) file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".odt", ".ott"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an ODT loader."""
        try:
            from langchain_community.document_loaders import UnstructuredODTLoader

            return UnstructuredODTLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredODTLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create ODT loader: {e}")
            return None


class VisioSource(LocalFileSource):
    """Microsoft Visio diagram file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".vsdx", ".vsd"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Visio loader."""
        try:
            # Try UnstructuredFileLoader as a general fallback
            from langchain_community.document_loaders import UnstructuredFileLoader

            return UnstructuredFileLoader(
                file_path=self.file_path,
                mode="elements",
            )

        except ImportError:
            logger.warning(
                "UnstructuredFileLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create Visio loader: {e}")
            return None


class RTFSource(LocalFileSource):
    """Rich Text Format (RTF) file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".rtf"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an RTF loader."""
        try:
            from langchain_community.document_loaders import UnstructuredRTFLoader

            return UnstructuredRTFLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredRTFLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create RTF loader: {e}")
            return None


# Export office file sources
__all__ = [
    "WordDocumentSource",
    "ExcelSource",
    "PowerPointSource",
    "OpenDocumentTextSource",
    "VisioSource",
    "RTFSource",
]
