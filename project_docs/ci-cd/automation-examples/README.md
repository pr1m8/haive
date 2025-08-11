# Python Automation Examples

**Last Updated**: 2025-01-11

## Overview

This directory contains practical examples of automation patterns for Python projects, including configuration syncing, automated workflows, and tool integrations.

## 📁 Example Projects

### 1. Configuration Sync System

Based on your documentation sync system, here's a generalized configuration syncing framework:

```python
# sync_framework.py
"""
Generalized sync framework for managing shared configurations across packages.
"""
import json
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod
import toml
import yaml

@dataclass
class SyncConfig:
    """Configuration for sync operations."""
    source_dir: Path
    target_pattern: str
    file_patterns: List[str]
    exclude_patterns: List[str] = None
    transform_rules: Dict[str, Any] = None
    dry_run: bool = False

class ConfigTransformer(ABC):
    """Abstract base for configuration transformers."""

    @abstractmethod
    def transform(self, content: str, metadata: Dict[str, Any]) -> str:
        """Transform configuration content."""
        pass

class TemplateTransformer(ConfigTransformer):
    """Transform configurations using template substitution."""

    def __init__(self, variables: Dict[str, Any]):
        self.variables = variables

    def transform(self, content: str, metadata: Dict[str, Any]) -> str:
        """Replace template variables."""
        for key, value in self.variables.items():
            content = content.replace(f"{{{{ {key} }}}}", str(value))
        return content

class ConfigSyncer:
    """Sync configurations across multiple packages."""

    def __init__(self, root_dir: Path, config: SyncConfig):
        self.root_dir = root_dir
        self.config = config
        self.transformers: List[ConfigTransformer] = []

    def add_transformer(self, transformer: ConfigTransformer):
        """Add a configuration transformer."""
        self.transformers.append(transformer)

    def find_targets(self) -> List[Path]:
        """Find target directories matching pattern."""
        targets = []
        pattern = self.config.target_pattern

        for path in self.root_dir.glob(pattern):
            if path.is_dir():
                # Check exclusions
                if self.config.exclude_patterns:
                    excluded = any(
                        path.match(exclude)
                        for exclude in self.config.exclude_patterns
                    )
                    if excluded:
                        continue
                targets.append(path)

        return sorted(targets)

    def sync_to_target(self, target: Path) -> Dict[str, Any]:
        """Sync configurations to a single target."""
        results = {
            "target": str(target),
            "synced_files": [],
            "errors": []
        }

        for pattern in self.config.file_patterns:
            for source_file in self.config.source_dir.glob(pattern):
                try:
                    dest_file = target / source_file.name

                    # Read source content
                    content = source_file.read_text()

                    # Apply transformations
                    metadata = {"target": target, "source": source_file}
                    for transformer in self.transformers:
                        content = transformer.transform(content, metadata)

                    # Write to destination
                    if not self.config.dry_run:
                        dest_file.parent.mkdir(parents=True, exist_ok=True)
                        dest_file.write_text(content)

                    results["synced_files"].append(str(dest_file))

                except Exception as e:
                    results["errors"].append({
                        "file": str(source_file),
                        "error": str(e)
                    })

        return results

    def sync_all(self) -> List[Dict[str, Any]]:
        """Sync to all targets."""
        targets = self.find_targets()
        results = []

        for target in targets:
            result = self.sync_to_target(target)
            results.append(result)

            if result["errors"]:
                print(f"❌ Errors syncing to {target}")
            else:
                print(f"✅ Synced {len(result['synced_files'])} files to {target}")

        return results

# Example usage script
def main():
    """Example sync workflow."""
    root = Path(".")

    # Configure sync operation
    config = SyncConfig(
        source_dir=root / "shared" / "configs",
        target_pattern="packages/*/",
        file_patterns=["*.toml", "*.yaml", ".pre-commit-config.yaml"],
        exclude_patterns=["*/test/*", "*/temp/*"]
    )

    # Create syncer
    syncer = ConfigSyncer(root, config)

    # Add package name transformer
    syncer.add_transformer(TemplateTransformer({
        "package_name": "{{ PACKAGE_NAME }}",
        "python_version": "3.11"
    }))

    # Run sync
    results = syncer.sync_all()

    # Save results
    with open("sync_results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
```

### 2. Multi-Tool Integration Workflow

