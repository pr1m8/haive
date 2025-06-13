import os
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path

import nox

DOCS_SOURCE = "docs/source"
DOCS_BUILD = "docs/_build"
CONF_DIR = DOCS_SOURCE
LOG_DIR = Path("logs/docs/build")


def get_log_path() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    return LOG_DIR / f"{timestamp}.log"


@nox.session(name="docs")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation (static HTML only) and log output."""
    session.install("poetry")
    session.run("poetry", "install", "--no-root", "--with", "docs")

    log_path = get_log_path()
    log_path.parent.mkdir(parents=True, exist_ok=True)

    session.log(f"🛠️  Building docs... Logging to {log_path}")

    cmd = [
        "poetry",
        "run",
        "sphinx-build",
        "-b",
        "html",
        "-c",
        CONF_DIR,
        DOCS_SOURCE,
        DOCS_BUILD,
    ]

    # Run the command and capture output
    with log_path.open("w", encoding="utf-8") as logfile:
        process = subprocess.run(cmd, stdout=logfile, stderr=subprocess.STDOUT)

    if process.returncode == 0:
        session.log("✅ Docs built successfully.")
    else:
        session.error("❌ Docs build failed. See log for details.")

    # Show summary of warnings/errors
    with log_path.open(encoding="utf-8") as logfile:
        lines = logfile.readlines()

    warnings = [line for line in lines if "WARNING" in line]
    errors = [line for line in lines if "ERROR" in line]

    if warnings:
        session.log(f"⚠️  {len(warnings)} warnings found:")
        for line in warnings:
            session.log(f"  - {line.strip()}")

    if errors:
        session.error(f"❌ {len(errors)} errors found during docs build.")

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
