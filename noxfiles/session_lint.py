"""Linting and code quality nox sessions."""

from __future__ import annotations

import nox


@nox.session(python="3.12")
def lint(session):
    """Run all linters."""
    session.log("🔍 Running linters...")

    session.run("poetry", "install", "--with", "dev", external=True)

    # Run ruff
    session.log("Running ruff...")
    session.run("poetry", "run", "ruff", "check", "packages/", external=True)

    # Run black check
    session.log("Running black...")
    session.run("poetry", "run", "black", "--check", "packages/", external=True)

    # Run isort check
    session.log("Running isort...")
    session.run("poetry", "run", "isort", "--check-only", "packages/", external=True)

    session.log("✅ All linters passed!")


@nox.session(python="3.12")
def format(session):
    """Format code with black and isort."""
    session.log("🎨 Formatting code...")

    session.run("poetry", "install", "--with", "dev", external=True)

    # Run black
    session.run("poetry", "run", "black", "packages/", external=True)

    # Run isort
    session.run("poetry", "run", "isort", "packages/", external=True)

    # Run ruff with fixes
    session.run("poetry", "run", "ruff", "check", "--fix", "packages/", external=True)

    session.log("✅ Code formatted!")


@nox.session(python="3.12")
def mypy(session):
    """Type check with mypy."""
    session.log("🔍 Running type checker...")

    session.run("poetry", "install", "--with", "dev", external=True)

    session.run(
        "poetry",
        "run",
        "mypy",
        "packages/haive-core/src",
        "packages/haive-agents/src",
        "--ignore-missing-imports",
        external=True,
    )

    session.log("✅ Type checking complete!")


@nox.session(python="3.12")
def security(session):
    """Run security checks with bandit."""
    session.log("🔒 Running security checks...")

    session.run("poetry", "install", "--with", "dev", external=True)

    session.run(
        "poetry",
        "run",
        "bandit",
        "-r",
        "packages/",
        "-ll",  # Only show medium and high severity issues
        external=True,
    )

    session.log("✅ Security check complete!")
