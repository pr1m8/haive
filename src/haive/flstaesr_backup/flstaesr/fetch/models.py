from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union, List, Dict, Any
import os


class SourceFindingState(BaseModel):
    """State for the source finding step."""
    search_results: List[Dict[str, Any]] = Field(default_factory=list, description="Search results")
    selected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Selected sources")
    rejected_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Rejected sources")
    reasoning: Optional[str] = Field(default=None, description="Reasoning for source selection")

class DocumentLoadingState(BaseModel):
    """State for the document loading step."""
    loaded_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Successfully loaded sources")
    failed_sources: List[Dict[str, Any]] = Field(default_factory=list, description="Failed to load sources")
    loaded_documents_count: int = Field(default=0, description="Count of loaded documents")
    document_summaries: List[str] = Field(default_factory=list, description="Brief summaries of loaded documents")

class SourceQueryState(BaseModel):
    """State for the source query step."""
    query: str = Field(..., description="Original user query")
    analyzed_query: Optional[str] = Field(default=None, description="Analyzed version of the query")
    potential_topics: List[str] = Field(default_factory=list, description="Potential topics extracted from query")
    source_type_suggestions: List[str] = Field(default_factory=list, description="Suggested source types")



# ===========================================
# Tool Schemas
# ===========================================

class SearchQuery(BaseModel):
    """Schema for a search query."""
    query: str = Field(..., description="Search query")
    filter: Optional[str] = Field(default=None, description="Optional filter")
    max_results: int = Field(default=5, description="Maximum number of results")

class SearchResult(BaseModel):
    """Schema for a search result."""
    title: str = Field(..., description="Title of the result")
    url: Optional[str] = Field(default=None, description="URL of the result")
    snippet: Optional[str] = Field(default=None, description="Snippet from the result")
    source_type: str = Field(..., description="Type of source (web, github, docs, file, etc.)")
    relevance_score: float = Field(..., description="Relevance score (0-1)")

class SearchResults(BaseModel):
    """Schema for search results."""
    results: List[SearchResult] = Field(..., description="List of search results")
    query: str = Field(..., description="Original query")
    total_found: int = Field(..., description="Total number of results found")

class SourceAnalysis(BaseModel):
    """Schema for analyzing a potential source."""
    source_url: Optional[str] = Field(default=None, description="URL of the source")
    source_type: str = Field(..., description="Type of source")
    relevance: float = Field(..., description="Relevance to the query (0-1)")
    reliability: float = Field(..., description="Reliability of the source (0-1)")
    quality: float = Field(..., description="Quality of information (0-1)")
    recommendation: str = Field(..., description="Recommendation (use/reject)")
    reasoning: str = Field(..., description="Reasoning for the recommendation")

class SourceSelectionResult(BaseModel):
    """Schema for the result of source selection."""
    selected_sources: List[Dict[str, Any]] = Field(..., description="Selected sources")
    rejected_sources: List[Dict[str, Any]] = Field(..., description="Rejected sources")
    reasoning: str = Field(..., description="Overall reasoning for the selections")


# Document Source Models
class URLSource(BaseModel):
    """Represents a document source accessible via a URL."""
    url: str = Field(description="The URL of the document")

    @classmethod
    def from_url(cls, url: str):
        """Creates a source from a URL."""
        return cls(url=url)

class SitemapSource(URLSource):
    """Represents a document source from a sitemap."""
    url: str = Field(description="The base URL of the sitemap")
    
    @classmethod
    def from_base_url(cls, base_url: str):
        """Creates a source from a base URL."""
        return cls(url=base_url)
    
    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str):
        """Validates that the provided URL is a valid base URL."""
        if not v.endswith("/"):
            v += "/"
        return f"{v}sitemap.xml"

class ReadTheDocsSource(URLSource):
    """Represents a document source from a Read the Docs project."""
    project_name: str = Field(description="The name of the Read the Docs project")
    version: str = Field(description="The version of the Read the Docs project")
    file_path: str = Field(description="The path to the file in the Read the Docs project")
    url: str = Field(default_factory=lambda: "", description="The URL of the file in Read the Docs")

    @classmethod
    def from_project(cls, project_name: str, version: str, file_path: str):
        """Creates a Read the Docs source from a project name, version, and file path."""
        return cls(
            project_name=project_name,
            version=version,
            file_path=file_path,
            url=cls.get_url(project_name, version, file_path),
        )

    @staticmethod
    def get_url(project_name: str, version: str, file_path: str) -> str:
        """Constructs a URL for the Read the Docs file."""
        return f"https://{project_name}.readthedocs.io/en/{version}/{file_path}"

