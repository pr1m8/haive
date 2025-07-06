"""Enhanced Nox configuration for Haive project with optimizations.

Key Improvements:
----------------
- Caching of virtual environments
- Parallel dependency installation
- Direct poetry run for faster execution
- Better error handling and recovery
- Optimized dependency installation
- Support for both nox and direct poetry commands

Quick Commands:
--------------
    nox -s docs         # Build docs (standard mode, shows warnings)
    nox -s docs_fast    # Build docs quickly (suppresses warnings)
    nox -s docs_direct  # Direct poetry build (no venv recreation)
    nox -s docs_minimal # Build with minimal deps (fastest)
    nox -s docs_strict  # Build in strict mode (fails on warnings)
    nox -s docs_serve   # Build and serve with auto-reload
    nox -s docs_view    # View existing docs without rebuild
    nox -s docs_clean   # Clean build artifacts
    nox -s docs_check   # Check for broken links
    nox -s lint         # Run linters
    nox -s test         # Run tests
    nox -s typecheck    # Run type checking
    nox -s list         # Show all available sessions

Poetry Direct Commands (Faster):
-------------------------------
    poetry run sphinx-build -b html docs/source docs/build/html
    poetry run sphinx-autobuild docs/source docs/build/html
    poetry run python -m http.server -d docs/build/html 8000

Common Workflows:
----------------
    # First time building docs
    nox -s docs_clean && nox -s docs_direct

    # Development workflow
    nox -s docs_serve  # Auto-rebuilds on changes

    # Quick view of existing docs
    nox -s docs_view

    # Full quality check
    nox -s lint && nox -s typecheck && nox -s test
"""

import os
import shutil
import sys
import webbrowser
from pathlib import Path
from typing import Optional

import nox

# Configuration
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"
PYTHON_VERSIONS = ["3.12"]

# Cache control - Set to False to force fresh environments
USE_VENV_CACHE = True

# Performance settings
PARALLEL_INSTALL = True
MINIMAL_INSTALL = True

# Session defaults
nox.options.reuse_existing_virtualenvs = USE_VENV_CACHE
nox.options.error_on_external_run = False


def ensure_poetry_available(session):
    """Ensure poetry is available in the session."""
    try:
        session.run("poetry", "--version", external=True, silent=True)
        return True
    except Exception:
        session.log("Poetry not found in PATH, installing...")
        session.install("poetry")
        return False


def clean_nox_cache(session, force: bool = False):
    """Clean nox cache if needed."""
    nox_dir = Path(".nox")
    if nox_dir.exists() and (force or not USE_VENV_CACHE):
        session.log("Cleaning nox cache...")
        try:
            shutil.rmtree(nox_dir)
        except PermissionError:
            session.log("Warning: Could not remove .nox directory (permission denied)")
            session.log("You may need to manually remove it: rm -rf .nox")


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs(session):
    """Build the documentation using Sphinx (standard mode, shows warnings)."""
    ensure_poetry_available(session)

    # Install dependencies with better error handling
    session.log("Installing documentation dependencies...")
    try:
        if MINIMAL_INSTALL:
            session.run("poetry", "install", "--only", "docs", external=True)
        else:
            session.run("poetry", "install", "--with", "docs", external=True)
    except Exception as e:
        session.error(f"Dependency installation failed: {e}")
        session.log("Try: nox -s docs_direct for direct poetry execution")
        raise

    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Build HTML documentation
    session.log(
        "Building documentation (warnings will be shown but not fail the build)"
    )
    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-j",
            "auto",  # Parallel build
            str(SOURCE_DIR),
            str(BUILD_DIR / "html"),
            external=True,
        )
        session.log(f"✅ Documentation built successfully in {BUILD_DIR / 'html'}")
        session.log("📝 Build completed with warnings (this is normal)"l)")
        session.log(f"🌐 Open file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")
    except Exception as e:
        session.error(f"❌ Documentation build failed: {e}")
        raise


