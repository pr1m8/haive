from abc import ABC, abstractmethod
from enum import Enum
from typing import Union

from pydantic import (
    AnyUrl,
    BaseModel,
    DirectoryPath,
    EmailStr,
    Field,
    FilePath,
    HttpUrl,
)

from haive.core.engine.loaders.sources.types import SourceType


# from langchain_core.documents import Document
class SourceClass(Enum, str):
    """
    Enum of source classes.
    """

    LOCAL = "LOCAL"
    WEB = "WEB"
    EMAIL = "EMAIL"
    API = "API"
    DATABASE = "DATABASE"
    OTHER = "OTHER"


class BaseSource(ABC, BaseModel):
    """
    Base class for all sources.
    """

    source_type: SourceType = Field(description="The type of source.")
    source_class: SourceClass = Field(description="The class of source.")

    @abstractmethod
    def source(self) -> Union[HttpUrl, EmailStr, AnyUrl, FilePath, DirectoryPath, str]:
        """
        The source of the data to load.
        """
        raise NotImplementedError("Subclasses must implement this method.")

    # @classmethod
    # @computed_field
    @property
    def source_class(self) -> SourceClass:
        """
        The class of source.
        """
        return SourceClass(self.source_type)

    @classmethod
    def source_as_string(
        cls, source: Union[HttpUrl, EmailStr, AnyUrl, FilePath, DirectoryPath, str]
    ) -> str:
        """
        The source as a string.
        """
        return str(source)
