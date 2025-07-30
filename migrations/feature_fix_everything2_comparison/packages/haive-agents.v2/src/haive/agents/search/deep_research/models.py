"""Data models for Deep Research Agent."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from haive.agents.memory.search.base import SearchResponse


class ResearchSource(BaseModel):
    """Model for research source with detailed metadata."""

    url: str = Field(..., description="Source URL")
    title: str = Field(..., description="Source title")
    author: str | None = Field(default=None, description="Author if available")
    publication_date: datetime | None = Field(
        default=None, description="Publication date"
    )
    domain: str = Field(..., description="Source domain")
    credibility_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Credibility assessment"
    )
    relevance_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Relevance to query"
    )
    content_snippet: str = Field(default="", description="Relevant content excerpt")
    source_type: str = Field(
        default="web", description="Type of source (web, academic, news, etc.)"
    )


class ResearchSection(BaseModel):
    """Model for a section of the research report."""

    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")
    sources: list[ResearchSource] = Field(
        default_factory=list, description="Sources for this section"
    )
    key_points: list[str] = Field(
        default_factory=list, description="Key points from this section"
    )
    confidence_level: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Confidence in this section"
    )


class ResearchQuery(BaseModel):
    """Model for individual research queries performed."""

    query: str = Field(..., description="The research query")
    query_type: str = Field(
        ..., description="Type of query (background, specific, validation)"
    )
    results_found: int = Field(default=0, description="Number of results found")
    processing_time: float = Field(
        default=0.0, description="Time to process this query"
    )
    success: bool = Field(default=True, description="Whether query was successful")


class DeepResearchResponse(SearchResponse):
    """Response model for deep research operations.

    Extends the base SearchResponse with deep research specific fields.
    """

    search_type: str = Field(
        default="DeepResearch", description="Type of search performed"
    )
    research_sections: list[ResearchSection] = Field(
        default_factory=list, description="Research report sections"
    )
    executive_summary: str = Field(
        default="", description="Executive summary of findings"
    )
    research_queries: list[ResearchQuery] = Field(
        default_factory=list, description="Queries performed"
    )
    total_sources_examined: int = Field(default=0, description="Total sources examined")
    high_quality_sources: int = Field(
        default=0, description="High quality sources found"
    )
    research_depth: int = Field(
        default=1, ge=1, le=5, description="Research depth level"
    )
    limitations: list[str] = Field(
        default_factory=list, description="Research limitations"
    )
    related_topics: list[str] = Field(
        default_factory=list, description="Related topics discovered"
    )
    fact_checks: list[dict[str, Any]] = Field(
        default_factory=list, description="Fact checking results"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "What are the environmental impacts of electric vehicles?",
                "response": "# Environmental Impacts of Electric Vehicles: A Comprehensive Analysis\n\n## Executive Summary\n\nElectric vehicles (EVs) present both environmental benefits and challenges...",
                "sources": ["nature.com", "science.org", "epa.gov"],
                "confidence": 0.85,
                "search_type": "DeepResearch",
                "processing_time": 45.2,
                "executive_summary": "Electric vehicles show significant environmental benefits over traditional vehicles, with lifecycle emissions 40-60% lower despite manufacturing challenges.",
                "research_sections": [
                    {
                        "title": "Manufacturing Impact",
                        "content": "EV battery production requires significant energy and rare earth materials...",
                        "sources": [],
                        "key_points": [
                            "Battery production is energy-intensive",
                            "Rare earth mining concerns",
                        ],
                        "confidence_level": 0.8,
                    }
                ],
                "research_queries": [
                    {
                        "query": "electric vehicle lifecycle emissions studies",
                        "query_type": "background",
                        "results_found": 25,
                        "processing_time": 12.3,
                        "success": True,
                    }
                ],
                "total_sources_examined": 47,
                "high_quality_sources": 12,
                "research_depth": 4,
                "limitations": ["Limited data on long-term battery disposal"],
                "related_topics": [
                    "Battery recycling",
                    "Renewable energy grid integration",
                ],
                "fact_checks": [],
                "metadata": {},
            }
        }


class DeepResearchRequest(BaseModel):
    """Request model for deep research operations."""

    query: str = Field(..., min_length=1, max_length=2000, description="Research query")
    research_depth: int = Field(
        default=3, ge=1, le=5, description="Research depth level (1-5)"
    )
    focus_areas: list[str] = Field(
        default_factory=list, description="Specific areas to focus on"
    )
    source_types: list[str] = Field(
        default_factory=list, description="Preferred source types"
    )
    time_period: str | None = Field(
        default=None, description="Time period for sources (e.g., 'last_5_years')"
    )
    include_fact_checking: bool = Field(
        default=True, description="Include fact checking"
    )
    max_sources: int = Field(default=50, description="Maximum sources to examine")
    generate_report: bool = Field(
        default=True, description="Generate structured report"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "Impact of artificial intelligence on healthcare outcomes",
                "research_depth": 4,
                "focus_areas": [
                    "diagnostic accuracy",
                    "treatment efficiency",
                    "patient outcomes",
                ],
                "source_types": ["academic", "clinical_trials", "meta_analysis"],
                "time_period": "last_3_years",
                "include_fact_checking": True,
                "max_sources": 40,
                "generate_report": True,
            }
        }
