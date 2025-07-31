"""Data models for Pro Search Agent."""

from typing import Any

from pydantic import BaseModel, Field

from haive.agents.memory.search.base import SearchResponse


class SearchRefinement(BaseModel):
    """Model for search query refinements."""

    original_query: str = Field(..., description="Original user query")
    refined_query: str = Field(..., description="Refined search query")
    refinement_reason: str = Field(..., description="Why the query was refined")


class ContextualInsight(BaseModel):
    """Model for contextual insights from search."""

    insight: str = Field(..., description="The contextual insight")
    relevance_score: float = Field(..., ge=0.0, le=1.0, description="Relevance score")
    source_type: str = Field(..., description="Type of source (memory, web, etc.)")


class ProSearchResponse(SearchResponse):
    """Response model for pro search operations.

    Extends the base SearchResponse with pro search specific fields.
    """

    search_type: str = Field(
        default="ProSearch", description="Type of search performed"
    )
    refinements: list[SearchRefinement] = Field(
        default_factory=list, description="Query refinements made"
    )
    contextual_insights: list[ContextualInsight] = Field(
        default_factory=list, description="Contextual insights"
    )
    user_preferences_applied: dict[str, Any] = Field(
        default_factory=dict, description="User preferences considered"
    )
    reasoning_steps: list[str] = Field(
        default_factory=list, description="Reasoning steps taken"
    )
    follow_up_questions: list[str] = Field(
        default_factory=list, description="Suggested follow-up questions"
    )
    depth_level: int = Field(
        default=1, ge=1, le=5, description="Depth level of search (1-5)"
    )

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "How can I improve my productivity while working from home?",
                "response": "Based on your preferences for structured approaches and technology solutions, here are evidence-based strategies to improve work-from-home productivity:\n\n1. **Create a dedicated workspace**: Set up a specific area for work to maintain psychological boundaries...",
                "sources": ["harvard.edu", "mit.edu", "productivity-blog.com"],
                "confidence": 0.88,
                "search_type": "ProSearch",
                "processing_time": 3.2,
                "refinements": [
                    {
                        "original_query": "How can I improve my productivity while working from home?",
                        "refined_query": "evidence-based work from home productivity strategies structured approach",
                        "refinement_reason": "Added specificity for evidence-based and structured approaches based on user preferences",
                    }
                ],
                "contextual_insights": [
                    {
                        "insight": "User prefers structured, actionable advice over general tips",
                        "relevance_score": 0.9,
                        "source_type": "memory",
                    }
                ],
                "user_preferences_applied": {
                    "learning_style": "structured",
                    "preferred_sources": ["academic", "research-based"],
                    "format_preference": "numbered_lists",
                },
                "reasoning_steps": [
                    "Analyzed user query for intent and context",
                    "Retrieved relevant user preferences from memory",
                    "Identified need for evidence-based approaches",
                    "Structured response with actionable steps",
                ],
                "follow_up_questions": [
                    "What specific work-from-home challenges are you facing?",
                    "Would you like recommendations for productivity tools?",
                    "Are there particular times of day when you struggle most with focus?",
                ],
                "depth_level": 3,
                "metadata": {},
            }
        }


class ProSearchRequest(BaseModel):
    """Request model for pro search operations."""

    query: str = Field(..., min_length=1, max_length=1000, description="Search query")
    context: dict[str, Any] | None = Field(
        default=None, description="Additional context"
    )
    depth_level: int = Field(
        default=3, ge=1, le=5, description="Desired depth level (1-5)"
    )
    include_reasoning: bool = Field(default=True, description="Include reasoning steps")
    generate_follow_ups: bool = Field(
        default=True, description="Generate follow-up questions"
    )
    use_preferences: bool = Field(default=True, description="Apply user preferences")

    class Config:
        """Pydantic configuration."""

        json_schema_extra = {
            "example": {
                "query": "What are the best practices for machine learning model deployment?",
                "context": {"domain": "enterprise", "experience_level": "intermediate"},
                "depth_level": 4,
                "include_reasoning": True,
                "generate_follow_ups": True,
                "use_preferences": True,
            }
        }
