from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class ImsdbSource(URLSource):
    """
    A source that is an Imsdb source.
    """

    source_type: SourceType = Field(default=SourceType.IMSDB)
    url_prefix: str = Field(default="https://www.imsdb.com/")
