# Namespace Monorepo Documentation Best Practices

**Created**: 2025-01-27
**Purpose**: Comprehensive guide for documenting Python namespace monorepos

## The Challenge

Documenting a namespace monorepo like Haive presents unique challenges:

1. **Multiple packages** sharing a namespace (`haive`)
2. **Src layout** adding complexity
3. **Import paths** that don't match file paths
4. **Tool limitations** - Sphinx/AutoAPI designed for single packages

## Industry Best Practices (2024)

### 1. **Unified Documentation Site**

**Recommendation**: Single documentation site for entire monorepo

**Rationale**:

- Better discoverability
- Unified search
- Cross-package references
- Single source of truth

**Anti-pattern**: Creating separate docs for each package leads to fragmentation

### 2. **Documentation Structure**

```
docs/
├── source/
│   ├── index.rst                 # Landing page
│   ├── getting-started/          # Manual guides
│   │   ├── installation.rst
│   │   └── quickstart.rst
│   ├── tutorials/                # Hand-written tutorials
│   │   ├── basic-agent.rst
│   │   └── multi-agent.rst
│   ├── guides/                   # How-to guides
│   │   ├── building-agents.rst
│   │   └── custom-tools.rst
│   ├── api/                      # Generated API docs
│   │   ├── agents.rst
│   │   ├── core.rst
│   │   └── tools.rst
│   └── reference/                # Architecture, design docs
│       ├── architecture.rst
│       └── patterns.rst
```

### 3. **Handling Namespace Packages**

#### Path Configuration

```python
# conf.py - CRITICAL for namespace packages
import sys
from pathlib import Path

# Add ALL package src directories to sys.path
packages_dir = Path(__file__).parent.parent.parent / "packages"
for package in ["haive-core", "haive-agents", "haive-tools"]:
    src_path = packages_dir / package / "src"
    if src_path.exists():
        sys.path.insert(0, str(src_path))
```

#### AutoAPI Configuration

```python
# Option A: Point to namespace directories
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src" / "haive"),
    str(packages_dir / "haive-agents" / "src" / "haive"),
]

# Option B: Point to src with namespace support
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src"),
    str(packages_dir / "haive-agents" / "src"),
]
autoapi_python_use_implicit_namespaces = True
```

### 4. **Modern Tool Alternatives**

#### Sphinx Collections (Recommended for Monorepos)

```python
# Better monorepo support
extensions = ["sphinxcontrib.collections"]

collections = {
    "haive-agents": {
        "driver": "symlink",
        "source": "../packages/haive-agents/docs",
        "target": "agents"
    }
}
```

#### Alternative Documentation Tools

1. **MkDocs Material + mkdocstrings**
   - Better monorepo support
   - Easier configuration
   - Modern UI

2. **pdoc3**
   - Simpler setup
   - Good namespace handling
   - Less customizable

3. **Pydoctor**
   - Handles complex codebases
   - Good for large projects
   - Twisted/Zope heritage

### 5. **Import Path Resolution**

**Problem**: AutoAPI generates paths with 'src' prefix

**Solutions**:

1. **Custom Templates**

   ```python
   autoapi_template_dir = "_templates/autoapi"

   # In template, strip src prefix
   {% set name = obj.name.replace('src.', '') %}
   ```

2. **Post-Processing**

   ```python
   def fix_autoapi_paths(app, exception):
       """Remove src. prefix from generated docs."""
       # Implementation to fix paths
   ```

3. **Jinja Filters**
   ```python
   def prepare_autoapi_jinja_env(jinja_env):
       def fix_module_name(name):
           return name.replace('src.', '')
       jinja_env.filters['fix_module_name'] = fix_module_name
   ```

## Haive-Specific Recommendations

### 1. **Incremental Approach**

```python
# Phase 1: Core only
autoapi_dirs = [
    str(packages_dir / "haive-core" / "src" / "haive" / "core"),
]

# Phase 2: Add agents
autoapi_dirs.append(
    str(packages_dir / "haive-agents" / "src" / "haive" / "agents"),
)

# Phase 3: Complete coverage
# Add remaining packages
```

### 2. **Aggressive Filtering**

```python
autoapi_ignore = [
    # Test files
    "**/test_*.py",
    "**/tests/**",

    # Development files
    "**/examples/**",
    "**/scripts/**",
    "**/debug*.py",

    # Known problematic directories
    "**/supervisor/**",  # Too many variants
    "**/archive/**",
    "**/deprecated/**",
]
```

### 3. **Structure Simplification**

Instead of deep nesting:

```
api/haive/agents/base/agent_structured_output_mixin/index.rst
```

Aim for:

```
api/agents-base.rst
```

### 4. **Navigation Aids**

```rst
.. Custom index.rst
API Reference
=============

By Package
----------

.. toctree::
   :maxdepth: 2

   agents/index
   core/index
   tools/index

By Functionality
-----------------

**Agents**
- :doc:`Simple Agents <agents/simple>`
- :doc:`ReAct Agents <agents/react>`
- :doc:`Multi-Agent Systems <agents/multi>`

**Core Components**
- :doc:`Engine <core/engine>`
- :doc:`Schema <core/schema>`
- :doc:`Graph <core/graph>`
```

## Common Pitfalls to Avoid

### 1. **Fighting the Tools**

- Don't try to make Sphinx/AutoAPI do something they weren't designed for
- Consider alternatives if the fight is too hard

### 2. **Over-Documentation**

- Not every internal module needs docs
- Focus on public API
- Use `__all__` to control exports

### 3. **Ignoring Performance**

- Large monorepos can have slow builds
- Use incremental builds
- Consider splitting API generation

### 4. **Poor Organization**

- Keep narrative docs separate from API
- Use clear categories
- Provide multiple navigation paths

## Success Metrics

1. **Build Performance**
   - Full build < 2 minutes
   - Incremental build < 30 seconds

2. **Documentation Quality**
   - All public APIs documented
   - Cross-references work
   - Search returns relevant results

3. **User Experience**
   - Easy to find information
   - Clear navigation
   - Mobile-friendly

## Decision Framework

### When to Use Sphinx + AutoAPI

✅ **Good fit when**:

- Single package or simple structure
- Standard layout
- Well-established project

❌ **Poor fit when**:

- Complex monorepo
- Many namespace packages
- Need rapid iteration

### When to Consider Alternatives

✅ **MkDocs when**:

- Need better monorepo support
- Want modern UI
- Markdown-first approach

✅ **Custom Solution when**:

- Unique requirements
- Full control needed
- Resources available

## Final Recommendations for Haive

1. **Short Term**: Fix current Sphinx setup
   - Implement phases from documentation
   - Use aggressive filtering
   - Simplify structure where possible

2. **Medium Term**: Evaluate alternatives
   - Test MkDocs Material
   - Consider Sphinx Collections
   - Assess migration effort

3. **Long Term**: Optimize for users
   - Focus on use cases
   - Improve search
   - Add interactive examples

## Resources

- [Sphinx Collections](https://github.com/useblocks/sphinx-collections)
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/)
- [mkdocstrings](https://mkdocstrings.github.io/)
- [Sphinx Multiproject](https://sphinx-multiproject.readthedocs.io/)
- [Real Python - Namespace Packages](https://realpython.com/python-namespace-package/)
