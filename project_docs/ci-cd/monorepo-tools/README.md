# Monorepo Tools for Python

**Last Updated**: 2025-01-11

## Overview

Monorepo tools help manage multiple related projects within a single repository. For Python projects in 2024, the landscape includes specialized build systems like Pants and Bazel, as well as patterns for using traditional tools like Poetry in a monorepo setup.

## 🏗️ Key Monorepo Tools

### Pants Build (Python-Focused)

**What it is**: A fast, scalable build system specifically designed for Python monorepos, with support for fine-grained dependency management and caching.

**Key Features**:

- Fine-grained dependency tracking
- Incremental builds and test runs
- Built-in support for Python, with plugins for other languages
- Advanced caching to skip unchanged code
- Parallel execution by default

**Project Structure**:

```
monorepo/
├── pants.toml                 # Global Pants configuration
├── BUILD                      # Root BUILD file
├── 3rdparty/
│   └── python/
│       ├── BUILD
│       └── requirements.txt   # External dependencies
├── packages/
│   ├── core/
│   │   ├── BUILD
│   │   ├── src/
│   │   │   └── core/
│   │   │       ├── __init__.py
│   │   │       └── models.py
│   │   └── tests/
│   │       └── test_models.py
│   ├── api/
│   │   ├── BUILD
│   │   ├── src/
│   │   └── tests/
│   └── cli/
│       ├── BUILD
│       ├── src/
│       └── tests/
└── tools/
    └── scripts/
```

**Configuration Example**:

```toml
# pants.toml
[GLOBAL]
pants_version = "2.19.0"
backend_packages = [
    "pants.backend.python",
    "pants.backend.python.lint.black",
    "pants.backend.python.lint.ruff",
    "pants.backend.python.typecheck.mypy",
    "pants.backend.python.mixed_interpreter_constraints",
    "pants.backend.docker",
    "pants.backend.shell",
]

[anonymous-telemetry]
enabled = false

[source]
root_patterns = [
    "/packages/*/src",
    "/packages/*/tests",
    "/tools",
]

[python]
interpreter_constraints = [">=3.9,<3.12"]
enable_resolves = true

[python.resolves]
python-default = "3rdparty/python/default.lock"
data-science = "3rdparty/python/data-science.lock"
web = "3rdparty/python/web.lock"

[python-infer]
use_rust_parser = true

[test]
use_coverage = true

[coverage-py]
report = ["xml", "html", "console"]
global_report = true
```

**BUILD File Examples**:

```python
# packages/core/BUILD
python_sources(
    name="lib",
    sources=["src/core/**/*.py"],
    dependencies=[
        "//:reqs#pydantic",
        "//:reqs#httpx",
    ],
)

python_tests(
    name="tests",
    sources=["tests/**/*_test.py"],
    dependencies=[
        ":lib",
        "//:reqs#pytest",
        "//:reqs#pytest-asyncio",
    ],
)

pex_binary(
    name="cli",
    entry_point="src/core/cli.py",
    dependencies=[":lib"],
)

# packages/api/BUILD
python_sources(
    name="lib",
    sources=["src/api/**/*.py"],
    dependencies=[
        "//packages/core:lib",
        "//:reqs#fastapi",
        "//:reqs#uvicorn",
    ],
)

docker_image(
    name="docker",
    dependencies=[":lib"],
    image_tags=["api:latest"],
)
```

**Common Commands**:

```bash
# Run all tests
pants test ::

# Run tests for a specific package
pants test packages/core::

# Format all code
pants fmt ::

# Lint all code
pants lint ::

# Type check
pants check ::

# Build all packages
pants package ::

# Generate lockfiles
pants generate-lockfiles

# Show dependencies
pants dependencies packages/api:lib

# Run specific binary
pants run packages/core:cli -- --help
```

### Bazel (Multi-Language)

**What it is**: Google's build tool that emphasizes correctness, reproducibility, and scalability across multiple languages.

**Key Features**:

- Language-agnostic with Python support
- Hermetic builds (fully reproducible)
- Remote caching and execution
- Strict dependency declaration

**Example BUILD file**:

```python
# BUILD.bazel
load("@rules_python//python:defs.bzl", "py_library", "py_test", "py_binary")

py_library(
    name = "mylib",
    srcs = glob(["src/**/*.py"]),
    deps = [
        "@pip//pydantic",
        "@pip//httpx",
    ],
    visibility = ["//visibility:public"],
)

py_test(
    name = "mylib_test",
    srcs = glob(["tests/**/*_test.py"]),
    deps = [
        ":mylib",
        "@pip//pytest",
    ],
)

py_binary(
    name = "app",
    srcs = ["src/main.py"],
    deps = [":mylib"],
)
```

### Poetry Workspaces (Monorepo Pattern)

**What it is**: Using Poetry's path dependencies and workspace features to manage a monorepo.

**Project Structure**:

```
monorepo/
├── pyproject.toml          # Root workspace
├── packages/
│   ├── core/
│   │   ├── pyproject.toml
│   │   └── src/
│   ├── api/
│   │   ├── pyproject.toml
│   │   └── src/
│   └── shared/
│       ├── pyproject.toml
│       └── src/
└── apps/
    ├── web/
    │   ├── pyproject.toml
    │   └── src/
    └── cli/
        ├── pyproject.toml
        └── src/
```

