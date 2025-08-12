# Haive Monorepo Documentation Strategy

This document outlines the comprehensive documentation architecture implemented for the Haive ecosystem monorepo structure.

## Overview

The Haive ecosystem follows a **modular monorepo architecture** where:

- Each package maintains its own independent documentation
- Root-level documentation aggregates and cross-links all packages
- Shared configuration ensures consistency across the ecosystem
- Advanced build system handles complex interdependencies

## Architecture

```
haive/                                  # Monorepo root
├── packages/                           # Package directory
│   ├── haive-core/                    # Core package
│   │   ├── src/haive/core/            # Source code
│   │   ├── docs/                      # Package documentation
│   │   │   ├── conf.py               # Package-specific config
│   │   │   ├── index.rst             # Package main page
│   │   │   └── examples/             # Package examples
│   │   └── pyproject.toml            # Package metadata
│   ├── haive-ml/                     # ML package
│   │   ├── src/haive/ml/             # Source code
│   │   ├── docs/                     # Package documentation
│   │   └── pyproject.toml
│   └── haive-api/                    # API package
│       ├── src/haive/api/            # Source code
│       ├── docs/                     # Package documentation
│       └── pyproject.toml
├── shared-docs-config/                # Shared configuration system
│   ├── shared_config.py              # Base Sphinx configuration
│   └── __init__.py
├── docs/                             # Root documentation
│   ├── conf.py                      # Root Sphinx configuration
│   ├── index.rst                    # Ecosystem overview
│   └── _static/                     # Shared assets
├── scripts/                          # Build automation
│   └── build-monorepo-docs.py       # Advanced build system
└── _build/                           # Build output
    ├── packages/                     # Individual package docs
    │   ├── haive-core/
    │   ├── haive-ml/
    │   └── haive-api/
    └── html/                         # Root documentation
```

## Key Components

### 1. Shared Configuration System

**File: `shared-docs-config/shared_config.py`**

Provides centralized configuration management:

- Base Sphinx extensions (70+ extensions)
- Common theme and styling
- Intersphinx mappings
- AutoAPI configuration
- Custom Jinja2 macros

```python
def get_base_config(package_name: str, package_path: str, is_root: bool = False) -> Dict[str, Any]:
    """Get base Sphinx configuration for a package."""
```

### 2. Package-Level Documentation

Each package has its own `docs/conf.py` that:

- Imports shared configuration
- Adds package-specific customizations
- Configures AutoAPI for the package
- Sets up cross-package references

**Example Package Config:**

```python
from shared_config import get_base_config

config = get_base_config(
    package_name="haive-core",
    package_path=str(PACKAGE_PATH),
    is_root=False
)
globals().update(config)

# Package-specific customizations
project = "Haive Core"
html_title = "Haive Core Documentation"
```

### 3. Root-Level Aggregation

**File: `docs/conf.py`**

The root configuration:

- Aggregates all package documentation
- Provides ecosystem overview
- Sets up comprehensive intersphinx mappings
- Manages cross-package references

### 4. Advanced Build System

**File: `scripts/build-monorepo-docs.py`**

Features include:

- **Dependency-aware building**: Respects package dependencies
- **Parallel processing**: Builds packages concurrently when possible
- **Comprehensive error reporting**: Detailed error categorization
- **Build caching**: Incremental builds for efficiency
- **Cross-package linking**: Automatic intersphinx setup

**Usage Examples:**

```bash
# Build all packages
python scripts/build-monorepo-docs.py

# Clean build
python scripts/build-monorepo-docs.py --clean

# Build specific package
python scripts/build-monorepo-docs.py --package haive-core

# Parallel build with custom workers
python scripts/build-monorepo-docs.py --max-workers 8

# Sequential build (for debugging)
python scripts/build-monorepo-docs.py --no-parallel
```

## Documentation Structure

### Package Documentation Pattern

Each package follows this structure:

```rst
Package Name
============

Quick Start
-----------
- Installation
- Basic Usage

Core Components
---------------
- Main classes with autoclass directives
- Cross-references to other packages

Advanced Features
-----------------
- Complex usage patterns
- Integration examples

API Reference
-------------
- Complete autoapi documentation

Examples & Tutorials
-------------------
- Practical examples
- Step-by-step tutorials
```

### Root Documentation Pattern

```rst
Haive Ecosystem
===============

Architecture Overview
--------------------
- Ecosystem diagram
- Package relationships

Quick Start
-----------
- Complete integration example

Package Documentation
--------------------
- Links to individual packages
- Cross-package patterns

Development Guide
-----------------
- Setup instructions
- Contributing guidelines

Comprehensive API Reference
---------------------------
- All packages combined
```

