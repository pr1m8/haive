"""Models for the open_perplexity research agent.

This module defines data models used for representing, tracking, and evaluating
research sources, findings, and summaries. It includes enumerations for categorizing
data source types, content reliability, freshness, and research depth.
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field, field_validator


class DataSourceType(str, Enum):
    """Enumeration of data source types.

    Categorizes the different types of sources where research information can be found.

    Attributes:
        WEB: General web content
        GITHUB: Code repositories and issues from GitHub
        ACADEMIC: Academic papers and research publications
        NEWS: News articles and press releases
        SOCIAL_MEDIA: Content from social media platforms
        DOCUMENTS: Uploaded or local documents
        API: Data retrieved from APIs
        OTHER: Any other source type not covered above
    """

    WEB = "web"
    GITHUB = "github"
    ACADEMIC = "academic"
    NEWS = "news"
    SOCIAL_MEDIA = "social_media"
    DOCUMENTS = "documents"
    API = "api"
    OTHER = "other"


class ContentReliability(str, Enum):
    """Enumeration of content reliability levels.

    Categorizes the trustworthiness and reliability of information sources.

    Attributes:
        HIGH: Highly reliable sources (peer-reviewed, authoritative)
        MEDIUM: Moderately reliable sources (reputable but not authoritative)
        LOW: Low reliability sources (potentially biased or unverified)
        UNKNOWN: Sources with unknown or unclear reliability
    """

    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class ContentFreshness(str, Enum):
    """Enumeration of content freshness levels.

    Categorizes how recent or up-to-date the information content is.

    Attributes:
        VERY_RECENT: Content from the last few days
        RECENT: Content from the last few weeks
        SOMEWHAT_RECENT: Content from the last few months
        OUTDATED: Content from years ago
        UNKNOWN: Content with unknown or unclear publication date
    """

    VERY_RECENT = "very_recent"  # Days
    RECENT = "recent"  # Weeks
    SOMEWHAT_RECENT = "somewhat_recent"  # Months
    OUTDATED = "outdated"  # Years
    UNKNOWN = "unknown"


class ResearchDepth(str, Enum):
    """Enumeration of research depth levels.

    Categorizes the comprehensiveness and thoroughness of the research.

    Attributes:
        SUPERFICIAL: Basic overview with minimal sources
        INTERMEDIATE: Moderate depth with several sources
        DEEP: In-depth research with many high-quality sources
        COMPREHENSIVE: Exhaustive research with extensive sources
    """

    SUPERFICIAL = "superficial"
    INTERMEDIATE = "intermediate"
    DEEP = "deep"
    COMPREHENSIVE = "comprehensive"


class ResearchSource(BaseModel):
    """Model for tracking and evaluating research sources.

    Represents a source of information used in research, including metadata
    about its reliability, relevance, and content.

    Attributes:
        url: URL of the source
        title: Title of the source
        source_type: Type of data source
        content_snippet: Snippet of relevant content
        reliability: Assessed reliability of the source
        freshness: Content freshness/recency
        relevance_score: Relevance score from 0.0 to 1.0
        citation: Formatted citation for the source
        access_timestamp: When the source was accessed
    """

    url: str | None = Field(default=None, description="URL of the source")
    title: str | None = Field(default=None, description="Title of the source")
    source_type: DataSourceType = Field(
        default=DataSourceType.WEB, description="Type of data source"
    )
    content_snippet: str | None = Field(
        default=None, description="Snippet of relevant content"
    )
    reliability: ContentReliability = Field(
        default=ContentReliability.UNKNOWN, description="Assessed reliability"
    )
    freshness: ContentFreshness = Field(
        default=ContentFreshness.UNKNOWN, description="Content freshness/recency"
    )
    relevance_score: float = Field(
        default=0.0, ge=0.0, le=1.0, description="Relevance score (0.0 - 1.0)"
    )
    citation: str | None = Field(
        default=None, description="Formatted citation for the source"
    )
    access_timestamp: str | None = Field(
        default=None, description="When the source was accessed"
    )

    @field_validator("relevance_score")
    def validate_relevance_score(cls, v):
        """Ensure relevance score is between 0 and 1.

        Args:
            v: The relevance score to validate

        Returns:
            float: The validated relevance score, clamped between 0.0 and 1.0
        """
        return max(0.0, min(1.0, v))


class ResearchFinding(BaseModel):
    """Model for a specific research finding.

    Represents an individual insight or finding from the research,
    including supporting sources and confidence assessment.

    Attributes:
        finding: The actual finding or insight
        confidence: Confidence level in this finding (0.0 - 1.0)
        sources: Sources supporting this finding
        explanation: Explanation of the finding's significance
        related_findings: Related findings
    """

    finding: str = Field(description="The actual finding or insight")
    confidence: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence in this finding (0.0 - 1.0)",
    )
    sources: list[ResearchSource] = Field(
        default_factory=list, description="Sources supporting this finding"
    )
    explanation: str | None = Field(
        default=None, description="Explanation of the finding's significance"
    )
    related_findings: list[str] = Field(
        default_factory=list, description="Related findings"
    )

    @field_validator("confidence")
    def validate_confidence(cls, v):
        """Ensure confidence is between 0 and 1.

        Args:
            v: The confidence value to validate

        Returns:
            float: The validated confidence value, clamped between 0.0 and 1.0
        """
        return max(0.0, min(1.0, v))


class ResearchSummary(BaseModel):
    """Summary of research findings and assessment.

    Provides an overall summary of the research, including key findings,
    assessment of source quality, and confidence evaluation.

    Attributes:
        topic: Research topic
        question: Specific research question
        key_findings: Key findings from research
        sources_count: Total number of sources consulted
        high_reliability_sources: Number of high reliability sources
        recent_sources: Number of recent sources
        research_depth: Overall research depth
        contradictions: Contradictory findings identified
        confidence_score: Overall confidence score
        limitations: Research limitations
    """

    topic: str = Field(description="Research topic")
    question: str | None = Field(default=None, description="Specific research question")
    key_findings: list[ResearchFinding] = Field(
        default_factory=list, description="Key findings from research"
    )
    sources_count: int = Field(
        default=0, description="Total number of sources consulted"
    )
    high_reliability_sources: int = Field(
        default=0, description="Number of high reliability sources"
    )
    recent_sources: int = Field(default=0, description="Number of recent sources")
    research_depth: ResearchDepth = Field(
        default=ResearchDepth.SUPERFICIAL, description="Overall research depth"
    )
    contradictions: list[str] = Field(
        default_factory=list, description="Contradictory findings identified"
    )
    confidence_score: float = Field(
        default=0.5, ge=0.0, le=1.0, description="Overall confidence score"
    )
    limitations: list[str] = Field(
        default_factory=list, description="Research limitations"
    )

    @field_validator("confidence_score")
    def validate_confidence_score(cls, v):
        """Ensure confidence score is between 0 and 1.

        Args:
            v: The confidence score to validate

        Returns:
            float: The validated confidence score, clamped between 0.0 and 1.0
        """
        return max(0.0, min(1.0, v))

    def assess_depth(self) -> ResearchDepth:
        """Assess research depth based on source counts and diversity.

        Evaluates the depth of research based on the number of sources
        and the proportion of high reliability sources.

        Returns:
            ResearchDepth: The assessed research depth level
        """
        if self.sources_count >= 20 and self.high_reliability_sources >= 10:
            return ResearchDepth.COMPREHENSIVE
        if self.sources_count >= 10 and self.high_reliability_sources >= 5:
            return ResearchDepth.DEEP
        if self.sources_count >= 5 and self.high_reliability_sources >= 2:
            return ResearchDepth.INTERMEDIATE
        return ResearchDepth.SUPERFICIAL


class DataSourceConfig(BaseModel):
    """Configuration for a data source.

    Specifies parameters for interacting with a particular data source,
    including API keys and search parameters.

    Attributes:
        name: Name of the data source
        source_type: Type of data source
        enabled: Whether this source is enabled
        priority: Priority (1-10, higher = more important)
        api_key: API key for the data source if required
        max_results: Maximum number of results to return
        search_params: Custom search parameters
    """

    name: str = Field(description="Name of the data source")
    source_type: DataSourceType = Field(description="Type of data source")
    enabled: bool = Field(default=True, description="Whether this source is enabled")
    priority: int = Field(
        default=5, ge=1, le=10, description="Priority (1-10, higher = more important)"
    )
    api_key: str | None = Field(
        default=None, description="API key for the data source if required"
    )
    max_results: int = Field(
        default=10, description="Maximum number of results to return"
    )
    search_params: dict[str, Any] = Field(
        default_factory=dict, description="Custom search parameters"
    )

    @field_validator("priority")
    def validate_priority(cls, v):
        """Ensure priority is between 1 and 10.

        Args:
            v: The priority value to validate

        Returns:
            int: The validated priority value, clamped between 1 and 10
        """
        return max(1, min(10, v))
