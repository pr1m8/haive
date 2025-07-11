"""Universal Document Loader with Auto-Detection.

This module provides a comprehensive universal loader that automatically detects
the best loader for any given input (URL, file path, text, etc.) and can
handle preferences for optimal loader selection.
"""

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from urllib.parse import urlparse

from langchain_core.document_loaders.base import BaseLoader

from haive.core.engine.document.factory import AutoLoaderFactory
from haive.core.engine.document.loaders.sources.implementation import CredentialManager
from haive.core.engine.document.loaders.specific.cloud import (
    AzureBlobSource,
    GCSSource,
    S3Source,
)
from haive.core.engine.document.loaders.specific.database import (
    MongoDBSource,
    PostgreSQLSource,
)
from haive.core.engine.document.loaders.specific.files_code import (
    CppSource,
    GoSource,
    JavaScriptSource,
    JavaSource,
    JupyterNotebookSource,
    PythonCodeSource,
    RubySource,
    RustSource,
    ShellScriptSource,
)
from haive.core.engine.document.loaders.specific.files_data import (
    CSVSource,
    JSONSource,
    TOMLSource,
    TSVSource,
    XMLSource,
    YAMLSource,
)
from haive.core.engine.document.loaders.specific.files_media import (
    CHMSource,
    EPubSource,
    HTMLSource,
    ImageSource,
    MHTMLSource,
    PDFSource,
    SubtitleSource,
)
from haive.core.engine.document.loaders.specific.files_office import (
    ExcelSource,
    ODPSource,
    ODSSource,
    ODTSource,
    PowerPointSource,
    RTFSource,
    WordDocumentSource,
)
from haive.core.engine.document.loaders.specific.files_scientific import (
    BibtexSource,
    CONLLUSource,
    FortranSource,
    MathMLSource,
    MatlabSource,
    RSource,
)
from haive.core.engine.document.loaders.specific.files_text import (
    AsciiDocSource,
    LaTeXSource,
    MarkdownSource,
    OrgModeSource,
    ReStructuredTextSource,
    TextFileSource,
)
from haive.core.engine.document.loaders.specific.services import (
    NotionDBSource,
    ObsidianSource,
)

# Import all specific sources for registration
from haive.core.engine.document.loaders.specific.web import (
    ArXivSource,
    BasicWebSource,
    GitHubSource,
    PlaywrightWebSource,
    WikipediaSource,
)
from haive.core.engine.document.loaders.specific.web_api import (
    ApifyDatasetSource,
    AssemblyAITranscriptSource,
    BraveSearchSource,
    DiffbotSource,
    EtherscanSource,
    GoogleSearchSource,
    NewsAPISource,
    ScrapflySource,
    ScrapingBeeSource,
)
from haive.core.engine.document.loaders.specific.web_github_enhanced import (
    GitHubActionsSource,
    GitHubDiscussionsSource,
    GitHubGistsSource,
    GitHubReleasesSource,
    GitHubWikiSource,
)
from haive.core.engine.document.loaders.specific.web_huggingface_enhanced import (
    HuggingFaceCollectionsSource,
    HuggingFaceExtendedDatasetSource,
    HuggingFaceModelCardSource,
    HuggingFaceOrganizationsSource,
    HuggingFacePapersSource,
)
from haive.core.engine.document.loaders.specific.web_social import (
    BiliBiliSource,
    DiscordSource,
    FacebookChatSource,
    HackerNewsSource,
    IFixitSource,
    IMSDbSource,
    MastodonSource,
    RedditSource,
    TwitterSource,
    WhatsAppSource,
)

logger = logging.getLogger(__name__)


