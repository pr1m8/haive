# PyAutoDoc Quick Reference

## Command Reference

### Build Commands

```bash
# Build all packages
python scripts/build-monorepo-docs.py

# Clean build (removes previous build)
python scripts/build-monorepo-docs.py --clean

# Build specific package
python scripts/build-monorepo-docs.py -p haive-core

# Sequential build (no parallelization)
python scripts/build-monorepo-docs.py --no-parallel

# Custom worker count
python scripts/build-monorepo-docs.py -j 8

# Skip root documentation
python scripts/build-monorepo-docs.py --no-root
```

### Directory Structure

```
pyautodoc/
├── _build/                 # Generated docs (git-ignored)
│   ├── html/              # Root HTML docs
│   └── packages/          # Package HTML docs
├── docs/                  # Root documentation source
├── packages/              # Package sources
│   └── package-name/
│       ├── docs/         # Package documentation
│       │   ├── conf.py   # Sphinx configuration
│       │   └── index.rst # Main documentation
│       └── src/          # Source code
├── scripts/              # Build scripts
└── shared-docs-config/   # Shared configuration
```

## Configuration Quick Reference

### Minimal Package conf.py

```python
import sys
from pathlib import Path

# Add shared config
sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))
from shared_config_simple import get_base_config

# Get configuration
config = get_base_config(
    package_name="my-package",
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

# Apply
globals().update(config)

# Add autoapi
extensions.append('autoapi.extension')
autoapi_dirs = [str(Path(__file__).parents[1] / "src")]
```

### Common Customizations

```python
# Custom theme colors
html_theme_options['light_css_variables'].update({
    'color-brand-primary': '#007bff',
    'color-brand-content': '#0056b3',
})

# Add extensions
extensions.extend([
    'sphinx_click',           # For CLI docs
    'sphinxcontrib.openapi',  # For API specs
    'nbsphinx',              # For Jupyter notebooks
])

# Custom static files
html_static_path = ['_static']
html_css_files = ['custom.css']

# Intersphinx mappings
intersphinx_mapping.update({
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
})
```

## Writing Documentation

### RST Quick Reference

```rst
Title
=====

Subtitle
--------

**Bold** and *italic* text.

Code block::

    def hello():
        print("Hello, world!")

Inline code: ``variable_name``

Links: `Python <https://python.org>`_

Cross-references:
- :doc:`other-page`
- :py:class:`module.ClassName`
- :py:func:`module.function_name`

.. note::
   This is a note.

.. warning::
   This is a warning.

.. code-block:: python
   :linenos:

   # Python code with line numbers
   def example():
       pass
```

### Markdown Support

````markdown
# Title

## Subtitle

**Bold** and _italic_ text.

```python
def hello():
    print("Hello, world!")
```
````

Inline code: `variable_name`

Links: [Python](https://python.org)

:::note
This is a note.
:::

:::warning
This is a warning.
:::

````

### Docstring Format

```python
def function_name(param1: str, param2: int = 0) -> dict:
    """Brief description of function.

    Longer description explaining what the function does,
    any important details, algorithm used, etc.

    Args:
        param1: Description of param1.
        param2: Description of param2 (default: 0).

    Returns:
        Description of return value.

    Raises:
        ValueError: When param1 is empty.
        TypeError: When param2 is not an integer.

    Examples:
        Basic usage::

            result = function_name("test", 42)
            print(result['status'])

        With error handling::

            try:
                result = function_name("")
            except ValueError:
                print("Invalid input")
    """
````

## API Endpoint Quick Reference

### Request Formats

```python
# ML Prediction
{
    "samples": [
        {"feature1": 1.0, "feature2": 2.0}
    ]
}

# Data Processing
{
    "data": {
        "field1": "value",
        "field2": 123
    }
}

# Batch Operations
{
    "operations": [
        {"type": "predict", "data": {...}},
        {"type": "process", "data": {...}}
    ]
}
```

### Response Format

```python
# Success
{
    "success": true,
    "data": {...},  # or "predictions", "processed_data", etc.
    "metadata": {
        "endpoint": "ml",
        "request_id": 123
    }
}

# Error
{
    "success": false,
    "error": "Error message",
    "error_type": "ValidationError",
    "metadata": {...}
}
```

### Size Limits

- Max samples per ML request: 100
- Max sample size: 10KB
- Max data payload: 50KB
- Max batch operations: 50
- Rate limit: 100 requests/minute

## Environment Variables

```bash
# Debug mode
export PYAUTODOC_DEBUG=1

# Custom build directory
export PYAUTODOC_BUILD_DIR=/path/to/build

# Parallel workers
export PYAUTODOC_MAX_WORKERS=8
```

## Troubleshooting Checklist

1. **Import Errors**
   - [ ] Check sys.path in conf.py
   - [ ] Verify **init**.py files exist
   - [ ] Ensure src/ directory structure

2. **Build Failures**
   - [ ] Run with --clean flag
   - [ ] Check for syntax errors in RST/MD
   - [ ] Verify all extensions installed

3. **Missing API Docs**
   - [ ] Check autoapi_dirs configuration
   - [ ] Verify docstrings present
   - [ ] Ensure modules are importable

4. **Cross-Reference Issues**
   - [ ] Build all packages first
   - [ ] Check intersphinx_mapping
   - [ ] Use correct reference syntax

## Useful Commands

```bash
# Check RST syntax
rst-lint docs/**/*.rst

# Test specific module import
python -c "from haive.core import DataProcessor"

# List all packages
ls -la packages/

# Find all conf.py files
find . -name "conf.py" -type f

# Clean all builds
rm -rf _build/

# Watch for file changes and rebuild
watchmedo shell-command \
    --patterns="*.py;*.rst;*.md" \
    --recursive \
    --command='python scripts/build-monorepo-docs.py' \
    .
```

## VS Code Integration

`.vscode/settings.json`:

```json
{
  "restructuredtext.confPath": "${workspaceFolder}/docs",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "files.associations": {
    "*.rst": "restructuredtext"
  },
  "esbonio.sphinx.buildDir": "${workspaceFolder}/_build"
}
```

## Common Patterns

### Adding New Module to Package

1. Create module file: `src/package_name/new_module.py`
2. Add to `__init__.py`: `from .new_module import *`
3. Write docstrings
4. Rebuild docs

### Creating Cross-Package Link

```rst
# In haive-ml docs
See :py:class:`haive.core.DataProcessor` for processing details.

# In haive-api docs
Uses :doc:`haive-ml:index` for ML capabilities.
```

### Custom Landing Page

```rst
.. toctree::
   :hidden:
   :maxdepth: 2

   user-guide
   api-reference
   examples

Welcome to MyPackage
====================

.. grid:: 2
   :gutter: 2

   .. grid-item-card:: Getting Started
      :link: user-guide
      :link-type: doc

      Learn how to use MyPackage

   .. grid-item-card:: API Reference
      :link: api-reference
      :link-type: doc

      Complete API documentation
```
