"""Document-based Loaders for Haive Framework

This module implements document-based loaders for various file formats including
PDF, Word, Excel, PowerPoint, and other document types. It builds on the source
type system to provide a comprehensive solution for loading documents from
any source.
"""

from pathlib import Path
from typing import Any

from pydantic import FilePath, HttpUrl

# Import path analysis for auto-detection
from .path_analysis_implementation import analyze_path_comprehensive
from .source_implementation import (
    CredentialManager,
    LocalSource,
    RemoteSource,
    auto_source,
    registry,
)


@auto_source
class PDFSource(LocalSource):
    """PDF document source with multiple extraction strategies."""

    file_path: FilePath
    ocr_enabled: bool = False
    extract_images: bool = False

    class Config:
        file_extensions = [".pdf"]
        loader_strategies = {
            "fast": {
                "class": "PyPDFLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["text_heavy"],
            },
            "ocr": {
                "class": "UnstructuredPDFLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["scanned", "images"],
            },
            "tables": {
                "class": "PDFPlumberLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["tables", "forms"],
            },
            "math": {
                "class": "MathpixPDFLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["equations", "math"],
            },
            "pymupdf": {
                "class": "PyMuPDFLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_layouts"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a PDF loader with the specified strategy."""
        # If no strategy specified, choose based on document characteristics
        if not strategy_name:
            if self.ocr_enabled:
                strategy_name = "ocr"
            else:
                strategy_name = "fast"

        # Create the appropriate loader
        if strategy_name == "fast":
            return self.create_fast_loader()
        if strategy_name == "ocr":
            return self.create_ocr_loader()
        if strategy_name == "tables":
            return self.create_tables_loader()
        if strategy_name == "math":
            return self.create_math_loader()
        if strategy_name == "pymupdf":
            return self.create_pymupdf_loader()
        # Default to fast loader
        return self.create_fast_loader()

    def create_fast_loader(self):
        """Create a PyPDFLoader for fast text extraction."""
        try:
            from langchain_community.document_loaders import PyPDFLoader

            return PyPDFLoader(str(self.file_path))
        except ImportError:
            # Try alternate PDF loaders if PyPDF is not available
            try:
                return self.create_pymupdf_loader()
            except ImportError:
                try:
                    return self.create_tables_loader()
                except ImportError:
                    # Fallback to a basic text loader
                    from langchain_community.document_loaders import TextLoader

                    return TextLoader(str(self.file_path))

    def create_ocr_loader(self):
        """Create an UnstructuredPDFLoader with OCR capabilities."""
        try:
            from langchain_community.document_loaders import UnstructuredPDFLoader

            return UnstructuredPDFLoader(
                str(self.file_path),
                mode="elements",
                strategy="fast" if not self.ocr_enabled else "ocr_only",
            )
        except ImportError:
            # Fallback to basic loader
            return self.create_fast_loader()

    def create_tables_loader(self):
        """Create a PDFPlumberLoader for better table extraction."""
        try:
            from langchain_community.document_loaders import PDFPlumberLoader

            return PDFPlumberLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic loader
            return self.create_fast_loader()

    def create_math_loader(self):
        """Create a MathpixPDFLoader for math equation extraction."""
        try:
            from langchain_community.document_loaders import MathpixPDFLoader

            return MathpixPDFLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic loader
            return self.create_fast_loader()

    def create_pymupdf_loader(self):
        """Create a PyMuPDFLoader for better PDF handling."""
        try:
            from langchain_community.document_loaders import PyMuPDFLoader

            return PyMuPDFLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic loader
            return self.create_fast_loader()


@auto_source
class WordDocumentSource(LocalSource):
    """Word document source for .doc and .docx files."""

    file_path: FilePath

    class Config:
        file_extensions = [".doc", ".docx", ".dot", ".dotx"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredWordDocumentLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_formatting"],
            },
            "docx2txt": {
                "class": "Docx2txtLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_documents"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a Word document loader with the specified strategy."""
        if strategy_name == "docx2txt":
            return self.create_docx2txt_loader()
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredWordDocumentLoader for comprehensive parsing."""
        try:
            from langchain_community.document_loaders import (
                UnstructuredWordDocumentLoader,
            )

            return UnstructuredWordDocumentLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to simpler loader
            return self.create_docx2txt_loader()

    def create_docx2txt_loader(self):
        """Create a Docx2txtLoader for simple text extraction."""
        try:
            from langchain_community.document_loaders import Docx2txtLoader

            return Docx2txtLoader(str(self.file_path))
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class ExcelSource(LocalSource):
    """Excel spreadsheet source for .xls and .xlsx files."""

    file_path: FilePath
    sheet_name: str | None = None

    class Config:
        file_extensions = [".xls", ".xlsx", ".xlsm", ".xlt", ".xltx"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredExcelLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_spreadsheets"],
            },
            "pandas": {
                "class": "DataFrameLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["data_analysis"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an Excel loader with the specified strategy."""
        if strategy_name == "pandas":
            return self.create_pandas_loader()
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredExcelLoader for comprehensive parsing."""
        try:
            from langchain_community.document_loaders import UnstructuredExcelLoader

            return UnstructuredExcelLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to pandas loader
            return self.create_pandas_loader()

    def create_pandas_loader(self):
        """Create a DataFrameLoader using pandas for Excel files."""
        try:
            from langchain_community.document_loaders import DataFrameLoader
            import pandas as pd

            # Read Excel file into pandas DataFrame
            if self.sheet_name:
                df = pd.read_excel(self.file_path, sheet_name=self.sheet_name)
            else:
                df = pd.read_excel(self.file_path)

            # Select a column for the page content
            # Use the first column as default
            page_content_column = df.columns[0] if len(df.columns) > 0 else None

            return DataFrameLoader(
                data_frame=df, page_content_column=page_content_column
            )
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class PowerPointSource(LocalSource):
    """PowerPoint presentation source for .ppt and .pptx files."""

    file_path: FilePath

    class Config:
        file_extensions = [".ppt", ".pptx", ".pps", ".ppsx"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredPowerPointLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["presentations"],
            }
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a PowerPoint loader."""
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredPowerPointLoader for presentations."""
        try:
            from langchain_community.document_loaders import (
                UnstructuredPowerPointLoader,
            )

            return UnstructuredPowerPointLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class HTMLSource(LocalSource):
    """HTML document source for web pages and HTML files."""

    file_path: FilePath | None = None
    url: HttpUrl | None = None

    class Config:
        file_extensions = [".html", ".htm"]
        loader_strategies = {
            "bs4": {
                "class": "BSHTMLLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["simple_html"],
            },
            "unstructured": {
                "class": "UnstructuredHTMLLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["complex_html"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an HTML loader with the specified strategy."""
        if strategy_name == "unstructured":
            return self.create_unstructured_loader()
        return self.create_bs4_loader()

    def create_bs4_loader(self):
        """Create a BSHTMLLoader using BeautifulSoup."""
        try:
            from langchain_community.document_loaders import BSHTMLLoader

            if self.file_path:
                return BSHTMLLoader(str(self.file_path))
            if self.url:
                from langchain_community.document_loaders import WebBaseLoader

                return WebBaseLoader(str(self.url))
            raise ValueError("Either file_path or url must be provided")
        except ImportError:
            # Fallback to unstructured loader
            try:
                return self.create_unstructured_loader()
            except ImportError:
                # Last resort: basic text loader
                from langchain_community.document_loaders import TextLoader

                if self.file_path:
                    return TextLoader(str(self.file_path))
                raise ValueError("File path required when BS4 is not available")

    def create_unstructured_loader(self):
        """Create an UnstructuredHTMLLoader for better HTML parsing."""
        try:
            from langchain_community.document_loaders import UnstructuredHTMLLoader

            if self.file_path:
                return UnstructuredHTMLLoader(str(self.file_path))
            if self.url:
                from langchain_community.document_loaders import UnstructuredURLLoader

                return UnstructuredURLLoader(urls=[str(self.url)])
            raise ValueError("Either file_path or url must be provided")
        except ImportError:
            # Fallback to BS4 loader
            return self.create_bs4_loader()


@auto_source
class ImageSource(LocalSource):
    """Image source with OCR capabilities."""

    file_path: FilePath
    enable_ocr: bool = True
    caption_model: str | None = None

    class Config:
        file_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]
        file_categories = ["image"]
        loader_strategies = {
            "ocr": {
                "class": "UnstructuredImageLoader",
                "speed": "slow",
                "quality": "medium",
                "best_for": ["text_in_images"],
            },
            "caption": {
                "class": "ImageCaptionLoader",
                "speed": "slow",
                "quality": "high",
                "best_for": ["image_content"],
                "requires_auth": True,
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an image loader with the specified strategy."""
        if strategy_name == "caption" or self.caption_model:
            return self.create_caption_loader()
        return self.create_ocr_loader()

    def create_ocr_loader(self):
        """Create an UnstructuredImageLoader for OCR."""
        try:
            from langchain_community.document_loaders import UnstructuredImageLoader

            return UnstructuredImageLoader(str(self.file_path), mode="elements")
        except ImportError:
            # If unstructured is not available, try a simpler approach
            try:
                from PIL import Image
                import pytesseract

                def extract_text_with_tesseract():
                    try:
                        img = Image.open(str(self.file_path))
                        text = pytesseract.image_to_string(img)
                        from langchain_core.documents import Document

                        return [
                            Document(
                                page_content=text,
                                metadata={"source": str(self.file_path)},
                            )
                        ]
                    except Exception as e:
                        raise ValueError(f"Failed to extract text from image: {e}")

                return extract_text_with_tesseract()
            except ImportError:
                # No OCR libraries available
                from langchain_core.documents import Document

                return [
                    Document(
                        page_content="[Image content - OCR not available]",
                        metadata={"source": str(self.file_path)},
                    )
                ]

    def create_caption_loader(self):
        """Create an ImageCaptionLoader for generating image descriptions."""
        try:
            from langchain_community.document_loaders import ImageCaptionLoader

            # Use the specified model or default
            model_name = self.caption_model or "Salesforce/blip-image-captioning-base"

            return ImageCaptionLoader(
                path_images=[str(self.file_path)], model_name=model_name
            )
        except ImportError:
            # Fallback to OCR if caption model is not available
            return self.create_ocr_loader()


@auto_source
class OpenDocumentSource(LocalSource):
    """OpenDocument format source for LibreOffice/OpenOffice files."""

    file_path: FilePath

    class Config:
        file_extensions = [".odt", ".ods", ".odp", ".odg", ".odf"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredODTLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["open_document"],
            }
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an OpenDocument loader."""
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredODTLoader for OpenDocument formats."""
        try:
            from langchain_community.document_loaders import UnstructuredODTLoader

            return UnstructuredODTLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class EPubSource(LocalSource):
    """EPUB e-book source."""

    file_path: FilePath

    class Config:
        file_extensions = [".epub"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredEPubLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["ebooks"],
            }
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an EPUB loader."""
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredEPubLoader for e-books."""
        try:
            from langchain_community.document_loaders import UnstructuredEPubLoader

            return UnstructuredEPubLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class RTFSource(LocalSource):
    """Rich Text Format document source."""

    file_path: FilePath

    class Config:
        file_extensions = [".rtf"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredRTFLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["rich_text"],
            }
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an RTF loader."""
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredRTFLoader for rich text documents."""
        try:
            from langchain_community.document_loaders import UnstructuredRTFLoader

            return UnstructuredRTFLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))


@auto_source
class EmailSource(LocalSource):
    """Email document source for .eml files."""

    file_path: FilePath

    class Config:
        file_extensions = [".eml", ".msg"]
        loader_strategies = {
            "unstructured": {
                "class": "UnstructuredEmailLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["emails"],
            },
            "outlook": {
                "class": "OutlookMessageLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["outlook_messages"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an email loader with the specified strategy."""
        file_ext = Path(self.file_path).suffix.lower()

        if strategy_name == "outlook" or file_ext == ".msg":
            return self.create_outlook_loader()
        return self.create_unstructured_loader()

    def create_unstructured_loader(self):
        """Create an UnstructuredEmailLoader."""
        try:
            from langchain_community.document_loaders import UnstructuredEmailLoader

            return UnstructuredEmailLoader(str(self.file_path), mode="elements")
        except ImportError:
            # Fallback to basic text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(str(self.file_path))

    def create_outlook_loader(self):
        """Create an OutlookMessageLoader for .msg files."""
        try:
            from langchain_community.document_loaders import OutlookMessageLoader

            return OutlookMessageLoader(str(self.file_path))
        except ImportError:
            # Fallback to unstructured loader
            return self.create_unstructured_loader()


@auto_source
class DirectorySource(LocalSource):
    """Directory source for loading multiple files."""

    directory_path: Path
    glob_pattern: str = "**/*"
    recursive: bool = True

    class Config:
        loader_strategies = {
            "basic": {
                "class": "DirectoryLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["mixed_files"],
            },
            "pdf": {
                "class": "PyPDFDirectoryLoader",
                "speed": "fast",
                "quality": "medium",
                "best_for": ["pdf_directories"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a directory loader with the specified strategy."""
        if strategy_name == "pdf":
            return self.create_pdf_directory_loader()
        return self.create_basic_directory_loader()

    def create_basic_directory_loader(self):
        """Create a DirectoryLoader for loading multiple files."""
        try:
            from langchain_community.document_loaders import DirectoryLoader

            # Create a function to determine loader type based on file extension
            def loader_factory(file_path: str):
                """Determine the appropriate loader based on file extension."""
                path_obj = Path(file_path)
                ext = path_obj.suffix.lower()

                # Create document source based on file extension
                try:
                    analysis = analyze_path_comprehensive(file_path)
                    matches = registry.find_matching_sources(analysis)

                    if matches:
                        # Create source instance
                        source_type, _ = matches[0]
                        source = registry.create_source_instance(source_type, analysis)

                        # Create loader
                        if source:
                            return source.create_loader()

                    # Fallback to text loader if no matches
                    from langchain_community.document_loaders import TextLoader

                    return TextLoader(file_path)
                except Exception:
                    # Default to text loader
                    from langchain_community.document_loaders import TextLoader

                    return TextLoader(file_path)

            return DirectoryLoader(
                str(self.directory_path),
                glob=self.glob_pattern,
                recursive=self.recursive,
                loader_cls=loader_factory,
            )
        except ImportError:
            # No fallback for directory loader
            raise ImportError(
                "DirectoryLoader not available. Please install langchain_community."
            )

    def create_pdf_directory_loader(self):
        """Create a PyPDFDirectoryLoader for PDF directories."""
        try:
            from langchain_community.document_loaders import PyPDFDirectoryLoader

            return PyPDFDirectoryLoader(
                str(self.directory_path),
                glob=self.glob_pattern,
                recursive=self.recursive,
            )
        except ImportError:
            # Fallback to basic directory loader
            return self.create_basic_directory_loader()


@auto_source(domain_patterns=["github.com"])
class GitHubSource(RemoteSource):
    """GitHub repository or issue source."""

    url: HttpUrl
    include_issues: bool = True
    include_prs: bool = True
    github_token: str | None = None

    class Config:
        loader_strategies = {
            "issues": {
                "class": "GitHubIssuesLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["issues", "discussions"],
                "requires_auth": True,
                "required_credentials": ["github_token"],
            },
            "file": {
                "class": "GithubFileLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["single_file"],
                "requires_auth": True,
                "required_credentials": ["github_token"],
            },
        }
        required_credentials = ["github_token"]

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a GitHub loader with the specified strategy."""
        # Choose strategy based on URL pattern
        url_str = str(self.url)
        if strategy_name == "file" or "/blob/" in url_str:
            return self.create_file_loader()
        return self.create_issues_loader()

    def create_issues_loader(self):
        """Create a GitHubIssuesLoader for GitHub issues."""
        try:
            from langchain_community.document_loaders import GitHubIssuesLoader

            # Get token from credential manager or instance
            token = None
            if self.credential_manager:
                creds = self.credential_manager.get_credential("github_token")
                if creds:
                    token = creds.get("value")

            if not token and self.github_token:
                token = self.github_token

            # Extract owner and repo from URL
            url_parts = str(self.url).split("github.com/")
            if len(url_parts) != 2:
                raise ValueError("Invalid GitHub URL")

            path_parts = url_parts[1].strip("/").split("/")
            if len(path_parts) < 2:
                raise ValueError("Invalid GitHub repository URL")

            owner, repo = path_parts[0], path_parts[1]

            return GitHubIssuesLoader(
                repo=repo,
                owner=owner,
                github_token=token,
                load_issues=self.include_issues,
                load_prs=self.include_prs,
            )
        except ImportError:
            # Fallback to WebBaseLoader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(url=str(self.url))

    def create_file_loader(self):
        """Create a GithubFileLoader for GitHub files."""
        try:
            from langchain_community.document_loaders import GithubFileLoader

            # Get token from credential manager or instance
            token = None
            if self.credential_manager:
                creds = self.credential_manager.get_credential("github_token")
                if creds:
                    token = creds.get("value")

            if not token and self.github_token:
                token = self.github_token

            url_str = str(self.url)

            # Try to parse the GitHub URL to extract components
            # Format: https://github.com/{owner}/{repo}/blob/{branch}/{path}
            if "github.com" not in url_str or "/blob/" not in url_str:
                raise ValueError("Invalid GitHub file URL")

            # Split URL to get parts
            parts = url_str.split("github.com/")[1].split("/blob/")
            if len(parts) != 2:
                raise ValueError("Invalid GitHub file URL format")

            repo_part = parts[0]  # owner/repo
            path_with_branch = parts[1]  # branch/path/to/file

            # Split repo part into owner and repo
            repo_parts = repo_part.split("/")
            if len(repo_parts) != 2:
                raise ValueError("Invalid GitHub repository format")

            owner, repo = repo_parts

            # Split path part into branch and path
            path_parts = path_with_branch.split("/", 1)
            if len(path_parts) != 2:
                raise ValueError("Invalid GitHub file path format")

            branch, file_path = path_parts

            return GithubFileLoader(
                repo=repo,
                owner=owner,
                path=file_path,
                branch=branch,
                github_token=token,
            )
        except ImportError:
            # Fallback to WebBaseLoader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(url=str(self.url))


@auto_source(domain_patterns=["wikipedia.org"])
class WikipediaSource(RemoteSource):
    """Wikipedia article source."""

    url: HttpUrl
    lang: str = "en"

    class Config:
        loader_strategies = {
            "wiki": {
                "class": "WikipediaLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["encyclopedia", "articles"],
            }
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a Wikipedia loader."""
        return self.create_wiki_loader()

    def create_wiki_loader(self):
        """Create a WikipediaLoader for Wikipedia articles."""
        try:
            from langchain_community.document_loaders import WikipediaLoader

            # Extract article title from URL
            url_str = str(self.url)

            # Determine language from URL or use default
            lang = self.lang
            if "wikipedia.org" in url_str:
                domain_parts = url_str.split("wikipedia.org")[0].split(".")
                if len(domain_parts) > 1 and domain_parts[-1] == "":
                    lang = domain_parts[-2]

            # Extract article title
            title = None
            if "/wiki/" in url_str:
                title = url_str.split("/wiki/")[1].split("#")[0].replace("_", " ")

            if not title:
                raise ValueError("Could not extract article title from URL")

            return WikipediaLoader(query=title, lang=lang, load_max_docs=1)
        except ImportError:
            # Fallback to WebBaseLoader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(url=str(self.url))


@auto_source(domain_patterns=["youtube.com", "youtu.be"])
class YouTubeSource(RemoteSource):
    """YouTube video source."""

    url: HttpUrl
    add_video_info: bool = True
    language: str = "en"

    class Config:
        loader_strategies = {
            "transcript": {
                "class": "YoutubeLoader",
                "speed": "fast",
                "quality": "high",
                "best_for": ["transcripts"],
            },
            "audio": {
                "class": "YoutubeAudioLoader",
                "speed": "slow",
                "quality": "medium",
                "best_for": ["audio"],
            },
        }

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a YouTube loader with the specified strategy."""
        if strategy_name == "audio":
            return self.create_audio_loader()
        return self.create_transcript_loader()

    def create_transcript_loader(self):
        """Create a YoutubeLoader for video transcripts."""
        try:
            from langchain_community.document_loaders import YoutubeLoader

            return YoutubeLoader.from_youtube_url(
                str(self.url),
                add_video_info=self.add_video_info,
                language=self.language,
            )
        except ImportError:
            # Fallback to WebBaseLoader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(url=str(self.url))

    def create_audio_loader(self):
        """Create a YoutubeAudioLoader for audio extraction."""
        try:
            # Create a temporary directory to store audio
            import tempfile

            from langchain_community.document_loaders import YoutubeAudioLoader

            output_dir = tempfile.mkdtemp()

            # Load audio from YouTube
            return YoutubeAudioLoader.from_youtube_url(
                youtube_url=str(self.url), output_dir=output_dir
            )
        except ImportError:
            # Fallback to transcript loader
            return self.create_transcript_loader()


@auto_source(scheme_patterns=["postgresql", "postgres"])
class PostgreSQLSource(LocalSource):
    """PostgreSQL database source."""

    connection_string: str
    query: str | None = None

    class Config:
        loader_strategies = {
            "sql": {
                "class": "SQLDatabaseLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["database"],
                "requires_auth": True,
                "required_credentials": ["postgres_credentials"],
            }
        }
        required_credentials = ["postgres_credentials"]

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create a PostgreSQL loader."""
        return self.create_sql_loader()

    def create_sql_loader(self):
        """Create an SQLDatabaseLoader for PostgreSQL."""
        try:
            from langchain_community.document_loaders import SQLDatabaseLoader
            from langchain_community.utilities import SQLDatabase

            # Create SQL database connection
            db = SQLDatabase.from_uri(self.connection_string)

            # Create loader with optional query
            if self.query:
                return SQLDatabaseLoader(db, self.query)
            return SQLDatabaseLoader(db)
        except ImportError:
            raise ImportError(
                "SQLDatabaseLoader requires SQLAlchemy. Please install with pip install sqlalchemy."
            )


@auto_source(scheme_patterns=["s3"])
class S3Source(RemoteSource):
    """Amazon S3 bucket source."""

    bucket_name: str
    key: str | None = None
    prefix: str | None = None

    class Config:
        loader_strategies = {
            "file": {
                "class": "S3FileLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["single_file"],
                "requires_auth": True,
                "required_credentials": ["aws_credentials"],
            },
            "directory": {
                "class": "S3DirectoryLoader",
                "speed": "medium",
                "quality": "high",
                "best_for": ["multiple_files"],
                "requires_auth": True,
                "required_credentials": ["aws_credentials"],
            },
        }
        required_credentials = ["aws_credentials"]

    def create_loader(self, strategy_name: str | None = None) -> Any:
        """Create an S3 loader with the specified strategy."""
        if strategy_name == "directory" or self.prefix:
            return self.create_directory_loader()
        return self.create_file_loader()

    def create_file_loader(self):
        """Create an S3FileLoader for S3 objects."""
        try:
            from langchain_community.document_loaders import S3FileLoader

            if not self.key:
                raise ValueError("S3 key is required for S3FileLoader")

            return S3FileLoader(self.bucket_name, self.key)
        except ImportError:
            raise ImportError(
                "S3FileLoader requires boto3. Please install with pip install boto3."
            )

    def create_directory_loader(self):
        """Create an S3DirectoryLoader for S3 directories."""
        try:
            from langchain_community.document_loaders import S3DirectoryLoader

            prefix = self.prefix or ""

            return S3DirectoryLoader(self.bucket_name, prefix)
        except ImportError:
            raise ImportError(
                "S3DirectoryLoader requires boto3. Please install with pip install boto3."
            )


# Factory function to create document loaders for any path
def create_document_loader(
    path: str,
    strategy: str | None = None,
    credential_manager: CredentialManager | None = None,
) -> Any:
    """Create the appropriate document loader for any path or URL.

    Args:
        path: File path, URL, or URI to load
        strategy: Optional specific strategy to use
        credential_manager: Optional credential manager for authentication

    Returns:
        DocumentLoader instance
    """
    # Analyze the path to determine its type
    analysis_result = analyze_path_comprehensive(path)

    # Find matching source types
    matches = registry.find_matching_sources(analysis_result)

    if not matches:
        # No specific match, try to infer from file extension or use a general loader
        if analysis_result.file_extension:
            # Try to find a loader based on file extension
            if analysis_result.file_extension.lower() == ".pdf":
                return PDFSource(file_path=path).create_loader(strategy)
            if analysis_result.file_extension.lower() in [".doc", ".docx"]:
                return WordDocumentSource(file_path=path).create_loader(strategy)
            if analysis_result.file_extension.lower() in [".xls", ".xlsx"]:
                return ExcelSource(file_path=path).create_loader(strategy)
            if analysis_result.file_extension.lower() in [".ppt", ".pptx"]:
                return PowerPointSource(file_path=path).create_loader(strategy)
            if analysis_result.file_extension.lower() in [".html", ".htm"]:
                return HTMLSource(file_path=path).create_loader(strategy)
            # Default to text loader
            from langchain_community.document_loaders import TextLoader

            return TextLoader(path)
        if analysis_result.is_directory:
            # Directory loader
            return DirectorySource(directory_path=path).create_loader(strategy)
        if (
            analysis_result.url_components
            and analysis_result.url_components.scheme in ["http", "https"]
        ):
            # Web loader
            from langchain_community.document_loaders import WebBaseLoader

            return WebBaseLoader(path)
        # Default to text loader
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
