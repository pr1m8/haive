"""Source to Loader Mapping Functions.

This module provides functions for mapping sources to appropriate loaders.
It includes pre-defined mappings for common file types and source types.
"""

import logging
from pathlib import Path
from typing import Any

# Import from loader strategy
from loader_strategy import (
    LoaderStrategy,
    loader_registry,
)

# Import from path integration
from path_integration import (
    analyze_source,
)

# Import from source implementation (placeholder for now)
from source_implementation import (
    BaseSource,
    CloudSource,
    DatabaseSource,
    LocalSource,
    RemoteSource,
)

# Import from source registry
from source_registry import auto_source, registry

logger = logging.getLogger(__name__)


# File extension to loader mappings
FILE_EXTENSION_LOADER_MAP = {
    # Documents
    ".pdf": [
        ("pypdf_loader", "PyPDFLoader", "fast", "medium", ["text_heavy", "pdf"]),
        (
            "unstructured_pdf_loader",
            "UnstructuredPDFLoader",
            "medium",
            "high",
            ["scanned", "images", "pdf"],
        ),
    ],
    ".docx": [
        (
            "docx_loader",
            "UnstructuredWordDocumentLoader",
            "medium",
            "high",
            ["word", "docx"],
        ),
        ("docx2txt_loader", "Docx2txtLoader", "fast", "medium", ["word", "docx"]),
    ],
    ".doc": [
        (
            "doc_loader",
            "UnstructuredWordDocumentLoader",
            "medium",
            "high",
            ["word", "doc"],
        )
    ],
    ".pptx": [
        (
            "pptx_loader",
            "UnstructuredPowerPointLoader",
            "medium",
            "high",
            ["powerpoint", "presentation"],
        )
    ],
    ".xlsx": [
        (
            "xlsx_loader",
            "UnstructuredExcelLoader",
            "medium",
            "high",
            ["excel", "spreadsheet"],
        ),
        (
            "pandas_xlsx_loader",
            "PandasExcelLoader",
            "fast",
            "medium",
            ["excel", "spreadsheet"],
        ),
    ],
    ".xls": [
        (
            "xls_loader",
            "UnstructuredExcelLoader",
            "medium",
            "high",
            ["excel", "spreadsheet"],
        )
    ],
    ".odt": [
        (
            "odt_loader",
            "UnstructuredODTLoader",
            "medium",
            "high",
            ["document", "openoffice"],
        )
    ],
    # Text formats
    ".txt": [
        ("text_loader", "TextLoader", "fast", "medium", ["text", "plain"]),
        (
            "unstructured_text_loader",
            "UnstructuredFileLoader",
            "medium",
            "high",
            ["text", "plain"],
        ),
    ],
    ".csv": [
        ("csv_loader", "CSVLoader", "fast", "medium", ["csv", "tabular"]),
        (
            "unstructured_csv_loader",
            "UnstructuredCSVLoader",
            "medium",
            "high",
            ["csv", "tabular"],
        ),
    ],
    ".tsv": [
        ("csv_loader", "CSVLoader", "fast", "medium", ["tsv", "tabular"]),
        (
            "unstructured_csv_loader",
            "UnstructuredCSVLoader",
            "medium",
            "high",
            ["tsv", "tabular"],
        ),
    ],
    ".json": [
        ("json_loader", "JSONLoader", "fast", "high", ["json", "structured"]),
        (
            "unstructured_json_loader",
            "UnstructuredJSONLoader",
            "medium",
            "high",
            ["json", "structured"],
        ),
    ],
    ".jsonl": [
        ("jsonl_loader", "JSONLinesLoader", "fast", "high", ["jsonl", "structured"])
    ],
    ".md": [
        ("markdown_loader", "UnstructuredMarkdownLoader", "fast", "high", ["markdown"]),
        ("text_loader", "TextLoader", "fast", "medium", ["markdown", "text"]),
    ],
    ".rst": [
        (
            "restructuredtext_loader",
            "UnstructuredRSTLoader",
            "medium",
            "high",
            ["rst", "documentation"],
        )
    ],
    ".html": [
        ("bs_html_loader", "BSHTMLLoader", "fast", "medium", ["html", "web"]),
        (
            "unstructured_html_loader",
            "UnstructuredHTMLLoader",
            "medium",
            "high",
            ["html", "web"],
        ),
    ],
    ".htm": [
        ("bs_html_loader", "BSHTMLLoader", "fast", "medium", ["html", "web"]),
        (
            "unstructured_html_loader",
            "UnstructuredHTMLLoader",
            "medium",
            "high",
            ["html", "web"],
        ),
    ],
    ".xml": [
        (
            "unstructured_xml_loader",
            "UnstructuredXMLLoader",
            "medium",
            "high",
            ["xml", "structured"],
        )
    ],
    ".yaml": [
        (
            "yaml_loader",
            "UnstructuredYAMLLoader",
            "medium",
            "high",
            ["yaml", "configuration"],
        )
    ],
    ".yml": [
        (
            "yaml_loader",
            "UnstructuredYAMLLoader",
            "medium",
            "high",
            ["yaml", "configuration"],
        )
    ],
    # Code formats
    ".py": [("python_loader", "PythonLoader", "fast", "high", ["python", "code"])],
    ".js": [("text_loader", "TextLoader", "fast", "medium", ["javascript", "code"])],
    ".java": [("text_loader", "TextLoader", "fast", "medium", ["java", "code"])],
    ".ipynb": [
        ("notebook_loader", "NotebookLoader", "fast", "high", ["notebook", "jupyter"])
    ],
    # Other formats
    ".epub": [
        ("epub_loader", "UnstructuredEPubLoader", "medium", "high", ["ebook", "epub"])
    ],
    ".rtf": [
        ("rtf_loader", "UnstructuredRTFLoader", "medium", "high", ["rtf", "document"])
    ],
    ".eml": [("email_loader", "UnstructuredEmailLoader", "medium", "high", ["email"])],
    ".msg": [
        (
            "outlook_loader",
            "OutlookMessageLoader",
            "medium",
            "high",
            ["email", "outlook"],
        )
    ],
}

