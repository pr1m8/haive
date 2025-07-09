from typing import Optional, Union

from pydantic import Field, HttpUrl, field_validator

from haive.core.engine.loaders.sources.base import BaseSource
from haive.core.engine.loaders.sources.types import SourceType


class URLSource(BaseSource):
    """
    A source that is a remote file.
    """

    source_type: SourceType = Field(default=SourceType.URL)
    url: HttpUrl = Field(description="The url of the remote file.")
    url_prefix: Optional[str] = Field(default="", description="The prefix of the url.")

    @field_validator("url")
    def validate_url(cls, v):
        if not v.is_valid():
            raise ValueError(f"Invalid url: {v}")
        return v

    @property
    def source(self) -> HttpUrl:
        """
        The source of the remote file.
        """
        return self.url

    @classmethod
    def from_url(cls, url: Union[HttpUrl, str]) -> "URLSource":
        """
        Create a URLSource from a url.
        """
        if isinstance(url, str):
            url = HttpUrl(url)
        return cls(url=url)

    @field_validator("url")
    def validate_url(cls, v):
        if not v.is_valid():
            raise ValueError(f"Invalid url: {v}")
        return v
