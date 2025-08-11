# Documentation Build Issues Analysis

**Created**: 2025-08-06 19:47:26
**Purpose**: Analysis of current documentation build problems and solutions

## 🚨 Current Issues in `docs/build/html/`

### 1. Excessive Directory Nesting
**Problem**: AutoAPI is creating deeply nested directories for every module
```
api/src/haive/agents/agent/index.html
api/src/haive/agents/archive/
api/src/haive/agents/chain/index.html
... (hundreds more)
```

**Root Cause**: AutoAPI is documenting EVERYTHING including:
- Archive folders
- Experiments
- Internal modules
- Test utilities
- Migration files

### 2. Module Path Prefix Issue
**Problem**: All modules have `src.` prefix
- Expected: `haive.agents.simple`
- Actual: `src.haive.agents.simple`

**Root Cause**: AutoAPI directories point to `src/` folders:
```python
autoapi_dirs = [
    str(packages_dir / "haive-core/src"),  # This includes 'src' in module path
]
```

### 3. Performance Degradation
**Problem**: Documentation build is slow and output is massive
- Thousands of HTML files generated
- Each trivial module gets its own page
- Browser struggles to load the documentation

## 🔧 Recommended Solutions

### Solution 1: Fix Module Paths
```python
# In conf.py, add custom AutoAPI mapping:
def autoapi_skip_member(app, what, name, obj, skip, options):
    # Fix module names by removing 'src.' prefix
    if hasattr(obj, 'full_name') and obj.full_name.startswith('src.'):
        obj.full_name = obj.full_name[4:]  # Remove 'src.'
    return skip
```

### Solution 2: Aggressive Filtering
```python
# Add to conf.py:
autoapi_ignore = [
    # Test files
    "*/tests/*",
    "*/test_*",
    "*/*_test.py",
    
    # Internal/private modules
    "*/_*",
    "*/internal/*",
    
    # Archive and experiments
    "*/archive/*",
    "*/experiments/*",
    "*/deprecated/*",
    
    # Specific problematic modules
    "*/memory_reorganized/*",
    "*/memory_v2/*",
    "*/ltm/*",  # Long term memory experiments
    
    # Game-specific implementations (keep only base)
    "*/games/*/agents/*",  # Keep game base, skip agent implementations
    
    # MCP experiments
    "*/mcp/experiments/*",
    "*/mcp/*_mcp_*",  # Skip redundant MCP variations
    
    # Dataflow internals
    "*/dataflow/internal_*",
    "*/dataflow/bin/*",
]
```

### Solution 3: Optimize Page Generation
```python
# Reduce number of generated pages:
autoapi_own_page_level = "class"  # Only classes get own pages, not functions
autoapi_keep_files = False  # Don't keep .rst files after build
autoapi_generate_api_docs = True
autoapi_add_toctree_entry = True

# Further limit what gets documented:
autoapi_options = [
    "members",
    "show-inheritance",
    # Remove these to reduce output:
    # "undoc-members",  # Don't document undocumented members
    # "imported-members",  # Don't document imported items
]
```

### Solution 4: Package-Specific Builds
```bash
# Build one package at a time:
SPHINX_PACKAGES=haive-core poetry run sphinx-build -b html docs/source docs/build/html-core
SPHINX_PACKAGES=haive-agents poetry run sphinx-build -b html docs/source docs/build/html-agents

# Then combine or link them
```

## 📊 Expected Results

### Before Optimization
- Build time: 10+ minutes
- Output size: 500MB+
- HTML files: 5000+
- Navigation: Unusable

### After Optimization
- Build time: 2-3 minutes
- Output size: 50MB
- HTML files: 500-1000
- Navigation: Clean and usable

## 🎯 Implementation Priority

1. **High Priority**: Fix module path prefix issue
2. **High Priority**: Add ignore patterns for archives/experiments
3. **Medium Priority**: Optimize page generation settings
4. **Low Priority**: Implement package-specific builds

## 📝 Testing Checklist

- [ ] Module paths no longer have `src.` prefix
- [ ] Archive/experiment folders are excluded
- [ ] Build completes in under 5 minutes
- [ ] Documentation is navigable in browser
- [ ] Core API documentation is complete
- [ ] No duplicate or redundant pages

## 🔗 References

- **AutoAPI Guide**: `@project_docs/guides/sphinx_autoapi_comprehensive_guide.md`
- **Sphinx Config**: `@docs/source/conf.py`
- **Build Scripts**: `@scripts/maintenance/docs/`

---

**Note**: These solutions should significantly reduce the documentation build size and improve usability while maintaining comprehensive API documentation for the important modules.