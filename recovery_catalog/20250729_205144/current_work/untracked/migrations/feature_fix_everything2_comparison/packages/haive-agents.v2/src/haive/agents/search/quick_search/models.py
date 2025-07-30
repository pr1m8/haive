"""Data models for Quick Search Agent."""

from pydantic import BaseModel, Field

from haive.agents.memory.search.base import SearchResponse


class QuickSearchResponse(SearchResponse):
    """Response model for quick search operations.

    Extends the base SearchResponse with quick search specific fields.
    """

    search_type: str = Field(
        default="QuickSearch", description="Type of search performed"
    )
    answer_type: str = Field(
        default="factual", description="Type of answer (factual, definition, etc.)"
    )
    keywords: list[str] = Field(
        default_factory=list, description="Key terms identified in query"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "What is the capital of France?",
                "response": "The capital of France is Paris. It is located in the north-central part of the country and is the largest city in France.",
                "sources": ["wikipedia.org", "britannica.com"],
                "confidence": 0.95,
                "search_type": "QuickSearch",
                "processing_time": 0.8,
                "answer_type": "factual",
                "keywords": ["capital", "France", "Paris"],
                "metadata": {},
            }
        }


class QuickSearchRequest(BaseModel):
    """Request model for quick search operations."""

    query: str = Field(..., min_length=1, max_length=500, description="Search query")
    include_sources: bool = Field(
        default=True, description="Whether to include source links"
    )
    max_response_length: int = Field(
        default=200, description="Maximum response length in characters"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "What is machine learning?",
                "include_sources": True,
                "max_response_length": 200,
            }
        }
