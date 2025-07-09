"""Specialized platform source registrations.

This module implements specialized loaders from langchain_community including:
- Academic and research platforms (arXiv, PubMed, bioRxiv)
- Media platforms (YouTube, audio/video processing)
- Development platforms (GitHub, GitLab, Git repositories)
- Domain-specific systems (Wikipedia, weather data, financial data)
"""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import Field, validator

from .enhanced_registry import enhanced_registry, register_file_source, register_source
from .source_types import (
    CredentialType,
    LoaderCapability,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)


class SpecializedPlatform(str, Enum):
    """Specialized platform types."""

    # Academic & Research
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    BIORXIV = "biorxiv"
    SEMANTIC_SCHOLAR = "semantic_scholar"

    # Media Platforms
    YOUTUBE = "youtube"
    BILIBILI = "bilibili"
    VIMEO = "vimeo"

    # Development Platforms
    GITHUB = "github"
    GITLAB = "gitlab"
    BITBUCKET = "bitbucket"

    # Knowledge Platforms
    WIKIPEDIA = "wikipedia"
    MEDIAWIKI = "mediawiki"

    # Domain-Specific
    WEATHER = "weather"
    FINANCIAL = "financial"
    NEWS = "news"


class ResearchField(str, Enum):
    """Academic research fields."""

    PHYSICS = "physics"
    MATHEMATICS = "mathematics"
    COMPUTER_SCIENCE = "cs"
    BIOLOGY = "biology"
    CHEMISTRY = "chemistry"
    MEDICINE = "medicine"
    ENGINEERING = "engineering"
    ECONOMICS = "economics"
    ALL_FIELDS = "all"


class MediaType(str, Enum):
    """Media content types."""

    VIDEO = "video"
    AUDIO = "audio"
    TRANSCRIPT = "transcript"
    SUBTITLES = "subtitles"
    METADATA = "metadata"


class DevelopmentDataType(str, Enum):
    """Development platform data types."""

    REPOSITORIES = "repositories"
    ISSUES = "issues"
    PULL_REQUESTS = "pull_requests"
    COMMITS = "commits"
    WIKI = "wiki"
    RELEASES = "releases"
    DISCUSSIONS = "discussions"


# =============================================================================
# Academic & Research Sources
# =============================================================================


@register_source(
    name="arxiv",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "arxiv": {
            "class": "ArxivLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["arxiv"],
        }
    },
    default_loader="arxiv",
    description="arXiv research paper loader with search and download",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.SEARCH,
        LoaderCapability.FILTERING,
        LoaderCapability.BULK_LOADING,
    ],
    priority=9,
)
class ArxivSource(RemoteSource):
    """arXiv research paper source."""

    source_type: str = "arxiv"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.ARXIV

    # Search parameters
    query: Optional[str] = Field(None, description="Search query string")
    arxiv_ids: Optional[List[str]] = Field(None, description="Specific arXiv IDs")
    max_results: int = Field(10, ge=1, le=100, description="Maximum papers to retrieve")

    # Filtering
    categories: Optional[List[str]] = Field(
        None, description="arXiv categories (e.g., cs.AI)"
    )
    date_filter: Optional[Dict[str, str]] = Field(None, description="Date range filter")

    # Content options
    load_full_text: bool = Field(True, description="Load full paper text")
    load_abstract_only: bool = Field(False, description="Only load abstracts")
    include_metadata: bool = Field(True, description="Include paper metadata")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.arxiv_ids:
            kwargs["doc_content_chars_max"] = None  # Load full content
            kwargs["load_all_available_meta"] = self.include_metadata
            # For specific IDs, create search query
            kwargs["query"] = " OR ".join([f"id:{id}" for id in self.arxiv_ids])
        elif self.query:
            kwargs["query"] = self.query
            kwargs["load_max_docs"] = self.max_results

        if self.categories:
            cat_query = " OR ".join([f"cat:{cat}" for cat in self.categories])
            if "query" in kwargs:
                kwargs["query"] = f"({kwargs['query']}) AND ({cat_query})"
            else:
                kwargs["query"] = cat_query

        return kwargs


