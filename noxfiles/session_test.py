"""Testing-related nox sessions."""
from __future__ import annotations

import nox


@nox.session(python="3.12")
def test(session):
    """Run all tests."""
    session.log("🧪 Running tests...")

    session.run("poetry", "install", "--all-extras", external=True)

    session.run(
        "poetry",
        "run",
        "pytest",
        "-v",
        "--cov=haive",
        "--cov-report=html",
        "--cov-report=term",
        external=True,
    )

    session.log("✅ Tests complete!")


@nox.session(python="3.12")
def test_quick(session):
    """Run quick tests (no coverage)."""
    session.log("🏃 Running quick tests...")

    session.run("poetry", "install", external=True)

    session.run(
        "poetry",
        "run",
        "pytest",
        "-v",
        "-x",  # Stop on first failure
        "--no-cov",
        external=True,
    )


@nox.session(python="3.12")
def test_package(session):
    """Test a specific package."""
    if not session.posargs:
        session.error(
            "Please specify a package: nox -s test_package -- haive-agents")

    package = session.posargs[0]
    session.log(f"🧪 Testing {package}...")

    session.run("poetry", "install", "--all-extras", external=True)

    session.run(
        "poetry",
        "run",
        "pytest",
        f"packages/{package}/tests/",
        "-v",
        external=True,
    )


@nox.session(python="3.12")
def test_integration(session):
    """Run integration tests."""
    session.log("🔗 Running integration tests...")

    session.run("poetry", "install", "--all-extras", external=True)

    session.run(
        "poetry",
        "run",
        "pytest",
        "-v",
        "-m",
        "integration",
        "--tb=short",
        external=True,
    )
