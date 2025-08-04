"""Package-specific extension profiles for modular documentation builds.

This module defines extension profiles (minimal, standard, full) for
each Haive package, allowing targeted documentation builds with only the
necessary extensions.
"""

from __future__ import annotations


class ExtensionProfile:
    """Container for package-specific extension profiles."""

    def __init__(self, package_name: str):
        self.package_name = package_name
        self._minimal: list[str] = []
        self._standard: list[str] = []
        self._full: list[str] = []

    @property
    def minimal(self) -> list[str]:
        """Minimal extensions for basic documentation."""
        return self._minimal.copy()

    @property
    def standard(self) -> list[str]:
        """Standard extensions for typical documentation."""
        return list(set(self._minimal + self._standard))

    @property
    def full(self) -> list[str]:
        """Full extensions including all features."""
        return list(set(self._minimal + self._standard + self._full))

    def get_profile(self, level: str = "standard") -> list[str]:
        """Get extensions for specified profile level."""
        if level == "minimal":
            return self.minimal
        if level == "full":
            return self.full
        return self.standard


def get_core_minimal_extensions() -> list[str]:
    """Core Sphinx extensions needed by all packages."""
    return [
        # Essential Sphinx extensions
        "sphinx.ext.autodoc",
        "sphinx.ext.napoleon",
        "sphinx.ext.viewcode",
        "sphinx.ext.intersphinx",
        # Essential third-party
        "autoapi.extension",
        "myst_parser",
    ]


def get_haive_core_profile() -> ExtensionProfile:
    """Extension profile for haive-core package."""
    profile = ExtensionProfile("haive-core")

    # Minimal - just the essentials for API docs
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx.ext.inheritance_diagram",  # For class hierarchies
        "sphinx_autodoc_typehints",  # For type hints
    ]

    # Standard - add useful features
    profile._standard = [
        "sphinx.ext.graphviz",  # For architecture diagrams
        "sphinx_design",  # For cards/tabs
        "sphinx_copybutton",  # For code copy
        "sphinxcontrib.mermaid",  # For diagrams
        "autodocsumm",  # For better summaries
        "sphinxcontrib.autodoc_pydantic",  # For Pydantic models
    ]

    # Full - everything including development tools
    profile._full = [
        "sphinx.ext.coverage",
        "sphinx.ext.doctest",
        "sphinx.ext.todo",
        "sphinxcontrib.plantuml",
        "sphinx_paramlinks",
        "sphinx_inline_tabs",
    ]

    return profile


def get_haive_agents_profile() -> ExtensionProfile:
    """Extension profile for haive-agents package."""
    profile = ExtensionProfile("haive-agents")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
        "sphinxcontrib.autodoc_pydantic",  # Essential for agent configs
    ]

    # Standard - add agent-specific features
    profile._standard = [
        "sphinx.ext.graphviz",
        "sphinx_design",
        "sphinx_copybutton",
        "sphinxcontrib.mermaid",  # For agent flow diagrams
        "autodocsumm",
        "sphinx_tabs",  # For multi-agent examples
        "sphinx_togglebutton",  # For collapsible sections
        "sphinx_paramlinks",  # For parameter linking
    ]

    # Full - add advanced features
    profile._full = [
        "sphinx.ext.doctest",
        "sphinxcontrib.plantuml",
        "sphinx_exec_directive",  # For live examples
        "sphinx_examples",  # For example galleries
        "sphinx_collapse",  # For complex examples
        "sphinx_tippy",  # For tooltips
    ]

    return profile


def get_haive_tools_profile() -> ExtensionProfile:
    """Extension profile for haive-tools package."""
    profile = ExtensionProfile("haive-tools")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
    ]

    # Standard
    profile._standard = [
        "sphinx_design",
        "sphinx_copybutton",
        "sphinxcontrib.httpdomain",  # For API documentation
        "sphinx_click",  # For CLI tools
        "sphinx_argparse",  # For argparse docs
        "autodocsumm",
    ]

    # Full
    profile._full = [
        "sphinxcontrib.openapi",  # For OpenAPI specs
        "sphinxcontrib.redoc",  # For API visualization
        "sphinx_exec_directive",
        "sphinx_prompt",  # For command examples
    ]

    return profile


def get_haive_games_profile() -> ExtensionProfile:
    """Extension profile for haive-games package."""
    profile = ExtensionProfile("haive-games")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
    ]

    # Standard - add visualization
    profile._standard = [
        "sphinx_design",
        "sphinx_copybutton",
        "sphinxcontrib.mermaid",  # For game flow
        "sphinxcontrib.images",  # For game screenshots
        "sphinx_panels",  # For game galleries
        "autodocsumm",
    ]

    # Full - add interactive features
    profile._full = [
        "sphinxcontrib.youtube",  # For game videos
        "sphinx_carousel",  # For image carousels
        "sphinx_charts",  # For game statistics
        "sphinx_visualized",  # For visualizations
    ]

    return profile


