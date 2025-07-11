from enum import Enum


class ProgrammingLanguage(str, Enum):
    """Supported programming languages with common file extensions."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    KOTLIN = "kotlin"
    SWIFT = "swift"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    RUBY = "ruby"
    PHP = "php"
    GO = "go"
    RUST = "rust"
    SCALA = "scala"
    SQL = "sql"
    HTML = "html"
    CSS = "css"
    SHELL = "shell"
    R = "r"
    JULIA = "julia"
    HASKELL = "haskell"
    PERL = "perl"
    LUA = "lua"
    MATLAB = "matlab"


class CodeFileType(str, Enum):
    """Code-specific file types with language associations."""

    # Python
    PY = "py"
    PYI = "pyi"
    PYW = "pyw"
    IPYNB = "ipynb"

    # JavaScript/TypeScript
    JS = "js"
    MJS = "mjs"
    JSX = "jsx"
    TS = "ts"
    TSX = "tsx"

    # Java/Kotlin
    JAVA = "java"
    KT = "kt"
    KTS = "kts"

    # C/C++
    C = "c"
    CPP = "cpp"
    H = "h"
    HPP = "hpp"

    # C#
    CS = "cs"

    # Ruby
    RB = "rb"

    # PHP
    PHP = "php"

    # Go
    GO = "go"

    # Rust
    RS = "rs"

    # HTML/CSS
    HTML = "html"
    CSS = "css"
    SCSS = "scss"
    SASS = "sass"
    LESS = "less"

    # Shell
    SH = "sh"
    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"

    # SQL
    SQL = "sql"

    # R
    R = "r"
    RMD = "rmd"

    # Julia
    JL = "jl"

    # Haskell
    HS = "hs"

    # Perl
    PL = "pl"
    PM = "pm"

    # Lua
    LUA = "lua"

    # MATLAB
    M = "m"


from enum import Enum


class LocalSourceFileType(str, Enum):
    """Supported file types with their actual file extensions."""

    # Document formats
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"

    # Spreadsheet formats
    XLSX = "xlsx"
    XLS = "xls"
    CSV = "csv"

    # Text formats
    TXT = "txt"
    MD = "md"
    RTF = "rtf"
    RST = "rst"
    ODT = "odt"

    # Web formats
    HTML = "html"
    XML = "xml"
    MHTML = "mhtml"

    # Data formats
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    BIBTEX = "bib"

    # Code formats
    PYTHON = "py"  # Changed from "python" to actual file extension
    NOTEBOOK = "ipynb"  # Changed from "notebook" to actual file extension

    # Other formats
    VSDX = "vsdx"
    CHM = "chm"
    EPUB = "epub"
    SRT = "srt"
    EVERNOTE = "enex"
