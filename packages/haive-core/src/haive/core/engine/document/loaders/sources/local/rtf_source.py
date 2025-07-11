from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class RtfSource(FileSource):
    """A source that is a Rtf file."""

    source_type: SourceType = Field(default=SourceType.RTF)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.RTF)
