"""Path Analysis System for Document Loader Engine.

This module provides a path analysis system for the document loader engine,
which analyzes paths and URLs to determine their nature and properties.
"""

import logging
import mimetypes
import os
import re
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union
from urllib.parse import urlparse, urlunparse

from pydantic import BaseModel, Field, computed_field

logger = logging.getLogger(__name__)


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


class URLComponents(BaseModel):
    """Components of a URL."""

    scheme: str = ""
    netloc: str = ""
    hostname: str = ""
    port: int | None = None
    path: str = ""
    params: str = ""
    query: str = ""
    fragment: str = ""
    username: str | None = None
    password: str | None = None


class DomainInfo(BaseModel):
    """Information about a domain."""

    domain: str = ""
    tld: str = ""
    subdomain: str = ""
    is_ip: bool = False
    is_localhost: bool = False


class PathAnalysisResult(BaseModel):
    """Result of path analysis.

    This model contains comprehensive information about a path, including its type,
    properties, and metadata.
    """

    # Original input
    original_path: str = Field(
        ..., description="Original path string eqthat was analyzed"
    )

    # Primary classification
    path_type: PathType = Field(
        default=PathType.UNKNOWN, description="Primary path type classification"
    )

    # Basic properties
    is_local: bool = Field(
        default=False, description="Whether the path is on the local filesystem"
    )
    is_remote: bool = Field(
        default=False, description="Whether the path is remote (URL, cloud, etc.)"
    )
    is_file: bool = Field(default=False, description="Whether the path is a file")
    is_directory: bool = Field(
        default=False, description="Whether the path is a directory"
    )
    is_symlink: bool = Field(
        default=False, description="Whether the path is a symbolic link"
    )
    exists: bool = Field(default=False, description="Whether the path exists")

    # Path components
    normalized_path: str | None = Field(
        default=None, description="Normalized version of the path"
    )
    parent_path: str | None = Field(
        default=None, description="Parent directory of the path"
    )
    file_name: str | None = Field(default=None, description="File name (if applicable)")
    file_extension: str | None = Field(
        default=None, description="File extension (if applicable)"
    )

    # File properties
    file_size: int | None = Field(
        default=None, description="File size in bytes (if available)"
    )
    mime_type: str | None = Field(default=None, description="MIME type (if available)")
    encoding: str | None = Field(
        default=None, description="File encoding (if available)"
    )

    # Categorization
    file_category: FileCategory | None = Field(
        default=None, description="High-level file category"
    )

    # URL-specific properties
    url_components: URLComponents | None = Field(
        default=None, description="Components of the URL (if applicable)"
    )
    domain_info: DomainInfo | None = Field(
        default=None, description="Domain information (if applicable)"
    )

    # Database-specific properties
    database_type: DatabaseType | None = Field(
        default=None, description="Database type (if applicable)"
    )
    database_name: str | None = Field(
        default=None, description="Database name (if applicable)"
    )

    # Cloud storage properties
    cloud_provider: CloudProvider | None = Field(
        default=None, description="Cloud storage provider (if applicable)"
    )
    bucket_name: str | None = Field(
        default=None, description="Bucket name (if applicable)"
    )
    object_key: str | None = Field(
        default=None, description="Object key (if applicable)"
    )

    # Network properties
    is_secure: bool | None = Field(
        default=None, description="Whether the connection is secure (https, sftp, etc.)"
    )

    @computed_field
    def source_summary(self) -> str:
        """Generate a summary of the source."""
        if self.path_type in [PathType.LOCAL_FILE, PathType.LOCAL_DIRECTORY]:
            return f"Local {'directory' if self.is_directory else 'file'}: {self.original_path}"
        if self.path_type in [PathType.URL_HTTP, PathType.URL_HTTPS]:
            domain = self.domain_info.domain if self.domain_info else "unknown"
            return f"Web URL ({domain}): {self.original_path}"
        if self.path_type == PathType.DATABASE_URI:
            return f"Database ({self.database_type}): {self.original_path}"
        if self.path_type == PathType.CLOUD_STORAGE:
            return f"Cloud storage ({self.cloud_provider}): {self.original_path}"
        return f"Unknown source: {self.original_path}"


# File extension to MIME type mappings (in addition to standard ones)
EXTRA_MIME_TYPES = {
    ".md": "text/markdown",
    ".ipynb": "application/x-ipynb+json",
    ".yaml": "application/x-yaml",
    ".yml": "application/x-yaml",
    ".toml": "application/toml",
    ".rst": "text/x-rst",
    ".epub": "application/epub+zip",
}

