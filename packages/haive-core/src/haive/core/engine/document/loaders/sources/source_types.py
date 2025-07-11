"""Comprehensive source type system with proper typing for all langchain_community loaders.

This module defines the complete hierarchy of source types to support all 231
langchain_community document loaders with proper categorization and typing.
"""

from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Set, Union

from pydantic import BaseModel, Field, SecretStr

from haive.core.common.mixins.secure_config import SecureConfigMixin


class SourceCategory(str, Enum):
    """High-level source categories for organization."""

    # File-based sources
    FILE_DOCUMENT = "file_document"  # PDF, Word, etc.
    FILE_DATA = "file_data"  # CSV, JSON, etc.
    FILE_CODE = "file_code"  # Python, notebooks, etc.
    FILE_MEDIA = "file_media"  # Images, audio, etc.
    LOCAL_FILE = "local_file"  # General local files
    ARCHIVE = "archive"  # ZIP, TAR, etc.

    # Web-based sources
    WEB = "web"  # General web content
    WEB_SCRAPING = "web_scraping"  # URLs, web pages
    WEB_DOCUMENTATION = "web_documentation"  # Docs sites, wikis
    API = "api"  # REST APIs, GraphQL

    # Directory sources
    DIRECTORY_LOCAL = "directory_local"  # Local directories
    DIRECTORY_CLOUD = "directory_cloud"  # Cloud storage

    # Database sources
    DATABASE = "database"  # General database
    DATABASE_SQL = "database_sql"  # SQL databases
    DATABASE_NOSQL = "database_nosql"  # NoSQL databases

    # Cloud storage
    CLOUD_STORAGE = "cloud_storage"  # S3, GCS, Azure

    # Messaging sources
    MESSAGING = "messaging"  # General messaging
    MESSAGING_CHAT = "messaging_chat"  # Discord, Slack, etc.
    MESSAGING_EMAIL = "messaging_email"  # Email systems

    # Business sources
    BUSINESS = "business"  # General business tools
    BUSINESS_CRM = "business_crm"  # CRM systems
    BUSINESS_PRODUCTIVITY = "business_productivity"  # Office tools

    # Academic sources
    ACADEMIC_RESEARCH = "academic_research"  # arXiv, PubMed
    ACADEMIC_EDUCATION = "academic_education"  # Educational platforms

    # Knowledge management
    KNOWLEDGE_PERSONAL = "knowledge_personal"  # Obsidian, notes
    KNOWLEDGE_TEAM = "knowledge_team"  # Confluence, wikis

    # Media sources
    MEDIA_VIDEO = "media_video"  # YouTube, video platforms
    MEDIA_AUDIO = "media_audio"  # Audio processing

    # Social media
    SOCIAL_MEDIA = "social_media"  # Twitter, Reddit

    # Development
    DEVELOPMENT_VCS = "development_vcs"  # Git, GitHub

    # Analytics and specialized
    ANALYTICS = "analytics"  # Analytics platforms
    SPECIALIZED = "specialized"  # Specialized domains
    SPECIALIZED_DOMAIN = "specialized_domain"  # Domain-specific

    # Others
    COMMUNICATION = "communication"  # General communication
    GOVERNMENT = "government"  # Government sources
    HEALTHCARE = "healthcare"  # Healthcare systems
    EDUCATION = "education"  # Education platforms
    UNKNOWN = "unknown"  # Unknown category


class CredentialType(str, Enum):
    """Types of credentials required by sources."""

    NONE = "none"
    API_KEY = "api_key"
    ACCESS_KEY = "access_key"  # AWS/cloud access keys
    OAUTH = "oauth"  # OAuth 1.0/2.0
    OAUTH_TOKEN = "oauth_token"
    SERVICE_ACCOUNT = "service_account"  # Service account JSON
    CONNECTION_STRING = "connection_string"
    USERNAME_PASSWORD = "username_password"
    PASSWORD = "password"  # Simple password authentication
    SSH_KEY = "ssh_key"
    CLOUD_CREDENTIALS = "cloud_credentials"
    BEARER_TOKEN = "bearer_token"  # Bearer tokens
    COOKIES = "cookies"  # Cookie-based authentication
    JWT = "jwt"  # JSON Web Token
    CUSTOM = "custom"


