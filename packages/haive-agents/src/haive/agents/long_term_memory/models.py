from pydantic import BaseModel, Field


class KnowledgeTriple(BaseModel):
    """A knowledge triple is a tuple of (subject, predicate, object)."""

    subject: str = Field(description="The subject of the knowledge triple")
    predicate: str = Field(description="The predicate of the knowledge triple")
    object_: str = Field(description="The object of the knowledge triple")