# File extension to category mappings
FILE_CATEGORY_MAP = {
    # Documents
    ".pdf": FileCategory.DOCUMENT,
    ".doc": FileCategory.DOCUMENT,
    ".docx": FileCategory.DOCUMENT,
    ".odt": FileCategory.DOCUMENT,
    ".rtf": FileCategory.DOCUMENT,
    ".epub": FileCategory.DOCUMENT,
    ".md": FileCategory.DOCUMENT,
    ".markdown": FileCategory.DOCUMENT,
    ".rst": FileCategory.DOCUMENT,
    ".txt": FileCategory.TEXT,
    ".html": FileCategory.TEXT,
    ".htm": FileCategory.TEXT,
    # Data formats
    ".csv": FileCategory.DATA,
    ".json": FileCategory.DATA,
    ".xml": FileCategory.DATA,
    ".yaml": FileCategory.DATA,
    ".yml": FileCategory.DATA,
    ".toml": FileCategory.DATA,
    ".ini": FileCategory.DATA,
    ".conf": FileCategory.DATA,
    ".sqlite": FileCategory.DATA,
    ".db": FileCategory.DATA,
    ".xlsx": FileCategory.DATA,
    ".xls": FileCategory.DATA,
    ".ods": FileCategory.DATA,
    # Code
    ".py": FileCategory.CODE,
    ".js": FileCategory.CODE,
    ".ts": FileCategory.CODE,
    ".java": FileCategory.CODE,
    ".c": FileCategory.CODE,
    ".cpp": FileCategory.CODE,
    ".cs": FileCategory.CODE,
    ".go": FileCategory.CODE,
    ".rs": FileCategory.CODE,
    ".rb": FileCategory.CODE,
    ".php": FileCategory.CODE,
    ".ipynb": FileCategory.CODE,
    # Images
    ".jpg": FileCategory.IMAGE,
    ".jpeg": FileCategory.IMAGE,
    ".png": FileCategory.IMAGE,
    ".gif": FileCategory.IMAGE,
    ".bmp": FileCategory.IMAGE,
    ".tiff": FileCategory.IMAGE,
    ".webp": FileCategory.IMAGE,
    ".svg": FileCategory.IMAGE,
    ".ico": FileCategory.IMAGE,
    # Video
    ".mp4": FileCategory.VIDEO,
    ".avi": FileCategory.VIDEO,
    ".mov": FileCategory.VIDEO,
    ".mkv": FileCategory.VIDEO,
    ".webm": FileCategory.VIDEO,
    ".wmv": FileCategory.VIDEO,
    ".flv": FileCategory.VIDEO,
    # Audio
    ".mp3": FileCategory.AUDIO,
    ".wav": FileCategory.AUDIO,
    ".ogg": FileCategory.AUDIO,
    ".flac": FileCategory.AUDIO,
    ".aac": FileCategory.AUDIO,
    ".m4a": FileCategory.AUDIO,
    # Archives
    ".zip": FileCategory.ARCHIVE,
    ".tar": FileCategory.ARCHIVE,
    ".gz": FileCategory.ARCHIVE,
    ".7z": FileCategory.ARCHIVE,
    ".rar": FileCategory.ARCHIVE,
    ".bz2": FileCategory.ARCHIVE,
    ".xz": FileCategory.ARCHIVE,
    # Executables
    ".exe": FileCategory.EXECUTABLE,
    ".app": FileCategory.EXECUTABLE,
    ".bin": FileCategory.EXECUTABLE,
    ".sh": FileCategory.EXECUTABLE,
    ".bat": FileCategory.EXECUTABLE,
    ".dll": FileCategory.EXECUTABLE,
    ".so": FileCategory.EXECUTABLE,
    # Fonts
    ".ttf": FileCategory.FONT,
    ".otf": FileCategory.FONT,
    ".woff": FileCategory.FONT,
    ".woff2": FileCategory.FONT,
    ".eot": FileCategory.FONT,
    # Models
    ".onnx": FileCategory.MODEL,
    ".pkl": FileCategory.MODEL,
    ".h5": FileCategory.MODEL,
    ".pth": FileCategory.MODEL,
    ".pt": FileCategory.MODEL,
    ".pb": FileCategory.MODEL,
    ".tflite": FileCategory.MODEL,
    # System files
    ".sys": FileCategory.SYSTEM,
    ".log": FileCategory.SYSTEM,
    ".tmp": FileCategory.SYSTEM,
    ".bak": FileCategory.SYSTEM,
    ".cache": FileCategory.SYSTEM,
    ".config": FileCategory.SYSTEM,
}