```python
# automation_workflow.py
"""
Integrated automation workflow combining multiple tools.
"""
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional
import click
import toml

class AutomationWorkflow:
    """Orchestrate multiple automation tools."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load project configuration."""
        pyproject = self.project_root / "pyproject.toml"
        if pyproject.exists():
            return toml.load(pyproject)
        return {}

    def run_command(self, cmd: List[str], cwd: Optional[Path] = None) -> Tuple[int, str, str]:
        """Run a command and return exit code, stdout, stderr."""
        result = subprocess.run(
            cmd,
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True
        )
        return result.returncode, result.stdout, result.stderr

    def run_quality_checks(self) -> bool:
        """Run all quality checks."""
        checks = [
            ("Format check", ["just", "format-check"]),
            ("Lint", ["just", "lint"]),
            ("Type check", ["just", "type-check"]),
            ("Security scan", ["just", "security"]),
        ]

        all_passed = True

        for name, cmd in checks:
            print(f"\n🔍 Running {name}...")
            code, stdout, stderr = self.run_command(cmd)

            if code != 0:
                print(f"❌ {name} failed!")
                if stderr:
                    print(stderr)
                all_passed = False
            else:
                print(f"✅ {name} passed!")

        return all_passed

    def run_tests(self, coverage: bool = True) -> bool:
        """Run test suite."""
        print("\n🧪 Running tests...")

        cmd = ["nox", "-s", "tests"]
        if coverage:
            cmd.extend(["--", "--cov"])

        code, stdout, stderr = self.run_command(cmd)
        print(stdout)

        return code == 0

    def build_package(self) -> bool:
        """Build distribution package."""
        print("\n📦 Building package...")

        code, stdout, stderr = self.run_command(["poetry", "build"])
        if code == 0:
            print("✅ Package built successfully!")
            # List built files
            dist_dir = self.project_root / "dist"
            if dist_dir.exists():
                for file in dist_dir.iterdir():
                    print(f"  - {file.name}")
        else:
            print("❌ Build failed!")
            print(stderr)

        return code == 0

    def prepare_release(self, version: str) -> bool:
        """Prepare a new release."""
        print(f"\n🚀 Preparing release {version}")

        steps = [
            ("Update version", ["poetry", "version", version]),
            ("Update changelog", ["python", "scripts/update_changelog.py", version]),
            ("Run quality checks", self.run_quality_checks),
            ("Run tests", self.run_tests),
            ("Build package", self.build_package),
        ]

        for step_name, step_action in steps:
            print(f"\n📋 {step_name}...")

            if callable(step_action):
                success = step_action()
            else:
                code, _, _ = self.run_command(step_action)
                success = code == 0

            if not success:
                print(f"❌ Release preparation failed at: {step_name}")
                return False

        print("\n✅ Release preparation complete!")
        print("\nNext steps:")
        print("  1. Review changes")
        print("  2. Commit with: git commit -am 'chore: release v{version}'")
        print("  3. Tag with: git tag -a v{version} -m 'Release v{version}'")
        print("  4. Push with: git push && git push --tags")

        return True

@click.group()
def cli():
    """Automation workflow CLI."""
    pass

@cli.command()
@click.option("--no-coverage", is_flag=True, help="Skip coverage reporting")
def test(no_coverage):
    """Run test suite."""
    workflow = AutomationWorkflow(Path.cwd())
    success = workflow.run_tests(coverage=not no_coverage)
    sys.exit(0 if success else 1)

@cli.command()
def quality():
    """Run quality checks."""
    workflow = AutomationWorkflow(Path.cwd())
    success = workflow.run_quality_checks()
    sys.exit(0 if success else 1)

@cli.command()
@click.argument("version")
def release(version):
    """Prepare a new release."""
    workflow = AutomationWorkflow(Path.cwd())
    success = workflow.prepare_release(version)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    cli()
```

### 3. Monorepo Package Manager

