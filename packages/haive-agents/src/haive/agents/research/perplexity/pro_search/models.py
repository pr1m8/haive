# perplexity_search_models.py
"""Pydantic models for Perplexity-style quick search workflow.
These models support a multi-stage search process with reasoning, query generation,
parallel search execution, and synthesis.
"""

from datetime import datetime
from typing import Any, Dict, List, Literal, Optional, Set, Union

from pydantic import BaseModel, Field, computed_field, field_validator, model_validator
from pydantic.functional_validators import AfterValidator
from typing_extensions import Annotated

# ============================================================================
# Query Understanding and Context Models
# ============================================================================


class SearchContext(BaseModel):
    """Context information for search query understanding."""

    current_date: datetime = Field(
        default_factory=datetime.now,
        description="Current date and time for temporal context",
    )
    user_location: str | None = Field(
        default=None, description="User's location for geo-specific searches"
    )
    search_history: list[str] = Field(
        default_factory=list, description="Recent search queries for context"
    )
    domain_preferences: set[str] = Field(
        default_factory=set, description="Preferred domains or sources"
    )

    @computed_field
    @property
    def temporal_context(self) -> dict[str, str]:
        """Generate temporal context strings."""
        now = self.current_date
        return {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "day_of_week": now.strftime("%A"),
            "month_year": now.strftime("%B %Y"),
            "relative_time": self._get_relative_time(),
        }

    def _get_relative_time(self) -> str:
        """Get relative time context (morning, afternoon, etc.)."""
        hour = self.current_date.hour
        if 5 <= hour < 12:
            return "morning"
        if 12 <= hour < 17:
            return "afternoon"
        if 17 <= hour < 21:
            return "evening"
        return "night"


class QueryIntent(BaseModel):
    """Analyzed intent and characteristics of a search query."""

    intent_type: Literal[
        "factual",
        "comparison",
        "how-to",
        "definition",
        "current_events",
        "analysis",
        "recommendation",
        "navigation",
    ] = Field(description="Primary intent of the query")

    temporal_scope: Literal["historical", "current", "future", "timeless"] = Field(
        default="timeless", description="Temporal relevance of the query"
    )

    complexity_level: Literal["simple", "moderate", "complex"] = Field(
        default="moderate", description="Estimated complexity of the query"
    )

    required_sources: int = Field(
        default=3, ge=1, le=10, description="Estimated number of sources needed"
    )

    key_entities: list[str] = Field(
        default_factory=list, description="Key entities identified in the query"
    )

    related_concepts: list[str] = Field(
        default_factory=list, description="Related concepts that might enhance search"
    )

    @field_validator("required_sources")
    @classmethod
    def adjust_sources_by_complexity(cls, v, info):
        """Adjust required sources based on complexity."""
        if "complexity_level" in info.data:
            complexity = info.data["complexity_level"]
            if complexity == "simple" and v > 3:
                return 3
            if complexity == "complex" and v < 5:
                return 5
        return v


# ============================================================================
# Query Reasoning and Expansion Models
# ============================================================================


class QueryReasoning(BaseModel):
    """Reasoning output for query understanding and expansion."""

    original_query: str = Field(description="Original user query")

    understanding: str = Field(
        description="Natural language understanding of what the user is asking"
    )

    search_strategy: str = Field(
        description="Strategy for searching this query effectively"
    )

    potential_challenges: list[str] = Field(
        default_factory=list,
        description="Potential challenges in finding accurate information",
    )

    expansion_rationale: str = Field(
        description="Reasoning for how to expand or refine the query"
    )

    intent_analysis: QueryIntent = Field(description="Detailed intent analysis")

    @model_validator(mode="after")
    def validate_reasoning_completeness(self) -> "QueryReasoning":
        """Ensure reasoning provides actionable insights."""
        if len(self.understanding) < 20:
            raise ValueError("Understanding must be substantive (>20 chars)")

        if not self.search_strategy:
            self.search_strategy = f"Search for {self.intent_analysis.intent_type} information about {', '.join(self.intent_analysis.key_entities[:2])}"

        return self


# ============================================================================
# Search Query Generation Models
# ============================================================================


