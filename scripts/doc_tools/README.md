# Haive Documentation Tools

This directory contains tools for maintaining and enhancing documentation across the Haive framework.

## Available Tools

### `add_docstrings.py`

Automatically adds Google-style docstrings to Python modules, classes, and functions.

#### Features:

- Adds module-level docstrings to describe overall functionality
- Adds class docstrings with attributes and examples
- Adds function docstrings with arguments, return values, and examples
- Creates README.md files for modules
- Intelligently generates documentation based on naming conventions and context

#### Usage:

```bash
# Add docstrings to all files in a package
python scripts/doc_tools/add_docstrings.py --path packages/haive-games/src/haive/games

# Add docstrings to a specific module
python scripts/doc_tools/add_docstrings.py --path packages/haive-games/src/haive/games/chess

# Test what would be changed without modifying files
python scripts/doc_tools/add_docstrings.py --path packages/haive-core/src/haive/core --dry-run
```

## Templates

Documentation templates are available in the `templates` directory:

- `README_TEMPLATE.md` - Template for module-level README files
- `MODULE_DOCSTRING_TEMPLATE.txt` - Template for module-level docstrings

## Documentation Standards

For complete documentation on Haive's documentation standards and processes, see:

- [Documentation Guide](https://docs.haive.ai/en/latest/guides/documentation/index.html)
- [Docstring Standards](https://docs.haive.ai/en/latest/guides/documentation/docstring_standards.html)
- [Module READMEs](https://docs.haive.ai/en/latest/guides/documentation/module_readmes.html)

## Building Documentation

To build the full documentation:

```bash
# From the project root
nox -s docs

# For live documentation editing with auto-reload
nox -s docs-live

# For checking documentation without building
nox -s docs-check
```
