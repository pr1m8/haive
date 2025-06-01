import webbrowser
from pathlib import Path

import nox

DOCS_SOURCE = "docs/source"
DOCS_BUILD = "docs/_build"
CONF_DIR = DOCS_SOURCE


@nox.session(name="docs")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation (static HTML only)."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")

    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-c",
        CONF_DIR,
        DOCS_SOURCE,
        DOCS_BUILD,
    )

    session.log(f"📚 Docs built to: {DOCS_BUILD}/index.html")


@nox.session(name="docs-live")
def live_docs(session: nox.Session) -> None:
    """Start live-reloading Sphinx server with sphinx-autobuild."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")

    session.run(
        "poetry",
        "run",
        "sphinx-autobuild",
        DOCS_SOURCE,
        DOCS_BUILD,
        "--host",
        "0.0.0.0",
        "--port",
        "8001",
        "--open-browser",
        "--watch",
        "README.md",
        "--ignore",
        DOCS_BUILD,
    )


@nox.session(name="view-docs")
def view_docs(session: nox.Session) -> None:
    """Open the built documentation in the default web browser."""
    index_path = Path(DOCS_BUILD) / "index.html"
    if not index_path.exists():
        session.error(f"{index_path} not found. Run `nox -s docs` first.")
    webbrowser.open(index_path.resolve().as_uri())
    session.log(f"📖 Opened docs at: {index_path}")