class LoaderCapability(str, Enum):
    """Capabilities that loaders can have."""

    BULK_LOADING = "bulk_loading"  # Can load multiple items at once
    RECURSIVE = "recursive"  # Can recursively traverse structures
    STREAMING = "streaming"  # Supports streaming large data
    INCREMENTAL = "incremental"  # Supports incremental updates
    FILTERING = "filtering"  # Supports content filtering
    METADATA_EXTRACTION = "metadata_extraction"  # Rich metadata
    OCR = "ocr"  # Optical character recognition
    ASYNC_PROCESSING = "async_processing"  # Asynchronous processing
    RATE_LIMITED = "rate_limited"  # Has rate limiting
    PAGINATION = "pagination"  # Supports paginated loading
    TEXT_EXTRACTION = "text_extraction"  # Extract text from files
    WEB_SCRAPING = "web_scraping"  # Web scraping capability
    AUTHENTICATION = "authentication"  # Requires authentication
    REAL_TIME = "real_time"  # Real-time data loading
    BATCH_PROCESSING = "batch_processing"  # Batch processing
    MULTILINGUAL = "multilingual"  # Multi-language support
    STRUCTURED_DATA = "structured_data"  # Structured data parsing
    UNSTRUCTURED_DATA = "unstructured_data"  # Unstructured data parsing
    SEARCH = "search"  # Search capability
    QUERY = "query"  # Query support
    QUERY_BASED = "query_based"  # Query-based loading
    CLOUD_NATIVE = "cloud_native"  # Cloud-native integration
    ENCRYPTION_SUPPORT = "encryption_support"  # Encryption support
    TIME_TRAVEL = "time_travel"  # Time travel/versioning support
    FEDERATION = "federation"  # Federation support
    DELTA_SUPPORT = "delta_support"  # Delta table support
    PARTITIONED_DATA = "partitioned_data"  # Partitioned data support
    THREADING = "threading"  # Threading/conversation support
    FILE_ATTACHMENTS = "file_attachments"  # File attachment support
    LEGAL_CITATIONS = "legal_citations"  # Legal citation parsing
    CASE_LAW = "case_law"  # Case law processing
    FULL_TEXT_SEARCH = "full_text_search"  # Full text search capability
    HEALTHCARE_STANDARDS = "healthcare_standards"  # Healthcare data standards
    PATIENT_DATA = "patient_data"  # Patient data handling
    MEDICAL_IMAGING = "medical_imaging"  # Medical imaging support
    ALERTING = "alerting"  # Alerting capabilities
    ANALYTICS = "analytics"  # Analytics data
    APPS_INTEGRATION = "apps_integration"  # Apps integration
    ASSIGNMENTS = "assignments"  # Assignment data
    ATTACHMENTS = "attachments"  # File attachments
    AUTOMATION_LOGS = "automation_logs"  # Automation logs
    BLOCKCHAIN_DATA = "blockchain_data"  # Blockchain data
    CHANNEL_MESSAGES = "channel_messages"  # Channel messages
    CHAT_LOGS = "chat_logs"  # Chat logs
    CHINESE_CONTENT = "chinese_content"  # Chinese content support
    COLLABORATION_DATA = "collaboration_data"  # Collaboration data
    COLLABORATIVE_EDITING = "collaborative_editing"  # Collaborative editing
    COMMENTS = "comments"  # Comments support
    S3_COMPATIBLE = "s3_compatible"  # S3 compatible storage
    VISUALIZATION = "visualization"  # Data visualization
    TIMESERIES_DATA = "timeseries_data"  # Time series data
    RUSSIAN_CONTENT = "russian_content"  # Russian content support
    REGIONAL_SPECIFIC = "regional_specific"  # Region-specific features
    SEARCH_RESULTS = "search_results"  # Search results processing
    COURSE_CONTENT = "course_content"  # Course content
    DISCUSSIONS = "discussions"  # Discussion forums
    GRADEBOOK = "gradebook"  # Gradebook data
    FORUMS = "forums"  # Forum discussions
    RESOURCES = "resources"  # Learning resources
    SENSOR_DATA = "sensor_data"  # IoT sensor data
    TELEMETRY = "telemetry"  # Telemetry data
    RSS_FEEDS = "rss_feeds"  # RSS feed parsing
    XML_PARSING = "xml_parsing"  # XML parsing
    GEOSPATIAL_DATA = "geospatial_data"  # Geospatial data
    VECTOR_DATA = "vector_data"  # Vector data
    COORDINATE_SYSTEMS = "coordinate_systems"  # Coordinate systems
    SMART_CONTRACTS = "smart_contracts"  # Smart contracts
    TRANSACTION_HISTORY = "transaction_history"  # Transaction history
    WORKFLOW = "workflow"  # Workflow data
    MONITORING = "monitoring"  # System monitoring
    QR_CODE_AUTH = "qr_code_auth"  # QR code authentication
    MEDIA_CONTENT = "media_content"  # Media content handling
    SCHEMA_EVOLUTION = "schema_evolution"  # Schema evolution support
    CONTACT_SYNC = "contact_sync"  # Contact synchronization
    WEBHOOK_INTEGRATION = "webhook_integration"  # Webhook integration
    RICH_MESSAGING = "rich_messaging"  # Rich messaging support
    STICKERS = "stickers"  # Sticker support
    MEETING_RECORDING = "meeting_recording"  # Meeting recording support
    MEETING_RECORDINGS = "meeting_recordings"  # Meeting recordings support
    TRANSCRIPTS = "transcripts"  # Transcript support


