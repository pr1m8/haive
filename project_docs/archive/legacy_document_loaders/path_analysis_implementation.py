"""Path Analysis System for Document Loaders.

This module provides a comprehensive path analysis system that can determine
the nature of any input path, URL, or identifier and extract relevant metadata.

The path analysis system is a critical foundation for the document loader engine,
as it enables automatic detection of source types based on the input path.
"""

from abc import ABC, abstractmethod
from enum import Enum
import logging
import mimetypes
import os
from pathlib import Path
import re
from typing import ClassVar
from urllib.parse import parse_qs, urlparse

from pydantic import BaseModel, Field


# Configure logging
logger = logging.getLogger(__name__)

# ============================================================================
# TYPE DEFINITIONS
# ============================================================================

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


class DocumentType(str, Enum):
    """Document file types."""
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    ODT = "odt"
    RTF = "rtf"
    TXT = "txt"
    MARKDOWN = "markdown"
    HTML = "html"
    EPUB = "epub"
    MOBI = "mobi"
    PPTX = "pptx"
    XLSX = "xlsx"
    CSV = "csv"
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    UNKNOWN_DOCUMENT = "unknown_document"


class DataType(str, Enum):
    """Data file types."""
    CSV = "csv"
    TSV = "tsv"
    JSON = "json"
    JSONL = "jsonl"
    YAML = "yaml"
    XML = "xml"
    PARQUET = "parquet"
    AVRO = "avro"
    EXCEL = "excel"
    SQLITE = "sqlite"
    HDF5 = "hdf5"
    UNKNOWN_DATA = "unknown_data"


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


# ============================================================================
# COMPONENT MODELS
# ============================================================================

class URLComponents(BaseModel):
    """Detailed URL component analysis."""
    scheme: str | None = None
    netloc: str | None = None
    path: str | None = None
    query: str | None = None
    fragment: str | None = None
    hostname: str | None = None
    port: int | None = None
    domain: str | None = None
    subdomain: str | None = None
    root_url: str | None = None
    base_url: str | None = None
    path_segments: list[str] = Field(default_factory=list)
    query_params: dict[str, list[str]] = Field(default_factory=dict)
    is_secure: bool = False
    is_local_network: bool = False
    is_ip_address: bool = False
    content_type_hint: str | None = None


class DomainInfo(BaseModel):
    """Domain information and classification."""
    domain: str
    subdomain: str | None = None
    second_level_domain: str
    top_level_domain: str
    is_well_known: bool = False
    service_type: str | None = None

    # Known services mapping - using ClassVar to indicate this is not a field
    KNOWN_SERVICES: ClassVar[dict[str, str]] = {
        "github.com": "code_repository",
        "gitlab.com": "code_repository",
        "bitbucket.org": "code_repository",
        "youtube.com": "video",
        "youtu.be": "video",
        "vimeo.com": "video",
        "wikipedia.org": "encyclopedia",
        "arxiv.org": "academic",
        "scholar.google.com": "academic",
        "docs.google.com": "document",
        "drive.google.com": "cloud_storage",
        "dropbox.com": "cloud_storage",
        "box.com": "cloud_storage",
        "notion.so": "document",
        "airtable.com": "database",
        "slack.com": "communication",
        "twitter.com": "social_media",
        "linkedin.com": "social_media",
        "reddit.com": "social_media",
        "medium.com": "blog",
        "substack.com": "blog",
    }


# ============================================================================
# ANALYSIS RESULT
# ============================================================================

class PathAnalysisResult(BaseModel):
    """Comprehensive analysis result for a given path or URL."""
    original_path: str
    path_type: PathType = PathType.UNKNOWN

    # Basic properties
    is_local: bool = False
    is_remote: bool = False
    is_absolute: bool = False
    is_relative: bool = False
    exists: bool = False
    is_readable: bool = False
    is_writable: bool = False
    is_executable: bool = False
    is_file: bool = False
    is_directory: bool = False
    is_symlink: bool = False

    # File properties
    file_size: int | None = None
    parent_directory: str | None = None
    filename: str | None = None
    file_extension: str | None = None
    file_stem: str | None = None
    file_category: FileCategory | None = None
    specific_file_type: str | None = None
    mime_type: str | None = None
    permissions: str | None = None

    # URL properties
    url_components: URLComponents | None = None
    domain_info: DomainInfo | None = None

    # Database properties
    database_type: DatabaseType | None = None
    database_name: str | None = None

    # Cloud properties
    cloud_provider: CloudProvider | None = None
    bucket_name: str | None = None
    object_key: str | None = None

    # Path normalization
    resolved_path: str | None = None
    canonical_path: str | None = None

    # Analysis metadata
    analysis_errors: list[str] = Field(default_factory=list)
    analysis_warnings: list[str] = Field(default_factory=list)

    def get_source_hint(self) -> str:
        """Get a hint about the source type based on analysis."""
        if self.path_type == PathType.LOCAL_FILE:
            if self.file_category:
                return f"local_{self.file_category.value}"
            if self.file_extension:
                return f"local_file_{self.file_extension.lstrip('.')}"
            return "local_file"

        if self.path_type == PathType.LOCAL_DIRECTORY:
            return "local_directory"

        if self.path_type in [PathType.URL_HTTP, PathType.URL_HTTPS]:
            if self.domain_info and self.domain_info.service_type:
                return f"web_{self.domain_info.service_type}"
            if self.domain_info and self.domain_info.domain:
                return f"web_{self.domain_info.domain.replace('.', '_')}"
            return "web_page"

        if self.path_type == PathType.DATABASE_URI:
            if self.database_type:
                return f"database_{self.database_type.value}"
            return "database"

        if self.path_type == PathType.CLOUD_STORAGE:
            if self.cloud_provider:
                return f"cloud_{self.cloud_provider.value}"
            return "cloud_storage"

        return "unknown"


