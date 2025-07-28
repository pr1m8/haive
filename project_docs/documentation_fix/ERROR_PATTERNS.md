# Common Error Patterns in Documentation Build

**Purpose**: Catalog of error patterns and their solutions

## Import-Related Errors

### Pattern 1: Module Not Found

```
WARNING: Failed to import haive.agents.supervisor
ModuleNotFoundError: No module named 'haive.agents.supervisor'
```

**Cause**: Module path not in sys.path or circular import
**Solution**:

- Ensure src directory is in sys.path
- Check for circular imports
- Verify **init**.py exists

### Pattern 2: Attribute Import Error

```
WARNING: Failed to import module.submodule
AttributeError: module 'haive.core' has no attribute 'engine'
```

**Cause**: Incomplete imports in **init**.py
**Solution**:

- Check **init**.py exports
- Use explicit imports
- Fix import order

### Pattern 3: Circular Import

```
ImportError: cannot import name 'Agent' from partially initialized module
```

**Cause**: Modules importing each other
**Solution**:

- Restructure imports
- Use TYPE_CHECKING imports
- Move shared code to base module

## AutoAPI-Specific Errors

### Pattern 4: Object Not in Registry

```
KeyError: 'haive.agents.base.agent.Agent'
```

**Cause**: AutoAPI can't find object in its registry
**Solution**:

- Check autoapi_dirs configuration
- Verify module can be imported
- Fix namespace package setup

### Pattern 5: Duplicate Object

```
WARNING: Duplicate object description of haive.core.Agent
```

**Cause**: Same object imported multiple ways
**Solution**:

- Use consistent import paths
- Check for re-exports
- Fix **all** lists

### Pattern 6: Invalid Syntax in Docstring

```
WARNING: Error in "py:class" directive
```

**Cause**: Malformed docstring or type annotation
**Solution**:

- Validate docstring format
- Check for special characters
- Use proper RST syntax

## CSS/Theme Errors

### Pattern 7: CSS Variable Not Defined

```
WARNING: CSS variable --sidebar-width not found
```

**Cause**: Using undefined CSS variables
**Solution**:

- Define in light_css_variables
- Use Furo's documented variables
- Check variable names

### Pattern 8: Static File Not Found

```
WARNING: static file not found: 'haive-enhanced.css'
```

**Cause**: File not in \_static directory
**Solution**:

- Check html_static_path
- Verify file exists
- Use correct filename

## Configuration Errors

### Pattern 9: Extension Load Failure

```
WARNING: extension 'sphinx_tabs' has no setup() function
```

**Cause**: Extension not installed or wrong name
**Solution**:

- Install missing extension
- Check extension name
- Remove if not needed

### Pattern 10: Event Handler Error

```
WARNING: Unknown event name: autoapi-skip-member
```

**Cause**: Event doesn't exist when handler registered
**Solution**:

- Check if extension loaded
- Use conditional registration
- Verify event name

## File Processing Errors

### Pattern 11: Encoding Error

```
UnicodeDecodeError: 'utf-8' codec can't decode byte
```

**Cause**: Non-UTF8 file in source
**Solution**:

- Add to exclude_patterns
- Fix file encoding
- Use autoapi_ignore

### Pattern 12: File Too Large

```
WARNING: Document exceeds maximum size
```

**Cause**: Generated file too large
**Solution**:

- Split large modules
- Reduce autoapi verbosity
- Exclude problematic files

## Namespace Package Errors

### Pattern 13: Namespace Not Found

```
WARNING: No module named 'haive'
```

**Cause**: Namespace package not properly configured
**Solution**:

- Add src to sys.path
- Use autoapi_python_use_implicit_namespaces
- Check PEP 420 compliance

### Pattern 14: Wrong Module Path

```
WARNING: src.haive.agents referenced but not found
```

**Cause**: AutoAPI including 'src' in module path
**Solution**:

- Point autoapi_dirs correctly
- Add src directories to sys.path
- Use proper namespace configuration

## Quick Fixes Reference

### For Import Errors

```python
# In conf.py
for package in packages:
    src_path = package / "src"
    sys.path.insert(0, str(src_path))
```

### For AutoAPI Errors

```python
autoapi_python_use_implicit_namespaces = True
autoapi_ignore = ["**/test*", "**/example*"]
```

### For CSS Errors

```python
html_theme_options = {
    "light_css_variables": {
        # Use documented variables only
    }
}
```

### For Extension Errors

```python
if "autoapi.extension" in app.config.extensions:
    app.connect("autoapi-skip-member", handler)
```
