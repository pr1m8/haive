from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class YoutubeAudioSource(URLSource):
    """A source that is a Youtube audio source."""

    source_type: SourceType = Field(default=SourceType.YOUTUBE_AUDIO)
    url_prefix: str = Field(default="https://www.youtube.com/watch?v=")