class SourceCapabilities(BaseModel):
    """Capabilities and characteristics of a source type."""

    is_bulk_loader: bool = False
    supports_recursive: bool = False
    supports_streaming: bool = False
    supports_incremental: bool = False
    supports_filtering: bool = False
    has_rich_metadata: bool = False
    requires_credentials: bool = False
    credential_type: CredentialType = CredentialType.NONE
    rate_limited: bool = False
    capabilities: set[LoaderCapability] = Field(default_factory=set)

    # Processing characteristics
    typical_speed: str = "medium"  # fast, medium, slow
    typical_quality: str = "medium"  # low, medium, high
    memory_usage: str = "medium"  # low, medium, high

    # Supported formats/patterns
    file_extensions: set[str] = Field(default_factory=set)
    url_patterns: set[str] = Field(default_factory=set)
    mime_types: set[str] = Field(default_factory=set)


# =============================================================================
# Enhanced Base Source Classes
# =============================================================================


class BaseSource(BaseModel, ABC):
    """Enhanced base class for all document sources with comprehensive typing."""

    source_type: str
    source_id: str
    category: SourceCategory
    capabilities: SourceCapabilities

    # Common fields
    name: str | None = None
    description: str | None = None
    tags: set[str] = Field(default_factory=set)
    preferred_loader: str | None = None

    # Processing options
    chunk_size: int | None = None
    chunk_overlap: int | None = None
    encoding: str = "utf-8"

    class Config:
        use_enum_values = True

    @abstractmethod
    def get_loader_kwargs(self) -> dict[str, Any]:
        """Get kwargs for creating the actual loader."""

    def add_capability(self, capability: LoaderCapability) -> None:
        """Add a capability to this source."""
        self.capabilities.capabilities.add(capability)

    def has_capability(self, capability: LoaderCapability) -> bool:
        """Check if source has a specific capability."""
        return capability in self.capabilities.capabilities