@register_source(
    name="pubmed",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "pubmed": {
            "class": "PubMedLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["xmltodict"],
        }
    },
    default_loader="pubmed",
    description="PubMed biomedical literature database loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.SEARCH,
        LoaderCapability.FILTERING,
        LoaderCapability.BULK_LOADING,
    ],
    priority=9,
)
class PubMedSource(RemoteSource):
    """PubMed biomedical literature source."""

    source_type: str = "pubmed"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.PUBMED

    # Search parameters
    query: str = Field(..., description="PubMed search query")
    max_results: int = Field(10, ge=1, le=1000, description="Maximum results")

    # Content options
    load_full_text: bool = Field(False, description="Attempt to load full text")
    include_abstracts: bool = Field(True, description="Include abstracts")
    include_metadata: bool = Field(True, description="Include article metadata")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update({"query": self.query, "load_max_docs": self.max_results})

        return kwargs


@register_source(
    name="semantic_scholar",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "s2": {
            "class": "SemanticScholarLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["semanticscholar"],
        }
    },
    default_loader="s2",
    description="Semantic Scholar academic paper database",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.SEARCH,
        LoaderCapability.FILTERING,
        LoaderCapability.METADATA_EXTRACTION,
    ],
    priority=8,
)
class SemanticScholarSource(RemoteSource):
    """Semantic Scholar academic source."""

    source_type: str = "semantic_scholar"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.SEMANTIC_SCHOLAR

    # Search options
    query: Optional[str] = Field(None, description="Search query")
    paper_ids: Optional[List[str]] = Field(None, description="Specific paper IDs")
    author_id: Optional[str] = Field(None, description="Author ID to get papers from")

    # Filters
    year_range: Optional[tuple[int, int]] = Field(None, description="Year range filter")
    fields_of_study: Optional[List[str]] = Field(
        None, description="Fields of study filter"
    )

    # Content options
    include_citations: bool = Field(True, description="Include citation information")
    include_references: bool = Field(True, description="Include references")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.paper_ids:
            kwargs["paper_ids"] = self.paper_ids
        elif self.query:
            kwargs["query"] = self.query
        elif self.author_id:
            kwargs["author_id"] = self.author_id

        if self.year_range:
            kwargs["year_filter"] = self.year_range

        if self.fields_of_study:
            kwargs["fields_of_study"] = self.fields_of_study

        kwargs.update(
            {
                "include_citations": self.include_citations,
                "include_references": self.include_references,
            }
        )

        return kwargs


# =============================================================================
# Media Platform Sources
# =============================================================================


@register_source(
    name="youtube",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "transcript": {
            "class": "YoutubeLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["youtube-transcript-api"],
        },
        "audio": {
            "class": "YoutubeAudioLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["yt-dlp", "pydub", "librosa"],
        },
    },
    default_loader="transcript",
    description="YouTube video transcript and audio loader",
    requires_credentials=False,
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.STREAMING],
    priority=9,
)
class YouTubeSource(RemoteSource):
    """YouTube video source."""

    source_type: str = "youtube"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.YOUTUBE

    # Video identification
    video_url: Optional[str] = Field(None, description="YouTube video URL")
    video_id: Optional[str] = Field(None, description="YouTube video ID")
    playlist_id: Optional[str] = Field(None, description="YouTube playlist ID")
    channel_url: Optional[str] = Field(None, description="YouTube channel URL")

    # Content options
    media_type: MediaType = Field(
        MediaType.TRANSCRIPT, description="Type of content to load"
    )
    language: Optional[str] = Field(None, description="Transcript language")
    include_metadata: bool = Field(True, description="Include video metadata")

    # Audio options (for audio loader)
    save_audio_file: bool = Field(False, description="Save audio file locally")
    audio_format: str = Field("mp3", description="Audio format for download")

    @validator("video_id", always=True)
    def extract_video_id(cls, v, values):
        """Extract video ID from URL if provided."""
        if not v and values.get("video_url"):
            url = values["video_url"]
            if "youtube.com/watch?v=" in url:
                v = url.split("v=")[1].split("&")[0]
            elif "youtu.be/" in url:
                v = url.split("youtu.be/")[1].split("?")[0]
        return v

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.media_type == MediaType.TRANSCRIPT:
            kwargs["add_video_info"] = self.include_metadata
            if self.video_id:
                kwargs["video_id"] = self.video_id
            if self.language:
                kwargs["language"] = [self.language]
        elif self.media_type == MediaType.AUDIO:
            kwargs["save_dir"] = "./youtube_audio" if self.save_audio_file else None
            if self.video_url:
                kwargs["urls"] = [self.video_url]

        return kwargs


