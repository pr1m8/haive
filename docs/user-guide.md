# PyAutoDoc User Guide

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Basic Usage](#basic-usage)
5. [Advanced Features](#advanced-features)
6. [Monorepo Documentation](#monorepo-documentation)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

## Overview

PyAutoDoc is a comprehensive documentation system built on top of Sphinx, designed to automatically generate beautiful, cross-referenced documentation for Python projects and monorepos.

### Key Features

- **Automatic API Documentation**: Extracts docstrings and generates API docs
- **Monorepo Support**: Build documentation for multiple packages with cross-references
- **Rich Extensions**: 70+ Sphinx extensions pre-configured
- **Multiple Output Formats**: HTML, PDF, ePub, and more
- **Theme Customization**: Beautiful themes with package-specific branding
- **Cross-Package Linking**: Automatic intersphinx references

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/pyautodoc.git
cd pyautodoc

# Install dependencies
pip install -r requirements.txt

# Build all documentation
python scripts/build-monorepo-docs.py

# View the documentation
open _build/html/index.html
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip or poetry
- Git

### Install from Source

```bash
# Clone the repository
git clone https://github.com/yourusername/pyautodoc.git
cd pyautodoc

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Install with Poetry

```bash
# Install poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

## Basic Usage

### Single Package Documentation

To document a single Python package:

```bash
# Build specific package
python scripts/build-monorepo-docs.py --package haive-core

# Clean build
python scripts/build-monorepo-docs.py --package haive-core --clean
```

### Monorepo Documentation

To build documentation for all packages:

```bash
# Build all packages in parallel
python scripts/build-monorepo-docs.py

# Sequential build (useful for debugging)
python scripts/build-monorepo-docs.py --no-parallel

# Clean build
python scripts/build-monorepo-docs.py --clean
```

### Configuration

Each package should have a `docs/conf.py` file:

```python
# docs/conf.py
import sys
from pathlib import Path

# Add shared config to path
sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))

# Import shared configuration
from shared_config_simple import get_base_config

# Get base configuration
config = get_base_config(
    package_name="haive-core",
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

# Apply configuration
globals().update(config)

# Package-specific customizations
extensions.append('autoapi.extension')
autoapi_dirs = [str(Path(__file__).parents[1] / "src")]
```

## Advanced Features

### Custom Themes

PyAutoDoc supports package-specific theming:

```python
# In your package's conf.py
html_theme_options = {
    'light_css_variables': {
        'color-brand-primary': '#dc3545',  # Red for core
        'color-brand-content': '#c82333',
    }
}
```

### Cross-Package References

Reference other packages in your documentation:

```rst
See :py:class:`haive.core.DataProcessor` for details.

Link to :doc:`haive-ml:index` for ML documentation.
```

### Custom Extensions

Add package-specific extensions:

```python
# For CLI packages
extensions.append('sphinx_click')

# For API documentation
extensions.append('sphinxcontrib.openapi')

# For Jupyter notebooks
extensions.append('nbsphinx')
```

### Build Options

```bash
# Parallel builds with custom workers
python scripts/build-monorepo-docs.py -j 8

# Skip root documentation
python scripts/build-monorepo-docs.py --no-root

# Build specific packages only
python scripts/build-monorepo-docs.py -p haive-core -p haive-ml
```

## Monorepo Documentation

### Directory Structure

```
pyautodoc/
├── docs/                    # Root documentation
│   ├── conf.py
│   ├── index.rst
│   └── ...
├── packages/               # Individual packages
│   ├── haive-core/
│   │   ├── docs/
│   │   │   ├── conf.py
│   │   │   └── index.rst
│   │   └── src/
│   ├── haive-ml/
│   │   ├── docs/
│   │   └── src/
│   └── haive-api/
│       ├── docs/
│       └── src/
├── shared-docs-config/     # Shared configuration
│   ├── shared_config.py
│   └── shared_config_simple.py
├── scripts/
│   └── build-monorepo-docs.py
└── _build/                 # Build output
    ├── html/              # Root docs
    └── packages/          # Package docs
```

### Package Discovery

Packages are automatically discovered if they:

1. Are in the `packages/` directory
2. Have a `pyproject.toml` file
3. Have a `docs/` directory

### Dependency Resolution

The build system automatically:

- Detects inter-package dependencies
- Builds packages in the correct order
- Sets up cross-references

## API Reference

### Build Script Options

```bash
python scripts/build-monorepo-docs.py [OPTIONS]

Options:
  -h, --help            Show help message
  -c, --clean           Clean build directory before building
  -p, --package PKG     Build specific package only
  --no-parallel         Build sequentially
  -j, --max-workers N   Maximum parallel workers (default: 4)
  --no-root            Skip root documentation
```

### Configuration API

```python
from shared_config_simple import get_base_config

# Basic usage
config = get_base_config(
    package_name="my-package",
    package_path="/path/to/package/src",
    is_root=False
)

# Available options
config = {
    'project': 'Package Name',
    'extensions': [...],
    'html_theme': 'sphinx_rtd_theme',
    'intersphinx_mapping': {...},
    # ... many more
}
```

## Troubleshooting

### Common Issues

#### 1. Module Import Errors

**Problem**: `ModuleNotFoundError` when building docs

**Solution**:

```python
# In conf.py, ensure src path is added
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
```

#### 2. Missing Dependencies

**Problem**: Extension not found errors

**Solution**:

```bash
# Install all required extensions
pip install -r requirements.txt
```

#### 3. Build Failures

**Problem**: Documentation fails to build

**Solution**:

```bash
# Clean build and try again
python scripts/build-monorepo-docs.py --clean

# Check specific package
python scripts/build-monorepo-docs.py -p package-name
```

#### 4. Cross-References Not Working

**Problem**: Links between packages don't work

**Solution**:

- Ensure all packages are built
- Check intersphinx_mapping configuration
- Verify package names match

### Debug Mode

Enable verbose output:

```bash
# Set logging level
export SPHINX_DEBUG=1
python scripts/build-monorepo-docs.py
```

### Getting Help

1. Check the logs in `_build/` directory
2. Review Sphinx warnings and errors
3. Ensure all packages have proper `__init__.py` files
4. Verify docstring format (Google/NumPy style)

## Best Practices

1. **Consistent Docstrings**: Use Google-style docstrings
2. **Type Hints**: Always include type hints
3. **Examples**: Provide code examples in docstrings
4. **Cross-References**: Link related documentation
5. **Version Control**: Keep docs in sync with code

## Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License.
