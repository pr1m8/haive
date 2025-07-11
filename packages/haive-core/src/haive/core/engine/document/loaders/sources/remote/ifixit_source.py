from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class IfixitSource(URLSource):
    """A source that is an Ifixit source."""

    source_type: SourceType = Field(default=SourceType.IFIXIT)
    url_prefix: str = Field(default="https://www.ifixit.com/")
