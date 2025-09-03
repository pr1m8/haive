# Documentation Build Issues

**Generated**: August 1, 2025

This directory contains individual issue files for documentation build problems. Each issue can be worked on independently by different agents or developers.

## Critical Issues (Blocks Build)

1. **[sphinx_math_dollar_crash.md](sphinx_math_dollar_crash.md)** - CRITICAL
   - NotImplementedError preventing HTML generation
   - Must be fixed first to generate any documentation

## High Priority Issues

2. **[type_hint_references.md](type_hint_references.md)** - HIGH
   - 18,896 type reference warnings
   - Partial fix already applied (autodoc_typehints)
   - Needs nitpick_ignore expansion

3. **[import_errors.md](import_errors.md)** - HIGH
   - Missing dependencies (google-search-results)
   - Module not found errors
   - Circular imports

## Medium Priority Issues

4. **[pydantic_validators.md](pydantic_validators.md)** - MEDIUM
   - Invalid validator signatures in grade models
   - Clear fix pattern available

5. **[build_process.md](build_process.md)** - MEDIUM
   - Phased build improvements needed
   - Add debug vs strict modes
   - Re-enable phases 3 & 4

## How to Work on Issues

Each issue file contains:

- Problem description
- Root cause analysis
- Proposed solutions
- Files to modify
- Testing commands
- Success criteria

## Priority Order

1. Fix sphinx_math_dollar first (blocks everything)
2. Then work on any other issues in parallel
3. Build process improvements can be done anytime

## Testing

After fixing any issue:

```bash
poetry run nox -s docs_phased
```

## Full Report

See [../documentation_issues_2025_08_01.md](../documentation_issues_2025_08_01.md) for the comprehensive report.
