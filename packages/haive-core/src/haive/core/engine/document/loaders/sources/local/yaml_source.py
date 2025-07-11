from pydantic import Field

from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class YamlSource(FileSource):
    """A source that is a Yaml file."""

    source_type: SourceType = Field(default=SourceType.YAML)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.YAML)