class GithubSource(URLSource):
    """Represents a document source from a GitHub repository."""
    repo_url: str = Field(description="The URL of the GitHub repository")
    branch: str = Field(description="The branch of the repository")
    file_path: str = Field(description="The path to the file in the repository")
    url: str = Field(default_factory=lambda: "", description="The URL of the file in the repository")

    @classmethod
    def from_github(cls, repo_url: str, branch: str, file_path: str):
        """Creates a GitHub source from repository details."""
        return cls(
            repo_url=repo_url,
            branch=branch,
            file_path=file_path,
            url=cls.get_url(repo_url, branch, file_path),
        )

    @staticmethod
    def get_url(repo_url: str, branch: str, file_path: str) -> str:
        """Constructs a GitHub file URL."""
        return f"{repo_url}/blob/{branch}/{file_path}"

    @field_validator("repo_url")
    @classmethod
    def validate_repo_url(cls, v: str):
        """Validates that the provided repository URL is a valid GitHub URL."""
        if not v.startswith("https://github.com/"):
            raise ValueError(f"Invalid GitHub repository URL: {v}")
        return v

class LocalSource(BaseModel):
    """Represents a document source from a local file."""
    file_path: str = Field(description="The path to the file")

    @classmethod
    def from_file(cls, file_path: str):
        """Creates a LocalSource from a file path."""
        return cls(file_path=file_path)

    @classmethod
    def from_file_name(cls, file_path: str):
        """Extracts and sets only the filename from a file path."""
        return cls(file_path=os.path.basename(file_path))

class DirectorySource(BaseModel):
    """Represents a document source from a local directory."""
    directory_path: str = Field(description="The path to the directory")

    @classmethod
    def from_directory(cls, directory_path: str):
        """Creates a DirectorySource from a directory path."""
        return cls(directory_path=directory_path)

    @field_validator("directory_path")
    @classmethod
    def validate_directory_path(cls, v: str):
        """Validates that the provided path is a valid directory."""
        if "." in os.path.basename(v):
            raise ValueError(f"The path '{v}' appears to be a file, not a directory.")
        if not v.endswith("/"):
            v += "/"
        if not os.path.isdir(v):
            raise ValueError(f"The directory '{v}' does not exist.")
        return v

class FileSource(BaseModel):
    """Represents a document source from a local file with type detection."""
    file_path: str = Field(description="The path to the file")
    file_type: str = Field(default="", description="The file type")

    @classmethod
    def from_file(cls, file_path: str):
        """Creates a FileSource from a file path."""
        return cls(file_path=file_path, file_type=cls.get_file_type(file_path))

    @field_validator("file_path")
    @classmethod
    def validate_file_path(cls, v: str):
        """Validates that the provided file path points to an existing file."""
        if not os.path.exists(v):
            raise ValueError(f"The file '{v}' does not exist.")
        if not os.path.isfile(v):
            raise ValueError(f"The path '{v}' is not a file.")
        return v

    @staticmethod
    def get_file_type(file_path: str) -> str:
        """Extracts the file type from the file extension."""
        return os.path.splitext(file_path)[-1].lstrip(".") or "unknown"

class HuggingFaceModelSource(BaseModel):
    """Represents a document source from HuggingFace models."""
    search: Optional[str] = Field(default=None, description="Filter based on substrings")
    author: Optional[str] = Field(default=None, description="Filter models by author")
    filter: Optional[str] = Field(default=None, description="Filter based on tags")
    sort: Optional[str] = Field(default=None, description="Property to use when sorting")
    direction: Optional[str] = Field(default=None, description="Direction in which to sort")
    limit: int = Field(default=3, description="Limit the number of models fetched")
    full: Optional[bool] = Field(default=None, description="Whether to fetch most model data")
    config: Optional[bool] = Field(default=None, description="Whether to also fetch the repo config")

    @classmethod
    def from_search(cls, search: str, limit: int = 3):
        """Creates a source from a HuggingFace model search."""
        return cls(search=search, limit=limit)

