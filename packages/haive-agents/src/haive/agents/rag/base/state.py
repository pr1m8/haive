from langchain.schema import Document
from pydantic import BaseModel, Field


class BaseRAGInputState(BaseModel):
    """Input state for RAG agents."""

    query: str = Field(..., description="The query to search the RAG database with.")


class BaseRAGOutputState(BaseModel):
    """Output state for RAG agents."""

    # answer:str = Field(default="", description="The generation of the RAG search.")
    retrieved_documents: list[Document] | list[str] | None = Field(
        default=[], description="The results of the RAG search."
    )


class BaseRAGState(BaseRAGInputState, BaseRAGOutputState):
    """State for RAG agents."""
