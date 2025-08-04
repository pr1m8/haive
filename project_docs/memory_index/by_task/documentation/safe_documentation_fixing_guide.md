# Safe Documentation Fixing Guide

**Date**: 2025-01-21
**Purpose**: How to safely fix documentation using available tools without breaking code

## 🛡️ Safety First: Version Control

### Before ANY Changes
```bash
# 1. Check current state
git status
git diff

# 2. Create safety branch
git checkout -b docs/fix-documentation-$(date +%Y%m%d)

# 3. Commit current state if needed
git add -A
git commit -m "chore: checkpoint before documentation fixes"
```

## 🧰 Available Documentation Tools (from poetry dev dependencies)

### 1. Documentation Analysis Tools

#### interrogate - Find Missing Docstrings
```bash
# Check docstring coverage
poetry run interrogate -v packages/

# Generate detailed report
poetry run interrogate -v --fail-under 0 --generate-badge badges/ packages/

# Check specific package
poetry run interrogate -v packages/haive-core/

# Output formats
poetry run interrogate -v --output json packages/ > docstring_coverage.json
```

#### pydocstyle - Docstring Style Enforcement
```bash
# Check docstring style issues
poetry run pydocstyle packages/

# Check with specific convention (we use Google style)
poetry run pydocstyle --convention=google packages/

# Check specific file
poetry run pydocstyle packages/haive-core/src/haive/core/engine.py
```

#### darglint - Docstring-Code Sync Validation
```bash
# Check if docstrings match actual code
poetry run darglint packages/

# Check specific file
poetry run darglint -v 2 packages/haive-core/src/haive/core/engine.py
```

### 2. Type Hint Tools

#### mypy - Type Checking
```bash
# Run type checking
poetry run mypy packages/

# With strict mode
poetry run mypy --strict packages/haive-core/

# Check specific file
poetry run mypy packages/haive-core/src/haive/core/engine.py
```

#### monkeytype - Runtime Type Collection
```bash
# Collect runtime types (SAFE - just observes)
poetry run monkeytype run your_script.py

# Generate stub files (SAFE - doesn't modify code)
poetry run monkeytype stub haive.core.engine

# Apply types (DANGEROUS - review first!)
poetry run monkeytype apply haive.core.engine --diff  # Preview first
```

#### autotyping - Automatic Type Annotation
```bash
# Preview changes (SAFE)
poetry run autotyping --diff packages/haive-core/src/haive/core/engine.py

# Apply after review (DANGEROUS)
poetry run autotyping packages/haive-core/src/haive/core/engine.py
```

### 3. Code Quality & Linting

#### ruff - Fast Python Linter (with D rules for docs)
```bash
# Check documentation issues
poetry run ruff check --select D packages/

# Show fixable issues
poetry run ruff check --select D --diff packages/

# Fix safe issues (CAREFUL - review first)
poetry run ruff check --select D --fix --unsafe-fixes packages/

# Check specific rules
poetry run ruff check --select D100,D101,D102 packages/  # Module/class/method docstrings
```

### 4. Documentation Building & Validation

#### sphinx-build - Build Documentation
```bash
# Build docs and check for warnings
poetry run sphinx-build -W -b html docs/source docs/build/html

# Build with nitpicky mode (all warnings are errors)
poetry run sphinx-build -n -W -b html docs/source docs/build/html
```

#### doc8 - Documentation Linter
```bash
# Check RST files for issues
poetry run doc8 docs/

# Check with custom config
poetry run doc8 --max-line-length 100 docs/
```

#### codespell - Spell Checker
```bash
# Check for spelling errors
poetry run codespell packages/ docs/

# Fix spelling errors (CAREFUL)
poetry run codespell -w packages/ docs/
```

## 🔄 Safe Fixing Workflow

