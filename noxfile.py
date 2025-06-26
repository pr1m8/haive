"""Nox sessions for documentation building and serving."""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import nox

# Configuration
DOCS_DIR = Path("docs")
DOCS_SOURCE = DOCS_DIR / "source"
DOCS_BUILD = DOCS_DIR / "build"
DOCS_HTML = DOCS_BUILD / "html"
LOG_DIR = Path("logs/docs")

# Ensure log directory exists
LOG_DIR.mkdir(parents=True, exist_ok=True)


def is_docs_built():
    """Check if documentation has been built."""
    return DOCS_HTML.exists() and (DOCS_HTML / "index.html").exists()


def check_sphinx_installed():
    """Check if Sphinx is installed in the current environment."""
    try:
        import sphinx

        return True
    except ImportError:
        return False


def check_sphinx_autobuild_installed():
    """Check if sphinx-autobuild is installed."""
    try:
        import sphinx_autobuild

        return True
    except ImportError:
        return False


@nox.session(python=False, name="docs")
def build_docs(session: nox.Session) -> None:
    """Build documentation using Sphinx."""
    # Install dependencies if needed
    if not check_sphinx_installed():
        session.log("📦 Installing documentation dependencies...")
        session.run("poetry", "install", "--with", "docs", external=True)

    # Handle clean build
    if "--clean" in session.posargs:
        session.log("🧹 Cleaning previous build...")
        if DOCS_BUILD.exists():
            shutil.rmtree(DOCS_BUILD)
        # Also clean autosummary generated files
        api_generated = DOCS_SOURCE / "api" / "generated"
        if api_generated.exists():
            shutil.rmtree(api_generated)

    session.log("📚 Building documentation...")

    # Build command
    cmd = [
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_SOURCE),
        str(DOCS_HTML),
        "--keep-going",  # Continue despite errors
    ]

    # Add options from command line
    if "--fresh" in session.posargs or "-E" in session.posargs:
        cmd.append("-E")  # Don't use saved environment
        session.log("🔄 Performing fresh build...")

    if "--verbose" in session.posargs or "-v" in session.posargs:
        cmd.append("-v")  # Verbose output

    # Log warnings to file
    log_file = LOG_DIR / f"build_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    cmd.extend(["-w", str(log_file)])

    # Run build
    try:
        session.run(*cmd, external=True)
        session.log("✅ Documentation built successfully!")
        session.log(f"📄 View at: file://{DOCS_HTML.absolute()}/index.html")
        session.log(f"📝 Build log: {log_file}")
    except Exception:
        session.error(f"❌ Build failed! Check {log_file} for details")


@nox.session(python=False, name="docs-live")
def docs_live(session: nox.Session) -> None:
    """Run sphinx-autobuild for live editing with auto-reload."""
    # Check dependencies
    if not check_sphinx_autobuild_installed():
        session.log("📦 Installing sphinx-autobuild...")
        session.run("poetry", "install", "--with", "docs", external=True)

    session.log("🔄 Starting live documentation server...")
    session.log("📝 Changes will auto-rebuild")
    session.log("🌐 Server: http://localhost:8000")
    session.log("🛑 Press Ctrl+C to stop")

    cmd = [
        "sphinx-autobuild",
        str(DOCS_SOURCE),
        str(DOCS_HTML),
        "--host",
        "0.0.0.0",
        "--port",
        "8000",
        # Watch additional directories
        "--watch",
        "packages/haive-core/src",
        "--watch",
        "packages/haive-agents/src",
        "--watch",
        "packages/haive-tools/src",
        # Ignore patterns
        "--ignore",
        "*.pyc",
        "--ignore",
        "*.pyo",
        "--ignore",
        "*~",
        "--ignore",
        ".#*",
        "--ignore",
        "*.swp",
        "--ignore",
        "*__pycache__*",
    ]

    # Add --open to auto-open browser
    if "--open" in session.posargs:
        cmd.append("--open-browser")

    try:
        session.run(*cmd, external=True)
    except KeyboardInterrupt:
        session.log("\n✋ Live server stopped")