class HuggingFaceDatasetSource(BaseModel):
    """Represents a document source from HuggingFace datasets."""
    search: Optional[str] = Field(default=None, description="Filter based on substrings")
    author: Optional[str] = Field(default=None, description="Filter datasets by author")
    filter: Optional[str] = Field(default=None, description="Filter based on tags")
    sort: Optional[str] = Field(default=None, description="Property to use when sorting")
    direction: Optional[str] = Field(default=None, description="Direction in which to sort")
    limit: int = Field(default=3, description="Limit the number of datasets fetched")
    full: Optional[bool] = Field(default=None, description="Whether to fetch most dataset data")
    config: Optional[bool] = Field(default=None, description="Whether to also fetch the repo config")

    @classmethod
    def from_search(cls, search: str, limit: int = 3):
        """Creates a source from a HuggingFace dataset search."""
        return cls(search=search, limit=limit)

class WeatherSource(BaseModel):
    """Represents a document source for weather data."""
    city: str = Field(description="The city to get weather data for")
    country: str = Field(description="The country the city is in")
    api_key: str = Field(description="OpenWeatherMap API key")

    @classmethod
    def from_location(cls, city: str, country: str, api_key: str):
        """Creates a source from a location."""
        return cls(city=city, country=country, api_key=api_key)

class RecursiveURLSource(URLSource):
    """Represents a document source from a URL with recursive loading."""
    max_depth: int = Field(default=2, description="Maximum depth for recursion")
    prevent_outside: bool = Field(default=True, description="Prevent loading from outside URLs")
    
    @classmethod
    def from_url(cls, url: str, max_depth: int = 2):
        """Creates a source from a URL with specified recursion depth."""
        return cls(url=url, max_depth=max_depth)

class DocumentSource(BaseModel):
    """Represents a unified document source that can be from a URL, GitHub, or local file."""
    source: Union[
        URLSource, 
        GithubSource, 
        LocalSource, 
        DirectorySource, 
        FileSource, 
        SitemapSource, 
        ReadTheDocsSource,
        HuggingFaceModelSource,
        HuggingFaceDatasetSource,
        WeatherSource,
        RecursiveURLSource
    ] = Field(description="The source of the document")

    @classmethod
    def from_url(cls, url: str):
        """Creates a DocumentSource from a URL."""
        return cls(source=URLSource.from_url(url))

    @classmethod
    def from_github(cls, repo_url: str, branch: str, file_path: str):
        """Creates a DocumentSource from a GitHub repository."""
        return cls(source=GithubSource.from_github(repo_url, branch, file_path))

    @classmethod
    def from_local_file(cls, file_path: str):
        """Creates a DocumentSource from a local file."""
        return cls(source=FileSource.from_file(file_path))

    @classmethod
    def from_directory(cls, directory_path: str):
        """Creates a DocumentSource from a local directory."""
        return cls(source=DirectorySource.from_directory(directory_path))
    
    @classmethod
    def from_sitemap(cls, base_url: str):
        """Creates a DocumentSource from a sitemap URL."""
        return cls(source=SitemapSource.from_base_url(base_url))
    
    @classmethod
    def from_readthedocs(cls, project_name: str, version: str, file_path: str):
        """Creates a DocumentSource from a Read the Docs project."""
        return cls(source=ReadTheDocsSource.from_project(project_name, version, file_path))
    
    @classmethod
    def from_huggingface_model(cls, search: str, limit: int = 3):
        """Creates a DocumentSource from a HuggingFace model search."""
        return cls(source=HuggingFaceModelSource.from_search(search, limit))
    
    @classmethod
    def from_huggingface_dataset(cls, search: str, limit: int = 3):
        """Creates a DocumentSource from a HuggingFace dataset search."""
        return cls(source=HuggingFaceDatasetSource.from_search(search, limit))
    
    @classmethod
    def from_weather(cls, city: str, country: str, api_key: str):
        """Creates a DocumentSource from a weather location."""
        return cls(source=WeatherSource.from_location(city, country, api_key))
    
    @classmethod
    def from_recursive_url(cls, url: str, max_depth: int = 2):
        """Creates a DocumentSource from a URL with recursive loading."""
        return cls(source=RecursiveURLSource.from_url(url, max_depth))
