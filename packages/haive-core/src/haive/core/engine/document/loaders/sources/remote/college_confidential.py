from pydantic import Field

from haive.core.engine.loaders.sources.remote.base import URLSource
from haive.core.engine.loaders.sources.types import SourceType


class CollegeConfidentialSource(URLSource):
    """A source that is a College Confidential source."""

    source_type: SourceType = Field(default=SourceType.COLLEGE_CONFIDENTIAL)
    url_prefix: str = Field(default="https://www.collegeconfidential.com/")


# https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.college_confidential.CollegeConfidentialLoader.html
