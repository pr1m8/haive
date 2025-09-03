# Docstring Analyzer and Converter

This directory contains tools for converting Python docstrings from markdown format to Google style.

## Problem

Many files in the codebase use markdown-style code blocks (```) in docstrings, which is not standard Python documentation format. Google style docstrings use `>>>` prefixes for examples.

## Solution

We've created a suite of tools to detect, validate, and fix these docstrings:

### 1. `quick_scan.py` - Fast Detection
```bash
python scripts/docstring_analyzer/quick_scan.py
```
Quickly scans all packages and reports files with markdown blocks in docstrings.

### 2. `fix_docstrings_clean.py` - Main Converter ✅
```bash
# Dry-run on single file (default - safe!)
python scripts/docstring_analyzer/fix_docstrings_clean.py path/to/file.py

# Apply changes
python scripts/docstring_analyzer/fix_docstrings_clean.py path/to/file.py --apply

# Process entire directory
python scripts/docstring_analyzer/fix_docstrings_clean.py --dir packages/haive-core

# Apply to directory with verbose output
python scripts/docstring_analyzer/fix_docstrings_clean.py --dir packages --apply --verbose
```

**Features:**
- ✅ Robust error handling - no crashes on malformed docstrings
- ✅ Proper indentation preservation for module/function/class docstrings
- ✅ Safe dry-run mode by default
- ✅ Validates Python syntax before and after conversion
- ✅ Validates with `pydocstyle --convention=google`
- ✅ Creates automatic backups before modifying files
- ✅ Shows colored diff preview
- ✅ Filters out minor style warnings

### 3. `batch_fix_all.py` - Batch Processor
```bash
# Preview all changes
python scripts/docstring_analyzer/batch_fix_all.py --dry-run

# Apply to specific package
python scripts/docstring_analyzer/batch_fix_all.py --package haive-core --apply

# Get JSON output
python scripts/docstring_analyzer/batch_fix_all.py --json
```

## What Gets Converted

### Before (Markdown Style):
```python
"""Module with examples.

```python
from haive.core import something
result = something.process()
```

More text here.
"""
```

### After (Google Style):
```python
"""Module with examples.

Examples:
    >>> from haive.core import something
    >>> result = something.process()

More text here.
"""
```

## Statistics

Found **63 files** with markdown blocks across packages:
- `haive-core`: 38 files
- `haive-agents`: 10 files
- `haive-games`: 8 files
- `haive-mcp`: 4 files
- `haive-dataflow`: 2 files
- `haive-prebuilt`: 1 file

## Validation

All converted docstrings are validated with:
```bash
pydocstyle --convention=google <file>
```

Common minor warnings after conversion (can be ignored):
- `D415`: First line should end with period
- `D207`: Docstring indentation
- `D202`: No blank lines after function docstring

## Safety Features

1. **Dry-run by default** - Won't modify files unless `--apply` is used
2. **Syntax validation** - Checks Python syntax before and after
3. **Automatic backups** - Creates `.backup.TIMESTAMP` files
4. **Error recovery** - Returns original docstring if conversion fails
5. **Timeout protection** - 10-second timeout on validation

## Quick Start

```bash
# 1. See what needs fixing
python scripts/docstring_analyzer/quick_scan.py

# 2. Test on one file
python scripts/docstring_analyzer/fix_docstrings_clean.py packages/haive-core/src/haive/core/__init__.py

# 3. Apply to one file
python scripts/docstring_analyzer/fix_docstrings_clean.py packages/haive-core/src/haive/core/__init__.py --apply

# 4. Process entire package
python scripts/docstring_analyzer/fix_docstrings_clean.py --dir packages/haive-core --apply
```

## Development Files

- `detect_docstring_issues.py` - Original detector with AST parsing
- `convert_docstrings.py` - First converter attempt
- `preview_conversion.py` - Preview tool with rules display
- `fix_docstrings.py` - Earlier fixer version
- `test_example.py` - Test file for validation
- `test_original.py` - Copy of original test file

## Notes

- The converter preserves all other docstring content
- Only markdown code blocks are converted
- Indentation is properly maintained for nested docstrings
- Google style validation helps ensure quality
- Minor style warnings are expected and acceptable