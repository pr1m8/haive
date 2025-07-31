# 🤖 Haive Automation Tools Guide

**Created**: 2025-01-18
**Purpose**: Comprehensive guide to all automation tools available in Haive

## 🎯 Overview

This guide covers all the automation tools available in the Haive project to accelerate development, improve code quality, and maintain consistency.

## 📋 Table of Contents

1. [Type Hint Automation](#type-hint-automation)
2. [Documentation Automation](#documentation-automation)
3. [Code Quality Tools](#code-quality-tools)
4. [Testing Tools](#testing-tools)
5. [Formatting & Linting](#formatting--linting)
6. [Build & Deployment](#build--deployment)
7. [Analysis Tools](#analysis-tools)
8. [Custom Scripts](#custom-scripts)

## 🔧 Type Hint Automation

### autotyping (24.9.0)

Automatically adds type hints to your Python code.

```bash
# Add type hints to a file
poetry run autotyping --safe-imports packages/haive-core/src/haive/core/utils.py

# Process entire package
poetry run autotyping --safe-imports --recursive packages/haive-agents/src/
```

### mypy

Static type checker for Python.

```bash
# Check specific package
poetry run mypy packages/haive-core/src/ --ignore-missing-imports

# Check all packages with report
poetry run mypy packages/ --html-report mypy-report
```

### pyright

Microsoft's type checker (installed).

```bash
# Type check with pyright
poetry run pyright packages/haive-agents/src/
```

## 📚 Documentation Automation

### interrogate (1.7.0)

Check docstring coverage in your Python code.

```bash
# Check docstring coverage
poetry run interrogate packages/ -vv

# Generate badge
poetry run interrogate --generate-badge interrogate-badge.svg
```

### pydocstyle (6.3.0)

Check compliance with Python docstring conventions.

```bash
# Check docstring style
poetry run pydocstyle packages/haive-core/src/

# With specific conventions (Google style)
poetry run pydocstyle --convention=google packages/
```

### darglint (1.8.1)

Check docstring descriptions match function definitions.

```bash
# Validate docstrings match implementations
poetry run darglint packages/haive-agents/src/

# Check specific file
poetry run darglint -v 2 path/to/file.py
```

### doc8 (1.1.2)

Style checker for RST and plain text documentation.

```bash
# Check RST files
poetry run doc8 docs/source/

# Check with custom config
poetry run doc8 --max-line-length 100 docs/
```

### sphinx-build

Build documentation with our Furo theme.

```bash
# Build HTML docs
poetry run sphinx-build -b html docs/source docs/build/html

# Build with warnings as errors
poetry run sphinx-build -W -b html docs/source docs/build/html

# Auto-rebuild on changes
poetry run sphinx-autobuild docs/source docs/build/html
```

## 🔍 Code Quality Tools

### ruff

Fast Python linter and formatter.

```bash
# Check code
poetry run ruff check packages/

# Fix auto-fixable issues
poetry run ruff check --fix packages/

# Format code
poetry run ruff format packages/
```

### autoflake (2.3.1)

Remove unused imports and variables.

```bash
# Remove unused imports
poetry run autoflake --remove-all-unused-imports --in-place packages/haive-core/src/

# Remove unused variables too
poetry run autoflake --remove-unused-variables --in-place --recursive packages/
```

### autopep8 (2.3.2)

Automatically format Python code to PEP 8.

```bash
# Format file
poetry run autopep8 --in-place --aggressive file.py

# Format package
poetry run autopep8 --in-place --aggressive --recursive packages/haive-agents/
```

### black

The uncompromising Python code formatter.

```bash
# Format code
poetry run black packages/

# Check without modifying
poetry run black --check packages/
```

### isort

Sort and organize imports.

```bash
# Sort imports
poetry run isort packages/

# Check import order
poetry run isort --check-only packages/
```

## 🧪 Testing Tools

### pytest

Testing framework with extensive plugins.

```bash
# Run all tests
poetry run pytest

# With coverage
poetry run pytest --cov=haive --cov-report=html

# Run specific test
poetry run pytest -k test_simple_agent -v
```

### pytest-xdist

Run tests in parallel.

```bash
# Run tests in parallel
poetry run pytest -n auto

# Use 4 workers
poetry run pytest -n 4
```

### allure-pytest (2.14.3)

Generate Allure test reports.

```bash
# Run tests with Allure
poetry run pytest --alluredir=allure-results

# Generate report
poetry run allure serve allure-results
```

### hypothesis

Property-based testing.

```bash
# Run property-based tests
poetry run pytest --hypothesis-show-statistics
```

## 🚀 Build & Deployment Tools

### nox

Automation tool for multiple Python environments.

```bash
# Run all sessions
nox

# Run specific session
nox -s test
nox -s docs
nox -s lint
```

### trunk

Meta-linter and formatter.

```bash
# Check all files
trunk check --all

# Auto-fix issues
trunk check --fix --all

# Check specific files
trunk check packages/haive-core/
```

## 📊 Analysis Tools

### vulture

Find dead code.

```bash
# Find unused code
poetry run vulture packages/

# With minimum confidence
poetry run vulture packages/ --min-confidence 80
```

### bandit

Security linter.

```bash
# Security scan
poetry run bandit -r packages/

# Generate JSON report
poetry run bandit -r packages/ -f json -o security-report.json
```

### radon

Code complexity checker.

```bash
# Cyclomatic complexity
poetry run radon cc packages/ -a

# Maintainability index
poetry run radon mi packages/

# Raw metrics
poetry run radon raw packages/
```

### pylint

Comprehensive code analyzer.

```bash
# Analyze package
poetry run pylint packages/haive-core/src/

# With specific checks
poetry run pylint --disable=C0111 packages/
```

## 🛠️ Custom Haive Scripts

### Type Hint Analyzer

Our custom type hint analysis tool.

```bash
# Analyze all packages
poetry run python scripts/type_hint_analyzer.py --all

# Specific package
poetry run python scripts/type_hint_analyzer.py --package haive-core
```

### Type Hint Fixer

Our custom type hint fixing tool.

```bash
# Fix type hints with dry run
poetry run python scripts/type_hint_fixer.py --package haive-core --dry-run

# Apply fixes
poetry run python scripts/type_hint_fixer.py --package haive-core
```

### Parse Error Fixer

Fix common parse errors.

```bash
# Fix parse patterns
poetry run python scripts/fix_parse_patterns.py packages/
```

## 🎯 Automation Workflows

### Complete Code Quality Check

```bash
# 1. Fix imports and unused code
poetry run autoflake --remove-all-unused-imports --remove-unused-variables --in-place --recursive packages/
poetry run isort packages/

# 2. Format code
poetry run black packages/
poetry run autopep8 --in-place --aggressive --recursive packages/

# 3. Type hints
poetry run autotyping --safe-imports --recursive packages/

# 4. Lint
poetry run ruff check --fix packages/
poetry run pylint packages/

# 5. Type check
poetry run mypy packages/
```

### Documentation Pipeline

```bash
# 1. Check coverage
poetry run interrogate packages/ -vv

# 2. Validate style
poetry run pydocstyle --convention=google packages/
poetry run darglint packages/

# 3. Build docs
poetry run sphinx-build -W -b html docs/source docs/build/html

# 4. Check RST
poetry run doc8 docs/source/
```

### Pre-commit Workflow

```bash
# 1. Auto-fixes
trunk check --fix --all

# 2. Tests
poetry run pytest -n auto

# 3. Type checking
poetry run mypy packages/

# 4. Documentation
poetry run interrogate packages/
```

## 🔄 Continuous Integration

### GitHub Actions Integration

```yaml
- name: Lint
  run: |
    poetry run ruff check packages/
    poetry run mypy packages/

- name: Test
  run: |
    poetry run pytest --cov=haive

- name: Docs
  run: |
    poetry run interrogate packages/
    poetry run sphinx-build -W docs/source docs/build
```

## 📈 Metrics & Reporting

### Generate Comprehensive Report

```bash
# Code metrics
poetry run radon cc packages/ -a > metrics/complexity.txt
poetry run radon mi packages/ > metrics/maintainability.txt

# Coverage
poetry run pytest --cov=haive --cov-report=html --cov-report=term

# Type coverage
poetry run mypy packages/ --html-report mypy-report

# Docstring coverage
poetry run interrogate packages/ -vv > metrics/docstrings.txt

# Security
poetry run bandit -r packages/ -f json -o metrics/security.json
```

## 🚀 Next Steps

1. **Set up pre-commit hooks** with these tools
2. **Create GitHub Actions** for automation
3. **Build dashboards** for metrics
4. **Schedule regular** quality checks
5. **Document tool** configurations

## 💡 Pro Tips

1. **Combine tools** for maximum effect
2. **Start with** auto-fixers before manual work
3. **Use dry-run** options to preview changes
4. **Save reports** for tracking progress
5. **Integrate with** your IDE for real-time feedback

---

Remember: Automation tools are force multipliers. Use them to focus on creative work while they handle the repetitive tasks!
