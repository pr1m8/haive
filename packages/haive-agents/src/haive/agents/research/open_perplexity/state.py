"""State schemas for the open_perplexity research agent.

This module defines the state schemas used by the research agent to track
the progress of research, manage search queries, store sources, and generate
reports. It includes schemas for input, processing state, and output.
"""

from collections.abc import Sequence
from enum import Enum
from typing import Annotated, Any

from langchain_core.documents import Document
from langchain_core.messages import BaseMessage
from langgraph.graph import add_messages
from pydantic import BaseModel, Field


class ResearchConfidenceLevel(str, Enum):
    """Confidence level in research findings.

    Represents the overall confidence level in the research results,
    based on source quality, quantity, and consistency.

    Attributes:
        HIGH: High confidence based on numerous reliable sources
        MEDIUM: Medium confidence with good but limited sources
        LOW: Low confidence due to limited or questionable sources
        INSUFFICIENT_DATA: Not enough data to establish confidence
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INSUFFICIENT_DATA = "insufficient_data"


class ResearchState(BaseModel):
    """State schema for the open_perplexity research agent.

    Comprehensive state object that tracks all aspects of the research process,
    including messages, research parameters, report sections, sources, and findings.

    Attributes:
        messages: Conversation messages
        research_topic: Main topic of research
        research_question: Specific research question
        input_context: Additional context provided by the user
        search_parameters: Parameters for search and research customization
        report_sections: Sections of the research report
        current_section_index: Index of the current section being researched
        search_queries: List of search queries to execute
        query: Current search query
        retrieved_documents: Documents retrieved from search
        sources: Sources used in the research
        data_sources: Data sources available and used
        vectorstore_documents: Documents loaded into vector store
        research_findings: Key findings from the research
        confidence_level: Overall confidence level in research findings
        confidence_explanation: Explanation for the confidence level assessment
        final_report: Final research report content
        current_step: Current step in the workflow
        error: Error message if any step fails
    """

    # Conversation messages
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Conversation messages"
    )

    # Research topic and question
    research_topic: str | None = Field(
        default=None, description="Main topic of research"
    )

    research_question: str | None = Field(
        default=None, description="Specific research question"
    )

    # Context and parameters
    input_context: str | None = Field(
        default=None, description="Additional context provided by the user"
    )

    search_parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Parameters for search and research customization",
    )

    # Report sections and organization
    report_sections: list[dict[str, Any]] = Field(
        default_factory=list, description="Sections of the research report"
    )

    current_section_index: int | None = Field(
        default=None, description="Index of the current section being researched"
    )

    # Research queries and sources
    search_queries: list[dict[str, Any]] = Field(
        default_factory=list, description="List of search queries to execute"
    )

    query: str | None = Field(default=None, description="Current search query")

    # Document and source tracking
    retrieved_documents: list[Document] = Field(
        default_factory=list, description="Documents retrieved from search"
    )

    sources: list[dict[str, Any]] = Field(
        default_factory=list, description="Sources used in the research"
    )

    data_sources: list[dict[str, Any]] = Field(
        default_factory=list, description="Data sources available and used"
    )

    # Vector store documents for RAG
    vectorstore_documents: list[Document] = Field(
        default_factory=list, description="Documents loaded into vector store"
    )

    # Research findings
    research_findings: dict[str, Any] = Field(
        default_factory=dict, description="Key findings from the research"
    )

    # Assessment and confidence
    confidence_level: ResearchConfidenceLevel | None = Field(
        default=None, description="Overall confidence level in research findings"
    )

    confidence_explanation: str | None = Field(
        default=None, description="Explanation for the confidence level assessment"
    )

    # Final report
    final_report: str | None = Field(
        default=None, description="Final research report content"
    )

    # Process management
    current_step: str = Field(
        default="start", description="Current step in the workflow"
    )

    error: str | None = Field(
        default=None, description="Error message if any step fails"
    )


class ResearchInputState(BaseModel):
    """Input state for the research process.

    Represents the initial input to the research agent, including the
    user's query and any additional context.

    Attributes:
        messages: Input messages including user query
        input_context: Additional context provided for the research
        research_parameters: Optional parameters to customize the research process
    """

    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list, description="Input messages including user query"
    )
    input_context: str | None = Field(
        default=None, description="Additional context provided for the research"
    )
    research_parameters: dict[str, Any] | None = Field(
        default=None,
        description="Optional parameters to customize the research process",
    )


class ResearchOutputState(BaseModel):
    """Output state for the research process.

    Represents the final output from the research agent, including
    the completed report and confidence assessment.

    Attributes:
        final_report: Complete research report in markdown format
        confidence_level: Confidence level in the research findings
        sources: Sources used in the research
        messages: Conversation history including the assistant's final response
    """

    final_report: str = Field(description="Complete research report in markdown format")
    confidence_level: ResearchConfidenceLevel = Field(
        description="Confidence level in the research findings"
    )
    sources: list[dict[str, Any]] = Field(
        default_factory=list, description="Sources used in the research"
    )
    messages: Annotated[Sequence[BaseMessage], add_messages] = Field(
        default_factory=list,
        description="Conversation history including the assistant's final response",
    )


class WebSearchQuery(BaseModel):
    """Represents a web search query for retrieving information.

    Tracks a single search query, its purpose, execution status, and results.

    Attributes:
        query: The search query text
        purpose: Purpose of this search query
        data_source: Data source to query (web, github, academic, news, etc.)
        completed: Whether this query has been executed
        results: Search results
    """

    query: str = Field(description="The search query text")
    purpose: str = Field(description="Purpose of this search query")
    data_source: str = Field(
        description="Data source to query (web, github, academic, news, etc.)"
    )
    completed: bool = Field(
        default=False, description="Whether this query has been executed"
    )
    results: list[dict] = Field(default_factory=list, description="Search results")


class ReportSection(BaseModel):
    """Represents a section in the research report.

    Tracks a single report section, including its content, research needs,
    and associated queries and sources.

    Attributes:
        name: Section name
        description: Section description
        content: Section content
        requires_research: Whether this section requires research
        queries: Search queries for this section
        sources: Sources used in this section
        status: Section status (pending, in_progress, completed)
    """

    name: str = Field(description="Section name")
    description: str = Field(description="Section description")
    content: str = Field(default="", description="Section content")
    requires_research: bool = Field(
        default=True, description="Whether this section requires research"
    )
    queries: list[WebSearchQuery] = Field(
        default_factory=list, description="Search queries for this section"
    )
    sources: list[dict] = Field(
        default_factory=list, description="Sources used in this section"
    )
    status: str = Field(
        default="pending",
        description="Section status (pending, in_progress, completed)",
    )
