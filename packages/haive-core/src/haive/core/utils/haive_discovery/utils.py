"""
Utility and factory functions for easy component discovery.
"""

import json
import logging
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Type, Union

from haive.core.utils.haive_discovery.base_analyzer import ComponentAnalyzer
from haive.core.utils.haive_discovery.component_info import ComponentInfo
from haive.core.utils.haive_discovery.documentation_writer import DocumentationWriter
from haive.core.utils.haive_discovery.haive_discovery import HaiveComponentDiscovery

logger = logging.getLogger(__name__)


# ============================================================================
# QUICK DISCOVERY FUNCTIONS
# ============================================================================


def quick_discover(
    project_root: Optional[str] = None,
    component_type: Optional[str] = None,
    create_tools: bool = True,
) -> List[ComponentInfo]:
    """
    Quick discovery of components with minimal configuration.

    Args:
        project_root: Root directory of the Haive project (auto-detected if None)
        component_type: Specific type to discover (None for all)
        create_tools: Whether to create tool instances

    Returns:
        List of discovered components

    Example:
        >>> components = quick_discover(component_type="retriever")
        >>> print(f"Found {len(components)} retrievers")
    """
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)

    if component_type is None:
        return discover_all(project_root, create_tools)

    type_map = {
        "tool": discovery.discover_individual_tools,
        "toolkit": discovery.discover_toolkits,
        "retriever": discovery.discover_retrievers,
        "vector_store": discovery.discover_vector_stores,
        "document_loader": discovery.discover_document_loaders,
        "engine": discovery.discover_engines,
    }

    if component_type in type_map:
        return type_map[component_type](create_tools)
    else:
        logger.warning(f"Unknown component type: {component_type}")
        return []


def discover_tools(project_root: Optional[str] = None) -> List[ComponentInfo]:
    """Discover all tools (individual tools and toolkits)."""
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    tools = discovery.discover_individual_tools(create_tools=True)
    toolkits = discovery.discover_toolkits(create_tools=True)
    return tools + toolkits


def discover_retrievers(project_root: Optional[str] = None) -> List[ComponentInfo]:
    """Discover all retrievers."""
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    return discovery.discover_retrievers(create_tools=True)


def discover_vector_stores(project_root: Optional[str] = None) -> List[ComponentInfo]:
    """Discover all vector stores."""
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    return discovery.discover_vector_stores(create_tools=True)


def discover_loaders(project_root: Optional[str] = None) -> List[ComponentInfo]:
    """Discover all document loaders."""
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    return discovery.discover_document_loaders(create_tools=True)


def discover_engines(project_root: Optional[str] = None) -> List[ComponentInfo]:
    """Discover all engines."""
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    return discovery.discover_engines(create_tools=True)


def discover_all(
    project_root: Optional[str] = None, create_tools: bool = True
) -> List[ComponentInfo]:
    """
    Discover all components across all categories.

    Args:
        project_root: Root directory of the Haive project
        create_tools: Whether to create tool instances

    Returns:
        List of all discovered components
    """
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)
    categorized = discovery.discover_all_categorized(create_tools)

    all_components = []
    for components in categorized.values():
        all_components.extend(components)

    return all_components


# ============================================================================
# TOOL EXTRACTION FUNCTIONS
# ============================================================================


def get_all_tools(components: List[ComponentInfo]) -> List[Any]:
    """
    Extract all tool instances from components.

    Args:
        components: List of component info objects

    Returns:
        List of tool instances

    Example:
        >>> components = discover_all()
        >>> tools = get_all_tools(components)
        >>> print(f"Created {len(tools)} tools from {len(components)} components")
    """
    tools = []
    for comp in components:
        if comp.tool_instance is not None:
            tools.append(comp.tool_instance)
    return tools


def get_tools_by_type(
    components: List[ComponentInfo], component_type: str
) -> List[Any]:
    """
    Get tools created from a specific component type.

    Args:
        components: List of component info objects
        component_type: Type of component to filter

    Returns:
        List of tool instances from that component type
    """
    tools = []
    for comp in components:
        if comp.component_type == component_type and comp.tool_instance is not None:
            tools.append(comp.tool_instance)
    return tools


def create_tool_from_component(
    component: ComponentInfo, force: bool = False
) -> Optional[Any]:
    """
    Create a tool from a component if possible.

    Args:
        component: Component info object
        force: Force creation even if tool already exists

    Returns:
        Tool instance or None
    """
    if component.tool_instance is not None and not force:
        return component.tool_instance

    # Import the appropriate analyzer
    from haive.core.utils.haive_discovery.retriever_analyzers import (
        RetrieverAnalyzer,
        VectorStoreAnalyzer,
    )
    from haive.core.utils.haive_discovery.tool_analyzers import (
        DocumentLoaderAnalyzer,
        ToolAnalyzer,
    )

    analyzer_map = {
        "tool": ToolAnalyzer(),
        "document_loader": DocumentLoaderAnalyzer(),
        "retriever": RetrieverAnalyzer(),
        "vector_store": VectorStoreAnalyzer(),
    }

    analyzer = analyzer_map.get(component.component_type)
    if analyzer:
        try:
            tool = analyzer.create_tool(component)
            component.tool_instance = tool
            return tool
        except Exception as e:
            logger.error(f"Failed to create tool from {component.name}: {e}")

    return None


