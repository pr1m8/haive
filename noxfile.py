"""Nox configuration for Haive project tasks including documentation."""

import nox
from pathlib import Path

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
        "poetry", "run", "sphinx-build",
        "-W", "--keep-going",  # Treat warnings as errors but continue
        "-b", "html",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True
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
        "poetry", "run", "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port", "8000",
        "--watch", ".",
        external=True
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
        "poetry", "run", "sphinx-build",
        "-b", "linkcheck",
        str(SOURCE_DIR),
        str(BUILD_DIR / "linkcheck"),
        external=True
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_coverage(session):
    """Check documentation coverage for Python API."""
    session.install("poetry")
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Build with coverage check
    session.run(
        "poetry", "run", "sphinx-build",
        "-b", "coverage",
        str(SOURCE_DIR),
        str(BUILD_DIR / "coverage"),
        external=True
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


# Convenience session that lists all available sessions
@nox.session
def list(session):
    """List all available nox sessions."""
    session.log("Available sessions:")
    session.log("  docs         - Build documentation")
    session.log("  docs_serve   - Build and serve docs with auto-reload")
    session.log("  docs_clean   - Clean documentation build")
    session.log("  docs_check   - Check for broken links")
    session.log("  docs_coverage - Check documentation coverage")
    session.log("  lint         - Run linters")
    session.log("  test         - Run tests")
    session.log("  typecheck    - Run type checking")