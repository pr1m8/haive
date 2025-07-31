# Sphinx Configuration Modularization Plan

## Current State

The current `conf.py` is 1101 lines with these major sections:

1. **Path Setup** (lines 1-83)
   - Logging configuration
   - Warning suppression
   - Package discovery
   - sys.path management

2. **Project Information** (lines 84-94)
   - Basic metadata

3. **Extensions** (lines 95-185)
   - Core API documentation
   - Enhanced documentation features
   - Notebooks and examples
   - External integrations
   - ~40+ extensions total

4. **General Configuration** (lines 186-218)
   - File patterns, templates, etc.

5. **HTML/Theme Configuration** (lines 219-406)
   - Furo theme with extensive customization
   - Sidebar configuration
   - CSS variables

6. **Extension Configurations** (lines 407-898)
   - AutoAPI (180+ lines)
   - Napoleon
   - Autodoc & Type hints
   - Doctest
   - Coverage
   - TODO
   - External TOC
   - MyST Parser
   - Copy button
   - Design elements
   - Tabs
   - Toggle button
   - Favicon
   - Mermaid
   - Gallery
   - Jupyter
   - Exec directive
   - Needs
   - Open Graph
   - Sitemap
   - Code autolink
   - Search
   - Intersphinx
   - Mock imports

7. **LaTeX/PDF Configuration** (lines 899-906)

8. **Utility Functions** (lines 907-1075)
   - Skip patterns
   - Mock missing imports
   - Event handlers

9. **Setup Function** (lines 1076-1101)

## Modularization Strategy

### Option 1: Feature-Based Modules (Recommended)

```
docs/source/
├── conf.py                    # Main entry point (50 lines)
├── conf.d/                    # Configuration modules
│   ├── __init__.py
│   ├── core.py               # Paths, project info, logging
│   ├── extensions.py         # Extension lists by category
│   ├── theme.py              # HTML/Furo theme config
│   ├── api.py                # AutoAPI + autodoc config
│   ├── documentation.py      # MyST, notebooks, examples
│   ├── quality.py            # Testing, coverage, spelling
│   ├── external.py           # Intersphinx, links, social
│   ├── utilities.py          # Helper functions, handlers
│   └── presets/              # Pre-configured combinations
│       ├── minimal.py        # Bare minimum
│       ├── standard.py       # Common setup
│       ├── full.py           # Everything enabled
│       └── api_only.py       # Just API docs
```

### Option 2: Layer-Based Modules

```
docs/source/
├── conf.py                    # Main entry point
├── sphinx_config/
│   ├── __init__.py
│   ├── layer1_core.py        # Essential setup
│   ├── layer2_extensions.py  # Basic extensions
│   ├── layer3_theme.py       # Visual configuration
│   ├── layer4_api.py         # API documentation
│   ├── layer5_features.py    # Advanced features
│   └── layer6_custom.py      # Project-specific
```

### Option 3: Component Registry

```python
# conf.py
from sphinx_config import ConfigRegistry

registry = ConfigRegistry()

# Register components
registry.use("core")
registry.use("furo_theme")
registry.use("autoapi")
registry.use("jupyter_support")

# Apply configuration
locals().update(registry.build())
```

## Benefits of Modularization

1. **Maintainability**: Find and modify specific settings easily
2. **Reusability**: Share configurations across projects
3. **Testing**: Test configuration components individually
4. **Documentation**: Document each module's purpose
5. **Flexibility**: Mix and match features
6. **Performance**: Load only needed components
7. **Version Control**: Track changes to specific features

## Implementation Plan

### Phase 1: Create Module Structure

1. Create `conf.d/` directory
2. Extract core configuration
3. Group extensions by purpose
4. Move theme configuration

### Phase 2: Create Presets

1. Minimal configuration (200 lines)
2. Standard configuration (500 lines)
3. Full configuration (1000+ lines)
4. Special-purpose configs

### Phase 3: Add Builder/Registry

1. Configuration builder class
2. Component registry
3. Dependency resolution
4. Validation

### Phase 4: Migration Tools

1. Config analyzer
2. Migration script
3. Comparison tool
4. Documentation

## Example Usage After Modularization

### Minimal Setup

```python
# conf.py
from conf.d import minimal
locals().update(minimal.config)
```

### Custom Setup

```python
# conf.py
from conf.d import core, theme, api, documentation

config = {}
config.update(core.get_config())
config.update(theme.get_furo_config())
config.update(api.get_autoapi_config(
    packages=["haive-core", "haive-agents"]
))
config.update(documentation.get_myst_config())

locals().update(config)
```

### Builder Pattern

```python
# conf.py
from conf.d import SphinxConfig

config = (SphinxConfig()
    .with_project("Haive", "1.0.0")
    .with_theme("furo")
    .with_extensions(["autoapi", "myst", "jupyter"])
    .with_custom("html_logo", "logo.png")
    .build())

locals().update(config)
```

## Next Steps

1. Choose modularization approach
2. Create directory structure
3. Start extracting components
4. Test with simple project
5. Create migration guide
6. Update documentation
