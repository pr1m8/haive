"""
Haive Component Discovery System

A comprehensive tool for discovering, analyzing, and documenting components
in the Haive AI framework.
"""

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo
from haive.core.utils.haive_discovery.discovery_engine import EnhancedComponentDiscovery
from haive.core.utils.haive_discovery.documentation_writer import DocumentationWriter
from haive.core.utils.haive_discovery.engine_analyzer import EngineAnalyzer
from haive.core.utils.haive_discovery.haive_discovery import HaiveComponentDiscovery
from haive.core.utils.haive_discovery.retriever_analyzers import (
    RetrieverAnalyzer,
    VectorStoreAnalyzer,
)
from haive.core.utils.haive_discovery.tool_analyzers import (
    DocumentLoaderAnalyzer,
    ToolAnalyzer,
)

# Import utility functions
from haive.core.utils.haive_discovery.utils import (  # Quick discovery functions; Tool extraction functions; Engine functions; Documentation functions; Analysis functions; Factory functions
    analyze_failed_imports,
    create_custom_analyzer,
    create_discovery,
    create_tool_from_component,
    discover_all,
    discover_engines,
    discover_loaders,
    discover_retrievers,
    discover_tools,
    discover_vector_stores,
    find_components_by_name,
    find_components_with_env_vars,
    generate_json_catalog,
    generate_markdown_report,
    get_all_engine_configs,
    get_all_tools,
    get_discovery_stats,
    get_engines_by_type,
    get_tools_by_type,
    quick_discover,
    save_discovery_report,
)

__all__ = [
    # Core classes
    "ComponentInfo",
    "ComponentAnalyzer",
    "ToolAnalyzer",
    "DocumentLoaderAnalyzer",
    "RetrieverAnalyzer",
    "VectorStoreAnalyzer",
    "EngineAnalyzer",
    "EnhancedComponentDiscovery",
    "DocumentationWriter",
    "HaiveComponentDiscovery",
    # Quick discovery functions
    "quick_discover",
    "discover_tools",
    "discover_retrievers",
    "discover_vector_stores",
    "discover_loaders",
    "discover_engines",
    "discover_all",
    # Tool functions
    "get_all_tools",
    "get_tools_by_type",
    "create_tool_from_component",
    # Engine functions
    "get_all_engine_configs",
    "get_engines_by_type",
    # Documentation functions
    "save_discovery_report",
    "generate_markdown_report",
    "generate_json_catalog",
    # Analysis functions
    "analyze_failed_imports",
    "get_discovery_stats",
    "find_components_by_name",
    "find_components_with_env_vars",
    # Factory functions
    "create_discovery",
    "create_custom_analyzer",
]

__version__ = "0.1.0"
