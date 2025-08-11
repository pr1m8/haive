# PyAutoDoc Developer Guide

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Components](#core-components)
3. [Adding New Packages](#adding-new-packages)
4. [Extending Functionality](#extending-functionality)
5. [Build System](#build-system)
6. [Testing Documentation](#testing-documentation)
7. [Security Considerations](#security-considerations)
8. [Performance Optimization](#performance-optimization)

## Architecture Overview

PyAutoDoc is built with a modular architecture designed for extensibility and maintainability.

### System Components

```
┌─────────────────────────────────────────────────────┐
│                  PyAutoDoc System                    │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐│
│  │   Shared    │  │    Build     │  │  Package   ││
│  │   Config    │  │   System     │  │   Docs     ││
│  └─────────────┘  └──────────────┘  └────────────┘│
│         ↓                ↓                 ↓        │
│  ┌─────────────────────────────────────────────┐  │
│  │           Sphinx Documentation Engine        │  │
│  └─────────────────────────────────────────────┘  │
│                         ↓                          │
│  ┌─────────────────────────────────────────────┐  │
│  │              Output (HTML/PDF/etc)           │  │
│  └─────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

### Key Design Principles

1. **DRY (Don't Repeat Yourself)**: Shared configuration across packages
2. **Convention over Configuration**: Sensible defaults with override capability
3. **Parallel Processing**: Build multiple packages concurrently
4. **Extensibility**: Easy to add new packages and features
5. **Security First**: Input validation and safe operations

## Core Components

### 1. Shared Configuration System

Located in `shared-docs-config/`:

```python
# shared_config_simple.py
def get_base_config(
    package_name: str,
    package_path: str,
    is_root: bool = False
) -> Dict[str, Any]:
    """
    Generate base Sphinx configuration.

    Features:
    - Error handling and validation
    - Path management
    - Extension configuration
    - Theme customization
    """
```

### 2. Build System

The `MonorepoDocsBuilder` class handles:

```python
class MonorepoDocsBuilder:
    """Advanced documentation builder for monorepo architecture."""

    def __init__(self, project_root: Path):
        # Package discovery
        # Dependency resolution
        # Build state management

    def build_all(self, parallel=True):
        # Parallel/sequential builds
        # Error recovery
        # Progress tracking
```

### 3. Package Structure

Each package must follow this structure:

```
package-name/
├── pyproject.toml       # Package metadata
├── src/                 # Source code
│   └── package_name/
│       ├── __init__.py
│       └── modules.py
├── docs/               # Documentation
│   ├── conf.py        # Sphinx config
│   ├── index.rst      # Main page
│   └── api.rst        # API docs
└── tests/             # Unit tests
```

## Adding New Packages

### Step 1: Create Package Structure

```bash
# Create new package directory
mkdir -p packages/haive-newpkg/{src/haive/newpkg,docs,tests}

# Create necessary files
touch packages/haive-newpkg/pyproject.toml
touch packages/haive-newpkg/src/haive/__init__.py
touch packages/haive-newpkg/src/haive/newpkg/__init__.py
```

### Step 2: Configure Package

Create `pyproject.toml`:

```toml
[tool.poetry]
name = "haive-newpkg"
version = "0.1.0"
description = "New package for Haive ecosystem"

[tool.poetry.dependencies]
python = "^3.8"
haive-core = {path = "../haive-core", develop = true}

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

### Step 3: Setup Documentation

Create `docs/conf.py`:

```python
import sys
from pathlib import Path

# Add shared config
sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))
from shared_config_simple import get_base_config

# Configure
config = get_base_config(
    package_name="haive-newpkg",
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

# Apply config
globals().update(config)

# Add package-specific settings
extensions.append('autoapi.extension')
autoapi_dirs = [str(Path(__file__).parents[1] / "src")]

# Custom theme colors
html_theme_options['light_css_variables'].update({
    'color-brand-primary': '#your-color',
    'color-brand-content': '#your-color-dark',
})
```

Create `docs/index.rst`:

```rst
Haive NewPkg Documentation
==========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   introduction
   quickstart
   api
   examples

Introduction
------------

Welcome to Haive NewPkg documentation.

Installation
------------

.. code-block:: bash

   pip install haive-newpkg
```

### Step 4: Build Documentation

```bash
# Build your new package
python scripts/build-monorepo-docs.py -p haive-newpkg

# Build all including new package
python scripts/build-monorepo-docs.py --clean
```

## Extending Functionality

### Adding Custom Extensions

1. **Install Extension**:

```bash
# Using pip
pip install sphinx-your-extension

# Using poetry (recommended)
poetry add --group docs sphinx-your-extension
```

2. **Update Shared Config**:

```python
# In shared_config_simple.py
'extensions': [
    # ... existing extensions
    'your_new_extension',
]
```

3. **Configure Extension**:

```python
# Extension-specific settings
config['your_extension_setting'] = 'value'
```

### Automatic Intersphinx Mapping

PyAutoDoc uses `seed-intersphinx-mapping` to automatically configure documentation links for all your dependencies:

```python
# No manual configuration needed!
# seed-intersphinx-mapping reads from pyproject.toml
# and automatically adds mappings for:
# - numpy, pandas, scipy (if used)
# - pydantic, fastapi (if used)
# - Any other dependencies with Sphinx docs
```

Benefits:

- Zero configuration for dependency links
- Always up-to-date with your dependencies
- Works across all packages in the monorepo

See [Seed Intersphinx Guide](seed-intersphinx-guide.md) for details.

### Creating Custom Themes

1. **Create Theme Directory**:

```
shared-docs-config/themes/custom-theme/
├── theme.conf
├── static/
│   └── custom.css
└── templates/
    └── layout.html
```

2. **Register Theme**:

```python
# In shared config
html_theme_path = [str(Path(__file__).parent / "themes")]
html_theme = "custom-theme"
```

### Adding Build Hooks

```python
# In build-monorepo-docs.py
class MonorepoDocsBuilder:
    def add_pre_build_hook(self, hook_func):
        """Add function to run before build."""
        self.pre_build_hooks.append(hook_func)

    def add_post_build_hook(self, hook_func):
        """Add function to run after build."""
        self.post_build_hooks.append(hook_func)
```

## Build System

### Build Pipeline

1. **Package Discovery**
   - Scan `packages/` directory
   - Validate package structure
   - Extract metadata

2. **Dependency Resolution**
   - Parse `pyproject.toml`
   - Build dependency graph
   - Determine build order

3. **Parallel Building**
   - Thread pool execution
   - Progress tracking
   - Error handling

4. **Output Generation**
   - HTML generation
   - Asset copying
   - Cross-linking

### Build Optimization

```python
# Incremental builds
class IncrementalBuilder:
    def should_rebuild(self, package: PackageConfig) -> bool:
        """Check if package needs rebuilding."""
        # Check file modifications
        # Check dependency changes
        # Check configuration changes
```

### Error Recovery

```python
# Graceful error handling
try:
    result = self._build_single_package(config)
except BuildError as e:
    # Log error
    # Continue with other packages
    # Report at end
```

## Testing Documentation

### Unit Tests for Documentation

```python
# tests/test_docs.py
import pytest
from pathlib import Path
from scripts.build_monorepo_docs import MonorepoDocsBuilder

def test_package_discovery():
    """Test that all packages are discovered."""
    builder = MonorepoDocsBuilder(Path(__file__).parent.parent)
    assert len(builder.packages) > 0
    assert 'haive-core' in builder.packages

def test_build_single_package():
    """Test building a single package."""
    builder = MonorepoDocsBuilder(Path(__file__).parent.parent)
    result = builder.build_package('haive-core')
    assert result.success
    assert result.output_dir.exists()
```

### Documentation Linting

```bash
# Check RST syntax
rst-lint docs/**/*.rst

# Check for broken links
sphinx-build -b linkcheck docs _build/linkcheck

# Spell checking
sphinx-build -b spelling docs _build/spelling
```

### Visual Testing

```python
# Screenshot comparison
from selenium import webdriver

def test_documentation_appearance():
    driver = webdriver.Chrome()
    driver.get("file:///path/to/_build/html/index.html")
    driver.save_screenshot("docs-screenshot.png")
    # Compare with baseline
```

## Security Considerations

### Input Validation

All user inputs are validated:

```python
def get_base_config(package_name: str, package_path: str, is_root: bool = False):
    # Validate inputs
    if not package_name:
        raise ValueError("package_name cannot be empty")

    package_path = Path(package_path)
    if not package_path.exists():
        raise ValueError(f"Package path does not exist: {package_path}")
```

### Safe File Operations

```python
@contextmanager
def temporary_chdir(path: Path):
    """Safely change directory."""
    original_cwd = Path.cwd()
    try:
        os.chdir(path)
        yield
    finally:
        os.chdir(original_cwd)
```

### API Security

Endpoints include:

- Rate limiting
- Input size validation
- Thread-safe operations
- Error message sanitization

```python
class RateLimiter:
    """Rate limit API requests."""
    def is_allowed(self, identifier: str) -> bool:
        # Check request rate
        # Enforce limits
```

## Performance Optimization

### Parallel Building

```python
# Optimize worker count
import multiprocessing
optimal_workers = min(
    len(packages),
    multiprocessing.cpu_count(),
    max_workers
)
```

### Caching

```python
# Cache build artifacts
class BuildCache:
    def get_cache_key(self, package: PackageConfig) -> str:
        # Generate cache key from:
        # - Source file hashes
        # - Configuration
        # - Dependencies

    def is_cached(self, package: PackageConfig) -> bool:
        # Check if build is cached
```

### Memory Management

```python
# Stream large files
def process_large_docs():
    with open('large_file.rst') as f:
        for chunk in iter(lambda: f.read(4096), ''):
            process_chunk(chunk)
```

### Build Profiling

```python
# Profile build times
import cProfile
import pstats

def profile_build():
    profiler = cProfile.Profile()
    profiler.enable()

    # Run build
    builder.build_all()

    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

## Best Practices

### Code Style

1. **Type Hints**: Always use type hints
2. **Docstrings**: Google-style with examples
3. **Error Handling**: Specific exceptions
4. **Logging**: Structured logging
5. **Testing**: Unit tests for all components

### Documentation Style

1. **Clear Structure**: Logical organization
2. **Code Examples**: Working examples
3. **Cross-References**: Link related content
4. **Versioning**: Track API changes
5. **Accessibility**: Follow WCAG guidelines

### Contribution Workflow

1. Fork the repository
2. Create feature branch
3. Write tests first
4. Implement feature
5. Update documentation
6. Submit pull request

## Debugging Tips

### Enable Debug Mode

```python
# Set environment variable
os.environ['PYAUTODOC_DEBUG'] = '1'

# Or in code
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

1. **Import Errors**: Check sys.path
2. **Missing Extensions**: Install requirements
3. **Build Failures**: Check logs
4. **Slow Builds**: Profile and optimize

### Debug Tools

```python
# Interactive debugging
import pdb; pdb.set_trace()

# Print build state
print(builder._debug_state())

# Validate configuration
validate_sphinx_config(config)
```
