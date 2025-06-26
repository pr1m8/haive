"""Source Type System for Haive Document Loaders

This module implements the source type system that forms the bridge between
path analysis and document loaders. It provides base classes for different
source types and the registration mechanism.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
import inspect
import json
import logging
import os
from pathlib import Path
import re
from typing import (
    Any,
    Literal,
    Protocol,
)
from urllib.parse import urlparse

from pydantic import (
    BaseModel,
    Field,
    FilePath,
    HttpUrl,
)


# Import from path analysis module (commented out for now)
# from path_analysis import (
#     PathAnalysisResult,
#     PathType,
#     FileCategory,
#     DatabaseType,
#     CloudProvider
# )


logger = logging.getLogger(__name__)


# ============================================================================
# TYPE DEFINITIONS
# ============================================================================


# Temporary type definitions until we import from path_analysis
class PathType(str, Enum):
    """Primary path type classification."""

    LOCAL_FILE = "local_file"
    LOCAL_DIRECTORY = "local_directory"
    LOCAL_SYMLINK = "local_symlink"
    LOCAL_NONEXISTENT = "local_nonexistent"
    URL_HTTP = "url_http"
    URL_HTTPS = "url_https"
    URL_FTP = "url_ftp"
    URL_FILE = "url_file"
    DATABASE_URI = "database_uri"
    CLOUD_STORAGE = "cloud_storage"
    NETWORK_SHARE = "network_share"
    SPECIAL_PATH = "special_path"
    UNKNOWN = "unknown"


class FileCategory(str, Enum):
    """High-level file category."""

    DOCUMENT = "document"
    IMAGE = "image"
    VIDEO = "video"
    AUDIO = "audio"
    CODE = "code"
    DATA = "data"
    ARCHIVE = "archive"
    EXECUTABLE = "executable"
    TEXT = "text"
    FONT = "font"
    MODEL = "model"
    SYSTEM = "system"
    UNKNOWN_FILE = "unknown_file"


class DatabaseType(str, Enum):
    """Database type classification."""

    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
    SQLITE = "sqlite"
    MONGODB = "mongodb"
    REDIS = "redis"
    ORACLE = "oracle"
    MSSQL = "mssql"
    CASSANDRA = "cassandra"
    ELASTICSEARCH = "elasticsearch"
    CLICKHOUSE = "clickhouse"
    SNOWFLAKE = "snowflake"
    BIGQUERY = "bigquery"
    DYNAMODB = "dynamodb"
    COUCHDB = "couchdb"
    INFLUXDB = "influxdb"
    UNKNOWN_DB = "unknown_db"


class CloudProvider(str, Enum):
    """Cloud storage provider classification."""

    AWS_S3 = "aws_s3"
    AZURE_BLOB = "azure_blob"
    GOOGLE_CLOUD = "google_cloud"
    DROPBOX = "dropbox"
    BOX = "box"
    ONEDRIVE = "onedrive"
    ICLOUD = "icloud"
    BACKBLAZE = "backblaze"
    UNKNOWN_CLOUD = "unknown_cloud"


# Mock PathAnalysisResult for development
class PathAnalysisResult(BaseModel):
    """Mock for PathAnalysisResult."""

    original_path: str
    path_type: PathType = PathType.UNKNOWN
    is_local: bool = False
    is_remote: bool = False
    is_file: bool = False
    is_directory: bool = False
    file_extension: str | None = None
    file_category: FileCategory | None = None
    database_type: DatabaseType | None = None
    cloud_provider: CloudProvider | None = None
    url_components: dict[str, Any] | None = None


# ============================================================================
# PATTERN AND STRATEGY DEFINITIONS
# ============================================================================


@dataclass
class SourcePattern:
    """Flexible pattern specification for source matching."""

    # File-based patterns (for LocalSource)
    file_extensions: list[str] = field(default_factory=list)
    file_patterns: list[str] = field(default_factory=list)  # glob patterns
    directory_patterns: list[str] = field(default_factory=list)

    # URL-based patterns (for RemoteSource)
    url_patterns: list[str] = field(default_factory=list)
    domain_patterns: list[str] = field(default_factory=list)
    path_patterns: list[str] = field(default_factory=list)
    scheme_patterns: list[str] = field(default_factory=list)

    # Content-based patterns
    content_types: list[str] = field(default_factory=list)
    file_categories: list[FileCategory] = field(default_factory=list)

    # Database patterns
    database_types: list[DatabaseType] = field(default_factory=list)

    # Cloud patterns
    cloud_providers: list[CloudProvider] = field(default_factory=list)

    # Custom matching
    custom_matcher: Callable | None = None
    priority: int = 0


@dataclass
class LoaderStrategy:
    """Information about a loader strategy."""

    strategy_name: str
    loader_class: str
    loader_module: str = ""

    # Characteristics
    speed: Literal["fast", "medium", "slow"] = "medium"
    quality: Literal["low", "medium", "high"] = "medium"
    resource_usage: Literal["low", "medium", "high"] = "medium"

    # Capabilities
    supports_lazy_load: bool = False
    supports_async: bool = False
    supports_batching: bool = False

    # Conditions
    best_for: list[str] = field(
        default_factory=list
    )  # ["large_files", "tables", "images"]
    requires_auth: bool = False
    requires_network: bool = False

    # Authentication
    required_credentials: list[str] = field(default_factory=list)
    optional_credentials: list[str] = field(default_factory=list)

    # Performance hints
    max_file_size: int | None = None
    estimated_time_per_mb: float = 0.1  # seconds per MB

    def calculate_suitability(
        self, analysis_result: PathAnalysisResult, criteria: dict[str, Any]
    ) -> float:
        """Calculate suitability score for this strategy."""
        score = 0.5  # Base score

        # File size considerations
        if (
            hasattr(analysis_result, "file_size")
            and self.max_file_size
            and analysis_result.file_size
        ):
            if analysis_result.file_size > self.max_file_size:
                score -= 0.3
            elif analysis_result.file_size < self.max_file_size / 2:
                score += 0.1

        # Speed preference
        if criteria.get("prefer_speed", False):
            if self.speed == "fast":
                score += 0.2
            elif self.speed == "slow":
                score -= 0.2

        # Quality preference
        if criteria.get("prefer_quality", False):
            if self.quality == "high":
                score += 0.2
            elif self.quality == "low":
                score -= 0.2

        # Check best_for conditions
        if analysis_result.file_category:
            file_category = str(analysis_result.file_category).lower()
            if any(condition in file_category for condition in self.best_for):
                score += 0.3

        return max(0.0, min(1.0, score))

    def check_authentication(self, credential_manager: Any) -> bool:
        """Check if all required credentials are available."""
        if not self.requires_auth:
            return True

        if not credential_manager:
            return False

        for cred_name in self.required_credentials:
            if not credential_manager.get_credential(cred_name):
                return False
        return True


@dataclass
class SourceMetadata:
    """Complete metadata for a source type."""

    source_type: str
    source_class: str  # Module.ClassName
    category: Literal["local", "remote", "database", "cloud", "special"]

    patterns: list[SourcePattern] = field(default_factory=list)
    loader_strategies: list[LoaderStrategy] = field(default_factory=list)

    # Authentication
    required_credentials: list[str] = field(default_factory=list)
    optional_credentials: list[str] = field(default_factory=list)

    # Auto-detected info
    description: str = ""
    confidence: float = 0.0
    auto_detected: bool = True


# ============================================================================
# CREDENTIAL MANAGEMENT
# ============================================================================


class CredentialProvider(Protocol):
    """Protocol for credential providers."""

    def get_credential(self, credential_name: str) -> dict[str, Any] | None:
        """Get a credential by name."""
        ...

    def store_credential(
        self, credential_name: str, credential: dict[str, Any]
    ) -> bool:
        """Store a credential."""
        ...

    def list_available_credentials(self) -> list[str]:
        """List available credential names."""
        ...


class EnvironmentCredentialProvider:
    """Provides credentials from environment variables."""

    def __init__(
        self, prefix: str = "HAIVE_", env_map: dict[str, str] | None = None
    ):
        self.prefix = prefix
        self.env_map = env_map or {}

    def get_credential(self, credential_name: str) -> dict[str, Any] | None:
        """Get credentials from environment variables."""
        # Check direct environment variable
        env_var = f"{self.prefix}{credential_name.upper()}"
        if env_var in os.environ:
            return {"type": "api_key", "value": os.environ[env_var]}

        # Check mapped variables
        if credential_name in self.env_map:
            mapped_var = self.env_map[credential_name]
            if mapped_var in os.environ:
                return {"type": "api_key", "value": os.environ[mapped_var]}

        # Check JSON-encoded credentials
        json_var = f"{self.prefix}{credential_name.upper()}_JSON"
        if json_var in os.environ:
            try:
                return json.loads(os.environ[json_var])
            except json.JSONDecodeError:
                pass

        return None

    def store_credential(
        self, credential_name: str, credential: dict[str, Any]
    ) -> bool:
        """Store a credential in the environment (not supported)."""
        return False

    def list_available_credentials(self) -> list[str]:
        """List available credential names."""
        credentials = []

        # Check prefixed variables
        for var_name in os.environ:
            if var_name.startswith(self.prefix):
                name = var_name[len(self.prefix) :].lower()
                if name.endswith("_json"):
                    name = name[:-5]  # Remove _json suffix
                credentials.append(name)

        # Check mapped variables
        for cred_name, env_var in self.env_map.items():
            if env_var in os.environ:
                credentials.append(cred_name)

        return credentials


class CredentialManager:
    """Manages credentials from multiple providers."""

    def __init__(self, providers: list[CredentialProvider] | None = None):
        self.providers = providers or []

        # Add default environment provider if none provided
        if not self.providers:
            self.providers.append(EnvironmentCredentialProvider())

    def get_credential(self, credential_name: str) -> dict[str, Any] | None:
        """Get a credential from any provider."""
        for provider in self.providers:
            credential = provider.get_credential(credential_name)
            if credential:
                return credential
        return None

    def store_credential(
        self, credential_name: str, credential: dict[str, Any]
    ) -> bool:
        """Store a credential with the first provider that supports it."""
        for provider in self.providers:
            if provider.store_credential(credential_name, credential):
                return True
        return False

    def list_available_credentials(self) -> list[str]:
        """List all available credential names from all providers."""
        credentials = set()
        for provider in self.providers:
            credentials.update(provider.list_available_credentials())
        return list(credentials)


# ============================================================================
# BASE SOURCE CLASSES
# ============================================================================


class BaseSource(BaseModel):
    """Root base class for all sources."""

    # Auto-populated by registry
    source_type: str | None = None
    confidence_score: float = 0.0

    # Metadata
    description: str | None = None
    tags: list[str] = Field(default_factory=list)

    # Authentication state
    is_authenticated: bool = False
    credential_manager: Any | None = None  # CredentialManager

    class Config:
        # Store pattern and loader data at class level
        patterns: list[SourcePattern] = []
        file_extensions: list[str] = []
        url_patterns: list[str] = []
        domain_patterns: list[str] = []
        path_patterns: list[str] = []
        content_types: list[str] = []
        loader_strategies: dict[str, Any] = {}

        # Authentication requirements
        required_credentials: list[str] = []
        optional_credentials: list[str] = []

    @classmethod
    def get_patterns(cls) -> list[SourcePattern]:
        """Get patterns for this source class."""
        patterns = []

        # Get patterns from Config
        if hasattr(cls.Config, "patterns"):
            patterns.extend(cls.Config.patterns)

        # Build pattern from individual attributes
        pattern_data = {}
        for attr in [
            "file_extensions",
            "url_patterns",
            "domain_patterns",
            "path_patterns",
            "content_types",
        ]:
            if hasattr(cls.Config, attr):
                value = getattr(cls.Config, attr)
                if value:
                    pattern_data[attr] = value

        if pattern_data:
            patterns.append(SourcePattern(**pattern_data))

        return patterns

    @classmethod
    def get_loader_strategies(cls) -> list[LoaderStrategy]:
        """Get loader strategies for this source class."""
        strategies = []

        if hasattr(cls.Config, "loader_strategies"):
            loader_strategies = cls.Config.loader_strategies
            if isinstance(loader_strategies, dict):
                for name, config in loader_strategies.items():
                    if isinstance(config, str):
                        # Simple string format
                        strategies.append(
                            LoaderStrategy(strategy_name=name, loader_class=config)
                        )
                    elif isinstance(config, dict):
                        # Detailed config
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=name,
                                loader_class=config.get("class", ""),
                                speed=config.get("speed", "medium"),
                                quality=config.get("quality", "medium"),
                                best_for=config.get("best_for", []),
                                **{
                                    k: v
                                    for k, v in config.items()
                                    if k
                                    not in ["class", "speed", "quality", "best_for"]
                                },
                            )
                        )

        return strategies

    def authenticate(self, credential_manager: Any | None = None) -> bool:
        """Authenticate the source with credentials."""
        self.credential_manager = credential_manager

        # If no credentials required, consider authenticated
        required_credentials = getattr(self.Config, "required_credentials", [])
        if not required_credentials:
            self.is_authenticated = True
            return True

        # If no credential manager, authentication fails
        if not credential_manager:
            self.is_authenticated = False
            return False

        # Check all required credentials
        for cred_name in required_credentials:
            credential = credential_manager.get_credential(cred_name)
            if not credential:
                self.is_authenticated = False
                return False

        # Authentication successful
        self.is_authenticated = True
        return True

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader instance with the specified strategy."""
        # This is a placeholder - will be implemented in subclasses
        raise NotImplementedError("Subclasses must implement create_loader")


