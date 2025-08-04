# Import Format Issues - July 20, 2025

**Date Discovered**: 2025-07-20
**Priority**: Critical
**Status**: Active
**Affected Files**: 5 files with invalid import syntax

## Problem Description

Several files contain invalid import statements using the format `from haive-prebuilt.src.haive.prebuilt.module` which causes Python syntax errors. This appears to be a result of incorrect automated changes.

## Affected Files

### 1. packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py

```python
# ❌ BROKEN (Line 24)
from haive-prebuilt.src.haive.prebuilt.tldr2.models import (
    # This causes SyntaxError: invalid syntax
```

### 2. packages/haive-prebuilt/src/haive/prebuilt/tldr2/engines.py

```python
# ❌ BROKEN (Line 23)
from haive-prebuilt.src.haive.prebuilt.tldr2.models import (
    # This causes SyntaxError: invalid syntax
```

### 3. packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py

```python
# ❌ BROKEN (Line 30)
from haive-prebuilt.src.haive.prebuilt.tldr2.engines import create_all_engines
    # This causes SyntaxError: invalid syntax
```

### 4. Other haive-prebuilt files with similar patterns

- Similar issues exist in other prebuilt modules
- All follow the same broken pattern

## Root Cause Analysis

This issue was likely caused by:

1. **Automated text replacement** that incorrectly modified import paths
2. **Package name confusion** between `haive-prebuilt` (package directory) and `haive.prebuilt` (Python module)
3. **Overly aggressive find-replace** operations

## Correct Import Format

The correct import format follows Python module conventions:

```python
# ✅ CORRECT - Standard Python module path
from haive.prebuilt.tldr2.models import SomeModel
from haive.prebuilt.tldr2.engines import create_all_engines

# ❌ WRONG - Invalid syntax with hyphens and src paths
from haive-prebuilt.src.haive.prebuilt.tldr2.models import SomeModel
```

## Solution Approach

### Manual Fix Process (NO AUTOMATION)

For each affected file:

1. **Open file in editor**
2. **Locate broken import line**
3. **Replace manually** with correct format:

   ```python
   # Change this:
   from haive-prebuilt.src.haive.prebuilt.MODULE.submodule import Item

   # To this:
   from haive.prebuilt.MODULE.submodule import Item
   ```

4. **Test compilation**: `poetry run python -m py_compile [file]`
5. **Verify imports work**: `poetry run python -c "from haive.prebuilt.MODULE import Item"`

### Fix Commands (Reference Only)

```bash
# Test individual file compilation
poetry run python -m py_compile packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py

# Test import after fix
poetry run python -c "from haive.prebuilt.tldr2.models import TLDRState"
```

## Prevention Strategy

### Code Review Checklist

- [ ] All imports use proper `haive.package.module` format
- [ ] No imports contain hyphens or `src` paths
- [ ] All imports tested with `poetry run python -c "import ..."`

### Standards Reference

Follow the import patterns in:

- `project_docs/active/standards/coding/COMMAND_EXECUTION_GUIDE.md`
- Existing working files in the same package

## Related Issues

- [Compilation Errors](../../compilation_errors/by_date/2025-07-20/pycompile_failures.md)
- [Parse Error Recovery](../../../memory_index/by_date/2025-07-20/parse_error_recovery_session.md)
- [Package Structure](../../architecture_problems/by_date/2025-07-20/package_organization.md)

## Resolution Checklist

### Phase 1: Fix Critical Files

- [ ] packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py
- [ ] packages/haive-prebuilt/src/haive/prebuilt/tldr2/engines.py
- [ ] packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py

### Phase 2: Verify Fixes

- [ ] Test compilation of each fixed file
- [ ] Test import statements work correctly
- [ ] Run related tests if they exist

### Phase 3: Prevention

- [ ] Document correct import patterns
- [ ] Add to code review checklist
- [ ] Update development standards

## Testing After Fixes

```bash
# Test each file individually
poetry run python -m py_compile packages/haive-prebuilt/src/haive/prebuilt/tldr2/state.py
poetry run python -m py_compile packages/haive-prebuilt/src/haive/prebuilt/tldr2/engines.py
poetry run python -m py_compile packages/haive-prebuilt/src/haive/prebuilt/tldr2/agent.py

# Test imports work
poetry run python -c "from haive.prebuilt.tldr2 import models, engines"
```

---

**Critical**: These must be fixed manually, file by file. NO automated find-replace operations.
**Next Action**: Start with tldr2/state.py and work through each file individually.