# ============================================================================
# ENGINE FUNCTIONS
# ============================================================================


def get_all_engine_configs(components: List[ComponentInfo]) -> List[Dict[str, Any]]:
    """Extract all engine configurations from components."""
    configs = []
    for comp in components:
        if comp.engine_config is not None:
            configs.append(comp.engine_config)
    return configs


def get_engines_by_type(
    components: List[ComponentInfo], engine_type: str
) -> List[Dict[str, Any]]:
    """Get engine configs of a specific type."""
    configs = []
    for comp in components:
        if (
            comp.engine_config is not None
            and comp.engine_config.get("engine_type") == engine_type
        ):
            configs.append(comp.engine_config)
    return configs


# ============================================================================
# DOCUMENTATION FUNCTIONS
# ============================================================================


def save_discovery_report(
    components: List[ComponentInfo],
    output_dir: Optional[str] = None,
    format: str = "all",
) -> Dict[str, str]:
    """
    Save a comprehensive discovery report.

    Args:
        components: List of discovered components
        output_dir: Output directory (auto-created if None)
        format: Output format - "json", "markdown", or "all"

    Returns:
        Dictionary of created file paths
    """
    if output_dir is None:
        output_dir_path = Path.cwd() / "discovery_reports"
    else:
        output_dir_path = Path(output_dir)

    output_dir_path.mkdir(parents=True, exist_ok=True)

    created_files = {}

    if format in ["json", "all"]:
        json_path = generate_json_catalog(components, output_dir_path)
        created_files["json"] = json_path

    if format in ["markdown", "all"]:
        md_path = generate_markdown_report(components, output_dir_path)
        created_files["markdown"] = md_path

    # Also save using the documentation writer
    writer = DocumentationWriter()
    doc_files = writer.save_to_project_docs(
        components,
        project_root=str(output_dir_path.parent),
        subfolder=output_dir_path.name,
    )
    created_files.update(doc_files)

    return created_files


def generate_markdown_report(
    components: List[ComponentInfo], output_dir: Union[str, Path]
) -> str:
    """Generate a markdown report of discovered components."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "discovery_report.md"

    with open(report_path, "w") as f:
        f.write("# Component Discovery Report\n\n")

        # Summary
        stats = get_discovery_stats(components)
        f.write("## Summary\n\n")
        f.write(f"- **Total Components**: {stats['total']}\n")
        f.write(f"- **Components with Tools**: {stats['with_tools']}\n")
        f.write(f"- **Components with Engine Configs**: {stats['with_engines']}\n")
        f.write(
            f"- **Components with Environment Variables**: {stats['with_env_vars']}\n\n"
        )

        # By type
        f.write("## Components by Type\n\n")
        for comp_type, count in stats["by_type"].items():
            f.write(f"- **{comp_type}**: {count}\n")
        f.write("\n")

        # Component details
        f.write("## Component Details\n\n")
        for comp in components:
            f.write(comp.to_document_content())
            f.write("\n---\n\n")

    return str(report_path)


def generate_json_catalog(
    components: List[ComponentInfo], output_dir: Union[str, Path]
) -> str:
    """Generate a JSON catalog of discovered components."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    catalog_path = output_dir / "component_catalog.json"

    catalog = {
        "version": "1.0",
        "total_components": len(components),
        "components": [comp.to_dict() for comp in components],
        "summary": get_discovery_stats(components),
    }

    with open(catalog_path, "w") as f:
        json.dump(catalog, f, indent=2, default=str)

    return str(catalog_path)


# ============================================================================
# ANALYSIS FUNCTIONS
# ============================================================================


def analyze_failed_imports(discovery: HaiveComponentDiscovery) -> Dict[str, List[str]]:
    """
    Analyze failed module imports from a discovery run.

    Args:
        discovery: Discovery instance that has been run

    Returns:
        Dictionary categorizing failures
    """
    analysis = defaultdict(list)

    for module_path, error in discovery.failed_modules:
        if "sys.exit" in error:
            analysis["sys_exit"].append(module_path)
        elif "No module named" in error:
            # Extract missing module name
            import re

            match = re.search(r"No module named '([^']+)'", error)
            if match:
                missing = match.group(1)
                analysis["missing_dependencies"].append(f"{module_path} -> {missing}")
            else:
                analysis["import_errors"].append(f"{module_path}: {error}")
        elif "ImportError" in error:
            analysis["import_errors"].append(f"{module_path}: {error}")
        else:
            analysis["other_errors"].append(f"{module_path}: {error}")

    return dict(analysis)


