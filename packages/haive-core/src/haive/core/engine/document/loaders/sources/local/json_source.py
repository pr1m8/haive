from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class JsonSource(FileSource):
    """A source that is a Json file."""

    source_type: SourceType = Field(default=SourceType.JSON)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.JSON)
