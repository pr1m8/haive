"""Package-specific documentation builds using the main conf.py."""

from __future__ import annotations

from pathlib import Path

import nox

# Python versions to test
PYTHON_VERSIONS = ["3.12"]

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / "docs" / "source"
BUILD_DIR = PROJECT_ROOT / "docs" / "build"


@nox.session(python=PYTHON_VERSIONS, name="docs-package")
@nox.parametrize(
    "package",
    ["all", "core", "agents", "tools", "games", "mcp", "dataflow", "prebuilt"],
)
@nox.parametrize("profile", ["minimal", "standard", "full"])
def docs_package(session, package, profile):
    """Build documentation for specific package(s) with chosen profile.

    Examples:
        nox -s docs-package-all-full          # Full build (default)
        nox -s docs-package-core-minimal      # Fast core-only build
        nox -s docs-package-agents-standard   # Standard agents build

    You can also build multiple packages:
        SPHINX_PACKAGES=core,agents nox -s docs-package-all-minimal
    """
    # Using poetry environment - dependencies already installed

    # Set environment variables
    env = {
        "SPHINX_PACKAGES": package,
        "SPHINX_PROFILE": profile,
    }

    # Build directory name
    if package == "all":
        build_name = f"all_{profile}"
    else:
        build_name = f"{package}_{profile}"

    output_dir = BUILD_DIR / build_name

    session.log(f"📦 Building: {package} ({profile} profile)")
    session.log(f"📁 Output: {output_dir}")

    # Run sphinx-build using poetry environment (like docs_phased)
    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        "-E",  # Don't use saved environment
        "-W",
        "--keep-going",  # Treat warnings as errors but show all
        env=env,
        external=True,  # Use external poetry environment
    )

    session.log(f"✅ Build complete: {output_dir}")
    session.log(f"📄 View: file://{output_dir}/index.html")


@nox.session(name="docs-quick")
@nox.parametrize("package", ["core", "agents", "tools"])
def docs_quick(session, package):
    """Quick minimal build for a single package.

    This is the fastest way to build docs during development.

    Examples:
        nox -s docs-quick-core
        nox -s docs-quick-agents
    """
    # Using poetry environment - dependencies already installed

    env = {
        "SPHINX_PACKAGES": package,
        "SPHINX_PROFILE": "minimal",
    }

    output_dir = BUILD_DIR / f"{package}_quick"

    session.log(f"⚡ Quick build: {package}")

    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        env=env,
        external=True,
    )

    session.log(f"✅ Done: file://{output_dir}/index.html")


@nox.session(name="docs-multi")
def docs_multi(session):
    """Build multiple packages specified via SPHINX_PACKAGES env var.

    Example:
        SPHINX_PACKAGES=core,agents,tools nox -s docs-multi
    """
    import os

    packages = os.environ.get("SPHINX_PACKAGES", "core,agents")
    profile = os.environ.get("SPHINX_PROFILE", "standard")

    # Using poetry environment - dependencies already installed

    env = {
        "SPHINX_PACKAGES": packages,
        "SPHINX_PROFILE": profile,
    }

    # Create output dir name from packages
    pkg_list = packages.replace(",", "-")
    output_dir = BUILD_DIR / f"multi_{pkg_list}_{profile}"

    session.log(f"📦 Building: {packages} ({profile} profile)")

    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        str(DOCS_DIR),
        str(output_dir),
        env=env,
        external=True,
    )

    session.log(f"✅ Done: file://{output_dir}/index.html")
