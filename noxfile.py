"""Nox configuration for Haive project tasks including documentation."""

from pathlib import Path

import nox

# Define locations
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"

# Python versions to test
PYTHON_VERSIONS = ["3.12"]


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build the documentation using Sphinx."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Clean build directory
    if BUILD_DIR.exists():
        session.run("rm", "-rf", str(BUILD_DIR), external=True)

    # Build HTML documentation
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-W",
        "--keep-going",  # Treat warnings as errors but continue
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"Documentation built in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_fast(session):
    """Build documentation quickly without treating warnings as errors."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Build HTML documentation without warning flags
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )

    session.log(f"Documentation built in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Build and serve documentation with auto-reload."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    session.log("Starting documentation server at http://localhost:8000")
    session.log("Press Ctrl+C to stop")

    # Use sphinx-autobuild for live reloading
    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port",
        "8000",
        "--watch",
        ".",
        external=True,
    )


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


@nox.session(python=PYTHON_VERSIONS)
def docs_coverage(session):
    """Check documentation coverage for Python API."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    # Build with coverage check
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "coverage",
        str(SOURCE_DIR),
        str(BUILD_DIR / "coverage"),
        external=True,
    )

    # Show coverage report
    coverage_file = BUILD_DIR / "coverage" / "python.txt"
    if coverage_file.exists():
        session.run("cat", str(coverage_file), external=True)


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run linters on the codebase."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pre-commit", "run", "--all-files", external=True)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run the test suite."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "pytest", external=True)


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session):
    """Run type checking with mypy."""
    session.install("poetry")
    session.run("poetry", "install", external=True)
    session.run("poetry", "run", "mypy", "packages/", external=True)


@nox.session(python=PYTHON_VERSIONS)
def docs_view(session):
    """View existing documentation in browser (no rebuild)."""
    import os
    import webbrowser

    html_dir = BUILD_DIR / "html"

    if not html_dir.exists():
        session.error(f"Documentation not found at {html_dir}")
        session.log("Run 'nox -s docs' or 'nox -s docs_fast' first to build")
        return

    # Start a simple HTTP server
    session.log(f"Serving documentation from {html_dir}")
    session.log("Starting server at http://localhost:8000")
    session.log("Press Ctrl+C to stop")

    # Try to open in browser
    try:
        webbrowser.open("http://localhost:8000")
        session.log("✅ Opened documentation in browser")
    except Exception as e:
        session.log(f"Could not open browser: {e}")
        session.log("Open http://localhost:8000 manually")

    # Serve the documentation
    os.chdir(html_dir)
    session.run("python", "-m", "http.server", "8000", external=True)


# Convenience session that lists all available sessions
@nox.session(python=PYTHON_VERSIONS)
def docs_fix(session):
    """Fix common documentation warnings and build issues."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)

    import re
    from pathlib import Path

    session.log("Fixing common documentation issues...")

    # Fix triple backticks in RST files
    rst_files = list(SOURCE_DIR.rglob("*.rst"))
    fixed_count = 0

    for rst_file in rst_files:
        content = rst_file.read_text()
        original = content

        # Fix triple backticks in :doc: references
        content = re.sub(r":doc:```", ":doc:`", content)

        # Fix inline literal/strong issues
        content = re.sub(r"\*\*([^*]+)$", r"**\1**", content, flags=re.MULTILINE)
        content = re.sub(r"``([^`]+)$", r"``\1``", content, flags=re.MULTILINE)

        if content != original:
            rst_file.write_text(content)
            fixed_count += 1
            session.log(f"Fixed {rst_file}")

    session.log(f"Fixed {fixed_count} files")

    # Now build with fast mode to see remaining issues
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )


@nox.session
def list(session):
    """List all available nox sessions."""
    session.log("Available sessions:")
    session.log("  docs         - Build documentation (with warnings as errors)")
    session.log(
        "  docs_fast    - Build documentation (without treating warnings as errors)"
    )
    session.log("  docs_serve   - Build and serve docs with auto-reload")
    session.log("  docs_view    - View existing documentation (no rebuild)")
    session.log("  docs_fix     - Fix common documentation warnings and issues")
    session.log("  docs_clean   - Clean documentation build")
    session.log("  docs_check   - Check for broken links")
    session.log("  docs_coverage - Check documentation coverage")
    session.log("  lint         - Run linters")
    session.log("  test         - Run tests")
    session.log("  typecheck    - Run type checking")