class LocalSource(BaseSource):
    """Base for local filesystem sources."""

    # Path information
    file_path: FilePath | None = None
    directory_path: Path | None = None

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader for a local file source."""
        # Will be implemented with actual LangChain loader creation
        strategies = self.get_loader_strategies()

        # Find the requested strategy or use the first one
        strategy = next(
            (s for s in strategies if s.strategy_name == strategy_name),
            strategies[0] if strategies else None,
        )

        if not strategy:
            raise ValueError(f"No loader strategy found for {self.source_type}")

        # Placeholder - will be replaced with actual loader creation
        return {
            "strategy": strategy.strategy_name,
            "loader_class": strategy.loader_class,
            "file_path": str(self.file_path) if self.file_path else None,
            "directory_path": str(self.directory_path) if self.directory_path else None,
        }


class RemoteSource(BaseSource):
    """Base for remote/URL sources."""

    # URL information
    url: HttpUrl | None = None

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader for a remote source."""
        # Will be implemented with actual LangChain loader creation
        strategies = self.get_loader_strategies()

        # Find the requested strategy or use the first one
        strategy = next(
            (s for s in strategies if s.strategy_name == strategy_name),
            strategies[0] if strategies else None,
        )

        if not strategy:
            raise ValueError(f"No loader strategy found for {self.source_type}")

        # Placeholder - will be replaced with actual loader creation
        return {
            "strategy": strategy.strategy_name,
            "loader_class": strategy.loader_class,
            "url": str(self.url) if self.url else None,
        }


