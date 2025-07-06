"""Nox configuration for Haive project tasks including documentation.

Quick Commands:
--------------
    nox -s docs         # Build docs (standard mode, shows warnings)
    nox -s docs_fast    # Build docs quickly (suppresses warnings)
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

Common Workflows:
----------------
    # First time building docs
    nox -s docs_clean && nox -s docs

    # Development workflow
    nox -s docs_serve  # Auto-rebuilds on changes

    # Quick view of existing docs
    nox -s docs_view

    # Full quality check
    nox -s lint && nox -s typecheck && nox -s test
"""

import os
import webbrowser
from pathlib import Path

import nox

# Define locations
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"

# Python versions to test
PYTHON_VERSIONS = ["3.12"]

# Environment info
# ----------------
# The documentation build currently has ~12,448 warnings related to:
# - Missing titles in toctree references
# - Autodoc import issues for some modules
# - Deprecated Sphinx configurations
#
# These are handled by:
# - docs: Shows warnings but continues
# - docs_fast: Suppresses warnings
# - docs_strict: Treats warnings as errors (will fail)

# Enable virtual environment reuse for faster runs
nox.options.reuse_existing_virtualenvs = True


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs(session):
    """Build the documentation using Sphinx (default mode, ignores warnings)."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)

    # Build HTML documentation WITHOUT treating warnings as errors
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
            "auto",  # Use parallel builds
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


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_fast(session):
    """Build documentation quickly (ignore warnings)."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)

    # Build HTML documentation without treating warnings as errors
    session.log("Building documentation in fast mode (ignoring warnings)")
    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-b",
            "html",
            "-j",
            "auto",
            "--quiet",  # Suppress warnings output
            str(SOURCE_DIR),
            str(BUILD_DIR / "html"),
            external=True,
        )
        session.log(f"✅ Fast documentation built in {BUILD_DIR / 'html'}")
        session.log("📝 Note: Warnings were ignored for faster build")
        session.log(f"🌐 Open file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")
    except Exception as e:
        session.error(f"❌ Documentation build failed: {e}")
        session.log("💡 Check Sphinx configuration in docs/source/conf.py")
        raise


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_strict(session):
    """Build documentation in strict mode (warnings as errors)."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)

    # Build with warnings as errors
    session.log("Building documentation in STRICT mode (warnings = errors)")
    session.log("⚠️  This will fail if there are any warnings!")
    try:
        session.run(
            "poetry",
            "run",
            "sphinx-build",
            "-W",
            "--keep-going",  # Treat warnings as errors
            "-b",
            "html",
            "-j",
            "auto",
            str(SOURCE_DIR),
            str(BUILD_DIR / "html"),
            external=True,
        )
        session.log("✅ Documentation built with NO warnings!"!")
    except Exception:
        session.error("❌ Build failed due to warnings"s")
        session.log("💡 Use 'nox -s docs' for normal build that ignores warnings")
        raise


@nox.session(python=PYTHON_VERSIONS)
def docs_minimal(session):
    """Build documentation with minimal dependencies (fastest)."""
    # Only install docs dependencies, not the full project
    session.install(
        "sphinx",
        "furo",
        "myst-parser",
        "sphinx-autodoc-typehints",
        "sphinx-copybutton",
        "sphinx-design",
        "sphinxcontrib-mermaid",
    )

    # Clean build directory
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)

    # Build HTML documentation without treating warnings as errors
    session.log("Building documentation in minimal mode (basic sphinx only)")
    try:
        session.run(
            "sphinx-build",
            "-b",
            "html",
            "-j",
            "auto",
            "--quiet",  # Suppress warnings output
            str(SOURCE_DIR),
            str(BUILD_DIR / "html"),
            external=True,
        )
        session.log(f"✅ Minimal documentation built in {BUILD_DIR / 'html'}")
        session.log("📝 Note: API docs may be missing - this is content only")
        session.log(f"🌐 Open file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")
    except Exception as e:
        session.error(f"❌ Documentation build failed: {e}")
        session.log("💡 Try 'nox -s docs_fast' for full build")
        raise


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_serve(session):
    """Build and serve documentation with auto-reload."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Install sphinx-autobuild if not present
    try:
        session.run("poetry", "show", "sphinx-autobuild", external=True, silent=True)
    except:
        session.log("Installing sphinx-autobuild...")
        session.run(
            "poetry", "add", "--group", "docs", "sphinx-autobuild", external=True
        )

    session.log("🔨 Building and serving documentation with auto-reload")
    session.log("🌐 Server will be available at http://localhost:8000")
    session.log("🔄 Auto-reload enabled - changes will trigger rebuild")
    session.log("⏹️  Press Ctrl+C to stop")

    # Use sphinx-autobuild for live reloading
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
            external=True,
        )
    except KeyboardInterrupt:
        session.log("🛑 Documentation server stopped")
    except Exception as e:
        session.error(f"❌ Server failed: {e}")
        session.log("💡 Check if port 8000 is already in use")
        raise


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)
        session.log(f"Cleaned {BUILD_DIR}")

    # Clean any generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        session.run("rm", "-rf", str(api_dir), external=True)
        session.log(f"Cleaned {api_dir}")


