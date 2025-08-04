"""
Nox configuration for documentation testing and building.

This provides granular control over documentation builds for different
testing scenarios and package-level validation.
"""

from pathlib import Path

import nox

# Python versions to test with
PYTHON_VERSIONS = ["3.12"]

# Package configurations for granular testing
PACKAGES = {
    "core": {
        "path": "packages/haive-core/src",
        "autoapi_dirs": ["../../packages/haive-core/src"],
        "description": "Core framework components",
    },
    "agents": {
        "path": "packages/haive-agents/src",
        "autoapi_dirs": ["../../packages/haive-agents/src"],
        "description": "Agent implementations",
    },
    "tools": {
        "path": "packages/haive-tools/src",
        "autoapi_dirs": ["../../packages/haive-tools/src"],
        "description": "Tool integrations",
    },
    "games": {
        "path": "packages/haive-games/src",
        "autoapi_dirs": ["../../packages/haive-games/src"],
        "description": "Game environments",
    },
    "mcp": {
        "path": "packages/haive-mcp/src",
        "autoapi_dirs": ["../../packages/haive-mcp/src"],
        "description": "MCP integration",
    },
    "dataflow": {
        "path": "packages/haive-dataflow/src",
        "autoapi_dirs": ["../../packages/haive-dataflow/src"],
        "description": "Data processing",
    },
    "prebuilt": {
        "path": "packages/haive-prebuilt/src",
        "autoapi_dirs": ["../../packages/haive-prebuilt/src"],
        "description": "Pre-configured components",
    },
}

# Build configurations for different testing scenarios
BUILD_CONFIGS = {
    "minimal": {
        "extensions": ["sphinx.ext.autodoc", "furo"],
        "autoapi": False,
        "description": "Minimal build for basic testing",
    },
    "api_only": {
        "extensions": ["sphinx.ext.autodoc", "autoapi.extension", "furo"],
        "autoapi": True,
        "description": "API documentation only",
    },
    "full": {
        "extensions": "all",
        "autoapi": True,
        "description": "Full build with all features",
    },
}


@nox.session(python=PYTHON_VERSIONS)
def docs_test_structure(session):
    """Test documentation structure without building."""
    session.install("pathlib")
    session.run("python", "docs/test_doc_structure.py", external=True)


@nox.session(python=PYTHON_VERSIONS)
def docs_test_css(session):
    """Test CSS and design elements."""
    session.install("pathlib")
    session.run("python", "docs/test_doc_css.py", external=True)


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("package", list(PACKAGES.keys()))
def docs_test_package(session, package):
    """Test documentation for a single package."""
    pkg_config = PACKAGES[package]

    print(f"🧪 Testing {package}: {pkg_config['description']}")

    # Install minimal dependencies
    session.install("sphinx", "furo", "sphinx-autoapi")

    # Create temporary config for single package
    config_content = f"""
# Temporary config for testing {package} package
import sys
import os

project = "Haive - {package.title()} Package"
extensions = ["sphinx.ext.autodoc", "autoapi.extension", "furo"]
html_theme = "furo"

# AutoAPI config for single package
autoapi_type = "python"
autoapi_dirs = {pkg_config['autoapi_dirs']}
autoapi_root = "api"
autoapi_add_toctree_entry = True
autoapi_generate_api_docs = True

# Add package to path
sys.path.insert(0, os.path.abspath("{pkg_config['path']}"))
"""

    # Write temporary config
    temp_conf = Path("docs/source/conf_temp.py")
    temp_conf.write_text(config_content)

    try:
        # Test build for this package only
        session.run(
            "sphinx-build",
            "-b",
            "html",
            "-c",
            "docs/source",  # Use source dir but with temp config
            "-D",
            f"config_file=conf_temp.py",
            "docs/source",
            f"docs/build/test_{package}",
            "-q",
            "-W",  # Quiet mode, warnings as errors
            external=True,
        )
        print(f"✅ {package} package documentation builds successfully")

        # Check generated files
        api_dir = Path(f"docs/build/test_{package}/api")
        if api_dir.exists():
            rst_files = list(api_dir.rglob("*.rst"))
            html_files = list(Path(f"docs/build/test_{package}").rglob("*.html"))
            print(
                f"📊 Generated {len(rst_files)} RST files, {len(html_files)} HTML files"
            )

    finally:
        # Cleanup
        if temp_conf.exists():
            temp_conf.unlink()


@nox.session(python=PYTHON_VERSIONS)
@nox.parametrize("config", list(BUILD_CONFIGS.keys()))
def docs_test_config(session, config):
    """Test different build configurations."""
    build_config = BUILD_CONFIGS[config]

    print(f"🔧 Testing {config} configuration: {build_config['description']}")

    # Install dependencies based on config
    if config == "minimal":
        session.install("sphinx", "furo")
    elif config == "api_only":
        session.install("sphinx", "furo", "sphinx-autoapi")
    else:  # full
        session.install("-e", ".", "--extras", "docs")

    # Create config override
    config_overrides = []

    if not build_config["autoapi"]:
        config_overrides.extend(["-D", "autoapi_generate_api_docs=0"])

    if build_config["extensions"] != "all":
        ext_list = str(build_config["extensions"]).replace("'", '"')
        config_overrides.extend(["-D", f"extensions={ext_list}"])

    # Run build
    cmd = [
        "sphinx-build",
        "-b",
        "html",
        "docs/source",
        f"docs/build/test_{config}",
        "-q",
    ] + config_overrides

    session.run(*cmd, external=True)
    print(f"✅ {config} configuration builds successfully")


