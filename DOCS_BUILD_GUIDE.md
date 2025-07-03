# Documentation Build Guide

This guide explains how to build and serve the Haive documentation using nox and Sphinx.

## Prerequisites

1. **Install nox** (if not already installed):

   ```bash
   pip install nox
   # or
   pipx install nox
   ```

2. **Install Poetry** (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

## Building Documentation

### Quick Start

```bash
# Build documentation
nox -s docs

# Serve documentation with auto-reload
nox -s docs_serve

# Clean build artifacts
nox -s docs_clean
```

## Available Nox Sessions

### 1. Build Documentation (`nox -s docs`)

Builds the HTML documentation using Sphinx.

```bash
nox -s docs
```

Output will be in `docs/build/html/`

### 2. Serve Documentation (`nox -s docs_serve`)

Builds and serves documentation with auto-reload on changes.

```bash
nox -s docs_serve
```

- Access at: http://localhost:8000
- Auto-reloads on file changes
- Press Ctrl+C to stop

### 3. Clean Documentation (`nox -s docs_clean`)

Removes all build artifacts.

```bash
nox -s docs_clean
```

### 4. Check Links (`nox -s docs_check`)

Checks for broken links and references.

```bash
nox -s docs_check
```

### 5. Check Coverage (`nox -s docs_coverage`)

Checks documentation coverage for Python API.

```bash
nox -s docs_coverage
```

## Using Make (Alternative)

If you prefer using Make:

```bash
cd docs

# Build HTML docs
make html

# Serve with auto-reload
make livehtml

# Clean build
make clean
```

## Troubleshooting Common Issues

### Issue 1: Missing Dependencies

**Error**: `ModuleNotFoundError: No module named 'sphinx'`

**Solution**:

```bash
poetry install --with docs
```

### Issue 2: Build Warnings

**Error**: `WARNING: document isn't included in any toctree`

**Solution**: Add the document to an appropriate `index.rst` or toctree directive.

### Issue 3: Import Errors

**Error**: `ImportError: cannot import name 'SomeClass'`

**Solution**: Ensure all packages are installed:

```bash
poetry install
```

### Issue 4: Theme Not Found

**Error**: `Theme 'sphinx_rtd_theme' not found`

**Solution**:

```bash
poetry add --group docs sphinx-rtd-theme
```

### Issue 5: Mermaid Diagrams Not Rendering

**Error**: Mermaid diagrams show as code blocks

**Solution**: Ensure mermaid extension is enabled in `conf.py`:

```python
extensions = [
    # ... other extensions
    'sphinxcontrib.mermaid',
]
```

## Documentation Structure

```
docs/
├── Makefile              # Make commands
├── source/              # Source files
│   ├── conf.py         # Sphinx configuration
│   ├── index.rst       # Main index
│   ├── api/            # API documentation
│   ├── guides/         # User guides
│   └── agents/         # Agent documentation
└── build/              # Build output (git-ignored)
    └── html/           # HTML output
```

## Writing Documentation

### Adding New Pages

1. Create `.rst` or `.md` file in appropriate directory
2. Add to a toctree in `index.rst` or parent document
3. Build to verify

### Using Sphinx Features

- **Cross-references**: `:doc:`guide_name``
- **Code blocks**: Use `.. code-block:: python`
- **API docs**: Use `.. automodule::` directives
- **Mermaid diagrams**: Use `.. mermaid::` directive

## CI/CD Integration

To build docs in CI:

```yaml
# GitHub Actions example
- name: Build Documentation
  run: |
    pip install nox
    nox -s docs

- name: Upload Documentation
  uses: actions/upload-artifact@v3
  with:
    name: documentation
    path: docs/build/html/
```

## Best Practices

1. **Always build locally** before pushing
2. **Check for warnings** - use `-W` flag to treat as errors
3. **Update toctrees** when adding new documents
4. **Use consistent formatting** (RST vs Markdown)
5. **Include code examples** with proper syntax highlighting
6. **Add cross-references** to related documentation

## Advanced Usage

### Custom Themes

To use a custom theme, update `conf.py`:

```python
html_theme = 'sphinx_rtd_theme'  # or your preferred theme
```

### Internationalization

For multi-language docs:

```bash
# Extract translatable strings
make gettext

# Update translations
sphinx-intl update -p build/gettext -l es
```

### PDF Generation

To generate PDF documentation:

```bash
# Install LaTeX dependencies first
nox -s docs -- -b latexpdf
```

## Getting Help

- **Sphinx Documentation**: https://www.sphinx-doc.org/
- **Nox Documentation**: https://nox.thea.codes/
- **Project Issues**: Check project repository

---

For more information, see the [main documentation](./CLAUDE.md) or [quick reference](./project_docs/claude_documentation/CLAUDE_QUICKREF.md).