@register_source(
    name="bilibili",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "bilibili": {
            "class": "BiliBiliLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["bilibili-api-python"],
        }
    },
    default_loader="bilibili",
    description="Bilibili video platform loader",
    requires_credentials=True,
    credential_type=CredentialType.COOKIES,
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.RATE_LIMITED],
    priority=7,
)
class BilibiliSource(RemoteSource):
    """Bilibili video platform source."""

    source_type: str = "bilibili"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.BILIBILI

    # Video identification
    video_urls: List[str] = Field(..., description="Bilibili video URLs")

    # Authentication
    sessdata: Optional[str] = Field(None, description="SESSDATA cookie value")
    bili_jct: Optional[str] = Field(None, description="bili_jct cookie value")
    buvid3: Optional[str] = Field(None, description="buvid3 cookie value")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "video_urls": self.video_urls,
                "sessdata": self.sessdata,
                "bili_jct": self.bili_jct,
                "buvid3": self.buvid3,
            }
        )

        return kwargs


# =============================================================================
# Audio/Video Processing Sources
# =============================================================================


@register_file_source(
    name="audio_file",
    extensions=[".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg", ".wma"],
    loaders={
        "assembly": {
            "class": "AssemblyAIAudioTranscriptLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["assemblyai"],
        },
        "whisper": {
            "class": "WhisperParser",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["openai-whisper"],
        },
    },
    default_loader="whisper",
    description="Audio file transcription loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.STREAMING],
    priority=8,
)
class AudioFileSource(LocalFileSource):
    """Audio file transcription source."""

    source_type: str = "audio_file"
    category: SourceCategory = SourceCategory.SPECIALIZED

    # Transcription options
    language: Optional[str] = Field(None, description="Audio language")
    speaker_labels: bool = Field(False, description="Enable speaker diarization")
    timestamps: bool = Field(True, description="Include timestamps")

    # API configuration (for cloud services)
    api_key: Optional[str] = Field(
        None, description="API key for transcription service"
    )

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "file_path": str(self.path),
                "language": self.language,
                "speaker_labels": self.speaker_labels,
                "timestamps": self.timestamps,
            }
        )

        if self.api_key:
            kwargs["api_key"] = self.api_key

        return kwargs


# =============================================================================
# Development Platform Sources
# =============================================================================


@register_source(
    name="github",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "repo": {
            "class": "GitHubIssuesLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["PyGithub"],
        },
        "file": {
            "class": "GithubFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["PyGithub"],
        },
    },
    default_loader="repo",
    description="GitHub repository, issues, and file loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RATE_LIMITED,
    ],
    priority=9,
)
class GitHubSource(RemoteSource):
    """GitHub repository source."""

    source_type: str = "github"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.GITHUB

    # Repository identification
    repo: str = Field(..., description="Repository name (owner/repo)")
    access_token: Optional[str] = Field(None, description="GitHub access token")

    # Content selection
    data_types: List[DevelopmentDataType] = Field(
        default=[DevelopmentDataType.ISSUES], description="Types of data to load"
    )

    # Filtering
    branch: str = Field("main", description="Branch name")
    file_filter: Optional[str] = Field(None, description="File path filter")
    issue_state: str = Field("all", description="Issue state filter (open/closed/all)")

    # For file loading
    file_path: Optional[str] = Field(None, description="Specific file path")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "repo": self.repo,
                "access_token": (
                    self.access_token or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
            }
        )

        if DevelopmentDataType.ISSUES in self.data_types:
            kwargs["state"] = self.issue_state
            kwargs["include_prs"] = DevelopmentDataType.PULL_REQUESTS in self.data_types

        if self.file_path:
            kwargs["file_path"] = self.file_path
            kwargs["branch"] = self.branch

        return kwargs


