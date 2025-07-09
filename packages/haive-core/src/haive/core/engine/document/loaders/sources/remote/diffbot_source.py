from pydantic import Field, SecretStr

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class DiffbotSource(URLSource):
    """
    A source that is a Diffbot source.
    """

    source_type: SourceType = Field(default=SourceType.DIFFBOT)
    url_prefix: str = Field(default="https://www.diffbot.com/")
    api_token: SecretStr = Field(description="The api token for the Diffbot source.")


# https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.diffbot.DiffbotLoader.html
