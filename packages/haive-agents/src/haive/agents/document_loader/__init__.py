"""Document Loader Agents for loading documents from various sources.

This package provides agent implementations for loading documents from various sources,
including files, web pages, directories, and more.
"""

from haive.agents.document_loader.base.agent import DocumentLoaderAgent
from haive.agents.document_loader.directory.agent import DirectoryLoaderAgent
from haive.agents.document_loader.file.agent import FileLoaderAgent
from haive.agents.document_loader.web.agent import WebLoaderAgent

# Export all public components
__all__ = [
    "DirectoryLoaderAgent",
    "DocumentLoaderAgent",
    "FileLoaderAgent",
    "WebLoaderAgent",
]
