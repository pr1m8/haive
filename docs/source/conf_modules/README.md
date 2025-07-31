# Modular Sphinx Configuration

This directory contains a modular approach to Sphinx configuration, breaking down the monolithic 1100+ line conf.py into focused, manageable modules.

## Structure Plan

```
conf_modules/
├── README.md                    # This file
├── __init__.py                  # Package marker
├── core/
│   ├── __init__.py
│   ├── paths.py                 # Path setup and sys.path management
│   ├── project.py               # Project metadata (name, version, etc.)
│   └── logging.py               # Logging configuration
├── extensions/
│   ├── __init__.py
│   ├── core_sphinx.py           # Core Sphinx extensions
│   ├── api_generation.py        # AutoAPI, autodoc, napoleon
│   ├── documentation.py         # MyST, jupyter, notebooks
│   ├── testing.py               # Doctest, coverage, spell checking
│   ├── enhancement.py           # Copybutton, tabs, design
│   ├── external.py              # Intersphinx, opengraph, sitemap
│   └── custom.py                # Custom extensions
├── themes/
│   ├── __init__.py
│   ├── furo.py                  # Furo theme configuration
│   └── html.py                  # HTML output settings
├── processing/
│   ├── __init__.py
│   ├── markdown.py              # MyST parser configuration
│   ├── notebooks.py             # Jupyter notebook processing
│   └── autoapi.py               # AutoAPI configuration
├── quality/
│   ├── __init__.py
│   ├── doctest.py               # Doctest configuration
│   ├── coverage.py              # Documentation coverage
│   ├── spelling.py              # Spell checking
│   └── linkcheck.py             # Link checking
├── utilities/
│   ├── __init__.py
│   ├── mock_imports.py          # Mock imports for missing deps
│   ├── warnings.py              # Warning suppression
│   └── helpers.py               # Utility functions
└── conf_simple.py               # Simple all-in-one config
```

## Benefits

1. **Modularity**: Each aspect in its own file
2. **Reusability**: Import only what you need
3. **Maintainability**: Easy to find and modify settings
4. **Flexibility**: Mix and match configurations
5. **Testing**: Test individual components
6. **Documentation**: Each module can be documented

## Usage Patterns

### Full Configuration (like current)

```python
# conf.py
from conf_modules import create_full_config
locals().update(create_full_config())
```

### Minimal Configuration

```python
# conf.py
from conf_modules.core import project, paths
from conf_modules.themes import furo
from conf_modules.extensions import core_sphinx

# Apply configurations
locals().update(project.config)
locals().update(paths.config)
locals().update(furo.config)
locals().update(core_sphinx.config)
```

### Custom Mix

```python
# conf.py
from conf_modules import (
    get_core_config,
    get_api_config,
    get_theme_config,
)

config = {}
config.update(get_core_config())
config.update(get_api_config(packages=["haive-core", "haive-agents"]))
config.update(get_theme_config(theme="furo"))

locals().update(config)
```

## Migration Strategy

1. Create module structure
2. Extract configurations into modules
3. Create aggregator functions
4. Test with simple projects first
5. Gradually adopt in main project
