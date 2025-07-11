from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class EvernoteSource(FileSource):
    """A source that is an Evernote source."""

    source_type: SourceType = Field(default=SourceType.EVERNOTE)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.EVERNOTE)
