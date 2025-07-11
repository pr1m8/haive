"""Additional comprehensive source registrations to reach 231 langchain_community loaders.

This module implements additional loaders from langchain_community including:
- Academic and research platforms
- News and media sources
- API documentation sources
- Knowledge management systems
- Collaboration tools
- Specialized file formats
- Social platforms
- Developer tools
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import Field

from .enhanced_registry import enhanced_registry, register_bulk_source, register_source
from .source_types import (
    CredentialType,
    DatabaseSource,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)

# =============================================================================
# Academic and Research Sources
# =============================================================================


@register_source(
    name="biorxiv",
    category=SourceCategory.ACADEMIC_RESEARCH,
    loaders={
        "biorxiv": {
            "class": "BiorxivLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests", "beautifulsoup4"],
        }
    },
    default_loader="biorxiv",
    description="bioRxiv preprint repository loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class BiorxivSource(RemoteSource):
    """bioRxiv preprint source."""

    source_type: str = "biorxiv"
    query: str = Field(..., description="Search query")
    max_results: int = Field(10, description="Maximum results")


@register_source(
    name="medrxiv",
    category=SourceCategory.ACADEMIC_RESEARCH,
    loaders={
        "medrxiv": {
            "class": "MedrxivLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests", "beautifulsoup4"],
        }
    },
    default_loader="medrxiv",
    description="medRxiv medical preprint repository loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class MedrxivSource(RemoteSource):
    """medRxiv medical preprint source."""

    source_type: str = "medrxiv"
    query: str = Field(..., description="Search query")
    max_results: int = Field(10, description="Maximum results")


@register_source(
    name="ssrn",
    category=SourceCategory.ACADEMIC_RESEARCH,
    loaders={
        "ssrn": {
            "class": "SSRNLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="ssrn",
    description="SSRN social science research network loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class SSRNSource(RemoteSource):
    """SSRN research paper source."""

    source_type: str = "ssrn"
    paper_id: Optional[str] = Field(None, description="SSRN paper ID")
    query: Optional[str] = Field(None, description="Search query")


# =============================================================================
# News and Media Sources
# =============================================================================


@register_source(
    name="news_api",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "newsapi": {
            "class": "NewsAPILoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["newsapi-python"],
        }
    },
    default_loader="newsapi",
    description="News API aggregator loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.SEARCH],
    priority=8,
)
class NewsAPISource(RemoteSource):
    """News API aggregator source."""

    source_type: str = "news_api"
    query: str = Field(..., description="Search query")
    sources: Optional[List[str]] = Field(None, description="News sources")
    from_date: Optional[datetime] = Field(None, description="Start date")
    to_date: Optional[datetime] = Field(None, description="End date")


@register_source(
    name="hackernews_search",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "hn_search": {
            "class": "HNSearchLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="hn_search",
    description="Hacker News search API loader",
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.COMMENTS],
    priority=7,
)
class HackerNewsSearchSource(RemoteSource):
    """Hacker News search source."""

    source_type: str = "hackernews_search"
    query: str = Field(..., description="Search query")
    search_type: str = Field("story", description="story, comment, or all")
    max_results: int = Field(10, description="Maximum results")


@register_source(
    name="the_guardian",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "guardian": {
            "class": "GuardianLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="guardian",
    description="The Guardian news article loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class GuardianSource(RemoteSource):
    """The Guardian news source."""

    source_type: str = "the_guardian"
    query: str = Field(..., description="Search query")
    section: Optional[str] = Field(None, description="News section")
    from_date: Optional[datetime] = Field(None, description="Start date")


# =============================================================================
# Developer and API Documentation
# =============================================================================


@register_source(
    name="postman_collection",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "postman": {
            "class": "PostmanCollectionLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="postman",
    description="Postman API collection loader",
    file_extensions=[".json"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class PostmanCollectionSource(LocalFileSource):
    """Postman collection source."""

    source_type: str = "postman_collection"
    category: SourceCategory = SourceCategory.DEVELOPMENT_VCS


@register_source(
    name="swagger_api",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "swagger": {
            "class": "SwaggerLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyyaml"],
        }
    },
    default_loader="swagger",
    description="Swagger/OpenAPI documentation loader",
    file_extensions=[".yaml", ".yml", ".json"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=8,
)
class SwaggerAPISource(LocalFileSource):
    """Swagger/OpenAPI documentation source."""

    source_type: str = "swagger_api"
    category: SourceCategory = SourceCategory.DEVELOPMENT_VCS


@register_source(
    name="gitlab",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "gitlab": {
            "class": "GitLabLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-gitlab"],
        }
    },
    default_loader="gitlab",
    description="GitLab repository and issue loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class GitLabSource(RemoteSource):
    """GitLab repository source."""

    source_type: str = "gitlab"
    project_id: str = Field(..., description="GitLab project ID")
    branch: str = Field("main", description="Branch name")
    file_pattern: Optional[str] = Field(None, description="File pattern to match")


# =============================================================================
# Knowledge Management Systems
# =============================================================================


@register_source(
    name="roam_research",
    category=SourceCategory.KNOWLEDGE_PERSONAL,
    loaders={
        "roam": {
            "class": "RoamLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="roam",
    description="Roam Research knowledge graph loader",
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=7,
)
class RoamResearchSource(LocalFileSource):
    """Roam Research export source."""

    source_type: str = "roam_research"
    category: SourceCategory = SourceCategory.KNOWLEDGE_PERSONAL


@register_source(
    name="logseq",
    category=SourceCategory.KNOWLEDGE_PERSONAL,
    loaders={
        "logseq": {
            "class": "LogseqLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="logseq",
    description="Logseq knowledge management loader",
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=7,
)
class LogseqSource(LocalFileSource):
    """Logseq knowledge base source."""

    source_type: str = "logseq"
    category: SourceCategory = SourceCategory.KNOWLEDGE_PERSONAL


@register_source(
    name="dendron",
    category=SourceCategory.KNOWLEDGE_PERSONAL,
    loaders={
        "dendron": {
            "class": "DendronLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="dendron",
    description="Dendron hierarchical note-taking loader",
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.RECURSIVE],
    priority=7,
)
class DendronSource(LocalFileSource):
    """Dendron note-taking source."""

    source_type: str = "dendron"
    category: SourceCategory = SourceCategory.KNOWLEDGE_PERSONAL


# =============================================================================
# Social Media and Forums
# =============================================================================


@register_source(
    name="linkedin",
    category=SourceCategory.SOCIAL_MEDIA,
    loaders={
        "linkedin": {
            "class": "LinkedInLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["linkedin-api"],
        }
    },
    default_loader="linkedin",
    description="LinkedIn profile and post loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.CONTACT_SYNC, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class LinkedInSource(RemoteSource):
    """LinkedIn social media source."""

    source_type: str = "linkedin"
    profile_url: Optional[str] = Field(None, description="Profile URL")
    company_url: Optional[str] = Field(None, description="Company page URL")


@register_source(
    name="facebook",
    category=SourceCategory.SOCIAL_MEDIA,
    loaders={
        "facebook": {
            "class": "FacebookPostsLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["facebook-sdk"],
        }
    },
    default_loader="facebook",
    description="Facebook posts and pages loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.MEDIA_CONTENT, LoaderCapability.COMMENTS],
    priority=7,
)
class FacebookSource(RemoteSource):
    """Facebook social media source."""

    source_type: str = "facebook"
    page_id: Optional[str] = Field(None, description="Facebook page ID")
    group_id: Optional[str] = Field(None, description="Facebook group ID")


@register_source(
    name="instagram",
    category=SourceCategory.SOCIAL_MEDIA,
    loaders={
        "instagram": {
            "class": "InstagramLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["instaloader"],
        }
    },
    default_loader="instagram",
    description="Instagram posts and stories loader",
    requires_credentials=True,
    credential_type=CredentialType.USERNAME_PASSWORD,
    capabilities=[LoaderCapability.MEDIA_CONTENT, LoaderCapability.COMMENTS],
    priority=6,
)
class InstagramSource(RemoteSource):
    """Instagram social media source."""

    source_type: str = "instagram"
    username: str = Field(..., description="Instagram username")
    include_stories: bool = Field(False, description="Include stories")


# =============================================================================
# Specialized File Formats
# =============================================================================


@register_source(
    name="asciidoc",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "asciidoc": {
            "class": "AsciiDocLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="asciidoc",
    description="AsciiDoc documentation format loader",
    file_extensions=[".adoc", ".asciidoc", ".asc"],
    capabilities=[LoaderCapability.TEXT_EXTRACTION],
    priority=7,
)
class AsciiDocSource(LocalFileSource):
    """AsciiDoc documentation source."""

    source_type: str = "asciidoc"
    category: SourceCategory = SourceCategory.FILE_DOCUMENT


@register_source(
    name="org_mode",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "org": {
            "class": "OrgModeLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="org",
    description="Emacs Org-mode document loader",
    file_extensions=[".org"],
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class OrgModeSource(LocalFileSource):
    """Org-mode document source."""

    source_type: str = "org_mode"
    category: SourceCategory = SourceCategory.FILE_DOCUMENT


@register_source(
    name="textile",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "textile": {
            "class": "TextileLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["textile"],
        }
    },
    default_loader="textile",
    description="Textile markup language loader",
    file_extensions=[".textile"],
    capabilities=[LoaderCapability.TEXT_EXTRACTION],
    priority=6,
)
class TextileSource(LocalFileSource):
    """Textile markup source."""

    source_type: str = "textile"
    category: SourceCategory = SourceCategory.FILE_DOCUMENT


# =============================================================================
# E-commerce and Business
# =============================================================================


@register_source(
    name="stripe",
    category=SourceCategory.BUSINESS,
    loaders={
        "stripe": {
            "class": "StripeLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["stripe"],
        }
    },
    default_loader="stripe",
    description="Stripe payment data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.REAL_TIME],
    priority=8,
)
class StripeSource(RemoteSource):
    """Stripe payment platform source."""

    source_type: str = "stripe"
    resource_type: str = Field("charges", description="Stripe resource type")
    limit: int = Field(100, description="Number of records")


@register_source(
    name="square",
    category=SourceCategory.BUSINESS,
    loaders={
        "square": {
            "class": "SquareLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["squareup"],
        }
    },
    default_loader="square",
    description="Square payment and POS data loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.REAL_TIME],
    priority=7,
)
class SquareSource(RemoteSource):
    """Square payment platform source."""

    source_type: str = "square"
    location_id: str = Field(..., description="Square location ID")
    object_type: str = Field("payments", description="Object type to load")


# =============================================================================
# Media and Content Platforms
# =============================================================================


@register_source(
    name="vimeo",
    category=SourceCategory.MEDIA_VIDEO,
    loaders={
        "vimeo": {
            "class": "VimeoLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["vimeo"],
        }
    },
    default_loader="vimeo",
    description="Vimeo video platform loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.MEDIA_CONTENT, LoaderCapability.TRANSCRIPTS],
    priority=7,
)
class VimeoSource(RemoteSource):
    """Vimeo video platform source."""

    source_type: str = "vimeo"
    video_id: Optional[str] = Field(None, description="Specific video ID")
    channel_id: Optional[str] = Field(None, description="Channel ID")


@register_source(
    name="twitch",
    category=SourceCategory.MEDIA_VIDEO,
    loaders={
        "twitch": {
            "class": "TwitchLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["python-twitch-client"],
        }
    },
    default_loader="twitch",
    description="Twitch streaming platform loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.CHAT_LOGS],
    priority=6,
)
class TwitchSource(RemoteSource):
    """Twitch streaming platform source."""

    source_type: str = "twitch"
    channel_name: str = Field(..., description="Twitch channel name")
    include_chat: bool = Field(True, description="Include chat messages")


# =============================================================================
# Productivity and Office Tools
# =============================================================================


@register_source(
    name="onenote",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "onenote": {
            "class": "OneNoteLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["msal"],
        }
    },
    default_loader="onenote",
    description="Microsoft OneNote notebook loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[
        LoaderCapability.STRUCTURED_DATA,
        LoaderCapability.COLLABORATIVE_EDITING,
    ],
    priority=8,
)
class OneNoteSource(RemoteSource):
    """Microsoft OneNote source."""

    source_type: str = "onenote"
    notebook_id: Optional[str] = Field(None, description="Specific notebook ID")
    section_id: Optional[str] = Field(None, description="Specific section ID")


@register_source(
    name="apple_notes",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "apple_notes": {
            "class": "AppleNotesLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="apple_notes",
    description="Apple Notes app loader (macOS)",
    capabilities=[LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class AppleNotesSource(LocalFileSource):
    """Apple Notes source."""

    source_type: str = "apple_notes"
    category: SourceCategory = SourceCategory.BUSINESS_PRODUCTIVITY


# =============================================================================
# Analytics and BI Platforms
# =============================================================================


@register_source(
    name="looker",
    category=SourceCategory.ANALYTICS,
    loaders={
        "looker": {
            "class": "LookerLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["looker-sdk"],
        }
    },
    default_loader="looker",
    description="Looker business intelligence platform loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.VISUALIZATION],
    priority=8,
)
class LookerSource(RemoteSource):
    """Looker BI platform source."""

    source_type: str = "looker"
    dashboard_id: Optional[str] = Field(None, description="Dashboard ID")
    look_id: Optional[str] = Field(None, description="Look ID")


@register_source(
    name="metabase",
    category=SourceCategory.ANALYTICS,
    loaders={
        "metabase": {
            "class": "MetabaseLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="metabase",
    description="Metabase open-source BI tool loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.QUERY],
    priority=7,
)
class MetabaseSource(RemoteSource):
    """Metabase analytics source."""

    source_type: str = "metabase"
    question_id: Optional[int] = Field(None, description="Question ID")
    collection_id: Optional[int] = Field(None, description="Collection ID")


# =============================================================================
# Communication and Support
# =============================================================================


@register_source(
    name="zendesk",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "zendesk": {
            "class": "ZendeskLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["zenpy"],
        }
    },
    default_loader="zendesk",
    description="Zendesk support ticket loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.SEARCH],
    priority=8,
)
class ZendeskSource(RemoteSource):
    """Zendesk support platform source."""

    source_type: str = "zendesk"
    subdomain: str = Field(..., description="Zendesk subdomain")
    ticket_status: str = Field("all", description="Ticket status filter")


@register_source(
    name="freshdesk",
    category=SourceCategory.COMMUNICATION,
    loaders={
        "freshdesk": {
            "class": "FreshdeskLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="freshdesk",
    description="Freshdesk customer support loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.FILTERING],
    priority=7,
)
class FreshdeskSource(RemoteSource):
    """Freshdesk support source."""

    source_type: str = "freshdesk"
    domain: str = Field(..., description="Freshdesk domain")
    ticket_filter: Optional[str] = Field(None, description="Ticket filter")


# =============================================================================
# Database and Data Warehouse
# =============================================================================


@register_source(
    name="clickhouse",
    category=SourceCategory.DATABASE_SQL,
    loaders={
        "clickhouse": {
            "class": "ClickHouseLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["clickhouse-driver"],
        }
    },
    default_loader="clickhouse",
    description="ClickHouse columnar database loader",
    requires_credentials=True,
    credential_type=CredentialType.CONNECTION_STRING,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.QUERY],
    priority=8,
)
class ClickHouseSource(DatabaseSource):
    """ClickHouse database source."""

    source_type: str = "clickhouse"
    cluster: Optional[str] = Field(None, description="ClickHouse cluster")


@register_source(
    name="duckdb",
    category=SourceCategory.DATABASE_SQL,
    loaders={
        "duckdb": {
            "class": "DuckDBLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["duckdb"],
        }
    },
    default_loader="duckdb",
    description="DuckDB embedded analytical database loader",
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.QUERY],
    priority=8,
)
class DuckDBSource(DatabaseSource):
    """DuckDB analytical database source."""

    source_type: str = "duckdb"
    database_path: str = Field(":memory:", description="Database file path")


# =============================================================================
# File Processing Tools
# =============================================================================


@register_source(
    name="tesseract_ocr",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "tesseract": {
            "class": "TesseractOCRLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pytesseract", "pillow"],
        }
    },
    default_loader="tesseract",
    description="Tesseract OCR for scanned documents",
    file_extensions=[".png", ".jpg", ".jpeg", ".tiff", ".bmp"],
    capabilities=[LoaderCapability.OCR, LoaderCapability.TEXT_EXTRACTION],
    priority=8,
)
class TesseractOCRSource(LocalFileSource):
    """Tesseract OCR source for images."""

    source_type: str = "tesseract_ocr"
    language: str = Field("eng", description="OCR language")


@register_source(
    name="camelot_tables",
    category=SourceCategory.FILE_DOCUMENT,
    loaders={
        "camelot": {
            "class": "CamelotLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["camelot-py"],
        }
    },
    default_loader="camelot",
    description="Camelot table extraction from PDFs",
    file_extensions=[".pdf"],
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.TEXT_EXTRACTION],
    priority=7,
)
class CamelotTablesSource(LocalFileSource):
    """Camelot PDF table extraction source."""

    source_type: str = "camelot_tables"
    pages: str = Field("all", description="Pages to extract tables from")


# =============================================================================
# Geographic and Mapping
# =============================================================================


@register_source(
    name="openstreetmap",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "osm": {
            "class": "OpenStreetMapLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["osmium", "shapely"],
        }
    },
    default_loader="osm",
    description="OpenStreetMap geographic data loader",
    capabilities=[LoaderCapability.GEOSPATIAL_DATA, LoaderCapability.STRUCTURED_DATA],
    priority=7,
)
class OpenStreetMapSource(RemoteSource):
    """OpenStreetMap geographic data source."""

    source_type: str = "openstreetmap"
    bbox: List[float] = Field(
        ..., description="Bounding box [min_lon, min_lat, max_lon, max_lat]"
    )
    tags: Optional[Dict[str, str]] = Field(None, description="OSM tags to filter")


# =============================================================================
# Gaming and Virtual Worlds
# =============================================================================


@register_source(
    name="steam",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "steam": {
            "class": "SteamLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["steam"],
        }
    },
    default_loader="steam",
    description="Steam gaming platform data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=6,
)
class SteamSource(RemoteSource):
    """Steam gaming platform source."""

    source_type: str = "steam"
    app_id: Optional[int] = Field(None, description="Steam app ID")
    user_id: Optional[str] = Field(None, description="Steam user ID")


# =============================================================================
# Financial Data
# =============================================================================


@register_source(
    name="alpha_vantage",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "alphavantage": {
            "class": "AlphaVantageLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["alpha-vantage"],
        }
    },
    default_loader="alphavantage",
    description="Alpha Vantage financial data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.TIMESERIES_DATA],
    priority=8,
)
class AlphaVantageSource(RemoteSource):
    """Alpha Vantage financial data source."""

    source_type: str = "alpha_vantage"
    symbol: str = Field(..., description="Stock symbol")
    function: str = Field("TIME_SERIES_DAILY", description="API function")


# =============================================================================
# IoT and Sensor Data
# =============================================================================


@register_source(
    name="mqtt",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "mqtt": {
            "class": "MQTTLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["paho-mqtt"],
        }
    },
    default_loader="mqtt",
    description="MQTT IoT message broker loader",
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.SENSOR_DATA],
    priority=7,
)
class MQTTSource(RemoteSource):
    """MQTT IoT messaging source."""

    source_type: str = "mqtt"
    broker_host: str = Field(..., description="MQTT broker host")
    topic: str = Field(..., description="MQTT topic to subscribe")
    port: int = Field(1883, description="MQTT broker port")


# =============================================================================
# Legal and Compliance
# =============================================================================


@register_source(
    name="sec_edgar",
    category=SourceCategory.GOVERNMENT,
    loaders={
        "edgar": {
            "class": "SECEdgarLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["sec-edgar-downloader"],
        }
    },
    default_loader="edgar",
    description="SEC EDGAR financial filings loader",
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.SEARCH],
    priority=8,
)
class SECEdgarSource(RemoteSource):
    """SEC EDGAR filings source."""

    source_type: str = "sec_edgar"
    ticker: str = Field(..., description="Company ticker symbol")
    filing_type: str = Field("10-K", description="Filing type (10-K, 10-Q, 8-K)")
    start_date: Optional[datetime] = Field(None, description="Start date")


# =============================================================================
# Package Repositories
# =============================================================================


@register_source(
    name="pypi",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "pypi": {
            "class": "PyPILoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="pypi",
    description="Python Package Index (PyPI) loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.SEARCH],
    priority=7,
)
class PyPISource(RemoteSource):
    """PyPI package repository source."""

    source_type: str = "pypi"
    package_name: str = Field(..., description="Python package name")
    include_readme: bool = Field(True, description="Include README content")


@register_source(
    name="npm",
    category=SourceCategory.DEVELOPMENT_VCS,
    loaders={
        "npm": {
            "class": "NPMLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["requests"],
        }
    },
    default_loader="npm",
    description="NPM JavaScript package registry loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.SEARCH],
    priority=7,
)
class NPMSource(RemoteSource):
    """NPM package registry source."""

    source_type: str = "npm"
    package_name: str = Field(..., description="NPM package name")
    include_readme: bool = Field(True, description="Include README content")


# =============================================================================
# Time Tracking and Project Management
# =============================================================================


@register_source(
    name="toggl",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "toggl": {
            "class": "TogglLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["toggl-cli"],
        }
    },
    default_loader="toggl",
    description="Toggl time tracking data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.TIMESERIES_DATA],
    priority=7,
)
class TogglSource(RemoteSource):
    """Toggl time tracking source."""

    source_type: str = "toggl"
    workspace_id: str = Field(..., description="Toggl workspace ID")
    start_date: datetime = Field(..., description="Start date for time entries")
    end_date: datetime = Field(..., description="End date for time entries")


# =============================================================================
# Weather and Environmental Data
# =============================================================================


@register_source(
    name="openweather",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "openweather": {
            "class": "OpenWeatherLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pyowm"],
        }
    },
    default_loader="openweather",
    description="OpenWeather weather data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.GEOSPATIAL_DATA],
    priority=7,
)
class OpenWeatherSource(RemoteSource):
    """OpenWeather API source."""

    source_type: str = "openweather"
    location: str = Field(..., description="Location for weather data")
    forecast_days: int = Field(1, description="Number of forecast days")


# =============================================================================
# Blockchain and Crypto
# =============================================================================


@register_source(
    name="etherscan",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "etherscan": {
            "class": "EtherscanLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["etherscan-python"],
        }
    },
    default_loader="etherscan",
    description="Etherscan blockchain explorer loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BLOCKCHAIN_DATA,
        LoaderCapability.TRANSACTION_HISTORY,
    ],
    priority=7,
)
class EtherscanSource(RemoteSource):
    """Etherscan blockchain explorer source."""

    source_type: str = "etherscan"
    address: str = Field(..., description="Ethereum address")
    network: str = Field("mainnet", description="Ethereum network")


# =============================================================================
# Calendar and Scheduling
# =============================================================================


@register_source(
    name="google_calendar",
    category=SourceCategory.BUSINESS_PRODUCTIVITY,
    loaders={
        "gcal": {
            "class": "GoogleCalendarLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["google-api-python-client"],
        }
    },
    default_loader="gcal",
    description="Google Calendar events loader",
    requires_credentials=True,
    credential_type=CredentialType.OAUTH,
    capabilities=[LoaderCapability.STRUCTURED_DATA, LoaderCapability.REAL_TIME],
    priority=8,
)
class GoogleCalendarSource(RemoteSource):
    """Google Calendar source."""

    source_type: str = "google_calendar"
    calendar_id: str = Field("primary", description="Calendar ID")
    time_min: Optional[datetime] = Field(None, description="Start time")
    time_max: Optional[datetime] = Field(None, description="End time")


# Register all sources on import
__all__ = [
    # Academic
    "BiorxivSource",
    "MedrxivSource",
    "SSRNSource",
    # News
    "NewsAPISource",
    "HackerNewsSearchSource",
    "GuardianSource",
    # Developer
    "PostmanCollectionSource",
    "SwaggerAPISource",
    "GitLabSource",
    # Knowledge
    "RoamResearchSource",
    "LogseqSource",
    "DendronSource",
    # Social
    "LinkedInSource",
    "FacebookSource",
    "InstagramSource",
    # File formats
    "AsciiDocSource",
    "OrgModeSource",
    "TextileSource",
    # Business
    "StripeSource",
    "SquareSource",
    # Media
    "VimeoSource",
    "TwitchSource",
    # Productivity
    "OneNoteSource",
    "AppleNotesSource",
    # Analytics
    "LookerSource",
    "MetabaseSource",
    # Support
    "ZendeskSource",
    "FreshdeskSource",
    # Database
    "ClickHouseSource",
    "DuckDBSource",
    # OCR
    "TesseractOCRSource",
    "CamelotTablesSource",
    # Geographic
    "OpenStreetMapSource",
    # Gaming
    "SteamSource",
    # Financial
    "AlphaVantageSource",
    # IoT
    "MQTTSource",
    # Legal
    "SECEdgarSource",
    # Package repos
    "PyPISource",
    "NPMSource",
    # Time tracking
    "TogglSource",
    # Weather
    "OpenWeatherSource",
    # Blockchain
    "EtherscanSource",
    # Calendar
    "GoogleCalendarSource",
]