class DatabaseSource(RemoteSource):
    """Base for database sources."""

    # Database information
    connection_string: str | None = None
    database_name: str | None = None
    table_name: str | None = None
    query: str | None = None

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader for a database source."""
        # Will be implemented with actual LangChain loader creation
        strategies = self.get_loader_strategies()

        # Find the requested strategy or use the first one
        strategy = next(
            (s for s in strategies if s.strategy_name == strategy_name),
            strategies[0] if strategies else None,
        )

        if not strategy:
            raise ValueError(f"No loader strategy found for {self.source_type}")

        # Placeholder - will be replaced with actual loader creation
        return {
            "strategy": strategy.strategy_name,
            "loader_class": strategy.loader_class,
            "connection_string": self.connection_string,
            "database_name": self.database_name,
            "table_name": self.table_name,
            "query": self.query,
        }


class CloudSource(RemoteSource):
    """Base for cloud storage sources."""

    # Cloud information
    bucket_name: str | None = None
    object_key: str | None = None

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a loader for a cloud storage source."""
        # Will be implemented with actual LangChain loader creation
        strategies = self.get_loader_strategies()

        # Find the requested strategy or use the first one
        strategy = next(
            (s for s in strategies if s.strategy_name == strategy_name),
            strategies[0] if strategies else None,
        )

        if not strategy:
            raise ValueError(f"No loader strategy found for {self.source_type}")

        # Placeholder - will be replaced with actual loader creation
        return {
            "strategy": strategy.strategy_name,
            "loader_class": strategy.loader_class,
            "bucket_name": self.bucket_name,
            "object_key": self.object_key,
        }


# ============================================================================
# PATTERN DETECTION AND INFERENCE
# ============================================================================


class PatternDetector:
    """Automatically detects patterns from class definitions."""

    # Domain mappings for class names
    NAME_TO_DOMAIN = {
        "github": ["github.com"],
        "gitlab": ["gitlab.com"],
        "bitbucket": ["bitbucket.org"],
        "youtube": ["youtube.com", "youtu.be"],
        "huggingface": ["huggingface.co"],
        "kaggle": ["kaggle.com"],
        "dropbox": ["dropbox.com"],
        "notion": ["notion.so"],
        "confluence": ["atlassian.net", "confluence.com"],
        "slack": ["slack.com"],
        "google": ["docs.google.com", "drive.google.com"],
        "wikipedia": ["wikipedia.org"],
        "arxiv": ["arxiv.org"],
        "reddit": ["reddit.com"],
        "twitter": ["twitter.com", "x.com"],
        "linkedin": ["linkedin.com"],
    }

    @classmethod
    def auto_detect_patterns(
        cls, source_class: type[BaseSource]
    ) -> list[SourcePattern]:
        """Auto-detect patterns from class definition."""
        patterns = []

        # Get patterns from class
        patterns.extend(source_class.get_patterns())

        # Infer from class name
        patterns.extend(cls._extract_from_name(source_class.__name__))

        # Infer from fields
        if hasattr(source_class, "model_fields"):
            patterns.extend(cls._extract_from_fields(source_class.model_fields))

        # Infer from inheritance
        patterns.extend(cls._extract_from_inheritance(source_class.__mro__))

        # Infer from docstring
        if source_class.__doc__:
            patterns.extend(cls._extract_from_docstring(source_class.__doc__))

        return patterns

    @classmethod
    def _extract_from_name(cls, class_name: str) -> list[SourcePattern]:
        """Extract patterns from class name."""
        patterns = []
        name_lower = class_name.lower()

        # Check for known services
        for service, domains in cls.NAME_TO_DOMAIN.items():
            if service in name_lower:
                patterns.append(SourcePattern(domain_patterns=domains, priority=10))
                break

        # Extract file extensions from name
        if "pdf" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".pdf"]))
        elif "csv" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".csv"]))
        elif "json" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".json"]))
        elif "xml" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".xml"]))
        elif "markdown" in name_lower or "md" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".md", ".markdown"]))
        elif "text" in name_lower or "txt" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".txt", ".text"]))
        elif "html" in name_lower or "htm" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".html", ".htm"]))
        elif "docx" in name_lower or "word" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".docx", ".doc"]))
        elif "excel" in name_lower or "xlsx" in name_lower:
            patterns.append(SourcePattern(file_extensions=[".xlsx", ".xls"]))

        return patterns

    @classmethod
    def _extract_from_fields(cls, fields: dict[str, Any]) -> list[SourcePattern]:
        """Extract patterns from field types and names."""
        patterns = []

        for field_name, field_info in fields.items():
            field_name_lower = field_name.lower()

            # URL fields
            if hasattr(field_info, "annotation"):
                if (
                    str(field_info.annotation) == "HttpUrl"
                    or "url" in str(field_info.annotation).lower()
                ):
                    # Infer domain from field name
                    for service, domains in cls.NAME_TO_DOMAIN.items():
                        if service in field_name_lower:
                            patterns.append(SourcePattern(domain_patterns=domains))

            # File path fields
            if hasattr(field_info, "annotation"):
                if (
                    str(field_info.annotation) == "FilePath"
                    or "path" in field_name_lower
                ):
                    # Infer file type from field name
                    if "pdf" in field_name_lower:
                        patterns.append(SourcePattern(file_extensions=[".pdf"]))
                    elif "csv" in field_name_lower:
                        patterns.append(SourcePattern(file_extensions=[".csv"]))
                    elif "json" in field_name_lower:
                        patterns.append(SourcePattern(file_extensions=[".json"]))
                    elif "text" in field_name_lower or "txt" in field_name_lower:
                        patterns.append(SourcePattern(file_extensions=[".txt"]))

        return patterns

    @classmethod
    def _extract_from_inheritance(cls, mro: tuple[type, ...]) -> list[SourcePattern]:
        """Extract patterns from inheritance chain."""
        patterns = []

        for base_class in mro:
            if base_class.__name__ == "LocalSource":
                patterns.append(SourcePattern(scheme_patterns=["file", ""]))
            elif base_class.__name__ == "RemoteSource":
                patterns.append(SourcePattern(scheme_patterns=["http", "https"]))
            elif base_class.__name__ == "DatabaseSource":
                patterns.append(
                    SourcePattern(
                        scheme_patterns=[
                            "postgresql",
                            "mysql",
                            "sqlite",
                            "mongodb",
                            "redis",
                        ]
                    )
                )
            elif base_class.__name__ == "CloudSource":
                patterns.append(SourcePattern(scheme_patterns=["s3", "gs", "azure"]))

        return patterns

    @classmethod
    def _extract_from_docstring(cls, docstring: str) -> list[SourcePattern]:
        """Extract patterns from docstring."""
        patterns = []
        if not docstring:
            return patterns

        doc_lower = docstring.lower()

        # Look for domain mentions
        for service, domains in cls.NAME_TO_DOMAIN.items():
            if service in doc_lower:
                patterns.append(SourcePattern(domain_patterns=domains))

        # Look for file extensions
        extensions = [".pdf", ".csv", ".json", ".txt", ".html", ".docx", ".xlsx"]
        for ext in extensions:
            if ext in doc_lower:
                patterns.append(SourcePattern(file_extensions=[ext]))

        return patterns


