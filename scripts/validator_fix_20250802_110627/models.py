"""Models for the News Research Agent.

This module defines all Pydantic models used by the news research agent
for structured outputs, API parameters, and data validation.

Example:
    >>> from news_research.models import NewsApiParams, ArticleSummary
    >>> params = NewsApiParams(q="AI news", sources="bbc-news")
    >>> summary = ArticleSummary(title="...", summary="...", confidence=0.9)

Attributes:
    All models use Pydantic v2 with Field descriptions for documentation
    and validation. Models are designed to be serializable and type-safe.

Note:
    Following Haive conventions, all fields use descriptive names without
    underscores. Private attributes use PrivateAttr from Pydantic.
"""
from datetime import datetime
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, PrivateAttr, field_validator, model_validator
from pydantic.types import confloat, conint


class NewsApiParams(BaseModel):
    """Parameters for NewsAPI requests.

    This model structures the parameters needed to make NewsAPI calls,
    ensuring proper validation and formatting of search queries.

    Attributes:
        q: Search query keywords (1-3 concise terms)
        sources: Comma-separated list of news sources
        from_param: Start date for article search (YYYY-MM-DD format)
        to: End date for article search (YYYY-MM-DD format)
        language: Language code for articles (default: 'en')
        sort_by: Sort order for results
        page_size: Number of results per page

    Example:
        >>> params = NewsApiParams(
        ...     q="artificial intelligence",
        ...     sources="bbc-news,techcrunch",
        ...     from_param="2024-01-01",
        ...     to="2024-01-31"
        ... )
    """
    q: str = Field(description='1-3 concise keyword search terms that are not too specific', min_length=1, max_length=100)
    sources: str = Field(description='Comma-separated list of news sources', default='bbc-news,cnn,techcrunch,bloomberg,reuters')
    from_param: str = Field(description='Start date in YYYY-MM-DD format (minimum 2 days ago)', alias='from')
    to: str = Field(description='End date in YYYY-MM-DD format (default: today)', default_factory=lambda: datetime.now().strftime('%Y-%m-%d'))
    language: Literal['ar', 'de', 'en', 'es', 'fr', 'he', 'it', 'nl', 'no', 'pt', 'ru', 'se', 'ud', 'zh'] = Field(description='Language code for articles', default='en')
    sort_by: Literal['relevancy', 'popularity', 'publishedAt'] = Field(description='Sort order for results', default='relevancy')
    page_size: conint(ge=1, le=100) = Field(description='Number of results per page', default=20)

    @field_validator('from_param')
    def validate_from_date(cls, v: str) -> str:
        """Validate from_param is a valid date string."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('from_param must be in YYYY-MM-DD format')
        return v

    @field_validator('to')
    def validate_to_date(cls, v: str) -> str:
        """Validate to is a valid date string."""
        try:
            datetime.strptime(v, '%Y-%m-%d')
        except ValueError:
            raise ValueError('to must be in YYYY-MM-DD format')
        return v

    class Config:
        """Pydantic configuration."""
        populate_by_name = True

class ArticleMetadata(BaseModel):
    """Metadata for a news article.

    Represents the basic information about an article retrieved from NewsAPI
    before full text extraction.

    Attributes:
        title: Article headline
        url: Full URL to the article
        description: Brief article description
        source: News source information
        published_at: Publication timestamp
        author: Article author (if available)
    """
    title: str = Field(description='Article headline')
    url: str = Field(description='Full URL to the article')
    description: Optional[str] = Field(description='Brief article description', default=None)
    source: Dict[str, Any] = Field(description='News source information')
    published_at: Optional[datetime] = Field(description='Publication timestamp', default=None)
    author: Optional[str] = Field(description='Article author', default=None)

class ArticleContent(BaseModel):
    """Full article content with extracted text.

    Extends ArticleMetadata with the full text content extracted
    from web scraping.

    Attributes:
        title: Article headline
        url: Full URL to the article
        description: Brief article description
        text: Full article text content
        word_count: Number of words in the article
        extraction_confidence: Confidence score for text extraction
    """
    title: str = Field(description='Article headline')
    url: str = Field(description='Full URL to the article')
    description: Optional[str] = Field(description='Brief article description', default=None)
    text: str = Field(description='Full article text content', min_length=50)
    word_count: Optional[int] = Field(description='Number of words in the article', default=None)
    extraction_confidence: confloat(ge=0.0, le=1.0) = Field(description='Confidence score for text extraction quality', default=1.0)

    @model_validator(mode='after')
    def calculate_word_count(self) -> 'ArticleContent':
        """Calculate word count if not provided."""
        if self.word_count is None and self.text:
            self.word_count = len(self.text.split())
        return self

class ArticleSummary(BaseModel):
    """Summarized article with key points.

    Represents a fully processed article with title, URL, and
    bullet-point summary.

    Attributes:
        title: Article headline
        url: Full URL to the article
        summary: Bullet-point summary of key points
        relevance_score: How relevant the article is to the query
        key_topics: Main topics covered in the article
    """
    title: str = Field(description='Article headline')
    url: str = Field(description='Full URL to the article')
    summary: List[str] = Field(description='Bullet-point summary of key points', min_items=3, max_items=10)
    relevance_score: confloat(ge=0.0, le=1.0) = Field(description='Relevance score to the search query')
    key_topics: List[str] = Field(description='Main topics covered in the article', default_factory=list)

class SearchDecision(BaseModel):
    """Decision model for search continuation logic.

    Used by the agent to decide whether to continue searching
    or proceed with analysis.

    Attributes:
        action: Next action to take
        reason: Explanation for the decision
        confidence: Confidence in the decision
    """
    action: Literal['continue_search', 'analyze', 'insufficient_data'] = Field(description='Next action to take in the workflow')
    reason: str = Field(description='Explanation for the decision', min_length=10)
    confidence: confloat(ge=0.0, le=1.0) = Field(description='Confidence in this decision')

class ResearchAnalysis(BaseModel):
    """Analysis results from collected articles.

    Comprehensive analysis of all collected articles including
    themes, patterns, and insights.

    Attributes:
        main_themes: Primary themes identified across articles
        key_findings: Most important discoveries
        conflicting_info: Any contradictions found
        confidence_level: Overall confidence in the analysis
        data_gaps: Missing information or areas needing more research
        trend_analysis: Identified trends or patterns
    """
    main_themes: List[str] = Field(description='Primary themes identified across articles', min_items=1)
    key_findings: List[str] = Field(description='Most important discoveries from the research', min_items=1)
    conflicting_info: List[str] = Field(description='Contradictions or conflicting information found', default_factory=list)
    confidence_level: confloat(ge=0.0, le=1.0) = Field(description='Overall confidence in the analysis')
    data_gaps: List[str] = Field(description='Missing information or areas needing more research', default_factory=list)
    trend_analysis: Optional[Dict[str, str]] = Field(description='Identified trends or patterns in the data', default=None)

class ResearchReport(BaseModel):
    """Final research report structure.

    Complete research report with executive summary, detailed sections,
    and recommendations.

    Attributes:
        title: Report title
        executive_summary: High-level summary of findings
        sections: Detailed report sections
        recommendations: Actionable recommendations
        sources_count: Number of sources analyzed
        confidence_score: Overall confidence in the report
        metadata: Additional report metadata
    """
    title: str = Field(description='Report title', min_length=10, max_length=200)
    executive_summary: str = Field(description='High-level summary of findings', min_length=100, max_length=500)
    sections: List[Dict[str, str]] = Field(description='Report sections with heading and content', min_items=2)
    recommendations: List[str] = Field(description='Actionable recommendations based on research', min_items=1)
    sources_count: int = Field(description='Number of sources analyzed', ge=0)
    confidence_score: confloat(ge=0.0, le=1.0) = Field(description='Overall confidence in the report')
    metadata: Dict[str, Any] = Field(description='Additional report metadata', default_factory=dict)
    _generation_time: datetime = PrivateAttr(default_factory=datetime.now)
    _version: str = PrivateAttr(default='1.0.0')

    @field_validator('sections')
    def validate_sections(cls, v: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Ensure each section has required fields."""
        for section in v:
            if 'heading' not in section or 'content' not in section:
                raise ValueError("Each section must have 'heading' and 'content' fields")
        return v

    def to_markdown(self) -> str:
        """Convert report to markdown format.

        Returns:
            str: Formatted markdown string of the report

        Example:
            >>> report = ResearchReport(...)
            >>> markdown = report.to_markdown()
            >>> print(markdown)
        """
        md_parts = [f'# {self.title}', f'\n## Executive Summary\n{self.executive_summary}', '\n---\n']
        for section in self.sections:
            md_parts.append(f'\n## {section['heading']}\n{section['content']}')
        md_parts.append('\n## Recommendations')
        for i, rec in enumerate(self.recommendations, 1):
            md_parts.append(f'{i}. {rec}')
        md_parts.append(f'\n---\n*Report generated with {self.sources_count} sources*')
        md_parts.append(f'*Confidence Score: {self.confidence_score:.2f}*')
        return '\n'.join(md_parts)

class ErrorResponse(BaseModel):
    """Error response model for agent failures.

    Structured error information for debugging and user feedback.

    Attributes:
        error_type: Classification of the error
        message: Human-readable error message
        details: Additional error context
        timestamp: When the error occurred
        recoverable: Whether the operation can be retried
    """
    error_type: str = Field(description='Type of error encountered')
    message: str = Field(description='Human-readable error message')
    details: Optional[Dict[str, Any]] = Field(description='Additional error context', default=None)
    timestamp: datetime = Field(description='When the error occurred', default_factory=datetime.now)
    recoverable: bool = Field(description='Whether the operation can be retried', default=True)