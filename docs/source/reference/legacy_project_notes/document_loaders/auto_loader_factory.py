"""Auto Loader Factory for Document Sources

This module provides a comprehensive factory interface that can analyze any path or URL
and automatically select the appropriate document source and loader.
"""

from typing import Any

# Import all source types
from .document_loaders import (
    DirectorySource,
    EmailSource,
    EPubSource,
    ExcelSource,
    GitHubSource,
    HTMLSource,
    ImageSource,
    OpenDocumentSource,
    PDFSource,
    PostgreSQLSource,
    PowerPointSource,
    RTFSource,
    S3Source,
    WikipediaSource,
    WordDocumentSource,
    YouTubeSource,
)
from .path_analysis_implementation import analyze_path_comprehensive
from .source_implementation import CredentialManager, registry

# Import text-based source types
from .specific_loaders.text_loaders import (
    ConfigFileSource,
    CSVSource,
    JSONSource,
    LogFileSource,
    MarkdownSource,
    TextSource,
    TomlSource,
    XMLSource,
    YAMLSource,
)


def create_document_loader(
    path: str,
    strategy: str | None = None,
    credential_manager: CredentialManager | None = None,
    metadata: dict[str, Any] | None = None,
) -> Any:
    """Create the appropriate document loader for any path or URL.

    This factory function analyzes the given path to determine its nature (file, URL,
    database URI, etc.) and returns the appropriate loader instance. It leverages
    the source type registry and path analysis system to make intelligent decisions.

    Args:
        path: File path, URL, or URI to load
        strategy: Optional specific strategy to use (e.g., 'fast', 'ocr', 'tables')
        credential_manager: Optional credential manager for authenticated sources
        metadata: Optional additional metadata to include with the documents

    Returns:
        DocumentLoader instance appropriate for the given path

    Examples:
        >>> # Load a PDF file with OCR
        >>> loader = create_document_loader("path/to/document.pdf", strategy="ocr")
        >>>
        >>> # Load a webpage
        >>> loader = create_document_loader("https://example.com")
        >>>
        >>> # Load an S3 object with credentials
        >>> loader = create_document_loader("s3://my-bucket/document.pdf",
        ...                                credential_manager=credential_manager)
    """
    # Analyze the path to determine its type
    analysis_result = analyze_path_comprehensive(path)

    # Add metadata if provided
    if metadata is None:
        metadata = {}

    # Find matching source types
    matches = registry.find_matching_sources(analysis_result)

    if not matches:
        # No specific match, try to infer from file extension or use a general loader
        if analysis_result.file_extension:
            # Try to find a loader based on file extension
            ext = analysis_result.file_extension.lower()

            # Document files
            if ext == ".pdf":
                return PDFSource(file_path=path).create_loader(strategy)
            if ext in [".doc", ".docx", ".dot", ".dotx"]:
                return WordDocumentSource(file_path=path).create_loader(strategy)
            if ext in [".xls", ".xlsx", ".xlsm", ".xlt", ".xltx"]:
                return ExcelSource(file_path=path).create_loader(strategy)
            if ext in [".ppt", ".pptx", ".pps", ".ppsx"]:
                return PowerPointSource(file_path=path).create_loader(strategy)

            # Text-based files
            if ext in [".txt", ".text"]:
                return TextSource(file_path=path).create_loader(strategy)
            if ext in [".md", ".markdown"]:
                return MarkdownSource(file_path=path).create_loader(strategy)
            if ext == ".csv":
                return CSVSource(file_path=path).create_loader(strategy)
            if ext in [".json", ".jsonl"]:
                return JSONSource(file_path=path).create_loader(strategy)
            if ext in [".yaml", ".yml"]:
                return YAMLSource(file_path=path).create_loader(strategy)
            if ext == ".xml":
                return XMLSource(file_path=path).create_loader(strategy)
            if ext == ".toml":
                return TomlSource(file_path=path).create_loader(strategy)
            if ext in [".ini", ".cfg", ".conf"]:
                return ConfigFileSource(file_path=path).create_loader(strategy)
            if ext in [".log", ".out", ".err"]:
                return LogFileSource(file_path=path).create_loader(strategy)

            # Web files
            if ext in [".html", ".htm"]:
                return HTMLSource(file_path=path).create_loader(strategy)

            # Media files
            if ext in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]:
                return ImageSource(file_path=path).create_loader(strategy)

            # Other document formats
            if ext in [".odt", ".ods", ".odp", ".odg", ".odf"]:
                return OpenDocumentSource(file_path=path).create_loader(strategy)
            if ext == ".epub":
                return EPubSource(file_path=path).create_loader(strategy)
            if ext == ".rtf":
                return RTFSource(file_path=path).create_loader(strategy)
            if ext in [".eml", ".msg"]:
                return EmailSource(file_path=path).create_loader(strategy)

            # Default to text loader for unknown extensions
            from langchain_community.document_loaders import TextLoader

            return TextLoader(path)

        # Handle directories
        if analysis_result.is_directory:
            return DirectorySource(directory_path=path).create_loader(strategy)

        # Handle web URLs
        if (
            analysis_result.url_components
            and analysis_result.url_components.scheme in ["http", "https"]
        ):
            # Check for known domains
            if analysis_result.domain_info:
                domain = analysis_result.domain_info.domain

                if "github.com" in domain:
                    return GitHubSource(url=path).create_loader(strategy)
                if "wikipedia.org" in domain:
                    return WikipediaSource(url=path).create_loader(strategy)
                if "youtube.com" in domain or "youtu.be" in domain:
                    return YouTubeSource(url=path).create_loader(strategy)

            # Default web loader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(path)

        # Handle database URIs
        if analysis_result.database_type:
            if str(analysis_result.database_type).startswith("POSTGRESQL"):
                return PostgreSQLSource(connection_string=path).create_loader(strategy)
            # Generic SQL loader
            try:
                from langchain_community.document_loaders import SQLDatabaseLoader
                from langchain_community.utilities import SQLDatabase

                db = SQLDatabase.from_uri(path)
                return SQLDatabaseLoader(db)
            except ImportError:
                raise ImportError("SQLDatabaseLoader requires SQLAlchemy")

        # Handle cloud storage
        elif analysis_result.cloud_provider:
            if str(analysis_result.cloud_provider) == "AWS_S3":
                if analysis_result.bucket_name:
                    if analysis_result.object_key:
                        return S3Source(
                            bucket_name=analysis_result.bucket_name,
                            key=analysis_result.object_key,
                        ).create_loader(strategy)
                    return S3Source(
                        bucket_name=analysis_result.bucket_name, prefix=""
                    ).create_loader("directory")

            # Default for other cloud providers
            from langchain_community.document_loaders import TextLoader

            return TextLoader(path)

        # Default to text loader as last resort
        else:
            from langchain_community.document_loaders import TextLoader

            return TextLoader(path)

    # Create source instance from best match
    source_type, confidence = matches[0]
    source = registry.create_source_instance(source_type, analysis_result)

    if not source:
        raise ValueError(f"Failed to create source instance for {source_type}")

    # Authenticate if needed
    if hasattr(source, "authenticate") and credential_manager:
        authenticated = source.authenticate(credential_manager)
        if (
            not authenticated
            and registry.source_metadata[source_type].required_credentials
        ):
            raise ValueError(f"Authentication failed for {source_type}")

    # Create loader with specified strategy
    return source.create_loader(strategy)


