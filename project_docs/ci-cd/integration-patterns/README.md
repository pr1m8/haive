# Integration Patterns for Python CI/CD

**Last Updated**: 2025-01-11

## Overview

This guide covers how different CI/CD tools integrate together to create comprehensive automation workflows for Python projects. We'll explore practical patterns for combining task runners, pre-commit hooks, package managers, and CI/CD platforms.

## 🔄 Common Integration Stacks

### Modern Stack (2024 Recommended)

```yaml
# The "Fast and Modern" Stack
Package Manager: UV (20x faster than pip)
Task Runner: Just (simple, cross-platform)
Quality Tools: Ruff + Black + mypy
Testing: pytest + Nox (for matrix testing)
Pre-commit: pre-commit framework
CI/CD: GitHub Actions
Monorepo: Pants (if needed)
```

### Traditional Stack

```yaml
# The "Established" Stack
Package Manager: Poetry
Task Runner: Make or Invoke
Quality Tools: Flake8 + Black + mypy
Testing: pytest + Tox
Pre-commit: pre-commit framework
CI/CD: GitHub Actions / GitLab CI
```

## 📊 Integration Examples

### 1. UV + Just + Pre-commit

**Project Structure:**

```
project/
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── release.yml
├── src/
│   └── my_package/
├── tests/
├── .pre-commit-config.yaml
├── justfile
├── pyproject.toml
└── README.md
```

**justfile:**

```make
# Default recipe shows help
default:
    @just --list

# Install dependencies with UV
install:
    uv pip install -e ".[dev]"
    pre-commit install

# Run tests
test:
    uv run pytest tests/ -v

# Run tests with coverage
test-cov:
    uv run pytest tests/ --cov=src --cov-report=html

# Run all quality checks
quality:
    uv run ruff check .
    uv run black --check .
    uv run mypy src/

# Auto-fix quality issues
fix:
    uv run ruff check --fix .
    uv run black .

# Run pre-commit on all files
pre-commit:
    pre-commit run --all-files

# Build the package
build:
    uv pip install build
    uv run python -m build

# Clean build artifacts
clean:
    rm -rf dist/ build/ *.egg-info
    find . -type d -name __pycache__ -exec rm -rf {} +
    find . -type f -name "*.pyc" -delete

# Full CI simulation
ci: clean install quality test

# Bump version (major, minor, patch)
bump version:
    @echo "Current version: $(uv run python -c 'import toml; print(toml.load("pyproject.toml")["project"]["version"])')"
    uv run bumpver update --{{version}}

# Create a new release
release: quality test build
    @echo "Ready to release!"
    @echo "Don't forget to:"
    @echo "  1. Update CHANGELOG.md"
    @echo "  2. Commit changes"
    @echo "  3. Tag the release"
    @echo "  4. Push to GitHub"
```

**GitHub Actions Integration:**

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install UV
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install Just
        uses: extractions/setup-just@v1

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache UV packages
        uses: actions/cache@v4
        with:
          path: ~/.cache/uv
          key: ${{ runner.os }}-uv-${{ hashFiles('**/pyproject.toml') }}

      - name: Install dependencies
        run: just install

      - name: Run quality checks
        run: just quality

      - name: Run tests
        run: just test-cov

      - name: Upload coverage
        uses: codecov/codecov-action@v4
```

### 2. Poetry + Nox + Pre-commit

**noxfile.py:**

```python
import nox
from nox.sessions import Session

# Define Python versions to test
PYTHON_VERSIONS = ["3.9", "3.10", "3.11", "3.12"]