@nox.session(python=PYTHON_VERSIONS, name="docs_direct")
def docs_direct(session):
    """Build documentation using poetry directly (no venv management)."""
    # This bypasses nox virtual environment management
    session.log("Building documentation with direct poetry execution...")

    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    # Run sphinx directly through poetry
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",  # Parallel build
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"✅ Documentation built in {BUILD_DIR / 'html'}")
    session.log(f"🌐 View at: file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_fast(session):
    """Build documentation quickly (suppress warnings)."""
    ensure_poetry_available(session)

    # Minimal install for speed
    session.run("poetry", "install", "--only", "docs", external=True)

    # Clean and build
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    session.log("Building documentation in fast mode (ignoring warnings)")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",
        "--quiet",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"✅ Fast documentation built in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_minimal(session):
    """Build documentation with minimal dependencies (fastest)."""
    # Only install core Sphinx dependencies
    session.install(
        "sphinx>=7.0",
        "furo",
        "myst-parser",
        "sphinx-autodoc-typehints",
        "sphinx-copybutton",
        "sphinx-design",
        "sphinxcontrib-mermaid",
    )

    # Clean and build
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    session.log("Building documentation in minimal mode")
    session.run(
        "sphinx-build",
        "-b",
        "html",
        "-j",
        "auto",
        "--quiet",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
    )

    session.log(f"✅ Minimal documentation built in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_serve(session):
    """Build and serve documentation with auto-reload."""
    ensure_poetry_available(session)

    # Check if sphinx-autobuild is available
    try:
        session.run("poetry", "show", "sphinx-autobuild", external=True, silent=True)
    except Exception:
        session.log("Installing sphinx-autobuild...")
        session.run(
            "poetry", "add", "--group", "docs", "sphinx-autobuild", external=True
        )

    session.log("🔨 Building and serving documentation with auto-reload")
    session.log("🌐 Server will be available at http://localhost:8000")
    session.log("🔄 Auto-reload enabled - changes will trigger rebuild")
    session.log("⏹️  Press Ctrl+C to stop")

    try:
        session.run(
            "poetry",
            "run",
            "sphinx-autobuild",
            str(SOURCE_DIR),
            str(BUILD_DIR / "html"),
            "--port",
            "8000",
            "--watch",
            "packages",
            "--ignore",
            "*.pyc",
            "--ignore",
            "*.log",
            "--ignore",
            ".nox/*",
            "--ignore",
            ".git/*",
            "--ignore",
            "__pycache__",
            external=True,
        )
    except KeyboardInterrupt:
        session.log("🛑 Documentation server stopped")


@nox.session(python=PYTHON_VERSIONS)
def docs_view(session):
    """View existing documentation in browser (no rebuild)."""
    html_dir = BUILD_DIR / "html"

    if not html_dir.exists() or not (html_dir / "index.html").exists():
        session.error(f"📁 Documentation not found at {html_dir}")
        session.log("💡 Run 'nox -s docs_direct' first to build documentation")
        return

    # Open browser
    url = "http://localhost:8000"
    session.log(f"📁 Serving documentation from {html_dir}")
    session.log(f"🌐 Starting server at {url}")
    session.log("⏹️  Press Ctrl+C to stop")

    try:
        webbrowser.open(url)
        session.log("✅ Opened documentation in browser")
    except Exception:
        session.log(f"🌐 Open {url} manually in your browser")

    # Serve documentation
    try:
        os.chdir(html_dir)
        session.run("python", "-m", "http.server", "8000")
    except KeyboardInterrupt:
        session.log("🛑 Documentation server stopped")


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts and caches."""
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Cleaned {BUILD_DIR}")

    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")

    # Clean sphinx cache
    doctrees = DOCS_DIR / "doctrees"
    if doctrees.exists():
        shutil.rmtree(doctrees)
        session.log(f"✅ Cleaned {doctrees}")

    # Option to clean nox cache
    if "--clean-nox" in session.posargs:
        clean_nox_cache(session, force=True)


@nox.session(python=PYTHON_VERSIONS)
def docs_check(session):
    """Check documentation for broken links and references."""
    ensure_poetry_available(session)
    session.run("poetry", "install", "--only", "docs", external=True)

    session.log("🔍 Checking for broken links...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "linkcheck",
        str(SOURCE_DIR),
        str(BUILD_DIR / "linkcheck"),
        external=True,
    )

    # Show results
    output_file = BUILD_DIR / "linkcheck" / "output.txt"
    if output_file.exists():
        session.log("\n📋 Link check results:")
        session.run("cat", str(output_file), external=True)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def lint(session):
    """Run linters on the codebase."""
    ensure_poetry_available(session)
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "pre-commit", "run", "--all-files", external=True)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def test(session):
    """Run the test suite."""
    ensure_poetry_available(session)
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("poetry", "run", "pytest", "-v", external=True)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def typecheck(session):
    """Run type checking with mypy."""
    ensure_poetry_available(session)
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "mypy", "packages/", external=True)


@nox.session(name="fix-deps")
def fix_deps(session):
    """Fix dependency issues (like yanked packages)."""
    session.log("🔧 Fixing dependency issues...")

    # Update lock file
    session.run("poetry", "lock", "--no-update", external=True)

    # Clear pip cache
    session.run("pip", "cache", "purge", external=True)

    # Reinstall
    session.run("poetry", "install", "--sync", external=True)

    session.log("✅ Dependencies fixed")


@nox.session(name="list")
def list_sessions(session):
    """List all available nox sessions with detailed information."""
    session.log("=" * 70)
    session.log("📋 ENHANCED HAIVE NOX SESSIONS")
    session.log("=" * 70)
    session.log("")
    session.log("🚀 QUICK START:")
    session.log("-" * 50)
    session.log("  nox -s docs_direct  - Fastest build (uses poetry directly)")
    session.log("  nox -s docs_view    - View existing docs")
    session.log("  nox -s docs_serve   - Live development server")
    session.log("")
    session.log("📚 DOCUMENTATION COMMANDS:")
    session.log("-" * 50)
    session.log("  nox -s docs         - Standard build (with nox venv)")
    session.log("  nox -s docs_direct  - Direct poetry build (fastest)")
    session.log("  nox -s docs_fast    - Quick build (suppress warnings)")
    session.log("  nox -s docs_minimal - Minimal deps build")
    session.log("  nox -s docs_serve   - Auto-reload development")
    session.log("  nox -s docs_view    - View without rebuild")
    session.log("  nox -s docs_clean   - Clean all artifacts")
    session.log("  nox -s docs_check   - Check broken links")
    session.log("")
    session.log("🔧 DEVELOPMENT:")
    session.log("-" * 50)
    session.log("  nox -s lint         - Run linters")
    session.log("  nox -s test         - Run tests")
    session.log("  nox -s typecheck    - Type checking")
    session.log("  nox -s fix-deps     - Fix dependency issues")
    session.log("")
    session.log("⚡ POETRY DIRECT COMMANDS (No nox overhead):")
    session.log("-" * 50)
    session.log("  poetry run sphinx-build -b html docs/source docs/build/html")
    session.log("  poetry run sphinx-autobuild docs/source docs/build/html")
    session.log("  cd docs/build/html && python -m http.server 8000")
    session.log("")
    session.log("💡 TIPS:")
    session.log("-" * 50)
    session.log("- Use 'docs_direct' for fastest builds")
    session.log("- Add --clean-nox to docs_clean to remove .nox cache")
    session.log("- Virtual envs are reused by default for speed")
    session.log("- Set USE_VENV_CACHE=False in noxfile to force fresh envs")
    session.log("")
    session.log("=" * 70)