# Database URI patterns
DATABASE_URI_PATTERNS = {
    r"^postgresql://": DatabaseType.POSTGRESQL,
    r"^postgres://": DatabaseType.POSTGRESQL,
    r"^mysql://": DatabaseType.MYSQL,
    r"^mariadb://": DatabaseType.MYSQL,
    r"^sqlite://": DatabaseType.SQLITE,
    r"^mongodb://": DatabaseType.MONGODB,
    r"^mongodb\+srv://": DatabaseType.MONGODB,
    r"^redis://": DatabaseType.REDIS,
    r"^oracle://": DatabaseType.ORACLE,
    r"^mssql://": DatabaseType.MSSQL,
    r"^sqlserver://": DatabaseType.MSSQL,
    r"^cassandra://": DatabaseType.CASSANDRA,
    r"^elasticsearch://": DatabaseType.ELASTICSEARCH,
    r"^clickhouse://": DatabaseType.CLICKHOUSE,
    r"^snowflake://": DatabaseType.SNOWFLAKE,
    r"^bigquery://": DatabaseType.BIGQUERY,
    r"^dynamodb://": DatabaseType.DYNAMODB,
    r"^couchdb://": DatabaseType.COUCHDB,
    r"^influxdb://": DatabaseType.INFLUXDB,
}

# Cloud storage patterns
CLOUD_STORAGE_PATTERNS = {
    r"^s3://": CloudProvider.AWS_S3,
    r"^s3a://": CloudProvider.AWS_S3,
    r"^s3n://": CloudProvider.AWS_S3,
    r"^azure://": CloudProvider.AZURE_BLOB,
    r"^wasb://": CloudProvider.AZURE_BLOB,
    r"^wasbs://": CloudProvider.AZURE_BLOB,
    r"^adl://": CloudProvider.AZURE_BLOB,
    r"^gs://": CloudProvider.GOOGLE_CLOUD,
    r"^gcs://": CloudProvider.GOOGLE_CLOUD,
    r"^dropbox://": CloudProvider.DROPBOX,
    r"^box://": CloudProvider.BOX,
    r"^onedrive://": CloudProvider.ONEDRIVE,
    r"^icloud://": CloudProvider.ICLOUD,
    r"^b2://": CloudProvider.BACKBLAZE,
}


def detect_mime_type(file_path: str) -> str | None:
    """Detect the MIME type of a file.

    Args:
        file_path: Path to the file

    Returns:
        MIME type string, or None if unable to determine
    """
    # Register additional MIME types
    for ext, mime_type in EXTRA_MIME_TYPES.items():
        mimetypes.add_type(mime_type, ext)

    # Get MIME type from file extension
    mime_type, _ = mimetypes.guess_type(file_path)

    # If not found and file exists, try to detect from content
    if mime_type is None and os.path.exists(file_path):
        try:
            import magic

            mime_type = magic.from_file(file_path, mime=True)
        except (ImportError, Exception):
            # python-magic not available or error
            pass

    return mime_type


def is_binary_file(file_path: str) -> bool:
    """Check if a file is binary.

    Args:
        file_path: Path to the file

    Returns:
        True if the file is binary, False otherwise
    """
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return False

    # Check file extension first
    _, ext = os.path.splitext(file_path)
    if ext.lower() in [
        ".pdf",
        ".docx",
        ".xlsx",
        ".pptx",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".zip",
        ".tar",
        ".gz",
        ".mp3",
        ".mp4",
        ".exe",
    ]:
        return True

    # Check MIME type
    mime_type = detect_mime_type(file_path)
    if mime_type and not mime_type.startswith(
        ("text/", "application/json", "application/xml")
    ):
        return True

    # Check content (first few KB)
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(4096)
            if b"\x00" in chunk:  # Null bytes indicate binary
                return True

            # Try to decode as text
            try:
                chunk.decode("utf-8")
                return False
            except UnicodeDecodeError:
                return True
    except (OSError, Exception):
        # If we can't read the file, assume it's not binary
        pass

    return False


