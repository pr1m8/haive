from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class AzLyricsSource(URLSource):
    """A source that is a AzLyrics source."""

    source_type: SourceType = Field(default=SourceType.AZ_LYRICS)
    url_prefix: str = Field(default="https://www.azlyrics.com/")

    @classmethod
    def from_artist_and_song(cls, artist: str, song: str) -> "AzLyricsSource":
        """Create an AzLyricsSource from an artist and song."""
        return cls(
            url=f"{cls.url_prefix}{artist.lower().replace(' ', '')}/{song.lower().replace(' ', '')}.html"
        )
