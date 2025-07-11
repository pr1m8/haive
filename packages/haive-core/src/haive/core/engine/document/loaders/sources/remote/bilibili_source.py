from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.utils import SourceType


class BilibiliSource(URLSource):
    """A source that is a Bilibili source."""

    source_type: SourceType = Field(default=SourceType.BILIBILI)
    url_prefix: str = Field(default="https://www.bilibili.com/")
    sessdata: str = Field(default="", description="The sessdata of the user.")
    bili_jct: str = Field(default="", description="The bili_jct of the user.")
    buvid3: str = Field(default="", description="The buvid3 of the user.")


# from langchain_community.document_loaders.bilibili.BiliBiliLoader (takes in video urls ? (List[str]))