def detect_encoding(file_path: str) -> str | None:
    """Detect the encoding of a text file.

    Args:
        file_path: Path to the file

    Returns:
        Encoding name, or None if unable to determine
    """
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        return None

    if is_binary_file(file_path):
        return None

    try:
        import chardet

        with open(file_path, "rb") as f:
            result = chardet.detect(f.read(4096))
        return result["encoding"] if result["confidence"] > 0.7 else None
    except (ImportError, Exception):
        # chardet not available or error
        pass

    # Default to UTF-8
    return "utf-8"


def extract_url_components(url: str) -> URLComponents:
    """Extract components from a URL.

    Args:
        url: URL string

    Returns:
        URLComponents object
    """
    if not url:
        return URLComponents()

    try:
        parsed = urlparse(url)

        # Extract hostname and port
        hostname = parsed.hostname or ""
        port = parsed.port

        return URLComponents(
            scheme=parsed.scheme,
            netloc=parsed.netloc,
            hostname=hostname,
            port=port,
            path=parsed.path,
            params=parsed.params,
            query=parsed.query,
            fragment=parsed.fragment,
            username=parsed.username,
            password=parsed.password,
        )
    except Exception:
        return URLComponents()


def extract_domain_info(url_components: URLComponents) -> DomainInfo:
    """Extract domain information from URL components.

    Args:
        url_components: URLComponents object

    Returns:
        DomainInfo object
    """
    hostname = url_components.hostname or ""

    # Check if it's an IP address
    is_ip = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", hostname) is not None

    # Check if it's localhost
    is_localhost = hostname in ["localhost", "127.0.0.1", "::1"]

    # Extract domain and subdomain
    if is_ip or is_localhost:
        domain = hostname
        tld = ""
        subdomain = ""
    else:
        parts = hostname.split(".")

        # Handle cases like example.com, www.example.com, sub.example.com
        if len(parts) == 1:
            domain = parts[0]
            tld = ""
            subdomain = ""
        elif len(parts) == 2:
            domain = f"{parts[0]}.{parts[1]}"
            tld = parts[1]
            subdomain = ""
        else:
            tld = parts[-1]
            domain = f"{parts[-2]}.{parts[-1]}"
            subdomain = ".".join(parts[:-2])

    return DomainInfo(
        domain=domain,
        tld=tld,
        subdomain=subdomain,
        is_ip=is_ip,
        is_localhost=is_localhost,
    )


def extract_database_info(uri: str, db_type: DatabaseType) -> dict[str, Any]:
    """Extract database information from a URI.

    Args:
        uri: Database URI
        db_type: Database type

    Returns:
        Dictionary with database information
    """
    components = extract_url_components(uri)
    info = {"database_type": db_type, "connection_uri": uri}

    # Extract database name from path
    if components.path and components.path != "/":
        db_name = components.path.lstrip("/")
        if db_name:
            info["database_name"] = db_name

    # Extract host and port
    if components.hostname:
        info["host"] = components.hostname
    if components.port:
        info["port"] = components.port

    # Extract credentials
    if components.username:
        info["username"] = components.username

    return info


def extract_cloud_storage_info(uri: str, provider: CloudProvider) -> dict[str, Any]:
    """Extract cloud storage information from a URI.

    Args:
        uri: Cloud storage URI
        provider: Cloud provider

    Returns:
        Dictionary with cloud storage information
    """
    info = {"cloud_provider": provider, "uri": uri}

    # Parse URI to extract bucket and key
    parts = uri.split("://", 1)[1].split("/", 1)

    if parts:
        info["bucket_name"] = parts[0]
        if len(parts) > 1:
            info["object_key"] = parts[1]

    return info