**Root pyproject.toml**:

```toml
[tool.poetry]
name = "my-monorepo"
version = "0.0.0"
description = "Monorepo root"

[tool.poetry.dependencies]
python = "^3.9"

# Local packages as path dependencies
core = {path = "packages/core", develop = true}
api = {path = "packages/api", develop = true}
shared = {path = "packages/shared", develop = true}
web-app = {path = "apps/web", develop = true}
cli-app = {path = "apps/cli", develop = true}

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
black = "^24.0"
ruff = "^0.1"
mypy = "^1.7"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

**Package-level pyproject.toml**:

```toml
# packages/api/pyproject.toml
[tool.poetry]
name = "api"
version = "0.1.0"
description = "API package"

[tool.poetry.dependencies]
python = "^3.9"
core = {path = "../core", develop = true}
shared = {path = "../shared", develop = true}
fastapi = "^0.104.0"
uvicorn = "^0.24.0"
```

### Nx (with Python Plugin)

**What it is**: A build system focused on monorepo management with a Python plugin.

**Configuration**:

```json
// nx.json
{
  "tasksRunnerOptions": {
    "default": {
      "runner": "nx/tasks-runners/default",
      "options": {
        "cacheableOperations": ["build", "test", "lint"]
      }
    }
  },
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

## 📊 Comparison Matrix

| Feature            | Pants        | Bazel        | Poetry Workspaces | Nx        |
| ------------------ | ------------ | ------------ | ----------------- | --------- |
| Python-specific    | ✅ Excellent | ✅ Good      | ✅ Native         | ✅ Plugin |
| Learning curve     | Medium       | High         | Low               | Medium    |
| Build caching      | ✅ Advanced  | ✅ Advanced  | ❌ None           | ✅ Good   |
| Incremental builds | ✅ Automatic | ✅ Automatic | ❌ Manual         | ✅ Good   |
| Dependency graph   | ✅ Automatic | ✅ Explicit  | ⚠️ Limited        | ✅ Good   |
| Multi-language     | ✅ Good      | ✅ Excellent | ❌ Python only    | ✅ Good   |
| IDE support        | ✅ Good      | ⚠️ Limited   | ✅ Excellent      | ✅ Good   |
| Community          | Growing      | Large        | Large             | Growing   |

## 🔧 Integration Patterns

### CI/CD with Pants

```yaml
# .github/workflows/pants.yml
name: Pants CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4

    - uses: pantsbuild/actions/init-pants@v5
      with:
        pants-python-version: "3.11"

    - name: Cache Pants
      uses: actions/cache@v4
      with:
        path: |
          ~/.cache/pants/setup
          ~/.cache/pants/lmdb_store
          ~/.cache/pants/named_caches
        key: ${{ runner.os }}-pants-${{ hashFiles('pants.lock') }}

    - name: Check BUILD files
      run: pants tailor --check update-build-files --check

    - name: Lint
      run: pants lint ::

    - name: Test
      run: pants test ::

    - name: Package
      run: pants package ::
```

### Dependency Management

```python
# scripts/sync_deps.py
"""Sync dependencies across monorepo packages."""
import toml
from pathlib import Path
from typing import Dict, Set

def collect_all_deps(root: Path) -> Dict[str, Set[str]]:
    """Collect all dependencies from all packages."""
    all_deps = {}

    for pyproject in root.glob("**/pyproject.toml"):
        if "node_modules" in str(pyproject):
            continue

        config = toml.load(pyproject)
        if "tool" in config and "poetry" in config["tool"]:
            deps = config["tool"]["poetry"].get("dependencies", {})
            for dep, version in deps.items():
                if dep == "python":
                    continue
                if isinstance(version, dict) and "path" in version:
                    continue  # Skip local deps

                if dep not in all_deps:
                    all_deps[dep] = set()
                all_deps[dep].add(str(version))

    return all_deps

def find_conflicts(all_deps: Dict[str, Set[str]]) -> Dict[str, Set[str]]:
    """Find dependencies with conflicting versions."""
    conflicts = {}

    for dep, versions in all_deps.items():
        if len(versions) > 1:
            conflicts[dep] = versions

    return conflicts

# Usage
root = Path(".")
deps = collect_all_deps(root)
conflicts = find_conflicts(deps)

if conflicts:
    print("Version conflicts found:")
    for dep, versions in conflicts.items():
        print(f"  {dep}: {versions}")
```

### Shared Configuration

```python
# packages/shared/build_config.py
"""Shared build configuration for all packages."""
from pathlib import Path

class BuildConfig:
    """Shared configuration for monorepo packages."""

    # Common dependencies versions
    PYTHON_VERSION = ">=3.9,<3.12"
    PYDANTIC_VERSION = "^2.5"
    PYTEST_VERSION = "^7.4"

    # Common paths
    ROOT_DIR = Path(__file__).parent.parent.parent
    PACKAGES_DIR = ROOT_DIR / "packages"

    # Shared tool configs
    BLACK_CONFIG = {
        "line-length": 88,
        "target-version": ["py39", "py310", "py311"]
    }

    RUFF_CONFIG = {
        "line-length": 88,
        "select": ["E", "F", "I", "N", "UP", "B", "C4"]
    }

    @classmethod
    def get_package_config(cls, package_name: str) -> dict:
        """Get configuration for a specific package."""
        base_config = {
            "tool": {
                "black": cls.BLACK_CONFIG,
                "ruff": cls.RUFF_CONFIG,
            }
        }

        # Package-specific overrides
        if package_name == "api":
            base_config["tool"]["ruff"]["ignore"] = ["E501"]

        return base_config
```

## 🎯 Best Practices

### 1. Dependency Management

- **Centralize versions**: Keep dependency versions in one place
- **Use lockfiles**: Generate and commit lockfiles for reproducibility
- **Regular updates**: Automate dependency updates with tools like Renovate
- **Conflict detection**: Regularly check for version conflicts

### 2. Code Sharing

```python
# Good: Explicit imports from shared packages
from shared.models import BaseModel
from core.utils import process_data

# Bad: Relative imports across packages
from ../../../shared/models import BaseModel
```

### 3. Testing Strategy

- **Unit tests**: Each package tests its own code
- **Integration tests**: Separate package for cross-package tests
- **Test isolation**: Tests shouldn't depend on other packages' tests

### 4. Build Optimization

- **Incremental builds**: Only rebuild what changed
- **Parallel execution**: Run independent tasks in parallel
- **Remote caching**: Share build cache across team
- **Selective testing**: Only test affected packages

## 📚 Advanced Patterns

### Dynamic Package Discovery

```python
# scripts/discover_packages.py
"""Dynamically discover packages in monorepo."""
from pathlib import Path
import json

def discover_packages(root: Path) -> list:
    """Find all packages with pyproject.toml."""
    packages = []

    for pyproject in root.glob("**/pyproject.toml"):
        # Skip root and virtual environments
        if pyproject.parent == root:
            continue
        if ".venv" in str(pyproject):
            continue

        rel_path = pyproject.parent.relative_to(root)
        packages.append({
            "name": pyproject.parent.name,
            "path": str(rel_path),
            "type": "library" if "packages" in str(rel_path) else "app"
        })

    return packages

# Generate package manifest
packages = discover_packages(Path("."))
with open("packages.json", "w") as f:
    json.dump(packages, f, indent=2)
```

### Cross-Package Testing

```python
# tests/integration/test_cross_package.py
"""Test interactions between packages."""
import pytest
from core.service import CoreService
from api.handler import APIHandler

@pytest.fixture
def core_service():
    """Provide configured core service."""
    return CoreService(config={"test": True})

def test_api_uses_core_service(core_service):
    """Test API handler correctly uses core service."""
    handler = APIHandler(service=core_service)
    result = handler.process_request({"data": "test"})
    assert result["status"] == "success"
    assert core_service.was_called
```

### Monorepo Tooling

```python
# tools/monorepo.py
"""CLI tool for monorepo management."""
import click
from pathlib import Path
import subprocess

@click.group()
def cli():
    """Monorepo management tool."""
    pass

@cli.command()
@click.argument("package")
def test(package: str):
    """Run tests for a specific package."""
    cmd = ["pants", "test", f"packages/{package}::"]
    subprocess.run(cmd, check=True)

@cli.command()
@click.option("--changed-only", is_flag=True)
def lint(changed_only: bool):
    """Run linting."""
    target = "--changed-since=origin/main" if changed_only else "::"
    cmd = ["pants", "lint", target]
    subprocess.run(cmd, check=True)

@cli.command()
def deps():
    """Show dependency graph."""
    cmd = ["pants", "dependencies", "--transitive", "::"]
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    cli()
```

## 🚀 Migration Strategy

### From Multiple Repos to Monorepo

1. **Inventory**: List all repositories and dependencies
2. **Structure**: Design package hierarchy
3. **Dependencies**: Resolve version conflicts
4. **Migration**: Move code preserving history
5. **CI/CD**: Update pipelines for monorepo
6. **Documentation**: Update for new structure

### Gradual Adoption

```bash
# Start with shared code
mkdir -p packages/shared
git subtree add --prefix=packages/shared https://github.com/org/shared-lib.git main

# Add more packages gradually
git subtree add --prefix=packages/core https://github.com/org/core-lib.git main

# Update imports and dependencies
# Test thoroughly before removing old repos
```

## 📈 Performance Tips

1. **Use build caching**: Configure remote cache for CI/CD
2. **Parallelize**: Run independent tasks concurrently
3. **Incremental testing**: Only test changed packages
4. **Optimize imports**: Minimize cross-package dependencies
5. **Profile builds**: Identify and fix bottlenecks

## 🔗 Resources

- [Pants Documentation](https://www.pantsbuild.org/)
- [Bazel Python Rules](https://github.com/bazelbuild/rules_python)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Monorepo.tools](https://monorepo.tools/)
- [Nx Python Plugin](https://nx.dev/packages/nx-python)
