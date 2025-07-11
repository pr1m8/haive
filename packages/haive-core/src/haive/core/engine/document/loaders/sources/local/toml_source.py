from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class TomlSource(FileSource):
    """A source that is a Toml file."""

    source_type: SourceType = Field(default=SourceType.TOML)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.TOML)