def load_documents_from_paths(
    paths: list[str],
    strategy: str | None = None,
    credential_manager: CredentialManager | None = None,
    metadata: dict[str, Any] | None = None,
) -> list[Any]:
    """Load documents from multiple paths.

    Args:
        paths: List of file paths, URLs, or URIs to load
        strategy: Optional specific strategy to use for all loaders
        credential_manager: Optional credential manager for authenticated sources
        metadata: Optional additional metadata to include with the documents

    Returns:
        List of loaded documents
    """
    documents = []

    for path in paths:
        try:
            loader = create_document_loader(
                path=path,
                strategy=strategy,
                credential_manager=credential_manager,
                metadata=metadata,
            )

            # Load documents
            if hasattr(loader, "load"):
                docs = loader.load()
                documents.extend(docs)
            else:
                # If loader is already the documents list (rare case)
                documents.extend(loader)

        except Exception as e:
            # Log the error but continue with other paths
            import logging

            logging.exception(f"Error loading documents from {path}: {e}")

    return documents


def analyze_path_and_suggest_loader(path: str) -> dict[str, Any]:
    """Analyze a path and suggest the appropriate loader without actually loading it.

    This is useful for debugging and for understanding what loader would be used
    for a given path.

    Args:
        path: File path, URL, or URI to analyze

    Returns:
        Dict with analysis results and suggested loader
    """
    # Analyze the path
    analysis = analyze_path_comprehensive(path)

    # Find matching source types
    matches = registry.find_matching_sources(analysis)

    result = {
        "path": path,
        "analysis": {
            "path_type": str(analysis.path_type),
            "is_local": analysis.is_local,
            "is_remote": analysis.is_remote,
            "file_extension": analysis.file_extension,
            "file_category": (
                str(analysis.file_category) if analysis.file_category else None
            ),
            "database_type": (
                str(analysis.database_type) if analysis.database_type else None
            ),
            "cloud_provider": (
                str(analysis.cloud_provider) if analysis.cloud_provider else None
            ),
        },
        "matches": [],
    }

    # Add matches
    for source_type, confidence in matches:
        metadata = registry.source_metadata.get(source_type)
        if metadata:
            strategies = [s.strategy_name for s in metadata.loader_strategies]
            result["matches"].append(
                {
                    "source_type": source_type,
                    "confidence": confidence,
                    "category": metadata.category,
                    "strategies": strategies,
                }
            )

    return result