class SearchQueryConfig(BaseModel):
    """Configuration for individual search queries."""

    query_text: str = Field(
        min_length=1, max_length=200, description="The search query text"
    )

    query_type: Literal["primary", "supporting", "verification", "expansion"] = Field(
        default="primary", description="Type/purpose of this query"
    )

    target_source_types: list[
        Literal["web", "academic", "news", "wiki", "social", "video", "image"]
    ] = Field(
        default_factory=lambda: ["web"],
        description="Preferred source types for this query",
    )

    expected_result_type: Literal[
        "facts", "list", "explanation", "comparison", "tutorial", "mixed"
    ] = Field(default="mixed", description="Expected type of results")

    priority: int = Field(
        default=1, ge=1, le=5, description="Priority level (1=highest, 5=lowest)"
    )

    @field_validator("query_text")
    @classmethod
    def clean_query_text(cls, v):
        """Clean and validate query text."""
        # Remove excessive whitespace
        v = " ".join(v.split())
        # Remove dangerous characters
        v = v.replace('"', "").replace("'", "")
        return v


class QueryBatch(BaseModel):
    """Batch of queries to execute in parallel."""

    reasoning: QueryReasoning = Field(description="Reasoning that led to these queries")

    queries: list[SearchQueryConfig] = Field(
        min_length=1, max_length=10, description="List of queries to execute"
    )

    execution_strategy: Literal["parallel", "sequential", "priority"] = Field(
        default="parallel", description="How to execute these queries"
    )

    @model_validator(mode="after")
    def validate_query_diversity(self) -> "QueryBatch":
        """Ensure queries are diverse and non-redundant."""
        query_texts = [q.query_text.lower() for q in self.queries]

        # Check for duplicate queries
        if len(query_texts) != len(set(query_texts)):
            raise ValueError("Duplicate queries detected")

        # Ensure priority distribution
        priorities = [q.priority for q in self.queries]
        if len(self.queries) > 3 and all(p == priorities[0] for p in priorities):
            # Distribute priorities
            for i, query in enumerate(self.queries):
                query.priority = min(i + 1, 5)

        return self

    @computed_field
    @property
    def primary_queries(self) -> list[SearchQueryConfig]:
        """Get primary queries only."""
        return [q for q in self.queries if q.query_type == "primary"]

    @computed_field
    @property
    def total_expected_results(self) -> int:
        """Calculate total expected results based on queries."""
        return len(self.queries) * 5  # Assuming 5 results per query average


# ============================================================================
# Search Result Models
# ============================================================================


class SearchResult(BaseModel):
    """Individual search result with metadata."""

    url: str = Field(description="URL of the result")
    title: str = Field(description="Title of the result")
    snippet: str = Field(description="Snippet/summary of the result")

    relevance_score: float = Field(ge=0.0, le=1.0, description="Relevance score")

    source_type: Literal[
        "web", "academic", "news", "wiki", "social", "video", "image"
    ] = Field(default="web")

    publish_date: datetime | None = Field(
        default=None, description="Publication date if available"
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )

    @computed_field
    @property
    def age_days(self) -> int | None:
        """Calculate age of content in days."""
        if self.publish_date:
            return (datetime.now() - self.publish_date).days
        return None

    @computed_field
    @property
    def is_recent(self) -> bool:
        """Check if content is recent (< 30 days)."""
        return self.age_days is not None and self.age_days < 30


class SearchQueryResult(BaseModel):
    """Results for a single search query."""

    query: SearchQueryConfig = Field(description="The query that was executed")
    results: list[SearchResult] = Field(
        default_factory=list, description="Search results"
    )
    execution_time_ms: int = Field(
        ge=0, description="Query execution time in milliseconds"
    )
    error: str | None = Field(default=None, description="Error message if query failed")

    @computed_field
    @property
    def success(self) -> bool:
        """Check if query executed successfully."""
        return self.error is None and len(self.results) > 0

    @computed_field
    @property
    def top_results(self) -> list[SearchResult]:
        """Get top 3 results by relevance."""
        return sorted(self.results, key=lambda x: x.relevance_score, reverse=True)[:3]


# ============================================================================
# Analysis and Synthesis Models
# ============================================================================


