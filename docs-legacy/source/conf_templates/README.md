# Documentation Configuration Templates

This directory contains different Sphinx configuration templates for various documentation builds.

## Available Templates

### Furo Theme Configurations

- **`conf_furo_minimal.py`** - Ultra-minimal Furo build with NO AutoAPI
  - Fastest build, no API documentation
  - Good for testing theme and basic content

- **`conf_furo.py`** - Original Furo configuration
  - Basic Furo theme with AutoAPI
  - Automatic toctree generation
  - Standard configuration

- **`conf_furo_with_autoapi.py`** - Enhanced Furo configuration
  - Manual toctree control for better navigation
  - Enhanced Furo theme options
  - Improved sidebar navigation
  - Better integration with AutoAPI

## Usage with Nox Sessions

```bash
# Original Furo build
nox -s docs-furo

# Enhanced Furo build with improved navigation
nox -s docs-furo-enhanced

# Minimal Furo build (fastest)
nox -s docs-furo-minimal
```

## Build Outputs

Each configuration builds to its own directory:
- `docs/builds/furo_original/` - Original Furo build
- `docs/builds/furo_enhanced/` - Enhanced Furo build  
- `docs/builds/furo_minimal/` - Minimal Furo build

## Configuration Features

### Enhanced Configuration Features:
- `autoapi_add_toctree_entry = False` - Manual toctree control
- Enhanced Furo theme options for better navigation
- Improved sidebar settings
- Better integration with submodule builds (core.engine, etc.)

### Submodule Support:
All configurations support granular package building:
- `core.engine` - Just the engine module (fast)
- `core.schema` - Just the schema module
- `core` - Full core package
- `all` - All packages

Set via environment variable:
```bash
SPHINX_PACKAGES=core.engine nox -s docs-furo-enhanced
```