"""Document Engine Agent Implementation.

This module provides agent implementations that integrate with the DocumentEngine
and the Haive agent framework for loading documents from various sources.

The agents handle document loading from various sources, including:
- Local files and directories
- Web pages and URLs
- Cloud storage
- Text input

The agents can be integrated into complex workflows and support both
synchronous and asynchronous operation modes.
"""

from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from langgraph.graph import END, START
from pydantic import Field

# Conditional import for agents - only needed if agents package is available
if TYPE_CHECKING:
    from haive.agents.base.agent import Agent
else:
    try:
        from haive.agents.base.agent import Agent
    except ImportError:
        # Create a placeholder base class if agents package not available
        from pydantic import BaseModel

        class Agent(BaseModel):
            """Placeholder Agent class when haive-agents package not available."""

            pass


from haive.core.engine.document.config import DocumentOutput
from haive.core.engine.document.engine import (
    DocumentEngine,
    create_directory_document_engine,
    create_file_document_engine,
    create_web_document_engine,
)
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph


class DocumentAgent(Agent):
    """Document Agent that integrates the document engine with the agent framework.

    This agent provides a simple interface for loading and processing documents from
    various sources through the agent framework. It can be used as a standalone agent
    or as part of a more complex agent workflow.

    The agent supports loading from:
    - Local files and directories
    - Web pages and URLs
    - Text input
    - Cloud storage (with proper credentials)

    Attributes:
        name: Name of the agent
        engine: The document engine to use
        include_content: Whether to include document content in the output
        include_metadata: Whether to include document metadata in the output
        max_documents: Maximum number of documents to load (None for unlimited)
    """

    name: str = "Document Agent"

    # The main engine - a document engine
    engine: DocumentEngine = Field(
        default_factory=lambda: DocumentEngine(),
        description="Document engine",
    )

    # Configuration options
    include_content: bool = Field(
        default=True, description="Whether to include document content in the output"
    )

    include_metadata: bool = Field(
        default=True, description="Whether to include document metadata in the output"
    )

    max_documents: Optional[int] = Field(
        default=None,
        description="Maximum number of documents to load (None for unlimited)",
    )

    def setup_agent(self) -> None:
        """Set up the agent by configuring the document engine.

        This method is called during agent initialization to set up the engine
        with the agent's configuration parameters.
        """
        # Ensure we have a document engine
        if not isinstance(self.engine, DocumentEngine):
            self.engine = DocumentEngine()

        # Synchronize config options from agent to engine
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        # Register the engine
        self.engines["document_engine"] = self.engine

    def build_graph(self) -> BaseGraph:
        """Build the document agent graph.

        Creates a simple linear graph that loads and processes documents from the input source.

        Returns:
            A BaseGraph instance for document processing
        """
        # Create base graph with proper name
        graph = BaseGraph(name="DocumentGraph")

        # Add the document processor node
        processor_node = EngineNodeConfig(
            engine=self.engine, name="document_processor_node"
        )
        graph.add_node("document_processor", processor_node)

        # Set up simple linear flow: START -> document_processor -> END
        graph.add_edge(START, "document_processor")
        graph.add_edge("document_processor", END)

        return graph

    def process_output(self, output: DocumentOutput) -> Dict[str, Any]:
        """Process the output from the document engine.

        This method filters and formats the output based on the agent's configuration.

        Args:
            output: The raw output from the document engine

        Returns:
            A dictionary with processed document data
        """
        result = {
            "total_documents": output.total_documents,
            "operation_time": output.operation_time,
            "source_type": (
                output.source_type.value if output.source_type else "unknown"
            ),
            "loader_names": output.loader_names,
            "original_source": output.original_source,
            "has_errors": output.has_errors,
            "processing_strategy": (
                output.processing_strategy.value
                if output.processing_strategy
                else "unknown"
            ),
        }

        # Add documents if requested
        if self.include_content:
            documents = []
            for doc in output.documents:
                if self.include_metadata:
                    # Include full document with metadata
                    doc_dict = {
                        "source": doc.source,
                        "content": doc.content,
                        "metadata": doc.metadata,
                        "chunks": [
                            {
                                "content": chunk.content,
                                "metadata": chunk.metadata,
                                "chunk_index": chunk.chunk_index,
                                "chunk_id": chunk.chunk_id,
                            }
                            for chunk in doc.chunks
                        ],
                        "format": doc.format.value if doc.format else "unknown",
                        "source_type": (
                            doc.source_type.value if doc.source_type else "unknown"
                        ),
                        "loader_name": doc.loader_name,
                        "character_count": doc.character_count,
                        "word_count": doc.word_count,
                        "chunk_count": doc.chunk_count,
                        "processing_time": doc.processing_time,
                    }
                    documents.append(doc_dict)
                else:
                    # Include only content
                    documents.append(
                        {
                            "content": doc.content,
                            "source": doc.source,
                        }
                    )
            result["documents"] = documents
        else:
            # Just include document count if content not requested
            result["document_count"] = len(output.documents)

        # Add errors if present
        if output.has_errors:
            result["errors"] = output.errors

        return result