```python
# monorepo_manager.py
"""
Manage packages in a Python monorepo.
"""
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Set
import networkx as nx
import click

class Package:
    """Represent a package in the monorepo."""

    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load package configuration."""
        pyproject = self.path / "pyproject.toml"
        if pyproject.exists():
            import toml
            return toml.load(pyproject)
        return {}

    @property
    def dependencies(self) -> Set[str]:
        """Get internal dependencies."""
        deps = set()

        poetry_deps = self.config.get("tool", {}).get("poetry", {}).get("dependencies", {})
        for dep, spec in poetry_deps.items():
            if isinstance(spec, dict) and "path" in spec:
                # Internal dependency
                dep_name = Path(spec["path"]).name
                deps.add(dep_name)

        return deps

    @property
    def version(self) -> str:
        """Get package version."""
        return self.config.get("tool", {}).get("poetry", {}).get("version", "0.0.0")

class MonorepoManager:
    """Manage monorepo operations."""

    def __init__(self, root: Path):
        self.root = root
        self.packages = self._discover_packages()
        self.dependency_graph = self._build_dependency_graph()

    def _discover_packages(self) -> Dict[str, Package]:
        """Discover all packages in the monorepo."""
        packages = {}

        for pyproject in self.root.glob("packages/*/pyproject.toml"):
            package = Package(pyproject.parent)
            packages[package.name] = package

        return packages

    def _build_dependency_graph(self) -> nx.DiGraph:
        """Build dependency graph."""
        graph = nx.DiGraph()

        # Add nodes
        for name, package in self.packages.items():
            graph.add_node(name, package=package)

        # Add edges
        for name, package in self.packages.items():
            for dep in package.dependencies:
                if dep in self.packages:
                    graph.add_edge(dep, name)  # dep -> package

        return graph

    def get_affected_packages(self, changed_packages: List[str]) -> Set[str]:
        """Get all packages affected by changes."""
        affected = set(changed_packages)

        # Add all dependents
        for package in changed_packages:
            if package in self.dependency_graph:
                descendants = nx.descendants(self.dependency_graph, package)
                affected.update(descendants)

        return affected

    def get_build_order(self) -> List[str]:
        """Get packages in build order."""
        try:
            return list(nx.topological_sort(self.dependency_graph))
        except nx.NetworkXUnfeasible:
            print("❌ Circular dependencies detected!")
            cycles = list(nx.simple_cycles(self.dependency_graph))
            for cycle in cycles:
                print(f"  Cycle: {' -> '.join(cycle)}")
            return []

    def run_command_on_packages(
        self,
        packages: List[str],
        command: List[str],
        parallel: bool = False
    ) -> Dict[str, bool]:
        """Run command on specified packages."""
        results = {}

        if parallel:
            # Use GNU parallel or similar
            # Simplified for example
            pass
        else:
            for package_name in packages:
                if package_name not in self.packages:
                    print(f"⚠️  Package '{package_name}' not found")
                    continue

                package = self.packages[package_name]
                print(f"\n📦 Running on {package_name}...")

                result = subprocess.run(
                    command,
                    cwd=package.path,
                    capture_output=True,
                    text=True
                )

                success = result.returncode == 0
                results[package_name] = success

                if success:
                    print(f"✅ {package_name}: Success")
                else:
                    print(f"❌ {package_name}: Failed")
                    if result.stderr:
                        print(result.stderr)

        return results

    def check_versions_sync(self) -> Dict[str, List[str]]:
        """Check for version conflicts across packages."""
        dep_versions = {}

        for package in self.packages.values():
            deps = package.config.get("tool", {}).get("poetry", {}).get("dependencies", {})

            for dep, version in deps.items():
                if dep == "python":
                    continue
                if isinstance(version, dict) and "path" in version:
                    continue

                if dep not in dep_versions:
                    dep_versions[dep] = []

                dep_versions[dep].append({
                    "package": package.name,
                    "version": version
                })

        # Find conflicts
        conflicts = {}
        for dep, versions in dep_versions.items():
            unique_versions = set(v["version"] for v in versions)
            if len(unique_versions) > 1:
                conflicts[dep] = versions

        return conflicts

@click.group()
def cli():
    """Monorepo management CLI."""
    pass

@cli.command()
def info():
    """Show monorepo information."""
    manager = MonorepoManager(Path.cwd())

    print(f"📊 Monorepo Information")
    print(f"  Packages: {len(manager.packages)}")

    print(f"\n📦 Packages:")
    for name, package in sorted(manager.packages.items()):
        print(f"  - {name} (v{package.version})")
        if package.dependencies:
            print(f"    Dependencies: {', '.join(package.dependencies)}")

@cli.command()
@click.argument("packages", nargs=-1)
@click.argument("command", nargs=1)
def run(packages, command):
    """Run command on packages."""
    manager = MonorepoManager(Path.cwd())

    if not packages:
        packages = manager.get_build_order()

    results = manager.run_command_on_packages(
        list(packages),
        command.split()
    )

    # Summary
    success = sum(1 for s in results.values() if s)
    print(f"\n📊 Summary: {success}/{len(results)} succeeded")

@cli.command()
def check():
    """Check for issues."""
    manager = MonorepoManager(Path.cwd())

    # Check versions
    conflicts = manager.check_versions_sync()
    if conflicts:
        print("❌ Version conflicts found:")
        for dep, versions in conflicts.items():
            print(f"\n  {dep}:")
            for v in versions:
                print(f"    - {v['package']}: {v['version']}")
    else:
        print("✅ No version conflicts")

    # Check circular dependencies
    build_order = manager.get_build_order()
    if build_order:
        print("\n✅ No circular dependencies")
        print(f"Build order: {' -> '.join(build_order)}")

if __name__ == "__main__":
    cli()
```

