"""Web-specific Document Loader Agent.

This module provides a specialized document loader agent for loading
documents from web URLs.
"""

from haive.core.engine.document_loader import create_web_loader_engine
from pydantic import Field

from haive.agents.document_loader.base.agent import DocumentLoaderAgent


class WebLoaderAgent(DocumentLoaderAgent):
    """Specialized document loader agent for loading documents from web URLs.

    This agent is pre-configured for loading from web sources and provides
    additional web-specific options.

    Attributes:
        name: Name of the agent
        url: URL to load
        dynamic_loading: Whether to use a dynamic loading strategy (e.g., Playwright)
        recursive: Whether to recursively crawl links
        max_depth: Maximum depth for recursive crawling
        headers: Custom headers to use for requests
    """

    name: str = "Web Loader Agent"

    # Web-specific options
    url: str | None = Field(default=None, description="URL to load")

    dynamic_loading: bool = Field(
        default=False,
        description="Whether to use a dynamic loading strategy (e.g., Playwright)",
    )

    recursive: bool = Field(
        default=False, description="Whether to recursively crawl links"
    )

    max_depth: int = Field(
        default=1, description="Maximum depth for recursive crawling"
    )

    headers: dict[str, str] | None = Field(
        default=None, description="Custom headers to use for requests"
    )

    def setup_agent(self) -> None:
        """Set up the agent with a web loader engine."""
        # Create a web loader engine
        self.engine = create_web_loader_engine(
            url=self.url,
            dynamic_loading=self.dynamic_loading,
            recursive=self.recursive,
            max_depth=self.max_depth,
            headers=self.headers,
        )

        # Apply agent configuration
        if self.max_documents is not None:
            self.engine.config.max_documents = self.max_documents

        self.engine.config.use_async = self.use_async

        # Register the engine
        self.engines["web_loader"] = self.engine
