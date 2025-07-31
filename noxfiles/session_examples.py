"""Example-related nox sessions."""

from pathlib import Path

import nox


@nox.session(python="3.12")
def examples(session):
    """Run all examples."""
    session.log("🚀 Running examples...")

    session.run("poetry", "install", "--all-extras", external=True)

    # Find all example files
    example_files = list(Path("examples").glob("*.py"))

    for example in example_files:
        session.log(f"Running {example.name}...")
        try:
            session.run("poetry", "run", "python", str(example), external=True)
            session.log(f"✓ {example.name} completed")
        except Exception as e:
            session.warn(f"✗ {example.name} failed: {e}")


@nox.session(python="3.12")
def validate_examples(session):
    """Validate that examples have proper imports and syntax."""
    session.log("🔍 Validating examples...")

    session.run("poetry", "install", "--with", "dev", external=True)

    # Check syntax with ruff
    session.run("poetry", "run", "ruff", "check", "examples/", external=True)

    # Check imports
    example_files = list(Path("examples").glob("*.py"))

    for example in example_files:
        session.log(f"Checking {example.name}...")
        session.run(
            "poetry", "run", "python", "-m", "py_compile", str(example), external=True
        )

    session.log("✅ All examples validated!")


@nox.session(python="3.12")
def run_example(session):
    """Run a specific example."""
    if not session.posargs:
        session.error(
            "Please specify an example: nox -s run_example -- simple_agent.py"
        )

    example = session.posargs[0]
    example_path = Path("examples") / example

    if not example_path.exists():
        session.error(f"Example not found: {example_path}")

    session.log(f"🚀 Running {example}...")

    session.run("poetry", "install", "--all-extras", external=True)
    session.run("poetry", "run", "python", str(example_path), external=True)


@nox.session(python="3.12")
def examples_simple(session):
    """Run SimpleAgent examples only."""
    session.log("🤖 Running SimpleAgent examples...")

    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)

    # Run agent-specific examples
    session.run(
        "poetry",
        "run",
        "python",
        "run_agent_examples.py",
        "--agent",
        "SimpleAgent",
        "--visualize",
        external=True,
    )


@nox.session(python="3.12")
def examples_react(session):
    """Run ReactAgent examples only."""
    session.log("🧠 Running ReactAgent examples...")

    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)

    # Run agent-specific examples
    session.run(
        "poetry",
        "run",
        "python",
        "run_agent_examples.py",
        "--agent",
        "ReactAgent",
        "--visualize",
        external=True,
    )


@nox.session(python="3.12")
def examples_rag(session):
    """Run RAG agent examples only."""
    session.log("📚 Running RAG agent examples...")

    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)

    # Run agent-specific examples
    session.run(
        "poetry",
        "run",
        "python",
        "run_agent_examples.py",
        "--agent",
        "RAGAgent",
        "--visualize",
        external=True,
    )


@nox.session(python="3.12")
def examples_docs(session):
    """Generate examples for documentation."""
    session.log("📚 Generating examples for documentation...")

    # Install dependencies
    session.run("poetry", "install", "--all-extras", external=True)

    # Change to docs directory and run docs example generator
    session.chdir("docs")
    session.run("poetry", "run", "python", "run_examples_for_docs.py", external=True)
