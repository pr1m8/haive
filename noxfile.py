import nox


@nox.session(name="docs")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation using Poetry."""
    session.install("poetry")

    # Install doc dependencies
    session.run("poetry", "install", "--no-root", "--with", "docs")

    # Optional: Specify conf.py location if it's not in 'docs/'
    # Use `-c` to point to the folder containing conf.py
    sphinx_source_dir = "docs/source"  # ← your restructured source folder
    sphinx_build_dir = "docs/_build"  # ← output directory
    conf_dir = sphinx_source_dir  # ← where conf.py lives

    session.run(
        "poetry",
        "run",
        "sphinx-build",
        "-c",
        conf_dir,
        sphinx_source_dir,
        sphinx_build_dir,
    )


@nox.session(name="tests", python=["3.12"])
def run_tests(session: nox.Session) -> None:
    """Run pytest via poetry."""
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "pytest")
