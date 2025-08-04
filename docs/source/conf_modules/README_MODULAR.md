# Modular Documentation Build System

This directory contains the modular documentation build system for Haive, which allows building package-specific documentation with customized extension profiles.

## Overview

The modular build system provides:

- **Package-specific builds**: Build docs for individual packages (core, agents, tools, etc.)
- **Extension profiles**: Three levels of extensions (minimal, standard, full)
- **Performance optimization**: Only load necessary extensions for each package
- **Rich logging**: Visual feedback during builds using rich library
- **Incremental builds**: Start minimal and add extensions as needed

## Components

### 1. `package_configs.py`
Defines extension profiles for each package:
- **Minimal**: Essential extensions only (fastest builds)
- **Standard**: Commonly used extensions (recommended)
- **Full**: All relevant extensions (comprehensive)

### 2. `modular_builder.py`
The build logic that:
- Loads appropriate extensions for a package/profile
- Applies configurations from `extension_configs.py`
- Generates Sphinx configuration
- Provides build statistics and logging

### 3. `noxfiles/session_docs_modular.py`
Nox sessions for building documentation:
- `docs-build-package`: Build specific package with profile
- `docs-test-modular`: Test the modular system
- `docs-list-profiles`: List all available profiles
- `docs-quick`: Quick minimal builds for development
- `docs-compare-profiles`: Compare all profiles for a package

## Usage

### Build Documentation for a Package

```bash
# Build with standard profile (recommended)
nox -s docs-build-package-agents-standard

# Build with minimal profile (fastest)
nox -s docs-build-package-core-minimal

# Build with full profile (all features)
nox -s docs-build-package-tools-full
```

### Quick Development Builds

```bash
# Quick build for agents package
nox -s docs-quick-agents

# Quick build for core package
nox -s docs-quick-core
```

### Compare Profiles

```bash
# Build agents package with all three profiles
nox -s docs-compare-profiles-agents
```

### List Available Profiles

```bash
# Show all packages and their extension counts
nox -s docs-list-profiles
```

### Test the System

```bash
# Run comprehensive tests
nox -s docs-test-modular

# Or use the test script directly
python scripts/test_modular_docs.py
```

## Extension Profiles

### Core Package
- **Minimal** (8 extensions): Basic API documentation
- **Standard** (14 extensions): + diagrams, Pydantic support
- **Full** (20 extensions): + testing, development tools

### Agents Package
- **Minimal** (8 extensions): Basic API documentation
- **Standard** (17 extensions): + tabs, toggles, diagrams
- **Full** (23 extensions): + live examples, tooltips

### Tools Package
- **Minimal** (7 extensions): Basic API documentation
- **Standard** (13 extensions): + CLI docs, HTTP domain
- **Full** (17 extensions): + OpenAPI, command examples

### Games Package
- **Minimal** (7 extensions): Basic API documentation
- **Standard** (13 extensions): + images, panels
- **Full** (17 extensions): + videos, charts

### MCP Package
- **Minimal** (7 extensions): Basic API documentation
- **Standard** (13 extensions): + HTTP/OpenAPI, JSON schemas
- **Full** (16 extensions): + MCP-specific tools

### Dataflow Package
- **Minimal** (7 extensions): Basic API documentation
- **Standard** (13 extensions): + flow diagrams
- **Full** (16 extensions): + advanced diagrams

### Prebuilt Package
- **Minimal** (8 extensions): Basic API documentation
- **Standard** (14 extensions): + tabs, examples
- **Full** (17 extensions): + galleries, live demos

## Customization

### Adding Extensions to a Profile

Edit `package_configs.py`:

```python
def get_haive_agents_profile() -> ExtensionProfile:
    profile = ExtensionProfile("haive-agents")
    
    # Add to minimal profile
    profile._minimal = get_core_minimal_extensions() + [
        "your_essential_extension",
    ]
    
    # Add to standard profile
    profile._standard = [
        "your_standard_extension",
    ]
    
    # Add to full profile
    profile._full = [
        "your_advanced_extension",
    ]
    
    return profile
```

### Creating a New Package Profile

Add a new function in `package_configs.py`:

```python
def get_haive_newpackage_profile() -> ExtensionProfile:
    profile = ExtensionProfile("haive-newpackage")
    
    profile._minimal = get_core_minimal_extensions()
    profile._standard = ["sphinx_design", "sphinx_copybutton"]
    profile._full = ["sphinx_examples", "sphinx_exec_directive"]
    
    return profile

# Don't forget to add to PACKAGE_PROFILES dict
PACKAGE_PROFILES["newpackage"] = get_haive_newpackage_profile()
```

## Performance Considerations

1. **Use minimal profile** during development for fastest builds
2. **Use standard profile** for production documentation
3. **Use full profile** only when all features are needed
4. **Extension loading** is validated - missing extensions are skipped

## Troubleshooting

### Extension Not Available
If you see warnings about extensions not being available:
1. Install the extension: `pip install sphinx-extension-name`
2. Or remove it from the profile if not needed

### Build Failures
1. Check the build output for specific errors
2. Try with minimal profile first
3. Gradually add extensions to identify problematic ones

### Import Errors
Ensure you're running from the project root or that PYTHONPATH includes the conf_modules directory.

## Future Enhancements

1. **Caching**: Cache built configurations for faster rebuilds
2. **Dependency resolution**: Automatically install required extensions
3. **Profile inheritance**: Base profiles that others extend
4. **Dynamic profiles**: Runtime profile selection based on content
5. **Multi-package builds**: Build multiple packages in one command