# Docstring Indentation Fixes Summary

Fixed docstring formatting issues in the following files to resolve Sphinx documentation build errors:

## Files Fixed

### 1. `/packages/haive-agents/src/haive/agents/react/agent_v3.py`

**Issue**: Missing blank line before code block in `build_graph` method docstring
- Line ~415: Changed from markdown-style code block to RST code-block directive
- Added proper blank line before code block
- Fixed "Key Differences" list formatting with proper blank line

### 2. `/packages/haive-agents/src/haive/agents/multi/clean.py`

**Issue**: Missing blank line and improper indentation in `add_conditional_edges` method
- Line ~594: Added "Basic routing function::" label before code example
- Added proper blank line between label and code block

### 3. `/packages/haive-agents/src/haive/agents/multi/core/clean_multi_agent.py`

**Issue**: Same as clean.py - missing blank line in `add_conditional_edges` method
- Line ~597: Added "Basic routing function::" label before code example
- Added proper blank line between label and code block

### 4. `/packages/haive-agents/src/haive/agents/patterns/sequential_with_structured_output.py`

**Issue**: Missing proper formatting in module-level docstring examples
- Line ~7: Added "Common sequential patterns::" label
- Added proper indentation for the list items

## RST Docstring Best Practices Applied

1. **Code blocks**: Use `.. code-block:: text` or `.. code-block:: python` instead of markdown-style triple backticks
2. **Examples section**: Always add a label ending with `::` before code examples
3. **Blank lines**: Always have a blank line before and after code blocks
4. **Lists**: Ensure proper blank line before bulleted lists

## Common Pattern Fixed

```python
# Before (incorrect):
Examples:
    def my_function():
        pass

# After (correct):
Examples:
    Basic usage::

        def my_function():
            pass
```

These fixes ensure that Sphinx can properly parse and render the docstrings in the generated documentation.