class SmartSourceRegistry:
    """Enhanced source registry with intelligent matching."""

    def __init__(self):
        self._sources: List[Tuple[type, float, List[str]]] = []
        self._domain_patterns: Dict[str, List[Tuple[type, float]]] = {}
        self._extension_patterns: Dict[str, List[Tuple[type, float]]] = {}
        self._url_patterns: Dict[str, List[Tuple[type, float]]] = {}
        self._register_all_sources()

    def _register_all_sources(self):
        """Register all available source types with their patterns and priorities."""

        # Web sources with domain-specific matching
        web_sources = [
            # GitHub ecosystem
            (GitHubSource, 0.95, ["github.com"]),
            (GitHubDiscussionsSource, 0.97, ["github.com/*/discussions"]),
            (GitHubGistsSource, 0.97, ["gist.github.com"]),
            (GitHubReleasesSource, 0.96, ["github.com/*/releases"]),
            (GitHubActionsSource, 0.96, ["github.com/*/actions"]),
            (GitHubWikiSource, 0.96, ["github.com/*/wiki"]),
            # HuggingFace ecosystem
            (HuggingFaceExtendedDatasetSource, 0.95, ["huggingface.co/datasets"]),
            (HuggingFaceModelCardSource, 0.95, ["huggingface.co"]),
            (HuggingFacePapersSource, 0.90, ["huggingface.co/papers"]),
            (HuggingFaceCollectionsSource, 0.90, ["huggingface.co/collections"]),
            (HuggingFaceOrganizationsSource, 0.90, ["huggingface.co/organizations"]),
            # Social media and communities
            (RedditSource, 0.95, ["reddit.com", "old.reddit.com"]),
            (HackerNewsSource, 0.95, ["news.ycombinator.com"]),
            (TwitterSource, 0.95, ["twitter.com", "x.com"]),
            (DiscordSource, 0.90, ["discord.com", "discord.gg"]),
            (MastodonSource, 0.90, ["mastodon.social", "mastodon.online"]),
            (BiliBiliSource, 0.95, ["bilibili.com", "www.bilibili.com"]),
            # Academic and reference
            (ArXivSource, 0.95, ["arxiv.org"]),
            (WikipediaSource, 0.95, ["wikipedia.org"]),
            # Technical and repair
            (IFixitSource, 0.95, ["ifixit.com"]),
            (IMSDbSource, 0.95, ["imsdb.com"]),
            # API services
            (NewsAPISource, 0.80, ["newsapi.org"]),
            (EtherscanSource, 0.95, ["etherscan.io"]),
            # General web (lower priority)
            (PlaywrightWebSource, 0.70, []),  # JavaScript-heavy sites
            (BasicWebSource, 0.50, []),  # Fallback for any web URL
        ]

        # File sources with extension matching
        file_sources = [
            # Office documents
            (WordDocumentSource, 0.95, [".docx", ".doc"]),
            (ExcelSource, 0.95, [".xlsx", ".xls"]),
            (PowerPointSource, 0.95, [".pptx", ".ppt"]),
            (ODTSource, 0.95, [".odt"]),
            (ODSSource, 0.95, [".ods"]),
            (ODPSource, 0.95, [".odp"]),
            (RTFSource, 0.95, [".rtf"]),
            # Data formats
            (CSVSource, 0.95, [".csv"]),
            (TSVSource, 0.95, [".tsv", ".tab"]),
            (JSONSource, 0.95, [".json", ".jsonl"]),
            (XMLSource, 0.95, [".xml"]),
            (YAMLSource, 0.95, [".yaml", ".yml"]),
            (TOMLSource, 0.95, [".toml"]),
            # Programming files
            (PythonCodeSource, 0.95, [".py", ".pyw"]),
            (JupyterNotebookSource, 0.95, [".ipynb"]),
            (JavaScriptSource, 0.95, [".js", ".jsx", ".ts", ".tsx", ".mjs"]),
            (CppSource, 0.95, [".cpp", ".cc", ".cxx", ".c++", ".hpp", ".h", ".hxx"]),
            (JavaSource, 0.95, [".java"]),
            (GoSource, 0.95, [".go"]),
            (RustSource, 0.95, [".rs"]),
            (RubySource, 0.95, [".rb"]),
            (ShellScriptSource, 0.95, [".sh", ".bash", ".zsh", ".fish"]),
            # Text formats
            (MarkdownSource, 0.95, [".md", ".markdown"]),
            (ReStructuredTextSource, 0.95, [".rst", ".rest"]),
            (LaTeXSource, 0.95, [".tex", ".latex"]),
            (OrgModeSource, 0.95, [".org"]),
            (AsciiDocSource, 0.95, [".adoc", ".asciidoc", ".asc"]),
            (TextFileSource, 0.90, [".txt", ".text", ".log"]),
            # Media files
            (PDFSource, 0.95, [".pdf"]),
            (
                ImageSource,
                0.95,
                [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"],
            ),
            (SubtitleSource, 0.95, [".srt", ".vtt", ".sub", ".ass"]),
            (EPubSource, 0.95, [".epub"]),
            (HTMLSource, 0.95, [".html", ".htm"]),
            (MHTMLSource, 0.95, [".mhtml", ".mht"]),
            (CHMSource, 0.95, [".chm"]),
            # Scientific formats
            (BibtexSource, 0.95, [".bib", ".bibtex"]),
            (CONLLUSource, 0.95, [".conllu", ".conll"]),
            (MathMLSource, 0.95, [".mml", ".mathml"]),
            (FortranSource, 0.95, [".f", ".for", ".f90", ".f95", ".f03", ".f08"]),
            (MatlabSource, 0.95, [".m", ".mat"]),
            (RSource, 0.95, [".r", ".R", ".Rmd", ".Rnw"]),
        ]

        # Database sources
        database_sources = [
            (PostgreSQLSource, 0.95, ["postgresql://", "postgres://"]),
            (MongoDBSource, 0.95, ["mongodb://", "mongodb+srv://"]),
        ]

        # Cloud sources
        cloud_sources = [
            (S3Source, 0.95, ["s3://", "https://s3.", ".amazonaws.com"]),
            (GCSSource, 0.95, ["gs://", "googleapis.com"]),
            (AzureBlobSource, 0.95, ["https://", ".blob.core.windows.net"]),
        ]

        # Service sources
        service_sources = [
            (NotionDBSource, 0.95, ["notion.so", "notion.com"]),
            (ObsidianSource, 0.95, [".obsidian"]),
        ]

        # Register all sources
        for source_type, priority, patterns in (
            web_sources
            + file_sources
            + database_sources
            + cloud_sources
            + service_sources
        ):
            self._sources.append((source_type, priority, patterns))

            # Build lookup tables for faster matching
            for pattern in patterns:
                if pattern.startswith("."):
                    # File extension
                    if pattern not in self._extension_patterns:
                        self._extension_patterns[pattern] = []
                    self._extension_patterns[pattern].append((source_type, priority))
                elif "://" in pattern:
                    # URL scheme
                    if pattern not in self._url_patterns:
                        self._url_patterns[pattern] = []
                    self._url_patterns[pattern].append((source_type, priority))
                else:
                    # Domain or URL pattern
                    if pattern not in self._domain_patterns:
                        self._domain_patterns[pattern] = []
                    self._domain_patterns[pattern].append((source_type, priority))

    def find_best_sources(self, path: str, limit: int = 3) -> List[Tuple[type, float]]:
        """Find the best source types for a given path."""
        candidates = []

        # Parse the path
        parsed_url = urlparse(path)
        path_obj = Path(path)

        # Check URL patterns
        if parsed_url.scheme:
            # Check scheme patterns
            scheme_pattern = f"{parsed_url.scheme}://"
            if scheme_pattern in self._url_patterns:
                candidates.extend(self._url_patterns[scheme_pattern])

            # Check domain patterns
            domain = parsed_url.netloc.lower()
            for pattern, sources in self._domain_patterns.items():
                if pattern in domain or any(
                    part in domain for part in pattern.split("/")
                ):
                    candidates.extend(sources)

            # Check URL path patterns
            full_url = path.lower()
            for pattern, sources in self._domain_patterns.items():
                if "/" in pattern and pattern in full_url:
                    # Boost priority for specific path matches
                    candidates.extend([(src, prio + 0.05) for src, prio in sources])

        # Check file extension patterns
        if path_obj.suffix:
            ext = path_obj.suffix.lower()
            if ext in self._extension_patterns:
                candidates.extend(self._extension_patterns[ext])

        # Check for special cases
        candidates.extend(self._check_special_cases(path))

        # Remove duplicates and sort by priority
        seen = set()
        unique_candidates = []
        for source_type, priority in candidates:
            if source_type not in seen:
                seen.add(source_type)
                unique_candidates.append((source_type, priority))

        # Sort by priority (highest first)
        unique_candidates.sort(key=lambda x: x[1], reverse=True)

        return unique_candidates[:limit]

    def _check_special_cases(self, path: str) -> List[Tuple[type, float]]:
        """Check for special case patterns that need custom logic."""
        candidates = []

        # Chat file exports (usually text files with specific content)
        if any(keyword in path.lower() for keyword in ["whatsapp", "telegram", "chat"]):
            if "whatsapp" in path.lower():
                candidates.append((WhatsAppSource, 0.90))
            if "telegram" in path.lower():
                # Telegram could be chat export or web
                candidates.append((WhatsAppSource, 0.85))  # Generic chat handler

        # Check for database connection strings
        if any(
            db in path.lower() for db in ["postgresql", "postgres", "mongodb", "mysql"]
        ):
            if "postgresql" in path.lower() or "postgres" in path.lower():
                candidates.append((PostgreSQLSource, 0.95))
            elif "mongodb" in path.lower():
                candidates.append((MongoDBSource, 0.95))

        # Check for file system paths that might be directories
        if not urlparse(path).scheme and Path(path).is_dir():
            # Could be Obsidian vault or other directory-based sources
            if any(file.name == ".obsidian" for file in Path(path).rglob("*")):
                candidates.append((ObsidianSource, 0.95))

        return candidates


class UniversalDocumentLoader:
    """Universal document loader with intelligent source detection."""

    def __init__(self, credential_manager: Optional[CredentialManager] = None):
        """Initialize the universal loader.

        Args:
            credential_manager: Optional credential manager for authenticated sources
        """
        self.credential_manager = credential_manager or CredentialManager()
        self.source_registry = SmartSourceRegistry()
        self.factory = AutoLoaderFactory(self.credential_manager)

    def load(
        self,
        path: str,
        preferences: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None,
        strategy: Optional[str] = None,
        fallback: bool = True,
    ) -> Optional[BaseLoader]:
        """Load documents from any source with intelligent detection.

        Args:
            path: File path, URL, or source identifier
            preferences: Preferences for loader selection
            options: Loader-specific options
            strategy: Force a specific strategy
            fallback: Whether to use fallback loaders

        Returns:
            Appropriate document loader or None

        Examples:
            >>> loader = UniversalDocumentLoader()
            >>>
            >>> # Auto-detect and load
            >>> doc_loader = loader.load("https://github.com/user/repo")
            >>> doc_loader = loader.load("document.pdf")
            >>> doc_loader = loader.load("data.csv")
            >>>
            >>> # With preferences
            >>> doc_loader = loader.load(
            ...     "https://example.com",
            ...     preferences={"web_strategy": "playwright", "include_images": True}
            ... )
        """
        if preferences is None:
            preferences = {}
        if options is None:
            options = {}

        logger.info(f"Loading document from: {path}")

        # Find the best sources for this path
        source_candidates = self.source_registry.find_best_sources(path)

        if not source_candidates:
            logger.warning(
                f"No specific sources found for {path}, using generic factory"
            )
            if fallback:
                return self.factory.create_loader(path, strategy, options, preferences)
            return None

        # Try each source candidate in order of priority
        for source_type, confidence in source_candidates:
            try:
                logger.info(
                    f"Trying {source_type.__name__} (confidence: {confidence:.2f})"
                )

                # Create source instance
                source_instance = self._create_source_instance(
                    source_type, path, options, preferences
                )

                if source_instance:
                    # Create loader from source
                    loader = source_instance.create_loader()
                    if loader:
                        logger.info(
                            f"Successfully created loader using {source_type.__name__}"
                        )
                        return loader
                    else:
                        logger.warning(
                            f"{source_type.__name__} could not create loader"
                        )
                else:
                    logger.warning(f"Could not create {source_type.__name__} instance")

            except Exception as e:
                logger.warning(
                    f"Failed to create loader with {source_type.__name__}: {e}"
                )
                continue

        # If all specific sources failed, try the generic factory
        if fallback:
            logger.info("All specific sources failed, trying generic factory")
            return self.factory.create_loader(path, strategy, options, preferences)

        logger.error(f"Failed to create any loader for {path}")
        return None

    def _create_source_instance(
        self,
        source_type: type,
        path: str,
        options: Dict[str, Any],
        preferences: Dict[str, Any],
    ) -> Optional[Any]:
        """Create an instance of a specific source type."""
        try:
            # Extract relevant parameters for the source
            source_kwargs = self._extract_source_kwargs(
                source_type, path, options, preferences
            )

            # Add credential manager
            source_kwargs["credential_manager"] = self.credential_manager

            # Create the source instance
            return source_type(**source_kwargs)

        except Exception as e:
            logger.error(f"Failed to create {source_type.__name__} instance: {e}")
            return None

    def _extract_source_kwargs(
        self,
        source_type: type,
        path: str,
        options: Dict[str, Any],
        preferences: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Extract appropriate kwargs for a source type."""
        kwargs = {"source_path": path}

        # Add common parameters based on source type
        if "GitHub" in source_type.__name__:
            kwargs["repo_url"] = path
            if "include_issues" in preferences:
                kwargs["include_issues"] = preferences["include_issues"]
            if "include_pull_requests" in preferences:
                kwargs["include_pull_requests"] = preferences["include_pull_requests"]

        elif "Reddit" in source_type.__name__:
            # Extract subreddit from URL
            if "reddit.com/r/" in path:
                subreddit = path.split("/r/")[1].split("/")[0]
                kwargs["subreddit"] = subreddit
                kwargs["mode"] = "subreddit"

        elif "Twitter" in source_type.__name__:
            # Extract username from URL
            if "twitter.com/" in path or "x.com/" in path:
                username = path.split("/")[-1].split("?")[0]
                kwargs["username"] = username
                kwargs["mode"] = "user_timeline"

        elif "PDF" in source_type.__name__:
            kwargs["file_path"] = path
            if "pdf_strategy" in preferences:
                kwargs["strategy"] = preferences["pdf_strategy"]
            if "extract_images" in preferences:
                kwargs["extract_images"] = preferences["extract_images"]

        elif "CSV" in source_type.__name__:
            kwargs["file_path"] = path
            if "csv_args" in options:
                kwargs["csv_args"] = options["csv_args"]

        # Add any additional options
        for key, value in options.items():
            if key not in kwargs:
                kwargs[key] = value

        return kwargs

    def analyze_source(self, path: str) -> Dict[str, Any]:
        """Analyze a source and return information about available loaders."""
        source_candidates = self.source_registry.find_best_sources(path, limit=10)

        analysis = {
            "path": path,
            "candidates": [],
            "recommended": None,
            "supports_auth": False,
            "estimated_difficulty": "easy",
        }

        for source_type, confidence in source_candidates:
            candidate_info = {
                "source_type": source_type.__name__,
                "confidence": confidence,
                "description": source_type.__doc__ or "No description available",
            }

            # Check if source requires authentication
            try:
                temp_instance = source_type(source_path=path)
                if hasattr(temp_instance, "requires_authentication"):
                    candidate_info["requires_auth"] = (
                        temp_instance.requires_authentication()
                    )
                    if candidate_info["requires_auth"]:
                        analysis["supports_auth"] = True
                        analysis["estimated_difficulty"] = "medium"
            except:
                candidate_info["requires_auth"] = False

            analysis["candidates"].append(candidate_info)

        if source_candidates:
            analysis["recommended"] = source_candidates[0][0].__name__

        return analysis

    def get_supported_sources(self) -> List[str]:
        """Get list of all supported source types."""
        return [
            source_type.__name__ for source_type, _, _ in self.source_registry._sources
        ]


# Convenience functions
def load_document(
    path: str,
    credential_manager: Optional[CredentialManager] = None,
    preferences: Optional[Dict[str, Any]] = None,
    options: Optional[Dict[str, Any]] = None,
    strategy: Optional[str] = None,
) -> Optional[BaseLoader]:
    """Convenience function to load a document from any source.

    Args:
        path: File path, URL, or source identifier
        credential_manager: Optional credential manager
        preferences: Preferences for loader selection
        options: Loader-specific options
        strategy: Force a specific strategy

    Returns:
        Document loader or None
    """
    loader = UniversalDocumentLoader(credential_manager)
    return loader.load(path, preferences, options, strategy)


def analyze_document_source(path: str) -> Dict[str, Any]:
    """Analyze a document source and return information about available loaders.

    Args:
        path: Path to analyze

    Returns:
        Analysis information
    """
    loader = UniversalDocumentLoader()
    return loader.analyze_source(path)


# Export main components
__all__ = [
    "UniversalDocumentLoader",
    "SmartSourceRegistry",
    "load_document",
    "analyze_document_source",
]
