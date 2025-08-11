# Sphinx Tippy Extension Troubleshooting Guide

## Overview

The `sphinx_tippy` extension provides rich tooltips for Sphinx documentation but can sometimes encounter issues during the build process.

## Common Issues

### KeyError: None Issue

**Error Message:**
```
KeyError: None
File "sphinx_tippy.py", line 685, in write_tippy_props_page
tippy_page_data[refpage]["id_to_html"][None], relfolder
```

**Root Cause:**
- The extension tries to process HTML references that resolve to `None`
- Usually occurs when cross-references fail to resolve properly
- Can happen with certain theme/extension combinations

**Solution Applied in conf.py:**
```python
# Conservative configuration to avoid KeyError(None) issues
tippy_enable_doitips = False  # Known to cause KeyError with None values
tippy_enable_wikitips = False  # Conservative - disable unless needed
tippy_enable_rtdtips = True   # Enable RTD tooltips (generally stable)
```

## Configuration Options

### Environment Variables

- `SPHINX_INCLUDE_MCP_DOCS=true` - Enable MCP server documentation
- `SPHINX_MCP_FORMAT=rst|md` - Choose documentation format (default: rst)

### Extension Configuration

```python
# Safe sphinx_tippy configuration
tippy_enable_mathjax = False      # Avoid conflicts
tippy_enable_doitips = False      # Disable problematic DOI tips  
tippy_enable_wikitips = False     # Conservative approach
tippy_enable_rtdtips = True       # Generally stable
```

## Fallback Strategy

The configuration includes automatic fallback:

1. **Try Configuration**: Attempt to configure sphinx_tippy with safe settings
2. **Log Debug Info**: Provide detailed logging for troubleshooting
3. **Auto-Remove on Failure**: If configuration fails, remove extension and continue build

## Testing the Fix

```bash
# Test with MCP docs disabled (default)
poetry run sphinx-build -b html docs/source docs/build/html

# Test with MCP docs enabled
SPHINX_INCLUDE_MCP_DOCS=true poetry run sphinx-build -b html docs/source docs/build/html

# Test with markdown format
SPHINX_INCLUDE_MCP_DOCS=true SPHINX_MCP_FORMAT=md poetry run sphinx-build -b html docs/source docs/build/html
```

## Alternative Solutions

If issues persist:

1. **Disable Extension**: Remove `sphinx_tippy` from extensions list temporarily
2. **Update Extension**: Check for newer version of sphinx_tippy
3. **Theme Compatibility**: Test with different Sphinx themes
4. **Report Bug**: Submit issue to sphinx_tippy GitHub repository

## Integration with Haive Documentation

This fix is integrated into the main Sphinx configuration at:
- `docs/source/conf.py` - Main configuration with safe fallback
- Automatic logging provides build-time feedback
- MCP documentation is now optional and disabled by default