# Domain to loader mappings
DOMAIN_LOADER_MAP = {
    "github.com": [
        (
            "github_issues_loader",
            "GitHubIssuesLoader",
            "medium",
            "high",
            ["github", "issues"],
        ),
        (
            "github_repo_loader",
            "GitHubFileLoader",
            "medium",
            "high",
            ["github", "repository"],
        ),
    ],
    "youtube.com": [
        (
            "youtube_loader",
            "YoutubeLoader",
            "medium",
            "high",
            ["youtube", "video", "transcript"],
        ),
        (
            "youtube_audio_loader",
            "YoutubeAudioLoader",
            "slow",
            "medium",
            ["youtube", "audio"],
        ),
    ],
    "youtu.be": [
        (
            "youtube_loader",
            "YoutubeLoader",
            "medium",
            "high",
            ["youtube", "video", "transcript"],
        ),
        (
            "youtube_audio_loader",
            "YoutubeAudioLoader",
            "slow",
            "medium",
            ["youtube", "audio"],
        ),
    ],
    "arxiv.org": [
        (
            "arxiv_loader",
            "ArxivLoader",
            "medium",
            "high",
            ["arxiv", "research", "paper"],
        )
    ],
    "wikipedia.org": [
        (
            "wikipedia_loader",
            "WikipediaLoader",
            "fast",
            "high",
            ["wikipedia", "encyclopedia"],
        )
    ],
    "reddit.com": [
        ("reddit_loader", "RedditPostsLoader", "medium", "medium", ["reddit", "forum"])
    ],
    "twitter.com": [
        (
            "twitter_loader",
            "TwitterTweetLoader",
            "medium",
            "medium",
            ["twitter", "social"],
        )
    ],
    "linkedin.com": [
        ("web_base_loader", "WebBaseLoader", "fast", "medium", ["linkedin", "social"])
    ],
    "notion.so": [
        ("notion_loader", "NotionDBLoader", "medium", "high", ["notion", "database"])
    ],
    "docs.google.com": [
        (
            "google_docs_loader",
            "GoogleDriveLoader",
            "medium",
            "high",
            ["google", "document"],
        )
    ],
    "drive.google.com": [
        (
            "google_drive_loader",
            "GoogleDriveLoader",
            "medium",
            "high",
            ["google", "drive"],
        )
    ],
    "airtable.com": [
        (
            "airtable_loader",
            "AirtableLoader",
            "medium",
            "high",
            ["airtable", "database"],
        )
    ],
}

