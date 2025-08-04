"""Granular documentation testing sessions.

This module provides fine-grained control over documentation testing,
allowing developers to test specific packages, configurations, and
changes incrementally.
"""

import json
import os
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional

import nox
from env_utils import ensure_poetry_sync, log_environment_info

# Configuration
PYTHON_VERSIONS = ["3.12"]
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"

# Package-level testing configurations
PACKAGES = {
    "core": {
        "path": "packages/haive-core/src",
        "autoapi_dirs": ["../../packages/haive-core/src"],
        "description": "Core framework components",
        "priority": 1,  # Build order priority
        "dependencies": [],  # No dependencies
    },
    "agents": {
        "path": "packages/haive-agents/src",
        "autoapi_dirs": ["../../packages/haive-agents/src"],
        "description": "Agent implementations",
        "priority": 2,
        "dependencies": ["core"],  # Depends on core
    },
    "tools": {
        "path": "packages/haive-tools/src",
        "autoapi_dirs": ["../../packages/haive-tools/src"],
        "description": "Tool integrations",
        "priority": 2,
        "dependencies": ["core"],
    },
    "games": {
        "path": "packages/haive-games/src",
        "autoapi_dirs": ["../../packages/haive-games/src"],
        "description": "Game environments",
        "priority": 3,
        "dependencies": ["core", "agents"],
    },
    "mcp": {
        "path": "packages/haive-mcp/src",
        "autoapi_dirs": ["../../packages/haive-mcp/src"],
        "description": "MCP integration",
        "priority": 2,
        "dependencies": ["core"],
    },
    "dataflow": {
        "path": "packages/haive-dataflow/src",
        "autoapi_dirs": ["../../packages/haive-dataflow/src"],
        "description": "Data processing",
        "priority": 3,
        "dependencies": ["core", "agents"],
    },
    "prebuilt": {
        "path": "packages/haive-prebuilt/src",
        "autoapi_dirs": ["../../packages/haive-prebuilt/src"],
        "description": "Pre-configured components",
        "priority": 4,
        "dependencies": ["core", "agents", "tools"],
    },
}

# Configuration presets for different testing scenarios
CONFIG_PRESETS = {
    "minimal": {
        "description": "Minimal config for structure testing",
        "extensions": ["sphinx.ext.autodoc"],
        "theme": "alabaster",
        "autoapi": False,
        "intersphinx": False,
        "build_time_limit": 30,  # seconds
    },
    "api_only": {
        "description": "API documentation only",
        "extensions": ["sphinx.ext.autodoc", "autoapi.extension"],
        "theme": "furo",
        "autoapi": True,
        "intersphinx": False,
        "build_time_limit": 120,
    },
    "standard": {
        "description": "Standard documentation build",
        "extensions": ["sphinx.ext.autodoc", "autoapi.extension"],
        "theme": "furo",
        "autoapi": True,
        "intersphinx": True,
        "build_time_limit": 300,
    },
    "full": {
        "description": "Full-featured build",
        "config_function": "create_full_config",
        "build_time_limit": 600,
    },
}


def create_package_config(
    package_name: str, preset: str = "api_only", include_deps: bool = True
) -> str:
    """Create a temporary Sphinx config for testing a specific package."""

    if package_name not in PACKAGES:
        raise ValueError(f"Unknown package: {package_name}")

    pkg_info = PACKAGES[package_name]
    preset_info = CONFIG_PRESETS[preset]

    # Build autoapi_dirs including dependencies if requested
    autoapi_dirs = pkg_info["autoapi_dirs"].copy()
    if include_deps:
        for dep in pkg_info["dependencies"]:
            if dep in PACKAGES:
                autoapi_dirs.extend(PACKAGES[dep]["autoapi_dirs"])

    # Generate config content
    config_content = f'''"""
Temporary Sphinx configuration for testing {package_name} package.
Generated automatically - do not edit manually.
"""

import sys
import os
from pathlib import Path

# Basic project info
project = "Haive - {package_name.title()} Package Test"
author = "Haive Team"
copyright = "2025, Haive Team"

# Extensions based on preset: {preset}
extensions = {preset_info.get("extensions", [])}

# Theme
html_theme = "{preset_info.get("theme", "furo")}"

# AutoAPI configuration
autoapi_type = "python"
autoapi_dirs = {autoapi_dirs}
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = {preset_info.get("autoapi", True)}
autoapi_member_order = "bysource"
autoapi_options = [
    "members",
    "undoc-members", 
    "show-inheritance",
    "show-module-summary",
]

# Skip test files
autoapi_ignore = [
    "**/test*.py",
    "**/tests/**/*.py",
    "**/*_test.py",
    "**/examples/**/app.py",
]

# Path setup
sys.path.insert(0, os.path.abspath("{pkg_info["path"]}"))

# Minimal HTML options
html_title = f"{{project}} Documentation"
html_short_title = "{package_name.title()}"

# Suppress warnings for cleaner output
suppress_warnings = ["ref.python", "autosummary", "autoapi"]
'''

    if preset_info.get("intersphinx", False):
        config_content += """
# Intersphinx
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
"""

    return config_content