# ============================================================================
# LOADER DETECTION
# ============================================================================


class LoaderDetector:
    """Automatically detects compatible loaders."""

    # Known loader mappings
    LOADER_MAPPINGS = {
        "local": {
            "file_extensions": {
                # Documents
                ".pdf": [
                    ("PyPDFLoader", "fast", "medium"),
                    ("UnstructuredPDFLoader", "medium", "high"),
                    ("PDFPlumberLoader", "slow", "high"),
                ],
                ".doc": [("UnstructuredWordDocumentLoader", "medium", "high")],
                ".docx": [
                    ("UnstructuredWordDocumentLoader", "medium", "high"),
                    ("Docx2txtLoader", "fast", "low"),
                ],
                ".xlsx": [
                    ("UnstructuredExcelLoader", "medium", "high"),
                    ("PandasExcelLoader", "fast", "medium"),
                ],
                ".xls": [("UnstructuredExcelLoader", "medium", "high")],
                ".csv": [
                    ("CSVLoader", "fast", "medium"),
                    ("UnstructuredCSVLoader", "medium", "high"),
                ],
                ".json": [
                    ("JSONLoader", "fast", "high"),
                    ("UnstructuredJSONLoader", "medium", "high"),
                ],
                ".txt": [
                    ("TextLoader", "fast", "medium"),
                    ("UnstructuredFileLoader", "medium", "high"),
                ],
                ".md": [
                    ("UnstructuredMarkdownLoader", "fast", "high"),
                    ("TextLoader", "fast", "medium"),
                ],
                ".html": [
                    ("BSHTMLLoader", "fast", "medium"),
                    ("UnstructuredHTMLLoader", "medium", "high"),
                ],
                ".xml": [("UnstructuredXMLLoader", "medium", "high")],
                ".rst": [("UnstructuredRSTLoader", "medium", "high")],
                ".rtf": [("UnstructuredRTFLoader", "medium", "high")],
                ".epub": [("UnstructuredEPubLoader", "medium", "high")],
                ".pptx": [("UnstructuredPowerPointLoader", "medium", "high")],
                ".jpg": [("UnstructuredImageLoader", "slow", "medium")],
                ".png": [("UnstructuredImageLoader", "slow", "medium")],
                ".jpeg": [("UnstructuredImageLoader", "slow", "medium")],
                ".py": [("PythonLoader", "fast", "high")],
                ".ipynb": [("NotebookLoader", "fast", "high")],
            },
            "directories": [
                ("DirectoryLoader", "fast", "medium"),
                ("PyPDFDirectoryLoader", "fast", "medium"),
                ("NotionDirectoryLoader", "medium", "high"),
                ("ObsidianLoader", "medium", "high"),
            ],
        },
        "remote": {
            "domains": {
                "github.com": [
                    ("GitHubIssuesLoader", "medium", "high"),
                    ("GitHubFileLoader", "medium", "high"),
                ],
                "youtube.com": [
                    ("YoutubeLoader", "medium", "high"),
                    ("YoutubeAudioLoader", "medium", "medium"),
                ],
                "youtu.be": [
                    ("YoutubeLoader", "medium", "high"),
                    ("YoutubeAudioLoader", "medium", "medium"),
                ],
                "arxiv.org": [("ArxivLoader", "medium", "high")],
                "wikipedia.org": [("WikipediaLoader", "fast", "high")],
                "reddit.com": [("RedditPostsLoader", "medium", "medium")],
                "twitter.com": [("TwitterTweetLoader", "medium", "medium")],
                "notion.so": [("NotionDBLoader", "medium", "high")],
                "airtable.com": [("AirtableLoader", "medium", "high")],
            },
            "general": [
                ("WebBaseLoader", "fast", "medium"),
                ("PlaywrightURLLoader", "slow", "high"),
                ("SeleniumURLLoader", "slow", "medium"),
                ("RecursiveUrlLoader", "slow", "high"),
            ],
        },
        "database": {
            "postgresql": [("SQLDatabaseLoader", "medium", "high")],
            "postgres": [("SQLDatabaseLoader", "medium", "high")],
            "mysql": [("SQLDatabaseLoader", "medium", "high")],
            "sqlite": [("SQLDatabaseLoader", "fast", "high")],
            "mongodb": [("MongodbLoader", "medium", "high")],
            "snowflake": [("SnowflakeLoader", "medium", "high")],
            "bigquery": [("BigQueryLoader", "slow", "high")],
        },
        "cloud": {
            "s3": [
                ("S3FileLoader", "medium", "high"),
                ("S3DirectoryLoader", "slow", "high"),
            ],
            "gs": [
                ("GCSFileLoader", "medium", "high"),
                ("GCSDirectoryLoader", "slow", "high"),
            ],
            "azure": [
                ("AzureBlobStorageContainerLoader", "medium", "high"),
                ("AzureBlobStorageFileLoader", "fast", "high"),
            ],
            "dropbox": [("DropboxLoader", "medium", "high")],
            "onedrive": [
                ("OneDriveLoader", "medium", "high"),
                ("OneDriveFileLoader", "fast", "high"),
            ],
            "gdrive": [("GoogleDriveLoader", "medium", "high")],
        },
    }

    @classmethod
    def detect_loaders(
        cls, source_class: type[BaseSource], patterns: list[SourcePattern]
    ) -> list[LoaderStrategy]:
        """Detect compatible loaders for a source class."""
        strategies = []

        # Get explicit strategies from class
        strategies.extend(source_class.get_loader_strategies())

        # Auto-detect based on patterns and inheritance
        category = cls._determine_category(source_class)

        if category == "local":
            strategies.extend(cls._detect_local_loaders(patterns))
        elif category == "remote":
            strategies.extend(cls._detect_remote_loaders(patterns))
        elif category == "database":
            strategies.extend(cls._detect_database_loaders(patterns))
        elif category == "cloud":
            strategies.extend(cls._detect_cloud_loaders(patterns))

        return strategies

    @classmethod
    def _determine_category(cls, source_class: type[BaseSource]) -> str:
        """Determine source category from inheritance."""
        if "CloudSource" in [c.__name__ for c in source_class.__mro__]:
            return "cloud"
        if "DatabaseSource" in [c.__name__ for c in source_class.__mro__]:
            return "database"
        if "LocalSource" in [c.__name__ for c in source_class.__mro__]:
            return "local"
        if "RemoteSource" in [c.__name__ for c in source_class.__mro__]:
            return "remote"
        return "unknown"

    @classmethod
    def _detect_local_loaders(
        cls, patterns: list[SourcePattern]
    ) -> list[LoaderStrategy]:
        """Detect loaders for local sources."""
        strategies = []
        mappings = cls.LOADER_MAPPINGS["local"]

        for pattern in patterns:
            # File extension based
            for ext in pattern.file_extensions:
                if ext in mappings["file_extensions"]:
                    for loader_name, speed, quality in mappings["file_extensions"][ext]:
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=f"{ext.lstrip('.')}_loader",
                                loader_class=loader_name,
                                loader_module="langchain_community.document_loaders",
                                speed=speed,
                                quality=quality,
                                best_for=[ext.lstrip(".")],
                            )
                        )

            # Directory based
            if pattern.directory_patterns:
                for loader_name, speed, quality in mappings["directories"]:
                    strategies.append(
                        LoaderStrategy(
                            strategy_name=f"directory_{loader_name.lower()}",
                            loader_class=loader_name,
                            loader_module="langchain_community.document_loaders",
                            speed=speed,
                            quality=quality,
                            best_for=["directory"],
                        )
                    )

        return strategies

    @classmethod
    def _detect_remote_loaders(
        cls, patterns: list[SourcePattern]
    ) -> list[LoaderStrategy]:
        """Detect loaders for remote sources."""
        strategies = []
        mappings = cls.LOADER_MAPPINGS["remote"]

        for pattern in patterns:
            # Domain-specific loaders
            for domain in pattern.domain_patterns:
                if domain in mappings["domains"]:
                    for loader_name, speed, quality in mappings["domains"][domain]:
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=f"{domain.replace('.', '_')}_loader",
                                loader_class=loader_name,
                                loader_module="langchain_community.document_loaders",
                                speed=speed,
                                quality=quality,
                                best_for=[domain],
                                requires_network=True,
                            )
                        )

        # Add general web loaders
        for loader_name, speed, quality in mappings["general"]:
            strategies.append(
                LoaderStrategy(
                    strategy_name=f"general_{loader_name.lower()}",
                    loader_class=loader_name,
                    loader_module="langchain_community.document_loaders",
                    speed=speed,
                    quality=quality,
                    best_for=["web", "html"],
                    requires_network=True,
                )
            )

        return strategies

    @classmethod
    def _detect_database_loaders(
        cls, patterns: list[SourcePattern]
    ) -> list[LoaderStrategy]:
        """Detect loaders for database sources."""
        strategies = []
        mappings = cls.LOADER_MAPPINGS["database"]

        for pattern in patterns:
            for scheme in pattern.scheme_patterns:
                if scheme in mappings:
                    for loader_name, speed, quality in mappings[scheme]:
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=f"{scheme}_loader",
                                loader_class=loader_name,
                                loader_module="langchain_community.document_loaders",
                                speed=speed,
                                quality=quality,
                                best_for=[scheme],
                                requires_auth=True,
                                required_credentials=[f"{scheme}_credentials"],
                            )
                        )

        return strategies

    @classmethod
    def _detect_cloud_loaders(
        cls, patterns: list[SourcePattern]
    ) -> list[LoaderStrategy]:
        """Detect loaders for cloud sources."""
        strategies = []
        mappings = cls.LOADER_MAPPINGS["cloud"]

        for pattern in patterns:
            for scheme in pattern.scheme_patterns:
                if scheme in mappings:
                    for loader_name, speed, quality in mappings[scheme]:
                        strategies.append(
                            LoaderStrategy(
                                strategy_name=f"{scheme}_loader",
                                loader_class=loader_name,
                                loader_module="langchain_community.document_loaders",
                                speed=speed,
                                quality=quality,
                                best_for=[scheme],
                                requires_auth=True,
                                required_credentials=[f"{scheme}_credentials"],
                            )
                        )

        return strategies


