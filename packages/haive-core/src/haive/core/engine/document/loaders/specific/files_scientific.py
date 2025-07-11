"""Scientific and Academic File Loaders.

This module contains loaders for scientific formats like BibTeX, LaTeX,
and other academic file types.
"""

import logging
from typing import Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

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


class CONLLUSource(LocalFileSource):
    """CoNLL-U format file source for linguistic annotations."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".conllu", ".conll"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a CoNLL-U loader."""
        try:
            from langchain_community.document_loaders import CoNLLULoader

            return CoNLLULoader(file_path=self.file_path)

        except ImportError:
            logger.warning("CoNLLULoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create CoNLL-U loader: {e}")
            return None


class MathMLSource(LocalFileSource):
    """MathML mathematical markup file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".mml", ".mathml"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a MathML loader."""
        try:
            # Use UnstructuredXMLLoader for MathML
            from langchain_community.document_loaders import UnstructuredXMLLoader

            return UnstructuredXMLLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("UnstructuredXMLLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create MathML loader: {e}")
            return None


class FortranSource(LocalFileSource):
    """Fortran source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".f", ".for", ".f90", ".f95", ".f03", ".f08"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Fortran loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create Fortran loader: {e}")
            return None


class MatlabSource(LocalFileSource):
    """MATLAB/Octave source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".m", ".mat"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a MATLAB loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create MATLAB loader: {e}")
            return None


class RSource(LocalFileSource):
    """R statistical programming file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".r", ".R", ".Rmd", ".Rnw"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an R loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create R loader: {e}")
            return None


# Export scientific file sources
__all__ = [
    "BibtexSource",
    "CONLLUSource",
    "MathMLSource",
    "FortranSource",
    "MatlabSource",
    "RSource",
]
