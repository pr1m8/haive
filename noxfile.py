import nox

@nox.session
def docs(session):
    """Build the documentation."""
    session.install("-e", ".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-press-theme", 
                   "myst-parser", "sphinx-copybutton", "sphinx-tabs", "sphinx-design")
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")

@nox.session
def docs_live(session):
    """Build the documentation with live reloading."""
    session.install("-e", ".")
    session.install("sphinx", "sphinx-autobuild", "sphinx-press-theme", 
                   "myst-parser", "sphinx-copybutton", "sphinx-tabs", "sphinx-design")
    session.run("sphinx-autobuild", "-a", "--watch", "src", 
               "docs/source", "docs/build/html")