# Database type to loader mappings
DATABASE_LOADER_MAP = {
    "postgresql": [
        (
            "sql_database_loader",
            "SQLDatabaseLoader",
            "medium",
            "high",
            ["postgresql", "database"],
        )
    ],
    "mysql": [
        (
            "sql_database_loader",
            "SQLDatabaseLoader",
            "medium",
            "high",
            ["mysql", "database"],
        )
    ],
    "sqlite": [
        (
            "sql_database_loader",
            "SQLDatabaseLoader",
            "fast",
            "high",
            ["sqlite", "database"],
        )
    ],
    "mongodb": [
        ("mongodb_loader", "MongodbLoader", "medium", "high", ["mongodb", "database"])
    ],
    "elasticsearch": [
        (
            "elasticsearch_loader",
            "ElasticsearchLoader",
            "medium",
            "high",
            ["elasticsearch", "search"],
        )
    ],
}

# Cloud provider to loader mappings
CLOUD_LOADER_MAP = {
    "aws_s3": [
        ("s3_file_loader", "S3FileLoader", "medium", "high", ["s3", "file"]),
        (
            "s3_directory_loader",
            "S3DirectoryLoader",
            "slow",
            "high",
            ["s3", "directory"],
        ),
    ],
    "google_cloud": [
        ("gcs_file_loader", "GCSFileLoader", "medium", "high", ["gcs", "file"]),
        (
            "gcs_directory_loader",
            "GCSDirectoryLoader",
            "slow",
            "high",
            ["gcs", "directory"],
        ),
    ],
    "azure_blob": [
        (
            "azure_blob_loader",
            "AzureBlobStorageFileLoader",
            "fast",
            "high",
            ["azure", "file"],
        ),
        (
            "azure_container_loader",
            "AzureBlobStorageContainerLoader",
            "medium",
            "high",
            ["azure", "container"],
        ),
    ],
    "dropbox": [
        ("dropbox_loader", "DropboxLoader", "medium", "high", ["dropbox", "file"])
    ],
    "onedrive": [
        ("onedrive_loader", "OneDriveLoader", "medium", "high", ["onedrive", "file"])
    ],
}

# Generic web loaders
WEB_LOADERS = [
    ("web_base_loader", "WebBaseLoader", "fast", "medium", ["web", "html"]),
    (
        "playwright_loader",
        "PlaywrightURLLoader",
        "slow",
        "high",
        ["web", "javascript", "dynamic"],
    ),
    ("selenium_loader", "SeleniumURLLoader", "slow", "medium", ["web", "javascript"]),
    (
        "recursive_url_loader",
        "RecursiveUrlLoader",
        "slow",
        "high",
        ["web", "recursive"],
    ),
]

# Directory loaders
DIRECTORY_LOADERS = [
    ("directory_loader", "DirectoryLoader", "fast", "medium", ["directory", "mixed"]),
    (
        "pdf_directory_loader",
        "PyPDFDirectoryLoader",
        "fast",
        "medium",
        ["directory", "pdf"],
    ),
    (
        "notion_directory_loader",
        "NotionDirectoryLoader",
        "medium",
        "high",
        ["directory", "notion"],
    ),
    ("obsidian_loader", "ObsidianLoader", "medium", "high", ["directory", "obsidian"]),
]


