from pydantic import BaseModel, Field, field_validator
import os
from typing import Union

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
    #sitemap_url: str = Field(description="The URL of the sitemap")
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


class DocumentSource(BaseModel):
    """Represents a unified document source that can be from a URL, GitHub, or local file."""
    source: Union[URLSource, GithubSource, LocalSource, DirectorySource, FileSource] = Field(
        description="The source of the document"
    )

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


class FLSTAESR(BaseModel):
    """Represents a structured document in the FLSTAESR system."""
    doc_source: DocumentSource = Field(description="The source of the document")
    doc_type: str = Field(description="The type of the document")
    doc_path: str = Field(description="The path to the document")
    doc_content: str = Field(description="The content of the document")
