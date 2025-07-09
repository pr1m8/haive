"""
Haive-specific component discovery implementation.
"""

import logging
from pathlib import Path
from typing import Dict, List

from haive.core.utils.haive_discovery.component_info import ComponentInfo
from haive.core.utils.haive_discovery.discovery_engine import EnhancedComponentDiscovery
from haive.core.utils.haive_discovery.documentation_writer import DocumentationWriter

logger = logging.getLogger(__name__)


class HaiveComponentDiscovery(EnhancedComponentDiscovery):
    """Specialized discovery for Haive project structure."""

    def __init__(self, haive_root: str):
        super().__init__(haive_root)
        self.haive_root = Path(haive_root)
        self.doc_writer = DocumentationWriter()

    def discover_individual_tools(
        self, create_tools: bool = True
    ) -> List[ComponentInfo]:
        """Discover individual tools (not toolkits)."""
        tools_path = (
            self.haive_root
            / "packages"
            / "haive-tools"
            / "src"
            / "haive"
            / "tools"
            / "tools"
        )
        if tools_path.exists():
            return self.discover_from_directory(
                tools_path, "haive.tools.tools", create_tools=create_tools
            )
        return []

    def discover_toolkits(self, create_tools: bool = True) -> List[ComponentInfo]:
        """Discover toolkits (collections of tools)."""
        toolkits_path = (
            self.haive_root
            / "packages"
            / "haive-tools"
            / "src"
            / "haive"
            / "tools"
            / "toolkits"
        )
        if toolkits_path.exists():
            return self.discover_from_directory(
                toolkits_path, "haive.tools.toolkits", create_tools=create_tools
            )
        return []

    def discover_retrievers(self, create_tools: bool = True) -> List[ComponentInfo]:
        """Discover retrievers from engine package."""
        retriever_path = (
            self.haive_root
            / "packages"
            / "haive-core"
            / "src"
            / "haive"
            / "core"
            / "engine"
            / "retriever"
        )
        components = []

        if retriever_path.exists():
            components.extend(
                self.discover_from_directory(
                    retriever_path,
                    "haive.core.engine.retriever",
                    create_tools=create_tools,
                )
            )

        # Also check for retrievers in other engine modules
        engine_path = (
            self.haive_root
            / "packages"
            / "haive-core"
            / "src"
            / "haive"
            / "core"
            / "engine"
        )
        if engine_path.exists():
            all_engine_components = self.discover_from_directory(
                engine_path, "haive.core.engine", create_tools=create_tools
            )
            # Filter for retrievers
            components.extend(
                [c for c in all_engine_components if c.component_type == "retriever"]
            )

        return components

    def discover_vector_stores(self, create_tools: bool = True) -> List[ComponentInfo]:
        """Discover vector stores from engine package."""
        vectorstore_path = (
            self.haive_root
            / "packages"
            / "haive-core"
            / "src"
            / "haive"
            / "core"
            / "engine"
            / "vectorstore"
        )
        components = []

        if vectorstore_path.exists():
            components.extend(
                self.discover_from_directory(
                    vectorstore_path,
                    "haive.core.engine.vectorstore",
                    create_tools=create_tools,
                )
            )

        # Also check for vector stores in other locations
        engine_path = (
            self.haive_root
            / "packages"
            / "haive-core"
            / "src"
            / "haive"
            / "core"
            / "engine"
        )
        if engine_path.exists():
            all_engine_components = self.discover_from_directory(
                engine_path, "haive.core.engine", create_tools=create_tools
            )
            # Filter for vector stores
            components.extend(
                [c for c in all_engine_components if c.component_type == "vector_store"]
            )

        return components

    def discover_document_loaders(
        self, create_tools: bool = True
    ) -> List[ComponentInfo]:
        """Discover document loaders."""
        loader_path = (
            self.haive_root
            / "packages"
            / "haive-core"
            / "src"
            / "haive"
            / "core"
            / "engine"
            / "document"
            / "loaders"
        )
        components = []

        if loader_path.exists():
            components.extend(
                self.discover_from_directory(
                    loader_path,
                    "haive.core.engine.document.loaders",
                    create_tools=create_tools,
                )
            )

        # Also check haive-tools for document loaders
        tools_components = self.discover_individual_tools(create_tools)
        components.extend(
            [c for c in tools_components if c.component_type == "document_loader"]
        )

        return components

    def discover_engines(self, create_tools: bool = True) -> List[ComponentInfo]:
        """Discover engines from haive-core package."""
        core_path = (
            self.haive_root / "packages" / "haive-core" / "src" / "haive" / "core"
        )
        engine_path = core_path / "engine"

        if engine_path.exists():
            return self.discover_from_directory(
                engine_path, "haive.core.engine", create_tools=create_tools
            )
        return []

    def discover_all_categorized(
        self, create_tools: bool = True
    ) -> Dict[str, List[ComponentInfo]]:
        """Discover all components, properly categorized."""
        return {
            "individual_tools": self.discover_individual_tools(create_tools),
            "toolkits": self.discover_toolkits(create_tools),
            "retrievers": self.discover_retrievers(create_tools),
            "vector_stores": self.discover_vector_stores(create_tools),
            "document_loaders": self.discover_document_loaders(create_tools),
            "engines": self.discover_engines(create_tools),
        }

    def save_to_project_docs(
        self, components: List[ComponentInfo], subfolder: str = "component_discovery"
    ) -> Dict[str, str]:
        """Save components to project documentation."""
        return self.doc_writer.save_to_project_docs(
            components, project_root=str(self.haive_root), subfolder=subfolder
        )
