# Documentation Build Fixes

This directory contains chronological documentation of all major build fixes and improvements.

## 📋 Fix History

### [2025-01-16 Major Build Fixes](2025-01-16_major_build_fixes.md)

**Impact**: 🚀 97% error reduction

**Key Achievements**:

- ✅ Resolved critical `KeyError: 'containers_tilebag'`
- ✅ Fixed AutoAPI/autosummary conflicts
- ✅ Enabled Sphinx Gallery with package examples
- ✅ Fixed Python syntax errors in example files
- ✅ Enhanced Furo theme with showcase styling

**Results**:

- Errors: 195 → 3 (98.5% reduction)
- Warnings: 475 → 5 (97% reduction)
- Build Status: ✅ Successful

### [Previous Build Success](previous_build_success.md)

Earlier documentation build improvements and successes.

## 🔧 Common Issues & Solutions

### 1. KeyError in AutoAPI

**Symptom**: `KeyError: 'module_name'` during build
**Cause**: Files with invalid Python module names (spaces, parentheses)
**Solution**: Remove or rename files with invalid names

### 2. AutoAPI/Autosummary Conflicts

**Symptom**: Duplicate or conflicting documentation entries
**Cause**: Manual autosummary directives in AutoAPI-generated files
**Solution**: Remove manual directives, let AutoAPI handle generation

### 3. Syntax Errors in Examples

**Symptom**: AST parsing failures, SyntaxError in build
**Cause**: Malformed Python code in example files
**Solution**: Fix syntax or add to `autoapi_ignore` list

### 4. Gallery Configuration Issues

**Symptom**: Examples not showing in documentation
**Cause**: Incorrect `sphinx_gallery_conf` settings
**Solution**: Configure proper example directories and patterns

## 📊 Build Metrics Tracking

| Date       | Errors | Warnings | Build Time | Status |
| ---------- | ------ | -------- | ---------- | ------ |
| 2025-01-16 | 3      | 5        | ~2 min     | ✅     |
| 2025-01-15 | 195    | 475      | Failed     | ❌     |

## 🚀 Best Practices

1. **Always test locally** before pushing documentation changes
2. **Check for invalid file names** when adding new modules
3. **Run syntax checks** on example files
4. **Keep autoapi_ignore updated** for problematic files
5. **Monitor build logs** for new warnings

## 🔍 Debugging Commands

```bash
# Check for syntax errors
find packages -name "*.py" -exec python -m py_compile {} \; 2>&1 | grep -E "Error|Sorry"

# Find files with invalid names
find . -name "*\ *" -o -name "*(*" -o -name "*)*"

# Test specific module import
poetry run python -c "import haive.module.submodule"

# Quick documentation build
poetry run sphinx-build -b html docs/source docs/build/html -W --keep-going
```
