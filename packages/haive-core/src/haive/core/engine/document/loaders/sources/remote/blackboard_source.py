from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class BlackboardSource(URLSource):
    """
    A source that is a Blackboard source.
    """

    source_type: SourceType = Field(default=SourceType.BLACKBOARD)
    url_prefix: str = Field(default="https://blackboard.com/")
    bbrouter_url: str = Field(description="The bbrouter url of the user.")
