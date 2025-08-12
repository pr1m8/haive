#!/usr/bin/env python3
"""
Configuration Loader for PyAutoDoc
Loads YAML configurations and environment variables for hyper-organized Sphinx builds
"""

import logging
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


@dataclass
class ExtensionConfig:
    """Configuration for a single Sphinx extension."""

    name: str
    priority: int
    package: Optional[str] = None
    required: bool = False
    enabled_by_default: bool = True
    requires: List[str] = None
    config: Dict[str, Any] = None

    def __post_init__(self):
        if self.requires is None:
            self.requires = []
        if self.config is None:
            self.config = {}


class ConfigLoader:
    """Loads and manages PyAutoDoc configuration from YAML and environment files."""

    def __init__(self, config_dir: str = None):
        if config_dir is None:
            config_dir = Path(__file__).parent
        self.config_dir = Path(config_dir)
        self.extensions: Dict[str, ExtensionConfig] = {}
        self.theme_config: Dict[str, Any] = {}
        self.env_vars: Dict[str, str] = {}

    def load_environment(self, env_file: str = "sphinx.env") -> Dict[str, str]:
        """Load environment variables from .env file."""
        env_path = self.config_dir / env_file
        env_vars = {}

        if env_path.exists():
            with open(env_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        env_vars[key.strip()] = value.strip()

        # Override with actual environment variables
        for key, default_value in env_vars.items():
            env_vars[key] = os.environ.get(key, default_value)

        self.env_vars = env_vars
        return env_vars

    def load_extensions(
        self, extensions_file: str = "extensions.yaml"
    ) -> Dict[str, ExtensionConfig]:
        """Load extension configurations from YAML."""
        extensions_path = self.config_dir / extensions_file

        if not extensions_path.exists():
            logger.error(f"Extensions file not found: {extensions_path}")
            return {}

        with open(extensions_path, "r") as f:
            data = yaml.safe_load(f)

        extensions = {}

        # Process each category
        for category, category_extensions in data.items():
            if category in ["profiles"]:  # Skip non-extension sections
                continue

            if not isinstance(category_extensions, dict):
                continue

            for ext_name, ext_config in category_extensions.items():
                if not isinstance(ext_config, dict):
                    continue

                extensions[ext_name] = ExtensionConfig(
                    name=ext_name,
                    priority=ext_config.get("priority", 100),
                    package=ext_config.get("package"),
                    required=ext_config.get("required", False),
                    enabled_by_default=ext_config.get("enabled_by_default", True),
                    requires=ext_config.get("requires", []),
                    config=ext_config.get("config", {}),
                )

        self.extensions = extensions
        return extensions

    def load_theme_config(self, theme_file: str = None) -> Dict[str, Any]:
        """Load theme configuration from YAML."""
        if theme_file is None:
            theme = self.env_vars.get("SPHINX_THEME", "furo")
            theme_file = f"{theme}.yaml"

        theme_path = self.config_dir / theme_file

        if not theme_path.exists():
            logger.warning(f"Theme config not found: {theme_path}")
            return {}

        with open(theme_path, "r") as f:
            self.theme_config = yaml.safe_load(f)

        return self.theme_config

    def get_extension_list(self, profile: str = None) -> List[str]:
        """Get ordered list of extensions based on profile."""
        if profile is None:
            profile = self.env_vars.get("SPHINX_EXTENSION_PROFILE", "standard")

        # Load profiles from extensions.yaml
        extensions_path = self.config_dir / "extensions.yaml"
        with open(extensions_path, "r") as f:
            data = yaml.safe_load(f)

        profiles = data.get("profiles", {})
        categories = profiles.get(profile, ["core"])

        # Get all extensions from specified categories
        selected_extensions = []
        for category in categories:
            category_data = data.get(category, {})
            for ext_name in category_data.keys():
                if ext_name in self.extensions:
                    ext_config = self.extensions[ext_name]
                    if ext_config.enabled_by_default or ext_config.required:
                        selected_extensions.append(ext_name)

        # Sort by priority
        selected_extensions.sort(key=lambda x: self.extensions[x].priority)

        return selected_extensions

    def get_sphinx_config(self) -> Dict[str, Any]:
        """Generate complete Sphinx configuration dictionary."""
        extensions_list = self.get_extension_list()

        # Base configuration
        config = {
            "extensions": extensions_list,
            "project": "pyautodoc",
            "author": "William R. Astley",
            "copyright": "2025, William R. Astley",
            "release": "0.1.0",
            "templates_path": ["_templates", "_autoapi_templates"],
            "html_static_path": ["_static"],
            "exclude_patterns": [],
            "add_module_names": False,
            "toc_object_entries_show_parents": "hide",
            "jinja_env_options": {"extensions": ["jinja2.ext.do"]},
        }

        # Add extension-specific configurations
        for ext_name in extensions_list:
            if ext_name in self.extensions:
                ext_config = self.extensions[ext_name].config
                config.update(ext_config)

        # Add theme configuration
        if self.theme_config:
            theme_config = self.theme_config.get("theme", {})
            theme_options = self.theme_config.get("options", {})

            config["html_theme"] = theme_config.get("name", "furo")
            if theme_options:
                config["html_theme_options"] = theme_options

            # Custom CSS/JS
            custom_css = self.theme_config.get("custom_css", [])
            custom_js = self.theme_config.get("custom_js", [])

            if custom_css:
                config.setdefault("html_css_files", []).extend(custom_css)
            if custom_js:
                config.setdefault("html_js_files", []).extend(custom_js)

        return config

    def check_dependencies(self) -> Dict[str, List[str]]:
        """Check extension dependencies and return missing packages."""
        missing = {}

        for ext_name, ext_config in self.extensions.items():
            if not ext_config.package:
                continue

            try:
                __import__(ext_config.package.replace("-", "_"))
            except ImportError:
                missing[ext_name] = [ext_config.package]

        return missing

    def generate_sphinx_conf(self, output_file: str = None) -> str:
        """Generate a complete conf.py file."""
        if output_file is None:
            output_file = self.config_dir.parent / "source" / "conf_generated.py"

        config = self.get_sphinx_config()

        conf_content = f"""# Generated Sphinx Configuration
# Auto-generated by PyAutoDoc ConfigLoader
# DO NOT EDIT MANUALLY - Edit YAML files instead

import os
import sys
from sphinx.application import Sphinx

# Path setup
sys.path.insert(0, os.path.abspath("../../src"))

# Project information
project = "{config['project']}"
author = "{config['author']}"
copyright = "{config['copyright']}"
release = "{config['release']}"

# Extensions
extensions = {config['extensions']!r}

# General configuration
templates_path = {config['templates_path']!r}
html_static_path = {config['html_static_path']!r}
exclude_patterns = {config['exclude_patterns']!r}
add_module_names = {config['add_module_names']!r}
toc_object_entries_show_parents = "{config['toc_object_entries_show_parents']}"

# Jinja2 options
jinja_env_options = {config['jinja_env_options']!r}

"""

        # Add extension-specific configs
        for key, value in config.items():
            if key not in [
                "extensions",
                "project",
                "author",
                "copyright",
                "release",
                "templates_path",
                "html_static_path",
                "exclude_patterns",
                "add_module_names",
                "toc_object_entries_show_parents",
                "jinja_env_options",
                "html_theme",
                "html_theme_options",
                "html_css_files",
                "html_js_files",
            ]:
                conf_content += f"{key} = {value!r}\n"

        # Add theme configuration
        if "html_theme" in config:
            conf_content += f"\n# Theme configuration\n"
            conf_content += f"html_theme = {config['html_theme']!r}\n"

            if "html_theme_options" in config:
                conf_content += (
                    f"html_theme_options = {config['html_theme_options']!r}\n"
                )

            if "html_css_files" in config:
                conf_content += f"html_css_files = {config['html_css_files']!r}\n"

            if "html_js_files" in config:
                conf_content += f"html_js_files = {config['html_js_files']!r}\n"

        # Add event hooks
        conf_content += """
# Event Hooks
def autoapi_skip_member(app, what, name, obj, skip, options):
    if name.startswith("__pydantic"):
        return True
    return None

def setup(app: Sphinx):
    app.connect("autoapi-skip-member", autoapi_skip_member)
"""

        # Write to file if output_file is provided
        if output_file:
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "w") as f:
                f.write(conf_content)

            logger.info(f"Generated Sphinx configuration: {output_path}")

        return conf_content


if __name__ == "__main__":
    # CLI usage for testing
    loader = ConfigLoader()
    loader.load_environment()
    loader.load_extensions()
    loader.load_theme_config()

    print("Environment Variables:")
    for key, value in loader.env_vars.items():
        print(f"  {key} = {value}")

    print(f"\nLoaded {len(loader.extensions)} extensions")

    extensions_list = loader.get_extension_list()
    print(f"\nActive Extensions ({len(extensions_list)}):")
    for ext in extensions_list:
        priority = loader.extensions[ext].priority
        print(f"  {priority:2d}: {ext}")

    missing = loader.check_dependencies()
    if missing:
        print(f"\nMissing Dependencies:")
        for ext, packages in missing.items():
            print(f"  {ext}: {', '.join(packages)}")

    print(f"\nGenerating conf.py...")
    conf_content = loader.generate_sphinx_conf()
    print("Configuration generated successfully!")
