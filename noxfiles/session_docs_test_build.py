"""Test documentation builds with minimal setup for quick iteration."""

from __future__ import annotations

import os
from pathlib import Path

import nox

# Python versions to test
PYTHON_VERSIONS = ["3.12"]

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs" / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / "builds"  # Use consistent builds directory


@nox.session(name="docs-test-build")
def docs_test_build(session):
    """Test documentation build with minimal setup (core package only).

    This is the fastest way to test if documentation builds successfully.
    Uses only haive-core package to minimize build time.

    Usage:
        nox -s docs-test-build
    """
    # Environment variables for minimal build
    env = {
        "SPHINX_PACKAGES": "core",  # Only build core package
        "SPHINX_PROFILE": "minimal",
        "SPHINX_INCLUDE_MCP_DOCS": "false",  # Disable MCP docs
        "SPHINX_INCLUDE_READMES": "false",  # Disable README integration for speed
        "AUTOAPI_GENERATE_API_DOCS": "true",
        "AUTOAPI_KEEP_FILES": "false",
    }

    output_dir = BUILD_DIR / "test_minimal"

    session.log("🧪 Testing minimal documentation build...")
    session.log("📦 Package: haive-core only")
    session.log("⚡ Profile: minimal (fastest)")

    # Run sphinx-build with minimal options
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        "-q",  # Quiet mode
        env=env,
        external=True,
    )

    session.log(f"✅ Test build successful: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-test-errors")
def docs_test_errors(session):
    """Test documentation build and show all errors/warnings.

    This builds with core+agents packages and shows all issues.

    Usage:
        nox -s docs-test-errors
    """
    env = {
        "SPHINX_PACKAGES": "core,agents",  # Two packages for better testing
        "SPHINX_PROFILE": "minimal",
        "SPHINX_INCLUDE_MCP_DOCS": "false",
        "SPHINX_INCLUDE_READMES": "true",  # Test README integration
    }

    output_dir = BUILD_DIR / "test_errors"

    session.log("🔍 Testing documentation build with error reporting...")
    session.log("📦 Packages: haive-core, haive-agents")

    # Run sphinx-build with full error reporting
    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            str(DOCS_DIR),
            str(output_dir),
            "-v",  # Verbose
            "-W",  # Treat warnings as errors
            "--keep-going",  # Continue despite errors
            "-T",  # Show full traceback
            env=env,
            external=True,
        )
        session.log("✅ Build completed without errors")
    except Exception as e:
        session.log(f"❌ Build failed with errors: {e}")
        # Still show where output is
        session.log(f"📄 Partial output: file://{output_dir}/index.html")


@nox.session(name="docs-test-incremental")
def docs_test_incremental(session):
    """Test incremental documentation build (uses cached doctrees).

    This is faster for iterative development as it reuses previous build artifacts.

    Usage:
        nox -s docs-test-incremental
    """
    env = {
        "SPHINX_PACKAGES": "core,agents,tools",  # Three packages
        "SPHINX_PROFILE": "standard",
    }

    output_dir = BUILD_DIR / "test_incremental"
    doctree_dir = BUILD_DIR / "doctrees" / "test_incremental"

    session.log("♻️ Testing incremental documentation build...")
    session.log("📦 Packages: core, agents, tools")
    session.log("🗂️ Using cached doctrees for speed")

    # Run sphinx-build with doctree caching
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        "-d",
        str(doctree_dir),  # Specify doctree directory
        env=env,
        external=True,
    )

    session.log(f"✅ Incremental build complete: {output_dir}")
    session.log("💡 Tip: Subsequent runs will be faster!")


@nox.session(name="docs-test-clean")
def docs_test_clean(session):
    """Clean all test build artifacts.

    Usage:
        nox -s docs-test-clean
    """
    import shutil

    test_dirs = [
        BUILD_DIR / "test_minimal",
        BUILD_DIR / "test_errors",
        BUILD_DIR / "test_incremental",
        BUILD_DIR / "doctrees" / "test_incremental",
    ]

    session.log("🧹 Cleaning test build artifacts...")

    for dir_path in test_dirs:
        if dir_path.exists():
            shutil.rmtree(dir_path)
            session.log(f"  ✅ Removed: {dir_path}")

    session.log("✨ Test build directories cleaned")


@nox.session(name="docs-test-single")
@nox.parametrize("package", ["core", "agents", "tools", "games", "mcp", "dataflow"])
def docs_test_single(session, package):
    """Test build for a single package.

    Examples:
        nox -s docs-test-single-core
        nox -s docs-test-single-agents
    """
    env = {
        "SPHINX_PACKAGES": package,
        "SPHINX_PROFILE": "minimal",
    }

    output_dir = BUILD_DIR / f"test_{package}"

    session.log(f"🧪 Testing {package} documentation build...")

    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        "-q",  # Quiet for speed
        env=env,
        external=True,
    )

    session.log(f"✅ {package} build successful")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-test-toc")
def docs_test_toc(session):
    """Test documentation build focusing on TOC tree structure.

    This helps debug navigation and TOC issues.

    Usage:
        nox -s docs-test-toc
    """
    env = {
        "SPHINX_PACKAGES": "core,agents",
        "SPHINX_PROFILE": "minimal",
        # Force specific TOC settings
        "SPHINX_SHOW_NAV_LEVEL": "3",  # Show 3 levels in nav
    }

    output_dir = BUILD_DIR / "test_toc"

    session.log("🌳 Testing TOC tree structure...")

    # Build with extra verbosity for TOC debugging
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        "-v",  # Verbose to see TOC processing
        "-D",
        "html_theme_options.show_nav_level=3",  # Override nav level
        "-D",
        "html_theme_options.navigation_depth=4",  # Deep navigation
        env=env,
        external=True,
    )

    session.log(f"✅ TOC test build complete: {output_dir}")
    session.log("🔍 Check the navigation sidebar for proper hierarchy")
