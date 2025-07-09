"""
Comprehensive Path/URL Analysis Module for Haive Framework

This module provides a robust analysis system that determines the nature, type,
and properties of various path and URL inputs using Pydantic v2, typing, urllib, and pathlib.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum

# ============================================================================
# COMPREHENSIVE FILE TYPE ENUMS
# ============================================================================


class DocumentType(str, Enum):
    """Document file types."""

    # PDF
    PDF = "pdf"

    # Microsoft Office
    DOC = "doc"
    DOCX = "docx"
    DOT = "dot"
    DOTX = "dotx"
    XLS = "xls"
    XLSX = "xlsx"
    XLT = "xlt"
    XLTX = "xltx"
    PPT = "ppt"
    PPTX = "pptx"
    PPS = "pps"
    PPSX = "ppsx"

    # LibreOffice/OpenOffice
    ODT = "odt"
    ODS = "ods"
    ODP = "odp"
    ODG = "odg"
    ODF = "odf"

    # Rich Text/Text Processing
    RTF = "rtf"
    TEX = "tex"
    LATEX = "latex"

    # E-book formats
    EPUB = "epub"
    MOBI = "mobi"
    AZW = "azw"
    AZW3 = "azw3"

    # Other document formats
    PAGES = "pages"
    NUMBERS = "numbers"
    KEYNOTE = "keynote"


class ImageType(str, Enum):
    """Image file types."""

    # Common raster formats
    JPEG = "jpeg"
    JPG = "jpg"
    PNG = "png"
    GIF = "gif"
    BMP = "bmp"
    WEBP = "webp"

    # High-quality/professional formats
    TIFF = "tiff"
    TIF = "tif"
    RAW = "raw"
    NEF = "nef"  # Nikon
    CR2 = "cr2"  # Canon
    ARW = "arw"  # Sony
    DNG = "dng"  # Adobe Digital Negative

    # Vector formats
    SVG = "svg"
    AI = "ai"  # Adobe Illustrator
    EPS = "eps"
    PS = "ps"

    # Other formats
    ICO = "ico"
    ICNS = "icns"
    PSD = "psd"  # Photoshop
    XCF = "xcf"  # GIMP
    SKETCH = "sketch"
    FIGMA = "figma"


class VideoType(str, Enum):
    """Video file types."""

    # Common formats
    MP4 = "mp4"
    AVI = "avi"
    MKV = "mkv"
    MOV = "mov"
    WMV = "wmv"
    FLV = "flv"
    WEBM = "webm"

    # Professional/broadcast formats
    MPG = "mpg"
    MPEG = "mpeg"
    M4V = "m4v"
    M2V = "m2v"
    VOB = "vob"
    ASF = "asf"

    # High-quality formats
    MXF = "mxf"
    PRORES = "prores"
    AVCHD = "avchd"

    # Streaming formats
    M3U8 = "m3u8"
    TS = "ts"
    F4V = "f4v"

    # Other formats
    OGV = "ogv"
    DIVX = "divx"
    XVID = "xvid"
    RMVB = "rmvb"
    THREE_GP = "3gp"
    THREE_G2 = "3g2"


class AudioType(str, Enum):
    """Audio file types."""

    # Lossless formats
    FLAC = "flac"
    ALAC = "alac"
    APE = "ape"
    WAV = "wav"
    AIFF = "aiff"
    AU = "au"

    # Lossy compressed formats
    MP3 = "mp3"
    AAC = "aac"
    OGG = "ogg"
    VORBIS = "vorbis"
    WMA = "wma"
    OPUS = "opus"

    # Professional formats
    BWF = "bwf"
    RF64 = "rf64"

    # Other formats
    M4A = "m4a"
    M4P = "m4p"
    M4B = "m4b"  # Audiobook
    RA = "ra"  # RealAudio
    AMR = "amr"
    MID = "mid"  # MIDI
    MIDI = "midi"


class CodeType(str, Enum):
    """Code and markup file types."""

    # Python
    PY = "py"
    PYC = "pyc"
    PYO = "pyo"
    PYW = "pyw"
    PYNB = "ipynb"  # Jupyter notebook

    # JavaScript/TypeScript
    JS = "js"
    TS = "ts"
    JSX = "jsx"
    TSX = "tsx"
    MJS = "mjs"
    CJS = "cjs"

    # Web technologies
    HTML = "html"
    HTM = "htm"
    CSS = "css"
    SCSS = "scss"
    SASS = "sass"
    LESS = "less"

    # Java
    JAVA = "java"
    CLASS = "class"
    JAR = "jar"
    WAR = "war"

    # C/C++
    C = "c"
    CPP = "cpp"
    CXX = "cxx"
    CC = "cc"
    H = "h"
    HPP = "hpp"
    HXX = "hxx"

    # C#/.NET
    CS = "cs"
    VB = "vb"
    FS = "fs"  # F#

    # Other compiled languages
    GO = "go"
    RUST = "rs"
    SWIFT = "swift"
    KOTLIN = "kt"
    SCALA = "scala"

    # Scripting languages
    PHP = "php"
    RB = "rb"  # Ruby
    PL = "pl"  # Perl
    LUA = "lua"
    R = "r"
    JULIA = "jl"

    # Functional languages
    HS = "hs"  # Haskell
    ML = "ml"
    ELM = "elm"
    CLOJURE = "clj"
    LISP = "lisp"
    SCHEME = "scm"

    # Assembly
    ASM = "asm"
    S = "s"

    # SQL
    SQL = "sql"

    # Shell scripts
    SH = "sh"
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    PS1 = "ps1"  # PowerShell
    BAT = "bat"
    CMD = "cmd"


class DataType(str, Enum):
    """Data and configuration file types."""

    # Structured data formats
    JSON = "json"
    XML = "xml"
    YAML = "yaml"
    YML = "yml"
    TOML = "toml"
    INI = "ini"
    CFG = "cfg"
    CONF = "conf"

    # Database formats
    SQLITE = "sqlite"
    SQLITE3 = "sqlite3"
    DB = "db"
    MDB = "mdb"  # Access
    ACCDB = "accdb"  # Access

    # Big data formats
    PARQUET = "parquet"
    ARROW = "arrow"
    AVRO = "avro"
    ORC = "orc"

    # Scientific data
    HDF5 = "hdf5"
    H5 = "h5"
    MAT = "mat"  # MATLAB
    NPY = "npy"  # NumPy
    NPZ = "npz"  # NumPy

    # Serialization formats
    PICKLE = "pkl"
    PICKLE_ALT = "pickle"
    MSGPACK = "msgpack"
    PROTOBUF = "proto"

    # Tabular data
    CSV = "csv"
    TSV = "tsv"
    XLS = "xls"  # Also in DocumentType
    XLSX = "xlsx"  # Also in DocumentType

    # Log files
    LOG = "log"
    OUT = "out"
    ERR = "err"

    # Backup files
    BAK = "bak"
    BACKUP = "backup"
    OLD = "old"


class ArchiveType(str, Enum):
    """Archive and compression file types."""

    # Common archives
    ZIP = "zip"
    RAR = "rar"
    SEVEN_Z = "7z"

    # Unix/Linux archives
    TAR = "tar"
    TAR_GZ = "tar.gz"
    TGZ = "tgz"
    TAR_BZ2 = "tar.bz2"
    TBZ2 = "tbz2"
    TAR_XZ = "tar.xz"
    TXZ = "txz"
    TAR_LZ = "tar.lz"
    TAR_LZMA = "tar.lzma"

    # Compression only
    GZ = "gz"
    BZ2 = "bz2"
    XZ = "xz"
    LZ = "lz"
    LZMA = "lzma"
    Z = "z"

    # Other archive formats
    CAB = "cab"  # Windows Cabinet
    MSI = "msi"  # Windows Installer
    DMG = "dmg"  # macOS Disk Image
    PKG = "pkg"  # macOS Package
    DEB = "deb"  # Debian Package
    RPM = "rpm"  # Red Hat Package
    APK = "apk"  # Android Package
    IPA = "ipa"  # iOS Package

    # Disk images
    ISO = "iso"
    IMG = "img"
    VHD = "vhd"
    VMDK = "vmdk"


class TextType(str, Enum):
    """Plain text and markup file types."""

    # Plain text
    TXT = "txt"
    TEXT = "text"

    # Markdown
    MD = "md"
    MARKDOWN = "markdown"

    # reStructuredText
    RST = "rst"

    # Other markup
    TEXTILE = "textile"
    ASCIIDOC = "adoc"
    ORG = "org"  # Org-mode

    # Documentation
    README = "readme"
    CHANGELOG = "changelog"
    LICENSE = "license"
    TODO = "todo"

    # Template files
    TEMPLATE = "template"
    TPL = "tpl"

    # Subtitle files
    SRT = "srt"
    VTT = "vtt"
    ASS = "ass"
    SSA = "ssa"


# ============================================================================
# BASE CLASSES AND PROTOCOLS
# ============================================================================


class BasePathAnalyzer(ABC):
    """Abstract base class for path analyzers."""

    @abstractmethod
    def can_analyze(self, path: str) -> bool:
        """Check if this analyzer can handle the given path."""
        pass

    @abstractmethod
    def analyze(self, path: str, result: "PathAnalysisResult") -> None:
        """Perform analysis and update the result object."""
        pass


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
