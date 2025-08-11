#!/usr/bin/env python3
"""
Haive Modular Documentation Sync System
Ensures each package has independent, complete documentation while staying synced
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class ModularDocsManager:
    """Manages modular documentation system for all Haive packages"""

    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.shared_docs = repo_root / "shared" / "docs"
        self.packages_dir = repo_root / "packages"
        self.sync_config = self.shared_docs / "sync_config.json"

        # Load package configurations
        self.packages = self.load_package_config()

    def load_package_config(self) -> Dict:
        """Load package configuration from JSON file"""
        config_file = self.shared_docs / "package_config.json"
        if not config_file.exists():
            self.create_default_config(config_file)

        return json.loads(config_file.read_text())

    def create_default_config(self, config_file: Path):
        """Create default package configuration"""
        default_config = {
            "packages": {
                "haive-core": {
                    "title": "Haive Core Framework",
                    "description": "Core components, engines, and base infrastructure",
                    "color": "#2563eb",
                    "priority": 1,
                    "has_cli": False,
                    "has_examples": True,
                },
                "haive-agents": {
                    "title": "Haive Agents",
                    "description": "Pre-built AI agents with specialized capabilities",
                    "color": "#059669",
                    "priority": 2,
                    "has_cli": False,
                    "has_examples": True,
                },
                "haive-dataflow": {
                    "title": "Haive Dataflow",
                    "description": "Data processing pipelines and persistence systems",
                    "color": "#7c3aed",
                    "priority": 3,
                    "has_cli": True,
                    "has_examples": True,
                },
                "haive-games": {
                    "title": "Haive Games",
                    "description": "Game-playing agents and tournament systems",
                    "color": "#dc2626",
                    "priority": 4,
                    "has_cli": False,
                    "has_examples": True,
                },
                "haive-mcp": {
                    "title": "Haive MCP",
                    "description": "Model Context Protocol integration and server management",
                    "color": "#ea580c",
                    "priority": 5,
                    "has_cli": True,
                    "has_examples": True,
                },
                "haive-tools": {
                    "title": "Haive Tools",
                    "description": "Utility tools and helper functions",
                    "color": "#0891b2",
                    "priority": 6,
                    "has_cli": False,
                    "has_examples": True,
                },
                "haive-prebuilt": {
                    "title": "Haive Prebuilt",
                    "description": "Ready-to-use components and templates",
                    "color": "#be123c",
                    "priority": 7,
                    "has_cli": False,
                    "has_examples": False,
                },
            },
            "sync_settings": {
                "template_version": "1.0.0",
                "last_sync": None,
                "auto_sync": True,
                "preserve_customizations": True,
            },
        }

        config_file.write_text(json.dumps(default_config, indent=2))
        return default_config

    def sync_all_packages(self, force: bool = False):
        """Sync documentation to all packages with modularity checks"""
        print("🚀 Starting Haive Modular Documentation Sync")
        print(f"📁 Repository: {self.repo_root}")
        print(f"📦 Packages: {len(self.packages['packages'])}")
        print()

        # Check if sync is needed
        if not force and not self.needs_sync():
            print("✅ All packages are up to date. Use --force to sync anyway.")
            return

        # Sync each package
        results = {}
        for package_name, config in self.packages["packages"].items():
            print(f"📦 Syncing {package_name}...")
            try:
                result = self.sync_package_modular(package_name, config)
                results[package_name] = {"status": "success", "details": result}
                print(f"✅ {package_name}: {result}")
            except Exception as e:
                results[package_name] = {"status": "error", "error": str(e)}
                print(f"❌ {package_name}: {e}")
            print()

        # Update sync record
        self.update_sync_record(results)
        print("🎉 Modular sync complete!")

    def sync_package_modular(self, package_name: str, config: Dict) -> str:
        """Sync single package with full modularity"""
        package_dir = self.packages_dir / package_name
        if not package_dir.exists():
            raise FileNotFoundError(f"Package directory not found: {package_dir}")

        docs_dir = package_dir / "docs"
        source_dir = docs_dir / "source"

        # Create complete independent docs structure
        self.create_package_structure(docs_dir, source_dir)

        # Copy shared assets (with package-specific overrides)
        self.copy_shared_assets_modular(source_dir, package_name)

        # Generate customized conf.py (full 635-line template)
        self.generate_package_conf(source_dir, package_name, config)

        # Generate package-specific index.rst
        self.generate_package_index(source_dir, package_name, config)

        # Create build files (Makefile, make.bat)
        self.create_build_files(docs_dir)

        # Test the configuration (syntax check)
        self.validate_package_config(source_dir)

        return "Complete independent documentation system created"

    def create_package_structure(self, docs_dir: Path, source_dir: Path):
        """Create complete directory structure for package docs"""
        dirs_to_create = [
            docs_dir,
            source_dir,
            source_dir / "_static",
            source_dir / "_templates",
            source_dir / "_autoapi_templates",
            docs_dir / "build",
        ]

        for dir_path in dirs_to_create:
            dir_path.mkdir(parents=True, exist_ok=True)

    def copy_shared_assets_modular(self, target_source: Path, package_name: str):
        """Copy shared assets with package-specific override support"""
        main_source = self.repo_root / "docs" / "source"

        # Copy shared static assets
        shared_static = main_source / "_static"
        target_static = target_source / "_static"

        if shared_static.exists():
            # Copy all shared static files
            shutil.copytree(shared_static, target_static, dirs_exist_ok=True)

        # Copy package-specific overrides if they exist
        package_overrides = self.shared_docs / "package_overrides" / package_name
        if package_overrides.exists():
            shutil.copytree(package_overrides, target_source, dirs_exist_ok=True)

        # Copy shared templates
        shared_templates = main_source / "_templates"
        target_templates = target_source / "_templates"
        if shared_templates.exists():
            shutil.copytree(shared_templates, target_templates, dirs_exist_ok=True)

        # Copy autoapi templates
        shared_autoapi = main_source / "_autoapi_templates"
        target_autoapi = target_source / "_autoapi_templates"
        if shared_autoapi.exists():
            shutil.copytree(shared_autoapi, target_autoapi, dirs_exist_ok=True)

    def generate_package_conf(self, source_dir: Path, package_name: str, config: Dict):
        """Generate complete conf.py from full template"""
        template_file = self.shared_docs / "conf_template_full.py"
        if not template_file.exists():
            raise FileNotFoundError(f"Template file not found: {template_file}")

        template_content = template_file.read_text()

        # Apply package-specific customizations
        customized = self.apply_template_customizations(
            template_content, package_name, config
        )

        # Write to package
        conf_file = source_dir / "conf.py"
        conf_file.write_text(customized)

        # Add package-specific metadata comment
        self.add_package_metadata(conf_file, package_name, config)

    def apply_template_customizations(
        self, template: str, package_name: str, config: Dict
    ) -> str:
        """Apply all package-specific template customizations"""
        # All the same replacements as in the previous script
        # But more systematic and trackable

        replacements = [
            # Header
            (
                "# Generated Sphinx Configuration\\n# Auto-generated by PyAutoDoc ConfigLoader\\n# DO NOT EDIT MANUALLY - Edit YAML files instead",
                f'# {config["title"]} Documentation\\n# Generated from Haive shared template\\n# Package: {package_name}',
            ),
            # Paths (key difference from PyAutoDoc)
            (
                'sys.path.insert(0, os.path.abspath("../../src"))',
                'sys.path.insert(0, os.path.abspath("../src"))',
            ),
            ('autoapi_dirs = ["../../src"]', 'autoapi_dirs = ["../src"]'),
            # Project info
            ('project = "pyautodoc"', f'project = "{config["title"]}"'),
            ('author = "William R. Astley"', 'author = "Haive Team"'),
            ('copyright = "2025, William R. Astley"', 'copyright = "2025, Haive Team"'),
            # Repository links
            (
                '"source_repository": "https://github.com/yourusername/pyautodoc/"',
                '"source_repository": "https://github.com/prim8/haive/"',
            ),
            (
                '"source_directory": "docs/"',
                f'"source_directory": "packages/{package_name}/docs/"',
            ),
            # Branding
            (
                'html_baseurl = "https://pyautodoc.readthedocs.io/"',
                f'html_baseurl = "https://haive.readthedocs.io/packages/{package_name}/"',
            ),
            ('ogp_site_name = "PyAutoDoc"', f'ogp_site_name = "{config["title"]}"'),
            (
                'ogp_site_description = "Hyper-organized documentation system with intense Furo theming"',
                f'ogp_site_description = "{config["description"]}"',
            ),
            # Color scheme
            (
                '"color-brand-primary": "#2563eb"',
                f'"color-brand-primary": "{config["color"]}"',
            ),
            # Final message
            (
                'print("✨ Intense Furo theme with sphinx-design enabled!")',
                f'print("✨ {config["title"]} documentation system loaded!")',
            ),
        ]

        # Apply all replacements
        result = template
        for old, new in replacements:
            result = result.replace(old, new)

        return result

    def add_package_metadata(self, conf_file: Path, package_name: str, config: Dict):
        """Add metadata comment to track sync info"""
        metadata = f"""