class ContentAnalysis(BaseModel):
    """Analysis of search results content."""

    key_findings: list[str] = Field(
        min_length=1, description="Key findings from the search results"
    )

    common_themes: list[str] = Field(
        default_factory=list, description="Common themes across results"
    )

    contradictions: list[dict[str, str]] = Field(
        default_factory=list, description="Contradictions found between sources"
    )

    confidence_level: Literal["high", "medium", "low"] = Field(
        default="medium", description="Confidence in the findings"
    )

    gaps_identified: list[str] = Field(
        default_factory=list, description="Information gaps that remain"
    )

    @model_validator(mode="after")
    def adjust_confidence_by_contradictions(self) -> "ContentAnalysis":
        """Adjust confidence based on contradictions."""
        if len(self.contradictions) > 2 and self.confidence_level == "high":
            self.confidence_level = "medium"
        elif len(self.contradictions) > 4:
            self.confidence_level = "low"
        return self


class SearchSynthesis(BaseModel):
    """Final synthesis of search results."""

    query_batch: QueryBatch = Field(description="Original query batch")

    search_results: list[SearchQueryResult] = Field(description="All search results")

    analysis: ContentAnalysis = Field(description="Analysis of the content")

    summary: str = Field(min_length=50, description="Comprehensive summary of findings")

    answer_completeness: float = Field(
        ge=0.0, le=1.0, description="How completely the search answered the query"
    )

    follow_up_queries: list[str] = Field(
        default_factory=list, max_length=5, description="Suggested follow-up queries"
    )

    citations: list[dict[str, str]] = Field(
        default_factory=list, description="Citations for key claims"
    )

    @computed_field
    @property
    def total_sources_used(self) -> int:
        """Count total unique sources used."""
        urls = set()
        for result in self.search_results:
            urls.update(r.url for r in result.results)
        return len(urls)

    @computed_field
    @property
    def requires_follow_up(self) -> bool:
        """Determine if follow-up search is needed."""
        return (
            self.answer_completeness < 0.7
            or len(self.analysis.gaps_identified) > 2
            or self.analysis.confidence_level == "low"
        )

    @model_validator(mode="after")
    def ensure_citations(self) -> "SearchSynthesis":
        """Ensure citations are provided for summary."""
        if not self.citations and self.total_sources_used > 0:
            # Auto-generate basic citations
            for result in self.search_results[:3]:
                if result.success and result.top_results:
                    top = result.top_results[0]
                    self.citations.append(
                        {
                            "claim": f"Information about {result.query.query_text}",
                            "source": top.title,
                            "url": top.url,
                        }
                    )
        return self


# ============================================================================
# State Model for Search Workflow
# ============================================================================


class PerplexitySearchState(BaseModel):
    """Complete state for Perplexity-style search workflow."""

    # Input
    user_query: str = Field(description="Original user query")
    context: SearchContext = Field(
        default_factory=SearchContext, description="Search context"
    )

    # Processing stages
    reasoning: QueryReasoning | None = Field(
        default=None, description="Query reasoning and understanding"
    )

    query_batch: QueryBatch | None = Field(
        default=None, description="Generated search queries"
    )

    search_results: list[SearchQueryResult] = Field(
        default_factory=list, description="Raw search results"
    )

    synthesis: SearchSynthesis | None = Field(
        default=None, description="Final synthesis"
    )

    # Workflow control
    iteration_count: int = Field(default=0, description="Number of search iterations")

    max_iterations: int = Field(default=2, description="Maximum search iterations")

    @computed_field
    @property
    def is_complete(self) -> bool:
        """Check if search workflow is complete."""
        return (
            self.synthesis is not None and not self.synthesis.requires_follow_up
        ) or self.iteration_count >= self.max_iterations

    @computed_field
    @property
    def next_action(
        self,
    ) -> Literal["reason", "generate_queries", "search", "synthesize", "complete"]:
        """Determine next action in workflow."""
        if self.synthesis and self.is_complete:
            return "complete"
        if not self.reasoning:
            return "reason"
        if not self.query_batch:
            return "generate_queries"
        if len(self.search_results) < len(self.query_batch.queries):
            return "search"
        return "synthesize"
