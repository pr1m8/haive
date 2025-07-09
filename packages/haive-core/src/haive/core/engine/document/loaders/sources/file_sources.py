"""Complete file-based source registrations.

This module implements all file-based document loaders from langchain_community
with focus on unstructured processing, generic loaders, and code language support.
"""

from typing import Any, Dict, List, Optional

from .enhanced_registry import (
    enhanced_registry,
    register_bulk_source,
    register_file_source,
)
from .source_types import (
    DirectorySource,
    LoaderCapability,
    LocalFileSource,
    SourceCategory,
)

# =============================================================================
# Generic and Unstructured File Loaders
# =============================================================================


@register_file_source(
    name="unstructured_file",
    extensions=[".txt", ".md", ".rst", ".doc", ".docx", ".pdf", ".html", ".xml"],
    loaders={
        "auto": {
            "class": "UnstructuredFileLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
        "api": {
            "class": "UnstructuredAPIFileLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured-client"],
        },
    },
    default_loader="auto",
    description="Generic unstructured file loader with auto-detection",
    capabilities=[LoaderCapability.METADATA_EXTRACTION, LoaderCapability.OCR],
    priority=5,
)
class UnstructuredFileSource(LocalFileSource):
    """Generic unstructured file source with auto-format detection."""

    mode: str = "elements"  # single, elements, paged
    strategy: str = "auto"  # auto, fast, ocr_only, hi_res
    include_metadata: bool = True
    coordinates: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "mode": self.mode,
                "strategy": self.strategy,
                "include_metadata": self.include_metadata,
                "coordinates": self.coordinates,
            }
        )
        return kwargs


@register_file_source(
    name="generic_file",
    extensions=[".*"],  # Matches any extension
    loaders={
        "text": {
            "class": "TextLoader",
            "speed": "fast",
            "quality": "low",
            "module": "langchain_community.document_loaders",
        },
        "unstructured": {
            "class": "UnstructuredFileLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
    },
    default_loader="text",
    description="Fallback generic file loader for unknown formats",
    priority=1,  # Lowest priority - fallback only
)
class GenericFileSource(LocalFileSource):
    """Fallback generic file source for unknown file types."""

    autodetect_encoding: bool = True
    fallback_encoding: str = "utf-8"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "autodetect_encoding": self.autodetect_encoding,
                "encoding": self.fallback_encoding,
            }
        )
        return kwargs


# =============================================================================
# Code and Programming Language Files
# =============================================================================


@register_file_source(
    name="python_code",
    extensions=[".py", ".pyx", ".pyi"],
    loaders={
        "simple": {
            "class": "PythonLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        },
        "text": {
            "class": "TextLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
    },
    default_loader="simple",
    description="Python source code loader with syntax awareness",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=9,
)
class PythonCodeSource(LocalFileSource):
    """Python source code with syntax parsing."""

    include_docstrings: bool = True
    include_comments: bool = True
    parse_functions: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "include_docstrings": self.include_docstrings,
                "include_comments": self.include_comments,
            }
        )
        return kwargs


@register_file_source(
    name="notebook",
    extensions=[".ipynb"],
    loaders={
        "notebook": {
            "class": "NotebookLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="notebook",
    description="Jupyter notebook loader with cell-level processing",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=9,
)
class NotebookSource(LocalFileSource):
    """Jupyter notebook source."""

    include_outputs: bool = True
    max_output_length: int = 10000
    remove_newline: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "include_outputs": self.include_outputs,
                "max_output_length": self.max_output_length,
                "remove_newline": self.remove_newline,
            }
        )
        return kwargs


# =============================================================================
# Office and Productivity Documents (Extended)
# =============================================================================


