from pydantic import Field

from haive.agents.rag.base.state import (
    BaseRAGInputState,
    BaseRAGOutputState,
    BaseRAGState,
)


class LLMRAGInputState(BaseRAGInputState):
    """Input state for LLM RAG agents."""


class LLMRAGOutputState(BaseRAGOutputState):
    """Output state for LLM RAG agents."""

    answer: str = Field(
        default="", description="The generated answer based on retrieved documents"
    )
    is_relevant: bool = Field(
        default=False,
        description="Whether the retrieved documents are relevant to the query",
    )


class LLMRAGState(BaseRAGState, LLMRAGOutputState):
    """State for LLM RAG agents."""
