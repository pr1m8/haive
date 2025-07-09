"""Advanced File Loaders for Document Engine.

This module implements advanced file loaders for specialized formats including
BibTeX, ReStructuredText, TSV, Org Mode, MHTML, Visio, and subtitle files.
"""

import logging
from typing import Any, Dict, Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import (
    LocalFileSource,
)

logger = logging.getLogger(__name__)


class BibtexSource(LocalFileSource):
    """BibTeX bibliography file source."""

    def __init__(self, file_path: str, max_docs: Optional[int] = None, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".bib", ".bibtex"], **kwargs
        )
        self.file_path = file_path
        self.max_docs = max_docs

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a BibTeX loader."""
        try:
            from langchain_community.document_loaders import BibtexLoader

            return BibtexLoader(
                file_path=self.file_path,
                max_docs=self.max_docs,
            )

        except ImportError:
            logger.warning(
                "BibtexLoader not available. Install with: pip install bibtexparser"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create BibTeX loader: {e}")
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


class TSVSource(LocalFileSource):
    """Tab-separated values (TSV) file source."""

    def __init__(
        self, file_path: str, csv_args: Optional[Dict[str, Any]] = None, **kwargs
    ):
        super().__init__(
            source_path=file_path, file_extensions=[".tsv", ".tab"], **kwargs
        )
        self.file_path = file_path
        self.csv_args = csv_args or {}
        # Ensure tab delimiter for TSV
        self.csv_args["delimiter"] = "\t"

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a TSV loader."""
        try:
            from langchain_community.document_loaders import CSVLoader

            return CSVLoader(
                file_path=self.file_path,
                csv_args=self.csv_args,
            )

        except Exception as e:
            logger.error(f"Failed to create TSV loader: {e}")
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


class JupyterNotebookSource(LocalFileSource):
    """Jupyter Notebook file source."""

    def __init__(
        self,
        file_path: str,
        include_outputs: bool = False,
        max_output_length: Optional[int] = None,
        **kwargs,
    ):
        super().__init__(source_path=file_path, file_extensions=[".ipynb"], **kwargs)
        self.file_path = file_path
        self.include_outputs = include_outputs
        self.max_output_length = max_output_length

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Jupyter Notebook loader."""
        try:
            from langchain_community.document_loaders import NotebookLoader

            return NotebookLoader(
                path=self.file_path,
                include_outputs=self.include_outputs,
                max_output_length=self.max_output_length,
            )

        except ImportError:
            logger.warning(
                "NotebookLoader not available. Install with: pip install nbconvert"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create notebook loader: {e}")
            return None


class PythonCodeSource(LocalFileSource):
    """Python source code file loader with AST parsing."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".py", ".pyw"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Python code loader."""
        try:
            from langchain_community.document_loaders import PythonLoader

            return PythonLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("PythonLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create Python loader: {e}")
            return None


# Export advanced file sources
__all__ = [
    "BibtexSource",
    "ReStructuredTextSource",
    "TSVSource",
    "OrgModeSource",
    "MHTMLSource",
    "VisioSource",
    "SubtitleSource",
    "JupyterNotebookSource",
    "PythonCodeSource",
]