def analyze_local_path(path: str) -> PathAnalysisResult:
    """Analyze a local filesystem path.

    Args:
        path: Path to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(
        original_path=path,
        is_local=True,
        normalized_path=os.path.normpath(path),
        parent_path=os.path.dirname(path),
    )

    # Check if path exists
    if os.path.exists(path):
        result.exists = True

        # Check if it's a symlink
        if os.path.islink(path):
            result.path_type = PathType.LOCAL_SYMLINK
            result.is_symlink = True

            # Determine if the target is a file or directory
            target_path = os.path.realpath(path)
            if os.path.isfile(target_path):
                result.is_file = True
            elif os.path.isdir(target_path):
                result.is_directory = True

        # Check if it's a file
        elif os.path.isfile(path):
            result.path_type = PathType.LOCAL_FILE
            result.is_file = True
            result.file_name = os.path.basename(path)

            # Get file extension
            _, ext = os.path.splitext(path)
            if ext:
                result.file_extension = ext.lower()

                # Get file category
                result.file_category = FILE_CATEGORY_MAP.get(
                    ext.lower(), FileCategory.UNKNOWN_FILE
                )

            # Get file size
            try:
                result.file_size = os.path.getsize(path)
            except (OSError, Exception):
                pass

            # Get MIME type
            result.mime_type = detect_mime_type(path)

            # Get encoding for text files
            if not is_binary_file(path):
                result.encoding = detect_encoding(path)

        # Check if it's a directory
        elif os.path.isdir(path):
            result.path_type = PathType.LOCAL_DIRECTORY
            result.is_directory = True
            result.file_name = os.path.basename(path)
    else:
        result.path_type = PathType.LOCAL_NONEXISTENT

    return result


def analyze_url(url: str) -> PathAnalysisResult:
    """Analyze a URL.

    Args:
        url: URL to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(original_path=url, is_remote=True)

    # Extract URL components
    components = extract_url_components(url)
    result.url_components = components

    # Extract domain information
    if components.hostname:
        result.domain_info = extract_domain_info(components)

    # Set URL-specific properties
    scheme = components.scheme.lower()

    if scheme == "http":
        result.path_type = PathType.URL_HTTP
        result.is_secure = False
    elif scheme == "https":
        result.path_type = PathType.URL_HTTPS
        result.is_secure = True
    elif scheme in ["ftp", "sftp"]:
        result.path_type = PathType.URL_FTP
        result.is_secure = scheme == "sftp"
    elif scheme == "file":
        result.path_type = PathType.URL_FILE
        result.is_local = True
        # Convert to local path for further analysis
        local_path = components.path
        local_result = analyze_local_path(local_path)

        # Copy relevant properties
        result.is_file = local_result.is_file
        result.is_directory = local_result.is_directory
        result.exists = local_result.exists
        result.file_name = local_result.file_name
        result.file_extension = local_result.file_extension
        result.file_category = local_result.file_category
        result.file_size = local_result.file_size
        result.mime_type = local_result.mime_type
        result.encoding = local_result.encoding

    # Extract file information from path
    if components.path and components.path != "/":
        file_path = components.path.rstrip("/")
        file_name = os.path.basename(file_path)
        if file_name:
            result.file_name = file_name

            # Get file extension
            _, ext = os.path.splitext(file_name)
            if ext:
                result.file_extension = ext.lower()

                # Get file category
                result.file_category = FILE_CATEGORY_MAP.get(
                    ext.lower(), FileCategory.UNKNOWN_FILE
                )

                # Assume it's a file if it has an extension
                result.is_file = True

    return result


def analyze_database_uri(uri: str) -> PathAnalysisResult:
    """Analyze a database URI.

    Args:
        uri: Database URI to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(
        original_path=uri, path_type=PathType.DATABASE_URI, is_remote=True
    )

    # Extract URL components
    components = extract_url_components(uri)
    result.url_components = components

    # Determine database type
    db_type = DatabaseType.UNKNOWN_DB
    for pattern, db in DATABASE_URI_PATTERNS.items():
        if re.match(pattern, uri):
            db_type = db
            break

    result.database_type = db_type

    # Extract database name from path
    if components.path and components.path != "/":
        db_name = components.path.lstrip("/")
        if db_name:
            result.database_name = db_name

    return result


def analyze_cloud_path(path: str) -> PathAnalysisResult:
    """Analyze a cloud storage path.

    Args:
        path: Cloud storage path to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(
        original_path=path, path_type=PathType.CLOUD_STORAGE, is_remote=True
    )

    # Determine cloud provider
    provider = CloudProvider.UNKNOWN_CLOUD
    for pattern, prov in CLOUD_STORAGE_PATTERNS.items():
        if re.match(pattern, path):
            provider = prov
            break

    result.cloud_provider = provider

    # Parse path to extract bucket and key
    try:
        scheme, rest = path.split("://", 1)
        parts = rest.split("/", 1)

        if parts:
            result.bucket_name = parts[0]
            if len(parts) > 1:
                result.object_key = parts[1]

                # Determine if it's a file or directory
                if result.object_key.endswith("/"):
                    result.is_directory = True
                else:
                    result.is_file = True

                    # Extract file name and extension
                    result.file_name = os.path.basename(result.object_key)
                    _, ext = os.path.splitext(result.file_name)
                    if ext:
                        result.file_extension = ext.lower()

                        # Get file category
                        result.file_category = FILE_CATEGORY_MAP.get(
                            ext.lower(), FileCategory.UNKNOWN_FILE
                        )
    except Exception:
        # Unable to parse, leave properties as defaults
        pass

    return result


