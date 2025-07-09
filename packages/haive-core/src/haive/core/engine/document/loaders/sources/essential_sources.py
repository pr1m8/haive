"""Essential source registrations for Phase 1 implementation.

This module registers the most commonly used document loaders to support
the core functionality needed for the document engine migration.
"""

from typing import Any, Dict, Optional

from .enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_database_source,
    register_file_source,
    register_web_source,
)
from .source_types import (
    CredentialType,
    DatabaseSource,
    DirectorySource,
    LocalFileSource,
    RemoteSource,
    SourceCategory,
)

# =============================================================================
# Phase 1: Essential File-Based Sources (20 core loaders)
# =============================================================================


@register_file_source(
    name="pdf",
    extensions=[".pdf"],
    loaders={
        "fast": {
            "class": "PyPDFLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "quality": {
            "class": "UnstructuredPDFLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
        "advanced": {
            "class": "PyMuPDFLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["pymupdf"],
        },
    },
    default_loader="fast",
    description="PDF document loader with multiple processing options",
    typical_speed="medium",
    typical_quality="high",
    priority=10,
)
class PDFSource(LocalFileSource):
    """PDF document source with OCR and layout analysis options."""

    ocr_enabled: bool = False
    extract_images: bool = False
    layout_analysis: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update({"extract_images": self.extract_images})
        return kwargs


@register_file_source(
    name="csv",
    extensions=[".csv"],
    loaders={
        "simple": {
            "class": "CSVLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "unstructured": {
            "class": "UnstructuredCSVLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
    },
    default_loader="simple",
    description="CSV file loader with structured data processing",
    is_bulk_loader=True,
    priority=8,
)
class CSVSource(LocalFileSource):
    """CSV file source with column mapping and filtering."""

    delimiter: str = ","
    encoding: str = "utf-8"
    skip_rows: int = 0
    columns: Optional[list] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "csv_args": {
                    "delimiter": self.delimiter,
                    "encoding": self.encoding,
                    "skiprows": self.skip_rows,
                }
            }
        )
        return kwargs


