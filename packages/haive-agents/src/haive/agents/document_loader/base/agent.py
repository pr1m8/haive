"""Document Loader Agent implementation.

This module provides an agent implementation that uses the DocumentLoaderEngine
to load documents from various sources and integrate with the Haive agent framework.

The agent handles document loading from various sources, including:
- Local files and directories
- Web pages and URLs
- Databases
- Cloud storage
- API services

The agent can be integrated into more complex workflows and supports both
synchronous and asynchronous operation modes.
"""

from typing import Any

from haive.core.engine.document_loader import (
    DocumentLoaderEngine,
    DocumentLoaderOutput,
    create_document_loader_engine,
)
from haive.core.graph.node.engine_node import EngineNodeConfig
from haive.core.graph.state_graph.base_graph2 import BaseGraph
from langgraph.graph import END, START
from pydantic import Field

from haive.agents.base.agent import Agent


class DocumentLoaderAgent(Agent):
    """Document Loader Agent that integrates the document loader engine with the agent framework.

    This agent provides a simple interface for loading documents from various sources
    through the agent framework. It can be used as a standalone agent or as part of
    a more complex agent workflow.

    The agent supports loading from:
    - Local files and directories
    - Web pages and URLs
    - Databases (with proper credentials)
    - Cloud storage (with proper credentials)

    Attributes:
        name: Name of the agent
        engine: The document loader engine to use
        config: Configuration for the document loader engine
        include_content: Whether to include document content in the output
        include_metadata: Whether to include document metadata in the output
        max_documents: Maximum number of documents to load (None for unlimited)
        use_async: Whether to use async loading if available
    """

    name: str = "Document Loader Agent"

    # The main engine - a document loader engine
    engine: DocumentLoaderEngine = Field(
        default_factory=create_document_loader_engine,
        description="Document loader engine",
    )

    # Configuration options
    include_content: bool = Field(
        default=True, description="Whether to include document content in the output"
    )

    include_metadata: bool = Field(
        default=True, description="Whether to include document metadata in the output"
    )

    max_documents: int | None = Field(
        default=None,
        description="Maximum number of documents to load (None for unlimited)",
    )

    use_async: bool = Field(
        default=False, description="Whether to use async loading if available"
    )

    def setup_agent(self) -> None:
        """Set up the agent by configuring the document loader engine.

        This method is called during agent initialization to set up the engine
        with the agent's configuration parameters.
        """
        # Ensure we have a document loader engine
        if not isinstance(self.engine, DocumentLoaderEngine):
            self.engine = create_document_loader_engine()

        # Synchronize config options from agent to engine
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        self.engine.config.use_async = self.use_async

        # Register the engine
        self.engines["document_loader"] = self.engine

    def build_graph(self) -> BaseGraph:
        """Build the document loader agent graph.

        Creates a simple linear graph that loads documents from the input source.

        Returns:
            A BaseGraph instance for document loading
        """
        # Create base graph with proper name
        graph = BaseGraph(name="DocumentLoaderGraph")

        # Add the document loader node
        loader_node = EngineNodeConfig(engine=self.engine, name="document_loader_node")
        graph.add_node("document_loader", loader_node)

        # Set up simple linear flow: START -> document_loader -> END
        graph.add_edge(START, "document_loader")
        graph.add_edge("document_loader", END)

        return graph

    def process_output(self, output: DocumentLoaderOutput) -> dict[str, Any]:
        """Process the output from the document loader engine.

        This method filters and formats the output based on the agent's configuration.

        Args:
            output: The raw output from the document loader engine

        Returns:
            A dictionary with processed document data
        """
        result = {
            "total_documents": output.total_documents,
            "operation_time": output.operation_time,
            "source_type": output.source_type,
            "loader_name": output.loader_name,
            "original_source": output.original_source,
            "has_errors": output.has_errors,
        }

        # Add documents if requested
        if self.include_content:
            documents = []
            for doc in output.documents:
                if self.include_metadata:
                    # Include full document with metadata
                    documents.append(doc)
                else:
                    # Include only content
                    documents.append(
                        {
                            "page_content": doc.get("page_content", ""),
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
