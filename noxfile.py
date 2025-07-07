"""Nox configuration for Haive project.

Quick Commands:
--------------
    nox -s docs         # Build docs with autosummary
    nox -s docs_fast    # Build docs without autosummary 
    nox -s docs_serve   # Build and serve with auto-reload
    nox -s docs_clean   # Clean build artifacts
    nox -s lint         # Run linters
    nox -s test         # Run tests
    nox -s typecheck    # Run type checking
"""

import os
import shutil
import webbrowser
from pathlib import Path

import nox

# Configuration
PYTHON_VERSIONS = ["3.12"]
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_external_run = False

# Paths
DOCS_DIR = Path("docs")
SOURCE_DIR = DOCS_DIR / "source"
BUILD_DIR = DOCS_DIR / "build"


@nox.session(python=PYTHON_VERSIONS)
def docs(session):
    """Build documentation with full autosummary generation."""
    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)
    
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # Enable autosummary generation
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "true"
    
    # Build documentation
    session.log("Building documentation with autosummary...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b", "html",
        "-j", "auto",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )
    
    # Run fix script if it exists
    fix_script = Path("scripts/fix_autosummary_output.py")
    if fix_script.exists():
        session.log("Fixing autosummary output...")
        session.run("poetry", "run", "python", str(fix_script), external=True)
    
    session.log(f"✅ Documentation built in {BUILD_DIR / 'html'}")
    session.log(f"🌐 Open file://{BUILD_DIR.absolute() / 'html' / 'index.html'}")


@nox.session(python=PYTHON_VERSIONS, name="docs_fast")
def docs_fast(session):
    """Build documentation quickly without autosummary generation."""
    # Install minimal dependencies
    session.run("poetry", "install", "--only", "docs", external=True)
    
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    
    # Disable autosummary generation for speed
    os.environ["SPHINX_AUTOSUMMARY_GENERATE"] = "false"
    
    # Build documentation
    session.log("Building documentation (fast mode)...")
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b", "html",
        "-j", "auto",
        "-q",  # Quiet mode
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        external=True,
    )
    
    session.log(f"✅ Fast build complete in {BUILD_DIR / 'html'}")


@nox.session(python=PYTHON_VERSIONS)
def docs_serve(session):
    """Build and serve documentation with auto-reload using sphinx-autobuild."""
    # Install dependencies
    session.run("poetry", "install", "--with", "docs", external=True)
    
    session.log("🔨 Building and serving documentation with auto-reload")
    session.log("🌐 Server at http://localhost:8000")
    
    # Simple sphinx-autobuild
    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        str(SOURCE_DIR),
        str(BUILD_DIR / "html"),
        "--port", "8000",
        external=True,
    )


@nox.session(python=PYTHON_VERSIONS)
def docs_clean(session):
    """Clean documentation build artifacts."""
    # Clean build directory
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
        session.log(f"✅ Cleaned {BUILD_DIR}")
    
    # Clean generated API docs
    api_dir = SOURCE_DIR / "api" / "generated"
    if api_dir.exists():
        shutil.rmtree(api_dir)
        session.log(f"✅ Cleaned {api_dir}")
    
    # Clean doctrees
    doctrees = DOCS_DIR / "doctrees"
    if doctrees.exists():
        shutil.rmtree(doctrees)
        session.log(f"✅ Cleaned {doctrees}")
    
    session.log("✅ Documentation artifacts cleaned")


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    """Run code quality checks."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "ruff", "check", "packages/", external=True)
    session.run("poetry", "run", "black", "--check", "packages/", external=True)


@nox.session(python=PYTHON_VERSIONS)
def test(session):
    """Run test suite."""
    session.run("poetry", "install", "--with", "test", external=True)
    session.run("poetry", "run", "pytest", "-v", external=True)


@nox.session(python=PYTHON_VERSIONS)
def typecheck(session):
    """Run type checking with mypy."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("poetry", "run", "mypy", "packages/", external=True)




@nox.session
def fix_autosummary(session):
    """Fix autosummary generated files."""
    scripts_dir = Path("scripts")
    
    # Run fix scripts
    fix_scripts = [
        "fix_generated_modules.py",
        "fix_autosummary_output.py"
    ]
    
    for script in fix_scripts:
        script_path = scripts_dir / script
        if script_path.exists():
            session.log(f"Running {script}...")
            session.run("python", str(script_path), external=True)
        else:
            session.log(f"Script not found: {script}")
    
    session.log("✅ Autosummary fixes applied")