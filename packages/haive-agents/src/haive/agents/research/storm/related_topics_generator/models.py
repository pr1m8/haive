from pydantic import BaseModel, Field


class RelatedSubjects(BaseModel):
    topics: list[str] = Field(
        description="Comprehensive list of related subjects as background research.",
    )