@register_source(
    name="git",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "git": {
            "class": "GitLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["GitPython"],
        }
    },
    default_loader="git",
    description="Local Git repository loader",
    requires_credentials=False,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.FILTERING,
        LoaderCapability.RECURSIVE,
    ],
    priority=8,
)
class GitSource(LocalFileSource):
    """Local Git repository source."""

    source_type: str = "git"
    category: SourceCategory = SourceCategory.SPECIALIZED

    # Repository options
    repo_path: Path = Field(..., description="Path to Git repository")
    branch: str = Field("main", description="Branch to load from")

    # Content filtering
    file_filter: Optional[str] = Field(None, description="File pattern filter")
    include_commits: bool = Field(False, description="Include commit history")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "repo_path": str(self.repo_path),
                "branch": self.branch,
                "file_filter": self.file_filter,
            }
        )

        return kwargs


# =============================================================================
# Knowledge Platform Sources
# =============================================================================


@register_source(
    name="wikipedia",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "wikipedia": {
            "class": "WikipediaLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["wikipedia-api"],
        }
    },
    default_loader="wikipedia",
    description="Wikipedia article loader with search",
    requires_credentials=False,
    capabilities=[LoaderCapability.SEARCH, LoaderCapability.METADATA_EXTRACTION],
    priority=9,
)
class WikipediaSource(RemoteSource):
    """Wikipedia knowledge source."""

    source_type: str = "wikipedia"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.WIKIPEDIA

    # Search/load options
    query: Optional[str] = Field(None, description="Search query")
    page_titles: Optional[List[str]] = Field(None, description="Specific page titles")
    lang: str = Field("en", description="Wikipedia language")
    load_max_docs: int = Field(10, ge=1, le=50, description="Maximum documents")

    # Content options
    load_all_available_meta: bool = Field(True, description="Load all metadata")
    doc_content_chars_max: Optional[int] = Field(None, description="Max content length")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        if self.query:
            kwargs["query"] = self.query
        elif self.page_titles:
            # Wikipedia loader expects query even for specific pages
            kwargs["query"] = (
                self.page_titles[0] if len(self.page_titles) == 1 else None
            )
            kwargs["load_max_docs"] = len(self.page_titles)

        kwargs.update(
            {
                "lang": self.lang,
                "load_max_docs": self.load_max_docs,
                "load_all_available_meta": self.load_all_available_meta,
            }
        )

        if self.doc_content_chars_max:
            kwargs["doc_content_chars_max"] = self.doc_content_chars_max

        return kwargs


@register_source(
    name="mediawiki",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "mediawiki": {
            "class": "MWDumpLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["mwparserfromhell", "mwxml"],
        }
    },
    default_loader="mediawiki",
    description="MediaWiki XML dump loader",
    requires_credentials=False,
    capabilities=[LoaderCapability.BULK_LOADING, LoaderCapability.FILTERING],
    priority=7,
)
class MediaWikiSource(LocalFileSource):
    """MediaWiki dump source."""

    source_type: str = "mediawiki"
    category: SourceCategory = SourceCategory.SPECIALIZED

    # Dump file options
    encoding: str = Field("utf-8", description="File encoding")
    namespaces: Optional[List[int]] = Field(None, description="Namespaces to include")
    skip_redirects: bool = Field(True, description="Skip redirect pages")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "file_path": str(self.path),
                "encoding": self.encoding,
                "skip_redirects": self.skip_redirects,
            }
        )

        if self.namespaces:
            kwargs["namespaces"] = self.namespaces

        return kwargs


# =============================================================================
# Domain-Specific Sources
# =============================================================================


@register_source(
    name="weather",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "weather": {
            "class": "WeatherDataLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["openweathermap"],
        }
    },
    default_loader="weather",
    description="Weather data loader from OpenWeatherMap",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class WeatherSource(RemoteSource):
    """Weather data source."""

    source_type: str = "weather"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.WEATHER

    # Location
    locations: List[str] = Field(..., description="City names or coordinates")

    # API configuration
    openweathermap_api_key: Optional[str] = Field(
        None, description="OpenWeatherMap API key"
    )

    # Data options
    include_forecast: bool = Field(True, description="Include weather forecast")
    forecast_days: int = Field(5, ge=1, le=16, description="Number of forecast days")
    units: str = Field("metric", description="Units (metric/imperial)")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs.update(
            {
                "places": self.locations,
                "openweathermap_api_key": (
                    self.openweathermap_api_key or self.get_api_key()
                    if hasattr(self, "get_api_key")
                    else None
                ),
                "units": self.units,
            }
        )

        return kwargs


