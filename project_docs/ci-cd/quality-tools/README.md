# Pre-commit and Quality Tools for Python

**Last Updated**: 2025-01-11

## Overview

Quality tools and pre-commit hooks ensure code consistency, catch bugs early, and maintain high standards across Python projects. The pre-commit framework has become the de facto standard for managing these tools.

## 🎯 Pre-commit Framework

### What is Pre-commit?

Pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It ensures specific checks (linting, formatting, security scanning) run automatically before every commit.

### Installation and Setup

```bash
# Install pre-commit
pip install pre-commit

# Or with other package managers
poetry add --group dev pre-commit
uv pip install pre-commit

# Install the git hook scripts
pre-commit install

# Optional: Install for other git hooks
pre-commit install --hook-type commit-msg
pre-commit install --hook-type pre-push
```

### Basic Configuration

```yaml
# .pre-commit-config.yaml
default_language_version:
  python: python3.11

# Don't run on these files
exclude: '^(\.git|\.hg|\.mypy_cache|\.tox|\.venv|_build|buck-out|build|dist)'

repos:
  # Pre-commit hooks for general file fixes
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: check-json
      - id: check-xml
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: check-added-large-files
        args: ["--maxkb=1000"]
      - id: check-case-conflict
      - id: check-merge-conflict
      - id: detect-private-key
      - id: fix-byte-order-marker
      - id: mixed-line-ending
        args: ["--fix=lf"]

  # Python code formatting
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        language_version: python3.11
        args: ["--line-length=88"]

  # Fast Python linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format # Ruff's black-compatible formatter

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black", "--line-length", "88"]
```

## 🛠️ Essential Quality Tools

### 1. Ruff (Fast Python Linter)

**What it is**: An extremely fast Python linter written in Rust that replaces Flake8, pylint, and many other tools.

**Configuration in pyproject.toml**:

```toml
[tool.ruff]
line-length = 88
target-version = "py39"

select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "C4",  # flake8-comprehensions
    "DTZ", # flake8-datetimez
    "T10", # flake8-debugger
    "ISC", # flake8-implicit-str-concat
    "ICN", # flake8-import-conventions
    "PIE", # flake8-pie
    "PT",  # flake8-pytest-style
    "RET", # flake8-return
    "SIM", # flake8-simplify
    "ERA", # eradicate
]

ignore = [
    "E501",  # line too long (handled by formatter)
    "E402",  # module import not at top
]

[tool.ruff.per-file-ignores]
"tests/*" = ["S101"]  # Allow asserts in tests
"__init__.py" = ["F401"]  # Allow unused imports

[tool.ruff.isort]
known-first-party = ["myproject"]
```

**Pre-commit hook**:

```yaml
- repo: https://github.com/astral-sh/ruff-pre-commit
  rev: v0.1.11
  hooks:
    - id: ruff
      args: [--fix]
```

### 2. Black (Code Formatter)

**What it is**: The uncompromising Python code formatter that enforces consistent style.

**Configuration**:

```toml
[tool.black]
line-length = 88
target-version = ['py39', 'py310', 'py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  # directories
  \.eggs
  | \.git
  | \.hg
  | \.mypy_cache
  | \.tox
  | \.venv
  | build
  | dist
)/
'''
```

### 3. mypy (Type Checker)

**What it is**: Static type checker for Python that helps catch type-related bugs.

**Configuration**:

```toml
[tool.mypy]
python_version = "3.9"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_incomplete_defs = true
check_untyped_defs = true
disallow_untyped_decorators = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true

[[tool.mypy.overrides]]
module = "tests.*"
ignore_errors = true

[[tool.mypy.overrides]]
module = "third_party.*"
ignore_missing_imports = true
```

**Pre-commit hook**:

```yaml
- repo: local
  hooks:
    - id: mypy
      name: mypy
      entry: mypy
      language: system
      types: [python]
      require_serial: true
      args: ["--config-file", "pyproject.toml"]
```

### 4. Bandit (Security Linter)

