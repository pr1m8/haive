# PyAutoDoc Configuration Cleanup Migration Guide

## Overview

We've consolidated the PyAutoDoc configuration system from multiple overlapping systems into a single, unified configuration module. This guide helps you migrate to the new structure.

## What Changed

### Before (Multiple Systems)

- `shared_config.py` - Complex configuration with many features
- `shared_config_simple.py` - Simplified version with basic features
- `docs/conf.py` AND `docs/source/conf.py` - Duplicate root configs
- YAML-based configuration system (unused)
- Inconsistent theme and extension management

### After (Unified System)

- `unified_config.py` - Single configuration module for all needs
- One root configuration location
- Consistent theme management
- Centralized extension handling
- Clear package-specific overrides

## Migration Steps

### 1. Update Package conf.py Files

Replace your existing conf.py with this simplified version:

```python
"""Sphinx configuration for [package-name]."""
import sys
from pathlib import Path

# Add shared config to path
sys.path.insert(0, str(Path(__file__).parents[2] / "shared-docs-config"))

# Import unified configuration
from unified_config import create_sphinx_config

# Generate configuration
config = create_sphinx_config(
    package_name="haive-core",  # Your package name
    package_path=str(Path(__file__).parents[1] / "src"),
    is_root=False
)

# Apply configuration
globals().update(config)

# Package-specific additions (if needed)
extensions.append('autoapi.extension')
autoapi_dirs = [str(Path(__file__).parents[1] / "src")]
```

### 2. Update Root Documentation

For root documentation, use:

```python
"""Sphinx configuration for PyAutoDoc root documentation."""
import sys
from pathlib import Path

# Add shared config to path
sys.path.insert(0, str(Path(__file__).parent.parent / "shared-docs-config"))

# Import unified configuration
from unified_config import create_sphinx_config

# Generate configuration
config = create_sphinx_config(
    package_name="pyautodoc",
    package_path=str(Path(__file__).parent),
    is_root=True
)

# Apply configuration
globals().update(config)
```

### 3. Remove Redundant Files

Delete these files after migration:

- `shared-docs-config/shared_config.py` (after verifying migration)
- `shared-docs-config/shared_config_simple.py` (after verifying migration)
- `docs/source/` directory (if using `docs/conf.py` as root)
- YAML configuration files if not being used

## Configuration Options

### Basic Usage

```python
config = create_sphinx_config(
    package_name="my-package",
    package_path="/path/to/src",
    is_root=False
)
```

### Advanced Options

```python
config = create_sphinx_config(
    package_name="my-package",
    package_path="/path/to/src",
    is_root=False,
    enable_optional_extensions=True,  # Enable extra extensions
    theme='furo'  # or 'sphinx_rtd_theme'
)
```

### Package-Specific Customization

The unified config automatically handles:

- **Color Themes**: Each package gets its own color scheme
- **Extensions**: Package-specific extensions (CLI, API, ML)
- **Version Detection**: Reads from pyproject.toml
- **Cross-References**: Automatic intersphinx setup

## Benefits of the New System

1. **Single Source of Truth**: One configuration module to maintain
2. **Consistent Behavior**: All packages use the same base configuration
3. **Easy Customization**: Clear override points for package-specific needs
4. **Better Maintainability**: Less code duplication
5. **Automatic Features**: Version detection, color themes, cross-references

## Customization Guide

### Adding New Package Colors

In `unified_config.py`:

```python
PACKAGE_THEMES = {
    'haive-core': PackageColors('#dc3545', '#c82333'),
    'my-new-package': PackageColors('#17a2b8', '#138496'),  # Add here
}
```

### Adding Package-Specific Extensions

```python
PACKAGE_EXTENSIONS = {
    'haive-cli': ['sphinx_click'],
    'my-package': ['my_special_extension'],  # Add here
}
```

### Overriding in conf.py

You can still override any setting in your package's conf.py:

```python
# Get base config
config = create_sphinx_config(...)
globals().update(config)

# Override specific settings
html_theme_options['custom_setting'] = 'value'
extensions.append('additional_extension')
```

## Troubleshooting

### Import Errors

If you get import errors:

1. Verify the path to shared-docs-config is correct
2. Check that unified_config.py exists
3. Ensure Python path includes the shared config directory

### Missing Extensions

The unified config includes core extensions by default. To add more:

1. Set `enable_optional_extensions=True`
2. Or manually append to the extensions list

### Theme Issues

The default theme is 'furo'. To use RTD theme:

```python
config = create_sphinx_config(..., theme='sphinx_rtd_theme')
```

## Verification Checklist

After migration:

- [ ] All packages build successfully
- [ ] Root documentation builds
- [ ] Cross-references work between packages
- [ ] Themes display correctly
- [ ] Package-specific extensions load
- [ ] No import errors

## Next Steps

1. Test the build with the new configuration
2. Remove old configuration files
3. Update CI/CD if needed
4. Document any package-specific customizations
