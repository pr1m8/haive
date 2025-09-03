"""Auto-discovery of modules for comprehensive Sphinx documentation."""

from __future__ import annotations

import importlib
import pkgutil
import sys
from pathlib import Path


def discover_modules(package_name, base_path=None):
    """Discover all modules in a package recursively."""
    modules = []

    try:
        # Import the package
        package = importlib.import_module(package_name)

        # If base_path not provided, use package path
        if base_path is None:
            if hasattr(package, "__path__"):
                base_path = package.__path__[0]
            else:
                return modules

        # Walk through all modules in the package
        for _importer, modname, ispkg in pkgutil.walk_packages(
            package.__path__,
            package.__name__ + ".",
        ):
            try:
                # Try to import the module to ensure it's valid
                importlib.import_module(modname)
                modules.append(modname)

                # If it's a package, also add it
                if ispkg:
                    modules.append(modname)

            except (ImportError, AttributeError, ModuleNotFoundError):
                continue

    except (ImportError, AttributeError, ModuleNotFoundError):
        pass

    return sorted(set(modules))


def discover_haive_modules():
    """Discover all Haive modules."""
    all_modules = {}

    # Base packages to discover
    packages = [
        "haive.core",
        "haive.agents",
        "haive.tools",
        "haive.games",
        "haive.dataflow",
        "haive.prebuilt",
        "haive.mcp",
    ]

    for package in packages:
        modules = discover_modules(package)
        all_modules[package] = modules

    return all_modules


def generate_autosummary_rst(modules_dict, output_file):
    """Generate RST content for autosummary."""
    content = []

    for package, modules in modules_dict.items():
        content.append(f"\n{package} Modules")
        content.append("=" * (len(package) + 8))
        content.append("")
        content.append(".. autosummary::")
        content.append("   :toctree: generated")
        content.append("   :template: module.rst")
        content.append("   :recursive:")
        content.append("")

        for module in modules:
            content.append(f"   {module}")
        content.append("")

    # Write to file
    with open(output_file, "w") as f:
        f.write("\n".join(content))


if __name__ == "__main__":
    # Add package paths to sys.path
    project_root = Path(__file__).parent.parent.parent.parent
    packages_dir = project_root / "packages"

    for package_dir in packages_dir.glob("haive-*"):
        src_dir = package_dir / "src"
        if src_dir.exists():
            sys.path.insert(0, str(src_dir))

    # Discover all modules
    modules = discover_haive_modules()

    # Print results
    for _package, mods in modules.items():
        for _mod in mods:
            pass

    # Generate RST file
    output_file = Path(__file__).parent.parent / "auto_modules.rst"
    generate_autosummary_rst(modules, output_file)