@register_source(
    name="financial_news",
    category=SourceCategory.SPECIALIZED,
    loaders={
        "alpha_vantage": {
            "class": "AlphaVantageLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["alpha-vantage"],
        }
    },
    default_loader="alpha_vantage",
    description="Financial news and market data loader",
    requires_credentials=True,
    credential_type=CredentialType.API_KEY,
    capabilities=[LoaderCapability.REAL_TIME, LoaderCapability.SEARCH],
    priority=8,
)
class FinancialNewsSource(RemoteSource):
    """Financial news and data source."""

    source_type: str = "financial_news"
    category: SourceCategory = SourceCategory.SPECIALIZED
    platform: SpecializedPlatform = SpecializedPlatform.FINANCIAL

    # Query options
    symbols: Optional[List[str]] = Field(None, description="Stock symbols")
    topics: Optional[List[str]] = Field(None, description="News topics")

    # API configuration
    api_key: Optional[str] = Field(None, description="Alpha Vantage API key")

    # Time range
    time_from: Optional[str] = Field(None, description="Start time (YYYYMMDDTHHMM)")
    time_to: Optional[str] = Field(None, description="End time (YYYYMMDDTHHMM)")

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()

        kwargs["api_key"] = (
            self.api_key or self.get_api_key() if hasattr(self, "get_api_key") else None
        )

        if self.symbols:
            kwargs["tickers"] = self.symbols
        if self.topics:
            kwargs["topics"] = self.topics
        if self.time_from:
            kwargs["time_from"] = self.time_from
        if self.time_to:
            kwargs["time_to"] = self.time_to

        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_specialized_sources_statistics() -> Dict[str, Any]:
    """Get statistics about specialized sources."""
    registry = enhanced_registry

    # Count by platform type
    platform_counts = {}
    for platform in SpecializedPlatform:
        count = len(
            [
                name
                for name, reg in registry._sources.items()
                if hasattr(reg, "platform")
                and getattr(reg, "platform", None) == platform
            ]
        )
        if count > 0:
            platform_counts[platform.value] = count

    # Category counts
    academic_count = len(
        [
            name
            for name in ["arxiv", "pubmed", "semantic_scholar", "biorxiv"]
            if name in registry._sources
        ]
    )

    media_count = len(
        [
            name
            for name in ["youtube", "bilibili", "audio_file", "vimeo"]
            if name in registry._sources
        ]
    )

    dev_count = len(
        [
            name
            for name in ["github", "gitlab", "git", "bitbucket"]
            if name in registry._sources
        ]
    )

    return {
        "total_specialized": len(
            registry.find_sources_by_category(SourceCategory.SPECIALIZED)
        ),
        "academic_sources": academic_count,
        "media_sources": media_count,
        "development_sources": dev_count,
        "platform_breakdown": platform_counts,
    }


def validate_specialized_sources() -> bool:
    """Validate specialized source registrations."""
    registry = enhanced_registry

    required_sources = ["arxiv", "pubmed", "youtube", "github", "git", "wikipedia"]

    missing = []
    for source_name in required_sources:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing specialized sources: {missing}")
        return False

    print("✅ All essential specialized sources registered!")
    return True


def detect_specialized_platform(url_or_path: str) -> Optional[SpecializedPlatform]:
    """Auto-detect specialized platform from URL or path."""
    lower = url_or_path.lower()

    patterns = {
        SpecializedPlatform.ARXIV: ["arxiv.org", "arxiv:"],
        SpecializedPlatform.PUBMED: ["pubmed.ncbi", "pmid:"],
        SpecializedPlatform.YOUTUBE: ["youtube.com", "youtu.be"],
        SpecializedPlatform.GITHUB: ["github.com"],
        SpecializedPlatform.WIKIPEDIA: ["wikipedia.org"],
        SpecializedPlatform.BILIBILI: ["bilibili.com"],
    }

    for platform, keywords in patterns.items():
        if any(keyword in lower for keyword in keywords):
            return platform

    return None


# Auto-validate on import
if __name__ == "__main__":
    validate_specialized_sources()
    stats = get_specialized_sources_statistics()
    print(f"Specialized Sources Statistics: {stats}")
