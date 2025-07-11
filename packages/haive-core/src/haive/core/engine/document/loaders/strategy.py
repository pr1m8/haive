"""Loader Strategy System for Document Engine.

This module implements the loader strategy system for intelligent loader selection
based on source type, performance requirements, and capabilities.
"""

import importlib
import logging
from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from langchain_core.document_loaders.base import BaseLoader
from pydantic import BaseModel, Field

from haive.core.engine.document.loaders.sources.implementation import EnhancedSource

logger = logging.getLogger(__name__)


class LoaderPriority(str, Enum):
    """Priority levels for loader selection."""

    HIGHEST = "highest"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    LOWEST = "lowest"


class LoaderCapability(str, Enum):
    """Capabilities that loaders may support."""

    ASYNC = "async"
    METADATA = "metadata"
    CONTENT_EXTRACTION = "content_extraction"
    TEXT_EXTRACTION = "text_extraction"
    IMAGE_EXTRACTION = "image_extraction"
    TABLE_EXTRACTION = "table_extraction"
    STRUCTURE_PRESERVATION = "structure_preservation"
    LAZY_LOADING = "lazy_loading"
    PAGINATION = "pagination"
    CHUNKING = "chunking"
    FILTERING = "filtering"
    BATCHING = "batching"


class LoaderStrategy(BaseModel):
    """Information about a document loader strategy."""

    # Identification
    strategy_name: str = Field(..., description="Unique name for this loader strategy")

    # Loader class information
    loader_class: str = Field(..., description="Name of the loader class")
    module_path: str = Field(
        default="langchain_community.document_loaders",
        description="Import path for the loader module",
    )

    # Performance characteristics
    speed: Literal["fast", "medium", "slow"] = Field(
        default="medium", description="Relative speed of the loader"
    )
    quality: Literal["low", "medium", "high"] = Field(
        default="medium", description="Quality of document extraction"
    )
    resource_usage: Literal["low", "medium", "high"] = Field(
        default="medium", description="Resource consumption of the loader"
    )

    # Capabilities
    supports_async: bool = Field(
        default=False, description="Whether the loader supports async loading"
    )
    supports_metadata: bool = Field(
        default=True, description="Whether the loader extracts document metadata"
    )
    supports_batching: bool = Field(
        default=False, description="Whether the loader supports batch loading"
    )

    capabilities: List[LoaderCapability] = Field(
        default_factory=list, description="Special capabilities of this loader"
    )

    # Suitability indicators
    best_for: List[str] = Field(
        default_factory=list,
        description="Types of content this loader is best suited for",
    )

    # Requirements
    requires_dependencies: List[str] = Field(
        default_factory=list,
        description="Additional dependencies required for this loader",
    )
    requires_authentication: bool = Field(
        default=False, description="Whether this loader requires authentication"
    )

    # Priority and availability
    priority: LoaderPriority = Field(
        default=LoaderPriority.MEDIUM, description="Selection priority for this loader"
    )
    is_available: bool = Field(
        default=True, description="Whether this loader is currently available"
    )

    def create_loader(
        self, source: EnhancedSource, options: Dict[str, Any]
    ) -> Optional[BaseLoader]:
        """Create a loader instance for the given source."""
        try:
            # Import the loader class
            module = importlib.import_module(self.module_path)
            loader_cls = getattr(module, self.loader_class)

            # Create loader with appropriate arguments
            if hasattr(source, "source_path"):
                return loader_cls(source.source_path, **options)
            else:
                return loader_cls(**options)

        except Exception as e:
            logger.error(f"Failed to create loader {self.loader_class}: {e}")
            return None

    def check_availability(self) -> bool:
        """Check if this loader strategy is available."""
        try:
            # Try to import the required module and class
            module = importlib.import_module(self.module_path)
            getattr(module, self.loader_class)

            # Check for required dependencies
            for dep in self.requires_dependencies:
                try:
                    importlib.import_module(dep)
                except ImportError:
                    logger.warning(
                        f"Dependency {dep} not available for {self.strategy_name}"
                    )
                    return False

            return True

        except Exception as e:
            logger.warning(f"Loader {self.strategy_name} not available: {e}")
            return False


