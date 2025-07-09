"""File-specific Document Loader Agent.

This module provides a specialized document loader agent for loading
documents from local files.
"""

from pathlib import Path

from haive.core.engine.document_loader import create_file_loader_engine
from pydantic import Field

from haive.agents.document_loader.base.agent import DocumentLoaderAgent


class FileLoaderAgent(DocumentLoaderAgent):
    """Specialized document loader agent for loading documents from files.

    This agent is pre-configured for loading from local files and provides
    additional file-specific options.

    Attributes:
        name: Name of the agent
        file_path: Path to the file to load
        file_extension: File extension to use for loader selection
        loader_name: Explicit loader name to use
    """

    name: str = "File Loader Agent"

    # File-specific options
    file_path: str | Path | None = Field(
        default=None, description="Path to the file to load"
    )

    file_extension: str | None = Field(
        default=None, description="File extension to use for loader selection"
    )

    loader_name: str | None = Field(
        default=None, description="Explicit loader name to use"
    )

    def setup_agent(self) -> None:
        """Set up the agent with a file loader engine."""
        # Create a file loader engine
        self.engine = create_file_loader_engine(
            file_path=self.file_path,
            file_extension=self.file_extension,
            loader_name=self.loader_name,
        )

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        self.engine.config.use_async = self.use_async

        # Register the engine
        self.engines["file_loader"] = self.engine