@register_file_source(
    name="powerpoint",
    extensions=[".ppt", ".pptx"],
    loaders={
        "unstructured": {
            "class": "UnstructuredPowerPointLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="PowerPoint presentation loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class PowerPointSource(LocalFileSource):
    """PowerPoint presentation source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


@register_file_source(
    name="odt_document",
    extensions=[".odt"],
    loaders={
        "unstructured": {
            "class": "UnstructuredODTLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="OpenDocument text file loader",
    priority=7,
)
class ODTDocumentSource(LocalFileSource):
    """OpenDocument text source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


@register_file_source(
    name="rtf_document",
    extensions=[".rtf"],
    loaders={
        "unstructured": {
            "class": "UnstructuredRTFLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="Rich Text Format document loader",
    priority=7,
)
class RTFDocumentSource(LocalFileSource):
    """RTF document source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


# =============================================================================
# Email and Communication Files
# =============================================================================


@register_file_source(
    name="email",
    extensions=[".eml", ".msg"],
    loaders={
        "unstructured": {
            "class": "UnstructuredEmailLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
        "outlook": {
            "class": "OutlookMessageLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["extract_msg"],
        },
    },
    default_loader="unstructured",
    description="Email file loader with header extraction",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=8,
)
class EmailSource(LocalFileSource):
    """Email file source."""

    mode: str = "elements"
    extract_attachments: bool = False

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"mode": self.mode, "extract_attachments": self.extract_attachments}
        )
        return kwargs


# =============================================================================
# E-book and Publication Formats
# =============================================================================


@register_file_source(
    name="epub",
    extensions=[".epub"],
    loaders={
        "unstructured": {
            "class": "UnstructuredEPubLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="EPUB e-book loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class EPubSource(LocalFileSource):
    """EPUB e-book source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


# =============================================================================
# Archive and Compressed Files
# =============================================================================


@register_file_source(
    name="chm_help",
    extensions=[".chm"],
    loaders={
        "unstructured": {
            "class": "UnstructuredCHMLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured", "chm"],
        }
    },
    default_loader="unstructured",
    description="Compiled HTML Help file loader",
    priority=6,
)
class CHMHelpSource(LocalFileSource):
    """CHM help file source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


# =============================================================================
# Configuration and Data Files (Extended)
# =============================================================================


@register_file_source(
    name="toml_config",
    extensions=[".toml"],
    loaders={
        "toml": {
            "class": "TomlLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="toml",
    description="TOML configuration file loader",
    priority=7,
)
class TOMLConfigSource(LocalFileSource):
    """TOML configuration file source."""

    parse_structure: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["parse_structure"] = self.parse_structure
        return kwargs


@register_file_source(
    name="yaml_config",
    extensions=[".yaml", ".yml"],
    loaders={
        "text": {
            "class": "TextLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "unstructured": {
            "class": "UnstructuredFileLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        },
    },
    default_loader="text",
    description="YAML configuration file loader",
    priority=7,
)
class YAMLConfigSource(LocalFileSource):
    """YAML configuration file source."""

    parse_yaml: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["parse_yaml"] = self.parse_yaml
        return kwargs


@register_file_source(
    name="xml_data",
    extensions=[".xml"],
    loaders={
        "unstructured": {
            "class": "UnstructuredXMLLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured"],
        }
    },
    default_loader="unstructured",
    description="XML data file loader with structure preservation",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class XMLDataSource(LocalFileSource):
    """XML data file source."""

    mode: str = "elements"

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["mode"] = self.mode
        return kwargs


# =============================================================================
# Subtitle and Caption Files
# =============================================================================


@register_file_source(
    name="subtitle",
    extensions=[".srt", ".vtt", ".ass", ".ssa"],
    loaders={
        "srt": {
            "class": "SRTLoader",
            "speed": "fast",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        },
        "text": {
            "class": "TextLoader",
            "speed": "fast",
            "quality": "low",
            "module": "langchain_community.document_loaders",
        },
    },
    default_loader="srt",
    description="Subtitle and caption file loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=6,
)
class SubtitleSource(LocalFileSource):
    """Subtitle file source."""

    include_timestamps: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs["include_timestamps"] = self.include_timestamps
        return kwargs


# =============================================================================
# Enhanced Directory Sources (Bulk Loading)
# =============================================================================


@register_bulk_source(
    name="pdf_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "bulk": {
            "class": "PyPDFDirectoryLoader",
            "speed": "medium",
            "quality": "medium",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="bulk",
    description="Bulk PDF directory loader with recursive processing",
    max_concurrent=6,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ],
    priority=9,
)
class PDFDirectorySource(DirectorySource):
    """PDF directory source for bulk processing."""

    extract_images: bool = False
    silent_errors: bool = True

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"extract_images": self.extract_images, "silent_errors": self.silent_errors}
        )
        return kwargs


@register_bulk_source(
    name="unstructured_directory",
    category=SourceCategory.DIRECTORY_LOCAL,
    loaders={
        "auto": {
            "class": "DirectoryLoader",
            "speed": "medium",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="auto",
    description="Directory loader with unstructured file processing",
    max_concurrent=4,
    capabilities=[
        LoaderCapability.BULK_LOADING,
        LoaderCapability.RECURSIVE,
        LoaderCapability.FILTERING,
    ],
    priority=8,
)
class UnstructuredDirectorySource(DirectorySource):
    """Directory source with unstructured processing."""

    loader_cls_name: str = "UnstructuredFileLoader"
    loader_kwargs: Dict[str, Any] = {}

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {"loader_cls": self.loader_cls_name, "loader_kwargs": self.loader_kwargs}
        )
        return kwargs


# =============================================================================
# Advanced Image Processing
# =============================================================================


@register_file_source(
    name="image_document",
    extensions=[".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    loaders={
        "unstructured": {
            "class": "UnstructuredImageLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["unstructured", "pillow"],
        },
        "caption": {
            "class": "ImageCaptionLoader",
            "speed": "slow",
            "quality": "high",
            "module": "langchain_community.document_loaders",
            "requires_packages": ["transformers", "torch"],
        },
    },
    default_loader="unstructured",
    description="Image file loader with OCR and caption generation",
    capabilities=[LoaderCapability.OCR, LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class ImageDocumentSource(LocalFileSource):
    """Image document source with OCR capabilities."""

    mode: str = "elements"
    strategy: str = "auto"
    ocr_languages: List[str] = ["eng"]

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        kwargs.update(
            {
                "mode": self.mode,
                "strategy": self.strategy,
                "languages": self.ocr_languages,
            }
        )
        return kwargs


# =============================================================================
# Academic and Research File Formats
# =============================================================================


@register_file_source(
    name="bibtex",
    extensions=[".bib"],
    loaders={
        "bibtex": {
            "class": "BibtexLoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="bibtex",
    description="BibTeX bibliography file loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=7,
)
class BibtexSource(LocalFileSource):
    """BibTeX bibliography source."""

    file_path: str
    max_docs: Optional[int] = None

    def get_loader_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_loader_kwargs()
        if self.max_docs:
            kwargs["max_docs"] = self.max_docs
        return kwargs


@register_file_source(
    name="conllu_linguistic",
    extensions=[".conllu", ".conll"],
    loaders={
        "conllu": {
            "class": "CoNLLULoader",
            "speed": "fast",
            "quality": "high",
            "module": "langchain_community.document_loaders",
        }
    },
    default_loader="conllu",
    description="CoNLL-U linguistic annotation file loader",
    capabilities=[LoaderCapability.METADATA_EXTRACTION],
    priority=6,
)
class CoNLLULinguisticSource(LocalFileSource):
    """CoNLL-U linguistic data source."""

    def get_loader_kwargs(self) -> Dict[str, Any]:
        return super().get_loader_kwargs()


# =============================================================================
# Utility Functions
# =============================================================================


def get_file_sources_statistics() -> Dict[str, Any]:
    """Get statistics about registered file sources."""
    registry = enhanced_registry
    stats = registry.get_statistics()

    # File-specific analysis
    file_categories = [
        SourceCategory.FILE_DOCUMENT,
        SourceCategory.FILE_DATA,
        SourceCategory.FILE_CODE,
        SourceCategory.FILE_MEDIA,
        SourceCategory.DIRECTORY_LOCAL,
    ]

    file_stats = {}
    for category in file_categories:
        sources = registry.find_sources_by_category(category)
        file_stats[category.value] = len(sources)

    # Capability analysis
    bulk_capable = len(
        registry.find_sources_with_capability(LoaderCapability.BULK_LOADING)
    )
    ocr_capable = len(registry.find_sources_with_capability(LoaderCapability.OCR))
    metadata_capable = len(
        registry.find_sources_with_capability(LoaderCapability.METADATA_EXTRACTION)
    )

    return {
        "total_file_sources": sum(file_stats.values()),
        "by_category": file_stats,
        "capabilities": {
            "bulk_loading": bulk_capable,
            "ocr_processing": ocr_capable,
            "metadata_extraction": metadata_capable,
        },
        "extensions_covered": stats["extensions_covered"],
        "unstructured_loaders": len(
            [
                name
                for name in registry._sources.keys()
                if "unstructured" in name.lower()
            ]
        ),
    }


def validate_file_sources() -> bool:
    """Validate file source registrations."""
    registry = enhanced_registry

    required_file_types = [
        "unstructured_file",
        "python_code",
        "notebook",
        "powerpoint",
        "email",
        "epub",
        "image_document",
        "pdf_directory",
    ]

    missing = []
    for source_name in required_file_types:
        if source_name not in registry._sources:
            missing.append(source_name)

    if missing:
        print(f"Missing file sources: {missing}")
        return False

    print(f"All {len(required_file_types)} essential file sources registered!")
    return True


# Auto-validate on import
if __name__ == "__main__":
    validate_file_sources()
    stats = get_file_sources_statistics()
    print(f"File Sources Statistics: {stats}")