@nox.session(python=PYTHON_VERSIONS, name="docs-test-package")
@nox.parametrize("package", list(PACKAGES.keys()))
@nox.parametrize("preset", ["minimal", "api_only"])
def docs_test_package(session, package: str, preset: str):
    """Test documentation for a single package with different configurations."""

    pkg_info = PACKAGES[package]
    preset_info = CONFIG_PRESETS[preset]

    session.log(f"🧪 Testing {package} with {preset} preset")
    session.log(f"📝 {pkg_info['description']}")

    # Install minimal dependencies for the preset
    if preset == "minimal":
        session.install("sphinx")
    elif preset == "api_only":
        session.install("sphinx", "sphinx-autoapi", "furo")
    else:
        session.install("sphinx", "sphinx-autoapi", "furo", "myst-parser")

    # Create temporary config and directories
    config_content = create_package_config(package, preset, include_deps=False)

    # Build output directory
    build_dir = DOCS_DIR / "build" / f"test_{package}_{preset}"

    # Create isolated config directory
    temp_conf_dir = build_dir.parent / f"conf_{package}_{preset}"
    temp_conf_dir.mkdir(exist_ok=True)
    temp_conf_file = temp_conf_dir / "conf.py"
    temp_conf_file.write_text(config_content)

    # Create minimal source directory with just index.rst
    temp_source_dir = build_dir.parent / f"source_{package}_{preset}"
    temp_source_dir.mkdir(exist_ok=True)

    index_content = f"""
{package.title()} Package Test
{"=" * (len(package) + 13)}

Testing {pkg_info["description"]} documentation build.

This is a test build for the {package} package using {preset} preset.
"""

    (temp_source_dir / "index.rst").write_text(index_content)

    try:
        start_time = time.time()

        # Run the build with isolated config and source
        session.run(
            "python",
            "-m",
            "sphinx",
            "-b",
            "html",
            "-c",
            str(temp_conf_dir),
            str(temp_source_dir),
            str(build_dir),
            "-q",
            "-W",  # Quiet mode, warnings as errors
            external=True,
        )

        build_time = time.time() - start_time

        # Check build time against limit
        if build_time > preset_info["build_time_limit"]:
            session.log(
                f"⚠️  Build time {build_time:.1f}s exceeded limit {preset_info['build_time_limit']}s"
            )

        # Analyze results
        results = analyze_build_results(build_dir, package, preset, build_time)
        session.log(f"✅ {package} ({preset}): {results['summary']}")

        # Save results for comparison
        save_test_results(package, preset, results)

    except Exception as e:
        session.log(f"❌ {package} ({preset}) failed: {e}")
        raise
    finally:
        # Cleanup temp directories
        import shutil

        for temp_dir in [temp_conf_dir, temp_source_dir]:
            if temp_dir.exists():
                shutil.rmtree(temp_dir)