def register_standard_loaders() -> None:
    """Register standard loaders with the registry."""
    # Register file extension loaders
    for ext, loaders in FILE_EXTENSION_LOADER_MAP.items():
        for loader_info in loaders:
            strategy_name, loader_class, speed, quality, best_for = loader_info
            loader_registry.register_strategy(
                LoaderStrategy(
                    strategy_name=strategy_name,
                    loader_class=loader_class,
                    module_path="langchain_community.document_loaders",
                    speed=speed,
                    quality=quality,
                    best_for=best_for,
                ),
                file_extensions=[ext],
            )

    # Register domain loaders
    for domain, loaders in DOMAIN_LOADER_MAP.items():
        for loader_info in loaders:
            strategy_name, loader_class, speed, quality, best_for = loader_info
            loader_registry.register_strategy(
                LoaderStrategy(
                    strategy_name=strategy_name,
                    loader_class=loader_class,
                    module_path="langchain_community.document_loaders",
                    speed=speed,
                    quality=quality,
                    best_for=best_for,
                ),
                source_types=[domain.replace(".", "_")],
            )

    # Register database loaders
    for db_type, loaders in DATABASE_LOADER_MAP.items():
        for loader_info in loaders:
            strategy_name, loader_class, speed, quality, best_for = loader_info
            loader_registry.register_strategy(
                LoaderStrategy(
                    strategy_name=strategy_name,
                    loader_class=loader_class,
                    module_path="langchain_community.document_loaders",
                    speed=speed,
                    quality=quality,
                    best_for=best_for,
                    requires_auth=True,
                    required_credentials=[f"{db_type}_credentials"],
                ),
                source_types=[f"{db_type}_database"],
            )

    # Register cloud loaders
    for cloud_provider, loaders in CLOUD_LOADER_MAP.items():
        for loader_info in loaders:
            strategy_name, loader_class, speed, quality, best_for = loader_info
            loader_registry.register_strategy(
                LoaderStrategy(
                    strategy_name=strategy_name,
                    loader_class=loader_class,
                    module_path="langchain_community.document_loaders",
                    speed=speed,
                    quality=quality,
                    best_for=best_for,
                    requires_auth=True,
                    required_credentials=[
                        f"{cloud_provider.split('_')[0]}_credentials"
                    ],
                ),
                source_types=[cloud_provider],
            )

    # Register web loaders
    for loader_info in WEB_LOADERS:
        strategy_name, loader_class, speed, quality, best_for = loader_info
        loader_registry.register_strategy(
            LoaderStrategy(
                strategy_name=strategy_name,
                loader_class=loader_class,
                module_path="langchain_community.document_loaders",
                speed=speed,
                quality=quality,
                best_for=best_for,
            ),
            source_types=["web", "url", "html"],
        )

    # Register directory loaders
    for loader_info in DIRECTORY_LOADERS:
        strategy_name, loader_class, speed, quality, best_for = loader_info
        loader_registry.register_strategy(
            LoaderStrategy(
                strategy_name=strategy_name,
                loader_class=loader_class,
                module_path="langchain_community.document_loaders",
                speed=speed,
                quality=quality,
                best_for=best_for,
            ),
            source_types=["directory"],
        )


def register_standard_sources() -> None:
    """Register standard source types with the registry."""
    # Register file sources
    for ext, loaders in FILE_EXTENSION_LOADER_MAP.items():
        # Get source type name from extension
        source_type = ext.lstrip(".").lower() + "_source"

        # Create a new source class dynamically
        @auto_source(source_type=source_type, file_extensions=[ext])
        class DynamicSource(LocalSource):
            """Dynamically created source for file extension."""

            file_path: Path | None = None

            class Config:
                file_extensions = [ext]
                loader_strategies = {
                    loader_info[0]: {
                        "class": loader_info[1],
                        "speed": loader_info[2],
                        "quality": loader_info[3],
                        "best_for": loader_info[4],
                    }
                    for loader_info in loaders
                }

    # Register domain sources
    for domain, loaders in DOMAIN_LOADER_MAP.items():
        # Get source type name from domain
        source_type = domain.replace(".", "_").lower() + "_source"

        # Create a new source class dynamically
        @auto_source(source_type=source_type, domain_patterns=[domain])
        class DynamicSource(RemoteSource):
            """Dynamically created source for domain."""

            url: str | None = None

            class Config:
                domain_patterns = [domain]
                loader_strategies = {
                    loader_info[0]: {
                        "class": loader_info[1],
                        "speed": loader_info[2],
                        "quality": loader_info[3],
                        "best_for": loader_info[4],
                    }
                    for loader_info in loaders
                }

    # Register database sources
    for db_type, loaders in DATABASE_LOADER_MAP.items():
        # Get source type name from database type
        source_type = db_type + "_database_source"

        # Create a new source class dynamically
        @auto_source(source_type=source_type, scheme_patterns=[db_type])
        class DynamicSource(DatabaseSource):
            """Dynamically created source for database."""

            connection_string: str | None = None

            class Config:
                scheme_patterns = [db_type]
                loader_strategies = {
                    loader_info[0]: {
                        "class": loader_info[1],
                        "speed": loader_info[2],
                        "quality": loader_info[3],
                        "best_for": loader_info[4],
                        "requires_auth": True,
                        "required_credentials": [f"{db_type}_credentials"],
                    }
                    for loader_info in loaders
                }
                required_credentials = [f"{db_type}_credentials"]

    # Register cloud sources
    for cloud_provider, loaders in CLOUD_LOADER_MAP.items():
        # Get source type name from cloud provider
        source_type = cloud_provider + "_source"

        # Create a new source class dynamically
        @auto_source(source_type=source_type)
        class DynamicSource(CloudSource):
            """Dynamically created source for cloud provider."""

            bucket_name: str | None = None
            object_key: str | None = None

            class Config:
                cloud_providers = [cloud_provider]
                loader_strategies = {
                    loader_info[0]: {
                        "class": loader_info[1],
                        "speed": loader_info[2],
                        "quality": loader_info[3],
                        "best_for": loader_info[4],
                        "requires_auth": True,
                        "required_credentials": [
                            f"{cloud_provider.split('_')[0]}_credentials"
                        ],
                    }
                    for loader_info in loaders
                }
                required_credentials = [f"{cloud_provider.split('_')[0]}_credentials"]


