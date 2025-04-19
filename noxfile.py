import nox


@nox.session(name="docs")
def build_docs(session: nox.Session) -> None:
    """Build the Sphinx documentation using Poetry."""
    session.install("poetry")

    # Install docs dependencies via poetry (assumes group 'docs' exists)
    session.run("poetry", "install", "--no-root", "--with", "docs")

    # Build docs
    session.run("poetry", "run", "sphinx-build", "docs", "docs/_build")


@nox.session(name="tests", python=["3.12"])
def run_tests(session: nox.Session) -> None:
    """Run pytest via poetry."""
    session.install("poetry")
    session.run("poetry", "install")
    session.run("poetry", "run", "pytest")