# HAIVE PACKAGE DOCUMENTATION METADATA
# Package: {package_name}
# Title: {config["title"]}
# Sync Version: {self.packages["sync_settings"]["template_version"]}
# Generated: {datetime.now().isoformat()}
# Source Template: shared/docs/conf_template_full.py

"""

        original_content = conf_file.read_text()
        conf_file.write_text(metadata + original_content)

    def generate_package_index(self, source_dir: Path, package_name: str, config: Dict):
        """Generate package-specific index.rst"""
        package_part = package_name.replace("haive-", "")

        # More sophisticated index based on package features
        index_content = self.build_package_index_content(
            package_name, package_part, config
        )

        (source_dir / "index.rst").write_text(index_content)

    def build_package_index_content(
        self, package_name: str, package_part: str, config: Dict
    ) -> str:
        """Build rich index content based on package configuration"""
        title_line = "=" * (len(config["title"]) + 13)

        # Base content
        content = f"""{config["title"]} Documentation
{title_line}

Welcome to **{config["title"]}** - {config["description"]}.

This package is part of the Haive AI Agent Framework ecosystem.

.. admonition:: Framework Integration
   :class: tip

   {config["title"]} seamlessly integrates with other Haive packages. 
   See the `complete framework documentation <https://github.com/prim8/haive>`_ for the full ecosystem.