def get_loader_for_source(
    source: str | Path | dict[str, Any] | BaseSource,
    strategy_name: str | None = None,
    options: dict[str, Any] | None = None,
) -> Any:
    """Get a loader for a source.

    Args:
        source: The source to load documents from
        strategy_name: Optional explicit strategy name
        options: Options for the loader

    Returns:
        A loader instance

    Raises:
        ValueError: If no suitable loader is found
    """
    options = options or {}

    # Analyze the source
    if isinstance(source, BaseSource):
        source_instance = source
        analysis = analyze_source(
            getattr(source, "file_path", None)
            or getattr(source, "url", None)
            or getattr(source, "connection_string", None)
            or str(source)
        )
    else:
        # Analyze and resolve the source
        from path_integration import analyze_and_resolve_source

        source_instance, analysis = analyze_and_resolve_source(source)

    # Get loader strategy
    if strategy_name:
        strategy = loader_registry.get_strategy(strategy_name)
        if not strategy:
            raise ValueError(f"Loader strategy '{strategy_name}' not found")
    else:
        # Select best strategy
        strategy = loader_registry.select_strategy(source_instance, analysis)
        if not strategy:
            raise ValueError(f"No suitable loader strategy found for {source}")

    # Create loader
    return strategy.create_loader(source_instance, options)


def get_loaders_for_file_extension(extension: str) -> list[LoaderStrategy]:
    """Get all loader strategies for a file extension.

    Args:
        extension: The file extension (with or without leading dot)

    Returns:
        List of loader strategies
    """
    if not extension.startswith("."):
        extension = f".{extension}"

    return loader_registry.get_strategies_for_extension(extension)


def get_loaders_for_source_type(source_type: str) -> list[LoaderStrategy]:
    """Get all loader strategies for a source type.

    Args:
        source_type: The source type

    Returns:
        List of loader strategies
    """
    return loader_registry.get_strategies_for_source(source_type)


def get_best_loader_for_path(
    path: str | Path, preference: str | None = None
) -> LoaderStrategy | None:
    """Get the best loader strategy for a path.

    Args:
        path: The path to analyze
        preference: Optional preference ('speed', 'quality', or 'balanced')

    Returns:
        The best loader strategy, or None if no suitable strategy is found
    """
    # Analyze the path
    analysis = analyze_source(path)

    # Get source type
    source_type = None
    matches = registry.find_matching_sources(analysis)
    if matches:
        source_type, _ = matches[0]

    if not source_type:
        return None

    # Create source instance
    source_instance = registry.create_source(source_type, analysis)
    if not source_instance:
        return None

    # Prepare preferences
    preferences = {}
    if preference == "speed":
        preferences["prefer_speed"] = True
    elif preference == "quality":
        preferences["prefer_quality"] = True

    # Select best strategy
    return loader_registry.select_strategy(source_instance, analysis, preferences)


# Initialize registries
def initialize_registries():
    """Initialize the source and loader registries."""
    register_standard_sources()
    register_standard_loaders()


# Export all components
__all__ = [
    "CLOUD_LOADER_MAP",
    "DATABASE_LOADER_MAP",
    "DIRECTORY_LOADERS",
    "DOMAIN_LOADER_MAP",
    "FILE_EXTENSION_LOADER_MAP",
    "WEB_LOADERS",
    "get_best_loader_for_path",
    "get_loader_for_source",
    "get_loaders_for_file_extension",
    "get_loaders_for_source_type",
    "initialize_registries",
    "register_standard_loaders",
    "register_standard_sources",
]
