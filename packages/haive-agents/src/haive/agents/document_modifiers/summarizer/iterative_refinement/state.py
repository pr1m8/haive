from typing import Any, Literal

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field, field_validator


class IterativeSummarizerInput(BaseModel):
    """Input for the summarizer – supports string, Document, message, or dict content."""

    contents: list[str | Document | BaseMessage | dict[str, Any]] = Field(
        description="List of inputs (str, Document, BaseMessage, or dict) to summarize."
    )

    @field_validator("contents", mode="before")
    @classmethod
    def normalize_contents(cls, value):
        """Ensure all items are string representations."""
        normalized = []
        for item in value:
            if isinstance(item, str):
                normalized.append(item)
            elif isinstance(item, Document):
                normalized.append(item.page_content)
            elif isinstance(item, BaseMessage):
                normalized.append(item.content)
            elif isinstance(item, dict):
                normalized.append(item.get("content", str(item)))
            else:
                normalized.append(str(item))
        return normalized


class IterativeSummarizerOutput(BaseModel):
    """Output for the summarizer – stores the final summary result."""

    summary: str = Field(
        default="", description="The final summary of the input contents."
    )


class IterativeSummarizerState(IterativeSummarizerInput, IterativeSummarizerOutput):
    """Full state for the iterative summarizer agent – tracks progress and summary."""

    index: int = Field(
        default=0, description="The current index of the document being summarized."
    )

    def should_refine(self) -> Literal["refine_summary", "__end__"]:
        return "refine_summary" if self.index < len(self.contents) else "__end__"
