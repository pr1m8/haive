from typing import (
    List,
    TypeVar,
    Union,
)

from langchain_community.graphs import GraphDocument
from langchain_core.documents import Document
from pydantic import BaseModel, Field

DocumentLike = TypeVar("DocumentLike", bound=Union[Document, GraphDocument])


class LoaderInputSchema(BaseModel):
    """
    Schema for the input of a loader.
    """

    source: Union[str, List[str]] = Field(description="The source of the data to load.")


class LoaderOutputSchema(BaseModel):
    """
    Schema for the output of a loader.
    """

    documents: List[DocumentLike] = Field(description="The loaded documents.")