@nox.session(python=PYTHON_VERSIONS)
def docs_incremental_test(session):
    """Test incremental builds for development workflow."""
    session.install("-e", ".", "--extras", "docs")

    print("🔄 Testing incremental build workflow...")

    # First: Clean build
    import time

    start = time.time()
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "docs/source",
        "docs/build/incremental",
        "-E",  # Clean build
        external=True,
    )
    clean_time = time.time() - start
    print(f"🏗️  Clean build: {clean_time:.2f}s")

    # Second: Touch a file and rebuild
    test_file = Path("docs/source/index.rst")
    test_file.touch()

    start = time.time()
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "docs/source",
        "docs/build/incremental",
        external=True,
    )
    incremental_time = time.time() - start
    print(f"⚡ Incremental build: {incremental_time:.2f}s")

    # Performance check
    speedup = clean_time / incremental_time if incremental_time > 0 else float("inf")
    print(f"📈 Speedup: {speedup:.1f}x faster")

    if incremental_time > 60:
        session.error("❌ Incremental build too slow (>60s)")


@nox.session(python=PYTHON_VERSIONS)
def docs_validate_links(session):
    """Validate documentation links and cross-references."""
    session.install("-e", ".", "--extras", "docs")

    print("🔗 Validating documentation links...")

    # Build with link checking
    session.run(
        "sphinx-build",
        "-b",
        "linkcheck",
        "docs/source",
        "docs/build/linkcheck",
        external=True,
    )

    # Check for broken links in output
    linkcheck_output = Path("docs/build/linkcheck/output.txt")
    if linkcheck_output.exists():
        content = linkcheck_output.read_text()
        broken_links = [
            line for line in content.split("\n") if "broken" in line.lower()
        ]

        if broken_links:
            print(f"❌ Found {len(broken_links)} broken links:")
            for link in broken_links[:5]:  # Show first 5
                print(f"  - {link}")
        else:
            print("✅ All links valid")


@nox.session(python=PYTHON_VERSIONS)
def docs_performance_profile(session):
    """Profile documentation build performance."""
    session.install("-e", ".", "--extras", "docs", "cProfile")

    print("📊 Profiling documentation build performance...")

    # Profile the build
    session.run(
        "python",
        "-m",
        "cProfile",
        "-o",
        "docs_build.prof",
        "-m",
        "sphinx",
        "-b",
        "html",
        "docs/source",
        "docs/build/profile",
        external=True,
    )

    # Analyze profile
    session.run(
        "python",
        "-c",
        """
import pstats
p = pstats.Stats('docs_build.prof')
print('🔥 Top 10 slowest functions:')
p.sort_stats('cumulative').print_stats(10)
print('\\n📦 Top 10 by total time:')
p.sort_stats('tottime').print_stats(10)
        """,
        external=True,
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve documentation locally for testing."""
    session.install("-e", ".", "--extras", "docs")

    # Ensure docs are built
    session.run(
        "sphinx-build", "-b", "html", "docs/source", "docs/build/html", external=True
    )

    print("🌐 Starting documentation server at http://localhost:8000")
    print("   Use Ctrl+C to stop")

    # Serve the docs
    import os

    os.chdir("docs/build/html")
    session.run("python", "-m", "http.server", "8000", external=True)


@nox.session(python=PYTHON_VERSIONS)
def docs_quick(session):
    """Quick documentation build for development."""
    session.install("sphinx", "furo")

    print("⚡ Quick documentation build (no API generation)...")

    session.run(
        "sphinx-build",
        "-b",
        "html",
        "docs/source",
        "docs/build/quick",
        "-D",
        "autoapi_generate_api_docs=0",
        "-q",
        external=True,
    )

    print("✅ Quick build complete at docs/build/quick/")


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean all documentation build artifacts."""
    import shutil

    build_dir = Path("docs/build")
    if build_dir.exists():
        shutil.rmtree(build_dir)
        print("🧹 Cleaned build directory")

    api_dir = Path("docs/source/api")
    if api_dir.exists() and api_dir.is_dir():
        # Only remove if it looks like generated content
        if len(list(api_dir.rglob("*.rst"))) > 100:  # Lots of RST files = generated
            response = input("Remove generated API files? (y/N): ")
            if response.lower() == "y":
                shutil.rmtree(api_dir)
                print("🧹 Cleaned API directory")

    print("✅ Cleanup complete")


# Default session for quick testing
@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Default documentation build."""
    session.install("-e", ".", "--extras", "docs")

    session.run(
        "sphinx-build", "-b", "html", "docs/source", "docs/build/html", external=True
    )

    print("✅ Documentation built at docs/build/html/")
    print("🌐 Run 'nox -s docs_serve' to serve locally")


if __name__ == "__main__":
    print("Available documentation sessions:")
    print("  nox -s docs              # Full build")
    print("  nox -s docs_quick         # Quick build (no API)")
    print("  nox -s docs_serve         # Serve locally")
    print("  nox -s docs_test_package  # Test single package")
    print("  nox -s docs_clean         # Clean builds")
    print("  nox -s docs_incremental_test  # Test build speed")
    print("  nox -s docs_validate_links    # Check links")
    print("  nox -s docs_performance_profile  # Profile performance")