# ============================================================================
# PATH ANALYZERS
# ============================================================================

class BasePathAnalyzer(ABC):
    """Abstract base class for path analyzers."""

    @abstractmethod
    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""

    @abstractmethod
    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Perform analysis and update the result object."""


class LocalPathAnalyzer(BasePathAnalyzer):
    """Analyzer for local filesystem paths."""

    # File extension to category mappings
    EXTENSION_CATEGORIES: ClassVar[dict[str, dict[str, set[str]]]] = {
        # Documents
        ".pdf": (FileCategory.DOCUMENT, DocumentType.PDF),
        ".docx": (FileCategory.DOCUMENT, DocumentType.DOCX),
        ".doc": (FileCategory.DOCUMENT, DocumentType.DOC),
        ".odt": (FileCategory.DOCUMENT, DocumentType.ODT),
        ".rtf": (FileCategory.DOCUMENT, DocumentType.RTF),
        ".txt": (FileCategory.TEXT, DocumentType.TXT),
        ".md": (FileCategory.TEXT, DocumentType.MARKDOWN),
        ".markdown": (FileCategory.TEXT, DocumentType.MARKDOWN),
        ".html": (FileCategory.TEXT, DocumentType.HTML),
        ".htm": (FileCategory.TEXT, DocumentType.HTML),
        ".epub": (FileCategory.DOCUMENT, DocumentType.EPUB),
        ".mobi": (FileCategory.DOCUMENT, DocumentType.MOBI),
        ".pptx": (FileCategory.DOCUMENT, DocumentType.PPTX),
        ".ppt": (FileCategory.DOCUMENT, DocumentType.PPTX),
        ".xlsx": (FileCategory.DATA, DocumentType.XLSX),
        ".xls": (FileCategory.DATA, DocumentType.XLSX),

        # Data
        ".csv": (FileCategory.DATA, DataType.CSV),
        ".tsv": (FileCategory.DATA, DataType.TSV),
        ".json": (FileCategory.DATA, DataType.JSON),
        ".jsonl": (FileCategory.DATA, DataType.JSONL),
        ".yaml": (FileCategory.DATA, DataType.YAML),
        ".yml": (FileCategory.DATA, DataType.YAML),
        ".xml": (FileCategory.DATA, DataType.XML),
        ".parquet": (FileCategory.DATA, DataType.PARQUET),
        ".avro": (FileCategory.DATA, DataType.AVRO),
        ".sqlite": (FileCategory.DATA, DataType.SQLITE),
        ".db": (FileCategory.DATA, DataType.SQLITE),
        ".h5": (FileCategory.DATA, DataType.HDF5),

        # Code
        ".py": (FileCategory.CODE, "python"),
        ".js": (FileCategory.CODE, "javascript"),
        ".ts": (FileCategory.CODE, "typescript"),
        ".java": (FileCategory.CODE, "java"),
        ".c": (FileCategory.CODE, "c"),
        ".cpp": (FileCategory.CODE, "cpp"),
        ".cs": (FileCategory.CODE, "csharp"),
        ".go": (FileCategory.CODE, "go"),
        ".rb": (FileCategory.CODE, "ruby"),
        ".php": (FileCategory.CODE, "php"),
        ".rs": (FileCategory.CODE, "rust"),
        ".swift": (FileCategory.CODE, "swift"),
        ".kt": (FileCategory.CODE, "kotlin"),
        ".sh": (FileCategory.CODE, "shell"),
        ".sql": (FileCategory.CODE, "sql"),
        ".ipynb": (FileCategory.CODE, "jupyter"),

        # Images
        ".jpg": (FileCategory.IMAGE, "jpeg"),
        ".jpeg": (FileCategory.IMAGE, "jpeg"),
        ".png": (FileCategory.IMAGE, "png"),
        ".gif": (FileCategory.IMAGE, "gif"),
        ".bmp": (FileCategory.IMAGE, "bmp"),
        ".tiff": (FileCategory.IMAGE, "tiff"),
        ".tif": (FileCategory.IMAGE, "tiff"),
        ".svg": (FileCategory.IMAGE, "svg"),
        ".webp": (FileCategory.IMAGE, "webp"),

        # Audio
        ".mp3": (FileCategory.AUDIO, "mp3"),
        ".wav": (FileCategory.AUDIO, "wav"),
        ".flac": (FileCategory.AUDIO, "flac"),
        ".aac": (FileCategory.AUDIO, "aac"),
        ".ogg": (FileCategory.AUDIO, "ogg"),
        ".m4a": (FileCategory.AUDIO, "m4a"),

        # Video
        ".mp4": (FileCategory.VIDEO, "mp4"),
        ".avi": (FileCategory.VIDEO, "avi"),
        ".mov": (FileCategory.VIDEO, "mov"),
        ".mkv": (FileCategory.VIDEO, "mkv"),
        ".webm": (FileCategory.VIDEO, "webm"),
        ".flv": (FileCategory.VIDEO, "flv"),

        # Archives
        ".zip": (FileCategory.ARCHIVE, "zip"),
        ".tar": (FileCategory.ARCHIVE, "tar"),
        ".gz": (FileCategory.ARCHIVE, "gzip"),
        ".bz2": (FileCategory.ARCHIVE, "bzip2"),
        ".rar": (FileCategory.ARCHIVE, "rar"),
        ".7z": (FileCategory.ARCHIVE, "7zip"),

        # Executables
        ".exe": (FileCategory.EXECUTABLE, "windows_executable"),
        ".dll": (FileCategory.EXECUTABLE, "windows_library"),
        ".so": (FileCategory.EXECUTABLE, "shared_object"),
        ".dmg": (FileCategory.EXECUTABLE, "mac_disk_image"),
        ".app": (FileCategory.EXECUTABLE, "mac_application"),

        # Other
        ".ttf": (FileCategory.FONT, "truetype"),
        ".otf": (FileCategory.FONT, "opentype"),
        ".woff": (FileCategory.FONT, "webfont"),
        ".woff2": (FileCategory.FONT, "webfont2"),
    }

    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        # Local analyzer is very permissive and can handle most paths
        # that aren't clearly URLs or special URIs
        if path.startswith(("http://", "https://", "ftp://", "s3://", "gs://", "azure://")):
            return False

        # Check for database URIs
        return not (re.match(r"^[a-zA-Z0-9]+://.*$", path) and ":" in path and "@" in path)

    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Analyze a local path and update the result object."""
        result.is_local = True
        result.resolved_path = path

        # Convert to Path object for easier analysis
        path_obj = Path(path)

        # Check if the path exists
        if path_obj.exists():
            result.exists = True

            # Check file vs directory
            if path_obj.is_file():
                result.is_file = True
                result.path_type = PathType.LOCAL_FILE

                # Get file metadata
                result.file_size = path_obj.stat().st_size
                result.filename = path_obj.name
                result.file_extension = path_obj.suffix.lower()
                result.file_stem = path_obj.stem
                result.parent_directory = str(path_obj.parent)
                result.is_absolute = path_obj.is_absolute()
                result.is_relative = not path_obj.is_absolute()

                # Get permissions
                try:
                    result.is_readable = os.access(path, os.R_OK)
                    result.is_writable = os.access(path, os.W_OK)
                    result.is_executable = os.access(path, os.X_OK)

                    # Format permissions like ls -l
                    mode = path_obj.stat().st_mode
                    result.permissions = format(mode & 0o777, "o")
                except Exception as e:
                    result.analysis_warnings.append(f"Failed to check permissions: {e!s}")

                # Determine file category and type
                if result.file_extension in self.EXTENSION_CATEGORIES:
                    category, specific_type = self.EXTENSION_CATEGORIES[result.file_extension]
                    result.file_category = category
                    result.specific_file_type = str(specific_type)
                else:
                    # Try to determine from content
                    try:
                        import magic  # python-magic package
                        mime = magic.from_file(path, mime=True)
                        result.mime_type = mime

                        # Map MIME type to category
                        if mime.startswith("text/"):
                            result.file_category = FileCategory.TEXT
                        elif mime.startswith("image/"):
                            result.file_category = FileCategory.IMAGE
                        elif mime.startswith("video/"):
                            result.file_category = FileCategory.VIDEO
                        elif mime.startswith("audio/"):
                            result.file_category = FileCategory.AUDIO
                        elif mime in ["application/pdf"]:
                            result.file_category = FileCategory.DOCUMENT
                            result.specific_file_type = str(DocumentType.PDF)
                        elif mime in ["application/json"]:
                            result.file_category = FileCategory.DATA
                            result.specific_file_type = str(DataType.JSON)
                        elif mime in ["application/zip", "application/x-gzip", "application/x-tar"]:
                            result.file_category = FileCategory.ARCHIVE
                        elif mime in ["application/x-executable", "application/x-mach-binary"]:
                            result.file_category = FileCategory.EXECUTABLE
                        # Use extension if we have it, otherwise mark as unknown
                        elif not result.file_category:
                            result.file_category = FileCategory.UNKNOWN_FILE
                    except ImportError:
                        # Fallback to mimetypes library
                        mime_type, _ = mimetypes.guess_type(path)
                        if mime_type:
                            result.mime_type = mime_type

            elif path_obj.is_dir():
                result.is_directory = True
                result.path_type = PathType.LOCAL_DIRECTORY
                result.parent_directory = str(path_obj.parent)
                result.is_absolute = path_obj.is_absolute()
                result.is_relative = not path_obj.is_absolute()

                # Check permissions
                try:
                    result.is_readable = os.access(path, os.R_OK)
                    result.is_writable = os.access(path, os.W_OK)
                    result.is_executable = os.access(path, os.X_OK)
                except Exception as e:
                    result.analysis_warnings.append(f"Failed to check permissions: {e!s}")

            elif path_obj.is_symlink():
                result.is_symlink = True
                result.path_type = PathType.LOCAL_SYMLINK

                # Get target
                try:
                    target = path_obj.resolve()
                    result.resolved_path = str(target)
                    result.is_file = target.is_file()
                    result.is_directory = target.is_dir()
                except Exception as e:
                    result.analysis_warnings.append(f"Failed to resolve symlink: {e!s}")
        else:
            # Path doesn't exist
            result.path_type = PathType.LOCAL_NONEXISTENT

            # We can still extract some information
            result.filename = path_obj.name
            result.file_extension = path_obj.suffix.lower()
            result.file_stem = path_obj.stem
            result.parent_directory = str(path_obj.parent)
            result.is_absolute = path_obj.is_absolute()
            result.is_relative = not path_obj.is_absolute()

            # Try to categorize based on extension
            if result.file_extension in self.EXTENSION_CATEGORIES:
                category, specific_type = self.EXTENSION_CATEGORIES[result.file_extension]
                result.file_category = category
                result.specific_file_type = str(specific_type)

            # Check if parent directory exists
            if path_obj.parent.exists():
                result.analysis_warnings.append("Path doesn't exist, but parent directory does")
            else:
                result.analysis_warnings.append("Neither path nor parent directory exist")

        # Try to get canonical path
        try:
            result.canonical_path = str(path_obj.resolve())
        except Exception as e:
            result.analysis_errors.append(f"Failed to get canonical path: {e!s}")


