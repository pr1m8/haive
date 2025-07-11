"""Nox configuration for Haive project.

Simple Commands:
---------------
    nox -s docs                 # Build docs once
    nox -s docs_serve           # Build and serve with auto-reload (port 8003)
    nox -s docs_clean           # Clean build artifacts
    nox -s lint                 # Run linters
    nox -s test                 # Run tests
"""

import os
import shutil
import subprocess
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "_build"


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build documentation once with verbose output and import error handling."""
    session.log("📚 Building documentation...")

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for graceful import handling
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = (
        "false"  # Disable problematic autosummary
    )
    os.environ["HAIVE_DOCS_MODE"] = "true"
    os.environ["SPHINX_AUTODOC_MOCK_IMPORTS"] = "true"

    # Test critical imports first
    session.log("🔍 Testing critical imports...")
    test_modules = [
        "haive.core",
        "haive.agents.simple",
        "haive.agents.react",
        "haive.agents.rag.base",
    ]

    for module in test_modules:
        try:
            session.run(
                "poetry",
                "run",
                "python",
                "-c",
                f"import {module}; print(f'✅ {module}')",
                external=True,
                silent=True,
            )
        except Exception:
            session.log(f"⚠️  Import issue with {module} - will be handled gracefully")

    # Build with error tolerance
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-v",  # Verbose output
        "-b",
        "html",  # HTML output
        "-j",
        "auto",  # Parallel builds
        "--keep-going",  # Continue on errors
        "-W",
        "--keep-going",  # Treat warnings as errors but keep going
        "-T",  # Show full traceback on error
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"✅ Documentation built at: {BUILD_DIR / 'html' / 'index.html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Serve documentation with auto-reload and smart caching."""
    session.log("🚀 Starting documentation server with auto-reload...")

    # Kill any existing processes on port 8003
    try:
        session.run("pkill", "-f", "sphinx-autobuild.*--port 8003", external=True)
        session.log("🧹 Killed existing sphinx processes")
    except Exception:
        pass  # No existing processes

    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)

    # Set environment for graceful handling
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"  # Faster for serving
    os.environ["HAIVE_DOCS_MODE"] = "true"

    session.log("🌐 Server starting at: http://localhost:8003")
    session.log("📁 Watching packages/ for changes")
    session.log("⚠️  Import warnings are normal and handled gracefully")

    # Start sphinx-autobuild with smart options
    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port",
        "8003",
        "--host",
        "0.0.0.0",
        "--watch",
        "packages",  # Watch source code changes
        "--ignore",
        "*.pyc",
        "--ignore",
        "*.pyo",
        "--ignore",
        "*~",
        "--ignore",
        ".git/*",
        "--ignore",
        "_build/*",
        "--ignore",
        "__pycache__/*",
        "--open-browser",
        "--delay",
        "1",  # Smart delay for rapid changes
        "-v",  # Verbose output
        "-j",
        "auto",  # Parallel builds
        external=True,
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Cleaned {BUILD_DIR}")

    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")

    session.log("✅ Documentation cleaned")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run code quality checks."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "ruff", "check", "packages/", external=True)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run test suite."""
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("poetry", "run", "pytest", "-v", external=True)
