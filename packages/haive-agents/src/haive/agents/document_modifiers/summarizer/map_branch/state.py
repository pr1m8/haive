"""State for the summarizer agent."""

import operator
from typing import Annotated

from langchain_core.documents import Document
from pydantic import BaseModel, Field, field_validator


class InputState(BaseModel):
    contents: list[str] = Field(
        default_factory=list, description="The contents of the documents"
    )

    @field_validator("contents", mode="before")
    @classmethod
    def normalize_contents(cls, v):
        """Normalize inputs to strings.
        Accepts:
        - List[str]
        - List[Document]
        - Mixed.
        """
        if not isinstance(v, list):
            raise TypeError("Expected a list for 'contents'")

        normalized = []
        for item in v:
            if isinstance(item, Document):
                # Convert Document to string content
                normalized.append(item.page_content)
            elif isinstance(item, str):
                normalized.append(item)
            else:
                raise TypeError(f"Unsupported item type in contents: {type(item)}")

        return normalized


class OutputState(BaseModel):
    """Output state for the summarizer agent."""

    final_summary: str = Field(
        default="", description="The final summary of the documents"
    )


class SummaryState(InputState, OutputState):
    """State for the summarizer agent - we use the operator.add to combine the summaries."""

    summaries: Annotated[list, operator.add] = Field(
        default_factory=list, description="The summaries of the documents"
    )
    collapsed_summaries: list[Document] = Field(
        default_factory=list, description="The collapsed summaries of the documents"
    )