@nox.session(python=PYTHON_VERSIONS)
def docs_view(session):
    """View existing documentation in browser (no rebuild)."""
    html_dir = BUILD_DIR / "html"

    if not html_dir.exists():
        session.error(f"📁 Documentation not found at {html_dir}")
        session.log("💡 Run 'nox -s docs_fast' first to build documentation")
        return

    index_file = html_dir / "index.html"
    if not index_file.exists():
        session.error(f"📄 index.html not found in {html_dir}")
        session.log("💡 Documentation may be incomplete - try rebuilding")
        return

    # Start a simple HTTP server
    session.log(f"📁 Serving documentation from {html_dir}")
    session.log("🌐 Starting server at http://localhost:8000")
    session.log("⏹️  Press Ctrl+C to stop")

    # Try to open in browser
    try:
        webbrowser.open("http://localhost:8000")
        session.log("✅ Opened documentation in browser")
    except Exception as e:
        session.log(f"⚠️  Could not open browser: {e}")
        session.log("🌐 Open http://localhost:8000 manually")

    # Serve the documentation
    try:
        os.chdir(html_dir)
        session.run("python", "-m", "http.server", "8000", external=True)
    except KeyboardInterrupt:
        session.log("🛑 Documentation server stopped")
    except Exception as e:
        session.error(f"❌ Server failed: {e}")
        session.log("💡 Check if port 8000 is already in use")
        raise


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def docs_check(session):
    """Check documentation for broken links and references."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Build with linkcheck
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


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def lint(session):
    """Run linters on the codebase."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pre-commit", "run", "--all-files", external=True)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def test(session):
    """Run the test suite."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", external=True)


@nox.session(python=PYTHON_VERSIONS, reuse_venv=True)
def typecheck(session):
    """Run type checking with mypy."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "mypy", "packages/", external=True)


@nox.session(name="list")
def list_sessions(session):
    """List all available nox sessions with detailed information."""
    session.log("=" * 70)
    session.log("📋 HAIVE NOX SESSIONS - Complete Command Reference")
    session.log("=" * 70)
    session.log("")
    session.log("📚 DOCUMENTATION COMMANDS:")
    session.log("-" * 50)
    session.log("  nox -s docs         - Build documentation (standard mode)")
    session.log("                        Shows warnings but continues building")
    session.log("                        ✅ Recommended for normal use")
    session.log("")
    session.log("  nox -s docs_fast    - Build documentation quickly")
    session.log("                        Suppresses warning output with --quiet")
    session.log("                        ⚡ Fastest full build")
    session.log("")
    session.log("  nox -s docs_minimal - Build with minimal dependencies")
    session.log("                        Only basic Sphinx, no full project install")
    session.log("                        🚀 Fastest option, but no API docs")
    session.log("")
    session.log("  nox -s docs_strict  - Build in strict mode (warnings = errors)")
    session.log("                        Will fail if any warnings exist")
    session.log("                        ❌ Currently fails with 12,448 warnings")
    session.log("")
    session.log("  nox -s docs_serve   - Build and serve with auto-reload")
    session.log("                        Watches for changes and rebuilds")
    session.log("                        🔄 Best for documentation development")
    session.log("")
    session.log("  nox -s docs_view    - View existing docs without rebuild")
    session.log("                        Serves pre-built docs on localhost:8000")
    session.log("                        👀 Quick preview of last build")
    session.log("")
    session.log("  nox -s docs_clean   - Clean documentation build artifacts")
    session.log("                        Removes docs/build directory")
    session.log("                        🧹 Use before fresh build")
    session.log("")
    session.log("  nox -s docs_check   - Check for broken links and references")
    session.log("                        Runs Sphinx linkcheck builder")
    session.log("                        🔍 Quality assurance check")
    session.log("")
    session.log("🔧 DEVELOPMENT COMMANDS:")
    session.log("-" * 50)
    session.log("  nox -s lint         - Run pre-commit linters on all files")
    session.log("                        Includes black, flake8, mypy, etc.")
    session.log("")
    session.log("  nox -s test         - Run the full test suite")
    session.log("                        Runs pytest on all packages")
    session.log("")
    session.log("  nox -s typecheck    - Run MyPy type checking")
    session.log("                        Checks packages/ directory")
    session.log("")
    session.log("💡 COMMON WORKFLOWS:")
    session.log("-" * 50)
    session.log("  # First time building:")
    session.log("  nox -s docs_clean && nox -s docs")
    session.log("")
    session.log("  # Quick build and view:")
    session.log("  nox -s docs_fast && nox -s docs_view")
    session.log("")
    session.log("  # Development with auto-reload:")
    session.log("  nox -s docs_serve")
    session.log("")
    session.log("  # Full quality check before commit:")
    session.log("  nox -s lint && nox -s typecheck && nox -s test")
    session.log("")
    session.log("  # Check what sessions are available:")
    session.log("  nox -s list  # or just 'nox --list'")
    session.log("")
    session.log("🚀 PERFORMANCE TIPS:")
    session.log("-" * 50)
    session.log("- Virtual environments are now reused by default (faster!)")
    session.log("- Use -j auto flag for parallel builds")
    session.log("- Direct poetry commands skip nox overhead:")
    session.log("    poetry run sphinx-build -b html docs/source docs/build/html")
    session.log("")
    session.log("📝 NOTES:")
    session.log("-" * 50)
    session.log("- Documentation output: docs/build/html/")
    session.log("- Current warnings: ~12,448 (mostly toctree and autodoc issues)")
    session.log("- Python version: 3.12")
    session.log("- Use 'nohup' for long-running builds to avoid timeouts")
    session.log("")
    session.log("=" * 70)
