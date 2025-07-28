# AutoAPI Configuration Strategy for Namespace Packages

**Purpose**: Comprehensive guide for configuring AutoAPI with Haive's namespace structure

## The Challenge

Haive uses a namespaced monorepo structure:

```
packages/
├── haive-core/
│   └── src/
│       └── haive/
│           ├── __init__.py  # Namespace package
│           └── core/
│               ├── __init__.py
│               └── engine.py
├── haive-agents/
│   └── src/
│       └── haive/
│           ├── __init__.py  # Namespace package
│           └── agents/
│               ├── __init__.py
│               └── simple.py
```

AutoAPI must generate docs with correct import paths:

- ✅ `from haive.core.engine import Engine`
- ❌ `from src.haive.core.engine import Engine`

## Solution Approach

### 1. Path Configuration

```python
# Add src directories to Python path FIRST
packages_dir = Path(__file__).parent.parent.parent / "packages"
for package in ["haive-core", "haive-agents", "haive-tools", "haive-games"]:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))
```

### 2. AutoAPI Directory Setup

```python
# Option A: Point to namespace directories (current approach)
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src" / "haive"),
    str(packages_dir / "haive-agents" / "src" / "haive"),
]

# Option B: Point to src directories (with namespace support)
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src"),
    str(packages_dir / "haive-agents" / "src"),
]
autoapi_python_use_implicit_namespaces = True
```

### 3. Namespace Package Support

```python
# Critical for PEP 420 namespace packages
autoapi_python_use_implicit_namespaces = True

# Additional options
autoapi_options = [
    "members",
    "show-inheritance",
    "show-module-summary",
    "imported-members",  # Show imported members
]
```

## Ignore Pattern Strategy

### Current Problems

- Processing 1000s of test files
- Multiple supervisor variants
- Example and demo files
- Archive and deprecated code

### Comprehensive Ignore List

```python
autoapi_ignore = [
    # Test files
    "**/test_*.py",
    "**/tests/**",
    "**/*_test.py",
    "**/testing/**",
    "**/test/**",

    # Examples and demos
    "**/examples/**",
    "**/example_*.py",
    "**/demo*.py",
    "**/*_demo.py",
    "**/*_example.py",
    "**/showcase/**",

    # Development files
    "**/scripts/**",
    "**/.ipynb_checkpoints/**",
    "**/debug*.py",
    "**/cli.py",
    "**/*_cli.py",

    # Archive and old code
    "**/archive/**",
    "**/old/**",
    "**/deprecated/**",
    "**/legacy/**",
    "**/backup/**",

    # Specific problem directories
    "**/supervisor/**",  # 40+ variants causing noise
    "**/experimental/**",
    "**/sandbox/**",

    # Build artifacts
    "**/__pycache__/**",
    "**/*.pyc",
    "**/.pytest_cache/**",
    "**/*.egg-info/**",

    # Notebooks and data
    "**/*.ipynb",
    "**/*.json",
    "**/*.yaml",
    "**/*.yml",
]
```

## Package-Specific Configuration

### haive-core

```python
# Minimal ignores - this is the foundation
autoapi_ignore_for_core = [
    "**/test*",
    "**/example*",
]
```

### haive-agents

```python
# More aggressive - lots of experimental code
autoapi_ignore_for_agents = [
    "**/supervisor/**",  # Too many variants
    "**/experimental/**",
    "**/research/**",  # If too noisy
    "**/archive/**",
]
```

### haive-tools

```python
# Tool-specific ignores
autoapi_ignore_for_tools = [
    "**/deprecated/**",
    "**/legacy/**",
    "**/vendor/**",  # Third-party code
]
```

## Debugging AutoAPI Issues

### 1. Check What's Being Processed

```python
# In conf.py
autoapi_keep_files = True  # Keeps generated RST files

# After build, check:
# docs/build/html/autoapi/
```

### 2. Test Import Paths

```python
# Test script: verify_imports.py
import sys
sys.path.insert(0, "packages/haive-core/src")
sys.path.insert(0, "packages/haive-agents/src")

try:
    from haive.core import Engine
    print("✅ haive.core imports work")
except ImportError as e:
    print(f"❌ haive.core import failed: {e}")

try:
    from haive.agents import SimpleAgent
    print("✅ haive.agents imports work")
except ImportError as e:
    print(f"❌ haive.agents import failed: {e}")
```

### 3. Check Generated Paths

Look for patterns in generated documentation:

- Correct: `haive.agents.simple.SimpleAgent`
- Wrong: `src.haive.agents.simple.SimpleAgent`
- Wrong: `agents.simple.SimpleAgent`

## Common Issues and Solutions

### Issue 1: "src" in Module Names

**Symptom**: Documentation shows `src.haive.core.Engine`
**Solution**:

- Add src to sys.path
- Point autoapi_dirs to namespace level
- Enable implicit namespaces

### Issue 2: Missing Modules

**Symptom**: Some modules not documented
**Solution**:

- Check import works manually
- Reduce ignore patterns
- Check for **init**.py issues

### Issue 3: Duplicate Entries

**Symptom**: Same class appears multiple times
**Solution**:

- Check for re-exports
- Fix **all** lists
- Use consistent import paths

### Issue 4: Import Errors

**Symptom**: "Failed to import module X"
**Solution**:

- Add dependencies to sys.path
- Fix circular imports
- Check for missing dependencies

## Best Practices

1. **Start Small**
   - Test with one package first
   - Get imports working
   - Then scale up

2. **Use Specific Ignores**
   - Target problem directories
   - Don't over-ignore
   - Document why ignored

3. **Verify Imports**
   - Test outside Sphinx first
   - Check generated paths
   - Validate cross-references

4. **Monitor Performance**
   - Track file count
   - Watch build time
   - Optimize patterns

## Performance Optimization

### 1. Reduce File Processing

```python
# Very specific patterns
autoapi_ignore = [
    # Instead of "**/test*"
    "**/test_*.py",
    "**/tests/",

    # Instead of "**/*example*"
    "**/examples/",
    "**/example_*.py",
]
```

### 2. Enable Caching

```python
# Keep generated files between builds
autoapi_keep_files = True
```

### 3. Parallel Processing

```python
# In build command
sphinx-build -j auto
```

## Validation Checklist

- [ ] All packages have src in sys.path
- [ ] Import test script passes
- [ ] No "src" in generated module names
- [ ] Reasonable file processing count
- [ ] Cross-package references work
- [ ] Build time under 2 minutes