def get_haive_mcp_profile() -> ExtensionProfile:
    """Extension profile for haive-mcp package."""
    profile = ExtensionProfile("haive-mcp")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
    ]

    # Standard
    profile._standard = [
        "sphinx_design",
        "sphinx_copybutton",
        "sphinxcontrib.httpdomain",  # For MCP protocol
        "sphinxcontrib.openapi",  # For API specs
        "sphinx_jsonschema",  # For JSON schemas
        "autodocsumm",
    ]

    # Full
    profile._full = [
        "sphinxcontrib.redoc",
        "sphinx_exec_directive",
        "sphinx_mcp",  # MCP-specific if available
    ]

    return profile


def get_haive_dataflow_profile() -> ExtensionProfile:
    """Extension profile for haive-dataflow package."""
    profile = ExtensionProfile("haive-dataflow")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
    ]

    # Standard - add flow visualization
    profile._standard = [
        "sphinx_design",
        "sphinx_copybutton",
        "sphinxcontrib.mermaid",  # For dataflow diagrams
        "sphinx.ext.graphviz",  # For complex flows
        "autodocsumm",
        "sphinxcontrib.plantuml",  # For UML diagrams
    ]

    # Full
    profile._full = [
        "sphinx_diagrams",  # For advanced diagrams
        "sphinx_uml",  # For UML
        "sphinx_exec_directive",
    ]

    return profile


def get_haive_prebuilt_profile() -> ExtensionProfile:
    """Extension profile for haive-prebuilt package."""
    profile = ExtensionProfile("haive-prebuilt")

    # Minimal
    profile._minimal = get_core_minimal_extensions() + [
        "sphinx_autodoc_typehints",
        "sphinxcontrib.autodoc_pydantic",  # For configurations
    ]

    # Standard - focus on examples
    profile._standard = [
        "sphinx_design",
        "sphinx_copybutton",
        "sphinx_tabs",  # For multiple examples
        "sphinx_togglebutton",  # For collapsible configs
        "autodocsumm",
        "sphinx_inline_tabs",  # For inline examples
    ]

    # Full
    profile._full = [
        "sphinx_examples",  # For example gallery
        "sphinx_exec_directive",  # For live demos
        "sphinx_collapse",  # For complex configs
    ]

    return profile


# Package profile registry
PACKAGE_PROFILES: dict[str, ExtensionProfile] = {
    "core": get_haive_core_profile(),
    "agents": get_haive_agents_profile(),
    "tools": get_haive_tools_profile(),
    "games": get_haive_games_profile(),
    "mcp": get_haive_mcp_profile(),
    "dataflow": get_haive_dataflow_profile(),
    "prebuilt": get_haive_prebuilt_profile(),
}


def get_package_extensions(package: str, level: str = "standard") -> list[str]:
    """Get extensions for a specific package and profile level.

    Args:
        package: Package name (core, agents, tools, etc.)
        level: Profile level (minimal, standard, full)

    Returns:
        List of extension names
    """
    if package not in PACKAGE_PROFILES:
        # Default to core profile for unknown packages
        return get_core_minimal_extensions()

    return PACKAGE_PROFILES[package].get_profile(level)


def get_all_unique_extensions() -> set[str]:
    """Get all unique extensions across all packages and profiles."""
    all_extensions = set()

    for profile in PACKAGE_PROFILES.values():
        all_extensions.update(profile.full)

    return all_extensions


def get_extension_usage_map() -> dict[str, list[str]]:
    """Get mapping of extensions to packages that use them."""
    usage_map: dict[str, list[str]] = {}

    for package_name, profile in PACKAGE_PROFILES.items():
        for ext in profile.full:
            if ext not in usage_map:
                usage_map[ext] = []
            usage_map[ext].append(package_name)

    return usage_map


def get_common_extensions(threshold: int = 3) -> list[str]:
    """Get extensions used by at least 'threshold' packages."""
    usage_map = get_extension_usage_map()
    return [
        ext for ext, packages in usage_map.items()
        if len(packages) >= threshold
    ]


if __name__ == "__main__":
    # Test the profiles
    print("Package Extension Profiles Test\n")

    for package_name, profile in PACKAGE_PROFILES.items():
        print(f"\n{package_name.upper()} Package:")
        print(f"  Minimal: {len(profile.minimal)} extensions")
        print(f"  Standard: {len(profile.standard)} extensions")
        print(f"  Full: {len(profile.full)} extensions")

    print(f"\n\nTotal unique extensions: {len(get_all_unique_extensions())}")

    common = get_common_extensions(4)
    print(f"\nExtensions used by 4+ packages: {len(common)}")
    for ext in sorted(common):
        print(f"  - {ext}")