@register_file_source(
    name="json",
    extensions=[".json", ".jsonl"],
    loaders={
        "simple": {
            "class": "JSONLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="simple",
    description="JSON file loader with jq schema support",
    priority=8,
)
class JSONSource(LocalFileSource):
    """JSON file source with schema extraction."""

    jq_schema: Optional[str] = None
    text_content: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        if self.jq_schema:
            kwargs["jq_schema"] = self.jq_schema
        kwargs["text_content"] = self.text_content
        return kwargs


@register_file_source(
    name="text",
    extensions=[".txt", ".text"],
    loaders={
        "simple": {
            "class": "TextLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="simple",
    description="Plain text file loader",
    priority=7,
)
class TextSource(LocalFileSource):
    """Plain text file source."""

    autodetect_encoding: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["autodetect_encoding"] = self.autodetect_encoding
        return kwargs


@register_file_source(
    name="markdown",
    extensions=[".md", ".markdown"],
    loaders={
        "simple": {
            "class": "UnstructuredMarkdownLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="simple",
    description="Markdown file loader with structure preservation",
    priority=7,
)
class MarkdownSource(LocalFileSource):
    """Markdown file source with metadata extraction."""

    mode: str = "elements"  # single, elements, paged

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


@register_file_source(
    name="word_document",
    extensions=[".doc", ".docx"],
    loaders={
        "unstructured": {
            "class": "UnstructuredWordDocumentLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
        "docx2txt": {
            "class": "Docx2txtLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["docx2txt"],
        },
    },
    default_loader="unstructured",
    description="Microsoft Word document loader",
    priority=8,
)
class WordDocumentSource(LocalFileSource):
    """Microsoft Word document source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


@register_file_source(
    name="excel",
    extensions=[".xls", ".xlsx"],
    loaders={
        "unstructured": {
            "class": "UnstructuredExcelLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="Microsoft Excel spreadsheet loader",
    priority=7,
)
class ExcelSource(LocalFileSource):
    """Microsoft Excel spreadsheet source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


@register_file_source(
    name="html",
    extensions=[".html", ".htm"],
    loaders={
        "unstructured": {
            "class": "UnstructuredHTMLLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
        "bs4": {
            "class": "BSHTMLLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["beautifulsoup4"],
        },
    },
    default_loader="unstructured",
    description="HTML file loader with tag preservation",
    priority=6,
)
class HTMLSource(LocalFileSource):
    """HTML file source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


# =============================================================================
# Web-Based Sources
# =============================================================================


@register_web_source(
    name="web_page",
    url_patterns=["http", "https"],
    loaders={
        "simple": {
            "class": "WebBaseLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "async": {
            "class": "AsyncHtmlLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "playwright": {
            "class": "PlaywrightURLLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["playwright"],
        },
    },
    default_loader="simple",
    description="Web page loader with browser automation support",
    priority=8,
)
class WebPageSource(RemoteSource):
    """Web page source with JavaScript rendering support."""

    wait_for_js: bool = False
    scroll_to_bottom: bool = False
    selector: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "wait_for_js": self.wait_for_js,
                "scroll": self.scroll_to_bottom,
                "selector": self.selector,
            }
        )
        return kwargs


@register_web_source(
    name="github",
    url_patterns=["github.com"],
    loaders={
        "file": {
            "class": "GithubFileLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="file",
    description="GitHub repository and file loader",
    credential_type=CredentialType.API_KEY,
    priority=7,
)
class GitHubSource(RemoteSource):
    """GitHub repository source."""

    repository: str
    branch: str = "main"
    file_path: Optional[str] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "repo": self.repository,
                "branch": self.branch,
                "file_path": self.file_path,
            }
        )
        return kwargs


# =============================================================================
# Directory Sources (Bulk Loading)
# =============================================================================


@register_bulk_source(
    name="local_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "recursive": {
            "class": "DirectoryLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="recursive",
    description="Local directory loader with recursive traversal",
    max_concurrent=4,
    priority=9,
)
class LocalDirectorySource(DirectorySource):
    """Local directory source for bulk file processing."""

    use_multithreading: bool = True
    max_concurrency: int = 4
    show_progress: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "use_multithreading": self.use_multithreading,
                "max_concurrency": self.max_concurrency,
                "show_progress": self.show_progress,
            }
        )
        return kwargs


# =============================================================================
# Database Sources
# =============================================================================


@register_database_source(
    name="postgresql",
    database_type="postgresql",
    loaders={
        "sql": {
            "class": "SQLDatabaseLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="sql",
    description="PostgreSQL database loader",
    priority=8,
)
class PostgreSQLSource(DatabaseSource):
    """PostgreSQL database source."""

    page_size: int = 1000

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["page_size"] = self.page_size
        return kwargs


@register_database_source(
    name="mongodb",
    database_type="mongodb",
    loaders={
        "mongo": {
            "class": "MongodbLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="mongo",
    description="MongoDB document database loader",
    priority=7,
)
class MongoDBSource(DatabaseSource):
    """MongoDB database source."""

    collection_name: str
    filter_criteria: Optional[dict] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "collection_name": self.collection_name,
                "filter_criteria": self.filter_criteria or {},
            }
        )
        return kwargs


# =============================================================================
# Utility Functions
# =============================================================================


def get_essential_sources_statistics() -> Dict[str, Any]:
    """Get statistics about registered essential sources."""
    stats = enhanced_registry.get_statistics()

    # Add Phase 1 specific info
    phase1_sources = [
        "pdf",
        "csv",
        "json",
        "text",
        "markdown",
        "word_document",
        "excel",
        "html",
        "web_page",
        "github",
        "local_directory",
        "postgresql",
        "mongodb",
    ]

    registered_phase1 = [
        name for name in phase1_sources if name in enhanced_registry._sources
    ]

    stats["phase1_registered"] = len(registered_phase1)
    stats["phase1_total"] = len(phase1_sources)
    stats["phase1_sources"] = registered_phase1

    return stats


def validate_essential_sources() -> bool:
    """Validate that all essential sources are properly registered."""
    required_sources = [
        "pdf",
        "csv",
        "json",
        "text",
        "markdown",
        "word_document",
        "excel",
        "html",
        "web_page",
        "local_directory",
        "postgresql",
    ]

    missing = []
    for source_name in required_sources:
        if source_name not in enhanced_registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing essential sources: {missing}")
        return False

    print(f"All {len(required_sources)} essential sources registered successfully!")
    return True


# Auto-validate on import
if __name__ == "__main__":
    validate_essential_sources()
    stats = get_essential_sources_statistics()
    print(f"Registry Statistics: {stats}")
