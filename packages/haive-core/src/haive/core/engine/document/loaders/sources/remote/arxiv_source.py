from pydantic import Field

from haive.core.engine.document.loaders.base.schema import (
    DocumentEngineInputSchema,
    DocumentEngineOutputSchema,
)
from haive.core.engine.document.loaders.sources.remote.base import URLSource
from haive.core.engine.document.loaders.sources.source_types import SourceCategory


class ArxivSource(URLSource):
    """
    A source that is an Arxiv source.
    """

    source_type: SourceType = Field(default=SourceType.ARXIV)
    url_prefix: str = Field(default="https://arxiv.org/")

    def load(self, input: DocumentEngineInputSchema) -> DocumentEngineOutputSchema:
        """
                Initialize with search query to find documents in the Arxiv. Supports all arguments of ArxivAPIWrapper.

        Parameters
        :
        query (str) – free text which used to find documents in the Arxiv

        doc_content_chars_max (int | None) – cut limit for the length of a document’s content

        kwargs (Any)

        Methods

        __init__(query[, doc_content_chars_max])

        Initialize with search query to find documents in the Arxiv.

        alazy_load()

        A lazy loader for Documents.

        aload()

        Load data into Document objects.

        get_summaries_as_docs()

        Uses papers summaries as documents rather than source Arvix papers

        lazy_load()

        Lazy load Arvix documents

        load()

        Load data into Document objects.

        load_and_split([text_splitter])

        Load Documents and split into chunks.

        __init__(
        query: str,
        doc_content_chars_max: int | None = None,
        **kwargs: Any,
        )[source]
        Initialize with search query to find documents in the Arxiv. Supports all arguments of ArxivAPIWrapper.

        Parameters
        :
        query (str) – free text which used to find documents in the Arxiv

        doc_content_chars_max (int | None) – cut limit for the length of a document’s content

        kwargs (Any)

        async alazy_load() → AsyncIterator[Document]
        A lazy loader for Documents.

        Return type
        :
        AsyncIterator[Document]

        async aload() → list[Document]
        Load data into Document objects.

        Return type
        :
        list[Document]

        get_summaries_as_docs() → List[Document][source]
        Uses papers summaries as documents rather than source Arvix papers

        Return type
        :
        List[Document]

        lazy_load() → Iterator[Document][source]
        Lazy load Arvix documents

        Return type
        :
        Iterator[Document]

        load() → list[Document]
        Load data into Document objects.

        Return type
        :
        list[Document]

        load_and_split(
        text_splitter: TextSplitter | None = None,
        ) → list[Document]
        Load Documents and split into chunks. Chunks are returned as Documents.

        Do not override this method. It should be considered to be deprecated!

        Parameters
        :
        text_splitter (Optional[TextSplitter]) – TextSplitter instance to use for splitting documents. Defaults to RecursiveCharacterTextSplitter.

        Returns
        :
        List of Documents.

        Return type
        :
        list[Document]

        Examples using ArxivLoader

        Arxiv

        ArxivLoader
        """