## Cross-Package Integration

### 1. Intersphinx Linking

Packages can reference each other using standard Sphinx syntax:

```rst
:class:`haive.core.BaseModel`          # Reference to core package
:doc:`haive-ml:tutorials/training`     # Reference to ML tutorials
:meth:`haive.api.APIServer.add_endpoint`  # Reference to API method
```

### 2. Shared Extensions

All packages benefit from shared extensions:

- `sphinx-autoapi` for automatic API documentation
- `sphinx-copybutton` for code copying
- `myst-parser` for Markdown support
- `sphinx-design` for modern layouts
- `sphinx-notfound-page` for custom 404 pages
- Many more (70+ extensions total)

### 3. Consistent Theming

- Unified RTD theme configuration
- Shared CSS and JavaScript
- Consistent navigation patterns
- Common favicon and logos

## Development Workflow

### Adding a New Package

1. **Create package structure:**

   ```bash
   mkdir -p packages/haive-new/{src/haive/new,docs}
   ```

2. **Create pyproject.toml with dependencies:**

   ```toml
   [tool.poetry.dependencies]
   haive-core = {path = "../haive-core", develop = true}
   ```

3. **Create docs/conf.py:**

   ```python
   from shared_config import get_base_config
   config = get_base_config("haive-new", str(PACKAGE_PATH))
   globals().update(config)
   ```

4. **Create docs/index.rst with package overview**

5. **Build system automatically discovers the package**

### Modifying Shared Configuration

1. **Update `shared-docs-config/shared_config.py`**
2. **All packages automatically inherit changes**
3. **Test with:** `python scripts/build-monorepo-docs.py --clean`

### Building Documentation

```bash
# Development build (fast)
python scripts/build-monorepo-docs.py

# Production build (clean, all packages)
python scripts/build-monorepo-docs.py --clean --max-workers 4

# Debug build (sequential, single package)
python scripts/build-monorepo-docs.py --no-parallel --package haive-core
```

## Production Deployment

### CI/CD Integration

```yaml
name: Build Documentation
on: [push, pull_request]

jobs:
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install --with docs

      - name: Build documentation
        run: |
          python scripts/build-monorepo-docs.py --clean

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_build/html
```

### Hosting Strategy

- **Root docs** at `https://docs.haive.ai/`
- **Package docs** at subdirectories:
  - `https://docs.haive.ai/core/`
  - `https://docs.haive.ai/ml/`
  - `https://docs.haive.ai/api/`
- **Cross-linking** works seamlessly between all levels

## Advanced Features

### 1. Automatic CLI Documentation

The system detects CLI entry points and generates documentation:

- Uses `sphinx-argparse` for argument parsing
- Integrates with `sphinx-prompt` for command examples
- Automatically discovers CLI tools in packages

### 2. Enhanced Error Reporting

Build system provides comprehensive error reporting:

- Categorizes warnings vs errors
- Shows context for build failures
- Suggests fixes for common issues
- Tracks build performance metrics

### 3. Dependency Management

- **seed-intersphinx-mapping** integration
- Automatic discovery of cross-references
- Pre-commit hooks for dependency sync
- Trunk.io integration for development workflow

### 4. Custom Extensions

Includes custom extensions for:

- **Model detection** (Pydantic, dataclasses)
- **CLI documentation** generation
- **Cross-package** reference validation
- **Build optimization** and caching

## Benefits

### For Developers

- **Single command** builds entire ecosystem docs
- **Consistent** documentation patterns
- **Automatic** cross-package linking
- **Fast** incremental builds

### For Users

- **Unified** documentation experience
- **Easy** navigation between packages
- **Complete** API reference in one place
- **Rich** examples and tutorials

### For Maintainers

- **Modular** architecture allows independent updates
- **Shared** configuration reduces duplication
- **Automated** build system prevents errors
- **Comprehensive** monitoring and reporting

## Future Enhancements

### Short Term (v0.2.0)

- Interactive API explorer
- Live code examples
- Version-specific documentation
- Search improvements

### Long Term (v0.3.0+)

- Multi-language support
- Automated screenshot generation
- Performance benchmarking docs
- AI-powered documentation assistance

## Conclusion

This monorepo documentation strategy provides:

1. **Scalability**: Easy to add new packages
2. **Consistency**: Shared configuration and patterns
3. **Maintainability**: Centralized tooling and automation
4. **User Experience**: Unified, cross-linked documentation
5. **Developer Experience**: Simple workflow and comprehensive tooling

The implementation demonstrates advanced Sphinx usage and provides a template for other complex documentation projects.
