import mimetypes
import os
from datetime import datetime
from pathlib import Path
from typing import Any, ClassVar, Dict, List, Union

from pydantic import DirectoryPath, Field, FilePath, computed_field, model_validator

from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.types import SourceType


class FileSource(BaseSource):
    """
    Base class for all file-based sources.
    """

    file_path: FilePath = Field(description="Path to the file")

    # Class variable for MIME type mapping
    MIME_TYPES: ClassVar[Dict[str, str]] = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".csv": "text/csv",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".html": "text/html",
        ".htm": "text/html",
        ".json": "application/json",
        ".xml": "application/xml",
        ".epub": "application/epub+zip",
        ".rtf": "application/rtf",
    }

    @model_validator(mode="after")
    def validate_file_exists(self):
        """Validate the file exists after model initialization."""
        if not os.path.isfile(self.file_path):
            raise ValueError(f"File does not exist: {self.file_path}")
        return self

    def get_source_value(self) -> FilePath:
        """Get the file path as the source value."""
        return self.file_path

    def validate(self) -> bool:
        """Validate the file exists and is readable."""
        return os.path.isfile(self.file_path) and os.access(self.file_path, os.R_OK)

    @computed_field
    def file_name(self) -> str:
        """Get the file name without path."""
        return os.path.basename(self.file_path)

    @computed_field
    def file_extension(self) -> str:
        """Get the file extension."""
        return os.path.splitext(self.file_path)[1].lower()

    @computed_field
    def file_size(self) -> int:
        """Get the file size in bytes."""
        return os.path.getsize(self.file_path)

    @computed_field
    def last_modified(self) -> datetime:
        """Get the last modified timestamp."""
        timestamp = os.path.getmtime(self.file_path)
        return datetime.fromtimestamp(timestamp)

    @computed_field
    def content_type(self) -> str:
        """Get the content type (MIME type)."""
        # Try from class mapping first
        if self.file_extension in self.MIME_TYPES:
            return self.MIME_TYPES[self.file_extension]

        # Use mimetypes module as fallback
        mime_type, _ = mimetypes.guess_type(str(self.file_path))
        return mime_type or "application/octet-stream"

    def get_metadata(self) -> Dict[str, Any]:
        """Get file metadata."""
        metadata = super().get_metadata()

        # Add file-specific metadata
        metadata.update(
            {
                "file_name": self.file_name,
                "file_extension": self.file_extension,
                "file_size": self.file_size,
                "last_modified": self.last_modified.isoformat(),
                "content_type": self.content_type,
                "file_path": str(self.file_path),
            }
        )

        return metadata

    @classmethod
    def from_path(cls, path: Union[str, Path], **kwargs) -> "FileSource":
        """Create a FileSource from a path."""
        if isinstance(path, str):
            path = Path(path)

        # Set default name from filename if not provided
        if "name" not in kwargs:
            kwargs["name"] = os.path.basename(path)

        return cls(file_path=path, **kwargs)


class DirectorySource(BaseSource):
    """
    Source representing a directory of files.
    """

    source_type: SourceType = Field(default=SourceType.DIRECTORY)
    directory_path: DirectoryPath = Field(description="Path to the directory")

    @model_validator(mode="after")
    def validate_directory_exists(self):
        """Validate the directory exists after model initialization."""
        if not os.path.isdir(self.directory_path):
            raise ValueError(f"Directory does not exist: {self.directory_path}")
        return self

    def get_source_value(self) -> DirectoryPath:
        """Get the directory path as the source value."""
        return self.directory_path

    def validate(self) -> bool:
        """Validate the directory exists and is readable."""
        return os.path.isdir(self.directory_path) and os.access(
            self.directory_path, os.R_OK
        )

    @computed_field
    def directory_name(self) -> str:
        """Get the directory name without path."""
        return os.path.basename(self.directory_path)

    @computed_field
    def file_count(self) -> int:
        """Get the number of files in the directory (non-recursive)."""
        return len(
            [
                f
                for f in os.listdir(self.directory_path)
                if os.path.isfile(os.path.join(self.directory_path, f))
            ]
        )

    @computed_field
    def last_modified(self) -> datetime:
        """Get the last modified timestamp."""
        timestamp = os.path.getmtime(self.directory_path)
        return datetime.fromtimestamp(timestamp)

    def get_metadata(self) -> Dict[str, Any]:
        """Get directory metadata."""
        metadata = super().get_metadata()
        metadata.update(
            {
                "directory_name": self.directory_name,
                "file_count": self.file_count,
                "last_modified": self.last_modified.isoformat(),
                "directory_path": str(self.directory_path),
            }
        )
        return metadata

    def list_files(self, pattern: str = "*", recursive: bool = False) -> List[Path]:
        """
        List files in the directory.

        Args:
            pattern: Glob pattern for filtering files
            recursive: Whether to search recursively

        Returns:
            List[Path]: List of file paths
        """
        if recursive:
            return list(self.directory_path.glob(f"**/{pattern}"))
        return list(self.directory_path.glob(pattern))

    def list_subdirectories(self) -> List[Path]:
        """List subdirectories."""
        return [p for p in self.directory_path.iterdir() if p.is_dir()]

    @classmethod
    def from_path(cls, path: Union[str, Path], **kwargs) -> "DirectorySource":
        """Create a DirectorySource from a path."""
        if isinstance(path, str):
            path = Path(path)

        # Set default name from directory name if not provided
        if "name" not in kwargs:
            kwargs["name"] = os.path.basename(path)

        return cls(directory_path=path, **kwargs)
