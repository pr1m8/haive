# Seed Intersphinx Mapping Guide

## Overview

`seed-intersphinx-mapping` is a Sphinx extension that automatically populates the `intersphinx_mapping` configuration based on your project's dependencies. This means you don't have to manually maintain mappings for all your dependencies - they're automatically discovered and configured!

## How It Works

1. **Dependency Discovery**: The extension reads your `pyproject.toml` file
2. **URL Resolution**: It finds the documentation URLs for each dependency
3. **Automatic Configuration**: It adds these mappings to your Sphinx configuration
4. **Merge with Existing**: It preserves any manually configured mappings

## Configuration

### Basic Setup

The extension is already configured in PyAutoDoc's shared configuration:

```python
# Automatically included in shared config
extensions = [
    # ... other extensions
    'seed_intersphinx_mapping',
]

# Configuration options
pkg_requirements_source = 'pyproject'  # Read from pyproject.toml
repository_root = '/path/to/project'   # Project root directory
```

### Supported Dependency Sources

- `pyproject` - Reads from `pyproject.toml` (Poetry or PEP 621)
- `setup.py` - Reads from setup.py
- `setup.cfg` - Reads from setup.cfg
- `requirements` - Reads from requirements.txt

## Benefits

### 1. Automatic Documentation Links

When you use numpy in your project:

```toml
[tool.poetry.dependencies]
numpy = "^1.24.0"
```

You can automatically reference numpy docs:

```rst
See :py:func:`numpy.array` for details.
```

### 2. Always Up-to-Date

As you add or update dependencies, the documentation links are automatically updated.

### 3. Consistent Mapping

All packages in your monorepo get the same dependency mappings automatically.

## Example Usage

### Before seed-intersphinx-mapping

```python
# Manual configuration in conf.py
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'requests': ('https://requests.readthedocs.io/en/latest/', None),
    # ... manually maintain for each dependency
}
```

### After seed-intersphinx-mapping

```python
# Just configure the extension
extensions = ['seed_intersphinx_mapping']
pkg_requirements_source = 'pyproject'

# All dependencies are automatically mapped!
```

## How PyAutoDoc Uses It

In PyAutoDoc, seed-intersphinx-mapping is integrated into the shared configuration system:

1. **Shared Config** (`shared_config.py`):
   - Automatically enabled for all packages
   - Reads from each package's `pyproject.toml`
   - Merges with custom mappings

2. **Package Level**:
   - Each package gets mappings for its dependencies
   - Cross-package references work automatically
   - No manual configuration needed

3. **Root Documentation**:
   - Gets mappings for all monorepo dependencies
   - Can reference any package's dependencies

## Debugging

### Check Generated Mappings

```python
# In your conf.py or a test script
def print_intersphinx_mappings(app, config):
    print("Generated intersphinx mappings:")
    for name, (url, inv) in config.intersphinx_mapping.items():
        print(f"  {name}: {url}")

def setup(app):
    app.connect('config-inited', print_intersphinx_mappings)
```

### Test Script

```bash
# Run the test script to see mappings
python scripts/test-intersphinx-seed.py
```

### Common Issues

1. **Missing Mappings**:
   - Ensure dependency is in pyproject.toml
   - Check if package has public docs
   - Some packages may not have sphinx docs

2. **Wrong URLs**:
   - The extension uses a database of known URLs
   - You can override with manual mapping

3. **Performance**:
   - First build may be slower (fetching URLs)
   - Subsequent builds use cached data

## Manual Overrides

You can still manually configure mappings:

```python
# Manual mappings take precedence
intersphinx_mapping = {
    'special-package': ('https://custom-url.com/docs/', None),
}

# seed-intersphinx-mapping will add others automatically
```

## Supported Packages

The extension has built-in support for many popular packages:

- Scientific: numpy, scipy, pandas, matplotlib
- Web: django, flask, requests, fastapi
- Data: sqlalchemy, pydantic, marshmallow
- ML: scikit-learn, tensorflow, pytorch
- Testing: pytest, unittest, mock
- And many more...

## Integration with CI/CD

```yaml
# GitHub Actions example
- name: Build Documentation
  run: |
    # seed-intersphinx-mapping will read dependencies
    # and configure mappings automatically
    python scripts/build-monorepo-docs.py
```

## Best Practices

1. **Keep Dependencies Updated**: The extension uses the declared version ranges
2. **Use Standard Names**: Use PyPI package names in dependencies
3. **Test Links**: Periodically verify generated cross-references work
4. **Cache in CI**: Cache the intersphinx inventory files for faster builds

## Example Output

When building with seed-intersphinx-mapping:

```
Loading intersphinx inventory from https://docs.python.org/3/objects.inv...
Loading intersphinx inventory from https://numpy.org/doc/stable/objects.inv...
Loading intersphinx inventory from https://pandas.pydata.org/docs/objects.inv...
[seed_intersphinx_mapping] Added 15 mappings from pyproject.toml
```

## Limitations

1. Only works with packages that have Sphinx documentation
2. Requires internet connection for first fetch
3. Some packages may have non-standard documentation URLs
4. Private packages need manual configuration

## Conclusion

`seed-intersphinx-mapping` eliminates the tedious task of maintaining intersphinx mappings manually. In PyAutoDoc, it's seamlessly integrated to provide automatic cross-references for all your dependencies across the entire monorepo.
