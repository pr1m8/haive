# Pyright Error Analysis Scripts

This directory contains scripts for analyzing pyright errors in the Haive codebase, categorizing them by severity, and identifying which errors will break at runtime.

## Scripts

### 1. `pyright_error_analyzer.py` - Comprehensive Analysis

The main analysis script that:

- Runs pyright on all packages
- Categorizes errors by severity (critical/medium/type-only)
- Identifies runtime-breaking errors
- Groups errors by type (import/type/attribute/other)
- Generates detailed reports

**Usage:**

```bash
poetry run python scripts/analysis/pyright_error_analyzer.py
```

**Output:**

- `error_reports/YYYYMMDD_HHMMSS/error_analysis_summary.md` - Markdown summary
- `error_reports/YYYYMMDD_HHMMSS/error_analysis_detailed.json` - Full JSON data
- `error_reports/YYYYMMDD_HHMMSS/priority_fixes.md` - Priority fix recommendations

### 2. `quick_error_summary.py` - Fast Package Summary

Quick script that shows error counts per package without detailed analysis.

**Usage:**

```bash
poetry run python scripts/analysis/quick_error_summary.py
```

### 3. `analyze_errors.sh` - Convenience Runner

Shell script that runs the full analysis and opens the report.

**Usage:**

```bash
./scripts/analysis/analyze_errors.sh
```

## Error Categories

### Severity Levels

1. **Critical** - Will definitely break at runtime
   - Import errors (module not found)
   - Attribute errors on None
   - Missing required arguments
   - Undefined variables
   - Type mismatches in function calls

2. **Medium** - May cause runtime issues
   - General type mismatches
   - Potential attribute errors
   - Operator type issues

3. **Type-only** - Won't break at runtime
   - Unknown types
   - Type annotation issues
   - Literal type mismatches
   - Generic type problems

### Error Types

1. **Import Errors**
   - Missing modules
   - Circular imports
   - Failed relative imports

2. **Type Errors**
   - Type annotation mismatches
   - Generic type issues
   - Return type problems

3. **Attribute Errors**
   - Accessing non-existent attributes
   - None type attribute access
   - Wrong object type

4. **Other Errors**
   - Syntax issues
   - Function call problems
   - Variable issues

## Example Output

```
=== Pyright Error Analysis Summary ===

Total Errors: 19,099
Total Warnings: 1,567

⚠️  Runtime Breaking Errors: 8,234
   These errors WILL cause crashes when the code runs!

Error Categories:
  Import errors: 5,432
  Type errors: 7,123
  Attribute errors: 3,456
  Other errors: 3,088

Top 5 Packages with Errors:
  haive-agents         ████████████████████████████ 7,238
  haive-games          █████████████████████ 5,264
  haive-core           ███████████████████ 4,701
  haive-dataflow       ███ 650
  haive-mcp            ██ 573
```

## Quick Fixes

The analyzer identifies common patterns that can be fixed systematically:

1. **Missing typing imports**

   ```python
   from typing import Any, Optional, Dict, List, Union
   ```

2. **Missing Pydantic imports**

   ```python
   from pydantic import Field, field_validator
   ```

3. **Field syntax fixes**

   ```python
   # Wrong
   field: str = Field(None, description="...")

   # Correct
   field: str = Field(default=None, description="...")
   ```

## Interpreting Results

1. **Focus on Critical Errors First**
   - These WILL crash your application
   - Usually import and attribute errors

2. **Package Priority**
   - Fix packages with the most errors first
   - Or fix critical packages (haive-core) first

3. **Common Patterns**
   - Look for errors that appear many times
   - These can often be fixed with find/replace

4. **Type-Only Errors**
   - Can be addressed later
   - Won't affect runtime behavior
   - Improve code quality and IDE support
