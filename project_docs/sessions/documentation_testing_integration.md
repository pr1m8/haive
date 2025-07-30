# Documentation Testing Integration Plan

## Overview

This document outlines how to integrate all the documentation quality and testing tools with Haive's namespaced monorepo structure, preserving the existing successful patterns while adding comprehensive testing capabilities.

## Key Considerations

### 1. Namespacing Approach (CRITICAL TO PRESERVE)

The current `conf_improved.py` successfully handles namespaced packages:

```python
# For namespaced packages, we need to add the src directory
for package in package_names:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))

        # Try to import the package
        package_module = f"haive.{package.split('-')[1]}"
        try:
            __import__(package_module)
            logger.info(f"Successfully imported {package_module}")
        except Exception as e:
            logger.warning(f"Failed to import {package_module}: {e}")
```

This approach is **WORKING** and must be preserved in all testing configurations.

### 2. Documentation Testing Tools Integration

#### pytest-doctestplus Configuration

Create `pytest.ini` or add to `pyproject.toml`:

```toml
[tool.pytest.ini_options]
doctest_plus = "enabled"
doctest_optionflags = [
    "NORMALIZE_WHITESPACE",
    "ELLIPSIS",
    "ALLOW_UNICODE"
]
doctest_plus_continue_on_failure = true
# Handle namespaced imports
doctest_plus_import_mode = "importlib"

# Skip patterns for .v2 files
doctest_plus_skip = [
    "*_v2.py",
    "*.v2.py"
]

# Required modules check
doctest_plus_requires = {
    "haive.agents.simple": ["langchain"],
    "haive.core.engine": ["pydantic>=2.0"]
}
```

#### darglint Configuration

Add to `pyproject.toml`:

```toml
[tool.darglint]
docstring_style = "google"
strictness = "short"
# Ignore .v2 files
ignore_regex = ".*_v2\\.py|.*\\.v2\\.py"
message_template = "{path}:{line} {msg_id}: {msg}"
```

#### pydocstyle Configuration

```toml
[tool.pydocstyle]
convention = "google"
add-ignore = ["D100", "D104"]  # Module and package docstrings
match-dir = "^(?!test|__pycache__|.v2).*"
match = "^(?!test_|.*_v2|.*\\.v2).*\\.py"
```

#### interrogate Configuration

```toml
[tool.interrogate]
ignore-init-method = true
ignore-init-module = false
ignore-magic = false
ignore-semiprivate = false
ignore-private = false
ignore-property-decorators = false
ignore-module = false
ignore-nested-functions = false
ignore-nested-classes = true
ignore-setters = false
fail-under = 80
exclude = ["setup.py", "docs", "build", "*_v2.py", "*.v2.py"]
ignore-regex = ["^get$", "^mock_.*", ".*BaseClass.*"]
verbose = 2
quiet = false
whitelist-regex = []
color = true
generate-badge = "docs/badges/"
badge-format = "svg"
```

### 3. Nox Integration Strategy

The enhanced `noxfile_enhanced.py` provides comprehensive testing while preserving the original graceful error handling:

#### Key Features:

1. **Preserves original sessions** - All existing docs commands work unchanged
2. **Adds test sessions** - New `docs_test_*` commands for quality checking
3. **Namespace-aware** - Sets PYTHONPATH correctly for imports
4. **Graceful handling** - Continues on errors like the original
5. **Comprehensive reporting** - JSON reports for tracking quality

#### Usage Pattern:

```bash
# Quick quality check
nox -s docs_test_docstrings

# Full testing pipeline
nox -s docs_test_all

# Traditional build (unchanged)
nox -s docs_fast
```

### 4. CI/CD Integration

Create `.github/workflows/docs-quality.yml`:

```yaml
name: Documentation Quality

on:
  push:
    branches: [main, develop]
  pull_request:
    paths:
      - "**.py"
      - "**.md"
      - "**.rst"
      - "docs/**"

jobs:
  doc-quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.12"

      - name: Install Poetry
        uses: snok/install-poetry@v1

      - name: Install dependencies
        run: poetry install --with dev,docs

      - name: Run documentation tests
        run: |
          poetry run nox -s docs_test_docstrings
          poetry run nox -s docs_test_examples
          poetry run nox -s docs_test_spelling

      - name: Upload quality reports
        uses: actions/upload-artifact@v3
        with:
          name: doc-quality-reports
          path: docs/quality-reports/
```

