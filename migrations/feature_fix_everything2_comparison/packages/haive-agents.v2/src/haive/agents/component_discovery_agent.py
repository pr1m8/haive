"""Component Discovery Agent for Dynamic Activation.

This module provides ComponentDiscoveryAgent, a RAG-based agent for discovering
components from documentation. It uses MetaStateSchema for tracking and follows
the Dynamic Activation Pattern.

Based on: @project_docs/active/patterns/dynamic_activation_pattern.md
"""

import logging
from pathlib import Path
from typing import Any, Optional

from haive.core.engine.retriever import BaseRetrieverConfig
from haive.core.schema.prebuilt.meta_state import MetaStateSchema
from haive.core.utils.haive_discovery import HaiveComponentDiscovery
from langchain_core.documents import Document
from pydantic import BaseModel, ConfigDict, Field, PrivateAttr, model_validator

from haive.agents.rag.base.agent import BaseRAGAgent

logger = logging.getLogger(__name__)


class ComponentDiscoveryAgent(BaseModel):
    """RAG-based agent for discovering components from documentation.

    This agent uses retrieval-augmented generation to find components that
    can satisfy specific requirements. It wraps a BaseRAGAgent in MetaStateSchema
    for tracking and recompilation support.

    Key Features:
        - RAG-based component discovery from documentation
        - MetaStateSchema integration for tracking
        - Automatic document loading from various sources
        - Component parsing and metadata extraction
        - Caching for performance
        - Error handling and logging

    Args:
        document_path: Path to documentation or component sources
        discovery_agent: BaseRAGAgent for performing retrieval
        meta_state: MetaStateSchema wrapper for the discovery agent
        discovery_config: Configuration for discovery behavior
        component_cache: Cache for discovered components

    Examples:
        Basic usage::

            from haive.agents.discovery.component_discovery_agent import ComponentDiscoveryAgent

            # Create discovery agent
            agent = ComponentDiscoveryAgent(
                document_path="@haive-tools/docs"
            )

            # Discover components
            components = await agent.discover_components("math tools")

            for comp in components:
                print(f"Found: {comp['name']} - {comp['description']}")

        With custom configuration::

            agent = ComponentDiscoveryAgent(
                document_path="/path/to/docs",
                discovery_config={
                    "max_results": 5,
                    "similarity_threshold": 0.7,
                    "use_cache": True
                }
            )

            # Discover specific capabilities
            components = await agent.discover_components(
                "tools for data visualization and charting"
            )

        From Haive components::

            # Use HaiveComponentDiscovery for automatic loading
            agent = ComponentDiscoveryAgent(
                document_path="@haive-tools"
            )

            # Find tools that can handle specific tasks
            tools = await agent.discover_components("file processing tools")

            # Parse and load actual tool instances
            for tool_doc in tools:
                tool_instance = await agent.load_component_from_doc(tool_doc)
                if tool_instance:
                    print(f"Loaded tool: {tool_instance.name}")
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True, validate_assignment=True, extra="forbid"
    )

    # Core configuration
    document_path: str = Field(
        ..., description="Path to documentation or component sources"
    )

    # Component instances (initialized via model_validator)
    discovery_agent: Optional[BaseRAGAgent] = Field(
        default=None, description="BaseRAGAgent for performing retrieval"
    )

    meta_state: Optional[MetaStateSchema] = Field(
        default=None, description="MetaStateSchema wrapper for the discovery agent"
    )

    # Configuration and caching
    discovery_config: dict[str, Any] = Field(
        default_factory=dict, description="Configuration for discovery behavior"
    )

    component_cache: dict[str, list[dict[str, Any]]] = Field(
        default_factory=dict, description="Cache for discovered components"
    )

    # Internal state (private attributes)
    _documents: list[Document] | None = PrivateAttr(default=None)
    _haive_discovery: Optional[HaiveComponentDiscovery] = PrivateAttr(default=None)

    @model_validator(mode="after")
    def setup_discovery_agent(self) -> "ComponentDiscoveryAgent":
        """Initialize the discovery agent after model creation.

        This validator:
        1. Loads documents from the specified path
        2. Creates BaseRAGAgent with documents
        3. Wraps agent in MetaStateSchema
        4. Sets up configuration defaults
        5. Initializes caching system
        """
        if self.discovery_agent is None:
            try:
                # Load documents from path
                self._documents = self._load_documents(self.document_path)

                if not self._documents:
                    logger.warning(f"No documents found at path: {self.document_path}")
                    # Create empty documents list to avoid errors
                    self._documents = [
                        Document(
                            page_content="No components found",
                            metadata={"source": "empty", "type": "placeholder"},
                        )
                    ]

                # Create retriever configuration
                retriever_config = BaseRetrieverConfig(
                    name="component_retriever", documents=self._documents
                )

                # Create RAG agent with retriever
                self.discovery_agent = BaseRAGAgent(
                    name="component_discovery", engine=retriever_config
                )

                # Wrap in MetaStateSchema for tracking
                self.meta_state = MetaStateSchema(
                    agent=self.discovery_agent,
                    agent_state={"discovery_mode": "components"},
                    graph_context={
                        "purpose": "component_discovery",
                        "document_path": self.document_path,
                        "document_count": len(self._documents),
                    },
                )

                logger.info(
                    f"Initialized discovery agent with {len(self._documents)} documents"
                )

            except Exception as e:
                logger.exception(f"Failed to initialize discovery agent: {e}")
                # Create minimal fallback configuration
                self._setup_fallback_agent()

        # Setup discovery configuration defaults
        if not self.discovery_config:
            self.discovery_config = {
                "max_results": 10,
                "similarity_threshold": 0.6,
                "use_cache": True,
                "cache_ttl": 3600,  # 1 hour
                "include_metadata": True,
                "parse_components": True,
            }

        return self

    def _setup_fallback_agent(self) -> None:
        """Setup a minimal fallback agent when initialization fails."""
        logger.warning("Setting up fallback discovery agent")

        # Create minimal document
        fallback_doc = Document(
            page_content="Fallback component discovery agent",
            metadata={"source": "fallback", "type": "system"},
        )

        # Create basic retriever
        retriever_config = BaseRetrieverConfig(
            name="fallback_retriever", documents=[fallback_doc]
        )

        # Create basic agent
        self.discovery_agent = BaseRAGAgent(
            name="fallback_discovery", engine=retriever_config
        )

        # Wrap in MetaStateSchema
        self.meta_state = MetaStateSchema(
            agent=self.discovery_agent,
            agent_state={"discovery_mode": "fallback"},
            graph_context={"purpose": "fallback_discovery"},
        )

    def _load_documents(self, path: str) -> list[Document]:
        """Load documents from the specified path.

        Args:
            path: Path to documents (supports @haive-* notation)

        Returns:
            List of Document objects
        """
        documents = []

        try:
            if path.startswith("@haive-"):
                # Use HaiveComponentDiscovery for Haive components
                documents = self._load_haive_components(path)
            elif path.startswith("@"):
                # Handle other @ notation
                documents = self._load_at_notation(path)
            else:
                # Regular file/directory path
                documents = self._load_from_filesystem(path)

        except Exception as e:
            logger.exception(f"Failed to load documents from {path}: {e}")

        return documents

    def _load_haive_components(self, path: str) -> list[Document]:
        """Load components using HaiveComponentDiscovery.

        Args:
            path: Path in @haive-* format

        Returns:
            List of Document objects
        """
        documents = []

        try:
            # Extract haive root path (assuming standard structure)
            haive_root = "/home/will/Projects/haive/backend/haive"

            # Initialize HaiveComponentDiscovery
            self._haive_discovery = HaiveComponentDiscovery(haive_root)

            # Discover all components
            all_components = self._haive_discovery.discover_all_categorized(
                create_tools=True
            )

            # Convert to documents
            for category, components in all_components.items():
                for component in components:
                    doc = Document(
                        page_content=component.to_document_content(),
                        metadata={
                            "name": component.name,
                            "type": component.component_type,
                            "category": category,
                            "module": component.module_path,
                            "has_tool": component.tool_instance is not None,
                            "source": "haive_discovery",
                        },
                    )
                    documents.append(doc)

            logger.info(f"Loaded {len(documents)} Haive components")

        except Exception as e:
            logger.exception(f"Failed to load Haive components: {e}")

        return documents

    def _load_at_notation(self, path: str) -> list[Document]:
        """Load documents from @ notation paths.

        Args:
            path: Path with @ notation

        Returns:
            List of Document objects
        """
        # For now, treat as regular filesystem path
        cleaned_path = path.replace("@", "")
        return self._load_from_filesystem(cleaned_path)

    def _load_from_filesystem(self, path: str) -> list[Document]:
        """Load documents from filesystem path.

        Args:
            path: Filesystem path

        Returns:
            List of Document objects
        """
        documents = []
        path_obj = Path(path)

        try:
            if path_obj.is_file():
                # Load single file
                with open(path_obj, encoding="utf-8") as f:
                    content = f.read()
                    doc = Document(
                        page_content=content,
                        metadata={
                            "source": str(path_obj),
                            "type": "file",
                            "filename": path_obj.name,
                        },
                    )
                    documents.append(doc)

            elif path_obj.is_dir():
                # Load directory recursively
                for file_path in path_obj.rglob("*.py"):
                    try:
                        with open(file_path, encoding="utf-8") as f:
                            content = f.read()
                            doc = Document(
                                page_content=content,
                                metadata={
                                    "source": str(file_path),
                                    "type": "file",
                                    "filename": file_path.name,
                                    "relative_path": str(
                                        file_path.relative_to(path_obj)
                                    ),
                                },
                            )
                            documents.append(doc)
                    except Exception as e:
                        logger.warning(f"Failed to load file {file_path}: {e}")

        except Exception as e:
            logger.exception(f"Failed to load from filesystem path {path}: {e}")

        return documents

    async def discover_components(self, query: str) -> list[dict[str, Any]]:
        """Discover components based on a query.

        Args:
            query: Natural language query describing needed components

        Returns:
            List of component dictionaries with metadata

        Examples:
            Discover math tools::

                components = await agent.discover_components("math and calculation tools")

            Discover with specific requirements::

                components = await agent.discover_components(
                    "tools for file processing and data extraction"
                )
        """
        # Check cache first
        if self.discovery_config.get("use_cache", True):
            cached_results = self.component_cache.get(query)
            if cached_results:
                logger.info(f"Returning cached results for query: {query}")
                return cached_results

        try:
            # Execute discovery through meta state
            discovery_prompt = f"""
            Find components that can help with: {query}

            Look for:
            - Functions or classes that match the requirements
            - Tools that provide the needed functionality
            - Agents that can handle the task
            - Components with relevant capabilities

            Return information about:
            - Component name and description
            - Module path and location
            - Capabilities and features
            - Usage examples if available
            """

            result = await self.meta_state.execute_agent(
                input_data=discovery_prompt, update_state=True
            )

            # Parse components from result
            components = self._parse_components(result.get("output", ""))

            # Cache results
            if self.discovery_config.get("use_cache", True):
                self.component_cache[query] = components

            logger.info(f"Discovered {len(components)} components for query: {query}")
            return components

        except Exception as e:
            logger.exception(f"Failed to discover components for query '{query}': {e}")
            return []

    def _parse_components(self, output: str) -> list[dict[str, Any]]:
        """Parse component data from discovery output.

        Args:
            output: Raw output from discovery agent

        Returns:
            List of parsed component dictionaries
        """
        components = []

        try:
            # If we have documents with metadata, use them
            if self._documents:
                for doc in self._documents:
                    metadata = doc.metadata

                    # Check if document is relevant to output
                    if self._is_relevant_document(doc, output):
                        component = {
                            "id": metadata.get("name", "unknown"),
                            "name": metadata.get("name", "Unknown Component"),
                            "description": self._extract_description(doc),
                            "type": metadata.get("type", "unknown"),
                            "module_path": metadata.get("module", ""),
                            "source": metadata.get("source", ""),
                            "has_tool": metadata.get("has_tool", False),
                            "metadata": metadata,
                        }
                        components.append(component)

            # Limit results based on configuration
            max_results = self.discovery_config.get("max_results", 10)
            components = components[:max_results]

        except Exception as e:
            logger.exception(f"Failed to parse components: {e}")

        return components

    def _is_relevant_document(self, doc: Document, output: str) -> bool:
        """Check if a document is relevant to the discovery output.

        Args:
            doc: Document to check
            output: Discovery output

        Returns:
            True if document is relevant
        """
        # Simple relevance check - can be enhanced with similarity scoring
        doc_text = doc.page_content.lower()
        output_text = output.lower()

        # Check if document name or content appears in output
        name = doc.metadata.get("name", "").lower()
        if name and name in output_text:
            return True

        # Check for common keywords
        keywords = ["tool", "agent", "component", "function", "class"]
        return any(key in doc_text and key in output_text for key in keywords)

    def _extract_description(self, doc: Document) -> str:
        """Extract description from document content.

        Args:
            doc: Document to extract description from

        Returns:
            Extracted description string
        """
        content = doc.page_content

        # Try to extract docstring or description
        lines = content.split("\n")

        # Look for docstrings
        for i, line in enumerate(lines):
            if '"""' in line or "'''" in line:
                # Found docstring start
                desc_lines = []
                for j in range(i + 1, len(lines)):
                    if '"""' in lines[j] or "'''" in lines[j]:
                        break
                    desc_lines.append(lines[j].strip())

                if desc_lines:
                    return " ".join(desc_lines).strip()

        # Fallback to metadata or default
        metadata = doc.metadata
        return metadata.get(
            "description", f"Component from {metadata.get('source', 'unknown source')}"
        )

    async def load_component_from_doc(
        self, component_doc: dict[str, Any]
    ) -> Optional[Any]:
        """Load actual component instance from component document.

        Args:
            component_doc: Component dictionary from discovery

        Returns:
            Loaded component instance or None if loading fails

        Examples:
            Load discovered component::

                components = await agent.discover_components("calculator")
                for comp_doc in components:
                    instance = await agent.load_component_from_doc(comp_doc)
                    if instance:
                        print(f"Loaded: {instance}")
        """
        try:
            # Use the tool loading pattern from notebooks/tool_loader.ipynb
            if self._haive_discovery and component_doc.get("has_tool"):
                # Try to load using HaiveComponentDiscovery
                component_doc.get("module_path", "")
                component_doc.get("name", "")

                # This would need to be implemented based on the actual
                # tool loading logic from the notebook
                # For now, return the component document
                return component_doc

        except Exception as e:
            logger.exception(
                f"Failed to load component {component_doc.get('name', 'unknown')}: {e}"
            )

        return None

    def clear_cache(self) -> None:
        """Clear the component cache.

        Examples:
            Clear cache::

                agent.clear_cache()
                print("Cache cleared")
        """
        self.component_cache.clear()
        logger.info("Component cache cleared")

    def get_cache_stats(self) -> dict[str, Any]:
        """Get statistics about the component cache.

        Returns:
            Dictionary with cache statistics

        Examples:
            Check cache status::

                stats = agent.get_cache_stats()
                print(f"Cached queries: {stats['cached_queries']}")
                print(f"Total components: {stats['total_components']}")
        """
        total_components = sum(
            len(components) for components in self.component_cache.values()
        )

        return {
            "cached_queries": len(self.component_cache),
            "total_components": total_components,
            "cache_size_bytes": len(str(self.component_cache)),
            "cache_enabled": self.discovery_config.get("use_cache", True),
        }