@nox.session(python=PYTHON_VERSIONS)
def tests(session: Session) -> None:
    """Run the test suite."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("pytest", "--cov=src", "--cov-report=xml")

@nox.session(python="3.11")
def lint(session: Session) -> None:
    """Run linters."""
    args = session.posargs or ["src", "tests", "noxfile.py"]
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("ruff", "check", *args)
    session.run("black", "--check", *args)
    session.run("mypy", *args)

@nox.session(python="3.11")
def format(session: Session) -> None:
    """Format code."""
    args = session.posargs or ["src", "tests", "noxfile.py"]
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("black", *args)
    session.run("ruff", "check", "--fix", *args)

@nox.session(python="3.11")
def docs(session: Session) -> None:
    """Build documentation."""
    session.run("poetry", "install", "--with", "docs", external=True)
    session.run("sphinx-build", "docs", "docs/_build")

@nox.session(python="3.11")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    session.run("poetry", "install", "--with", "dev", external=True)
    session.run("coverage", "xml")
    session.run("codecov")
```

**Integration with Makefile:**

```makefile
.PHONY: install test lint format docs clean

install:
	poetry install --with dev
	pre-commit install

test:
	nox -s tests

test-all:
	nox

lint:
	nox -s lint

format:
	nox -s format

docs:
	nox -s docs

pre-commit:
	pre-commit run --all-files

clean:
	rm -rf .nox/ .pytest_cache/ .coverage coverage.xml htmlcov/
	find . -type d -name __pycache__ -exec rm -rf {} +
```

### 3. Monorepo with Pants

**pants.toml:**

```toml
[GLOBAL]
pants_version = "2.19.0"
backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.black",
    "pants.backend.python.lint.ruff",
    "pants.backend.python.typecheck.mypy",
    "pants.backend.python.mixed_interpreter_constraints",
]

[source]
root_patterns = [
    "/packages/*",
    "/libs/*",
    "/tools/*",
]

[python]
interpreter_constraints = [">=3.9,<3.12"]
enable_resolves = true

[python.resolves]
python-default = "3rdparty/python/default.lock"
data-science = "3rdparty/python/data-science.lock"

[test]
use_coverage = true

[coverage-py]
report = ["xml", "html", "console"]
```

**BUILD files for packages:**

```python
# packages/core/BUILD
python_sources(
    name="src",
    dependencies=[
        "//:reqs#pydantic",
        "//:reqs#httpx",
    ],
)

python_tests(
    name="tests",
    dependencies=[
        ":src",
        "//:reqs#pytest",
    ],
)

# packages/api/BUILD
python_sources(
    name="src",
    dependencies=[
        "//packages/core:src",
        "//:reqs#fastapi",
    ],
)
```

**Integration with Just:**

```make
# Pants + Just integration
# Run all tests
test:
    pants test ::

# Run specific package tests
test-package package:
    pants test packages/{{package}}::

# Format all code
fmt:
    pants fmt ::

# Lint all code
lint:
    pants lint ::

# Type check
typecheck:
    pants check ::

# Build all packages
build:
    pants package ::

# Run REPL with dependencies
repl package:
    pants repl packages/{{package}}:src
```

## 🎯 Advanced Integration Patterns

### Multi-Stage Docker Builds with CI

```dockerfile
# Dockerfile
# Stage 1: Build environment
FROM python:3.11-slim as builder

RUN pip install uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen

# Stage 2: Test environment
FROM builder as tester

COPY . .
RUN uv run pytest tests/

# Stage 3: Production
FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
COPY src/ ./src/

ENV PATH="/app/.venv/bin:$PATH"
CMD ["python", "-m", "my_app"]
```

**GitHub Action for Docker:**

```yaml
name: Docker Build

on:
  push:
    branches: [main]
    tags: ["v*"]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to DockerHub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USERNAME }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}

      - name: Build and test
        uses: docker/build-push-action@v5
        with:
          context: .
          target: tester
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: user/app:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### Automated Dependency Updates

**renovate.json:**

```json
{
  "extends": ["config:base"],
  "python": {
    "packageRules": [
      {
        "matchPackagePatterns": ["*"],
        "rangeStrategy": "pin"
      }
    ]
  },
  "poetry": {
    "enabled": true
  },
  "pip-compile": {
    "enabled": true
  },
  "github-actions": {
    "enabled": true
  },
  "pre-commit": {
    "enabled": true
  },
  "schedule": ["every weekend"],
  "automerge": true,
  "automergeType": "pr",
  "platformAutomerge": true
}
```

### Performance Optimization Pattern

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmark

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install uv
          uv sync

      - name: Run benchmarks
        run: |
          uv run pytest tests/benchmarks/ --benchmark-json=new.json

      - name: Compare with main
        run: |
          git checkout main
          uv sync
          uv run pytest tests/benchmarks/ --benchmark-json=old.json
          uv run pytest-benchmark compare old.json new.json --fail-on-performance-regression
```

## 🔧 Tool-Specific Integrations

### Pre-commit with Multiple Tools

```yaml
# .pre-commit-config.yaml
repos:
  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  # Fast Python linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix]

  # Security scanning
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: [-r, src/]

  # Dockerfile linting
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint

  # YAML/JSON validation
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: check-json
      - id: check-toml

  # Custom local hooks
  - repo: local
    hooks:
      - id: pytest-check
        name: pytest-check
        entry: uv run pytest
        language: system
        pass_filenames: false
        always_run: true
```

### Nox + Tox Migration

```python
# Convert from tox.ini to noxfile.py
# Old tox.ini:
# [tox]
# envlist = py{39,310,311}, lint, docs

# New noxfile.py:
import nox

@nox.session(python=["3.9", "3.10", "3.11"])
def tests(session):
    """Run tests (replaces tox testenv)."""
    session.install(".[test]")
    session.run("pytest")

@nox.session
def lint(session):
    """Run linting (replaces tox env:lint)."""
    session.install(".[lint]")
    session.run("ruff", "check", ".")

@nox.session
def docs(session):
    """Build docs (replaces tox env:docs)."""
    session.install(".[docs]")
    session.run("sphinx-build", "docs", "docs/_build")

# Backwards compatibility
@nox.session
def tox_to_nox(session):
    """Help migrate from tox."""
    session.log("Tox envlist mapping:")
    session.log("  py39,py310,py311 -> nox -s tests")
    session.log("  lint -> nox -s lint")
    session.log("  docs -> nox -s docs")
```

## 📈 Monitoring and Reporting

### Integration Dashboard

```python
# scripts/ci_dashboard.py
"""Generate CI/CD metrics dashboard."""
import json
from pathlib import Path
from datetime import datetime, timedelta
import requests

class CIDashboard:
    def __init__(self, repo: str, token: str):
        self.repo = repo
        self.headers = {"Authorization": f"token {token}"}

    def get_workflow_stats(self, days: int = 30):
        """Get workflow statistics."""
        since = (datetime.now() - timedelta(days=days)).isoformat()

        url = f"https://api.github.com/repos/{self.repo}/actions/runs"
        params = {"created": f">{since}"}

        response = requests.get(url, headers=self.headers, params=params)
        runs = response.json()["workflow_runs"]

        stats = {
            "total_runs": len(runs),
            "success_rate": sum(1 for r in runs if r["conclusion"] == "success") / len(runs),
            "average_duration": sum(r["duration"] for r in runs) / len(runs),
        }

        return stats

    def generate_report(self):
        """Generate HTML report."""
        stats = self.get_workflow_stats()

        html = f"""
        <html>
        <head><title>CI/CD Dashboard</title></head>
        <body>
            <h1>CI/CD Metrics</h1>
            <p>Total Runs: {stats['total_runs']}</p>
            <p>Success Rate: {stats['success_rate']:.1%}</p>
            <p>Avg Duration: {stats['average_duration']:.1f}s</p>
        </body>
        </html>
        """

        Path("ci_dashboard.html").write_text(html)
```

## 🚀 Best Practices

1. **Start Simple**: Don't over-engineer; add complexity as needed
2. **Cache Aggressively**: Cache dependencies, build artifacts, test results
3. **Fail Fast**: Run quick checks (formatting, linting) before slow tests
4. **Parallelize**: Run independent jobs in parallel
5. **Monitor Performance**: Track CI times and optimize bottlenecks
6. **Document Integration**: Clear README on how tools work together
7. **Version Lock**: Use lock files for reproducible builds
8. **Automate Everything**: If you do it twice, automate it
