"""Data File Loaders.

This module contains loaders for data formats like CSV, JSON, XML, YAML, TOML,
and other structured data files.
"""

import logging
from typing import Any, Dict, Optional

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.loaders.sources.implementation import LocalFileSource

logger = logging.getLogger(__name__)


class CSVSource(LocalFileSource):
    """CSV file source."""

    def __init__(
        self, file_path: str, csv_args: Optional[Dict[str, Any]] = None, **kwargs
    ):
        super().__init__(source_path=file_path, file_extensions=[".csv"], **kwargs)
        self.file_path = file_path
        self.csv_args = csv_args or {}

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a CSV loader."""
        try:
            from langchain_community.document_loaders import CSVLoader

            return CSVLoader(
                file_path=self.file_path,
                csv_args=self.csv_args,
            )

        except Exception as e:
            logger.error(f"Failed to create CSV loader: {e}")
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


class JSONSource(LocalFileSource):
    """JSON file source."""

    def __init__(self, file_path: str, jq_schema: str = ".", **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".json", ".jsonl"], **kwargs
        )
        self.file_path = file_path
        self.jq_schema = jq_schema

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a JSON loader."""
        try:
            from langchain_community.document_loaders import JSONLoader

            return JSONLoader(
                file_path=self.file_path,
                jq_schema=self.jq_schema,
            )

        except ImportError as e:
            logger.warning(f"JSON loader dependency not available: {e}")
            return None
        except Exception as e:
            logger.error(f"Failed to create JSON loader: {e}")
            return None


class XMLSource(LocalFileSource):
    """XML file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".xml"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create an XML loader."""
        try:
            from langchain_community.document_loaders import UnstructuredXMLLoader

            return UnstructuredXMLLoader(file_path=self.file_path)

        except ImportError:
            logger.warning(
                "UnstructuredXMLLoader not available. Install with: pip install unstructured"
            )
            return None
        except Exception as e:
            logger.error(f"Failed to create XML loader: {e}")
            return None


class YAMLSource(LocalFileSource):
    """YAML file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(
            source_path=file_path, file_extensions=[".yaml", ".yml"], **kwargs
        )
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a YAML loader."""
        try:
            # Use UnstructuredFileLoader for YAML
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
            logger.error(f"Failed to create YAML loader: {e}")
            return None


class TOMLSource(LocalFileSource):
    """TOML file source."""

    def __init__(self, file_path: str, **kwargs):
        super().__init__(source_path=file_path, file_extensions=[".toml"], **kwargs)
        self.file_path = file_path

    def create_loader(self) -> Optional[BaseLoader]:
        """Create a TOML loader."""
        try:
            from langchain_community.document_loaders import TomlLoader

            return TomlLoader(file_path=self.file_path)

        except ImportError:
            logger.warning("TomlLoader not available")
            # Fallback to text loader
            try:
                from langchain_community.document_loaders import TextLoader

                return TextLoader(file_path=self.file_path)
            except Exception:
                return None
        except Exception as e:
            logger.error(f"Failed to create TOML loader: {e}")
            return None


# Export data file sources
__all__ = [
    "CSVSource",
    "TSVSource",
    "JSONSource",
    "XMLSource",
    "YAMLSource",
    "TOMLSource",
]
