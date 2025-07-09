from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class ReadTheDocsSource(URLSource):
    """
    A source that is a ReadTheDocs source.
    """

    source_type: SourceType = Field(default=SourceType.READTHEDOCS)
    url_prefix: str = Field(default="https://readthedocs.org/")
