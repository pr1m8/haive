"""Text-based Document Loaders for Haive Framework

This module implements various text-based document loaders for different
file formats including plain text, markdown, CSV, JSON, and YAML.
"""

from pathlib import Path
from typing import Any

from pydantic import FilePath

from ..source_implementation import LocalSource, auto_source


@auto_source
class TextSource(LocalSource):
    """Plain text file source."""

    file_path: FilePath
    encoding: str = "utf-8"

    class Config:
        file_extensions = [".txt", ".text"]
        loader_strategies = {
            "basic": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["plain_text"],
            },
            "unstructured": {
                "class": "UnstructuredFileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_text"],
            },
        }

    def create_basic_loader(self):
        """Create a basic TextLoader."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path), encoding=self.encoding)
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding=self.encoding) as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]

    def create_unstructured_loader(self):
        """Create an UnstructuredFileLoader for better text extraction."""
        try:
            from langchain_community.document_loaders import UnstructuredFileLoader

            return UnstructuredFileLoader(
                str(self.file_path), mode="elements", strategy="fast"
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()


@auto_source
class MarkdownSource(LocalSource):
    """Markdown document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".md", ".markdown"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredMarkdownLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["markdown"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_markdown"],
            },
        }

    def create_unstructured_loader(self):
        """Create an UnstructuredMarkdownLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredMarkdownLoader

            return UnstructuredMarkdownLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for markdown."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class CSVSource(LocalSource):
    """CSV data source."""

    file_path: FilePath
    has_header: bool = True
    delimiter: str = ","

    class Config:
        file_extensions = [".csv"]
        loader_strategies = {
            "basic": {
                "class": "CSVLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["tabular_data"],
            },
            "unstructured": {
                "class": "UnstructuredCSVLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_csv"],
            },
            "pandas": {
                "class": "DataFrameLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["analysis", "processing"],
            },
        }

    def create_basic_loader(self):
        """Create a basic CSVLoader."""
        try:
            from langchain_community.document_loaders import CSVLoader

            return CSVLoader(
                file_path=str(self.file_path),
                csv_args={
                    "delimiter": self.delimiter,
                    "fieldnames": None if self.has_header else [],
                },
            )
        except ImportError:
            # Fallback to pandas if available
            try:
                return self.create_pandas_loader()
            except ImportError:
                # Last resort: read as text
                from langchain_community.document_loaders import TextLoader

                return TextLoader(str(self.file_path))

    def create_unstructured_loader(self):
        """Create an UnstructuredCSVLoader for better parsing."""
        try:
            from langchain_community.document_loaders import UnstructuredCSVLoader

            return UnstructuredCSVLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def create_pandas_loader(self):
        """Create a DataFrameLoader using pandas."""
        try:
            import pandas as pd
            from langchain_community.document_loaders import DataFrameLoader

            # Read CSV into pandas DataFrame
            df = pd.read_csv(
                self.file_path,
                delimiter=self.delimiter,
                header=0 if self.has_header else None,
            )

            # Use first column as index if it makes sense
            page_content_column = df.columns[0] if len(df.columns) > 0 else None

            return DataFrameLoader(
                data_frame=df, page_content_column=page_content_column
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()


@auto_source
class JSONSource(LocalSource):
    """JSON data source."""

    file_path: FilePath
    jq_schema: str | None = None
    pointer_path: str | None = None

    class Config:
        file_extensions = [".json", ".jsonl"]
        loader_strategies = {
            "basic": {
                "class": "JSONLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["structured_data"],
            },
            "unstructured": {
                "class": "UnstructuredJSONLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_json"],
            },
            "lines": {
                "class": "JSONLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["jsonl", "line_delimited"],
            },
        }

    def create_basic_loader(self):
        """Create a JSONLoader with optional jq schema."""
        try:
            from langchain_community.document_loaders import JSONLoader

            # Use jq_schema if provided
            if self.jq_schema:
                return JSONLoader(
                    file_path=str(self.file_path),
                    jq_schema=self.jq_schema,
                    text_content=False,
                )

            # Use JSONPointer if provided
            if self.pointer_path:
                return JSONLoader(
                    file_path=str(self.file_path),
                    pointer_path=self.pointer_path,
                    text_content=False,
                )

            # Default: load entire JSON
            return JSONLoader(file_path=str(self.file_path), text_content=False)

        except ImportError:
            # Fallback to reading JSON directly
            import json

            with open(self.file_path, encoding="utf-8") as f:
                data = json.load(f)

            from langchain_core.documents import Document

            return [
                Document(
                    page_content=str(data), metadata={"source": str(self.file_path)}
                )
            ]

    def create_unstructured_loader(self):
        """Create an UnstructuredJSONLoader for better parsing."""
        try:
            from langchain_community.document_loaders import UnstructuredJSONLoader

            return UnstructuredJSONLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()

    def create_lines_loader(self):
        """Create a JSONLoader for line-delimited JSON files."""
        try:
            from langchain_community.document_loaders import JSONLoader

            return JSONLoader(
                file_path=str(self.file_path),
                jq_schema=".",
                text_content=False,
                json_lines=True,
            )
        except ImportError:
            # Fallback to reading JSONL directly
            import json

            documents = []

            from langchain_core.documents import Document

            with open(self.file_path, encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if line.strip():
                        try:
                            data = json.loads(line)
                            documents.append(
                                Document(
                                    page_content=str(data),
                                    metadata={"source": str(self.file_path), "line": i},
                                )
                            )
                        except json.JSONDecodeError:
                            # Skip invalid lines
                            pass

            return documents


@auto_source
class YAMLSource(LocalSource):
    """YAML data source."""

    file_path: FilePath

    class Config:
        file_extensions = [".yaml", ".yml"]
        loader_strategies = {
            "basic": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["config_files"],
            },
            "structured": {
                "class": "YAMLLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["structured_yaml"],
            },
        }

    def create_basic_loader(self):
        """Create a TextLoader for YAML."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]

    def create_structured_loader(self):
        """Create a custom YAML loader that preserves structure."""
        try:
            import yaml

            with open(self.file_path, encoding="utf-8") as f:
                data = yaml.safe_load(f)

            from langchain_core.documents import Document

            # Convert YAML to text representation
            text_content = yaml.dump(data, default_flow_style=False)

            return [
                Document(
                    page_content=text_content,
                    metadata={
                        "source": str(self.file_path),
                        "format": "yaml",
                        "structure": data,  # Include structured data in metadata
                    },
                )
            ]
        except ImportError:
            # Fallback to basic loader
            return self.create_basic_loader()


