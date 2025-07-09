from langchain_community.document_loaders import VsdxLoader
from pydantic import Field

from haive.core.engine.loaders.base.schema import LoaderOutputSchema
from haive.core.engine.loaders.sources.local.base import FileSource
from haive.core.engine.loaders.sources.local.types import LocalSourceFileType
from haive.core.engine.loaders.sources.types import SourceType


class VsdxSource(FileSource):
    """
    A source that is a Vsdx file.
    """

    source_type: SourceType = Field(default=SourceType.VSDX)
    file_type: LocalSourceFileType = Field(default=LocalSourceFileType.VSDX)

    def load(self, input: LoaderInputSchema) -> LoaderOutputSchema:
        """
        Load the Vsdx file.
        """
        return VsdxLoader(file_path=self.file_path).load()
