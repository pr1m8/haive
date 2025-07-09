from pydantic import BaseModel, Field


class Queries(BaseModel):
    """Structure for search queries."""

    queries: list[str] = Field(
        description="List of search queries.",
    )


class ReflectionOutput(BaseModel):
    """Structure for reflection output."""

    is_satisfactory: bool = Field(
        description="True if all required fields are well populated, False otherwise"
    )
    missing_fields: list[str] = Field(
        description="List of field names that are missing or incomplete"
    )
    search_queries: list[str] = Field(
        description="If is_satisfactory is False, provide 1-3 targeted search queries to find the missing information"
    )
    reasoning: str = Field(description="Brief explanation of the assessment")
