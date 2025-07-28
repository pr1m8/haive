# Development Dependencies Memory

**Created**: 2025-07-28
**Purpose**: Track available dev tools in pyproject.toml

## 🎯 Key Discovery: Documentation Tools Already Available

### Documentation & Quality Tools (Lines 188-299)

```toml
# Documentation coverage and validation
interrogate = "^1.5.0"          # Measure docstring coverage
pydocstyle = "^6.3.0"           # Google-style enforcement
darglint = "^1.8.1"             # Args/Returns/Raises validation

# Code formatting and cleanup
docformatter = "^1.7.7"         # Auto-format docstrings
autoflake = "^2.3.1"            # Remove unused imports
autopep8 = "^2.3.2"             # PEP 8 formatting
black = "^25.1.0"               # Code formatting

# Type system
monkeytype = "^23.3.0"          # Generate type annotations
mypy = "^1.15.0"                # Type checking
autotyping = "^24.9.0"          # Auto type annotation

# Linting
flake8 = "^7.1.2"               # Linting framework
ruff = "^0.11.6"                # Fast linter (Google-style configured!)
pylint = "^3.3.7"               # Additional linting

# Pre-commit and CI/CD
pre-commit = "^4.1.0"           # Git hooks
commitizen = "^4.8.3"           # Conventional commits

# Testing
pytest = "^8.3.5"               # Test framework
pytest-asyncio = "^0.26.0"      # Async testing
pytest-benchmark = "^5.1.0"     # Performance testing

# Profiling and debugging
ipdb = "^0.13.13"               # Interactive debugger
viztracer = "^1.0.3"            # Visual tracing
memray = "^1.17.1"              # Memory profiling
py-spy = "^0.4.0"               # Performance profiling
```

### Configuration Already Present

```toml
# Lines 578-579
[tool.ruff.lint.pydocstyle]
convention = "google"  # Google-style already configured!

# Lines 508-523
[tool.mypy]
disallow_untyped_defs = true
disallow_incomplete_defs = true
# ... comprehensive type checking
```

## 🔧 Missing Tools (Need to Add)

For complete Google-style workflow:

```bash
flake8-docstrings              # pydocstyle → Flake8 integration
pydoclint[flake8]              # Ultra-fast semantic validation
```

## 📊 Documentation Dependencies (Lines 301-343)

```toml
[tool.poetry.group.docs.dependencies]
sphinx = "^8.0.0"
sphinx-autoapi = "^3.6.0"
sphinx-gallery = "^0.19.0"
furo = "^2024.8.6"              # Modern theme
myst-parser = "^4.0.1"          # Markdown support
# ... many more Sphinx extensions
```

## 🚀 Immediate Usage Commands

These work RIGHT NOW without any setup:

```bash
# Documentation coverage
poetry run interrogate packages/ --verbose --fail-under=80

# Google-style validation
poetry run pydocstyle packages/ --convention=google

# Semantic validation
poetry run darglint packages/ --strictness=short

# Auto-formatting
poetry run docformatter --in-place --recursive packages/

# Import cleanup
poetry run autoflake --in-place --remove-all-unused-imports --recursive packages/

# Fast Google-style check
poetry run ruff check packages/ --select=D
```

## 🔗 Related Memories

- @memory_index/by_date/2025-07-28/documentation_automation_discovery.md
- @project_docs/documentation_fix/COMPREHENSIVE_GOOGLE_STYLE_SUMMARY.md
- @memory_index/by_task/documentation/google_style_enforcement.md