@auto_source
class XMLSource(LocalSource):
    """XML data source."""

    file_path: FilePath
    xpath_filter: str | None = None

    class Config:
        file_extensions = [".xml"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredXMLLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["xml_documents"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_xml"],
            },
        }

    def create_unstructured_loader(self):
        """Create an UnstructuredXMLLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredXMLLoader

            return UnstructuredXMLLoader(str(self.file_path))
        except ImportError:
            # Fallback to text loader
            return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for XML."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class TomlSource(LocalSource):
    """TOML configuration file source."""

    file_path: FilePath

    class Config:
        file_extensions = [".toml"]
        loader_strategies = {
            "basic": {
                "class": "TomlLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["config_files"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_toml"],
            },
        }

    def create_basic_loader(self):
        """Create a TomlLoader."""
        try:
            from langchain_community.document_loaders import TomlLoader

            return TomlLoader(str(self.file_path))
        except ImportError:
            # Fallback to text loader
            return self.create_text_loader()

    def create_text_loader(self):
        """Create a basic TextLoader for TOML."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class ConfigFileSource(LocalSource):
    """Configuration file source (INI, CFG, etc.)."""

    file_path: FilePath

    class Config:
        file_extensions = [".ini", ".cfg", ".conf"]
        loader_strategies = {
            "basic": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["config_files"],
            }
        }

    def create_basic_loader(self):
        """Create a TextLoader for config files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]


@auto_source
class LogFileSource(LocalSource):
    """Log file source."""

    file_path: FilePath
    max_lines: int = 1000  # Limit for large log files
    read_from_tail: bool = True  # Most recent logs are often most relevant

    class Config:
        file_extensions = [".log", ".out", ".err"]
        loader_strategies = {
            "basic": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["small_logs"],
            },
            "tail": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["large_logs"],
            },
        }

    def create_basic_loader(self):
        """Create a TextLoader for log files."""
        try:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))
        except ImportError:
            # Fallback to reading the file directly
            with open(self.file_path, encoding="utf-8", errors="ignore") as f:
                text = f.read()
            from langchain_core.documents import Document

            return [
                Document(page_content=text, metadata={"source": str(self.file_path)})
            ]

    def create_tail_loader(self):
        """Create a loader that reads from the end of large log files."""
        try:
            # Read the last N lines of the file
            from collections import deque

            with open(self.file_path, encoding="utf-8", errors="ignore") as f:
                # Use deque with maxlen for memory efficiency
                last_lines = deque(maxlen=self.max_lines)

                # Process the file in reverse if reading from tail
                if self.read_from_tail:
                    # Seek to end and read backward
                    f.seek(0, 2)  # Go to end of file
                    file_size = f.tell()

                    # Start from end and read in chunks
                    chunk_size = 4096
                    position = max(file_size - chunk_size, 0)

                    # Buffer for incomplete lines
                    remainder = ""

                    # Read chunks from end to beginning
                    while position >= 0 and len(last_lines) < self.max_lines:
                        f.seek(position)
                        chunk = f.read(chunk_size) + remainder
                        lines = chunk.splitlines()

                        # Save incomplete first line
                        if position > 0:
                            remainder = lines[0]
                            lines = lines[1:]
                        else:
                            remainder = ""

                        # Add lines to deque (in reverse)
                        for line in reversed(lines):
                            if len(last_lines) < self.max_lines:
                                last_lines.appendleft(line)
                            else:
                                break

                        # Move position backward
                        position -= chunk_size

                    # Handle the remainder if any and if we have room
                    if remainder and len(last_lines) < self.max_lines:
                        last_lines.appendleft(remainder)
                else:
                    # Simple approach: read line by line from beginning
                    for i, line in enumerate(f):
                        if i < self.max_lines:
                            last_lines.append(line)
                        else:
                            break

            # Create document from lines
            from langchain_core.documents import Document

            text_content = "".join(last_lines)

            return [
                Document(
                    page_content=text_content,
                    metadata={
                        "source": str(self.file_path),
                        "from_tail": self.read_from_tail,
                        "max_lines": self.max_lines,
                    },
                )
            ]
        except Exception:
            # Fallback to basic loader
            return self.create_basic_loader()


# Additional convenience function for automatic loader creation


def create_text_loader(file_path: str | Path, **kwargs) -> Any:
    """Create the appropriate text-based loader for a given file path.

    Args:
        file_path: Path to the file
        **kwargs: Additional arguments for specific loaders

    Returns:
        A document loader instance
    """
    # Convert to Path object if string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Get file extension
    extension = file_path.suffix.lower()

    # Create appropriate source based on extension
    if extension in [".txt", ".text"]:
        source = TextSource(file_path=file_path, **kwargs)
    elif extension in [".md", ".markdown"]:
        source = MarkdownSource(file_path=file_path, **kwargs)
    elif extension == ".csv":
        source = CSVSource(file_path=file_path, **kwargs)
    elif extension in [".json", ".jsonl"]:
        source = JSONSource(file_path=file_path, **kwargs)
    elif extension in [".yaml", ".yml"]:
        source = YAMLSource(file_path=file_path, **kwargs)
    elif extension == ".xml":
        source = XMLSource(file_path=file_path, **kwargs)
    elif extension == ".toml":
        source = TomlSource(file_path=file_path, **kwargs)
    elif extension in [".ini", ".cfg", ".conf"]:
        source = ConfigFileSource(file_path=file_path, **kwargs)
    elif extension in [".log", ".out", ".err"]:
        source = LogFileSource(file_path=file_path, **kwargs)
    else:
        # Default to basic text loader
        source = TextSource(file_path=file_path, **kwargs)

    # Get strategy if specified
    strategy = kwargs.get("strategy")

    # Create loader with specified or default strategy
    return source.create_loader(strategy)