class LoaderStrategyRegistry:
    """Registry for managing loader strategies."""

    def __init__(self):
        self._strategies: Dict[str, LoaderStrategy] = {}
        self._register_default_strategies()

    def _register_default_strategies(self):
        """Register default loader strategies."""

        # PDF loaders
        self.register(
            LoaderStrategy(
                strategy_name="pdf_pymupdf",
                loader_class="PyMuPDFLoader",
                speed="fast",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["pdf", "document"],
                requires_dependencies=["pymupdf"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="pdf_pdfplumber",
                loader_class="PDFPlumberLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["pdf", "tables"],
                requires_dependencies=["pdfplumber"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="pdf_unstructured",
                loader_class="UnstructuredPDFLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.IMAGE_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["pdf", "scanned", "ocr"],
                requires_dependencies=["unstructured", "pdf2image", "pytesseract"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Web loaders
        self.register(
            LoaderStrategy(
                strategy_name="web_base",
                loader_class="WebBaseLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["web", "html", "url"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="playwright",
                loader_class="PlaywrightURLLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[LoaderCapability.TEXT_EXTRACTION, LoaderCapability.ASYNC],
                best_for=["web", "javascript", "dynamic"],
                requires_dependencies=["playwright"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="selenium",
                loader_class="SeleniumURLLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["web", "javascript", "dynamic"],
                requires_dependencies=["selenium"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Document loaders
        self.register(
            LoaderStrategy(
                strategy_name="docx",
                loader_class="Docx2txtLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["docx", "doc", "document"],
                requires_dependencies=["docx2txt"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="unstructured_word",
                loader_class="UnstructuredWordDocumentLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["docx", "doc"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Text loaders
        self.register(
            LoaderStrategy(
                strategy_name="text_file",
                loader_class="TextLoader",
                speed="fast",
                quality="low",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["text", "txt", "log"],
                priority=LoaderPriority.LOW,
            )
        )

        # CSV loaders
        self.register(
            LoaderStrategy(
                strategy_name="csv",
                loader_class="CSVLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["csv", "data"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # JSON loaders
        self.register(
            LoaderStrategy(
                strategy_name="json",
                loader_class="JSONLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["json", "jsonl"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Markdown loaders
        self.register(
            LoaderStrategy(
                strategy_name="markdown",
                loader_class="UnstructuredMarkdownLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["md", "markdown"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Excel loaders
        self.register(
            LoaderStrategy(
                strategy_name="excel",
                loader_class="UnstructuredExcelLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["xlsx", "xls", "excel"],
                requires_dependencies=["unstructured", "openpyxl"],
                priority=LoaderPriority.HIGH,
            )
        )

        # PowerPoint loaders
        self.register(
            LoaderStrategy(
                strategy_name="powerpoint",
                loader_class="UnstructuredPowerPointLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.IMAGE_EXTRACTION,
                ],
                best_for=["pptx", "ppt", "powerpoint"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Email loaders
        self.register(
            LoaderStrategy(
                strategy_name="email",
                loader_class="UnstructuredEmailLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["eml", "msg", "email"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # HTML loaders
        self.register(
            LoaderStrategy(
                strategy_name="html",
                loader_class="UnstructuredHTMLLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["html", "htm"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # XML loaders
        self.register(
            LoaderStrategy(
                strategy_name="xml",
                loader_class="UnstructuredXMLLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["xml"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        # RTF loaders
        self.register(
            LoaderStrategy(
                strategy_name="rtf",
                loader_class="UnstructuredRTFLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["rtf"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Directory loaders
        self.register(
            LoaderStrategy(
                strategy_name="directory",
                loader_class="DirectoryLoader",
                speed="medium",
                quality="medium",
                resource_usage="medium",
                capabilities=[LoaderCapability.BATCHING],
                best_for=["directory", "folder"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Git repository loaders
        self.register(
            LoaderStrategy(
                strategy_name="git",
                loader_class="GitLoader",
                speed="slow",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["git", "repository", "code"],
                requires_dependencies=["gitpython"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # YouTube loaders
        self.register(
            LoaderStrategy(
                strategy_name="youtube",
                loader_class="YoutubeLoader",
                module_path="langchain_community.document_loaders",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["youtube", "video"],
                requires_dependencies=["youtube-transcript-api"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Wikipedia loaders
        self.register(
            LoaderStrategy(
                strategy_name="wikipedia",
                loader_class="WikipediaLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["wikipedia", "wiki"],
                requires_dependencies=["wikipedia"],
                priority=LoaderPriority.HIGH,
            )
        )

        # ArXiv loaders
        self.register(
            LoaderStrategy(
                strategy_name="arxiv",
                loader_class="ArxivLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["arxiv", "research", "paper"],
                requires_dependencies=["arxiv"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Additional PDF loaders
        self.register(
            LoaderStrategy(
                strategy_name="pypdf",
                loader_class="PyPDFLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["pdf"],
                requires_dependencies=["pypdf"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="pdfminer",
                loader_class="PDFMinerLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["pdf", "complex"],
                requires_dependencies=["pdfminer.six"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="pypdfium2",
                loader_class="PyPDFium2Loader",
                speed="fast",
                quality="high",
                resource_usage="medium",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["pdf"],
                requires_dependencies=["pypdfium2"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="mathpix_pdf",
                loader_class="MathpixPDFLoader",
                speed="slow",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.IMAGE_EXTRACTION,
                ],
                best_for=["pdf", "math", "scientific"],
                requires_dependencies=["mathpix-pdf-to-html"],
                requires_authentication=True,
                priority=LoaderPriority.LOW,
            )
        )

        # YAML loaders - use JSONLoader which supports YAML
        self.register(
            LoaderStrategy(
                strategy_name="yaml",
                loader_class="JSONLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["yaml", "yml", "config"],
                requires_dependencies=["pyyaml"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="toml",
                loader_class="TomlLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["toml", "config"],
                requires_dependencies=["toml"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Code/Programming loaders
        self.register(
            LoaderStrategy(
                strategy_name="python",
                loader_class="PythonLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["py", "python", "code"],
                requires_dependencies=[],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="notebook",
                loader_class="NotebookLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["ipynb", "jupyter", "notebook"],
                requires_dependencies=["nbformat"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Scientific/Academic loaders
        self.register(
            LoaderStrategy(
                strategy_name="bibtex",
                loader_class="BibtexLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["bib", "bibtex", "bibliography"],
                requires_dependencies=["pybtex"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="pubmed",
                loader_class="PubMedLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["pubmed", "medical", "research"],
                requires_dependencies=["biopython"],
                priority=LoaderPriority.HIGH,
            )
        )

        # OpenDocument formats
        self.register(
            LoaderStrategy(
                strategy_name="odt",
                loader_class="UnstructuredODTLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["odt", "opendocument"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # E-book formats
        self.register(
            LoaderStrategy(
                strategy_name="epub",
                loader_class="UnstructuredEPubLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["epub", "ebook"],
                requires_dependencies=["unstructured", "ebooklib"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Media/Subtitle loaders
        self.register(
            LoaderStrategy(
                strategy_name="srt",
                loader_class="SRTLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["srt", "subtitle", "caption"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Image loaders
        self.register(
            LoaderStrategy(
                strategy_name="image",
                loader_class="UnstructuredImageLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.IMAGE_EXTRACTION,
                ],
                best_for=["jpg", "jpeg", "png", "gif", "bmp", "tiff", "image"],
                requires_dependencies=["unstructured", "pytesseract", "pillow"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Cloud storage loaders
        self.register(
            LoaderStrategy(
                strategy_name="s3_file",
                loader_class="S3FileLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["s3", "aws"],
                requires_dependencies=["boto3"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="s3_directory",
                loader_class="S3DirectoryLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[LoaderCapability.BATCHING],
                best_for=["s3", "aws", "directory"],
                requires_dependencies=["boto3"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="gcs_file",
                loader_class="GCSFileLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["gcs", "google"],
                requires_dependencies=["google-cloud-storage"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="azure_blob",
                loader_class="AzureBlobStorageFileLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["azure", "blob"],
                requires_dependencies=["azure-storage-blob"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # Database loaders
        self.register(
            LoaderStrategy(
                strategy_name="sql_database",
                loader_class="SQLDatabaseLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["sql", "database"],
                requires_dependencies=["sqlalchemy"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="mongodb",
                loader_class="MongodbLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["mongodb", "nosql"],
                requires_dependencies=["pymongo"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # API/Service loaders
        self.register(
            LoaderStrategy(
                strategy_name="notion",
                loader_class="NotionDBLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["notion"],
                requires_dependencies=["notion-client"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="confluence",
                loader_class="ConfluenceLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["confluence", "wiki"],
                requires_dependencies=["atlassian-python-api"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="google_drive",
                loader_class="GoogleDriveLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["gdrive", "google"],
                requires_dependencies=["google-auth", "google-api-python-client"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # Chat/Messaging loaders
        self.register(
            LoaderStrategy(
                strategy_name="slack",
                loader_class="SlackDirectoryLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["slack", "chat"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="discord",
                loader_class="DiscordChatLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["discord", "chat"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # News/Content loaders
        self.register(
            LoaderStrategy(
                strategy_name="reddit",
                loader_class="RedditPostsLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["reddit", "social"],
                requires_dependencies=["praw"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="hackernews",
                loader_class="HNLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["hackernews", "hn"],
                requires_dependencies=["beautifulsoup4"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # More Unstructured file loaders
        self.register(
            LoaderStrategy(
                strategy_name="unstructured_file",
                loader_class="UnstructuredFileLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["generic", "unknown"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.LOW,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="unstructured_rst",
                loader_class="UnstructuredRSTLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["rst", "restructuredtext"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="unstructured_org_mode",
                loader_class="UnstructuredOrgModeLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["org", "orgmode"],
                requires_dependencies=["unstructured", "pandoc"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="unstructured_tsv",
                loader_class="UnstructuredTSVLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["tsv", "tab"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Archive/Compressed file loaders
        self.register(
            LoaderStrategy(
                strategy_name="unstructured_chm",
                loader_class="UnstructuredCHMLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["chm", "help"],
                requires_dependencies=["unstructured"],
                priority=LoaderPriority.LOW,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="mhtml",
                loader_class="MHTMLLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["mhtml", "mht"],
                requires_dependencies=["beautifulsoup4"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Specialized document loaders
        self.register(
            LoaderStrategy(
                strategy_name="vsdx",
                loader_class="VsdxLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[LoaderCapability.TEXT_EXTRACTION],
                best_for=["vsdx", "visio"],
                requires_dependencies=["vsdx", "beautifulsoup4"],
                priority=LoaderPriority.LOW,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="outlook_message",
                loader_class="OutlookMessageLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["msg", "outlook"],
                requires_dependencies=["extract_msg"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Data science loaders
        self.register(
            LoaderStrategy(
                strategy_name="dataframe",
                loader_class="DataFrameLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["dataframe", "pandas"],
                requires_dependencies=["pandas"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Enhanced web loaders
        self.register(
            LoaderStrategy(
                strategy_name="recursive_url",
                loader_class="RecursiveUrlLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.BATCHING,
                ],
                best_for=["website", "crawl"],
                requires_dependencies=["beautifulsoup4"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="sitemap",
                loader_class="SitemapLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.BATCHING,
                ],
                best_for=["sitemap", "xml"],
                requires_dependencies=["beautifulsoup4"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Async loaders
        self.register(
            LoaderStrategy(
                strategy_name="async_html",
                loader_class="AsyncHtmlLoader",
                speed="fast",
                quality="medium",
                resource_usage="low",
                capabilities=[LoaderCapability.TEXT_EXTRACTION, LoaderCapability.ASYNC],
                best_for=["html", "async"],
                requires_dependencies=["aiohttp", "beautifulsoup4"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # More API loaders
        self.register(
            LoaderStrategy(
                strategy_name="unstructured_api",
                loader_class="UnstructuredAPIFileLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.IMAGE_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["api", "unstructured"],
                requires_dependencies=["unstructured"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # News/RSS loaders
        self.register(
            LoaderStrategy(
                strategy_name="rss_feed",
                loader_class="RSSFeedLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["rss", "feed"],
                requires_dependencies=["feedparser"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Knowledge base loaders
        self.register(
            LoaderStrategy(
                strategy_name="obsidian",
                loader_class="ObsidianLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                    LoaderCapability.BATCHING,
                ],
                best_for=["obsidian", "vault", "markdown"],
                requires_dependencies=[],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="roam",
                loader_class="RoamLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["roam", "graph"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # More cloud/service loaders
        self.register(
            LoaderStrategy(
                strategy_name="dropbox",
                loader_class="DropboxLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["dropbox", "cloud"],
                requires_dependencies=["dropbox"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="onedrive",
                loader_class="OneDriveLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["onedrive", "microsoft"],
                requires_dependencies=["o365"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="sharepoint",
                loader_class="SharePointLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["sharepoint", "microsoft"],
                requires_dependencies=["shareplum"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # Blockchain/Crypto loaders
        self.register(
            LoaderStrategy(
                strategy_name="etherscan",
                loader_class="EtherscanLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["ethereum", "blockchain", "crypto"],
                requires_dependencies=["web3"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Scientific data loaders
        self.register(
            LoaderStrategy(
                strategy_name="conllu",
                loader_class="CoNLLULoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.STRUCTURE_PRESERVATION,
                ],
                best_for=["conllu", "nlp", "linguistics"],
                requires_dependencies=["conllu"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Chat export loaders
        self.register(
            LoaderStrategy(
                strategy_name="whatsapp",
                loader_class="WhatsAppChatLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["whatsapp", "chat"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="telegram",
                loader_class="TelegramChatLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["telegram", "chat"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="facebook_chat",
                loader_class="FacebookChatLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["facebook", "messenger", "chat"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        # More specialized loaders
        self.register(
            LoaderStrategy(
                strategy_name="chatgpt",
                loader_class="ChatGPTLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["chatgpt", "openai", "conversation"],
                requires_dependencies=[],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="figma",
                loader_class="FigmaFileLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["figma", "design"],
                requires_dependencies=[],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="trello",
                loader_class="TrelloLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["trello", "kanban", "boards"],
                requires_dependencies=[],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="airtable",
                loader_class="AirtableLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["airtable", "database", "spreadsheet"],
                requires_dependencies=["pyairtable"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # More database loaders
        self.register(
            LoaderStrategy(
                strategy_name="elasticsearch",
                loader_class="ElasticsearchLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["elasticsearch", "search", "elastic"],
                requires_dependencies=["elasticsearch"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="cassandra",
                loader_class="CassandraLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["cassandra", "nosql"],
                requires_dependencies=["cassandra-driver"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="couchbase",
                loader_class="CouchbaseLoader",
                speed="medium",
                quality="high",
                resource_usage="medium",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["couchbase", "nosql"],
                requires_dependencies=["couchbase"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Document collaboration platforms
        self.register(
            LoaderStrategy(
                strategy_name="jira",
                loader_class="JiraLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["jira", "issues", "tickets"],
                requires_dependencies=["atlassian-python-api"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="asana",
                loader_class="AsanaLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["asana", "tasks", "projects"],
                requires_dependencies=["asana"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Code repository loaders
        self.register(
            LoaderStrategy(
                strategy_name="github_issues",
                loader_class="GitHubIssuesLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["github", "issues", "bugs"],
                requires_dependencies=[],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="gitlab",
                loader_class="GitLabLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["gitlab", "code", "repository"],
                requires_dependencies=["python-gitlab"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Scientific/Academic loaders
        self.register(
            LoaderStrategy(
                strategy_name="semantic_scholar",
                loader_class="SemanticScholarLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["research", "papers", "academic"],
                requires_dependencies=["semanticscholar"],
                priority=LoaderPriority.HIGH,
            )
        )

        # Streaming/Media platforms
        self.register(
            LoaderStrategy(
                strategy_name="twitch",
                loader_class="TwitchLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["twitch", "streaming", "chat"],
                requires_dependencies=["twitchio"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="spotify",
                loader_class="SpotifyLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["spotify", "music", "podcasts"],
                requires_dependencies=["spotipy"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # E-commerce/Payment loaders
        self.register(
            LoaderStrategy(
                strategy_name="stripe",
                loader_class="StripeLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["stripe", "payments", "transactions"],
                requires_dependencies=["stripe"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="shopify",
                loader_class="AirbyteShopifyLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["shopify", "ecommerce", "products"],
                requires_dependencies=["airbyte-cdk"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Weather/Environmental data
        self.register(
            LoaderStrategy(
                strategy_name="weather",
                loader_class="WeatherDataLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["weather", "climate", "forecast"],
                requires_dependencies=[],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        # Note-taking apps
        self.register(
            LoaderStrategy(
                strategy_name="evernote",
                loader_class="EverNoteLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["evernote", "notes"],
                requires_dependencies=["lxml"],
                priority=LoaderPriority.HIGH,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="onenote",
                loader_class="OneNoteLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["onenote", "notes", "microsoft"],
                requires_dependencies=["msal"],
                requires_authentication=True,
                priority=LoaderPriority.HIGH,
            )
        )

        # Additional specialized loaders
        self.register(
            LoaderStrategy(
                strategy_name="gutenberg",
                loader_class="GutenbergLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["gutenberg", "books", "literature"],
                requires_dependencies=[],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="mastodon",
                loader_class="MastodonTootsLoader",
                speed="medium",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                ],
                best_for=["mastodon", "fediverse", "social"],
                requires_dependencies=["mastodon.py"],
                requires_authentication=True,
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="mediawiki",
                loader_class="MWDumpLoader",
                speed="slow",
                quality="high",
                resource_usage="high",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.METADATA,
                    LoaderCapability.BATCHING,
                ],
                best_for=["mediawiki", "wiki", "dump"],
                requires_dependencies=["mwparserfromhell", "mwxml"],
                priority=LoaderPriority.MEDIUM,
            )
        )

        self.register(
            LoaderStrategy(
                strategy_name="duckdb",
                loader_class="DuckDBLoader",
                speed="fast",
                quality="high",
                resource_usage="low",
                capabilities=[
                    LoaderCapability.TEXT_EXTRACTION,
                    LoaderCapability.TABLE_EXTRACTION,
                ],
                best_for=["duckdb", "analytics", "sql"],
                requires_dependencies=["duckdb"],
                priority=LoaderPriority.HIGH,
            )
        )

    def register(self, strategy: LoaderStrategy):
        """Register a new loader strategy."""
        # Check availability when registering
        strategy.is_available = strategy.check_availability()
        self._strategies[strategy.strategy_name] = strategy

        logger.debug(
            f"Registered loader strategy: {strategy.strategy_name} "
            f"(available: {strategy.is_available})"
        )

    def get_strategy(self, name: str) -> Optional[LoaderStrategy]:
        """Get a strategy by name."""
        return self._strategies.get(name)

    def list_strategies(self, available_only: bool = True) -> List[LoaderStrategy]:
        """List all strategies."""
        strategies = list(self._strategies.values())
        if available_only:
            strategies = [s for s in strategies if s.is_available]
        return strategies

    def find_strategies_for_source(
        self, source: EnhancedSource, preferences: Optional[Dict[str, Any]] = None
    ) -> List[LoaderStrategy]:
        """Find suitable strategies for a source."""
        if preferences is None:
            preferences = {}

        suitable_strategies = []

        for strategy in self._strategies.values():
            if not strategy.is_available:
                continue

            # Check if strategy is suitable for this source type
            source_type_str = source.source_type.value
            if strategy.best_for and source_type_str not in strategy.best_for:
                # Check for file extension match
                if hasattr(source, "source_path"):
                    from pathlib import Path

                    ext = Path(source.source_path).suffix.lower().lstrip(".")
                    if ext not in strategy.best_for:
                        continue
                else:
                    continue

            # Check authentication requirements
            if (
                strategy.requires_authentication
                and not source.requires_authentication()
            ):
                continue

            # Apply preferences
            if preferences.get("prefer_speed") and strategy.speed != "fast":
                continue
            if preferences.get("prefer_quality") and strategy.quality != "high":
                continue
            if preferences.get("require_async") and not strategy.supports_async:
                continue

            suitable_strategies.append(strategy)

        # Sort by priority and quality
        suitable_strategies.sort(
            key=lambda s: (
                s.priority.value,
                {"high": 3, "medium": 2, "low": 1}[s.quality],
                {"fast": 3, "medium": 2, "slow": 1}[s.speed],
            ),
            reverse=True,
        )

        return suitable_strategies

    def select_best_strategy(
        self, source: EnhancedSource, preferences: Optional[Dict[str, Any]] = None
    ) -> Optional[LoaderStrategy]:
        """Select the best strategy for a source."""
        strategies = self.find_strategies_for_source(source, preferences)
        return strategies[0] if strategies else None


# Global registry instance
strategy_registry = LoaderStrategyRegistry()


def create_loader(
    source: EnhancedSource,
    strategy_name: Optional[str] = None,
    options: Optional[Dict[str, Any]] = None,
    preferences: Optional[Dict[str, Any]] = None,
) -> Optional[BaseLoader]:
    """Create a loader for the given source."""
    if options is None:
        options = {}

    if strategy_name:
        # Use specific strategy
        strategy = strategy_registry.get_strategy(strategy_name)
        if not strategy:
            logger.error(f"Strategy {strategy_name} not found")
            return None
        if not strategy.is_available:
            logger.error(f"Strategy {strategy_name} not available")
            return None
    else:
        # Auto-select best strategy
        strategy = strategy_registry.select_best_strategy(source, preferences)
        if not strategy:
            logger.error(
                f"No suitable strategy found for source type {source.source_type}"
            )
            return None

    return strategy.create_loader(source, options)


# Export key components
__all__ = [
    "LoaderPriority",
    "LoaderCapability",
    "LoaderStrategy",
    "LoaderStrategyRegistry",
    "strategy_registry",
    "create_loader",
]
