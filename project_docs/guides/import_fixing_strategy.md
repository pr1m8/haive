# Import Fixing Strategy for Haive Core

## Overview

This document outlines our comprehensive strategy for fixing the import issues in haive-core that are causing Sphinx AutoAPI documentation errors. The strategy uses a combination of automated tools and targeted fixes.

## Problem Analysis

### Current Issues:
1. **Missing __all__ exports** in various __init__.py files
2. **Incomplete module exposure** - __init__.py files not importing submodules (utils, types, tools, schema, runtime, etc.)
3. **Sphinx AutoAPI errors** - "ValueError: not enough values to unpack (expected 2, got 1)"
4. **Import structure** - Need to expose modules, not just select classes

### Root Cause:
The main issue is that our __init__.py files are only exposing select classes rather than the full module structure. Sphinx AutoAPI expects to find properly structured modules with complete imports.

## Implementation Strategy

### Phase 1: Syntax Verification (py_compile)
- Run py_compile on all Python files to establish baseline
- Identify any existing syntax errors before making changes
- Create a map of files that need attention

### Phase 2: Auto Import Fixing (autoimport)
- Use autoimport tool to automatically fix missing imports
- Run on all files with syntax errors first
- Then run on all files to catch import issues
- Verify syntax after each fix with py_compile

### Phase 3: __init__.py Analysis
- Analyze all __init__.py files to understand current structure
- Identify missing module imports
- Map out which submodules exist but aren't exposed
- Focus on key modules: utils, types, tools, schema, runtime, models, registry, etc.

### Phase 4: __init__.py Enhancement
- Add missing module imports using `from . import module_name`
- Update __all__ exports to include module names
- Implement lazy loading pattern where appropriate
- Maintain backward compatibility with existing imports

### Phase 5: Verification
- Re-run py_compile on all files
- Test imports manually
- Run Sphinx AutoAPI to verify documentation builds

## Tool Selection Rationale

### 1. autoimport (Primary Tool)
- **Why**: Already installed, actively maintained, fixes imports automatically
- **Usage**: `poetry run autoimport [--check] file.py`
- **Benefits**: 
  - Handles both missing and unused imports
  - Preserves code style
  - Can run in check-only mode first

### 2. py_compile (Verification)
- **Why**: Built-in Python tool, lightweight syntax checker
- **Usage**: `python -m py_compile file.py`
- **Benefits**:
  - Fast syntax verification
  - No external dependencies
  - Catches syntax errors before runtime

### 3. Manual __init__.py Updates
- **Why**: autoimport doesn't handle module-level imports in __init__.py
- **Approach**: Semi-automated with AST parsing
- **Benefits**:
  - Precise control over module exposure
  - Can implement lazy loading patterns
  - Maintains project structure

## Implementation Script

The implementation is in `/home/will/Projects/haive/backend/haive/scripts/maintenance/fix_imports_implementation_plan.py`

Key features:
- Color-coded output for easy reading
- Phased approach with verification at each step
- Preserves existing code structure
- Focuses on the specific pattern needed (exposing modules not just classes)

## Expected Outcomes

1. **All __init__.py files** will properly import their submodules
2. **Module exposure** - Can import like `from haive.core import utils, types, schema`
3. **Sphinx AutoAPI** will successfully parse the module structure
4. **No syntax errors** - All files will pass py_compile validation
5. **Backward compatibility** - Existing imports will continue to work

## Alternative Approaches Considered

### mkinit
- **Pros**: Powerful __init__.py generator, supports static/dynamic generation
- **Cons**: Might be overkill for our needs, requires learning new tool
- **Decision**: Keep as backup option if manual approach fails

### absolufy-imports
- **Pros**: Converts relative to absolute imports
- **Cons**: Not actively maintained, doesn't solve our __init__.py issue
- **Decision**: Not suitable for our specific problem

### python-module-loader
- **Pros**: Dynamic module loading
- **Cons**: More suited for plugin systems, adds runtime complexity
- **Decision**: Too complex for our needs

## Execution Plan

1. **Backup current state**: Create git stash or branch
2. **Run the implementation script**: `poetry run python scripts/maintenance/fix_imports_implementation_plan.py`
3. **Review changes**: Check git diff for all modifications
4. **Test imports**: Run sample imports to verify
5. **Run documentation build**: `poetry run sphinx-build -b html docs/source docs/build/html`
6. **Commit changes**: If successful, commit with clear message

## Success Criteria

- [ ] All Python files in haive-core pass py_compile
- [ ] autoimport reports no issues when run in check mode
- [ ] All __init__.py files import their submodules
- [ ] Module imports work: `from haive.core import utils, schema, types`
- [ ] Sphinx AutoAPI builds without import errors
- [ ] Existing imports continue to work

## Rollback Plan

If issues arise:
1. `git stash` to save changes
2. `git reset --hard HEAD` to revert
3. Analyze what went wrong
4. Adjust script and try again

## Notes

- The user emphasized: "we almost have to build it up the other way" - meaning expose modules first, then specific exports
- Focus on making sure __init__.py files import submodules, not just define classes
- Be careful and research before making big changes (as requested by user)
- Use py_compile to verify quality before and after changes