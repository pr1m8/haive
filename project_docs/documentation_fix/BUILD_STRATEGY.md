# Incremental Build Strategy

**Purpose**: Step-by-step approach to fix documentation build issues

## Overview

Instead of trying to fix everything at once, we'll build incrementally, fixing issues at each stage.

## Phase 1: Minimal Working Build

### Goal

- Zero errors
- Basic Furo theme working
- No AutoAPI

### Configuration

```python
# Minimal conf.py
project = "Haive"
extensions = ["myst_parser"]
html_theme = "furo"
exclude_patterns = ["_build", "**/__pycache__"]
```

### Validation

- Build completes without errors
- Basic pages render
- CSS layout correct

## Phase 2: Add Core Package

### Goal

- Document haive-core only
- Fix import issues
- Establish patterns

### Configuration Changes

```python
# Add to conf.py
extensions.append("autoapi.extension")

# Just core
autoapi_dirs = ["../../packages/haive-core/src/haive/core"]
autoapi_ignore = [
    "**/test*",
    "**/example*",
    "**/deprecated/**",
]

# Add to path
sys.path.insert(0, "../../packages/haive-core/src")
```

### Expected Issues

- Import errors for dependencies
- Some cross-references fail
- ~500 errors (down from 6800)

### Fixes

1. Add missing dependencies to path
2. Fix circular imports
3. Update ignore patterns

## Phase 3: Add Agents Package

### Goal

- Add haive-agents documentation
- Handle complex dependencies
- Reduce supervisor noise

### Configuration Changes

```python
# Add agents
autoapi_dirs.append("../../packages/haive-agents/src/haive/agents")

# More specific ignores
autoapi_ignore.extend([
    "**/supervisor/**",  # Too many variants
    "**/archive/**",
    "**/old/**",
])

# Add to path
sys.path.insert(0, "../../packages/haive-agents/src")
```

### Expected Issues

- Many supervisor variants
- Test file processing
- Cross-package references

### Fixes

1. Aggressive supervisor filtering
2. Fix agent base imports
3. Handle circular dependencies

## Phase 4: Add Remaining Packages

### Goal

- Complete documentation
- All packages included
- Minimal warnings

### Configuration Changes

```python
# Add all packages
for package in ["haive-tools", "haive-games", "haive-dataflow", "haive-mcp"]:
    autoapi_dirs.append(f"../../packages/{package}/src/haive")
    sys.path.insert(0, f"../../packages/{package}/src")
```

### Expected Issues

- Tool dependencies
- Game asset references
- MCP server configs

### Fixes

1. Package-specific ignores
2. Dependency resolution
3. Asset handling

## Phase 5: Polish and Optimize

### Goal

- < 100 warnings
- Fast builds
- Beautiful output

### Optimizations

1. **AutoAPI Caching**

   ```python
   autoapi_keep_files = True
   ```

2. **Parallel Building**

   ```python
   # In noxfile.py
   session.run("sphinx-build", "-j", "auto")
   ```

3. **CSS Minimization**
   - Single custom CSS file
   - Furo variables only
   - Remove unused styles

## Build Validation Checklist

### After Each Phase

- [ ] Error count decreased
- [ ] HTML files generated increased
- [ ] No new CSS issues
- [ ] Import errors resolved
- [ ] Build time acceptable

### Final Validation

- [ ] < 100 warnings total
- [ ] 0 errors
- [ ] 500+ HTML files
- [ ] All packages documented
- [ ] Cross-references work
- [ ] Search works
- [ ] Mobile responsive

## Debugging Tools

### 1. Build with Verbose Output

```bash
sphinx-build -vvv -b html docs/source docs/build/html
```

### 2. Check Import Issues

```python
# Test script
import sys
sys.path.insert(0, "packages/haive-core/src")
import haive.core
print("Success!")
```

### 3. AutoAPI Debugging

```python
# In conf.py
autoapi_keep_files = True  # Keep generated RST
```

### 4. CSS Debugging

```css
/* Add to custom CSS */
.debug * {
  border: 1px solid red !important;
}
```

## Common Pitfalls to Avoid

1. **Don't Fix Everything at Once**
   - Leads to confusion
   - Hard to track progress
   - Difficult to debug

2. **Don't Ignore Warnings**
   - They become errors later
   - Indicate real problems
   - Affect output quality

3. **Don't Fight the Theme**
   - Work with Furo's system
   - Use CSS variables
   - Avoid !important

4. **Don't Process Everything**
   - Use ignore patterns
   - Filter test files
   - Skip deprecated code

## Success Metrics by Phase

### Phase 1

- Errors: 0
- Warnings: < 10
- HTML files: 5-10
- Build time: < 10 seconds

### Phase 2

- Errors: < 500
- Warnings: < 500
- HTML files: 50-100
- Build time: < 30 seconds

### Phase 3

- Errors: < 100
- Warnings: < 1000
- HTML files: 200-300
- Build time: < 60 seconds

### Phase 4

- Errors: 0
- Warnings: < 500
- HTML files: 400-500
- Build time: < 90 seconds

### Phase 5

- Errors: 0
- Warnings: < 100
- HTML files: 500+
- Build time: < 120 seconds