class FileDocumentAgent(DocumentAgent):
    """Specialized document agent for loading documents from files.

    This agent is pre-configured for loading from local files and provides
    additional file-specific options.

    Attributes:
        name: Name of the agent
        file_path: Path to the file to load
        chunking_strategy: Strategy for chunking documents
        chunk_size: Size of chunks in characters
        chunk_overlap: Overlap between chunks
    """

    name: str = "File Document Agent"

    # File-specific options
    file_path: Optional[Union[str, Path]] = Field(
        default=None, description="Path to the file to load"
    )

    def setup_agent(self) -> None:
        """Set up the agent with a file document engine."""
        # Create a file document engine
        self.engine = create_file_document_engine(
            file_path=self.file_path or "",
        )

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        # Register the engine
        self.engines["file_document_engine"] = self.engine


class WebDocumentAgent(DocumentAgent):
    """Specialized document agent for loading documents from web URLs.

    This agent is pre-configured for loading from web sources and provides
    additional web-specific options.

    Attributes:
        name: Name of the agent
        url: URL to load
        chunking_strategy: Strategy for chunking documents
        chunk_size: Size of chunks in characters
    """

    name: str = "Web Document Agent"

    # Web-specific options
    url: Optional[str] = Field(default=None, description="URL to load")

    def setup_agent(self) -> None:
        """Set up the agent with a web document engine."""
        # Create a web document engine
        self.engine = create_web_document_engine()

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        # Register the engine
        self.engines["web_document_engine"] = self.engine


class DirectoryDocumentAgent(DocumentAgent):
    """Specialized document agent for loading documents from directories.

    This agent is pre-configured for loading from local directories and provides
    additional directory-specific options.

    Attributes:
        name: Name of the agent
        directory_path: Path to the directory to load
        recursive: Whether to recursively load files
        include_patterns: List of file patterns to include
        exclude_patterns: List of file patterns to exclude
    """

    name: str = "Directory Document Agent"

    # Directory-specific options
    directory_path: Optional[Union[str, Path]] = Field(
        default=None, description="Path to the directory to load"
    )

    recursive: bool = Field(
        default=True, description="Whether to recursively load files"
    )

    include_patterns: Optional[List[str]] = Field(
        default=None, description="List of file patterns to include"
    )

    exclude_patterns: Optional[List[str]] = Field(
        default=None, description="List of file patterns to exclude"
    )

    def setup_agent(self) -> None:
        """Set up the agent with a directory document engine."""
        # Create a directory document engine
        self.engine = create_directory_document_engine(
            directory_path=self.directory_path or "",
            recursive=self.recursive,
            include_patterns=self.include_patterns,
            exclude_patterns=self.exclude_patterns,
        )

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        # Register the engine
        self.engines["directory_document_engine"] = self.engine


# Export agent classes
__all__ = [
    "DocumentAgent",
    "FileDocumentAgent",
    "WebDocumentAgent",
    "DirectoryDocumentAgent",
]
