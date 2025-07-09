from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class MhtmlSource(FileSource):
    """
    A source that is a Mhtml file.
    """

    source_type: SourceType = Field(default=SourceType.MHTML)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.MHTML)