class URLAnalyzer(BasePathAnalyzer):
    """Analyzer for URLs and web resources."""

    # Well-known domains and their service types
    KNOWN_DOMAINS = DomainInfo.KNOWN_SERVICES

    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        return path.startswith(("http://", "https://", "ftp://"))

    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Analyze a URL and update the result object."""
        result.is_remote = True

        # Parse URL
        parsed_url = urlparse(path)

        # Set basic URL properties
        if parsed_url.scheme == "http":
            result.path_type = PathType.URL_HTTP
        elif parsed_url.scheme == "https":
            result.path_type = PathType.URL_HTTPS
        elif parsed_url.scheme == "ftp":
            result.path_type = PathType.URL_FTP
        else:
            result.path_type = PathType.URL_HTTP  # Default

        # Create URL components
        components = URLComponents(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            path=parsed_url.path,
            query=parsed_url.query,
            fragment=parsed_url.fragment,
            hostname=parsed_url.hostname,
            port=parsed_url.port,
            is_secure=parsed_url.scheme == "https"
        )

        # Extract domain info
        if parsed_url.hostname:
            # Extract domain components
            try:
                # Try to use tldextract if available
                import tldextract
                extracted = tldextract.extract(parsed_url.hostname)
                domain = f"{extracted.domain}.{extracted.suffix}"
                subdomain = extracted.subdomain if extracted.subdomain else None
                second_level = extracted.domain
                top_level = extracted.suffix
            except ImportError:
                # Fallback to basic parsing
                parts = parsed_url.hostname.split(".")
                if len(parts) >= 2:
                    top_level = parts[-1]
                    second_level = parts[-2]
                    domain = f"{second_level}.{top_level}"
                    subdomain = ".".join(parts[:-2]) if len(parts) > 2 else None
                else:
                    domain = parsed_url.hostname
                    top_level = ""
                    second_level = domain
                    subdomain = None

            components.domain = domain
            components.subdomain = subdomain

            # Check if it's an IP address
            if re.match(r"^\d+\.\d+\.\d+\.\d+$", parsed_url.hostname):
                components.is_ip_address = True

            # Check if local network
            if (
                parsed_url.hostname == "localhost"
                or parsed_url.hostname.startswith("127.")
                or parsed_url.hostname.startswith("192.168.")
                or parsed_url.hostname.startswith("10.")
                or parsed_url.hostname.startswith("172.")
            ):
                components.is_local_network = True

            # Create domain info
            domain_info = DomainInfo(
                domain=domain,
                subdomain=subdomain,
                second_level_domain=second_level,
                top_level_domain=top_level
            )

            # Check for well-known domains
            for known_domain, service_type in self.KNOWN_DOMAINS.items():
                if known_domain in domain:
                    domain_info.is_well_known = True
                    domain_info.service_type = service_type
                    break

            result.domain_info = domain_info

        # Extract path segments
        if parsed_url.path:
            segments = [s for s in parsed_url.path.split("/") if s]
            components.path_segments = segments

            # Check for file extension in last segment
            if segments and "." in segments[-1]:
                file_name = segments[-1]
                file_extension = "." + file_name.split(".")[-1].lower()

                result.filename = file_name
                result.file_extension = file_extension

                # Try to determine file type from extension
                if file_extension in LocalPathAnalyzer.EXTENSION_CATEGORIES:
                    category, specific_type = LocalPathAnalyzer.EXTENSION_CATEGORIES[file_extension]
                    result.file_category = category
                    result.specific_file_type = str(specific_type)

                    # Set content type hint
                    mime_type, _ = mimetypes.guess_type(file_name)
                    if mime_type:
                        components.content_type_hint = mime_type
                        result.mime_type = mime_type

        # Extract query parameters
        if parsed_url.query:
            components.query_params = parse_qs(parsed_url.query)

        # Set base URL (without query and fragment)
        components.base_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
        components.root_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # Store URL components
        result.url_components = components

        # Mark as file-like for specific web resources
        if result.file_extension and result.file_category:
            result.is_file = True

        # Set resolved path to original URL
        result.resolved_path = path


class DatabaseURIAnalyzer(BasePathAnalyzer):
    """Analyzer for database connection URIs."""

    # Regex patterns for common database URIs
    DB_PATTERNS: ClassVar[dict[str, str]] = {
        DatabaseType.POSTGRESQL: r"^postgres(?:ql)?://.*$",
        DatabaseType.MYSQL: r"^mysql://.*$",
        DatabaseType.SQLITE: r"^sqlite://.*$",
        DatabaseType.MONGODB: r"^mongodb://.*$",
        DatabaseType.REDIS: r"^redis://.*$",
        DatabaseType.ORACLE: r"^oracle://.*$",
        DatabaseType.MSSQL: r"^mssql://.*$",
        DatabaseType.CASSANDRA: r"^cassandra://.*$",
        DatabaseType.ELASTICSEARCH: r"^elasticsearch://.*$",
        DatabaseType.SNOWFLAKE: r"^snowflake://.*$",
        DatabaseType.BIGQUERY: r"^bigquery://.*$",
    }

    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        # Check for database URI patterns
        for pattern in self.DB_PATTERNS.values():
            if re.match(pattern, path):
                return True

        # Check for SQLite file paths
        return bool(path.endswith((".db", ".sqlite", ".sqlite3")) and not path.startswith(("http://", "https://")))

    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Analyze a database URI and update the result object."""
        result.is_remote = True
        result.path_type = PathType.DATABASE_URI

        # Determine database type
        db_type = None
        for db_type_enum, pattern in self.DB_PATTERNS.items():
            if re.match(pattern, path):
                db_type = db_type_enum
                break

        # Handle SQLite files
        if not db_type and path.endswith((".db", ".sqlite", ".sqlite3")):
            db_type = DatabaseType.SQLITE
            # SQLite file paths are local
            result.is_local = True
            result.is_remote = False

            # Analyze as a local file
            local_analyzer = LocalPathAnalyzer()
            local_analyzer.analyze(path, result)

            # Override some properties for database
            result.path_type = PathType.DATABASE_URI
            result.file_category = FileCategory.DATA
            result.specific_file_type = str(DataType.SQLITE)

        # Set database type
        if db_type:
            result.database_type = db_type
        else:
            result.database_type = DatabaseType.UNKNOWN_DB

        # Try to extract database name from URI
        if "://" in path:
            try:
                parsed_url = urlparse(path)

                # Path component often contains database name
                if parsed_url.path and parsed_url.path != "/":
                    # Remove leading slash
                    db_name = parsed_url.path.lstrip("/")

                    # Check for additional path components
                    if "/" in db_name:
                        db_name = db_name.split("/")[0]

                    result.database_name = db_name

                # Some database URIs have the name in the netloc
                elif parsed_url.netloc:
                    # Format often: username:password@host:port/dbname
                    if "@" in parsed_url.netloc:
                        host_part = parsed_url.netloc.split("@")[1]
                    else:
                        host_part = parsed_url.netloc

                    # Check for port separator
                    if ":" in host_part:
                        host_part = host_part.split(":")[0]

                    # Use host as fallback database name
                    if not result.database_name:
                        result.database_name = host_part

                # Set a default name if we couldn't extract one
                if not result.database_name:
                    result.database_name = f"{result.database_type.value}_db"

            except Exception as e:
                result.analysis_warnings.append(f"Failed to parse database URI: {e!s}")

        # Set resolved path to original URI
        result.resolved_path = path