@nox.session(python=PYTHON_VERSIONS, name="docs-test-incremental")
def docs_test_incremental(session):
    """Test incremental build performance and reliability."""

    session.install("sphinx", "sphinx-autoapi", "furo")

    session.log("🔄 Testing incremental build workflow...")

    build_dir = DOCS_DIR / "build" / "incremental_test"

    # Clean build first
    if build_dir.exists():
        shutil.rmtree(build_dir)

    times = {}

    # 1. Full clean build
    start = time.time()
    session.run(
        "python",
        "-m",
        "sphinx",
        "-b",
        "html",
        "-E",  # Clean build
        str(SOURCE_DIR),
        str(build_dir),
        external=True,
    )
    times["clean_build"] = time.time() - start
    session.log(f"🏗️  Clean build: {times['clean_build']:.1f}s")

    # 2. No-change rebuild
    start = time.time()
    session.run(
        "python",
        "-m",
        "sphinx",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(build_dir),
        external=True,
    )
    times["no_change"] = time.time() - start
    session.log(f"⚡ No-change rebuild: {times['no_change']:.1f}s")

    # 3. Touch index.rst and rebuild
    (SOURCE_DIR / "index.rst").touch()
    start = time.time()
    session.run(
        "python",
        "-m",
        "sphinx",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(build_dir),
        external=True,
    )
    times["index_change"] = time.time() - start
    session.log(f"📝 Index change rebuild: {times['index_change']:.1f}s")

    # 4. Touch API file and rebuild (if exists)
    api_files = list((SOURCE_DIR / "api").rglob("*.rst"))
    if api_files:
        api_files[0].touch()
        start = time.time()
        session.run(
            "python",
            "-m",
            "sphinx",
            "-b",
            "html",
            str(SOURCE_DIR),
            str(build_dir),
            external=True,
        )
        times["api_change"] = time.time() - start
        session.log(f"🔧 API change rebuild: {times['api_change']:.1f}s")

    # Performance analysis
    performance_report = {
        "timestamp": time.time(),
        "times": times,
        "speedup_no_change": (
            times["clean_build"] / times["no_change"]
            if times["no_change"] > 0
            else float("inf")
        ),
        "speedup_index": (
            times["clean_build"] / times["index_change"]
            if times["index_change"] > 0
            else float("inf")
        ),
    }

    # Save performance data
    perf_file = DOCS_DIR / "performance_incremental.json"
    with open(perf_file, "w") as f:
        json.dump(performance_report, f, indent=2)

    session.log(f"📊 Performance report saved to {perf_file}")

    # Performance assertions
    if times["no_change"] > 30:
        session.error("❌ No-change rebuild too slow (>30s)")
    if times["index_change"] > 60:
        session.error("❌ Index change rebuild too slow (>60s)")


@nox.session(python=PYTHON_VERSIONS, name="docs-test-config")
@nox.parametrize("config_type", ["minimal", "standard", "modular"])
def docs_test_config(session, config_type: str):
    """Test different configuration approaches."""

    session.log(f"🔧 Testing {config_type} configuration approach")

    if config_type == "minimal":
        session.install("sphinx", "furo")
        config_module = "create_minimal_config"
    elif config_type == "standard":
        session.install("sphinx", "sphinx-autoapi", "furo", "myst-parser")
        config_module = "create_standard_config"
    elif config_type == "modular":
        session.install("sphinx", "sphinx-autoapi", "furo", "myst-parser")
        config_module = "create_full_config"

    # Create test config using conf_modules
    test_config_content = f"""
from conf_modules import {config_module}

# Use modular configuration
config_dict = {config_module}()
locals().update(config_dict)

# Test-specific overrides
html_title = "Configuration Test - {config_type.title()}"
"""

    temp_conf = SOURCE_DIR / f"conf_{config_type}_test.py"
    temp_conf.write_text(test_config_content)

    build_dir = DOCS_DIR / "build" / f"config_test_{config_type}"

    try:
        start_time = time.time()

        session.run(
            "python",
            "-m",
            "sphinx",
            "-b",
            "html",
            "-c",
            str(SOURCE_DIR),
            "-D",
            f"config={temp_conf.stem}",
            str(SOURCE_DIR),
            str(build_dir),
            "-q",
            external=True,
        )

        build_time = time.time() - start_time

        # Check what was generated
        html_files = list(build_dir.rglob("*.html"))
        css_files = list(build_dir.rglob("*.css"))
        js_files = list(build_dir.rglob("*.js"))

        session.log(f"✅ {config_type} config: {build_time:.1f}s")
        session.log(
            f"   Generated: {len(html_files)} HTML, {len(css_files)} CSS, {len(js_files)} JS files"
        )

        # Test-specific validations
        if config_type == "minimal":
            # Should have basic files only
            assert (
                len(html_files) < 100
            ), f"Too many files for minimal config: {len(html_files)}"
        elif config_type == "modular":
            # Should have API documentation
            api_files = (
                list((build_dir / "api").rglob("*.html"))
                if (build_dir / "api").exists()
                else []
            )
            assert (
                len(api_files) > 10
            ), f"Expected API files in modular config, got {len(api_files)}"

    finally:
        if temp_conf.exists():
            temp_conf.unlink()


