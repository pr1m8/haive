"""Media and Special Format File Loaders.

This module contains loaders for media files like images, PDFs, subtitles,
and other special format files.
"""

import logging
from typing import Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

logger = logging.getLogger(__name__)


class PDFSource(LocalFileSource):
    """PDF document source with multiple loading strategies."""

    def __init__(
        self,
        file_path: str,
        strategy: str = "pymupdf",
        extract_images: bool = False,
        **kwargs,
    ):
        super().__init__(source_path=file_path, file_extensions=[".pdf"], **kwargs)
        self.file_path = file_path
        self.strategy = strategy
        self.extract_images = extract_images

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a PDF loader based on strategy."""
        try:
            if self.strategy == "pymupdf":
                from langchain_community.document_loaders import PyMuPDFLoader

                return PyMuPDFLoader(
                    file_path=self.file_path,
                    extract_images=self.extract_images,
                )

            elif self.strategy == "pdfplumber":
                from langchain_community.document_loaders import PDFPlumberLoader

                return PDFPlumberLoader(file_path=self.file_path)

            elif self.strategy == "pypdf":
                from langchain_community.document_loaders import PyPDFLoader

                return PyPDFLoader(file_path=self.file_path)

            elif self.strategy == "unstructured":
                from langchain_community.document_loaders import UnstructuredPDFLoader

                return UnstructuredPDFLoader(file_path=self.file_path)

            else:
                # Default to PyMuPDF
                from langchain_community.document_loaders import PyMuPDFLoader

                return PyMuPDFLoader(file_path=self.file_path)

        except ImportError as e:
            logger.warning(f"PDF loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create PDF loader: {e}")
            return None


class ImageSource(LocalFileSource):
    """Image file source with OCR capabilities."""

    def __init__(self, file_path: str, strategy: str = "unstructured", **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
            **kwargs,
        )
        self.file_path = file_path
        self.strategy = strategy

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an image loader with OCR."""
        try:
            if self.strategy == "unstructured":
                from langchain_community.document_loaders import UnstructuredImageLoader

                return UnstructuredImageLoader(file_path=self.file_path)

            else:
                # Default to unstructured
                from langchain_community.document_loaders import UnstructuredImageLoader

                return UnstructuredImageLoader(file_path=self.file_path)

        except ImportError as e:
            logger.warning(f"Image loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create image loader: {e}")
            return None


class SubtitleSource(LocalFileSource):
    """Subtitle (SRT/VTT) file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".srt", ".vtt", ".sub", ".ass"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a subtitle loader."""
        try:
            from langchain_community.document_loaders import SRTLoader

            return SRTLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("SRTLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create subtitle loader: {e}")
            return None


class EPubSource(LocalFileSource):
    """EPub e-book file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".epub"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an EPub loader."""
        try:
            from langchain_community.document_loaders import UnstructuredEPubLoader

            return UnstructuredEPubLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredEPubLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create EPub loader: {e}")
            return None


class MHTMLSource(LocalFileSource):
    """MHTML (MIME HTML) archive file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".mhtml", ".mht"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an MHTML loader."""
        try:
            from langchain_community.document_loaders import MHTMLLoader

            return MHTMLLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("MHTMLLoader not available")
            # Fallback to UnstructuredHTMLLoader
            try:
                from langchain_community.document_loaders import UnstructuredHTMLLoader

                return UnstructuredHTMLLoader(file_path=self.file_path)
            except ImportError:
                logger.warning("UnstructuredHTMLLoader not available")
                return None
        except Exception as e:
            logger.error(f"Failed to create MHTML loader: {e}")
            return None


class HTMLSource(LocalFileSource):
    """HTML file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".html", ".htm"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an HTML loader."""
        try:
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            return UnstructuredHTMLLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("UnstructuredHTMLLoader not available")
            # Fallback to BSHTMLLoader
            try:
                from langchain_community.document_loaders import BSHTMLLoader

                return BSHTMLLoader(file_path=self.file_path)
            except ImportError:
                logger.warning("BSHTMLLoader not available")
                return None
        except Exception as e:
            logger.error(f"Failed to create HTML loader: {e}")
            return None


class CHMSource(LocalFileSource):
    """Microsoft Compiled HTML Help (CHM) file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".chm"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a CHM loader."""
        try:
            # Try UnstructuredFileLoader as a general fallback
            from langchain_community.document_loaders import UnstructuredFileLoader

            return UnstructuredFileLoader(
                file_path=self.file_path,
                mode="elements",
            )

        except ImportError:
            logger.warning("UnstructuredFileLoader not available")
            return None
        except Exception as e:
            logger.error(f"Failed to create CHM loader: {e}")
            return None


# Export media file sources
__all__ = [
    "PDFSource",
    "ImageSource",
    "SubtitleSource",
    "EPubSource",
    "MHTMLSource",
    "HTMLSource",
    "CHMSource",
]