class CloudStorageAnalyzer(BasePathAnalyzer):
    """Analyzer for cloud storage paths."""

    # Regex patterns for cloud storage URLs
    CLOUD_PATTERNS: ClassVar[dict[str, str]] = {
        CloudProvider.AWS_S3: r"^s3://([^/]+)(?:/(.*))?$",
        CloudProvider.GOOGLE_CLOUD: r"^gs://([^/]+)(?:/(.*))?$",
        CloudProvider.AZURE_BLOB: r"^azure://([^/]+)(?:/(.*))?$",
        CloudProvider.DROPBOX: r"^dropbox://(.*)$",
        CloudProvider.ONEDRIVE: r"^onedrive://(.*)$",
    }

    # Domain patterns for HTTP URLs to cloud storage
    CLOUD_DOMAINS: ClassVar[dict[str, str]] = {
        r".*\.s3\.amazonaws\.com": CloudProvider.AWS_S3,
        r"storage\.googleapis\.com": CloudProvider.GOOGLE_CLOUD,
        r".*\.blob\.core\.windows\.net": CloudProvider.AZURE_BLOB,
        r".*\.dropboxusercontent\.com": CloudProvider.DROPBOX,
        r".*\.onedrive\.live\.com": CloudProvider.ONEDRIVE,
    }

    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        # Check for cloud storage URI patterns
        for pattern in self.CLOUD_PATTERNS.values():
            if re.match(pattern, path):
                return True

        # Check for HTTP URLs to cloud storage
        if path.startswith(("http://", "https://")):
            parsed_url = urlparse(path)
            for domain_pattern in self.CLOUD_DOMAINS:
                if re.match(domain_pattern, parsed_url.netloc):
                    return True

        return False

    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Analyze a cloud storage path and update the result object."""
        result.is_remote = True
        result.path_type = PathType.CLOUD_STORAGE

        # First check for direct cloud URIs
        for provider, pattern in self.CLOUD_PATTERNS.items():
            match = re.match(pattern, path)
            if match:
                result.cloud_provider = provider

                # Extract bucket and key
                if len(match.groups()) >= 1:
                    result.bucket_name = match.group(1)

                if len(match.groups()) >= 2 and match.group(2):
                    result.object_key = match.group(2)

                    # Try to extract file properties from key
                    if "/" in result.object_key:
                        # Last part is the filename
                        filename = result.object_key.split("/")[-1]
                        result.filename = filename

                        # Check for file extension
                        if "." in filename:
                            result.file_extension = "." + filename.split(".")[-1].lower()

                            # Try to determine file type from extension
                            if result.file_extension in LocalPathAnalyzer.EXTENSION_CATEGORIES:
                                category, specific_type = LocalPathAnalyzer.EXTENSION_CATEGORIES[result.file_extension]
                                result.file_category = category
                                result.specific_file_type = str(specific_type)

                    # Set as file if we have an object key
                    result.is_file = True
                else:
                    # No object key means it's a bucket/container
                    result.is_directory = True

                break

        # If not matched, check for HTTP URLs to cloud storage
        if not result.cloud_provider and path.startswith(("http://", "https://")):
            parsed_url = urlparse(path)

            for domain_pattern, provider in self.CLOUD_DOMAINS.items():
                if re.match(domain_pattern, parsed_url.netloc):
                    result.cloud_provider = provider

                    # Try to extract bucket and key from URL
                    if provider == CloudProvider.AWS_S3:
                        if parsed_url.netloc.endswith("s3.amazonaws.com"):
                            # Bucket is in path
                            path_parts = parsed_url.path.lstrip("/").split("/")
                            if path_parts:
                                result.bucket_name = path_parts[0]
                                if len(path_parts) > 1:
                                    result.object_key = "/".join(path_parts[1:])
                        else:
                            # Bucket is in hostname
                            result.bucket_name = parsed_url.netloc.split(".")[0]
                            result.object_key = parsed_url.path.lstrip("/")

                    elif provider == CloudProvider.GOOGLE_CLOUD:
                        path_parts = parsed_url.path.lstrip("/").split("/")
                        if path_parts:
                            result.bucket_name = path_parts[0]
                            if len(path_parts) > 1:
                                result.object_key = "/".join(path_parts[1:])

                    # Extract file information if we have an object key
                    if result.object_key:
                        result.is_file = True

                        # Get filename from last path segment
                        filename = result.object_key.split("/")[-1]
                        result.filename = filename

                        # Check for file extension
                        if "." in filename:
                            result.file_extension = "." + filename.split(".")[-1].lower()

                            # Try to determine file type from extension
                            if result.file_extension in LocalPathAnalyzer.EXTENSION_CATEGORIES:
                                category, specific_type = LocalPathAnalyzer.EXTENSION_CATEGORIES[result.file_extension]
                                result.file_category = category
                                result.specific_file_type = str(specific_type)
                    else:
                        # No object key means it's a bucket/container
                        result.is_directory = True

                    # Also set URL components
                    url_analyzer = URLAnalyzer()
                    url_analyzer.analyze(path, result)

                    # But override the path type
                    result.path_type = PathType.CLOUD_STORAGE

                    break

        # Set default provider if not detected
        if not result.cloud_provider:
            result.cloud_provider = CloudProvider.UNKNOWN_CLOUD

        # Set resolved path to original path
        result.resolved_path = path


class SpecialPathAnalyzer(BasePathAnalyzer):
    """Analyzer for special path formats and conventions."""

    # Patterns for special paths
    SPECIAL_PATTERNS: ClassVar[dict[str, str]] = {
        "git_repo": r"^git@([^:]+):([^/]+)/([^/]+)(?:.git)?$",
        "ssh_path": r"^([^@]+)@([^:]+):(.+)$",
        "network_share": r"^\\\\([^\\]+)\\(.+)$",
    }

    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        # Check for special path patterns
        return any(re.match(pattern, path) for pattern in self.SPECIAL_PATTERNS.values())

    def analyze(self, path: str, result: PathAnalysisResult) -> None:
        """Analyze a special path and update the result object."""
        result.path_type = PathType.SPECIAL_PATH
        result.is_remote = True

        # Check for Git SSH URLs
        git_match = re.match(self.SPECIAL_PATTERNS["git_repo"], path)
        if git_match:
            host, user, repo = git_match.groups()

            # Set as GitHub if host is github.com
            if host == "github.com":
                # Create URL components
                components = URLComponents(
                    scheme="https",
                    netloc="github.com",
                    path=f"/{user}/{repo}",
                    hostname="github.com",
                    is_secure=True
                )

                # Create domain info
                domain_info = DomainInfo(
                    domain="github.com",
                    subdomain="",
                    second_level_domain="github",
                    top_level_domain="com",
                    is_well_known=True,
                    service_type="code_repository"
                )

                result.url_components = components
                result.domain_info = domain_info

                # Set repository info
                result.is_directory = True
                result.filename = repo

            # Return early as we've handled this case
            return

        # Check for SSH paths
        ssh_match = re.match(self.SPECIAL_PATTERNS["ssh_path"], path)
        if ssh_match:
            user, host, remote_path = ssh_match.groups()

            # Create URL components
            components = URLComponents(
                scheme="ssh",
                netloc=f"{user}@{host}",
                path=remote_path,
                hostname=host,
                is_secure=True
            )

            result.url_components = components

            # Try to determine if path is file or directory
            if "." in remote_path.split("/")[-1]:
                result.is_file = True
                result.filename = remote_path.split("/")[-1]

                # Check for file extension
                if "." in result.filename:
                    result.file_extension = "." + result.filename.split(".")[-1].lower()

                    # Try to determine file type from extension
                    if result.file_extension in LocalPathAnalyzer.EXTENSION_CATEGORIES:
                        category, specific_type = LocalPathAnalyzer.EXTENSION_CATEGORIES[result.file_extension]
                        result.file_category = category
                        result.specific_file_type = str(specific_type)
            else:
                result.is_directory = True

            # Return early as we've handled this case
            return

        # Check for Windows network shares
        network_match = re.match(self.SPECIAL_PATTERNS["network_share"], path)
        if network_match:
            host, share_path = network_match.groups()

            result.path_type = PathType.NETWORK_SHARE

            # Create URL components
            components = URLComponents(
                scheme="file",
                netloc=host,
                path=f"/{share_path.replace('\\', '/')}",
                hostname=host,
                is_secure=False,
                is_local_network=True
            )

            result.url_components = components

            # Try to determine if path is file or directory
            if "." in share_path.split("\\")[-1]:
                result.is_file = True
                result.filename = share_path.split("\\")[-1]

                # Check for file extension
                if "." in result.filename:
                    result.file_extension = "." + result.filename.split(".")[-1].lower()

                    # Try to determine file type from extension
                    if result.file_extension in LocalPathAnalyzer.EXTENSION_CATEGORIES:
                        category, specific_type = LocalPathAnalyzer.EXTENSION_CATEGORIES[result.file_extension]
                        result.file_category = category
                        result.specific_file_type = str(specific_type)
            else:
                result.is_directory = True

            # Return early as we've handled this case
            return


# ============================================================================
# MAIN ANALYZER FUNCTION
# ============================================================================

def analyze_path_comprehensive(path_input: str | Path) -> PathAnalysisResult:
    """Comprehensively analyze a path or URL to determine its nature, type, and properties.

    This function is the primary entry point for path analysis, utilizing various
    specialized analyzers to determine the path's characteristics.

    Args:
        path_input: The path or URL to analyze

    Returns:
        PathAnalysisResult: Comprehensive analysis result
    """
    # Convert input to string for consistent processing
    original_path = str(path_input)

    # Initialize result object
    result = PathAnalysisResult(original_path=original_path)

    # Available analyzers in order of priority
    analyzers = [
        DatabaseURIAnalyzer(),
        CloudStorageAnalyzer(),
        URLAnalyzer(),
        SpecialPathAnalyzer(),
        LocalPathAnalyzer(),  # Should be last as it's most permissive
    ]

    # Find the appropriate analyzer
    analyzer_found = False
    for analyzer in analyzers:
        if analyzer.can_analyze(original_path):
            try:
                analyzer.analyze(original_path, result)
                analyzer_found = True
                break
            except Exception as e:
                result.analysis_errors.append(f"Analyzer {analyzer.__class__.__name__} failed: {e!s}")

    if not analyzer_found:
        result.analysis_errors.append("No suitable analyzer found for this path")
        result.path_type = PathType.UNKNOWN

    return result


# ============================================================================
# SIMPLIFIED INTERFACE FOR DOCUMENT LOADER ENGINE
# ============================================================================

def analyze_path(path: str | Path) -> PathAnalysisResult:
    """Analyze a path to determine its type, properties, and metadata.

    This function is a simplified wrapper around analyze_path_comprehensive that
    provides a convenient interface for the document loader engine.

    Args:
        path: The path, URL, or source identifier to analyze

    Returns:
        PathAnalysisResult containing the analysis results

    Examples:
        >>> result = analyze_path("/path/to/document.pdf")
        >>> print(result.path_type)  # PathType.LOCAL_FILE
        >>> print(result.mime_type)  # "application/pdf"

        >>> result = analyze_path("https://example.com/page.html")
        >>> print(result.path_type)  # PathType.URL_HTTPS
        >>> print(result.is_remote)  # True
    """
    return analyze_path_comprehensive(path)


def detect_mime_type(file_path: str) -> str | None:
    """Detect the MIME type of a file.

    Args:
        file_path: Path to the file

    Returns:
        Optional[str]: MIME type or None if it can't be determined
    """
    # Try using mimetypes first (standard library)
    mime_type, _ = mimetypes.guess_type(file_path)

    # If that fails, try python-magic if available
    if not mime_type:
        try:
            import magic
            mime_type = magic.from_file(file_path, mime=True)
        except ImportError:
            pass

    return mime_type


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary.

    Args:
        file_path: Path to the file

    Returns:
        bool: True if the file is binary, False otherwise
    """
    mime_type = detect_mime_type(file_path)

    # Check MIME type
    if mime_type:
        # Text types
        if mime_type.startswith(("text/", "application/json", "application/xml")):
            return False

        # Binary types
        if mime_type.startswith(("application/", "image/", "video/", "audio/")):
            return True

    # Fallback: check file content
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            return b"\0" in chunk
    except Exception:
        # If we can't open the file, assume it's binary
        return True


def get_file_encoding(file_path: str) -> str:
    """Guess the encoding of a text file.

    Args:
        file_path: Path to the file

    Returns:
        str: Detected encoding or 'utf-8' as fallback
    """
    try:
        import chardet

        # Read a chunk of the file
        with open(file_path, "rb") as f:
            chunk = f.read(4096)

        # Detect encoding
        result = chardet.detect(chunk)
        if result and result["encoding"] and result["confidence"] > 0.5:
            return result["encoding"]
    except ImportError:
        pass

    # Default to UTF-8
    return "utf-8"