@nox.session(python=PYTHON_VERSIONS, name="docs-compare-configs")
def docs_compare_configs(session):
    """Compare different configuration approaches side by side."""

    import shutil

    session.install("sphinx", "sphinx-autoapi", "furo", "myst-parser")

    configs_to_compare = ["minimal", "api_only", "standard"]
    results = {}

    for config in configs_to_compare:
        session.log(f"\n🔍 Building with {config} configuration...")

        build_dir = DOCS_DIR / "build" / f"compare_{config}"
        if build_dir.exists():
            shutil.rmtree(build_dir)

        # Use the config preset
        preset_info = CONFIG_PRESETS[config]

        # Create isolated config and source
        config_lines = [
            f'project = "Config Comparison - {config.title()}"',
            f'extensions = {preset_info["extensions"]}',
            f'html_theme = "{preset_info["theme"]}"',
            f'autoapi_generate_api_docs = {preset_info.get("autoapi", False)}',
            'master_doc = "index"',
        ]

        # Add autoapi_dirs if autoapi is enabled
        if preset_info.get("autoapi", False):
            # Use absolute path for autoapi_dirs
            import os

            core_src_path = os.path.abspath("packages/haive-core/src")
            config_lines.append(f'autoapi_dirs = ["{core_src_path}"]')
            config_lines.append('autoapi_type = "python"')
            config_lines.append('autoapi_root = "api"')

        config_content = "\n".join(config_lines)

        # Create isolated config directory
        temp_conf_dir = build_dir.parent / f"conf_compare_{config}"
        temp_conf_dir.mkdir(exist_ok=True)
        temp_conf_file = temp_conf_dir / "conf.py"
        temp_conf_file.write_text(config_content)

        # Create minimal source directory
        temp_source_dir = build_dir.parent / f"source_compare_{config}"
        temp_source_dir.mkdir(exist_ok=True)

        index_content = f"""
Configuration Comparison: {config.title()}
{"=" * (25 + len(config))}

This is a test build using the {config} configuration preset.

Features
--------

- Extensions: {preset_info["extensions"]}
- Theme: {preset_info["theme"]}
- AutoAPI: {preset_info.get("autoapi", False)}

Configuration comparison test completed.
"""

        (temp_source_dir / "index.rst").write_text(index_content)

        try:
            start_time = time.time()

            session.run(
                "python",
                "-m",
                "sphinx",
                "-b",
                "html",
                "-c",
                str(temp_conf_dir),
                str(temp_source_dir),
                str(build_dir),
                "-q",
                external=True,
            )

            build_time = time.time() - start_time

            # Collect metrics
            html_files = list(build_dir.rglob("*.html"))
            total_size = sum(
                f.stat().st_size for f in build_dir.rglob("*") if f.is_file()
            )

            results[config] = {
                "build_time": build_time,
                "html_files": len(html_files),
                "total_size_mb": total_size / 1024 / 1024,
                "has_api": (build_dir / "api").exists(),
            }

            session.log(
                f"   ⏱️  {build_time:.1f}s, {len(html_files)} files, {total_size/1024/1024:.1f}MB"
            )

        finally:
            # Cleanup temp directories
            for temp_dir in [temp_conf_dir, temp_source_dir]:
                if temp_dir.exists():
                    shutil.rmtree(temp_dir)

    # Generate comparison report
    session.log("\n📊 Configuration Comparison:")
    session.log("─" * 60)
    session.log(
        f"{'Config':<12} {'Time (s)':<8} {'Files':<6} {'Size (MB)':<10} {'API':<4}"
    )
    session.log("─" * 60)

    for config, metrics in results.items():
        api_marker = "✓" if metrics["has_api"] else "✗"
        session.log(
            f"{config:<12} {metrics['build_time']:<8.1f} {metrics['html_files']:<6} "
            f"{metrics['total_size_mb']:<10.1f} {api_marker:<4}"
        )

    # Save detailed comparison
    comparison_file = DOCS_DIR / "config_comparison.json"
    with open(comparison_file, "w") as f:
        json.dump(results, f, indent=2)

    session.log(f"\n📁 Detailed comparison saved to {comparison_file}")


