from typing import Union

from pydantic import Field, HttpUrl, field_validator

from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.types import SourceType


class RemoteSource(BaseSource):
    """A source that is a remote file."""

    source_type: SourceType = Field(
        default=SourceType.REMOTE, description="The type of source."
    )
    url: HttpUrl = Field(description="The url of the remote file.")

    @field_validator("url")
    def validate_url(self, v):
        if not v.is_valid():
            raise ValueError(f"Invalid url: {v}")
        return v

    @property
    def source(self) -> HttpUrl:
        return self.url

    @classmethod
    def from_url(cls, url: HttpUrl | str) -> "RemoteSource":
        if isinstance(url, str):
            url = HttpUrl(url)
        return cls(url=url)