# ============================================================================
# DYNAMIC SOURCE REGISTRY
# ============================================================================


class DynamicSourceRegistry:
    """Central registry for all source types with dynamic discovery."""

    def __init__(self):
        self.source_classes: dict[str, type[BaseSource]] = {}
        self.source_metadata: dict[str, SourceMetadata] = {}
        self.pattern_index: dict[str, list[str]] = {}  # pattern -> source_types
        self.loader_index: dict[str, list[str]] = {}  # loader -> source_types

    def register_source(
        self, source_class: type[BaseSource], **kwargs
    ) -> SourceMetadata:
        """Register a source class with auto-detection."""
        # Generate source type name
        source_type = kwargs.get("source_type") or self._generate_source_type(
            source_class.__name__
        )

        # Auto-detect patterns
        patterns = PatternDetector.auto_detect_patterns(source_class)

        # Auto-detect loaders
        loaders = LoaderDetector.detect_loaders(source_class, patterns)

        # Determine category
        category = self._determine_category(source_class)

        # Get credential requirements
        required_credentials = getattr(source_class.Config, "required_credentials", [])
        optional_credentials = getattr(source_class.Config, "optional_credentials", [])

        # Create metadata
        metadata = SourceMetadata(
            source_type=source_type,
            source_class=f"{source_class.__module__}.{source_class.__name__}",
            category=category,
            patterns=patterns,
            loader_strategies=loaders,
            required_credentials=required_credentials,
            optional_credentials=optional_credentials,
            description=source_class.__doc__ or "",
            auto_detected=True,
        )

        # Store in registry
        self.source_classes[source_type] = source_class
        self.source_metadata[source_type] = metadata

        # Update indices
        self._update_indices(source_type, metadata)

        logger.info(
            f"Registered source: {source_type} with {len(patterns)} patterns and {len(loaders)} loaders"
        )

        return metadata

    def find_matching_sources(
        self, analysis_result: PathAnalysisResult
    ) -> list[tuple[str, float]]:
        """Find source types that match the analysis result."""
        matches = []

        for source_type, metadata in self.source_metadata.items():
            score = self._calculate_match_score(analysis_result, metadata)
            if score > 0.1:  # Minimum threshold
                matches.append((source_type, score))

        # Sort by score descending
        matches.sort(key=lambda x: x[1], reverse=True)
        return matches

    def _calculate_match_score(
        self, analysis_result: PathAnalysisResult, metadata: SourceMetadata
    ) -> float:
        """Calculate how well a source matches the analysis result."""
        score = 0.0
        total_patterns = len(metadata.patterns)

        if total_patterns == 0:
            return 0.0

        for pattern in metadata.patterns:
            pattern_score = self._score_pattern_match(analysis_result, pattern)
            score += pattern_score

        # Normalize by number of patterns
        score = score / total_patterns

        # Boost for explicit high-priority patterns
        high_priority_patterns = [p for p in metadata.patterns if p.priority > 5]
        if high_priority_patterns:
            score += 0.2

        return min(1.0, score)

    def _score_pattern_match(
        self, analysis_result: PathAnalysisResult, pattern: SourcePattern
    ) -> float:
        """Score how well a pattern matches the analysis result."""
        score = 0.0
        total_checks = 0

        # File extension matching
        if pattern.file_extensions and analysis_result.file_extension:
            total_checks += 1
            if analysis_result.file_extension in pattern.file_extensions:
                score += 1.0

        # Domain matching
        if (
            pattern.domain_patterns
            and hasattr(analysis_result, "url_components")
            and analysis_result.url_components
        ):
            total_checks += 1
            hostname = analysis_result.url_components.get("hostname", "")
            for domain in pattern.domain_patterns:
                if domain in hostname:
                    score += 1.0
                    break

        # Scheme matching
        if (
            pattern.scheme_patterns
            and hasattr(analysis_result, "url_components")
            and analysis_result.url_components
        ):
            total_checks += 1
            scheme = analysis_result.url_components.get("scheme", "")
            if scheme in pattern.scheme_patterns:
                score += 1.0

        # Path pattern matching
        if (
            pattern.path_patterns
            and hasattr(analysis_result, "url_components")
            and analysis_result.url_components
        ):
            total_checks += 1
            path = analysis_result.url_components.get("path", "")
            for path_pattern in pattern.path_patterns:
                # Simple wildcard matching
                if self._wildcard_match(path, path_pattern):
                    score += 1.0
                    break

        # Database type matching
        if pattern.database_types and analysis_result.database_type:
            total_checks += 1
            if analysis_result.database_type in pattern.database_types:
                score += 1.0

        # Cloud provider matching
        if pattern.cloud_providers and analysis_result.cloud_provider:
            total_checks += 1
            if analysis_result.cloud_provider in pattern.cloud_providers:
                score += 1.0

        # File category matching
        if pattern.file_categories and analysis_result.file_category:
            total_checks += 1
            if analysis_result.file_category in pattern.file_categories:
                score += 0.5  # Lower weight for category

        # Custom matcher
        if pattern.custom_matcher:
            total_checks += 1
            try:
                if pattern.custom_matcher(analysis_result):
                    score += 1.0
            except Exception as e:
                logger.warning(f"Custom matcher failed: {e}")

        # Normalize score
        if total_checks > 0:
            score = score / total_checks
        else:
            score = 0.0

        # Apply priority boost
        if pattern.priority > 0:
            score += pattern.priority * 0.1

        return min(1.0, score)

    def _wildcard_match(self, text: str, pattern: str) -> bool:
        """Simple wildcard matching with * and ?."""
        import fnmatch

        return fnmatch.fnmatch(text, pattern)

    def _generate_source_type(self, class_name: str) -> str:
        """Generate source type from class name."""
        # Convert CamelCase to snake_case
        result = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()
        # Remove common suffixes
        result = result.replace("_source", "").replace("_loader", "")
        return result

    def _determine_category(self, source_class: type[BaseSource]) -> str:
        """Determine category from inheritance."""
        if "CloudSource" in [c.__name__ for c in source_class.__mro__]:
            return "cloud"
        if "DatabaseSource" in [c.__name__ for c in source_class.__mro__]:
            return "database"
        if "LocalSource" in [c.__name__ for c in source_class.__mro__]:
            return "local"
        if "RemoteSource" in [c.__name__ for c in source_class.__mro__]:
            return "remote"
        return "special"

    def _update_indices(self, source_type: str, metadata: SourceMetadata):
        """Update search indices."""
        # Pattern index
        for pattern in metadata.patterns:
            # Domain patterns
            for domain in pattern.domain_patterns:
                if domain not in self.pattern_index:
                    self.pattern_index[domain] = []
                if source_type not in self.pattern_index[domain]:
                    self.pattern_index[domain].append(source_type)

            # File extensions
            for ext in pattern.file_extensions:
                if ext not in self.pattern_index:
                    self.pattern_index[ext] = []
                if source_type not in self.pattern_index[ext]:
                    self.pattern_index[ext].append(source_type)

        # Loader index
        for loader in metadata.loader_strategies:
            loader_name = loader.loader_class
            if loader_name not in self.loader_index:
                self.loader_index[loader_name] = []
            if source_type not in self.loader_index[loader_name]:
                self.loader_index[loader_name].append(source_type)

    def create_source_instance(
        self, source_type: str, analysis_result: PathAnalysisResult
    ) -> BaseSource | None:
        """Create a source instance from the analysis result."""
        if source_type not in self.source_classes:
            return None

        source_class = self.source_classes[source_type]

        # Create instance with appropriate fields based on category
        if source_class.__name__ == "LocalSource" or issubclass(
            source_class, LocalSource
        ):
            if analysis_result.is_file:
                return source_class(file_path=analysis_result.original_path)
            if analysis_result.is_directory:
                return source_class(directory_path=analysis_result.original_path)
            return source_class(file_path=analysis_result.original_path)

        if source_class.__name__ == "RemoteSource" or issubclass(
            source_class, RemoteSource
        ):
            return source_class(url=analysis_result.original_path)

        if source_class.__name__ == "DatabaseSource" or issubclass(
            source_class, DatabaseSource
        ):
            return source_class(connection_string=analysis_result.original_path)

        if source_class.__name__ == "CloudSource" or issubclass(
            source_class, CloudSource
        ):
            return source_class(
                bucket_name=getattr(analysis_result, "bucket_name", None),
                object_key=getattr(analysis_result, "object_key", None),
            )

        # Fallback for unknown source types
        return source_class()


