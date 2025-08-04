# Invalid Import Format Errors

**Date Discovered**: 2025-01-21
**Priority**: Critical
**Status**: Active
**Package(s)**: haive-prebuilt

## Problem Description

5 files contain invalid import statements using the format:

```python
from haive-prebuilt.src.haive.prebuilt.module import something
```

This format is invalid Python syntax due to hyphens in module names.

## Impact

- **Compilation**: Files fail to compile with SyntaxError
- **Import System**: Breaks Python module resolution
- **Package Usage**: haive-prebuilt package unusable

## Affected Files

1. `packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py:24`
2. `packages/haive-prebuilt/src/haive/prebuilt/tldr2/engines.py:23`
3. `packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py:30`
4. (2 additional files from error log)

## Root Cause

Likely result of automated "parse error fixes" on July 20, 2025 that incorrectly modified import paths.

## Solution Approach

### Immediate Fix (Command)

```bash
find packages/haive-prebuilt -name "*.py" -exec sed -i 's/from haive-prebuilt\.src\.haive/from haive/g' {} \;
```

### Manual Verification

1. Check each affected file
2. Verify imports resolve correctly
3. Test compilation with `poetry run python -m py_compile`

## Expected Outcome

All 5 files should compile successfully after import path correction.

## Related Issues

- **Parse Error Recovery**: `memory_index/by_date/2025-07-20/parse_error_recovery_session.md`
- **July 20 Timeline**: Shows when these errors were introduced

## Resolution Notes

_To be filled when resolved_
