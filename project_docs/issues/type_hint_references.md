# Type Hint Reference Resolution Issue

**Date**: August 1, 2025
**Priority**: HIGH - 18,896 warnings
**Status**: Open (Partial Fix Applied)

## Problem

Sphinx is generating thousands of warnings for unresolved type references, particularly for basic Python types like `str`, `int`, `bool`, etc.

## Impact

- 18,896 missing-reference warnings in extension test phase
- Build fails with `-W` flag (warnings as errors)
- Documentation quality degraded

## Root Cause

1. **autodoc_typehints was set to "none"** - This disabled all type hint processing
2. Missing nitpick_ignore entries for basic types
3. Intersphinx not properly configured for Python built-ins

## Already Fixed

Changed in `/docs/source/conf_modules/extension_configs.py`:

- `autodoc_typehints` from `"none"` to `"description"`
- Enabled parameter and return type documentation

## Still Needed

1. **Enhance nitpick_ignore list** in conf.py
2. **Configure intersphinx** for Python types
3. **Add type aliases** for complex generics
4. **Test with updated configuration**

## Proposed Solution

### 1. Expand nitpick_ignore

Add more entries to conf.py:

```python
nitpick_ignore.extend([
    ("py:class", "typing.Any"),
    ("py:class", "typing.Optional"),
    ("py:class", "typing.List"),
    ("py:class", "typing.Dict"),
    ("py:class", "typing.Union"),
    ("py:class", "typing.Callable"),
    # Add all missing types from warnings
])
```

### 2. Fix Intersphinx Mapping

Ensure Python stdlib is properly mapped:

```python
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    # ... other mappings
}
```

### 3. Handle Generic Types

Add type aliases for problematic generics like `Agent[T]`

## Files to Modify

- `/docs/source/conf.py` - nitpick_ignore list
- `/docs/source/conf_modules/extension_configs.py` - ✅ Already fixed

## Testing

```bash
# Run without -W flag first
poetry run sphinx-build -n -b gettext docs/source docs/build/test
```

## Success Criteria

- Warnings reduced from 18,896 to < 100
- Basic Python types resolve correctly
- Generic types handled gracefully