def analyze_build_results(
    build_dir: Path, package: str, preset: str, build_time: float
) -> Dict:
    """Analyze build results and return metrics."""

    if not build_dir.exists():
        return {"success": False, "error": "Build directory not found"}

    # Count generated files
    html_files = list(build_dir.rglob("*.html"))
    css_files = list(build_dir.rglob("*.css"))
    js_files = list(build_dir.rglob("*.js"))

    # Check for API documentation
    api_dir = build_dir / "api"
    has_api = api_dir.exists()
    api_files = list(api_dir.rglob("*.html")) if has_api else []

    # Calculate sizes
    total_size = sum(f.stat().st_size for f in build_dir.rglob("*") if f.is_file())

    return {
        "success": True,
        "package": package,
        "preset": preset,
        "build_time": build_time,
        "file_counts": {
            "html": len(html_files),
            "css": len(css_files),
            "js": len(js_files),
            "api": len(api_files),
        },
        "has_api": has_api,
        "total_size_mb": total_size / 1024 / 1024,
        "summary": f"{build_time:.1f}s, {len(html_files)} files, {total_size/1024/1024:.1f}MB",
    }


def save_test_results(package: str, preset: str, results: Dict):
    """Save test results for trend analysis."""

    results_dir = DOCS_DIR / "test_results"
    results_dir.mkdir(exist_ok=True)

    results_file = results_dir / f"{package}_{preset}_results.json"

    # Load existing results
    if results_file.exists():
        with open(results_file) as f:
            all_results = json.load(f)
    else:
        all_results = []

    # Add timestamp and save
    results["timestamp"] = time.time()
    all_results.append(results)

    # Keep only last 10 results
    all_results = all_results[-10:]

    with open(results_file, "w") as f:
        json.dump(all_results, f, indent=2)


@nox.session(python=PYTHON_VERSIONS, name="docs-quick-test")
def docs_quick_test(session):
    """Quick smoke test for documentation changes."""

    session.install("sphinx", "furo")

    session.log("⚡ Running quick documentation test...")

    build_dir = DOCS_DIR / "build" / "quick_test"

    # Create minimal source directory with just index.rst
    temp_source_dir = build_dir.parent / "quick_test_source"
    temp_source_dir.mkdir(exist_ok=True)

    # Simple index.rst
    index_content = """
Haive Documentation Quick Test
==============================

This is a quick test of the documentation build system.

Features
--------

- Fast build testing
- Minimal configuration
- No API generation

Test passed!
"""

    (temp_source_dir / "index.rst").write_text(index_content)

    # Create minimal config
    minimal_config = """
project = "Haive Documentation Test"
extensions = []
html_theme = "furo"
html_title = "Quick Test"
master_doc = "index"
"""

    temp_conf_dir = build_dir.parent / "quick_test_conf"
    temp_conf_dir.mkdir(exist_ok=True)
    temp_conf_file = temp_conf_dir / "conf.py"
    temp_conf_file.write_text(minimal_config)

    try:
        start_time = time.time()
        session.run(
            "python",
            "-m",
            "sphinx",
            "-b",
            "html",
            "-c",
            str(temp_conf_dir),
            str(temp_source_dir),
            str(build_dir),
            "-q",
            external=True,
        )
        build_time = time.time() - start_time

        # Basic validation
        index_file = build_dir / "index.html"
        if not index_file.exists():
            session.error("❌ index.html not generated")

        session.log(f"✅ Quick test passed in {build_time:.1f}s")

    finally:
        # Cleanup temp directories
        cleanup_temp_dirs(temp_conf_dir, temp_source_dir)


# =============================================================================
# MODULAR CONFIGURATION SESSIONS
# =============================================================================


