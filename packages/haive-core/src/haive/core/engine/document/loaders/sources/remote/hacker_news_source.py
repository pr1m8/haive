from pydantic import Field, HttpUrl, field_validator

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class HackerNewsSource(URLSource):
    """A source that is a hacker news post."""

    source_type: SourceType = Field(default=SourceType.HACKER_NEWS)
    url: HttpUrl = Field(description="The url of the hacker news post.")

    @field_validator("url")
    def validate_url(self, v):
        if not v.startswith("https://news.ycombinator.com/"):
            raise ValueError(f"Invalid url: {v}")
        return v
