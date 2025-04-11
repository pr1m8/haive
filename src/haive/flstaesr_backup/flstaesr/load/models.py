# src/haive/core/docs/document_loader_registry.py

import os
import logging
from typing import Dict, List, Any, Optional, Union, Type, Set, Tuple, cast
from pydantic import BaseModel, Field

from langchain_core.documents import Document
from src.haive.core.registry.registy import registry_manager
# Import source models from your existing code
from src.haive.agents.flstaesr.fetch.models import (
    DocumentSource, URLSource, SitemapSource, ReadTheDocsSource, 
    GithubSource, RecursiveURLSource, FileSource, DirectorySource, 
    HuggingFaceModelSource, HuggingFaceDatasetSource, WeatherSource
)

# Set up logging
logger = logging.getLogger(__name__)

class LoaderMetadata(BaseModel):
    """Metadata for document loaders."""
    name: str = Field(..., description="Name of the loader")
    description: Optional[str] = Field(default=None, description="Description of the loader")
    supported_source_types: List[str] = Field(default_factory=list, description="List of supported source types")
    requires_dependencies: List[str] = Field(default_factory=list, description="External dependencies required")
    tags: List[str] = Field(default_factory=list, description="Tags for categorizing this loader")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")

class DocumentLoaderRegistry:
    """
    Registry for document loaders with factory methods based on source types.
    
    This registry integrates with the global registry system and provides:
    - Dynamic loader discovery and registration
    - Source type to loader mapping
    - Loading documents from various sources
    - Metadata enrichment for loaded documents
    """
    
    def __init__(self):
        """Initialize the document loader registry."""
        self._loader_cache = {}
        self._metadata_registry: Dict[str, LoaderMetadata] = {}
        self._register_built_in_loaders()
    
    def _register_built_in_loaders(self):
        """Register built-in document loaders."""
        # Register URL loaders
        self.register_loader(
            "web_loader",
            lambda source: self._get_web_loader(source),
            LoaderMetadata(
                name="web_loader",
                description="Loader for web pages",
                supported_source_types=["URLSource"],
                tags=["web", "html"]
            )
        )
        
        self.register_loader(
            "sitemap_loader",
            lambda source: self._get_sitemap_loader(source),
            LoaderMetadata(
                name="sitemap_loader",
                description="Loader for sitemaps",
                supported_source_types=["SitemapSource"],
                tags=["web", "sitemap"]
            )
        )
        
        self.register_loader(
            "readthedocs_loader",
            lambda source: self._get_readthedocs_loader(source),
            LoaderMetadata(
                name="readthedocs_loader",
                description="Loader for ReadTheDocs documentation",
                supported_source_types=["ReadTheDocsSource"],
                tags=["docs", "documentation"]
            )
        )
        
        self.register_loader(
            "github_loader",
            lambda source: self._get_github_loader(source),
            LoaderMetadata(
                name="github_loader",
                description="Loader for GitHub files",
                supported_source_types=["GithubSource"],
                tags=["github", "code"]
            )
        )
        
        self.register_loader(
            "recursive_url_loader",
            lambda source: self._get_recursive_url_loader(source),
            LoaderMetadata(
                name="recursive_url_loader",
                description="Loader for recursively crawling web pages",
                supported_source_types=["RecursiveURLSource"],
                tags=["web", "crawler"]
            )
        )
        
        # Register file loaders
        self.register_loader(
            "pdf_loader",
            lambda source: self._get_pdf_loader(source),
            LoaderMetadata(
                name="pdf_loader",
                description="Loader for PDF files",
                supported_source_types=["FileSource"],
                requires_dependencies=["pypdf"],
                tags=["pdf", "document"]
            )
        )
        
        self.register_loader(
            "docx_loader",
            lambda source: self._get_docx_loader(source),
            LoaderMetadata(
                name="docx_loader",
                description="Loader for Word documents",
                supported_source_types=["FileSource"],
                requires_dependencies=["docx2txt"],
                tags=["docx", "document", "word"]
            )
        )
        
        self.register_loader(
            "csv_loader",
            lambda source: self._get_csv_loader(source),
            LoaderMetadata(
                name="csv_loader",
                description="Loader for CSV files",
                supported_source_types=["FileSource"],
                tags=["csv", "data"]
            )
        )
        
        self.register_loader(
            "json_loader",
            lambda source: self._get_json_loader(source),
            LoaderMetadata(
                name="json_loader",
                description="Loader for JSON files",
                supported_source_types=["FileSource"],
                tags=["json", "data"]
            )
        )
        
        self.register_loader(
            "notebook_loader",
            lambda source: self._get_notebook_loader(source),
            LoaderMetadata(
                name="notebook_loader",
                description="Loader for Jupyter notebooks",
                supported_source_types=["FileSource"],
                requires_dependencies=["nbformat"],
                tags=["ipynb", "notebook", "jupyter"]
            )
        )
        
        self.register_loader(
            "python_loader",
            lambda source: self._get_python_loader(source),
            LoaderMetadata(
                name="python_loader",
                description="Loader for Python files",
                supported_source_types=["FileSource"],
                tags=["python", "code"]
            )
        )
        
        self.register_loader(
            "image_loader",
            lambda source: self._get_image_loader(source),
            LoaderMetadata(
                name="image_loader",
                description="Loader for image files",
                supported_source_types=["FileSource"],
                requires_dependencies=["unstructured"],
                tags=["image", "jpg", "png"]
            )
        )
        
        self.register_loader(
            "text_loader",
            lambda source: self._get_text_loader(source),
            LoaderMetadata(
                name="text_loader",
                description="Loader for text files",
                supported_source_types=["FileSource"],
                tags=["text", "txt", "md"]
            )
        )
        
        self.register_loader(
            "directory_loader",
            lambda source: self._get_directory_loader(source),
            LoaderMetadata(
                name="directory_loader",
                description="Loader for directories of files",
                supported_source_types=["DirectorySource"],
                tags=["directory", "multi-file"]
            )
        )
        
        # Register HuggingFace loaders
        self.register_loader(
            "hf_model_loader",
            lambda source: self._get_hf_model_loader(source),
            LoaderMetadata(
                name="hf_model_loader",
                description="Loader for HuggingFace models",
                supported_source_types=["HuggingFaceModelSource"],
                requires_dependencies=["huggingface_hub"],
                tags=["huggingface", "model"]
            )
        )
        
        self.register_loader(
            "hf_dataset_loader",
            lambda source: self._get_hf_dataset_loader(source),
            LoaderMetadata(
                name="hf_dataset_loader",
                description="Loader for HuggingFace datasets",
                supported_source_types=["HuggingFaceDatasetSource"],
                requires_dependencies=["huggingface_hub", "datasets"],
                tags=["huggingface", "dataset"]
            )
        )
        
        # Register Weather loader
        self.register_loader(
            "weather_loader",
            lambda source: self._get_weather_loader(source),
            LoaderMetadata(
                name="weather_loader",
                description="Loader for weather data",
                supported_source_types=["WeatherSource"],
                requires_dependencies=["openweathermap"],
                tags=["weather", "api"]
            )
        )
        
        logger.info(f"Registered {len(self._metadata_registry)} built-in document loaders")
    
    def register_loader(self, 
                        name: str, 
                        factory_func: callable, 
                        metadata: Optional[LoaderMetadata] = None):
        """
        Register a new document loader.
        
        Args:
            name: Name of the loader
            factory_func: Factory function that creates the loader instance
            metadata: Optional metadata for the loader
        """
        # Register with the global registry system
        #register_loader(name, tags=metadata.tags if metadata else [])(factory_func)
        
        # Cache the factory function
        self._loader_cache[name] = factory_func
        
        # Store metadata
        if metadata:
            self._metadata_registry[name] = metadata
            
        logger.debug(f"Registered document loader: {name}")
    
    def get_loader_for_source(self, source: DocumentSource):
        """
        Get the appropriate document loader for a given source.
        
        Args:
            source: DocumentSource instance
            
        Returns:
            Document loader instance
        """
        source_obj = source.source
        source_type = type(source_obj).__name__
        
        # Find appropriate loader factory based on source type
        factory_func = None
        
        # Check metadata registry for compatible loaders
        for name, metadata in self._metadata_registry.items():
            if source_type in metadata.supported_source_types:
                # Additional type-specific checks
                if source_type == "FileSource" and hasattr(source_obj, "file_type"):
                    # For file sources, check file type compatibility
                    file_type = source_obj.file_type.lower()
                    if any(tag.lower() == file_type for tag in metadata.tags):
                        factory_func = self._loader_cache.get(name)
                        break
                else:
                    # For non-file sources, use the first compatible loader
                    factory_func = self._loader_cache.get(name)
                    break
        
        # If no specific loader found, fall back to appropriate generic loader
        if factory_func is None:
            if isinstance(source_obj, URLSource):
                factory_func = self._loader_cache.get("web_loader")
            elif isinstance(source_obj, FileSource):
                factory_func = self._loader_cache.get("text_loader")  # Default to text loader
            elif isinstance(source_obj, DirectorySource):
                factory_func = self._loader_cache.get("directory_loader")
            else:
                raise ValueError(f"No loader available for source type: {source_type}")
        
        # Create and return the loader
        try:
            return factory_func(source)
        except Exception as e:
            logger.error(f"Error creating loader for {source_type}: {str(e)}")
            raise
    
    def load_from_directory(self, directory_path, filter_ext=None):
        """
        Load all documents from a directory with optional file extension filtering.
        
        Args:
            directory_path: Path to the directory
            filter_ext: Optional file extension to filter by
            
        Returns:
            List of loaded documents
        """
        documents = []
        try:
            for filename in os.listdir(directory_path):
                if filter_ext and not filename.endswith(filter_ext):
                    continue
                    
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path):
                    source = DocumentSource.from_local_file(file_path)
                    loader = self.get_loader_for_source(source)
                    docs = loader.load()
                    
                    # Add metadata about source
                    for doc in docs:
                        doc.metadata["source_file"] = file_path
                        doc.metadata["filename"] = filename
                        
                    documents.extend(docs)
            
            return documents
        except Exception as e:
            logger.error(f"Error loading from directory {directory_path}: {str(e)}")
            return []
    
    def load_from_source(self, source: DocumentSource, add_metadata: bool = True):
        """
        Load documents from a source.
        
        Args:
            source: DocumentSource instance
            add_metadata: Whether to add metadata about the source
            
        Returns:
            List of loaded documents
        """
        try:
            loader = self.get_loader_for_source(source)
            docs = loader.load()
            
            # Add metadata if requested
            if add_metadata:
                source_info = source.source.model_dump() if hasattr(source.source, "model_dump") else vars(source.source)
                for doc in docs:
                    doc.metadata["source_type"] = type(source.source).__name__
                    doc.metadata["source_info"] = source_info
            
            return docs
        except Exception as e:
            logger.error(f"Error loading from source {type(source.source).__name__}: {str(e)}")
            return []
    
    def get_metadata(self, loader_name: str) -> Optional[LoaderMetadata]:
        """Get metadata for a specific loader."""
        return self._metadata_registry.get(loader_name)
    
    def list_loaders(self) -> List[str]:
        """List all registered loader names."""
        return list(self._metadata_registry.keys())
    
    def get_loaders_by_tag(self, tag: str) -> List[str]:
        """Get loaders that have a specific tag."""
        return [
            name for name, metadata in self._metadata_registry.items()
            if tag in metadata.tags
        ]
    
    def get_loaders_for_source_type(self, source_type: str) -> List[str]:
        """Get loaders that support a specific source type."""
        return [
            name for name, metadata in self._metadata_registry.items()
            if source_type in metadata.supported_source_types
        ]
    
    # Private loader factory methods
    def _get_web_loader(self, source):
        """Get a web page loader."""
        from langchain_community.document_loaders import WebBaseLoader
        return WebBaseLoader(web_path=source.source.url)
    
    def _get_sitemap_loader(self, source):
        """Get a sitemap loader."""
        from langchain_community.document_loaders import SitemapLoader
        return SitemapLoader(web_path=source.source.url)
    
    def _get_readthedocs_loader(self, source):
        """Get a ReadTheDocs loader."""
        from langchain_community.document_loaders import ReadTheDocsLoader
        return ReadTheDocsLoader(path=source.source.url)
    
    def _get_github_loader(self, source):
        """Get a GitHub file loader."""
        from langchain_community.document_loaders import GitHubFileLoader
        return GitHubFileLoader(
            repo=source.source.repo_url.replace("https://github.com/", ""),
            branch=source.source.branch,
            path=source.source.file_path
        )
    
    def _get_recursive_url_loader(self, source):
        """Get a recursive URL loader."""
        from langchain_community.document_loaders import RecursiveUrlLoader
        return RecursiveUrlLoader(
            url=source.source.url,
            max_depth=source.source.max_depth,
            prevent_outside=source.source.prevent_outside
        )
    
    def _get_pdf_loader(self, source):
        """Get a PDF loader."""
        from langchain_community.document_loaders import PyPDFLoader
        return PyPDFLoader(file_path=source.source.file_path)
    
    def _get_docx_loader(self, source):
        """Get a Word document loader."""
        from langchain_community.document_loaders import Docx2txtLoader
        return Docx2txtLoader(file_path=source.source.file_path)
    
    def _get_csv_loader(self, source):
        """Get a CSV loader."""
        from langchain_community.document_loaders import CSVLoader
        return CSVLoader(file_path=source.source.file_path)
    
    def _get_json_loader(self, source):
        """Get a JSON loader."""
        from langchain_community.document_loaders import JSONLoader
        return JSONLoader(file_path=source.source.file_path, jq_schema='.[]')
    
    def _get_notebook_loader(self, source):
        """Get a Jupyter notebook loader."""
        from langchain_community.document_loaders import NotebookLoader
        return NotebookLoader(file_path=source.source.file_path)
    
    def _get_python_loader(self, source):
        """Get a Python file loader."""
        from langchain_community.document_loaders import PythonLoader
        return PythonLoader(file_path=source.source.file_path)
    
    def _get_image_loader(self, source):
        """Get an image loader."""
        from langchain_community.document_loaders import UnstructuredImageLoader
        return UnstructuredImageLoader(file_path=source.source.file_path)
    
    def _get_text_loader(self, source):
        """Get a text file loader."""
        from langchain_community.document_loaders import TextLoader
        return TextLoader(file_path=source.source.file_path)
    
    def _get_directory_loader(self, source):
        """Get a directory loader."""
        from langchain_community.document_loaders import DirectoryLoader
        return DirectoryLoader(
            source.source.directory_path,
            show_progress=True,
            use_multithreading=True
        )
    
    def _get_hf_model_loader(self, source):
        """Get a HuggingFace model loader."""
        from langchain_community.document_loaders import HuggingFaceModelLoader
        return HuggingFaceModelLoader(
            search=source.source.search,
            author=source.source.author,
            filter=source.source.filter,
            sort=source.source.sort,
            direction=source.source.direction,
            limit=source.source.limit,
            full=source.source.full,
            config=source.source.config
        )
    
    def _get_hf_dataset_loader(self, source):
        """Get a HuggingFace dataset loader."""
        from langchain_community.document_loaders import HuggingFaceDatasetLoader
        return HuggingFaceDatasetLoader(
            search=source.source.search,
            author=source.source.author,
            filter=source.source.filter,
            sort=source.source.sort,
            direction=source.source.direction,
            limit=source.source.limit,
            full=source.source.full,
            config=source.source.config
        )
    
    def _get_weather_loader(self, source):
        """Get a weather data loader."""
        from langchain_community.document_loaders import WeatherDataLoader
        return WeatherDataLoader.from_params(
            places=[source.source.city],
            openweathermap_api_key=source.source.api_key
        )

# Create a global instance
document_loader_registry = DocumentLoaderRegistry()