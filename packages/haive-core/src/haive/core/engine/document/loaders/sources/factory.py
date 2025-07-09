"""
Source object factory for creating sources from various input formats.

This module provides utility functions for creating source objects from
strings, paths, and dictionaries, determining the correct source type.
"""

import os
import re
from pathlib import Path
from typing import Any, Dict, Union

from haive.core.engine.document.loaders.sources.base.base import BaseSource
from haive.core.engine.document.loaders.sources.local.base import (
    DirectorySource,
    FileSource,
)
from haive.core.engine.document.loaders.sources.remote.base import URLSource
from haive.core.engine.document.loaders.sources.source_types import SourceCategory


def create_source_from_string(source_string: str) -> BaseSource:
    """
    Create a source object from a string.

    Args:
        source_string: String representing a source

    Returns:
        BaseSource object

    Raises:
        ValueError: If source type cannot be determined
    """
    # Check if it's a URL
    if source_string.startswith(("http://", "https://", "ftp://", "sftp://")):
        return URLSource(url=source_string)

    # Check if it's a local file or directory
    if os.path.exists(source_string):
        path = Path(source_string)
        if path.is_dir():
            return DirectorySource(directory_path=path)
        elif path.is_file():
            return FileSource(file_path=path)

    # If we get here, we couldn't determine the source type
    raise ValueError(f"Could not determine source type for: {source_string}")


def create_source_from_path(path: Path) -> BaseSource:
    """
    Create a source object from a Path.

    Args:
        path: Path object representing a file or directory

    Returns:
        BaseSource object

    Raises:
        ValueError: If path doesn't exist
    """
    if not path.exists():
        raise ValueError(f"Path does not exist: {path}")

    if path.is_dir():
        return DirectorySource(directory_path=path)
    elif path.is_file():
        return FileSource(file_path=path)

    # Should not get here unless path exists but is neither file nor directory
    raise ValueError(f"Path exists but is neither file nor directory: {path}")


def create_source_from_dict(source_dict: Dict[str, Any]) -> BaseSource:
    """
    Create a source object from a dictionary.

    Args:
        source_dict: Dictionary with source configuration

    Returns:
        BaseSource object

    Raises:
        ValueError: If dictionary doesn't contain valid source configuration
    """
    # Check if source_type is explicitly provided
    if "source_type" in source_dict:
        try:
            SourceType(source_dict["source_type"])
        except ValueError:
            # Invalid source type, will try to determine from other fields
            pass

    # Create source based on the fields present
    if "url" in source_dict:
        return URLSource(**source_dict)
    elif "file_path" in source_dict:
        return FileSource(**source_dict)
    elif "directory_path" in source_dict:
        return DirectorySource(**source_dict)
    elif "source" in source_dict:
        # Try to create a source from the "source" field
        source = source_dict.pop("source")
        if isinstance(source, str):
            base_source = create_source_from_string(source)
            # If we have additional configuration, create a new instance with it
            if source_dict:
                return type(base_source)(**{**base_source.model_dump(), **source_dict})
            return base_source

    # If we get here, we couldn't determine the source type
    raise ValueError(f"Could not determine source type from dictionary: {source_dict}")


def infer_source_type_from_url(url: str) -> SourceType:
    """
    Infer the source type from a URL.

    Args:
        url: URL string

    Returns:
        SourceType enum value
    """
    # Known patterns for common sources
    patterns = {
        r"youtube\.com/watch": SourceType.YOUTUBE,
        r"youtu\.be/": SourceType.YOUTUBE,
        r"arxiv\.org": SourceType.ARXIV,
        r"wikipedia\.org": SourceType.WIKIPEDIA,
        r"github\.com": SourceType.GITHUB,
        r"news\.ycombinator\.com": SourceType.HACKER_NEWS,
        r"docs\.readthedocs\.io": SourceType.READTHEDOCS,
        r"imdb\.com": SourceType.IMDB,
    }

    # Check for matches
    for pattern, source_type in patterns.items():
        if re.search(pattern, url):
            return source_type

    # Default to generic URL
    return SourceType.URL


def infer_source_type_from_file(file_path: Union[str, Path]) -> SourceType:
    """
    Infer the source type from a file path.

    Args:
        file_path: Path to the file

    Returns:
        SourceType enum value
    """
    # Convert to Path if string
    if isinstance(file_path, str):
        file_path = Path(file_path)

    # Get the file extension (without the dot)
    extension = file_path.suffix.lower().lstrip(".")

    # Map extensions to source types
    extension_map = {
        "pdf": SourceType.PDF,
        "docx": SourceType.DOCX,
        "doc": SourceType.DOCX,
        "xlsx": SourceType.EXCEL,
        "xls": SourceType.EXCEL,
        "csv": SourceType.CSV,
        "json": SourceType.JSON,
        "html": SourceType.HTML,
        "htm": SourceType.HTML,
        "md": SourceType.MARKDOWN,
        "xml": SourceType.XML,
        "txt": SourceType.FILE,
        "py": SourceType.PYTHON,
        "ipynb": SourceType.NOTEBOOK,
        "epub": SourceType.EPUB,
        "ppt": SourceType.PPT,
        "pptx": SourceType.PPT,
        "rtf": SourceType.RTF,
        "srt": SourceType.SRT,
    }

    return extension_map.get(extension, SourceType.FILE)
