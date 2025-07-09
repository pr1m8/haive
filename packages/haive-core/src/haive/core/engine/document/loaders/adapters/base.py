"""
Base loader adapter for document loaders.

This module provides the base LoaderAdapter class that all specific
loader adapters inherit from, establishing a consistent interface.
"""

from abc import ABC, abstractmethod
from typing import List

from langchain_core.documents import Document

from haive.core.engine.loaders.sources.base import BaseSource


class LoaderAdapter(ABC):
    """
    Base adapter class for document loaders.

    LoaderAdapter provides a unified interface for loading documents from
    different source types using various langchain document loaders.

    Each adapter is responsible for:
    1. Creating the appropriate loader for a specific source type
    2. Configuring the loader with the correct parameters
    3. Loading documents from the source
    4. Optionally, implementing fetch_all functionality when supported
    """

    def __init__(self, source: BaseSource, **params):
        """
        Initialize the adapter.

        Args:
            source: The source to load documents from
            **params: Additional parameters for the loader
        """
        self.source = source
        self.params = params

    @abstractmethod
    def load(self) -> List[Document]:
        """
        Load documents from the source.

        This method must be implemented by all subclasses.

        Returns:
            List of loaded documents
        """
        pass

    def load_and_split(self, **split_params) -> List[Document]:
        """
        Load and split documents.

        This method loads documents and then splits them into chunks
        using a text splitter.

        Args:
            **split_params: Parameters for the text splitter

        Returns:
            List of document chunks
        """
        # Load documents
        docs = self.load()

        # Get text splitter from parameters
        text_splitter = split_params.pop("text_splitter", None)
        if text_splitter is None:
            # Create default text splitter
            from langchain_text_splitters import RecursiveCharacterTextSplitter

            text_splitter = RecursiveCharacterTextSplitter(**split_params)

        # Split documents
        return text_splitter.split_documents(docs)

    def fetch_all(self) -> List[BaseSource]:
        """
        Fetch all available sources (if supported).

        This method is used for sources that contain multiple sub-sources,
        such as directories or sitemaps.

        Returns:
            List of individual sources

        Raises:
            NotImplementedError: If the adapter doesn't support fetch_all
        """
        raise NotImplementedError(
            f"This loader adapter ({self.__class__.__name__}) doesn't support fetch_all"
        )
