# Phase 1: Minimal Working Build

**Goal**: Establish a baseline with zero errors and working Furo theme

## Objectives

1. Remove all complexity
2. Get basic Sphinx + Furo working
3. Verify CSS layout is correct
4. No AutoAPI yet

## Configuration

### Minimal conf.py

```python
"""Minimal Sphinx configuration for testing."""

from pathlib import Path

# Basic project info
project = "Haive"
author = "William R. Astley"
copyright = "2025, William R. Astley"
version = "1.0"
release = "1.0.0"

# Minimal extensions
extensions = [
    "myst_parser",  # For Markdown support
]

# Theme
html_theme = "furo"
html_title = "Haive Documentation"

# Source file types
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# Master document
master_doc = "index"

# Exclude patterns
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Static files (start with none)
html_static_path = []
```

### Minimal index.rst

```rst
Haive Documentation
===================

Welcome to Haive documentation.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting_started

Getting Started
---------------

This is a test page.
```

### Create getting_started.md

````markdown
# Getting Started

This is a minimal page to test the build.

## Installation

```bash
pip install haive
```
````

## Basic Usage

```python
from haive import Agent
agent = Agent()
```

````

## Build Commands

```bash
# Clean previous build
rm -rf docs/build

# Build HTML
cd docs
sphinx-build -b html source build/html

# Check for errors
echo "Exit code: $?"
````

## Validation Checklist

- [ ] Build completes with exit code 0
- [ ] No errors in output
- [ ] No warnings (or < 5)
- [ ] HTML files generated:
  - [ ] index.html
  - [ ] getting_started.html
  - [ ] genindex.html
  - [ ] search.html

## CSS Validation

### Check Layout

1. Open `build/html/index.html` in browser
2. Verify:
   - [ ] Sidebar is reasonable width (~250-300px)
   - [ ] Content is centered, not pushed right
   - [ ] Code blocks use full width
   - [ ] Mobile responsive works

### Inspect CSS

```javascript
// In browser console
document.querySelector(".sidebar-drawer").offsetWidth;
// Should be ~250-300, not 494
```

## Common Issues

### Issue: Module Import Errors

**Solution**: This phase has no Python imports

### Issue: Extension Not Found

**Solution**: Ensure myst-parser is installed

```bash
pip install myst-parser
```

### Issue: Static File Errors

**Solution**: We're not using static files yet

## Success Criteria

✅ **Build Output**:

```
Running Sphinx v7.x.x
loading translations [en]... done
building [html]: targets for 2 source files
...
build succeeded.

The HTML pages are in build/html.
```

✅ **File Count**:

- 4-5 HTML files
- 0 errors
- < 5 warnings

✅ **Visual Check**:

- Sidebar normal width
- Content properly centered
- Clean Furo theme

## Next Steps

Once Phase 1 succeeds:

1. Save this configuration as baseline
2. Take screenshot of layout
3. Proceed to [Phase 2](./PHASE_2_CORE.md)

## Rollback Plan

If issues occur:

```bash
# Save current conf.py
cp docs/source/conf.py docs/source/conf_phase1_backup.py

# Restore if needed
cp docs/source/conf_minimal.py docs/source/conf.py
```

## Notes

- This phase proves Sphinx and Furo work correctly
- No Python code is imported or documented
- Pure documentation build only
- Establishes baseline metrics
