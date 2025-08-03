# Documentation Build Process Issues

**Date**: August 1, 2025  
**Priority**: MEDIUM - Process improvements needed  
**Status**: Open

## Problem

The phased documentation build has issues:

1. **Phase 3 (Extension Test)** uses `-W` flag treating warnings as errors
2. **Phase 4 (Content Validation)** builds gettext instead of checking content
3. **No option for non-strict builds** during debugging

## Current Workaround

Phases 3 & 4 are currently skipped to allow HTML generation.

## Proposed Solutions

### 1. Add Build Mode Options

```python
# In session_docs_phased.py
if "strict" in session.posargs:
    warning_flags = ["-W"]  # Treat warnings as errors
else:
    warning_flags = []  # Allow warnings during debug
```

### 2. Fix Phase 3 Extension Test

- Remove `-W` flag by default
- Add option to enable strict mode
- Better error reporting

### 3. Fix Phase 4 Content Validation

- Change from gettext to actual content checks
- Validate cross-references
- Check for broken links

### 4. Add Debug Mode

```bash
# Debug mode with verbose output, no strict checks
poetry run nox -s docs_phased -- debug

# Strict mode for CI
poetry run nox -s docs_phased -- strict
```

## Files to Modify

- `/noxfiles/session_docs_phased.py` - Main build logic

## Implementation

1. Add command-line argument parsing
2. Conditional `-W` flag based on mode
3. Better phase descriptions
4. More granular error reporting

## Testing

```bash
# Test debug mode
poetry run nox -s docs_phased -- debug

# Test strict mode
poetry run nox -s docs_phased -- strict
```

## Success Criteria

- Can run build without `-W` for debugging
- Clear separation between debug and production builds
- All phases provide useful feedback
- Phases 3 & 4 can be re-enabled
