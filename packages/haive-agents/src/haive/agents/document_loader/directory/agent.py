"""Directory-specific Document Loader Agent.

This module provides a specialized document loader agent for loading
documents from local directories.
"""

from pathlib import Path

from haive.core.engine.document_loader import create_directory_loader_engine
from pydantic import Field

from haive.agents.document_loader.base.agent import DocumentLoaderAgent


class DirectoryLoaderAgent(DocumentLoaderAgent):
    """Specialized document loader agent for loading documents from directories.

    This agent is pre-configured for loading from local directories and provides
    additional directory-specific options.

    Attributes:
        name: Name of the agent
        directory_path: Path to the directory to load
        recursive: Whether to recursively load files
        glob_pattern: Glob pattern for filtering files
        include_extensions: List of file extensions to include
        exclude_extensions: List of file extensions to exclude
    """

    name: str = "Directory Loader Agent"

    # Directory-specific options
    directory_path: str | Path | None = Field(
        default=None, description="Path to the directory to load"
    )

    recursive: bool = Field(
        default=True, description="Whether to recursively load files"
    )

    glob_pattern: str | None = Field(
        default=None, description="Glob pattern for filtering files"
    )

    include_extensions: list[str] | None = Field(
        default=None, description="List of file extensions to include"
    )

    exclude_extensions: list[str] | None = Field(
        default=None, description="List of file extensions to exclude"
    )

    def setup_agent(self) -> None:
        """Set up the agent with a directory loader engine."""
        # Create a directory loader engine
        self.engine = create_directory_loader_engine(
            directory_path=self.directory_path,
            recursive=self.recursive,
            glob_pattern=self.glob_pattern,
            include_extensions=self.include_extensions,
            exclude_extensions=self.exclude_extensions,
        )

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        self.engine.config.use_async = self.use_async

        # Register the engine
        self.engines["directory_loader"] = self.engine
