from pydantic import Field

from haive.core.engine.loaders.sources.types import SourceType


class GitSource(BaseSource):
    """
    A source that is a Git source.
    """

    source_type: SourceType = Field(default=SourceType.GIT)
    url_prefix: str = Field(default="https://www.git.com/")
    repo_path: str = Field(default="")
    branch: str = Field(default="main")
    commit: str = Field(default="")
    file_path: str = Field(default="")
    file_name: str = Field(default="")
    file_extension: str = Field(default="")


# https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.git.GitLoader.html