### 4. GitHub Actions Generator

```python
# generate_workflows.py
"""
Generate GitHub Actions workflows based on project configuration.
"""
import yaml
from pathlib import Path
from typing import Dict, List, Any

class WorkflowGenerator:
    """Generate GitHub Actions workflows."""

    def __init__(self, project_config: Dict[str, Any]):
        self.config = project_config

    def generate_ci_workflow(self) -> Dict[str, Any]:
        """Generate CI workflow."""
        python_versions = self.config.get("python_versions", ["3.9", "3.10", "3.11"])

        workflow = {
            "name": "CI",
            "on": {
                "push": {"branches": ["main", "develop"]},
                "pull_request": {"branches": ["main"]}
            },
            "jobs": {
                "test": {
                    "runs-on": "${{ matrix.os }}",
                    "strategy": {
                        "matrix": {
                            "os": ["ubuntu-latest"],
                            "python-version": python_versions
                        }
                    },
                    "steps": self._generate_test_steps()
                },
                "quality": {
                    "runs-on": "ubuntu-latest",
                    "steps": self._generate_quality_steps()
                }
            }
        }

        return workflow

    def _generate_test_steps(self) -> List[Dict[str, Any]]:
        """Generate test job steps."""
        steps = [
            {"uses": "actions/checkout@v4"},
            {
                "name": "Set up Python ${{ matrix.python-version }}",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": "${{ matrix.python-version }}"}
            }
        ]

        # Add package manager setup
        if self.config.get("package_manager") == "poetry":
            steps.extend([
                {
                    "name": "Install Poetry",
                    "uses": "snok/install-poetry@v1",
                    "with": {
                        "virtualenvs-create": True,
                        "virtualenvs-in-project": True
                    }
                },
                {
                    "name": "Cache dependencies",
                    "uses": "actions/cache@v4",
                    "with": {
                        "path": ".venv",
                        "key": "venv-${{ runner.os }}-${{ matrix.python-version }}-${{ hashFiles('**/poetry.lock') }}"
                    }
                },
                {
                    "name": "Install dependencies",
                    "run": "poetry install"
                }
            ])
        elif self.config.get("package_manager") == "uv":
            steps.extend([
                {
                    "name": "Install UV",
                    "run": "curl -LsSf https://astral.sh/uv/install.sh | sh"
                },
                {
                    "name": "Install dependencies",
                    "run": "uv sync"
                }
            ])

        # Add test command
        test_command = self.config.get("test_command", "pytest")
        steps.append({
            "name": "Run tests",
            "run": test_command
        })

        return steps

    def _generate_quality_steps(self) -> List[Dict[str, Any]]:
        """Generate quality check steps."""
        steps = [
            {"uses": "actions/checkout@v4"},
            {
                "name": "Set up Python",
                "uses": "actions/setup-python@v5",
                "with": {"python-version": "3.11"}
            }
        ]

        # Add pre-commit
        if self.config.get("use_precommit", True):
            steps.extend([
                {
                    "name": "Cache pre-commit",
                    "uses": "actions/cache@v4",
                    "with": {
                        "path": "~/.cache/pre-commit",
                        "key": "pre-commit-${{ runner.os }}-${{ hashFiles('.pre-commit-config.yaml') }}"
                    }
                },
                {
                    "name": "Run pre-commit",
                    "uses": "pre-commit/action@v3.0.0"
                }
            ])

        return steps

    def save_workflow(self, workflow: Dict[str, Any], filename: str):
        """Save workflow to file."""
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)

        workflow_file = workflows_dir / filename
        with open(workflow_file, "w") as f:
            yaml.dump(workflow, f, default_flow_style=False, sort_keys=False)

        print(f"✅ Generated {workflow_file}")

# Example usage
if __name__ == "__main__":
    config = {
        "python_versions": ["3.9", "3.10", "3.11", "3.12"],
        "package_manager": "poetry",
        "test_command": "poetry run pytest --cov",
        "use_precommit": True
    }

    generator = WorkflowGenerator(config)
    ci_workflow = generator.generate_ci_workflow()
    generator.save_workflow(ci_workflow, "ci.yml")
```

## 📚 Additional Resources

- [Example Justfile](justfile.example)
- [Example Noxfile](noxfile.example.py)
- [Pre-commit Configuration Examples](pre-commit-examples.yaml)
- [GitHub Actions Templates](workflows/)
- [Monorepo Structure Example](monorepo-structure.md)
