"""Modular documentation builder for package-specific builds.

This module provides the build logic for creating package-specific documentation
with appropriate extension profiles and configurations.
"""

import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# Try to use rich for better UI
try:
    from rich.console import Console
    from rich.logging import RichHandler
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.table import Table
    
    console = Console()
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True)],
    )
    RICH_AVAILABLE = True
except ImportError:
    logging.basicConfig(level=logging.INFO)
    console = None
    RICH_AVAILABLE = False

# Local imports
from package_configs import (
    PACKAGE_PROFILES,
    get_package_extensions,
    ExtensionProfile
)
from extension_configs import get_all_extension_configs
from memory import get_memory_safe_sphinx_config

logger = logging.getLogger("modular_builder")


class ModularSphinxBuilder:
    """Builder for package-specific Sphinx documentation."""
    
    def __init__(self, package: str, profile_level: str = "standard", project_root: Optional[Path] = None):
        """Initialize builder for specific package.
        
        Args:
            package: Package name (core, agents, tools, etc.)
            profile_level: Extension profile level (minimal, standard, full)
            project_root: Optional project root path for resolving package locations
        """
        self.package = package
        self.profile_level = profile_level
        self.project_root = project_root
        self.extensions: List[str] = []
        self.config: Dict[str, Any] = {}
        self.build_stats: Dict[str, Any] = {
            "extensions_loaded": 0,
            "configs_applied": 0,
            "warnings": [],
            "errors": []
        }
    
    def load_extensions(self) -> List[str]:
        """Load extensions for the package and profile level."""
        if RICH_AVAILABLE and console:
            console.print(f"[bold blue]Loading {self.profile_level} extensions for {self.package}[/bold blue]")
        else:
            logger.info(f"Loading {self.profile_level} extensions for {self.package}")
        
        # Get package-specific extensions
        self.extensions = get_package_extensions(self.package, self.profile_level)
        
        # Validate extensions are available
        available_extensions = []
        missing_extensions = []
        
        for ext in self.extensions:
            if self._is_extension_available(ext):
                available_extensions.append(ext)
            else:
                missing_extensions.append(ext)
                self.build_stats["warnings"].append(f"Extension not available: {ext}")
        
        self.extensions = available_extensions
        self.build_stats["extensions_loaded"] = len(self.extensions)
        
        # Log results
        if RICH_AVAILABLE and console:
            if missing_extensions:
                console.print(f"[yellow]⚠️  {len(missing_extensions)} extensions not available[/yellow]")
            console.print(f"[green]✅ Loaded {len(self.extensions)} extensions[/green]")
        else:
            if missing_extensions:
                logger.warning(f"{len(missing_extensions)} extensions not available")
            logger.info(f"Loaded {len(self.extensions)} extensions")
        
        return self.extensions
    
    def apply_configurations(self) -> Dict[str, Any]:
        """Apply configurations for loaded extensions."""
        if RICH_AVAILABLE and console:
            console.print("[bold blue]Applying extension configurations[/bold blue]")
        else:
            logger.info("Applying extension configurations")
        
        # Get memory-safe base config
        memory_config = get_memory_safe_sphinx_config(self.extensions)
        self.config.update(memory_config)
        
        # Get extension-specific configs
        extension_configs = get_all_extension_configs(self.extensions)
        self.config.update(extension_configs)
        
        # Apply package-specific overrides
        package_config = self._get_package_specific_config()
        self.config.update(package_config)
        
        self.build_stats["configs_applied"] = len(extension_configs)
        
        if RICH_AVAILABLE and console:
            console.print(f"[green]✅ Applied {len(extension_configs)} configurations[/green]")
        else:
            logger.info(f"Applied {len(extension_configs)} configurations")
        
        return self.config
    
    def get_sphinx_config(self) -> Dict[str, Any]:
        """Get complete Sphinx configuration for the package."""
        # Load extensions first
        self.load_extensions()
        
        # Apply configurations
        self.apply_configurations()
        
        # Add required base settings
        base_config = {
            "project": f"Haive {self.package.title()}",
            "copyright": "2025, Haive Team",
            "author": "Haive Team",
            "extensions": self.extensions,
            "templates_path": ["_templates"],
            "exclude_patterns": ["_build", "Thumbs.db", ".DS_Store"],
            "html_theme": "furo",
            "html_static_path": ["_static"],
        }
        
        # Merge with loaded config
        final_config = {**base_config, **self.config}
        
        # Add AutoAPI config for the package
        final_config.update(self._get_autoapi_config())
        
        return final_config
    
    def print_build_summary(self):
        """Print a summary of the build configuration."""
        if RICH_AVAILABLE and console:
            # Create summary table
            table = Table(title=f"Build Summary: {self.package} ({self.profile_level})")
            table.add_column("Metric", style="cyan")
            table.add_column("Value", style="green")
            
            table.add_row("Extensions Loaded", str(self.build_stats["extensions_loaded"]))
            table.add_row("Configs Applied", str(self.build_stats["configs_applied"]))
            table.add_row("Warnings", str(len(self.build_stats["warnings"])))
            table.add_row("Errors", str(len(self.build_stats["errors"])))
            
            console.print(table)
            
            # Show warnings if any
            if self.build_stats["warnings"]:
                console.print("\n[yellow]Warnings:[/yellow]")
                for warning in self.build_stats["warnings"]:
                    console.print(f"  • {warning}")
        else:
            # Simple text output
            logger.info(f"\nBuild Summary: {self.package} ({self.profile_level})")
            logger.info(f"  Extensions Loaded: {self.build_stats['extensions_loaded']}")
            logger.info(f"  Configs Applied: {self.build_stats['configs_applied']}")
            logger.info(f"  Warnings: {len(self.build_stats['warnings'])}")
            logger.info(f"  Errors: {len(self.build_stats['errors'])}")
            
            if self.build_stats["warnings"]:
                logger.warning("Warnings:")
                for warning in self.build_stats["warnings"]:
                    logger.warning(f"  • {warning}")
    
    def _is_extension_available(self, extension: str) -> bool:
        """Check if an extension is available for import."""
        if extension.startswith("sphinx.ext."):
            # Built-in Sphinx extensions are always available
            return True
        
        # Map extension names to import names
        import_map = {
            "autoapi.extension": "autoapi",
            "myst_parser": "myst_parser",
            "sphinx_design": "sphinx_design",
            "sphinx_copybutton": "sphinx_copybutton",
            "sphinx_autodoc_typehints": "sphinx_autodoc_typehints",
            "sphinxcontrib.autodoc_pydantic": "sphinxcontrib.autodoc_pydantic",
            "autodocsumm": "autodocsumm",
            "sphinx_tabs": "sphinx_tabs",
            "sphinx_togglebutton": "sphinx_togglebutton",
            "sphinx_paramlinks": "sphinx_paramlinks",
            "sphinxcontrib.mermaid": "sphinxcontrib.mermaid",
            "sphinxcontrib.plantuml": "sphinxcontrib.plantuml",
            "sphinx_inline_tabs": "sphinx_inline_tabs",
            "sphinx_exec_directive": "sphinx_exec_directive",
            "sphinx_examples": "sphinx_examples",
            "sphinx_collapse": "sphinx_collapse",
            "sphinx_tippy": "sphinx_tippy",
            "sphinxcontrib.httpdomain": "sphinxcontrib.httpdomain",
            "sphinx_click": "sphinx_click",
            "sphinx_argparse": "sphinx_argparse",
            "sphinxcontrib.openapi": "sphinxcontrib.openapi",
            "sphinxcontrib.redoc": "sphinxcontrib.redoc",
            "sphinx_prompt": "sphinx_prompt",
            "sphinxcontrib.images": "sphinxcontrib.images",
            "sphinx_panels": "sphinx_panels",
            "sphinxcontrib.youtube": "sphinxcontrib.youtube",
            "sphinx_carousel": "sphinx_carousel",
            "sphinx_charts": "sphinx_charts",
            "sphinx_visualized": "sphinx_visualized",
            "sphinx_jsonschema": "sphinx_jsonschema",
            "sphinx_mcp": "sphinx_mcp",
            "sphinx_diagrams": "sphinx_diagrams",
            "sphinx_uml": "sphinx_uml",
        }
        
        import_name = import_map.get(extension, extension)
        
        try:
            __import__(import_name)
            return True
        except ImportError:
            return False
    
    def _get_package_specific_config(self) -> Dict[str, Any]:
        """Get package-specific configuration overrides."""
        configs = {
            "core": {
                "autodoc_member_order": "bysource",
                "autodoc_typehints": "description",
                "autodoc_class_signature": "mixed",
            },
            "agents": {
                "autodoc_default_options": {
                    "members": True,
                    "member-order": "bysource",
                    "special-members": "__init__",
                    "undoc-members": True,
                    "exclude-members": "__weakref__",
                    "show-inheritance": True,
                },
            },
            "tools": {
                "autodoc_default_options": {
                    "members": True,
                    "undoc-members": False,
                },
            },
            "games": {
                "html_theme_options": {
                    "light_css_variables": {
                        "color-brand-primary": "#7C4DFF",
                        "color-brand-content": "#7C4DFF",
                    },
                },
            },
            "mcp": {
                "autodoc_mock_imports": [
                    "mcp",  # Mock if MCP SDK not installed
                ],
            },
            "dataflow": {
                "graphviz_output_format": "svg",
                "graphviz_dot_args": ["-Grankdir=LR"],
            },
            "prebuilt": {
                "html_theme_options": {
                    "announcement": "Check out our pre-built agent configurations!",
                },
            },
        }
        
        return configs.get(self.package, {})
    
    def _get_package_ignore_patterns(self) -> List[str]:
        """Get ignore patterns for AutoAPI based on package."""
        # Common patterns to ignore
        common_ignores = [
            "*test*",
            "*conftest*",
            "*/.git/*",
            "*/.*",
            "**/examples/**/*.py",
            "**/example*.py",
            "**/*example*.py",
            "**/demos/**/*.py",
            "**/demo*.py",
            "**/test*.py",
            "**/tests/**/*.py",
        ]
        
        # Package-specific ignores
        package_ignores = {
            "agents": [
                # Skip app.py files that cause logger issues
                "**/app.py",
                "**/app/**/*.py",
                # Skip problematic research and wiki-related agents
                "**/research/**/*.py",
                "**/agents/research/**/*.py",
                "**/agents/document_processing/**/*.py",
                # Skip files with generic class patterns that cause TypeError
                "**/supervisor/dynamic_activation_supervisor.py",
                "**/multi/experiments/implementations/*.py",
                "**/multi/base_multi_agent.py",
                "**/multi/enhanced_multi_agent_v3.py",
                "**/multi/enhanced_multi_agent_v4.py",
                "**/memory_v2/test_*.py",
                "**/discovery/semantic_discovery.py",
                "**/discovery/dynamic_tool_selector.py",
                "**/discovery/selection_strategies.py",
                # Modules with missing core dependencies
                "**/agents/base/compiled_agent.py",
                "**/agents/base/universal_agent.py",
                "**/agents/archive/meta/**/*.py",
                # Modules with Pydantic validation errors
                "**/agents/memory_v2/**/*.py",
                # Modules with missing imports
                "**/agents/chain/**/*.py",
                "**/agents/conversation/base/example*.py",
                "**/agents/document_loader/examples/**/*.py",
                "**/agents/document_modifiers/kg/**/*.py",
                "**/agents/experiments/**/*.py",
                "**/agents/memory/models_dir/**/*.py",
                # Multi-agent modules with various issues
                "**/agents/multi/archive/**/*.py",
                "**/agents/multi/enhanced_clean_multi_agent.py",
            ],
            "tools": [
                # Tools with missing dependencies
                "**/tools/google/google_finance.py",
                "**/tools/google/google_jobs.py",
                "**/tools/google/google_scholar.py",
                "**/tools/google/google_trends.py",
                "**/tools/search/wikipedia_search.py",
                "**/tools/search/arxiv_search.py",
                "**/tools/search/semantic_search.py",
            ],
        }
        
        # Combine common and package-specific ignores
        ignores = common_ignores.copy()
        if self.package in package_ignores:
            ignores.extend(package_ignores[self.package])
            
        return ignores
    
    def _get_autoapi_config(self) -> Dict[str, Any]:
        """Get AutoAPI configuration for the package."""
        # Determine package source directory
        package_name = f"haive-{self.package}"
        if self.package == "core":
            package_name = "haive-core"
        
        # Try to find the absolute path to the package
        if self.project_root:
            # Use provided project root
            project_root = self.project_root
        else:
            # Try to auto-detect from current file location
            current_file = Path(__file__).resolve()
            # Go up: modular_builder.py -> conf_modules -> source -> docs -> haive
            project_root = current_file.parent.parent.parent.parent
        
        packages_dir = project_root / "packages" / package_name / "src"
        
        logger.info(f"Project root: {project_root}")
        logger.info(f"Looking for package at: {packages_dir}")
        
        # Use absolute path if it exists, otherwise fall back to relative
        if packages_dir.exists():
            autoapi_dir = str(packages_dir.absolute())
            logger.info(f"Using absolute path for AutoAPI: {autoapi_dir}")
        else:
            # Fallback to relative path (for when running from docs/source)
            autoapi_dir = f"../../packages/{package_name}/src"
            logger.warning(f"Package directory not found at {packages_dir}, using relative path: {autoapi_dir}")
        
        return {
            "autoapi_type": "python",
            "autoapi_dirs": [autoapi_dir],
            "autoapi_root": "api",
            "autoapi_add_toctree_entry": True,
            "autoapi_options": [
                "members",
                "undoc-members",
                "show-inheritance",
                "show-module-summary",
                "imported-members",
            ],
            "autoapi_ignore": self._get_package_ignore_patterns(),
            "autoapi_python_class_content": "both",
            "autoapi_member_order": "bysource",
            "autoapi_python_use_implicit_namespaces": True,
        }


