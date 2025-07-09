"""Code and Programming File Loaders.

This module contains loaders for source code, notebooks, and other
programming-related files.
"""

import logging
from typing import Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

logger = logging.getLogger(__name__)


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


class JavaScriptSource(LocalFileSource):
    """JavaScript/TypeScript source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".js", ".jsx", ".ts", ".tsx", ".mjs"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a JavaScript loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create JavaScript loader: {e}")
            return None


class CppSource(LocalFileSource):
    """C++ source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".cpp", ".cc", ".cxx", ".c++", ".hpp", ".h", ".hxx"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a C++ loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create C++ loader: {e}")
            return None


class JavaSource(LocalFileSource):
    """Java source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".java"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Java loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create Java loader: {e}")
            return None


class GoSource(LocalFileSource):
    """Go source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".go"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Go loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create Go loader: {e}")
            return None


class RustSource(LocalFileSource):
    """Rust source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".rs"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Rust loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create Rust loader: {e}")
            return None


class RubySource(LocalFileSource):
    """Ruby source code file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".rb"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a Ruby loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create Ruby loader: {e}")
            return None


class ShellScriptSource(LocalFileSource):
    """Shell script file loader."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path,
            file_extensions=[".sh", ".bash", ".zsh", ".fish"],
            **kwargs,
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a shell script loader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(file_path=self.file_path, encoding="utf-8")
        except Exception as e:
            logger.error(f"Failed to create shell script loader: {e}")
            return None


# Export code file sources
__all__ = [
    "PythonCodeSource",
    "JupyterNotebookSource",
    "JavaScriptSource",
    "CppSource",
    "JavaSource",
    "GoSource",
    "RustSource",
    "RubySource",
    "ShellScriptSource",
]