@nox.session(python=PYTHON_VERSIONS, name="docs-test-modular")
@nox.parametrize("package", list(PACKAGES.keys()))
def docs_test_modular_config(session, package):
    """Test modular configuration with individual packages."""

    session.install(*DEPENDENCIES)

    session.log(f"🧩 Testing modular configuration with {package}")

    build_dir = DOCS_DIR / "build" / f"modular_test_{package}"

    # Create modular configuration for specific package
    modular_config = f'''
"""Modular configuration test for {package}."""

import sys
from pathlib import Path

# Add conf_modules to path
conf_modules_dir = Path(__file__).parent / "conf_modules"
sys.path.insert(0, str(conf_modules_dir))

# Load modular system
from extensions import get_all_extensions
from extension_configs import get_all_extension_configs
from memory import get_memory_safe_sphinx_config

project = "Haive {package.title()} - Modular Test"
extensions = get_all_extensions()

print(f"🔧 Loaded {{len(extensions)}} extensions for {package}")

# Apply memory-safe config
memory_config = get_memory_safe_sphinx_config(extensions)
extensions = memory_config["extensions"]
globals().update(memory_config)

# Apply extension configs
extension_configs = get_all_extension_configs(extensions)
globals().update(extension_configs)

# AutoAPI for specific package only
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-{package}/src"]
autoapi_root = "api"
autoapi_add_toctree_entry = True

# Basic settings
html_theme = "furo"
suppress_warnings = ["ref.python", "autosummary", "autoapi"]

# Mock problematic imports
autodoc_mock_imports = [
    "google_search_results", "serpapi", "agents", "complex_rag"
]

print(f"✅ Modular config ready for {package}")
'''

    # Use isolated directories
    temp_conf_dir, temp_source_dir = create_isolated_dirs(build_dir, package, "modular")

    try:
        # Write modular configuration
        conf_file = temp_conf_dir / "conf.py"
        conf_file.write_text(modular_config)

        # Copy conf_modules
        source_conf_modules = DOCS_DIR / "source" / "conf_modules"
        if source_conf_modules.exists():
            import shutil

            shutil.copytree(source_conf_modules, temp_conf_dir / "conf_modules")

        # Create simple test content
        index_content = f"""
{package.title()} Modular Configuration Test
{'=' * (len(package) + 30)}

Testing the modular configuration system with {package} package.

.. toctree::
   :maxdepth: 2
   
   api/index

Extensions Loaded
-----------------

This test uses the full modular configuration system with 70+ extensions.

Package Focus
-------------

- **Package**: haive-{package}
- **Configuration**: Full modular system
- **Extensions**: Memory-optimized selection
"""
        (temp_source_dir / "index.rst").write_text(index_content)

        # Test build
        start_time = time.time()

        session.run(
            "sphinx-build",
            "-b",
            "html",
            "-c",
            str(temp_conf_dir),
            str(temp_source_dir),
            str(build_dir),
            "-q",
        )

        build_time = time.time() - start_time

        # Check results
        html_files = list(build_dir.glob("**/*.html"))
        session.log(
            f"✅ Modular config test passed: {len(html_files)} files in {build_time:.1f}s"
        )

    finally:
        cleanup_temp_dirs(temp_conf_dir, temp_source_dir)