def create_package_config(package: str, profile_level: str = "standard") -> str:
    """Create a Sphinx conf.py content for a specific package.
    
    Args:
        package: Package name (core, agents, tools, etc.)
        profile_level: Extension profile level (minimal, standard, full)
        
    Returns:
        String content for conf.py file
    """
    builder = ModularSphinxBuilder(package, profile_level)
    config = builder.get_sphinx_config()
    
    # Generate conf.py content
    conf_content = f'''"""
Sphinx configuration for Haive {package.title()} package.
Generated by modular build system with {profile_level} profile.
"""

import sys
from pathlib import Path

# Configuration generated by modular builder
'''
    
    # Add extensions
    conf_content += f"\nextensions = {repr(config['extensions'])}\n"
    
    # Add other configurations
    for key, value in config.items():
        if key != "extensions":
            if isinstance(value, str):
                conf_content += f'\n{key} = {repr(value)}'
            else:
                conf_content += f'\n{key} = {repr(value)}'
    
    # Print build summary
    builder.print_build_summary()
    
    return conf_content


def test_all_packages():
    """Test configuration generation for all packages."""
    if RICH_AVAILABLE and console:
        console.print(Panel.fit(
            "[bold blue]Testing Modular Configuration for All Packages[/bold blue]",
            border_style="blue"
        ))
    else:
        logger.info("Testing Modular Configuration for All Packages")
    
    for package in PACKAGE_PROFILES.keys():
        for level in ["minimal", "standard", "full"]:
            if RICH_AVAILABLE and console:
                console.print(f"\n[cyan]Testing {package} with {level} profile[/cyan]")
            else:
                logger.info(f"\nTesting {package} with {level} profile")
            
            builder = ModularSphinxBuilder(package, level)
            config = builder.get_sphinx_config()
            
            if RICH_AVAILABLE and console:
                console.print(f"  Extensions: {len(config['extensions'])}")
                console.print(f"  AutoAPI dirs: {config.get('autoapi_dirs', 'Not configured')}")
            else:
                logger.info(f"  Extensions: {len(config['extensions'])}")
                logger.info(f"  AutoAPI dirs: {config.get('autoapi_dirs', 'Not configured')}")


if __name__ == "__main__":
    # Test the builder
    test_all_packages()
    
    # Example: Generate config for agents package
    print("\n" + "="*60)
    print("Example conf.py for haive-agents (standard profile):")
    print("="*60)
    
    conf_content = create_package_config("agents", "standard")
    print(conf_content[:500] + "...\n[truncated]")