def get_discovery_stats(components: List[ComponentInfo]) -> Dict[str, Any]:
    """
    Get statistics about discovered components.

    Args:
        components: List of component info objects

    Returns:
        Dictionary with various statistics
    """
    stats = {
        "total": len(components),
        "with_tools": sum(1 for c in components if c.tool_instance is not None),
        "with_engines": sum(1 for c in components if c.engine_config is not None),
        "with_env_vars": sum(1 for c in components if c.env_vars),
        "by_type": defaultdict(int),
        "by_module": defaultdict(int),
    }

    for comp in components:
        stats["by_type"][comp.component_type] += 1
        module_base = comp.module_path.split(".")[0]
        stats["by_module"][module_base] += 1

    stats["by_type"] = dict(stats["by_type"])
    stats["by_module"] = dict(stats["by_module"])

    return stats


def find_components_by_name(
    components: List[ComponentInfo], pattern: str, case_sensitive: bool = False
) -> List[ComponentInfo]:
    """
    Find components matching a name pattern.

    Args:
        components: List of component info objects
        pattern: Name pattern to search for
        case_sensitive: Whether to do case-sensitive matching

    Returns:
        List of matching components
    """
    import re

    if not case_sensitive:
        pattern = pattern.lower()

    matching = []
    for comp in components:
        comp_name = comp.name if case_sensitive else comp.name.lower()
        if re.search(pattern, comp_name):
            matching.append(comp)

    return matching


def find_components_with_env_vars(
    components: List[ComponentInfo], env_var: Optional[str] = None
) -> List[ComponentInfo]:
    """
    Find components that use environment variables.

    Args:
        components: List of component info objects
        env_var: Specific environment variable to search for (None for any)

    Returns:
        List of components using environment variables
    """
    matching = []

    for comp in components:
        if comp.env_vars:
            if env_var is None:
                matching.append(comp)
            elif env_var in comp.env_vars:
                matching.append(comp)

    return matching


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================


def create_discovery(
    project_root: Optional[str] = None,
    custom_analyzers: Optional[List[ComponentAnalyzer]] = None,
) -> HaiveComponentDiscovery:
    """
    Create a configured discovery instance.

    Args:
        project_root: Root directory of the Haive project
        custom_analyzers: Additional analyzers to add

    Returns:
        Configured HaiveComponentDiscovery instance

    Example:
        >>> discovery = create_discovery()
        >>> components = discovery.discover_all_categorized()
    """
    if project_root is None:
        project_root = _find_haive_root()

    discovery = HaiveComponentDiscovery(project_root)

    if custom_analyzers:
        for analyzer in custom_analyzers:
            discovery.add_analyzer(analyzer)

    return discovery


def create_custom_analyzer(
    name: str,
    can_analyze_func: Callable[[Any], bool],
    analyze_func: Callable[[Any, str], Any],
    create_tool_func: Optional[Callable[[Any], Any]] = None,
    create_engine_func: Optional[Callable[[Any], Any]] = None,
) -> Type[ComponentAnalyzer]:
    """
    Create a custom analyzer class dynamically.

    Args:
        name: Name for the analyzer class
        can_analyze_func: Function to check if object can be analyzed
        analyze_func: Function to analyze the object
        create_tool_func: Optional function to create tools
        create_engine_func: Optional function to create engine configs

    Returns:
        Custom analyzer class

    Example:
        >>> def can_analyze_custom(obj):
        ...     return hasattr(obj, "custom_attribute")
        ...
        >>> def analyze_custom(obj, module_path):
        ...     return ComponentInfo(
        ...         name=obj.__name__,
        ...         component_type="custom",
        ...         module_path=module_path,
        ...         # ... other fields
        ...     )
        ...
        >>> CustomAnalyzer = create_custom_analyzer(
        ...     "CustomAnalyzer",
        ...     can_analyze_custom,
        ...     analyze_custom
        ... )
        ...
        >>> discovery = create_discovery(custom_analyzers=[CustomAnalyzer()])
    """
    attrs = {
        "can_analyze": lambda self, obj: can_analyze_func(obj),
        "analyze": lambda self, obj, module_path: analyze_func(obj, module_path),
    }

    if create_tool_func:
        attrs["create_tool"] = lambda self, component_info: create_tool_func(
            component_info
        )

    if create_engine_func:
        attrs["create_engine_config"] = lambda self, component_info: create_engine_func(
            component_info
        )

    return type(name, (ComponentAnalyzer,), attrs)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================


def _find_haive_root() -> str:
    """Find the Haive project root directory."""
    current = Path.cwd()

    # Look for haive-specific markers
    markers = [
        "packages/haive-core",
        "packages/haive-tools",
        "packages/haive-agents",
    ]

    while current != current.parent:
        # Check if all markers exist
        if all((current / marker).exists() for marker in markers[:2]):
            return str(current)

        # Also check for general project markers
        if (current / "pyproject.toml").exists():
            # Check if it's the haive project
            pyproject = current / "pyproject.toml"
            content = pyproject.read_text()
            if "haive" in content.lower():
                return str(current)

        current = current.parent

    # Fallback to current directory
    logger.warning("Could not find Haive project root, using current directory")
    return str(Path.cwd())
