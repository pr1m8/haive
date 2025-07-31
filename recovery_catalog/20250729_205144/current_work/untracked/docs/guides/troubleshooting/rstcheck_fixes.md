# RST Documentation Fix Plan

## Overview

The rstcheck analysis revealed 4 main categories of issues:
1. **Sphinx directive recognition** (195+ false positives)
2. **Python code syntax errors** (20+ real issues)
3. **RST formatting problems** (30+ real issues)
4. **Template file issues** (can be ignored)

## Phase 1: Configure rstcheck (5 minutes)

### Create rstcheck configuration

Add to `pyproject.toml`:

```toml
[tool.rstcheck]
# Ignore Sphinx-specific directives
ignore_directives = [
    "automodule", "autoclass", "autofunction", "autoexception",
    "autodata", "automethod", "autoattribute", "autosummary",
    "grid", "grid-item", "grid-item-card", "exec_code",
    "agent-doc", "automodsumm", "toctree", "code-block",
    "literalinclude", "include", "image", "figure",
    "tabs", "tab", "card", "dropdown", "button-ref"
]

# Ignore Sphinx roles
ignore_roles = [
    "class", "func", "meth", "attr", "exc", "obj",
    "mod", "data", "ref", "doc", "term", "download"
]

# Skip template files and generated files
ignore_paths = [
    "docs/source/_templates/**",
    "docs/source/sg_*",
    "docs/build/**"
]

# Set to warning level to reduce noise
report_level = "warning"
```

This will eliminate ~80% of the false positives.

## Phase 2: Fix Critical Python Syntax Errors (30 minutes)

### 2.1 Fix `await` outside function (7 files)

**Files to fix:**
- `docs/source/guides/rag_agents.rst` (5 instances)
- `docs/source/examples/index.rst` (2 instances)

**Pattern to apply:**

```rst
# BEFORE:
.. code-block:: python

   result = await agent.arun("Query")

# AFTER:
.. code-block:: python

   async def example():
       result = await agent.arun("Query")
       return result

# OR use sync version:
.. code-block:: python

   result = agent.run("Query")  # Sync version
```

### 2.2 Fix indentation errors (4 files)

**Files to fix:**
- `docs/source/getting_started.rst:140`
- `docs/source/guides/rag_agents.rst:322, 364, 458`

**Pattern to apply:**

```rst
# BEFORE:
.. code-block:: python

   class MyAgent:
   def __init__(self):  # Missing indent

# AFTER:
.. code-block:: python

   class MyAgent:
       def __init__(self):
           pass
```

## Phase 3: Fix RST Formatting Issues (20 minutes)

### 3.1 Fix title underlines (3 files)

**Files to fix:**
- `docs/source/getting_started.rst` (lines 88, 125, 212)
- `docs/source/beta_status.rst`

**Pattern:**
```rst
# Ensure underline matches title length
Title Text
==========  # Must be at least as long as title
```

### 3.2 Fix missing blank lines

**Common issues:**
- Block quotes need blank lines before and after
- Definition lists need blank lines
- Transitions between different block types

**Pattern:**
```rst
# BEFORE:
.. note:: Something
Next paragraph

# AFTER:
.. note:: Something

Next paragraph
```

### 3.3 Fix inline literal issues

**File:** `docs/source/development/todo.rst` (line 111)

Check for unclosed inline literals:
```rst
# BEFORE:
Some ``code without closing

# AFTER:
Some ``code`` with closing
```

## Phase 4: Automated Fixes (10 minutes)

### Create fix script

```python
#!/usr/bin/env python3
"""Fix common RST issues automatically."""

import re
from pathlib import Path

def fix_await_outside_function(content):
    """Wrap standalone await statements in async functions."""
    # Pattern for standalone await in code blocks
    pattern = r'(\.\. code-block:: python\n\n)([ ]*)(.*await\s+.*?)(\n\n)'
    
    def replace_await(match):
        indent = match.group(2)
        await_line = match.group(3)
        
        # Check if already in a function
        if 'def ' in match.group(0) or 'async ' in match.group(0):
            return match.group(0)
        
        # Wrap in async function
        return (f"{match.group(1)}{indent}async def example():\n"
                f"{indent}    {await_line}\n{match.group(4)}")
    
    return re.sub(pattern, replace_await, content, flags=re.MULTILINE)

def fix_title_underlines(content):
    """Fix title underline lengths."""
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        if i > 0 and i < len(lines) - 1:
            prev_line = lines[i-1]
            next_line = lines[i] if i < len(lines) - 1 else ""
            
            # Check if current line is an underline
            if (line and all(c in '=-~^"' for c in line.strip()) and 
                prev_line and not prev_line.startswith(' ')):
                # Make underline match title length
                char = line.strip()[0]
                fixed_lines.append(char * len(prev_line))
                continue
        
        fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def process_file(filepath):
    """Process a single RST file."""
    content = filepath.read_text()
    original = content
    
    # Apply fixes
    content = fix_await_outside_function(content)
    content = fix_title_underlines(content)
    
    # Save if changed
    if content != original:
        filepath.write_text(content)
        print(f"Fixed: {filepath}")

# Process all RST files
for rst_file in Path('docs/source').rglob('*.rst'):
    if '_templates' not in str(rst_file):
        process_file(rst_file)
```

## Phase 5: Manual Review (15 minutes)

### Files requiring manual attention:

1. **`docs/source/beta_status.rst`** - Complex formatting issues
2. **`docs/source/development/todo.rst`** - Inline literal problems
3. **Any file with "Unknown directive" after configuration**

### Checklist:

- [ ] All `await` statements are inside async functions
- [ ] All code blocks have proper indentation
- [ ] All titles have matching underlines
- [ ] All block elements have proper spacing
- [ ] All inline literals are properly closed

## Phase 6: Validation (5 minutes)

### Re-run rstcheck with configuration:

```bash
poetry run rstcheck -r docs/ --config pyproject.toml
```

### Run doc8 for additional validation:

```bash
poetry run doc8 docs/source/
```

### Build docs to ensure no breaking changes:

```bash
nox -s docs
```

## Expected Outcomes

After implementing this plan:

1. **False positives eliminated**: ~195 Sphinx directive warnings gone
2. **Real syntax errors fixed**: ~20 Python code issues resolved
3. **Formatting improved**: ~30 RST structure issues fixed
4. **Build success**: Documentation builds without errors

## Time Estimate

- **Total time**: ~1.5 hours
- **Automated fixes**: 45 minutes
- **Manual fixes**: 30 minutes
- **Validation**: 15 minutes

## Priority Order

1. **Configure rstcheck** - Eliminates noise
2. **Fix Python syntax** - These are real errors
3. **Fix RST formatting** - Improves quality
4. **Run validation** - Ensures success

The most critical issues are the Python syntax errors in code examples, as these will confuse users. The Sphinx directive warnings are mostly false positives that will disappear with proper configuration.