class LocalFileSource(BaseSource):
    """Base for local file-based sources."""

    file_path: str | Path
    file_size: int | None = None
    file_modified: str | None = None

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {"file_path": str(self.file_path), "encoding": self.encoding}
        if self.chunk_size:
            kwargs["chunk_size"] = self.chunk_size
        return kwargs


class RemoteSource(BaseSource, SecureConfigMixin):
    """Base for remote sources requiring authentication."""

    url: str
    headers: dict[str, str] = Field(default_factory=dict)
    timeout: int = 30
    retry_count: int = 3

    # Required for SecureConfigMixin
    provider: str = Field(default="generic", description="API provider name")
    api_key: SecretStr | None = Field(None, description="API key for authentication")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {"url": self.url, "headers": self.headers, "timeout": self.timeout}
        # Add authentication if available
        auth_headers = self.get_auth_headers()
        if auth_headers:
            kwargs["headers"].update(auth_headers)
        return kwargs

    def get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers if credentials are available."""
        if hasattr(self, "api_key") and self.api_key:
            return {"Authorization": f"Bearer {self.api_key.get_secret_value()}"}
        return {}


class DatabaseSource(BaseSource, SecureConfigMixin):
    """Base for database sources."""

    connection_string: str | None = None
    database_name: str | None = None
    table_name: str | None = None
    query: str | None = None

    # Required for SecureConfigMixin
    provider: str = Field(default="database", description="Database provider")
    api_key: SecretStr | None = Field(None, description="Not used for databases")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {}
        if self.connection_string:
            kwargs["connection_string"] = self.connection_string
        if self.database_name:
            kwargs["database"] = self.database_name
        if self.table_name:
            kwargs["table"] = self.table_name
        if self.query:
            kwargs["query"] = self.query
        return kwargs


class CloudStorageSource(BaseSource, SecureConfigMixin):
    """Base for cloud storage sources."""

    bucket_name: str
    object_key: str
    provider: str  # aws, gcp, azure
    region: str | None = None

    # Required for SecureConfigMixin
    api_key: SecretStr | None = Field(None, description="Cloud storage credentials")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        return {
            "bucket": self.bucket_name,
            "key": self.object_key,
            "region": self.region,
        }


class DirectorySource(BaseSource):
    """Base for directory-based sources with bulk loading."""

    directory_path: str | Path
    glob_pattern: str = "**/*"
    recursive: bool = True
    max_files: int | None = None
    file_filter: str | None = None

    def get_loader_kwargs(self) -> dict[str, Any]:
        return {
            "path": str(self.directory_path),
            "glob": self.glob_pattern,
            "recursive": self.recursive,
            "max_files": self.max_files,
        }


class MessagingSource(BaseSource, SecureConfigMixin):
    """Base for messaging platform sources."""

    platform: str
    channel_id: str | None = None
    user_id: str | None = None
    date_from: str | None = None
    date_to: str | None = None

    # Required for SecureConfigMixin
    provider: str = Field(
        default="messaging", description="Messaging platform provider"
    )
    api_key: SecretStr | None = Field(None, description="Platform API key")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {"platform": self.platform}
        if self.channel_id:
            kwargs["channel_id"] = self.channel_id
        if self.user_id:
            kwargs["user_id"] = self.user_id
        if self.date_from:
            kwargs["date_from"] = self.date_from
        if self.date_to:
            kwargs["date_to"] = self.date_to
        return kwargs


class BusinessSource(BaseSource, SecureConfigMixin):
    """Base for business system sources (CRM, productivity tools)."""

    platform: str
    workspace_id: str | None = None
    object_type: str | None = None  # contacts, deals, etc.

    # Required for SecureConfigMixin
    provider: str = Field(default="business", description="Business platform provider")
    api_key: SecretStr | None = Field(None, description="Business platform API key")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {"platform": self.platform}
        if self.workspace_id:
            kwargs["workspace_id"] = self.workspace_id
        if self.object_type:
            kwargs["object_type"] = self.object_type
        return kwargs


class AcademicSource(BaseSource):
    """Base for academic and research sources."""

    query: str
    max_results: int = 10
    sort_by: str = "relevance"
    date_filter: str | None = None

    def get_loader_kwargs(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "max_results": self.max_results,
            "sort_by": self.sort_by,
            "date_filter": self.date_filter,
        }


class MediaSource(BaseSource, SecureConfigMixin):
    """Base for media platform sources (video, audio)."""

    platform: str
    content_id: str | None = None
    channel_id: str | None = None
    quality: str = "best"
    format_preference: str = "mp4"

    # Required for SecureConfigMixin
    provider: str = Field(default="media", description="Media platform provider")
    api_key: SecretStr | None = Field(None, description="Media platform API key")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = {
            "platform": self.platform,
            "quality": self.quality,
            "format": self.format_preference,
        }
        if self.content_id:
            kwargs["video_id"] = self.content_id
        if self.channel_id:
            kwargs["channel_id"] = self.channel_id
        return kwargs


class KnowledgeSource(BaseSource, SecureConfigMixin):
    """Base for knowledge management sources."""

    platform: str
    workspace_id: str | None = None
    page_id: str | None = None
    export_format: str = "markdown"
    include_metadata: bool = True

    # Required for SecureConfigMixin
    provider: str = Field(
        default="knowledge", description="Knowledge platform provider"
    )
    api_key: SecretStr | None = Field(None, description="Knowledge platform API key")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        return {
            "platform": self.platform,
            "workspace_id": self.workspace_id,
            "page_id": self.page_id,
            "format": self.export_format,
            "include_metadata": self.include_metadata,
        }


class DevelopmentSource(BaseSource, SecureConfigMixin):
    """Base for development and version control sources."""

    repository_url: str
    branch: str = "main"
    file_pattern: str = "**/*"
    include_history: bool = False

    # Required for SecureConfigMixin
    provider: str = Field(
        default="development", description="Development platform provider"
    )
    api_key: SecretStr | None = Field(None, description="Development platform API key")

    class Config:
        arbitrary_types_allowed = True

    def get_loader_kwargs(self) -> dict[str, Any]:
        return {
            "repo_url": self.repository_url,
            "branch": self.branch,
            "file_pattern": self.file_pattern,
            "include_history": self.include_history,
        }


# =============================================================================
# Specialized Source Types
# =============================================================================


class PDFSource(LocalFileSource):
    """PDF document source with multiple processing options."""

    category: SourceCategory = SourceCategory.FILE_DOCUMENT
    ocr_enabled: bool = False
    extract_images: bool = False
    layout_analysis: bool = False

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "ocr": self.ocr_enabled,
                "extract_images": self.extract_images,
                "layout_analysis": self.layout_analysis,
            }
        )
        return kwargs


class WebScrapingSource(RemoteSource):
    """Web scraping source with browser automation."""

    category: SourceCategory = SourceCategory.WEB_SCRAPING
    use_browser: bool = False
    wait_for_js: bool = False
    scroll_to_bottom: bool = False
    selector: str | None = None

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "use_browser": self.use_browser,
                "wait_for_js": self.wait_for_js,
                "scroll": self.scroll_to_bottom,
                "selector": self.selector,
            }
        )
        return kwargs


class DatabaseQuerySource(DatabaseSource):
    """Database source with custom query support."""

    category: SourceCategory = SourceCategory.DATABASE_SQL
    page_size: int = 1000
    streaming: bool = False

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update({"page_size": self.page_size, "streaming": self.streaming})
        return kwargs


class BulkDirectorySource(DirectorySource):
    """Directory source optimized for bulk loading."""

    category: SourceCategory = SourceCategory.DIRECTORY_LOCAL
    parallel_processing: bool = True
    worker_count: int = 4
    progress_callback: str | None = None

    def get_loader_kwargs(self) -> dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "parallel": self.parallel_processing,
                "workers": self.worker_count,
                "progress": self.progress_callback,
            }
        )
        return kwargs