@nox.session(python=False, name="serve")
def serve_docs(session: nox.Session) -> None:
    """Serve built documentation with Python's HTTP server."""
    if not is_docs_built():
        session.log("📚 Documentation not found. Building first...")
        build_docs(session)

    port = "8000"
    # Allow custom port
    for arg in session.posargs:
        if arg.isdigit():
            port = arg
            break

    session.log(f"🌐 Serving documentation at http://localhost:{port}")
    session.log("🛑 Press Ctrl+C to stop")

    # Change to HTML directory and serve
    original_dir = Path.cwd()
    try:
        os.chdir(DOCS_HTML)
        session.run(sys.executable, "-m", "http.server", port, external=True)
    except KeyboardInterrupt:
        session.log("\n✋ Server stopped")
    finally:
        os.chdir(original_dir)


@nox.session(python=False, name="docs-clean")
def clean_docs(session: nox.Session) -> None:
    """Remove all built documentation."""
    session.log("🧹 Cleaning documentation...")

    # Remove build directory
    if DOCS_BUILD.exists():
        shutil.rmtree(DOCS_BUILD)
        session.log(f"✓ Removed {DOCS_BUILD}")

    # Remove autosummary generated files
    api_generated = DOCS_SOURCE / "api" / "generated"
    if api_generated.exists():
        shutil.rmtree(api_generated)
        session.log(f"✓ Removed {api_generated}")

    # Clean old log files (older than 7 days)
    if LOG_DIR.exists():
        import time

        current_time = time.time()
        for log_file in LOG_DIR.glob("*.log"):
            file_age = current_time - log_file.stat().st_mtime
            if file_age > (7 * 24 * 60 * 60):  # 7 days in seconds
                log_file.unlink()
                session.log(f"✓ Removed old log: {log_file.name}")

    session.log("✅ Cleanup complete!")


@nox.session(python=False, name="docs-check")
def check_docs(session: nox.Session) -> None:
    """Check documentation for errors without building."""
    if not check_sphinx_installed():
        session.log("📦 Installing documentation dependencies...")
        session.run("poetry", "install", "--with", "docs", external=True)

    session.log("🔍 Checking documentation for errors...")

    # Use linkcheck builder to check for broken links
    cmd = [
        "sphinx-build",
        "-b",
        "linkcheck",
        str(DOCS_SOURCE),
        str(DOCS_BUILD / "linkcheck"),
        "-q",  # Quiet mode
    ]

    try:
        session.run(*cmd, external=True)
        session.log("✅ Link check passed!")
    except:
        session.warn("⚠️  Some links may be broken")

    # Also do a dummy build to check for other errors
    session.log("🔍 Checking for build errors...")
    cmd = [
        "sphinx-build",
        "-b",
        "dummy",
        "-W",  # Treat warnings as errors
        "--keep-going",
        str(DOCS_SOURCE),
        str(DOCS_BUILD / "dummy"),
    ]

    log_file = LOG_DIR / f"check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    cmd.extend(["-w", str(log_file)])

    try:
        session.run(*cmd, external=True)
        session.log("✅ Documentation check passed!")
    except:
        session.warn(f"⚠️  Documentation has warnings. See {log_file}")


# Convenience aliases
@nox.session(python=False, name="d")
def docs_alias(session: nox.Session) -> None:
    """Alias for 'docs' - build documentation."""
    build_docs(session)


@nox.session(python=False, name="dl")
def docs_live_alias(session: nox.Session) -> None:
    """Alias for 'docs-live' - live documentation server."""
    docs_live(session)


@nox.session(python=False, name="s")
def serve_alias(session: nox.Session) -> None:
    """Alias for 'serve' - serve built docs."""
    serve_docs(session)


# Example Usage:
"""
# Build docs (incremental)
nox -s docs

# Build fresh (clean build)
nox -s docs -- --clean

# Live server with auto-rebuild
nox -s docs-live
nox -s docs-live -- --open  # Auto-open browser

# Serve existing docs
nox -s serve
nox -s serve -- 8080  # Custom port

# Clean all docs
nox -s docs-clean

# Check for errors
nox -s docs-check

# Quick aliases
nox -s d    # Build
nox -s dl   # Live
nox -s s    # Serve
"""