### Step 1: Analysis Only (100% Safe)
```bash
# 1. Run comprehensive analysis
poetry run interrogate -v packages/ > interrogate_report.txt
poetry run pydocstyle --convention=google packages/ > pydocstyle_report.txt
poetry run darglint packages/ > darglint_report.txt
poetry run mypy packages/ > mypy_report.txt

# 2. Our custom audit
poetry run python docs/scripts/documentation_audit.py packages/ > full_audit_report.txt

# 3. Check current build status
poetry run sphinx-build -W -b html docs/source docs/build/html 2> sphinx_warnings.txt
```

### Step 2: Safe Preview Tools
```bash
# Preview type hints (no changes)
poetry run monkeytype stub haive.core.engine
poetry run autotyping --diff packages/haive-core/src/haive/core/engine.py

# Preview ruff fixes
poetry run ruff check --select D --diff packages/

# Generate fix suggestions
poetry run ruff check --select D --fix --diff packages/ > suggested_fixes.diff
```

### Step 3: Incremental Safe Fixes

#### Fix Parse Errors First (Critical)
```bash
# 1. Find parse errors
poetry run python -m py_compile packages/**/*.py 2>&1 | grep -E "SyntaxError|IndentationError"

# 2. Fix manually or with editor
```

#### Add __all__ Exports (Safe & Quick)
```bash
# Find missing __all__
grep -L "__all__" packages/*/*/__init__.py

# Add manually to each __init__.py
```

#### Add Module Docstrings (Safe)
```bash
# Find files without module docstrings
poetry run interrogate -v --fail-under 0 -i module packages/

# Use template:
"""Module description.

This module provides...

Example:
    >>> from haive.module import function
    >>> function()
"""
```

### Step 4: Testing After Changes
```bash
# 1. Run tests
poetry run pytest packages/ -v

# 2. Check imports work
poetry run python -c "from haive.core import *; from haive.agents import *"

# 3. Rebuild docs
poetry run sphinx-build -W -b html docs/source docs/build/html

# 4. Run linters
poetry run ruff check packages/
poetry run mypy packages/
```

## 🚦 Safety Levels

### 🟢 Completely Safe (Analysis Only)
- interrogate (coverage check)
- pydocstyle (style check)
- darglint (sync check)
- mypy (type check)
- doc8 (rst check)
- All custom audit scripts
- monkeytype stub generation
- ruff check (without --fix)

### 🟡 Safe with Review
- ruff --fix (review diffs first)
- codespell -w (check spelling fixes)
- autotyping (review type suggestions)

### 🔴 Potentially Dangerous
- monkeytype apply (can add wrong types)
- Any automated docstring generators
- Mass find/replace operations

## 📋 Recommended Fix Order

1. **Parse Errors** (20 files) - Manual fix required
2. **Missing `__all__`** (113 files) - Quick manual additions
3. **Missing Module Docstrings** (773 files) - Can use templates
4. **Missing Type Hints** (2,143) - Use monkeytype stubs + manual review
5. **Missing Function Docstrings** (1,324) - Manual or careful automation
6. **Missing Returns/Args Documentation** (9,946) - Manual updates

## 🔧 VS Code Integration

```json
// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.linting.ruffArgs": ["--select", "D,ANN"],
  "python.linting.mypyEnabled": true,
  "autoDocstring.docstringFormat": "google",
  "autoDocstring.includeExtendedSummary": true
}
```

## 🎯 Quick Commands Reference

```bash
# Safe analysis combo
poetry run interrogate -v packages/ && \
poetry run pydocstyle --count packages/ && \
poetry run ruff check --select D packages/

# Check specific package thoroughly
PKG=haive-core && \
poetry run interrogate -v packages/$PKG/ && \
poetry run pydocstyle packages/$PKG/ && \
poetry run mypy packages/$PKG/

# Generate comprehensive report
poetry run python docs/scripts/documentation_audit.py packages/ > doc_audit_$(date +%Y%m%d).txt
```

## 🚨 Recovery If Things Go Wrong

```bash
# Discard all changes
git reset --hard HEAD

# Discard specific file changes
git checkout -- path/to/file.py

# View what changed
git diff

# Create patch for later
git diff > my_changes.patch
```

Remember: **Always work on a branch, commit often, and test after each change!**
