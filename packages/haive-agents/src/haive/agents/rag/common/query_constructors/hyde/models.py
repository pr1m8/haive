from pydantic import BaseModel, Field


class HypotheticalDocument(BaseModel):
    """A hypothetical document generated for HyDE."""

    content: str = Field(description="The hypothetical document content")
    relevance_explanation: str = Field(
        description="Why this document would be relevant to the query"
    )
    key_concepts: list[str] = Field(
        description="Key concepts covered in the hypothetical document"
    )
    document_type: str = Field(
        description="Type of document (academic paper, news article, manual, etc.)"
    )

    def to_query(self) -> str:
        """Convert the hypothetical document to a query."""
        return self.content


class HyDEResponse(BaseModel):
    """HyDE (Hypothetical Document Embeddings) response."""

    original_query: str = Field(description="The original user query")
    query_analysis: str = Field(
        description="Analysis of what type of documents would be helpful"
    )
    hypothetical_documents: list[HypotheticalDocument] = Field(
        description="Generated hypothetical documents"
    )
    search_queries: list[str] = Field(
        description="Refined search queries based on hypothetical documents"
    )
    retrieval_strategy: str = Field(
        description="Recommended retrieval strategy using the hypothetical documents"
    )