"""

        # Add package-specific sections based on config
        if config.get("has_examples", False):
            content += """
Examples
--------

Explore practical examples and tutorials:

.. toctree::
   :maxdepth: 2
   :caption: Examples
   
   examples/index

"""

        if config.get("has_cli", False):
            content += """
Command Line Interface
----------------------

{config["title"]} provides CLI tools for easy interaction:

.. toctree::
   :maxdepth: 2
   :caption: CLI Reference
   
   cli/index

"""

        # API documentation (always included)
        content += f"""
API Reference
-------------

Complete API documentation for {config["title"]}:

.. toctree::
   :maxdepth: 2
   :caption: API Documentation
   
   autoapi/index

"""

        # Footer
        content += """
Development
-----------

.. toctree::
   :maxdepth: 1
   :caption: Development
   
   GitHub Repository <https://github.com/prim8/haive>
   Contributing Guide <https://github.com/prim8/haive/blob/main/CONTRIBUTING.md>
   Issue Tracker <https://github.com/prim8/haive/issues>

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
"""

        return content.strip()

    def create_build_files(self, docs_dir: Path):
        """Create Makefile and make.bat for independent building"""
        # Standard Sphinx Makefile
        makefile_content = """# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = source
BUILDDIR      = build

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
"""

        (docs_dir / "Makefile").write_text(makefile_content)

        # Windows batch file
        bat_content = """@ECHO OFF

pushd %~dp0

REM Command file for Sphinx documentation

if "%SPHINXBUILD%" == "" (
	set SPHINXBUILD=sphinx-build
)
set SOURCEDIR=source
set BUILDDIR=build

%SPHINXBUILD% >NUL 2>NUL
if errorlevel 9009 (
	echo.
	echo.The 'sphinx-build' command was not found. Make sure you have Sphinx
	echo.installed, then set the SPHINXBUILD environment variable to point
	echo.to the full path of the 'sphinx-build' executable. Alternatively you
	echo.may add the Sphinx directory to PATH.
	echo.
	echo.If you don't have Sphinx installed, grab it from
	echo.https://www.sphinx-doc.org/
	exit /b 1
)

if "%1" == "" goto help

%SPHINXBUILD% -M %1 %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%
goto end

:help
%SPHINXBUILD% -M help %SOURCEDIR% %BUILDDIR% %SPHINXOPTS% %O%

:end
popd
"""
        (docs_dir / "make.bat").write_text(bat_content)

    def validate_package_config(self, source_dir: Path):
        """Validate that the generated config is syntactically correct"""
        conf_file = source_dir / "conf.py"

        # Simple syntax check
        try:
            compile(conf_file.read_text(), str(conf_file), "exec")
        except SyntaxError as e:
            raise ValueError(f"Generated conf.py has syntax error: {e}")

    def needs_sync(self) -> bool:
        """Check if sync is needed based on timestamps and versions"""
        # For now, always return True - we can add smarter logic later
        return True

    def update_sync_record(self, results: Dict):
        """Update sync record with results"""
        sync_record = {
            "timestamp": datetime.now().isoformat(),
            "template_version": self.packages["sync_settings"]["template_version"],
            "results": results,
        }

        sync_file = self.shared_docs / "last_sync.json"
        sync_file.write_text(json.dumps(sync_record, indent=2))


def main():
    """Main CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="Haive Modular Documentation Sync")
    parser.add_argument(
        "--force", action="store_true", help="Force sync even if up to date"
    )
    parser.add_argument("--package", type=str, help="Sync specific package only")
    parser.add_argument(
        "--validate", action="store_true", help="Validate existing configs"
    )

    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent.parent
    manager = ModularDocsManager(repo_root)

    if args.validate:
        print("🔍 Validating existing package configurations...")
        # Add validation logic here
        return

    if args.package:
        print(f"🎯 Syncing single package: {args.package}")
        # Add single package sync logic here
        return

    manager.sync_all_packages(force=args.force)


if __name__ == "__main__":
    main()
