import os
from abc import ABC
from pathlib import Path
from typing import List

from pydantic import DirectoryPath, Field, FilePath, field_validator, model_validator

from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class LocalSource(BaseSource):
    """
    A source that is a file.
    """

    source_type: SourceType = Field(
        default=SourceType.FILE, description="The type of source."
    )
    file_path: FilePath = Field(description="The path to the file to load.")

    @field_validator("file_path")
    def validate_file_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")
        return v

    @field_validator("file_path", mode="before")
    def convert_to_path(cls, v):
        if isinstance(v, str):
            return Path(v)
        return v

    @field_validator("file_path", mode="before")
    def is_file(cls, v):
        if not v.is_file():
            raise ValueError(f"File does not exist: {v}")
        return v

    @property
    def source(self) -> FilePath:
        return self.file_path

    @classmethod
    def from_file_path(cls, file_path: FilePath) -> "LocalSource":
        return cls(file_path=file_path)

    @property
    def is_file(self) -> bool:
        return self.file_path.is_file()

    @property
    def is_directory(self) -> bool:
        return self.file_path.is_dir()


class FileSource(ABC, LocalSource):
    """
    A source that is a file.
    """

    file_path: FilePath = Field(description="The path to the file to load.")
    # file_type: LocalSourceFileType = Field(description="The type of file.")

    @field_validator("file_path")
    def validate_file_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"File does not exist: {v}")
        return v

    @field_validator("file_path", mode="before")
    def convert_to_path(cls, v):
        if isinstance(v, str):
            return Path(v)
        return v

    @model_validator(mode="before")
    def validate_file_type(cls, v):
        if not isinstance(v, LocalSourceFileType):
            v = LocalSourceFileType(v.suffix)
        return v

    @property
    def file_type(self) -> LocalSourceFileType:
        return LocalSourceFileType(self.file_path.suffix)

    @property
    def file_name(self) -> str:
        return self.file_path.name

    @property
    def file_size(self) -> int:
        return self.file_path.stat().st_size

    @property
    def source(self) -> FilePath:
        return self.file_path


class DirectorySource(LocalSource):
    """
    A source that is a directory.
    """

    directory_path: DirectoryPath = Field(
        description="The path to the directory to load."
    )

    @field_validator("directory_path")
    def validate_directory_path(cls, v):
        if not os.path.exists(v):
            raise ValueError(f"Directory does not exist: {v}")
        return v

    @classmethod
    def from_directory_path(cls, directory_path: DirectoryPath) -> "DirectorySource":
        return cls(directory_path=directory_path)

    @classmethod
    def list_files(cls, directory_path: DirectoryPath) -> List[FilePath]:
        return list(directory_path.glob("*"))

    @classmethod
    def list_directories(cls, directory_path: DirectoryPath) -> List[DirectoryPath]:
        return list(directory_path.glob("*"))