# Global registry instance
registry = DynamicSourceRegistry()


# ============================================================================
# AUTO-REGISTRATION DECORATOR
# ============================================================================


def auto_source(
    source_type: str | None = None,
    patterns: list[SourcePattern] | None = None,
    loaders: list[str] | None = None,
    **pattern_kwargs,
):
    """Auto-registration decorator for source classes.

    Usage:
        @auto_source
        class MySource(LocalSource):
            pass

        @auto_source(domain_patterns=["example.com"])
        class APISource(RemoteSource):
            pass
    """

    def decorator(cls):
        # Create a new Config class if needed
        if not hasattr(cls, "Config"):
            cls.Config = type("Config", (), {})

        # Add explicit patterns if provided
        if patterns:
            cls.Config.patterns = patterns

        if loaders:
            cls.Config.preferred_loaders = loaders

        # Add pattern kwargs as Config attributes
        for key, value in pattern_kwargs.items():
            setattr(cls.Config, key, value)

        # Register with the global registry
        metadata = registry.register_source(cls, source_type=source_type)

        # Add metadata to class (not as private attribute)
        cls.source_metadata = metadata

        return cls

    # Handle both @auto_source and @auto_source()
    if inspect.isclass(source_type) and issubclass(source_type, BaseSource):
        cls = source_type
        source_type = None
        return decorator(cls)

    return decorator


