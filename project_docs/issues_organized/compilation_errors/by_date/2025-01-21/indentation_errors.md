# Indentation Errors

**Date Discovered**: 2025-01-21
**Priority**: High
**Status**: Active
**Package(s)**: haive-prebuilt, haive-agents

## Problem Description

10 files have indentation-related compilation errors:

- **Unexpected indent**: 4 files
- **Missing indented block**: 2 files
- **General indentation**: 6 files

## Impact

- **Compilation**: Files fail with IndentationError
- **Code Structure**: Indicates incomplete or malformed code blocks
- **Maintainability**: Makes code unreadable

## Affected Files

### Unexpected Indent (4 files)

- `packages/haive-prebuilt/src/haive/prebuilt/project_manager/aug_llms.py:17`
- `packages/haive-prebuilt/src/haive/prebuilt/perplexity/base/engines.py:304`
- `packages/haive-prebuilt/src/haive/prebuilt/startup/agent.py:240`
- `packages/haive-prebuilt/src/haive/prebuilt/scientific_paper_agent/nodes.py:1`

### Missing Indented Block (2 files)

- `packages/haive-agents/src/haive/agents/reasoning_and_critique/lats/example.py:87`
- `packages/haive-agents/src/haive/agents/reasoning_and_critique/tot/modular/example.py:25`

## Root Cause Analysis

Likely causes:

1. **Automated fixes gone wrong**: July 20 parse error fixes may have corrupted indentation
2. **Incomplete code blocks**: if/for statements without proper bodies
3. **Mixed tabs/spaces**: Inconsistent indentation characters

## Solution Approach

### Step 1: Automated Analysis

```bash
# Check for mixed tabs/spaces
python -tt affected_file.py

# Use trunk to auto-fix
trunk check --fix packages/haive-prebuilt packages/haive-agents
```

### Step 2: Manual Review

For each file:

1. **Examine the error line** and surrounding context
2. **Identify the intended structure** (missing colon, incomplete block, etc.)
3. **Fix manually** if automated tools can't resolve

### Step 3: Validation

```bash
poetry run python -m py_compile affected_file.py
```

## Example Fixes

### Missing Block After if:

```python
# Before (error)
if condition:
# Missing indented block

# After (fixed)
if condition:
    pass  # or appropriate implementation
```

### Unexpected Indent:

```python
# Before (error)
def function():
return value
    extra_line  # unexpected indent

# After (fixed)
def function():
    return value
    # extra_line removed or properly indented
```

## Priority Order

1. **Scientific paper agent nodes.py:1** - Error on line 1 is critical
2. **Missing blocks in example files** - Break functionality
3. **Unexpected indents** - Fix formatting

## Automation Strategy

Most indentation errors can be fixed with:

```bash
# Use autopep8 for aggressive indentation fixing
poetry run autopep8 --aggressive --aggressive --in-place affected_file.py

# Or use black for consistent formatting
poetry run black affected_file.py
```

## Related Issues

- **Code Formatting Standards**: Need consistent indentation policy
- **Pre-commit Hooks**: Should catch indentation errors before commit

## Resolution Notes

_To be filled when resolved_