def analyze_network_path(path: str) -> PathAnalysisResult:
    """Analyze a network share path.

    Args:
        path: Network path to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(
        original_path=path, path_type=PathType.NETWORK_SHARE, is_remote=True
    )

    # Parse UNC path (\\server\share\path)
    if path.startswith("\\\\"):
        parts = path.lstrip("\\").split("\\")

        if len(parts) >= 2:
            server = parts[0]
            share = parts[1]

            # Store in URL components
            result.url_components = URLComponents(
                scheme="file",
                netloc=server,
                hostname=server,
                path=f"/{share}/{'/'.join(parts[2:]) if len(parts) > 2 else ''}",
            )

    # Determine if it's a file or directory
    if path.endswith(("\\", "/")):
        result.is_directory = True
    else:
        # Check file extension
        _, ext = os.path.splitext(path)
        if ext:
            result.is_file = True
            result.file_extension = ext.lower()
            result.file_name = os.path.basename(path)

            # Get file category
            result.file_category = FILE_CATEGORY_MAP.get(
                ext.lower(), FileCategory.UNKNOWN_FILE
            )

    return result


def analyze_special_path(path: str) -> PathAnalysisResult:
    """Analyze a special path (e.g., git SSH URL).

    Args:
        path: Special path to analyze

    Returns:
        PathAnalysisResult object
    """
    # Basic result with common properties
    result = PathAnalysisResult(
        original_path=path, path_type=PathType.SPECIAL_PATH, is_remote=True
    )

    # Handle git SSH URLs (git@github.com:user/repo.git)
    if re.match(r"^git@[a-zA-Z0-9.-]+:[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+\.git$", path):
        # Parse git SSH URL
        user_host, repo_path = path.split(":", 1)
        user, host = user_host.split("@", 1)

        # Store in URL components
        result.url_components = URLComponents(
            scheme="ssh",
            netloc=host,
            hostname=host,
            username=user,
            path=f"/{repo_path}",
        )

        # Store in domain info
        result.domain_info = extract_domain_info(result.url_components)

        # It's a Git repository
        result.is_file = False
        result.is_directory = True

    return result


def analyze_path_comprehensive(path: str | Path) -> PathAnalysisResult:
    """Analyze a path comprehensively.

    This function analyzes a path to determine its type, properties, and metadata.
    It handles various path types including local files, URLs, database URIs, and
    cloud storage paths.

    Args:
        path: Path to analyze (string or Path object)

    Returns:
        PathAnalysisResult object with comprehensive information about the path
    """
    # Convert Path to string
    if isinstance(path, Path):
        path = str(path)

    # Normalize path
    path = path.strip()

    # Handle empty path
    if not path:
        return PathAnalysisResult(original_path="", path_type=PathType.UNKNOWN)

    # Check for URL
    if re.match(r"^(https?|ftp|sftp|file)://", path):
        return analyze_url(path)

    # Check for database URI
    for pattern in DATABASE_URI_PATTERNS:
        if re.match(pattern, path):
            return analyze_database_uri(path)

    # Check for cloud storage path
    for pattern in CLOUD_STORAGE_PATTERNS:
        if re.match(pattern, path):
            return analyze_cloud_path(path)

    # Check for network share (UNC path)
    if path.startswith("\\\\"):
        return analyze_network_path(path)

    # Check for special paths (like git SSH URLs)
    if re.match(r"^git@[a-zA-Z0-9.-]+:", path):
        return analyze_special_path(path)

    # Default to local path
    return analyze_local_path(path)


__all__ = [
    "CloudProvider",
    "DatabaseType",
    "DomainInfo",
    "FileCategory",
    "PathAnalysisResult",
    "PathType",
    "URLComponents",
    "analyze_cloud_path",
    "analyze_database_uri",
    "analyze_local_path",
    "analyze_network_path",
    "analyze_path_comprehensive",
    "analyze_special_path",
    "analyze_url",
    "detect_encoding",
    "detect_mime_type",
    "extract_domain_info",
    "extract_url_components",
    "is_binary_file",
]