# ============================================================================
# EXAMPLE SOURCE DEFINITIONS
# ============================================================================


@auto_source
class PDFSource(LocalSource):
    """PDF document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".pdf"]
        loader_strategies = {
            "fast": {
                "class": "PyPDFLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["text_heavy"],
            },
            "ocr": {
                "class": "UnstructuredPDFLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["scanned", "images"],
            },
            "tables": {
                "class": "PDFPlumberLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["tables", "forms"],
            },
        }


@auto_source(domain_patterns=["github.com"])
class GitHubSource(RemoteSource):
    """GitHub repository source."""

    repo_url: HttpUrl
    include_issues: bool = True
    include_code: bool = True

    class Config:
        path_patterns = ["/*/*"]  # user/repo pattern
        loader_strategies = {
            "issues": {
                "class": "GitHubIssuesLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["issues", "discussions"],
                "requires_auth": True,
                "required_credentials": ["github_token"],
            },
            "repo": {
                "class": "GitHubFileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["code", "documentation"],
                "requires_auth": True,
                "required_credentials": ["github_token"],
            },
        }
        required_credentials = ["github_token"]


@auto_source(domain_patterns=["youtube.com", "youtu.be"])
class YouTubeSource(RemoteSource):
    """YouTube video source."""

    video_url: HttpUrl
    include_transcript: bool = True

    class Config:
        loader_strategies = {
            "transcript": {
                "class": "YoutubeLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["transcripts", "captions"],
            },
            "audio": {
                "class": "YoutubeAudioLoader",
                "speed": "slow",
                "quality": "medium",
                "best_for": ["audio", "speech"],
            },
        }


@auto_source
class WebPageSource(RemoteSource):
    """General web page source."""

    url: HttpUrl
    max_depth: int = 1

    class Config:
        loader_strategies = {
            "basic": {
                "class": "WebBaseLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_pages"],
            },
            "recursive": {
                "class": "RecursiveUrlLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["documentation", "wikis"],
            },
            "javascript": {
                "class": "PlaywrightURLLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["spa", "dynamic"],
            },
        }


@auto_source(scheme_patterns=["postgresql", "postgres"])
class PostgreSQLSource(DatabaseSource):
    """PostgreSQL database source."""

    connection_string: str
    table_name: str | None = None

    class Config:
        loader_strategies = {
            "sql": {
                "class": "SQLDatabaseLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["tables", "queries"],
                "requires_auth": True,
                "required_credentials": ["postgres_credentials"],
            }
        }
        required_credentials = ["postgres_credentials"]


@auto_source(scheme_patterns=["s3"])
class S3Source(CloudSource):
    """Amazon S3 bucket source."""

    bucket_name: str
    object_key: str | None = None
    is_directory: bool = False

    class Config:
        loader_strategies = {
            "file": {
                "class": "S3FileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["single_file"],
                "requires_auth": True,
                "required_credentials": ["aws_credentials"],
            },
            "directory": {
                "class": "S3DirectoryLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["multiple_files", "directory"],
                "requires_auth": True,
                "required_credentials": ["aws_credentials"],
            },
        }
        required_credentials = ["aws_credentials"]


@auto_source
class CSVSource(LocalSource):
    """CSV data source."""

    file_path: FilePath
    has_header: bool = True

    class Config:
        file_extensions = [".csv"]
        loader_strategies = {
            "basic": {
                "class": "CSVLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["tabular_data"],
            },
            "unstructured": {
                "class": "UnstructuredCSVLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_csv"],
            },
        }


@auto_source
class JSONSource(LocalSource):
    """JSON data source."""

    file_path: FilePath
    jq_schema: str | None = None

    class Config:
        file_extensions = [".json"]
        loader_strategies = {
            "basic": {
                "class": "JSONLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["structured_data"],
            }
        }


@auto_source
class TextSource(LocalSource):
    """Plain text source."""

    file_path: FilePath
    encoding: str = "utf-8"

    class Config:
        file_extensions = [".txt", ".text"]
        loader_strategies = {
            "basic": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["plain_text"],
            },
            "unstructured": {
                "class": "UnstructuredFileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_text"],
            },
        }


@auto_source
class MarkdownSource(LocalSource):
    """Markdown document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".md", ".markdown"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredMarkdownLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["markdown"],
            },
            "text": {
                "class": "TextLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_markdown"],
            },
        }


@auto_source
class DirectorySource(LocalSource):
    """Directory source with multiple files."""

    directory_path: Path
    glob_pattern: str = "**/*"
    recursive: bool = True

    class Config:
        loader_strategies = {
            "basic": {
                "class": "DirectoryLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["mixed_files"],
            }
        }


