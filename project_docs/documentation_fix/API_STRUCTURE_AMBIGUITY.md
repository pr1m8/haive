# API Structure Ambiguity Analysis

**Created**: 2025-01-27
**Issue**: AutoAPI generating confusing nested structure

## The Problem

Looking at `/docs/source/api/`, we see AutoAPI has generated:

```
api/
├── haive/
│   ├── agents/
│   │   ├── base/
│   │   │   ├── agent_structured_output_mixin/
│   │   │   │   └── index.rst
│   │   │   ├── agent_with_token_tracking/
│   │   │   │   └── index.rst
│   │   │   └── ... (hundreds more)
│   └── index.rst
└── index.rst
```

## Ambiguity Issues

### 1. **Redundant Nesting**

- We have `api/haive/agents/` when imports are just `haive.agents`
- Creates confusion: is it `api.haive.agents` or `haive.agents`?

### 2. **Excessive Directories**

- Every single module gets its own directory with `index.rst`
- Results in hundreds of directories
- Makes navigation extremely difficult

### 3. **Path Mismatch**

- Source: `packages/haive-agents/src/haive/agents/base/agent.py`
- Generated: `api/haive/agents/base/agent_structured_output_mixin/index.rst`
- URL becomes: `/api/haive/agents/base/agent_structured_output_mixin/`

### 4. **Module vs Package Confusion**

- Some directories represent packages (have submodules)
- Others represent single modules
- No visual distinction

## Why This Happens

### AutoAPI's Default Behavior

1. **Creates directory per module** - Even for single-file modules
2. **Preserves full namespace** - Including the `haive` prefix
3. **Uses index.rst pattern** - Following Sphinx conventions

### Configuration Issues

```python
# Current configuration
autoapi_dirs = [
    "../../packages/haive-core/src",
    "../../packages/haive-agents/src",
]
autoapi_root = "api"  # Everything goes under api/
```

This causes:

- `haive.agents.base` → `api/haive/agents/base/index.rst`
- Deep nesting under `api/`

## Better Structure Options

### Option 1: Flat API Structure

```
api/
├── haive.agents.rst
├── haive.agents.base.rst
├── haive.agents.react.rst
├── haive.core.rst
├── haive.core.engine.rst
└── index.rst
```

### Option 2: One Level Deep

```
api/
├── agents/
│   ├── index.rst
│   ├── base.rst
│   ├── react.rst
│   └── simple.rst
├── core/
│   ├── index.rst
│   ├── engine.rst
│   └── schema.rst
└── index.rst
```

### Option 3: Remove haive Prefix

```
api/
├── agents/
│   ├── base/
│   │   └── index.rst
│   └── index.rst
├── core/
│   ├── engine/
│   │   └── index.rst
│   └── index.rst
└── index.rst
```

## AutoAPI Configuration Solutions

### 1. **Custom Template Path**

```python
# Fix the output structure
autoapi_template_dir = "_templates/autoapi"

# In templates, control output structure
# _templates/autoapi/python/module.rst
```

### 2. **Flatten Structure**

```python
# Use autoapi file naming
autoapi_file_patterns = ["*.py"]
autoapi_generate_api_docs = True

# Custom naming function
def autoapi_prepare_jinja_env(jinja_env):
    def flatten_name(name):
        # haive.agents.base.Agent -> agents-base-Agent
        return name.replace("haive.", "").replace(".", "-")

    jinja_env.filters['flatten_name'] = flatten_name
```

### 3. **Post-Processing**

```python
def restructure_api_docs(app, exception):
    """Flatten the API documentation structure."""
    if exception:
        return

    # Move files from deep nesting to flatter structure
    # api/haive/agents/base/index.rst -> api/agents-base.rst
```

## Comparison with Other Projects

### Django

```
api/
├── django.rst
├── django.contrib.rst
├── django.contrib.admin.rst
└── django.db.models.rst
```

### FastAPI

```
api/
├── fastapi.rst
├── fastapi.routing.rst
├── fastapi.security.rst
└── index.rst
```

### NumPy

```
reference/
├── arrays.rst
├── routines.rst
└── index.rst
```

## Recommended Solution

### Short Term: Add Navigation Helpers

1. **Better index.rst**

   ```rst
   API Reference
   =============

   Quick Links
   -----------

   - :doc:`Agents <haive/agents/index>`
   - :doc:`Core <haive/core/index>`
   - :doc:`Tools <haive/tools/index>`
   ```

2. **Breadcrumbs** in templates
3. **Search functionality** emphasized

### Long Term: Custom Templates

1. Create custom AutoAPI templates
2. Flatten the structure
3. Remove redundant nesting
4. Better URLs

## Impact on Users

### Current Problems

- URLs like: `/api/haive/agents/base/agent_structured_output_mixin/`
- Deep navigation required
- Confusing hierarchy
- Poor SEO

### With Fixes

- URLs like: `/api/agents/base/`
- Clear navigation
- Better discoverability
- Improved user experience

## Implementation Priority

1. **Document the issue** ✓ (this file)
2. **Test custom templates** - Next step
3. **Create flatter structure** - Medium term
4. **Consider alternatives** - If AutoAPI can't be fixed

## Alternative: Manual API Docs

If AutoAPI continues to be problematic:

```python
# Use sphinx.ext.autosummary instead
extensions = [
    "sphinx.ext.autosummary",
    "sphinx.ext.autodoc",
]

# Create manual structure
autosummary_generate = True
```

This gives more control over structure but requires more maintenance.