**What it is**: Security linter that finds common security issues in Python code.

**Configuration**:

```yaml
# .bandit
[bandit]
exclude: /test,/tests
skips: B101,B601

# Pre-commit hook
- repo: https://github.com/pycqa/bandit
  rev: 1.7.6
  hooks:
    - id: bandit
      args: ['-c', '.bandit', '-r', 'src/']
      exclude: ^tests/
```

### 5. Safety (Dependency Scanner)

**What it is**: Checks Python dependencies for known security vulnerabilities.

**Pre-commit hook**:

```yaml
- repo: https://github.com/Lucas-C/pre-commit-hooks-safety
  rev: v1.3.2
  hooks:
    - id: python-safety-dependencies-check
      files: requirements.*\.txt$
```

## 📊 Advanced Pre-commit Patterns

### Custom Local Hooks

```yaml
# .pre-commit-config.yaml
- repo: local
  hooks:
    # Check for print statements
    - id: no-print-statements
      name: No print statements
      entry: 'print\('
      language: pygrep
      types: [python]
      exclude: ^(tests/|scripts/debug)

    # Ensure no TODO comments in production code
    - id: no-todos
      name: No TODO comments
      entry: "TODO|FIXME|XXX"
      language: pygrep
      types: [python]
      exclude: ^tests/

    # Run pytest on staged test files
    - id: pytest-check
      name: pytest
      entry: pytest
      language: system
      files: test_.*\.py$
      pass_filenames: true
      stages: [push]

    # Check for large files before commit
    - id: file-size-check
      name: Check file size
      entry: scripts/check_file_size.py
      language: python
      types: [python]
      exclude: ^(data/|fixtures/)
```

### Stage-Specific Hooks

```yaml
# Different hooks for different git stages
default_stages: [commit]

repos:
  # Run on every commit
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        stages: [commit]

  # Run only on push
  - repo: local
    hooks:
      - id: integration-tests
        name: Integration tests
        entry: pytest tests/integration/
        language: system
        pass_filenames: false
        stages: [push]

  # Run on manual stage only
  - repo: local
    hooks:
      - id: performance-test
        name: Performance benchmarks
        entry: pytest tests/performance/ --benchmark-only
        language: system
        pass_filenames: false
        stages: [manual]
```

### Language-Specific Hooks

```yaml
# Multi-language project hooks
repos:
  # Python
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black
        types: [python]

  # JavaScript/TypeScript
  - repo: https://github.com/pre-commit/mirrors-eslint
    rev: v8.56.0
    hooks:
      - id: eslint
        types: [javascript, jsx, ts, tsx]

  # Markdown
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.38.0
    hooks:
      - id: markdownlint
        args: ["--fix"]

  # Docker
  - repo: https://github.com/hadolint/hadolint
    rev: v2.12.0
    hooks:
      - id: hadolint

  # Shell scripts
  - repo: https://github.com/shellcheck-py/shellcheck-py
    rev: v0.9.0.6
    hooks:
      - id: shellcheck
```

## 🔄 CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/pre-commit.yml
name: pre-commit

on:
  pull_request:
  push:
    branches: [main, develop]

jobs:
  pre-commit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Cache pre-commit
        uses: actions/cache@v4
        with:
          path: ~/.cache/pre-commit
          key: pre-commit-${{ runner.os }}-${{ hashFiles('.pre-commit-config.yaml') }}

      - uses: pre-commit/action@v3.0.0
        with:
          extra_args: --all-files --show-diff-on-failure
```

### Auto-update Pre-commit

```yaml
# .github/workflows/pre-commit-update.yml
name: Pre-commit auto-update

on:
  schedule:
    - cron: "0 0 * * 0" # Weekly on Sunday
  workflow_dispatch:

jobs:
  auto-update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Update pre-commit hooks
        run: |
          pip install pre-commit
          pre-commit autoupdate

      - name: Create Pull Request
        uses: peter-evans/create-pull-request@v5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: update/pre-commit-hooks
          title: "chore: update pre-commit hooks"
          commit-message: "chore: update pre-commit hooks"
          body: |
            This PR updates the pre-commit hooks to their latest versions.

            Please review the changes and merge if all checks pass.
```

## 🎨 Quality Tool Combinations

### Minimal Setup

```yaml
# For small projects
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
```

### Comprehensive Setup

```yaml
# For production projects
repos:
  # File fixes
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-ast
      - id: check-builtin-literals
      - id: check-case-conflict
      - id: check-docstring-first
      - id: check-merge-conflict
      - id: check-toml
      - id: check-yaml
      - id: debug-statements
      - id: end-of-file-fixer
      - id: fix-byte-order-marker
      - id: mixed-line-ending
      - id: trailing-whitespace

  # Python formatting
  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  # Import sorting
  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  # Linting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix]

  # Security
  - repo: https://github.com/pycqa/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        exclude: ^tests/

  # Docstrings
  - repo: https://github.com/pycqa/pydocstyle
    rev: 6.3.0
    hooks:
      - id: pydocstyle
        additional_dependencies: [toml]

  # Type checking
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-all]
```

## 📈 Performance Optimization

### Speeding Up Pre-commit

```yaml
# Parallel execution
ci:
  autoupdate_commit_msg: "chore: update pre-commit hooks"
  autoupdate_schedule: weekly
  skip: [mypy] # Skip slow hooks in CI
  parallel: true # Run hooks in parallel

# Hook-specific optimizations
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.11
    hooks:
      - id: ruff
        args: [--fix, --force-exclude] # Faster exclusion

  - repo: local
    hooks:
      - id: pytest-fast
        name: pytest (fast)
        entry: pytest -x --ff # Exit on first failure, run failed first
        language: system
        types: [python]
        pass_filenames: false
```

### Caching Strategies

```bash
# Local caching
export PRE_COMMIT_HOME=$HOME/.cache/pre-commit

# CI caching (GitHub Actions)
- uses: actions/cache@v4
  with:
    path: |
      ~/.cache/pre-commit
      ~/.cache/pip
      .mypy_cache
    key: ${{ runner.os }}-pre-commit-${{ hashFiles('.pre-commit-config.yaml') }}
```

## 🚀 Best Practices

1. **Start Small**: Add basic hooks first, expand gradually
2. **Fast Feedback**: Put quick checks first, slow ones last
3. **CI Integration**: Always run pre-commit in CI
4. **Regular Updates**: Use autoupdate to keep hooks current
5. **Team Agreement**: Ensure team consensus on rules
6. **Skip When Needed**: Use `--no-verify` sparingly
7. **Stage-Specific**: Use appropriate stages for different checks
8. **Custom Hooks**: Create project-specific checks

## 📚 Troubleshooting

### Common Issues

```bash
# Hook installation failed
pre-commit clean
pre-commit install --force

# Specific hook failing
pre-commit run <hook-id> --all-files --verbose

# Skip a specific hook once
SKIP=mypy git commit -m "message"

# Update all hooks
pre-commit autoupdate

# Run on specific files
pre-commit run --files path/to/file.py

# Debug a hook
pre-commit run <hook-id> --all-files --show-diff-on-failure --verbose
```

### Hook Development

```python
#!/usr/bin/env python3
"""Custom pre-commit hook example."""
import argparse
import sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filenames', nargs='*')
    args = parser.parse_args()

    failed = False
    for filename in args.filenames:
        path = Path(filename)
        content = path.read_text()

        # Your check logic here
        if 'forbidden_pattern' in content:
            print(f"{filename}: Contains forbidden pattern")
            failed = True

    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
```

## 🔗 Resources

- [Pre-commit Documentation](https://pre-commit.com/)
- [Awesome Pre-commit](https://github.com/aitemr/awesome-pre-commit-hooks)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [Black Documentation](https://black.readthedocs.io/)
- [mypy Documentation](https://mypy.readthedocs.io/)