@auto_source(domain_patterns=["wikipedia.org"])
class WikipediaSource(RemoteSource):
    """Wikipedia article source."""

    url: HttpUrl
    lang: str = "en"

    class Config:
        loader_strategies = {
            "wiki": {
                "class": "WikipediaLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["encyclopedia", "articles"],
            }
        }


@auto_source(domain_patterns=["arxiv.org"])
class ArxivSource(RemoteSource):
    """ArXiv paper source."""

    url: HttpUrl
    load_all_available_pdfs: bool = False

    class Config:
        loader_strategies = {
            "arxiv": {
                "class": "ArxivLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["scientific_papers", "research"],
            }
        }


@auto_source(scheme_patterns=["sqlite", "sqlite3"])
class SQLiteSource(DatabaseSource):
    """SQLite database source."""

    connection_string: str
    query: str | None = None

    class Config:
        loader_strategies = {
            "sql": {
                "class": "SQLDatabaseLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["sql", "tables"],
            }
        }


# ============================================================================
# LOADING UTILITY FUNCTIONS
# ============================================================================


def analyze_and_load(
    path: str, credential_manager: CredentialManager | None = None
) -> tuple[Any, dict[str, Any]]:
    """Analyze a path and load documents using the appropriate source and loader.

    Args:
        path: The path to analyze and load
        credential_manager: Optional credential manager for authentication

    Returns:
        Tuple of (loaded_documents, metadata)
    """
    # Mock for now - replace with actual path analysis
    # analysis_result = analyze_path_comprehensive(path)
    analysis_result = PathAnalysisResult(
        original_path=path,
        is_file=True,
        file_extension=Path(path).suffix if "." in path else None,
    )

    # Find matching source types
    matches = registry.find_matching_sources(analysis_result)

    if not matches:
        raise ValueError(f"No matching source types found for {path}")

    # Select best source type
    source_type, confidence = matches[0]

    # Create source instance
    source = registry.create_source_instance(source_type, analysis_result)

    if not source:
        raise ValueError(f"Failed to create source instance for {source_type}")

    # Authenticate if needed
    if hasattr(source, "authenticate") and credential_manager:
        authenticated = source.authenticate(credential_manager)
        if not authenticated:
            raise ValueError(f"Authentication failed for {source_type}")

    # Create loader
    loader = source.create_loader()

    # In a real implementation, we would actually load documents here
    # documents = loader.load()

    # For now, return a mock result
    documents = ["Mock document 1", "Mock document 2"]

    metadata = {
        "source_type": source_type,
        "confidence": confidence,
        "loader": loader,
        "analysis_result": analysis_result,
    }

    return documents, metadata


# ============================================================================
# TESTING FUNCTIONS
# ============================================================================


def list_registered_sources():
    """List all registered source types."""
    print(f"Registered Sources: {len(registry.source_classes)}")
    for source_type, metadata in registry.source_metadata.items():
        print(
            f"  - {source_type}: {metadata.category} ({len(metadata.loader_strategies)} loaders)"
        )
        print(f"    Description: {metadata.description.strip()}")
        if metadata.patterns:
            print(f"    Patterns: {len(metadata.patterns)}")
            for pattern in metadata.patterns[:2]:  # Show first 2 patterns
                parts = []
                if pattern.file_extensions:
                    parts.append(f"file_ext={pattern.file_extensions}")
                if pattern.domain_patterns:
                    parts.append(f"domains={pattern.domain_patterns}")
                if pattern.scheme_patterns:
                    parts.append(f"schemes={pattern.scheme_patterns}")
                print(f"      - {', '.join(parts)}")

        if metadata.loader_strategies:
            print(f"    Loaders: {len(metadata.loader_strategies)}")
            for loader in metadata.loader_strategies[:2]:  # Show first 2 loaders
                print(
                    f"      - {loader.strategy_name}: {loader.loader_class} (speed={loader.speed}, quality={loader.quality})"
                )

        print()


def test_source_matching(paths):
    """Test source matching with different paths."""
    print("\nTesting Source Matching:")
    print("=" * 60)

    for path in paths:
        print(f"\nAnalyzing: {path}")

        # Mock analysis result - replace with actual path analysis
        analysis_result = PathAnalysisResult(
            original_path=path,
            is_file="." in path,  # Simple heuristic
            file_extension=Path(path).suffix if "." in path else None,
        )

        # Add URL components for URLs
        if path.startswith(("http://", "https://")):
            analysis_result.is_remote = True
            analysis_result.path_type = (
                PathType.URL_HTTPS if path.startswith("https://") else PathType.URL_HTTP
            )
            analysis_result.url_components = {
                "hostname": urlparse(path).netloc,
                "scheme": urlparse(path).scheme,
            }
        elif path.startswith("s3://"):
            analysis_result.is_remote = True
            analysis_result.path_type = PathType.CLOUD_STORAGE
            analysis_result.cloud_provider = CloudProvider.AWS_S3
        elif path.endswith(".db") or path.startswith(("postgresql://", "sqlite://")):
            analysis_result.is_remote = True
            analysis_result.path_type = PathType.DATABASE_URI
            analysis_result.database_type = (
                DatabaseType.SQLITE if path.endswith(".db") else DatabaseType.POSTGRESQL
            )
        else:
            analysis_result.is_local = True
            analysis_result.path_type = (
                PathType.LOCAL_FILE
                if analysis_result.is_file
                else PathType.LOCAL_DIRECTORY
            )

        # Find matching source types
        matches = registry.find_matching_sources(analysis_result)

        if matches:
            print(f"Matches found: {len(matches)}")
            for source_type, confidence in matches[:3]:  # Show top 3
                metadata = registry.source_metadata[source_type]
                print(
                    f"  - {source_type}: confidence={confidence:.2f}, category={metadata.category}"
                )

                # Try to create a source instance
                source = registry.create_source_instance(source_type, analysis_result)
                if source:
                    print(f"    Created source instance: {source.__class__.__name__}")

                    # Get available loader strategies
                    strategies = [s.strategy_name for s in metadata.loader_strategies]
                    print(f"    Available loaders: {strategies}")

                    # Create a loader (mock)
                    try:
                        loader = source.create_loader()
                        print(f"    Created loader: {loader}")
                    except Exception as e:
                        print(f"    Error creating loader: {e}")
        else:
            print("No matches found")


if __name__ == "__main__":
    # Register sources automatically through decorators

    # List all registered sources
    list_registered_sources()

    # Test with various paths
    test_paths = [
        "/path/to/document.pdf",
        "/path/to/data.csv",
        "/path/to/code.py",
        "/path/to/directory/",
        "https://github.com/user/repo",
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
        "https://arxiv.org/abs/2303.12712",
        "s3://my-bucket/path/to/file.pdf",
        "postgresql://user:pass@localhost:5432/db",
        "/path/to/database.db",
    ]

    # Test source matching
    test_source_matching(test_paths)