@nox.session(python=PYTHON_VERSIONS, name="docs-build-module")
@nox.parametrize("package", list(PACKAGES.keys()))
@nox.parametrize("module", ["engine", "schema", "memory", "init_only"])
def docs_build_specific_module(session, package, module):
    """Build documentation for specific modules within a package."""

    session.install(*DEPENDENCIES)

    session.log(f"🎯 Building {package}/{module} with modular config")

    build_dir = DOCS_DIR / "build" / f"{package}_{module}"

    # Module-specific AutoAPI patterns
    module_patterns = {
        "engine": f"haive.{package}.engine.*",
        "schema": f"haive.{package}.schema.*",
        "memory": f"haive.{package}.memory.*",
        "init_only": f"haive.{package}.__init__",
    }

    # Create focused configuration
    focused_config = f'''
"""Focused configuration for {package}/{module}."""

import sys
from pathlib import Path

# Load modular system
conf_modules_dir = Path(__file__).parent / "conf_modules"  
sys.path.insert(0, str(conf_modules_dir))

from extensions import get_all_extensions
from extension_configs import get_all_extension_configs

project = "Haive {package.title()} - {module.title()}"
extensions = get_all_extensions()

# Apply configs
extension_configs = get_all_extension_configs(extensions)
globals().update(extension_configs)

# AutoAPI focused on specific module
autoapi_type = "python"
autoapi_dirs = ["../../packages/haive-{package}/src"]

# Module-specific ignore patterns
autoapi_ignore = [
    "**/examples/**/*.py",
    "**/test*.py",
    "**/tests/**/*.py",
]

# Focus patterns for {module}
{f'# Focus on {module} module only' if module != 'init_only' else '# Focus on __init__.py files only'}

autoapi_root = "api"
html_theme = "furo"
suppress_warnings = ["ref.python", "autosummary", "autoapi"]

print(f"🎯 Focused on {package}/{module}")
'''

    temp_conf_dir, temp_source_dir = create_isolated_dirs(build_dir, package, module)

    try:
        # Write configuration
        conf_file = temp_conf_dir / "conf.py"
        conf_file.write_text(focused_config)

        # Copy conf_modules
        source_conf_modules = DOCS_DIR / "source" / "conf_modules"
        if source_conf_modules.exists():
            import shutil

            shutil.copytree(source_conf_modules, temp_conf_dir / "conf_modules")

        # Create focused content
        index_content = f"""
{package.title()} - {module.title()} Documentation
{'=' * (len(package) + len(module) + 20)}

Focused documentation for the {module} module in {package}.

.. toctree::
   :maxdepth: 3
   
   api/index

Module Focus: {module}
{'-' * (14 + len(module))}

This build focuses specifically on:

- **Package**: haive-{package}
- **Module**: {module}  
- **Pattern**: {module_patterns.get(module, 'all')}
"""
        (temp_source_dir / "index.rst").write_text(index_content)

        # Build with focus
        start_time = time.time()

        session.run(
            "sphinx-build",
            "-b",
            "html",
            "-c",
            str(temp_conf_dir),
            str(temp_source_dir),
            str(build_dir),
            "-v",  # Verbose for module builds
        )

        build_time = time.time() - start_time
        html_files = list(build_dir.glob("**/*.html"))

        session.log(
            f"✅ Module build completed: {len(html_files)} files in {build_time:.1f}s"
        )

        # Show specific module results
        module_files = list(build_dir.glob(f"**/haive/{package}/{module}/**/*.html"))
        if module_files:
            session.log(f"📁 {module} module files: {len(module_files)}")

    finally:
        cleanup_temp_dirs(temp_conf_dir, temp_source_dir)


@nox.session(python=PYTHON_VERSIONS, name="docs-explore-config")
def docs_explore_modular_config(session):
    """Explore and analyze the modular configuration system."""

    session.install(*DEPENDENCIES)

    session.log("🔍 Exploring modular configuration system...")

    # Test configuration loading
    session.run(
        "python",
        "-c",
        f"""
import sys
sys.path.insert(0, '{DOCS_DIR / "source" / "conf_modules"}')

from extensions import get_all_extensions
from extension_configs import get_all_extension_configs
from memory import get_memory_safe_sphinx_config

print("📊 MODULAR CONFIGURATION ANALYSIS")
print("=" * 40)

extensions = get_all_extensions()
print(f"Total extensions: {{len(extensions)}}")

# Test memory config
memory_config = get_memory_safe_sphinx_config(extensions[:10])  
print(f"Memory config keys: {{list(memory_config.keys())}}")

# Test extension configs
ext_configs = get_all_extension_configs(extensions[:5])
print(f"Extension configs: {{len(ext_configs)}} settings")

print("✅ Modular configuration system working!")
""",
    )
    import subprocess

    try:
        changed_files = (
            subprocess.check_output(
                ["git", "diff", "--name-only", "HEAD~1"], universal_newlines=True
            )
            .strip()
            .split("\n")
        )

        # Filter for documentation-related changes
        doc_changes = [
            f for f in changed_files if "docs/" in f or ".rst" in f or ".md" in f
        ]

        if doc_changes:
            session.log(f"📝 Found {len(doc_changes)} documentation changes")
            for change in doc_changes[:5]:  # Show first 5
                session.log(f"   - {change}")
        else:
            session.log("📝 No recent documentation changes detected")

    except subprocess.CalledProcessError:
        session.log("📝 Could not check for recent changes")

    # Run quick test first
    docs_quick_test(session)

    session.log("✅ Development build ready for testing")


if __name__ == "__main__":
    print("Granular Documentation Testing Sessions:")
    print("  nox -s docs-test-package         # Test individual packages")
    print("  nox -s docs-test-incremental     # Test build performance")
    print("  nox -s docs-test-config          # Test configurations")
    print("  nox -s docs-compare-configs      # Compare config approaches")
    print("  nox -s docs-quick-test           # Quick smoke test")
    print("  nox -s docs-dev                  # Development workflow")
