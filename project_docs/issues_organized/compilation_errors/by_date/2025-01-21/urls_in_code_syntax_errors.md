# URLs in Code Syntax Errors

**Date Discovered**: 2025-01-21
**Priority**: High
**Status**: Active
**Package(s)**: haive-prebuilt, haive-agents

## Problem Description

18 files contain bare URLs in Python code causing SyntaxError due to invalid syntax.

Example error:

```
File "packages/haive-prebuilt/src/haive/prebuilt/blog_writer_agent/__init__.py", line 17
    https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/blog_writer_swarm.ipynb
          ^^
SyntaxError: invalid syntax
```

## Impact

- **Compilation**: 18 files fail to compile
- **Package Loading**: Prevents module imports
- **Documentation**: URLs should be in comments or docstrings

## Affected Files Pattern

Files with bare URLs (not in strings or comments):

- `blog_writer_agent/__init__.py`
- `clause_ai/__init__.py`
- `graph_inspector/__init__.py`
- `scientific_paper_agent/example.py`
- Additional files in haive-agents package

## Root Cause

URLs were likely intended to be in comments or docstrings but are written as bare code statements.

## Solution Approach

### Option 1: Move to Comments

```python
# Reference: https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/blog_writer_swarm.ipynb
```

### Option 2: Move to Module Docstring

```python
"""Module for blog writer agent.

Based on: https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/blog_writer_swarm.ipynb
"""
```

### Option 3: String Constant

```python
SOURCE_URL = "https://github.com/NirDiamant/GenAI_Agents/blob/main/all_agents_tutorials/blog_writer_swarm.ipynb"
```

## Implementation Steps

1. **Identify all URL lines** in affected files
2. **Determine intent** (documentation vs code)
3. **Apply appropriate fix** (comment, docstring, or string)
4. **Test compilation** after each fix

## Automation Potential

Could be partially automated with regex:

```bash
# Find lines with bare URLs
grep -n "^[[:space:]]*https://" packages/*/src/**/*.py
```

## Related Issues

- **Documentation Standards**: URLs should follow documentation guidelines
- **Code Quality**: Bare statements in code indicate incomplete implementation

## Resolution Notes

_To be filled when resolved_