### 5. Pre-commit Hooks

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/PyCQA/docformatter
    rev: v1.7.5
    hooks:
      - id: docformatter
        args: [--in-place, --config, pyproject.toml]

  - repo: https://github.com/terrencepreilly/darglint
    rev: v1.8.1
    hooks:
      - id: darglint

  - repo: https://github.com/econchick/interrogate
    rev: 1.5.0
    hooks:
      - id: interrogate
        args: [--fail-under=80]
```

### 6. VSCode Integration

Add to `.vscode/settings.json`:

```json
{
  "python.testing.pytestArgs": ["--doctest-modules", "--doctest-plus"],
  "python.linting.pydocstyleEnabled": true,
  "python.linting.pydocstyleArgs": ["--convention=google"],
  "[python]": {
    "editor.rulers": [72, 79],
    "editor.wordWrap": "wordWrapColumn",
    "editor.wordWrapColumn": 79
  }
}
```

## Migration Strategy

### Phase 1: Backup and Test (Current)

1. ✅ Created timestamped backup of conf_improved.py
2. ✅ Created enhanced noxfile with new test sessions
3. Test enhanced noxfile alongside original

### Phase 2: Gradual Adoption

1. Run new test commands in parallel with existing workflow
2. Fix docstring issues incrementally
3. Build team familiarity with new tools

### Phase 3: Full Integration

1. Replace noxfile.py with noxfile_enhanced.py
2. Enable pre-commit hooks
3. Add to CI/CD pipeline

## Testing Commands Quick Reference

### Basic Quality Checks

```bash
# Docstring coverage
poetry run interrogate -vv packages/

# Style compliance
poetry run pydocstyle packages/ --convention=google

# Docstring/function match
poetry run darglint packages/

# Spell check
poetry run codespell .
```

### Nox Commands

```bash
# Traditional (unchanged)
nox -s docs_fast      # Quick build
nox -s docs          # Standard build
nox -s docs_full     # Full rebuild

# New quality tests
nox -s docs_test_docstrings  # Coverage & style
nox -s docs_test_examples    # Doctest examples
nox -s docs_test_spelling    # Spelling check
nox -s docs_test_all         # Everything
```

### Fix Commands

```bash
# Auto-fix docstring formatting
poetry run docformatter -i -r packages/

# Fix spelling interactively
poetry run codespell . -i 3

# Generate missing docstrings (manual review needed)
poetry run interrogate --generate-badge docs/badges/
```

## Quality Metrics Dashboard

Track these metrics over time:

1. **Docstring Coverage** (target: >90%)
   - interrogate badge
   - docstr-coverage reports

2. **Style Compliance** (target: 100%)
   - pydocstyle violations
   - darglint mismatches

3. **Documentation Tests** (target: 100% pass)
   - pytest-doctestplus results
   - sphinx doctest results

4. **Spelling/Prose** (target: 0 errors)
   - codespell findings
   - proselint suggestions

## Troubleshooting

### Import Errors in Doctests

Ensure PYTHONPATH includes all package src directories:

```python
# In test setup
for package in PACKAGE_NAMES:
    src_path = PACKAGES_DIR / package / "src"
    if src_path.exists():
        os.environ["PYTHONPATH"] = f"{src_path}:{os.environ.get('PYTHONPATH', '')}"
```

### .v2 Files Being Tested

Check all tools have exclusion patterns:

- `*_v2.py` and `*.v2.py` in all ignore lists
- Update glob patterns if needed

### Slow Test Runs

Use parallel execution where possible:

- `pytest -n auto` for doctests
- Nox session reuse with `--reuse-existing-virtualenvs`

## Summary

This integration plan preserves Haive's successful namespacing approach while adding world-class documentation testing. The key is gradual adoption - test the enhanced noxfile alongside the original, fix issues incrementally, and migrate when confident.

The enhanced tooling provides:

- Automated quality checking
- Comprehensive test coverage
- Continuous improvement tracking
- Team-wide consistency

All while maintaining the graceful error handling and namespace awareness that makes the current system work.
